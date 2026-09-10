# database-data-management

Habilidades de revisão de código e otimização de PostgreSQL.

## O que esta extensão reúne

| Componente | Tipo | Localização |
|-----------|------|----------|
| `postgresql-code-review` | Habilidade | [`.github/skills/postgresql-code-review/`](../../skills/postgresql-code-review/) |
| `postgresql-optimization` | Habilidade | [`.github/skills/postgresql-optimization/`](../../skills/postgresql-optimization/) |

O PostgreSQL 16 é o banco de dados de destino do kit, portanto somente as habilidades
de PostgreSQL são incluídas.

## Conteúdo relacionado do kit

A imersão mantém um agente da persona [`dba`](../../agents/dba.agent.md) e uma
habilidade [`query-optimization`](../../skills/query-optimization/). Esses são
artefatos próprios do kit, não renomeações diretas dos itens originais
`postgresql-dba` ou `sql-optimization`, portanto não são referenciados aqui como substitutos.

## Referências originais não incluídas

- `sql-code-review`, `sql-optimization` (habilidades) — não estão presentes neste kit.
- `ms-sql-dba`, `postgresql-dba` (agentes) — não estão presentes neste kit.

## Como é habilitado

O conteúdo em `.github/skills/` é descoberto nativamente pelo Copilot neste
repositório, portanto estas habilidades funcionam aqui sem instalar nenhuma extensão. A
camada de extensões as empacota como um conjunto nomeado no catálogo local
`datacorp-mm-team-kit` ([`marketplace.json`](../marketplace.json)) e é declarada
em [`.github/copilot/settings.json`](../../copilot/settings.json). Consulte o
[índice de extensões](../README.md) para conhecer o mecanismo e suas limitações.
