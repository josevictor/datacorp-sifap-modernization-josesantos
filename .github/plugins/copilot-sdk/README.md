# copilot-sdk

Crie aplicações baseadas em agentes com o GitHub Copilot SDK.

## O que esta extensão reúne

| Componente | Tipo | Localização |
|-----------|------|----------|
| `copilot-sdk` | Habilidade | [`.github/skills/copilot-sdk/`](../../skills/copilot-sdk/) |

## Como é habilitado

O conteúdo em `.github/skills/` é descoberto nativamente pelo Copilot neste
repositório, portanto esta habilidade funciona aqui sem instalar nenhuma extensão. A
camada de extensões a empacota como um conjunto nomeado no catálogo local
`datacorp-mm-team-kit` ([`marketplace.json`](../marketplace.json)) e é declarada
em [`.github/copilot/settings.json`](../../copilot/settings.json). Consulte o
[índice de extensões](../README.md) para conhecer o mecanismo e suas limitações.
