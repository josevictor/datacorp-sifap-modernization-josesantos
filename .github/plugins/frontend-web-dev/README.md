# frontend-web-dev

Agente de interface web React e habilidade de geração de testes Playwright.

## O que esta extensão reúne

| Componente | Tipo | Localização |
|-----------|------|----------|
| `expert-react-frontend-engineer` | Agente | [`.github/agents/expert-react-frontend-engineer.agent.md`](../../agents/expert-react-frontend-engineer.agent.md) |
| `playwright-generate-test` | Habilidade | [`.github/skills/playwright-generate-test/`](../../skills/playwright-generate-test/) |

## Referências originais não incluídas

- `playwright-explore-website` (habilidade) — não está presente neste kit.
- `electron-angular-native` (agente) — não está presente neste kit.

## Como é habilitado

O conteúdo em `.github/skills/` e `.github/agents/` é descoberto nativamente
pelo Copilot neste repositório, portanto estes componentes funcionam aqui sem
instalar nenhuma extensão. A camada de extensões os empacota como um conjunto nomeado
no catálogo local `datacorp-mm-team-kit`
([`marketplace.json`](../marketplace.json)) e é declarada em
[`.github/copilot/settings.json`](../../copilot/settings.json). Consulte o
[índice de extensões](../README.md) para conhecer o mecanismo e suas limitações.
