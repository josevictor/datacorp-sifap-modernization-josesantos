# Guia de tratamento de erros

Esta referência documenta erros comuns durante a validação pré-implantação e como tratá-los.

## Princípio fundamental

**Continue em caso de falha.** Registre todos os problemas no relatório final, em vez de parar no primeiro erro. Isso oferece uma visão completa do que precisa ser corrigido.

---

## Erros de autenticação

### Sem autenticação (Azure CLI)

**Detecção:**

```text
ERROR: Please run 'az login' to setup account.
ERROR: AADSTS700082: The refresh token has expired
```

**Códigos de saída:** diferente de zero

**Tratamento:**

1. Registre o erro no relatório
2. Inclua as etapas de correção
3. Ignore os demais comandos da Azure CLI
4. Continue com as outras etapas de validação, se possível

**Entrada no relatório:**

```markdown
#### ❌ Autenticação na Azure CLI obrigatória

- **Severidade:** Erro
- **Fonte:** CLI az
- **Mensagem:** Sem autenticação na Azure CLI
- **Correção:** Execute `az login` para autenticar e depois execute novamente a validação pré-implantação
- **Documentação:** https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli
```

### Sem autenticação (azd)

**Detecção:**

```text
ERROR: not logged in, run `azd auth login` to login
```

**Tratamento:**

1. Registre o erro no relatório
2. Ignore os comandos azd
3. Sugira `azd auth login`

**Entrada no relatório:**

```markdown
#### ❌ Autenticação na Azure Developer CLI obrigatória

- **Severidade:** Erro
- **Fonte:** azd
- **Mensagem:** Sem autenticação na Azure Developer CLI
- **Correção:** Execute `azd auth login` para autenticar e depois execute novamente a validação pré-implantação
```

### Token expirado

**Detecção:**

```text
AADSTS700024: Client assertion is not within its valid time range
AADSTS50173: The provided grant has expired
```

**Tratamento:**

1. Registre o erro
2. Sugira uma nova autenticação
3. Ignore as operações do Azure

---

## Erros de permissão

### Permissões RBAC insuficientes

**Detecção:**

```text
AuthorizationFailed: The client '...' with object id '...' does not have authorization
to perform action '...' over scope '...'
```

**Tratamento:**

1. **Primeira tentativa:** tente novamente com `--validation-level ProviderNoRbac`
2. Registre a limitação de permissão no relatório
3. Se ProviderNoRbac também falhar, informe a permissão específica ausente

**Entrada no relatório:**

```markdown
#### ⚠️ Validação com permissões limitadas

- **Severidade:** Aviso
- **Fonte:** what-if
- **Mensagem:** A validação RBAC completa falhou; usando validação somente leitura
- **Detalhe:** Permissão ausente: `Microsoft.Resources/deployments/write` no escopo `/subscriptions/xxx`
- **Recomendação:** Solicite a função Contributor no grupo de recursos de destino ou verifique as permissões de implantação com a administração
```

### Grupo de recursos não encontrado

**Detecção:**

```text
ResourceGroupNotFound: Resource group 'xxx' could not be found.
```

**Tratamento:**

1. Registre no relatório
2. Sugira a criação do grupo de recursos
3. Ignore o what-if para este escopo

**Entrada no relatório:**

````markdown
#### ❌ O grupo de recursos não existe

- **Severidade:** Erro
- **Fonte:** what-if
- **Mensagem:** O grupo de recursos 'my-rg' não existe
- **Correção:** Crie o grupo de recursos antes da implantação:
  ```bash
  az group create --name my-rg --location eastus
  ```

````

### Acesso à assinatura negado

**Detecção:**

```text

SubscriptionNotFound: The subscription 'xxx' could not be found.
InvalidSubscriptionId: Subscription '...' is not valid

```

**Tratamento:**

1. Registre no relatório
2. Sugira a verificação do ID da assinatura
3. Liste as assinaturas disponíveis

---

## Erros de sintaxe do Bicep

### Erros de compilação

**Detecção:**

```text

/path/main.bicep(22,51) : Error BCP064: Found unexpected tokens
/path/main.bicep(10,5) : Error BCP018: Expected the "=" character at this location

```

**Tratamento:**

1. Analise a saída de erro para obter números de linha/coluna
2. Inclua todos os erros no relatório (não pare no primeiro)
3. Continue para o what-if (ele pode fornecer contexto adicional)

**Entrada no relatório:**

```markdown
#### ❌ Erro de sintaxe do Bicep

- **Severidade:** Erro
- **Fonte:** bicep build
- **Local:** `main.bicep:22:51`
- **Código:** BCP064
- **Mensagem:** Tokens inesperados encontrados na expressão interpolada
- **Correção:** Verifique a sintaxe de interpolação da string na linha 22
- **Documentação:** https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/diagnostics/bcp064
```

### Módulo não encontrado

**Detecção:**

```text
Error BCP091: An error occurred reading file. Could not find file '...'
Error BCP190: The module is not valid
```

**Tratamento:**

1. Registre o módulo ausente
2. Verifique se `bicep restore` é necessário
3. Verifique o caminho do módulo

### Problemas no arquivo de parâmetros

**Detecção:**

```text
Error BCP032: The value must be a compile-time constant
Error BCP035: The specified object is missing required properties
```

**Tratamento:**

1. Registre os problemas nos parâmetros
2. Indique quais parâmetros apresentam problemas
3. Sugira correções

---

## Ferramenta não instalada

### Azure CLI não encontrada

**Detecção:**

```text
'az' is not recognized as an internal or external command
az: command not found
```

**Tratamento:**

1. Registre no relatório
2. Forneça instruções de instalação.

- Se disponível, use a ferramenta MCP do Azure `extension_cli_install` para obter instruções de instalação.
- Caso contrário, procure as instruções em https://learn.microsoft.com/en-us/cli/azure/install-azure-cli.

3. Ignore os comandos az

**Entrada no relatório:**

```markdown
#### ⏭️ Azure CLI não instalada

- **Severidade:** Aviso
- **Fonte:** ambiente
- **Mensagem:** A Azure CLI (az) não está instalada ou não está no PATH
- **Correção:** Instale a Azure CLI <ADICIONE AS INSTRUÇÕES DE INSTALAÇÃO AQUI>
- **Impacto:** A validação what-if com comandos az foi ignorada
```

### Bicep CLI não encontrada

**Detecção:**

```text
'bicep' is not recognized as an internal or external command
bicep: command not found
```

**Tratamento:**

1. Registre no relatório
2. A Azure CLI pode ter o Bicep integrado; tente `az bicep build`
3. Forneça o link de instalação

**Entrada no relatório:**

```markdown
#### ⏭️ Bicep CLI não instalada

- **Severidade:** Aviso
- **Fonte:** ambiente
- **Mensagem:** A Bicep CLI não está instalada
- **Correção:** Instale a Bicep CLI: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/install
- **Impacto:** A validação de sintaxe foi ignorada; o Azure validará durante o what-if
```

### Azure Developer CLI não encontrada

**Detecção:**

```text
'azd' is not recognized as an internal or external command
azd: command not found
```

**Tratamento:**

1. Se `azure.yaml` existir, esta ferramenta será obrigatória
2. Use comandos da CLI az como alternativa, se possível
3. Registre no relatório

---

## Erros específicos de what-if

### Limites de modelos aninhados

**Detecção:**

```text
The deployment exceeded the nested template limit of 500
```

**Tratamento:**

1. Registre como aviso (não como erro)
2. Explique que os recursos afetados aparecem como "Ignore"
3. Sugira uma revisão manual

### Link de modelo sem suporte

**Detecção:**

```text
templateLink references in nested deployments won't be visible in what-if
```

**Tratamento:**

1. Registre como aviso
2. Explique a limitação
3. Os recursos serão verificados durante a implantação real

### Expressões não avaliadas

**Detecção:** propriedades que mostram nomes de funções como `[utcNow()]` em vez de valores

**Tratamento:**

1. Registre como informação
2. Explique que elas são avaliadas durante a implantação
3. Não é um erro

---

## Erros de rede

### Timeout

**Detecção:**

```text
Connection timed out
Request timed out
```

**Tratamento:**

1. Sugira uma nova tentativa
2. Verifique a conectividade de rede
3. Pode indicar problemas no serviço do Azure

### Erros de SSL/TLS

**Detecção:**

```text
SSL: CERTIFICATE_VERIFY_FAILED
unable to get local issuer certificate
```

**Tratamento:**

1. Registre no relatório
2. Pode indicar um proxy ou firewall corporativo
3. Sugira a verificação das configurações de SSL

---

## Estratégia alternativa

Quando a validação principal falhar, tente as alternativas em ordem:

```text
Provider (validação RBAC completa)
    ↓ falha com erro de permissão
ProviderNoRbac (validação sem verificar permissão de gravação)
    ↓ falha
Template (somente sintaxe estática)
    ↓ falha
Informe todas as falhas e ignore a análise what-if
```

**Sempre continue para gerar o relatório**, mesmo que todas as etapas de validação falhem.

---

## Agregação de erros no relatório

Quando ocorrerem vários erros, agregue-os de forma lógica:

1. **Agrupe por fonte** (bicep, what-if e permissões)
2. **Ordene por severidade** (erros antes de avisos)
3. **Remova duplicações** de erros semelhantes
4. **Forneça a contagem resumida** no início

Exemplo:

```markdown
## Problemas

Foram encontrados **3 erros** e **2 avisos**

### Erros (3)

1. [Erro de sintaxe do Bicep - main.bicep:22:51](#error-1)
2. [Erro de sintaxe do Bicep - main.bicep:45:10](#error-2)
3. [Grupo de recursos não encontrado](#error-3)

### Avisos (2)

1. [Validação com permissões limitadas](#warning-1)
2. [Limite de modelos aninhados atingido](#warning-2)
```

---

## Referência de códigos de saída

| Ferramenta | Código de saída | Significado |
|------|-----------|---------|
| az | 0 | Sucesso |
| az | 1 | Erro geral |
| az | 2 | Comando não encontrado |
| az | 3 | Argumento obrigatório ausente |
| azd | 0 | Sucesso |
| azd | 1 | Erro |
| bicep | 0 | Compilação bem-sucedida |
| bicep | 1 | Falha na compilação (erros) |
| bicep | 2 | Compilação bem-sucedida com avisos |
