---
description: "Use para higiene geral de Terraform (layout de arquivos, variáveis, outputs, formatação, validação, testes e estado). As regras Azure autoritativas do kit ficam em infrastructure.instructions.md."
applyTo: "**/*.tf"
---

# Convenções de Terraform — Higiene geral

Este arquivo acrescenta higiene de Terraform no nível da linguagem às regras autoritativas de infraestrutura do kit. **[`infrastructure.instructions.md`](infrastructure.instructions.md) é autoritativo** para este kit: provider Azure `azurerm ~> 3.x` (`required_version` fixado), tags obrigatórias `project`/`environment`/`owner`, segredos somente em `azurerm_key_vault_secret`, um módulo por área de serviço Azure, Managed Identity e o portão `terraform fmt` + `terraform validate`. Em caso de divergência, prevalecem as regras de infraestrutura. A equipe cria `infra/` nos Estágios 3/4; não existe stack herdada para copiar.

## Layout de arquivos

Divida cada módulo por função para manter os arquivos navegáveis:

- `main.tf` — recursos
- `variables.tf` — entradas tipadas
- `outputs.tf` — outputs
- `locals.tf` — valores calculados e expressões repetidas
- `terraform.tf` — bloco `terraform {}` e requisitos de provider

Use `snake_case` nos nomes de variáveis, locals, outputs e módulos.

## Variáveis e outputs

- Toda variável e output declara `type` e `description` explícitos.
- Forneça valores padrão somente para entradas realmente opcionais; nunca defina um segredo por padrão.
- Marque entradas secretas e outputs com segredos como `sensitive = true`; sempre que possível, não exponha segredos.
- Exponha em `outputs` somente o que outro módulo ou consumidor realmente precisa.

## Locals e fontes de dados

- Mova expressões repetidas para `locals` (por exemplo, o mapa `common_tags`) para manter os valores consistentes.
- Use fontes `data` para ler recursos existentes em vez de fixar IDs. Evite buscas de dados para recursos criados na mesma configuração; referencie-os diretamente.

## Idempotência

Escreva configurações convergentes: um segundo `terraform apply` sem mudança de entrada deve informar zero alterações. Evite efeitos colaterais de `local-exec` / `null_resource` que executem novamente em todo apply.

## Formatação, validação e testes

- Execute `terraform fmt -recursive` e `terraform validate` por módulo antes de todo commit (corresponde ao portão de infraestrutura da CI).
- Execute `tflint` para detectar cedo problemas específicos do provider.
- Escreva testes de módulo com o framework nativo `*.tftest.hcl`, cobrindo um caso positivo e outro negativo; mantenha-os idempotentes.

## Estado

Armazene o estado em um backend remoto (Azure Storage) com locking; nunca faça commit de um arquivo `*.tfstate`. Trate o estado e os módulos obtidos em `.terraform/` como somente leitura; faça toda alteração por HCL e Terraform CLI.

## Convenções

| Regra | Justificativa |
|---|---|
| Uma responsabilidade por arquivo (`main`/`variables`/`outputs`/`locals`) | Módulos navegáveis |
| Nomes em `snake_case`, variáveis tipadas e descritas | HCL consistente e autoexplicativo |
| `sensitive = true` em entradas e outputs secretos | Segredos não aparecem na saída do plano nem no estado |
| `fmt` + `validate` por módulo + `tflint` sem problemas | Corresponde ao portão de infraestrutura da CI |
| Estado remoto, nunca versionado | Sem conflitos nem vazamento de estado |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Siga `infrastructure.instructions.md` para provider, tags, segredos e módulos | Reinvente aqui as regras Azure do kit |
| Fixe versões (base do kit: `azurerm ~> 3.x`) | Use providers flutuantes em `latest` |
| Mantenha o estado remoto e somente leitura | Versione `*.tfstate` ou o edite manualmente |
| Cubra módulos com testes `*.tftest.hcl` | Entregue módulos sem testes |

## Lista de verificação antes de abrir uma PR

- [ ] Os arquivos estão divididos em `main`/`variables`/`outputs`/`locals`, com nomes em `snake_case`
- [ ] Toda variável e output possui `type` e `description`; segredos estão marcados como `sensitive`
- [ ] `terraform fmt -recursive`, `validate` por módulo e `tflint` passam localmente
- [ ] As versões dos providers estão fixadas na base do kit (`azurerm ~> 3.x`)
- [ ] O estado permanece no backend remoto; nenhum `*.tfstate` está versionado
