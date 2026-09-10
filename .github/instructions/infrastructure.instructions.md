---
description: "Use ao criar ou revisar infraestrutura como código, Terraform, Bicep, definições de recursos Azure e configuração de ambientes."
applyTo: "infra/**,**/*.tf,**/*.bicep,compose*.yml,compose*.yaml,docker-compose*.yml,docker-compose*.yaml"
---

# Convenções de infraestrutura — Terraform e Compose

Este arquivo é ativado quando você edita arquivos em `infra/`, qualquer `*.tf` ou `*.bicep` ou um arquivo YAML `compose`/`docker-compose`. Ele ensina a provisionar o Azure com Terraform (`azurerm ~> 3.x`, a ferramenta principal) e a manter com segurança a paridade do Compose local. Prefira Terraform; use Bicep somente quando um módulo realmente o exigir. A equipe cria `infra/` nos Estágios 3/4; não existe stack herdada para copiar.

## Provider e versões

Fixe o provider e a versão mínima do Terraform. Mantenha um bloco `provider "azurerm"` por configuração.

```hcl
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```

## Layout de módulos

Use um módulo por área de serviço Azure para manter claros o raio de impacto e a responsabilidade.

```text
infra/
├── networking/   # VNet, sub-redes, NSGs
├── compute/      # App Service / Container Apps
├── database/     # PostgreSQL Flexible Server
└── monitoring/   # Log Analytics, alertas
```

## Tags obrigatórias em todos os recursos

Todo recurso possui `project`, `environment` e `owner` (adicione `cost-center` quando a equipe a acompanhar). Defina-as uma vez em `locals` e aplique-as.

```hcl
locals {
  common_tags = {
    project     = var.project
    environment = var.environment
    owner       = var.owner
  }
}

resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg-${var.location_short}"
  location = var.location
  tags     = local.common_tags
}
```

## Segredos

> [!WARNING]
> Segredos ficam somente em `azurerm_key_vault_secret`, nunca em `locals`, valores padrão de `variables`, `.tfvars` ou estado versionado. Marque entradas secretas com `sensitive = true` e injete-as pela sessão OIDC do pipeline.

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = var.db_password
  key_vault_id = azurerm_key_vault.main.id
  tags         = local.common_tags
}
```

## Managed Identity

A autenticação serviço a serviço usa Managed Identity (`azurerm_user_assigned_identity` ou identidade atribuída pelo sistema), não strings de conexão com senhas incorporadas. Atribua a identidade e conceda acesso ao Key Vault por uma atribuição de papel.

## Convenção de nomenclatura

Os nomes de recursos seguem `{project}-{env}-{resource}-{region}`.

| Recurso | Exemplo |
|---|---|
| Grupo de recursos | `sifap-prod-rg-brs` |
| Servidor PostgreSQL | `sifap-prod-psql-brs` |

## Portão de formatação e validação

A CI executa `terraform fmt -check -recursive` e, em cada módulo, `terraform init -backend=false` seguido de `terraform validate` (consulte [`ci.yml`](../workflows/ci.yml)). Antes do push, execute localmente `terraform fmt -recursive` e `terraform -chdir=<module> validate`. A skill [`iac-review`](../skills/iac-review/SKILL.md) detém a detecção de desvios e a revisão aprofundada de módulos.

## Paridade do Docker Compose

Compose destina-se somente ao desenvolvimento local. Fixe imagens por digest, mantenha segredos em um `.env` ignorado pelo Git e nunca versione credenciais reais.

```yaml
services:
  db:
    image: postgres:16@sha256:<digest> # fixe o digest
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD} # vem de .env, nunca fixada no código
```

## Convenções

| Regra | Justificativa |
|---|---|
| `azurerm ~> 3.x`, `required_version` fixado | Planos reproduzíveis entre máquinas |
| Um módulo por área de serviço | Responsabilidade clara e raio de impacto pequeno |
| Tags `project` + `environment` + `owner` em todos os recursos | Rastreabilidade de custo, auditoria e limpeza |
| Segredos somente em `azurerm_key_vault_secret` | Sem credenciais no código ou estado |
| Managed Identity para autenticação de serviços | Sem senhas armazenadas entre serviços |
| `fmt` + `validate` por módulo sem problemas | Corresponde ao portão de infraestrutura da CI |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Aplique `local.common_tags` a todo recurso | Entregue um recurso sem tags |
| Marque variáveis secretas com `sensitive = true` | Coloque um segredo no valor padrão de `variable` ou em `.tfvars` |
| Fixe imagens Compose por digest | Use `postgres:latest` |
| Autentique por Managed Identity | Incorpore uma senha em uma string de conexão |

## Lista de verificação antes de abrir uma PR

- [ ] O provider é `azurerm ~> 3.x`, com `required_version` fixado
- [ ] Todo recurso possui as tags `project`, `environment` e `owner`
- [ ] Nenhum segredo aparece fora de `azurerm_key_vault_secret`; variáveis secretas são `sensitive`
- [ ] A autenticação serviço a serviço usa Managed Identity
- [ ] `terraform fmt -check -recursive` e `validate` por módulo passam localmente
- [ ] Os arquivos Compose fixam os digests das imagens e leem segredos de um `.env` ignorado pelo Git
