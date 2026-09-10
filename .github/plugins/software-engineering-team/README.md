# software-engineering-team

Agente de projeto da experiência e da interface do usuário (UX/UI) do conjunto
da equipe de engenharia de software.

## O que esta extensão reúne

| Componente | Tipo | Localização |
|-----------|------|----------|
| `se-ux-ui-designer` | Agente | [`.github/agents/se-ux-ui-designer.agent.md`](../../agents/se-ux-ui-designer.agent.md) |

## Conteúdo relacionado do kit

A imersão fornece seus próprios agentes de persona e estágio em
[`.github/agents/`](../../agents/) (por exemplo, `software-architect`,
`product-owner`, `tech-writer`, `qa-engineer`). Eles cobrem os papéis atendidos
pelos agentes `se-*` originais, portanto esses agentes originais não são
referenciados aqui como substitutos.

## Referências originais não incluídas

- `se-gitops-ci-specialist`, `se-product-manager-advisor`,
  `se-responsible-ai-code`, `se-security-reviewer`,
  `se-system-architecture-reviewer`, `se-technical-writer` (agentes) — não
  estão presentes neste kit.

## Como é habilitado

O conteúdo em `.github/agents/` é descoberto nativamente pelo Copilot neste
repositório, portanto este agente funciona aqui sem instalar nenhuma extensão. A
camada de extensões o empacota como um conjunto nomeado no catálogo local
`datacorp-mm-team-kit` ([`marketplace.json`](../marketplace.json)) e é declarada
em [`.github/copilot/settings.json`](../../copilot/settings.json). Consulte o
[índice de extensões](../README.md) para conhecer o mecanismo e suas limitações.
