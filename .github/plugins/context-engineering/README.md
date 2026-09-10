# context-engineering

Mapeamento de contexto para maximizar a eficácia do GitHub Copilot.

## O que esta extensão reúne

| Componente | Tipo | Localização |
|-----------|------|----------|
| `context-map` | Habilidade | [`.github/skills/context-map/`](../../skills/context-map/) |

## Conteúdo relacionado do kit

A imersão também mantém
[`.github/skills/context-audit/`](../../skills/context-audit/) e
[`.github/skills/refactor-safely/`](../../skills/refactor-safely/), que são os
equivalentes próprios do kit às habilidades originais `what-context-needed` e
`refactor-plan`.

## Referências originais não incluídas

- `refactor-plan`, `what-context-needed` (habilidades) — o kit usa
  `refactor-safely` e `context-audit` no lugar delas.
- `context-architect` (agente) — não está presente neste kit.

## Como é habilitado

O conteúdo em `.github/skills/` é descoberto nativamente pelo Copilot neste
repositório, portanto esta habilidade funciona aqui sem instalar nenhuma extensão. A
camada de extensões a empacota como um conjunto nomeado no catálogo local
`datacorp-mm-team-kit` ([`marketplace.json`](../marketplace.json)) e é declarada
em [`.github/copilot/settings.json`](../../copilot/settings.json). Consulte o
[índice de extensões](../README.md) para conhecer o mecanismo e suas limitações.
