---
name: "azure-container-registry-cli"
description: "Use ao trabalhar com Azure Container Registry, executar comandos az acr ou enviar, importar, compilar ou limpar imagens de contêiner no Azure. Abrange registros, compilações na nuvem, ACR Tasks, autenticação, tokens, replicação geográfica e redes. Os gatilhos incluem \"az acr\", \"enviar imagem para o ACR\", \"compilar imagem no Azure\", \"autenticação do ACR\" e \"registro de contêiner\"."
---
# CLI do Azure Container Registry

Gerencie recursos do Azure Container Registry (ACR) com o grupo de comandos `az acr` da Azure CLI. `az acr` acompanha o núcleo da Azure CLI e não exige extensão. A extensão `acrtransfer` é necessária somente para fluxos automatizados de exportação/importação.

> [!NOTE]
> Esta habilidade depende da instalação e autenticação da **CLI `az`**. Neste kit, provisione o registro em Terraform (`azurerm_container_registry`, com as tags obrigatórias `project`, `environment` e `owner`) em `infra/`. Use `az acr` para tarefas operacionais, como compilar, importar, marcar e diagnosticar imagens, não como sistema de registro da infraestrutura.

## Quando usar

- "Envie nossa imagem do Spring Boot para o Azure Container Registry."
- "Compile uma imagem de contêiner no Azure sem um serviço local em segundo plano (daemon) do Docker."
- "Como permitir que o AKS baixe imagens deste registro sem usar o usuário administrador?"
- "Limpe tags antigas para reduzir o custo de armazenamento do ACR."

## Pré-requisitos

Instale a Azure CLI, entre e selecione uma assinatura:

```bash
brew install azure-cli                                     # macOS
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash     # Linux
winget install Microsoft.AzureCLI                          # Windows
az login
az account set --subscription {subscription-id}
```

## Início rápido

```bash
az acr create --resource-group {rg} --name {registry} --sku Standard          # SKU: Basic | Standard | Premium
az acr login --name {registry}                                                # autentica Docker/Podman
az acr build --registry {registry} --image app:v1 .                           # compilação na nuvem, sem Docker local
az acr import --name {registry} --source mcr.microsoft.com/hello-world:latest  # cópia no servidor
az acr repository list --name {registry} --output table
az acr repository show-tags --name {registry} --repository app --orderby time_desc
az acr check-health --name {registry} --yes                                   # diagnostica a conectividade
```

## Princípios fundamentais

- **Prefira `az acr build`/ACR Tasks** a `docker build` + `docker push` local: as compilações são executadas no Azure, funcionam sem um serviço local em segundo plano e integram-se a gatilhos.
- **Prefira `az acr import`** para mover imagens entre registros: a operação ocorre no servidor, é mais rápida e não exige armazenamento local.
- **Nunca ative o usuário administrador em produção.** Use identidades do Microsoft Entra (funções RBAC `AcrPull`/`AcrPush` ou `Container Registry Repository Reader`/`Writer` em registros com ABAC), tokens com escopo de repositório ou identidades gerenciadas.
- **Recursos exclusivos do Premium**: replicação geográfica, pontos de extremidade privados, políticas de retenção, registros conectados e conjuntos de agentes. Tokens com escopo de repositório funcionam em todas as camadas. A redundância de zona é automática nas regiões compatíveis.

## Estrutura da CLI

```text
az acr
├── create / delete / list / show / update   Ciclo de vida do registro
├── login                  Auxiliar de credenciais do Docker (ou --expose-token)
├── check-health / check-name / show-usage    Diagnóstico e cota
├── build                  Compilação de imagem na nuvem (tarefa rápida)
├── run                    Executa uma vez um comando ou tarefa com várias etapas
├── task                   ACR Tasks (gatilhos, temporizadores, registros e execuções)
├── agentpool              Conjuntos dedicados de agentes de tarefas (Premium)
├── import                 Cópia de imagem para o registro no servidor
├── repository             Lista/exibe/exclui/remove tags de repositórios e tags; bloqueia imagens
├── manifest               Metadados de manifestos, exclusão e referências OCI
├── credential             Credenciais do usuário administrador (evite em produção)
├── token / scope-map      Tokens com escopo de repositório (Premium)
├── replication            Replicação geográfica (Premium)
├── network-rule           Regras de rede IP
├── private-endpoint-connection   Aprovações do Private Link
├── config                 content-trust, retenção, exclusão reversível...
├── cache / credential-set Regras de armazenamento temporário de artefatos (pull-through cache)
├── webhook                Notificações HTTP de eventos de envio/exclusão
├── connected-registry     Registros conectados locais/IoT
└── export-pipeline / import-pipeline / pipeline-run   Extensão acrtransfer
```

## Arquivos de referência

Leia o arquivo de referência pertinente à tarefa. Cada arquivo contém a sintaxe completa dos comandos e exemplos do domínio.

| Arquivo | Quando ler | Abrange |
|---|---|---|
| [references/auth-and-security.md](references/auth-and-security.md) | Falhas de autenticação, permissões ou acesso para baixar imagens por CI/CD ou AKS | `az acr login` (incluindo `--expose-token`), funções RBAC do Entra, entidades de serviço, identidades gerenciadas, `--attach-acr` para AKS, tokens com escopo de repositório e mapas de escopo, usuário administrador e confiança no conteúdo |
| [references/build-and-tasks.md](references/build-and-tasks.md) | Compilação de imagens no Azure, automação e gatilhos de CI | `az acr build`, `az acr run`, YAML de tarefa com várias etapas, `az acr task` (gatilhos de git/imagem base/temporizador, registros e execuções) e conjuntos de agentes |
| [references/images-and-artifacts.md](references/images-and-artifacts.md) | Gerenciamento de repositórios, tags, limpeza e custo de armazenamento | `az acr import`, comandos de repositório e manifesto, remoção de tag versus exclusão, limpeza (`acr purge`), bloqueio de imagens, política de retenção, exclusão reversível, armazenamento temporário de artefatos e `show-usage` |
| [references/networking-and-geo.md](references/networking-and-geo.md) | Várias regiões, acesso privado e cenários de borda | Replicação geográfica, redundância de zona, pontos de extremidade privados, regras de rede, pontos de extremidade de dados dedicados, registros conectados e fluxos de transferência de registros |

## Modelo de saída

Forneça um plano de comandos executável que explicite o modelo de identidade:

```bash
az acr create --resource-group rg-sifap --name sifapregistry --sku Standard
az acr build --registry sifapregistry --image sifap-backend:$(git rev-parse --short HEAD) .
az acr repository show-tags --name sifapregistry --repository sifap-backend --output table
az role assignment create \
  --assignee <aks-kubelet-identity-object-id> \
  --role AcrPull \
  --scope $(az acr show --name sifapregistry --query id --output tsv)
```

Resuma o que foi feito e a postura de segurança:

```text
Registro: sifapregistry (Standard) em rg-sifap
Imagem: sifap-backend:<git-sha> compilada no Azure (sem Docker local)
Acesso: AcrPull concedido à identidade gerenciada do kubelet do AKS; usuário administrador desativado
```

## Critérios de qualidade

- [ ] A SKU do registro corresponde à necessidade (Premium somente quando forem exigidos replicação geográfica, pontos de extremidade privados ou tokens com escopo).
- [ ] Sempre que viável, as imagens são compiladas com `az acr build`/ACR Tasks, não com `docker build` + `docker push` local.
- [ ] O usuário administrador está desativado; o acesso usa uma identidade do Entra (`AcrPull`/`AcrPush`), uma identidade gerenciada ou um token com escopo de repositório.
- [ ] `az acr check-health --name {registry}` não informa erros.
- [ ] Movimentações de imagens entre registros usam `az acr import` (no servidor), não operações locais de download e envio.
- [ ] O recurso de registro está definido em Terraform em `infra/` com as tags obrigatórias `project`, `environment` e `owner`.
