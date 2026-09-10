---
name: "iac-module"
description: "Crie ou refatore um módulo Terraform da infraestrutura Azure do SIFAP 2.0 com etiquetas padronizadas, variáveis tipadas, saídas e validação."
argument-hint: "name=<module> service=<azurerm_resource> reqs=REQ-NNN"
agent: "devops-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /iac-module

## Objetivo

Produzir ou atualizar **um único módulo Terraform** em `infra/modules/` para o SIFAP 2.0, limitado a uma área de serviço do Azure (rede, computação, banco de dados, monitoramento ou segurança). O módulo aplica as etiquetas (`tags`) padrão do SIFAP a todos os recursos que as aceitam, mantém os segredos fora do código, usa identidade gerenciada para autenticação entre serviços e passa em `terraform fmt` e `terraform validate`, além de `tflint` e `checkov`, antes do registro da alteração. Assim, ele corresponde ao controle de infraestrutura em `.github/workflows/ci.yml`.

## Quando usar

Use quando um contexto delimitado precisar de um novo serviço do Azure ou quando um módulo existente precisar ser reforçado ou ampliado. As mudanças de módulo são entregues em sua própria solicitação de integração, separada do código da funcionalidade.

## Pré-condições

- `.specify/memory/constitution.md` declara as regras inegociáveis (identidade gerenciada, Key Vault e acesso à rede)
- O serviço do Azure e o `REQ-ID` vinculado são conhecidos
- O caminho do módulo alvo (`infra/modules/<name>/`) é novo ou já existe para atualização

## Entradas que a equipe deve fornecer

- O nome do módulo e o serviço do Azure, por exemplo, `database` para `azurerm_postgresql_flexible_server`
- O `REQ-ID` vinculado em `specs/<NNN>-<feature>/spec.md`, geralmente não funcional ou operacional
- Os ambientes alvo (`dev`, `stage`, `prod`) e todas as substituições específicas por ambiente
- A indicação de que a mudança cria um módulo novo ou modifica um existente

Solicite à pessoa usuária qualquer item ausente.

## O que farei

- Lerei [`../skills/iac-review/SKILL.md`](../skills/iac-review/SKILL.md) e a constituição e seguirei os padrões dos módulos existentes
- Escreverei a estrutura inicial do módulo com cinco arquivos e variáveis tipadas e documentadas
- Aplicarei o conjunto padrão de etiquetas do SIFAP a todos os recursos que aceitam etiquetas
- Manterei os segredos em `azurerm_key_vault_secret`, nunca em `locals`, `variables` ou `outputs`
- Usarei identidade gerenciada e rede privada por padrão
- Adicionarei `examples/basic/` e validarei localmente com `fmt`, `validate`, `tflint` e `checkov`

## O que não farei

- Inventar o preço de uma SKU, a disponibilidade de uma região ou um valor específico do SIFAP. As entradas desconhecidas serão parametrizadas e confirmadas pela equipe
- Criar a esteira de CI/CD (`/pipeline`), escrever código de aplicação (`@builder`) ou alterar requisitos (`@requirements-engineer`)
- Inserir um segredo em uma variável, um valor padrão, uma saída ou o arquivo de estado quando isso puder ser evitado
- Definir `public_network_access_enabled = true` sem uma exceção documentada em `.specify/memory/constitution.md`
- Inserir um bloco `provider` no módulo ou aplicar etiquetas somente a parte dos recursos

## Formato da saída

Um módulo com cinco arquivos (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`), além de `examples/basic/`. Os arquivos principais seguem o padrão `azurerm` real do repositório:

```hcl
# infra/modules/database/versions.tf
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.116"
    }
    random = { source = "hashicorp/random", version = "~> 3.6" }
  }
}

# infra/modules/database/main.tf
locals {
  tags = merge(var.tags, {
    project     = "sifap"
    environment = var.environment
    owner       = var.owner
    cost-center = var.cost_center
    module      = "database"
    managed-by  = "terraform"
  })
}

resource "random_password" "admin" {
  length  = 32
  special = true
}

resource "azurerm_postgresql_flexible_server" "this" {
  name                          = "${var.project}-${var.environment}-psql-${var.location_short}"
  resource_group_name           = var.resource_group_name
  location                      = var.location
  version                       = "16"
  administrator_login           = var.administrator_login
  administrator_password        = random_password.admin.result
  public_network_access_enabled = false # somente ponto de extremidade privado; nenhuma exceção registrada
  tags                          = local.tags
}

# O segredo fica no Key Vault, nunca em variáveis, saídas ou registros.
resource "azurerm_key_vault_secret" "admin_password" {
  name         = "${var.environment}-psql-admin-password"
  value        = random_password.admin.result
  key_vault_id = var.key_vault_id
  tags         = local.tags
}

# infra/modules/database/outputs.tf
output "server_fqdn" {
  description = "FQDN do PostgreSQL para consumidores; não contém segredos."
  value       = azurerm_postgresql_flexible_server.this.fqdn
}
```

Acompanhe o módulo com um relatório de validação (saída de `fmt`, `validate`, `tflint` e `checkov`) e uma observação de uma linha sobre o custo mensal por ambiente, com link para os preços do Azure.

## Definição de pronto

- [ ] `terraform fmt -check`, `terraform validate`, `tflint` e `checkov` passam
- [ ] Todos os recursos que aceitam etiquetas contêm `project`, `environment` e `owner`, além das etiquetas extras padrão
- [ ] Nenhum segredo aparece em variáveis, saídas ou valores padrão
- [ ] O acesso à rede pública permanece desativado, exceto quando houver referência a uma exceção na constituição
- [ ] A identidade gerenciada é usada e nenhuma credencial de principal de serviço aparece no código
- [ ] Um consumidor em `examples/basic/` compila e passa na validação
- [ ] O arquivo `README.md` documenta entradas, saídas, um exemplo e o `REQ-ID` vinculado

## Corpo do prompt

Você é `@devops-engineer`. A equipe precisa de um módulo focado e revisável que respeite as regras de Terraform do repositório.

**Etapa 1: leia a constituição e a habilidade.**
Abra `.specify/memory/constitution.md` para consultar as regras inegociáveis e [`../skills/iac-review/SKILL.md`](../skills/iac-review/SKILL.md) para consultar a lista de verificação da revisão. Revise os módulos existentes para identificar os padrões a seguir.

**Etapa 2: fixe o provedor.**
Use `azurerm ~> 3.x`, o padrão do repositório, fixado por `required_providers`, e consulte os [módulos verificados do Azure (Azure Verified Modules)](https://aka.ms/avm) quando aplicável.

**Etapa 3: escreva a estrutura inicial.**
Crie `main.tf` (somente recursos, sem bloco `provider`), `variables.tf` (todas as entradas tipadas e documentadas, com blocos `validation` quando os intervalos forem relevantes), `outputs.tf` (IDs, nomes e FQDNs, nunca segredos), `versions.tf` e `README.md`.

**Etapa 4: aplique as etiquetas padrão.**
Combine `var.tags` com `project`, `environment`, `owner`, `cost-center`, `module` e `managed-by` e associe o mapa a todos os recursos que aceitam etiquetas.

**Etapa 5: aplique a disciplina de segredos, identidade e rede.**
Os segredos passam por fontes de dados `azurerm_key_vault_secret` ou por valores gerados e armazenados no Key Vault, nunca por variáveis, valores padrão ou saídas. Use identidades gerenciadas atribuídas pelo sistema ou pela pessoa usuária para autenticação entre serviços. Mantenha `public_network_access_enabled = false`, exceto quando a constituição conceder uma exceção.

**Etapa 6: adicione um exemplo e valide.**
Escreva `examples/basic/main.tf` para consumir o módulo. Depois, execute `terraform fmt -check -recursive`, `terraform init -backend=false`, `terraform validate`, `tflint --recursive` e `checkov -d . --soft-fail false`. Todos os comandos devem passar.

`terraform fmt` e `terraform validate` devem passar antes do registro da alteração, conforme `.github/workflows/ci.yml`. Todos os recursos que aceitam etiquetas contêm as etiquetas obrigatórias. Nenhum segredo pode chegar a uma variável, saída ou valor padrão. Nunca habilite o acesso à rede pública sem uma exceção documentada nem invente um valor que a equipe precise confirmar.

## Exemplo de chamada

```
/iac-module name=database service=azurerm_postgresql_flexible_server reqs=REQ-NNN
```
