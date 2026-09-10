# Referência dos comandos de validação

Esta referência documenta todos os comandos usados na validação pré-implantação do Azure.

## Azure Developer CLI (azd)

### azd provision --preview

Visualiza as alterações de infraestrutura de projetos azd sem implantá-las.

```bash
azd provision --preview [options]
```

**Opções:**

| Opção | Descrição |
|--------|-------------|
| `--environment`, `-e` | Nome do ambiente a usar |
| `--no-prompt` | Aceita os padrões sem solicitar confirmação |
| `--debug` | Ativa registros de depuração |
| `--cwd` | Define o diretório de trabalho |

**Exemplos:**

```bash
# Visualiza com o ambiente padrão
azd provision --preview

# Visualiza um ambiente específico
azd provision --preview --environment dev

# Visualiza sem solicitações de confirmação (CI/CD)
azd provision --preview --no-prompt
```

**Saída:** mostra os recursos que serão criados, modificados ou excluídos.

### azd auth login

Autentica no Azure para operações do azd.

```bash
azd auth login [options]
```

**Opções:**

| Opção | Descrição |
|--------|-------------|
| `--check-status` | Verifica o status da autenticação sem entrar |
| `--use-device-code` | Usa o fluxo de código do dispositivo |
| `--tenant-id` | Especifica o tenant |
| `--client-id` | ID de cliente da entidade de serviço |

### azd env list

Lista os ambientes disponíveis.

```bash
azd env list
```

---

## Azure CLI (az)

### az deployment group what-if

Visualiza alterações de implantações em grupos de recursos.

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  [options]
```

**Parâmetros obrigatórios:**

| Parâmetro | Descrição |
|-----------|-------------|
| `--resource-group`, `-g` | Nome do grupo de recursos de destino |
| `--template-file`, `-f` | Caminho do arquivo Bicep |

**Parâmetros opcionais:**

| Parâmetro | Descrição |
|-----------|-------------|
| `--parameters`, `-p` | Arquivo de parâmetros ou valores em linha |
| `--validation-level` | `Provider` (padrão), `ProviderNoRbac` ou `Template` |
| `--result-format` | `FullResourcePayloads` (padrão) ou `ResourceIdOnly` |
| `--no-pretty-print` | Produz JSON bruto para análise |
| `--name`, `-n` | Nome da implantação |
| `--exclude-change-types` | Exclui tipos específicos de alterações da saída |

**Níveis de validação:**

| Nível | Descrição | Caso de uso |
|-------|-------------|----------|
| `Provider` | Validação completa com verificações de RBAC | Padrão, mais completa |
| `ProviderNoRbac` | Validação completa, somente com permissões de leitura | Quando faltam permissões de implantação |
| `Template` | Somente validação estática da sintaxe | Verificação rápida da sintaxe |

**Exemplos:**

```bash
# What-if básico
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep

# Com parâmetros e validação completa
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --validation-level Provider

# Alternativa sem verificações de RBAC
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --validation-level ProviderNoRbac

# Saída JSON para análise
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --no-pretty-print
```

### az deployment sub what-if

Visualiza alterações de implantações no nível da assinatura.

```bash
az deployment sub what-if \
  --location <location> \
  --template-file <bicep-file> \
  [options]
```

**Parâmetros obrigatórios:**

| Parâmetro | Descrição |
|-----------|-------------|
| `--location`, `-l` | Local dos metadados da implantação |
| `--template-file`, `-f` | Caminho do arquivo Bicep |

**Exemplos:**

```bash
az deployment sub what-if \
  --location eastus \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --validation-level Provider
```

### az deployment mg what-if

Visualiza alterações de implantações em grupos de gerenciamento.

```bash
az deployment mg what-if \
  --location <location> \
  --management-group-id <mg-id> \
  --template-file <bicep-file> \
  [options]
```

**Parâmetros obrigatórios:**

| Parâmetro | Descrição |
|-----------|-------------|
| `--location`, `-l` | Local dos metadados da implantação |
| `--management-group-id`, `-m` | ID do grupo de gerenciamento de destino |
| `--template-file`, `-f` | Caminho do arquivo Bicep |

### az deployment tenant what-if

Visualiza alterações de implantações no nível do locatário (`tenant`).

```bash
az deployment tenant what-if \
  --location <location> \
  --template-file <bicep-file> \
  [options]
```

**Parâmetros obrigatórios:**

| Parâmetro | Descrição |
|-----------|-------------|
| `--location`, `-l` | Local dos metadados da implantação |
| `--template-file`, `-f` | Caminho do arquivo Bicep |

### az login

Autentica na Azure CLI.

```bash
az login [options]
```

**Opções:**

| Opção | Descrição |
|--------|-------------|
| `--tenant`, `-t` | ID ou domínio do tenant |
| `--use-device-code` | Usa o fluxo de código do dispositivo |
| `--service-principal` | Entra como entidade de serviço |

### az account show

Exibe o contexto atual da assinatura.

```bash
az account show
```

### az group exists

Verifica se o grupo de recursos existe.

```bash
az group exists --name <rg-name>
```

---

## Bicep CLI

### bicep build

Compila Bicep para JSON do ARM e valida a sintaxe.

```bash
bicep build <bicep-file> [options]
```

**Opções:**

| Opção | Descrição |
|--------|-------------|
| `--stdout` | Produz a saída em stdout em vez de um arquivo |
| `--outdir` | Diretório de saída |
| `--outfile` | Caminho do arquivo de saída |
| `--no-restore` | Ignora a restauração de módulos |

**Exemplos:**

```bash
# Valida a sintaxe (saída em stdout, sem criar arquivo)
bicep build main.bicep --stdout > /dev/null

# Compila em um diretório específico
bicep build main.bicep --outdir ./build

# Valida vários arquivos
for f in *.bicep; do bicep build "$f" --stdout; done
```

**Formato da saída de erro:**

```text
/path/to/file.bicep(22,51) : Error BCP064: Found unexpected tokens in interpolated expression.
/path/to/file.bicep(22,51) : Error BCP004: The string at this location is not terminated.
```

Formato: `<file>(<line>,<column>) : <severity> <code>: <message>`

### bicep --version

Verifica a versão da Bicep CLI.

```bash
bicep --version
```

---

## Detecção de arquivos de parâmetros

### Parâmetros Bicep (.bicepparam)

Arquivos modernos de parâmetros Bicep (recomendados):

```bicep
using './main.bicep'

param location = 'eastus'
param environment = 'dev'
param tags = {
  environment: 'dev'
  project: 'myapp'
}
```

**Padrão de detecção:** `<template-name>.bicepparam`

### Parâmetros JSON (.parameters.json)

Arquivos tradicionais de parâmetros do ARM:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": { "value": "eastus" },
    "environment": { "value": "dev" }
  }
}
```

**Padrões de detecção:**

- `<template-name>.parameters.json`
- `parameters.json`
- `parameters/<env>.json`

### Uso de parâmetros com comandos

```bash
# Arquivo de parâmetros Bicep
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam

# Arquivo de parâmetros JSON
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters @parameters.json

# Substituições de parâmetros em linha
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --parameters location=westus
```

---

## Determinação do escopo da implantação

Verifique a declaração `targetScope` do arquivo Bicep:

```bicep
// Grupo de recursos (padrão quando não especificado)
targetScope = 'resourceGroup'

// Assinatura
targetScope = 'subscription'

// Grupo de gerenciamento
targetScope = 'managementGroup'

// Locatário
targetScope = 'tenant'
```

**Mapeamento de escopo para comando:**

| targetScope | Comando | Parâmetros obrigatórios |
|-------------|---------|---------------------|
| `resourceGroup` | `az deployment group what-if` | `--resource-group` |
| `subscription` | `az deployment sub what-if` | `--location` |
| `managementGroup` | `az deployment mg what-if` | `--location`, `--management-group-id` |
| `tenant` | `az deployment tenant what-if` | `--location` |

---

## Requisitos de versão

| Ferramenta | Versão mínima | Versão recomendada | Recursos principais |
|------|-----------------|---------------------|--------------|
| Azure CLI | 2.14.0 | 2.76.0+ | Opção `--validation-level` |
| Azure Developer CLI | 1.0.0 | Mais recente | Opção `--preview` |
| Bicep CLI | 0.4.0 | Mais recente | Melhores mensagens de erro |

**Verifique as versões:**

```bash
az --version
azd version
bicep --version
```
