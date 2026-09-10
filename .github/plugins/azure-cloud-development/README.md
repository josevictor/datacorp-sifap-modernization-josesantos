# azure-cloud-development

Habilidades de desenvolvimento em nuvem no Azure: otimização de custos, preços e integridade de recursos.

## O que esta extensão reúne

O manifesto referencia habilidades que ficam no nível do repositório em
`.github/skills/`. Elas são mantidas uma única vez nesse local e compartilhadas em todo o kit.

| Componente | Tipo | Localização |
|-----------|------|----------|
| `az-cost-optimize` | Habilidade | [`.github/skills/az-cost-optimize/`](../../skills/az-cost-optimize/) |
| `azure-pricing` | Habilidade | [`.github/skills/azure-pricing/`](../../skills/azure-pricing/) |
| `azure-resource-health-diagnose` | Habilidade | [`.github/skills/azure-resource-health-diagnose/`](../../skills/azure-resource-health-diagnose/) |

## Referências originais não incluídas

A extensão `azure-cloud-development` original também listava os itens abaixo. Eles
não estão presentes em `.github/skills/` e `.github/agents/` consolidados deste
kit, portanto o manifesto os omite:

- `import-infrastructure-as-code` (habilidade)
- `azure-logic-apps-expert`, `azure-principal-architect`, `azure-saas-architect`,
  `azure-verified-modules-bicep`, `azure-verified-modules-terraform`,
  `terraform-azure-implement`, `terraform-azure-planning` (agentes)

## Como é habilitado

O conteúdo em `.github/skills/` é descoberto nativamente pelo Copilot neste
repositório, portanto estas habilidades funcionam aqui sem instalar nenhuma extensão. A
camada de extensões as empacota como um conjunto nomeado no catálogo local
`datacorp-mm-team-kit` ([`marketplace.json`](../marketplace.json)) e é declarada
em [`.github/copilot/settings.json`](../../copilot/settings.json). Consulte o
[índice de extensões](../README.md) para conhecer o mecanismo e suas limitações.
