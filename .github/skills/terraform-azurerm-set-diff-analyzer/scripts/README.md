# Script analisador de diferenças em conjuntos do Terraform AzureRM

Script Python que analisa o JSON de planos do Terraform e identifica "diferenças falsas positivas" em atributos do tipo Set do AzureRM.

## Visão geral

Os atributos do tipo Set do provedor AzureRM, como `backend_address_pool` e `security_rule`, não garantem a ordem. Ao adicionar ou remover elementos, todos podem aparecer como "alterados". Este script diferencia essas "diferenças falsas positivas" das alterações reais.

### Casos de uso

- Como **habilidade de agente (Agent Skill)** (recomendado)
- Como **ferramenta de CLI** para execução manual
- Para análise automatizada em **fluxos de CI/CD**

## Pré-requisitos

- Python 3.8 ou superior
- Nenhum pacote adicional é necessário (usa apenas a biblioteca padrão)

## Uso

### Uso básico

```bash
# Ler de um arquivo
python analyze_plan.py plan.json

# Ler de stdin
terraform show -json plan.tfplan | python analyze_plan.py
```

### Opções

| Opção | Abreviação | Descrição | Padrão |
|--------|-------|-------------|---------|
| `--format` | `-f` | Formato de saída (markdown/json/summary) | markdown |
| `--exit-code` | `-e` | Retorna código de saída conforme as alterações | false |
| `--quiet` | `-q` | Suprime avisos | false |
| `--verbose` | `-v` | Mostra avisos detalhados | false |
| `--ignore-case` | - | Compara valores sem diferenciar maiúsculas de minúsculas | false |
| `--attributes` | - | Caminho do arquivo personalizado de definições de atributos | (interno) |
| `--include` | - | Filtra os recursos a analisar (pode ser repetido) | (todos) |
| `--exclude` | - | Filtra os recursos a excluir (pode ser repetido) | (nenhum) |

### Códigos de saída (com `--exit-code`)

| Código | Significado |
|------|---------|
| 0 | Sem alterações ou apenas alterações de ordem |
| 1 | Alterações reais em atributos Set |
| 2 | Substituição de recurso (excluir + criar) |
| 3 | Erro |

## Formatos de saída

### Markdown (padrão)

Formato legível para comentários de solicitações de pull e relatórios.

```bash
python analyze_plan.py plan.json --format markdown
```

### JSON

Dados estruturados para processamento programático.

```bash
python analyze_plan.py plan.json --format json
```

Exemplo de saída:

```json
{
  "summary": {
    "order_only_count": 3,
    "actual_set_changes_count": 1,
    "replace_count": 0
  },
  "has_real_changes": true,
  "resources": [...],
  "warnings": []
}
```

### Resumo

Resumo de uma linha para registros de CI/CD.

```bash
python analyze_plan.py plan.json --format summary
```

Exemplo de saída:

```text
🟢 3 apenas de ordem | 🟡 1 alteração de Set
```

## Uso em fluxos de CI/CD

### GitHub Actions

```yaml
name: Análise do plano do Terraform

on:
  pull_request:
    paths:
      - '**.tf'

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configurar o Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform init e plan
        run: |
          terraform init
          terraform plan -out=plan.tfplan
          terraform show -json plan.tfplan > plan.json

      - name: Analisar diff de Set
        run: |
          python path/to/analyze_plan.py plan.json --format markdown > analysis.md

      - name: Comentar na solicitação de pull
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          path: analysis.md
```

### GitHub Actions (critério de bloqueio com código de saída)

```yaml
      - name: Analisar e aplicar critério de bloqueio
        run: |
          python path/to/analyze_plan.py plan.json --exit-code --format summary
        # Falha com o código de saída 2 (substituição de recurso)
        continue-on-error: false
```

### Azure Pipelines

```yaml
- task: TerraformCLI@0
  inputs:
    command: 'plan'
    commandOptions: '-out=plan.tfplan'

- script: |
    terraform show -json plan.tfplan > plan.json
    python scripts/analyze_plan.py plan.json --format markdown > $(Build.ArtifactStagingDirectory)/analysis.md
  displayName: 'Analisar plano'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)/analysis.md'
    artifactName: 'plan-analysis'
```

### Exemplos de filtragem

Analise apenas recursos específicos:

```bash
python analyze_plan.py plan.json --include application_gateway --include load_balancer
```

Exclua recursos específicos:

```bash
python analyze_plan.py plan.json --exclude virtual_network
```

## Interpretação dos resultados

| Categoria | Significado | Ação recomendada |
|----------|---------|-------------------|
| 🟢 Apenas ordem | Diferença falsa positiva, sem alteração real | Pode ser ignorada com segurança |
| 🟡 Alteração real | Elemento Set adicionado, removido ou modificado | Revise o conteúdo; geralmente é uma atualização local |
| 🔴 Substituição de recurso | excluir + criar | Verifique o impacto de indisponibilidade |

## Definições personalizadas de atributos

Por padrão, usa `references/azurerm_set_attributes.json`, mas você pode informar um arquivo de definição personalizado:

```bash
python analyze_plan.py plan.json --attributes /path/to/custom_attributes.json
```

Consulte `references/azurerm_set_attributes.md` para conhecer o formato do arquivo de definição.

## Limitações

- Apenas recursos AzureRM (`azurerm_*`) são compatíveis
- Alguns recursos ou atributos podem não ser compatíveis
- As comparações podem ficar incompletas em atributos que contenham `after_unknown` (valores determinados após a aplicação do plano)
- As comparações podem ficar incompletas em atributos sensíveis (eles são mascarados)

## Documentação relacionada

- [SKILL.md](../SKILL.md): uso como habilidade de agente
- [azurerm_set_attributes.md](../references/azurerm_set_attributes.md): referência das definições de atributos
