# Autenticação e segurança

## Sumário

- [Autenticação individual](#autenticação-individual)
- [Funções RBAC do Microsoft Entra](#funções-rbac-do-microsoft-entra)
- [Entidades de serviço](#entidades-de-serviço)
- [Identidades gerenciadas](#identidades-gerenciadas)
- [Integração com AKS](#integração-com-aks)
- [Tokens com escopo de repositório](#tokens-com-escopo-de-repositório)
- [Usuário administrador](#usuário-administrador)
- [Confiança no conteúdo](#confiança-no-conteúdo-descontinuada)

---

## Autenticação individual

```bash
# Autenticação padrão: configura credenciais do Docker/Podman com sua identidade do az login
az acr login --name {registry}

# Sem o serviço em segundo plano do Docker: obtém um token do Entra e o envia ao docker login
LOGIN_SERVER=$(az acr show --name {registry} --query loginServer --output tsv)
az acr login --name {registry} --expose-token --query accessToken --output tsv | \
  docker login $LOGIN_SERVER --username 00000000-0000-0000-0000-000000000000 --password-stdin
```

Notas:

- Os tokens de `az acr login` são válidos por três horas. Execute novamente quando expirarem.
- Resolva o servidor de autenticação com `az acr show --name {registry} --query loginServer --output tsv` em vez de fixá-lo. Geralmente, ele é `{registry}.azurecr.io`, mas nuvens soberanas usam outros sufixos e registros com escopo de rótulo de nome de domínio recebem um sufixo de resumo criptográfico (`hash`).

## Funções RBAC do Microsoft Entra

As funções do plano de dados aplicáveis dependem do **modo de permissões de atribuição de função** do registro. Verifique-o primeiro:

```bash
az acr show --name {registry} --query roleAssignmentMode --output tsv
# LegacyRegistryPermissions  -> usar AcrPull/AcrPush/AcrDelete
# AbacRepositoryPermissions  -> usar Container Registry Repository Reader/Writer/Contributor
```

**Modo legado (RBAC Registry Permissions):**

| Função | Permissões |
|---|---|
| `AcrPull` | Baixar imagens |
| `AcrPush` | Baixar + enviar imagens |
| `AcrDelete` | Excluir imagens |
| `AcrImageSigner` | Assinar imagens (confiança no conteúdo) |
| `Contributor`/`Owner` | Gerenciamento completo do plano de controle + envio/download |

**Modo com ABAC (RBAC Registry + ABAC Repository Permissions):** `AcrPull`/`AcrPush`/`AcrDelete` **não são aceitas**, e `Owner`/`Contributor`/`Reader` concedem acesso somente ao plano de controle. Em vez disso, use:

| Função | Permissões |
|---|---|
| `Container Registry Repository Reader` | Lê imagens, tags e metadados (adicione condições ABAC para limitar o escopo aos repositórios) |
| `Container Registry Repository Writer` | Lê + grava/atualiza |
| `Container Registry Repository Contributor` | Lê + grava + exclui |
| `Container Registry Repository Catalog Lister` | Lista repositórios; atribua somente quando a identidade precisar enumerar o catálogo (por exemplo, `az acr repository list`). Não é necessária para baixar/enviar imagens de repositórios conhecidos |

```bash
# Obtém o ID do recurso de registro
ACR_ID=$(az acr show --name {registry} --query id --output tsv)

# Concede acesso para baixar imagens a usuário, grupo, entidade de serviço ou identidade gerenciada
az role assignment create --assignee {principal-id} --scope $ACR_ID --role AcrPull

# Lista quem tem acesso
az role assignment list --scope $ACR_ID --output table
```

## Entidades de serviço

Para sistemas de CI/CD que não podem usar OIDC/identidade gerenciada:

```bash
# Cria uma entidade de serviço com escopo somente para baixar imagens
ACR_ID=$(az acr show --name {registry} --query id --output tsv)
az ad sp create-for-rbac --name {sp-name} --scopes $ACR_ID --role AcrPull

# Autenticação do Docker com a entidade: envie o segredo por stdin, nunca como argumento
# (printf com uma variável entre aspas preserva exatamente espaços e caracteres glob)
printf '%s' "$SP_PASSWORD" | docker login $LOGIN_SERVER --username {appId} --password-stdin
```

Quando possível, prefira credenciais federadas (OIDC) a senhas de entidades de serviço no GitHub Actions/Azure DevOps.

## Identidades gerenciadas

Para computação do Azure (VM, App Service, Container Apps e Functions):

```bash
# Atribui uma identidade gerenciada pelo sistema e concede acesso para baixar imagens
az vm identity assign --name {vm} --resource-group {rg}
PRINCIPAL_ID=$(az vm show --name {vm} --resource-group {rg} --query identity.principalId --output tsv)
az role assignment create --assignee $PRINCIPAL_ID --scope $ACR_ID --role AcrPull
```

Depois, App Service/Container Apps baixam imagens com opções como `--assign-identity` + `--acr-identity` das próprias CLIs, sem necessidade de senha do registro.

## Integração com AKS

```bash
# Anexa durante a criação do cluster
az aks create --name {cluster} --resource-group {rg} --attach-acr {registry}

# Anexa/desanexa um cluster existente (concede AcrPull à identidade do kubelet)
az aks update --name {cluster} --resource-group {rg} --attach-acr {registry}
az aks update --name {cluster} --resource-group {rg} --detach-acr {registry}

# Valida se o cluster consegue acessar o registro
az aks check-acr --name {cluster} --resource-group {rg} --acr {registry}.azurecr.io
```

`--attach-acr` exige Owner ou User Access Administrator no registro. Para anexar entre assinaturas, passe o ID completo do recurso do ACR.

⚠️ `--attach-acr` atribui `AcrPull`, que **não é aceita em registros com ABAC** (`roleAssignmentMode` = `AbacRepositoryPermissions`). Nesses registros, atribua manualmente as funções ABAC à identidade do kubelet:

```bash
ACR_ID=$(az acr show --name {registry} --query id --output tsv)
KUBELET_ID=$(az aks show --name {cluster} --resource-group {rg} \
  --query identityProfile.kubeletidentity.objectId --output tsv)
az role assignment create --assignee $KUBELET_ID --scope $ACR_ID \
  --role "Container Registry Repository Reader"
# "Container Registry Repository Catalog Lister" NÃO é necessária para baixar imagens;
# adicione-a somente se a identidade precisar listar repositórios
```

## Tokens com escopo de repositório

Disponíveis em todas as camadas de serviço. São credenciais granulares que não usam o Entra (por exemplo, para parceiros externos ou dispositivos IoT):

```bash
# 1. Cria um mapa de escopo (ações: content/read, content/write, content/delete, metadata/read, metadata/write)
az acr scope-map create --name {scope-map} --registry {registry} \
  --repository app content/read metadata/read \
  --description "Acesso somente para baixar imagens do app"

# 2. Cria um token vinculado ao mapa de escopo
az acr token create --name {token} --registry {registry} --scope-map {scope-map}

# 3. Gera/alterna senhas (até duas, com expiração opcional)
az acr token credential generate --name {token} --registry {registry} --password1 --expiration-in-days 30

# Autenticação com o token: envie a senha por stdin, nunca como argumento
printf '%s' "$TOKEN_PWD" | docker login $LOGIN_SERVER --username {token} --password-stdin

# Desativa ou exclui
az acr token update --name {token} --registry {registry} --status disabled
az acr token delete --name {token} --registry {registry} --yes
```

## Usuário administrador

Conta única com envio/download completo em todo o registro, sem auditoria por usuário. **Mantenha-a desativada em produção**:

```bash
az acr update --name {registry} --admin-enabled false   # recomendado
az acr credential show --name {registry}                # exibe usuário/senhas (se ativado)
az acr credential renew --name {registry} --password-name password2   # alterna
```

Usos legítimos: testes locais rápidos e serviços que aceitam somente usuário/senha e não podem usar tokens.

## Confiança no conteúdo (descontinuada)

O Docker Content Trust (DCT) está sendo descontinuado: **desde 31 de maio de 2026, ele não pode ser ativado em registros novos** (nem em registros que nunca o ativaram) e será removido por completo em 31 de março de 2028. Não configure o DCT. Em vez disso, assine as imagens com **Notation (Notary Project)** e armazene as assinaturas como artefatos OCI. Consulte "Transition from Docker Content Trust to Notary Project" na documentação do ACR.

```bash
# Somente registros com DCT legado: inspeciona ou desativa a configuração existente
az acr config content-trust show --registry {registry}
az acr config content-trust update --registry {registry} --status disabled
```

Os signatários do DCT legado precisavam de `AcrImageSigner` além de `AcrPush`.
