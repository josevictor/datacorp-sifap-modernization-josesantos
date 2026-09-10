# DBA — Kit do Copilot

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › **DBA**

**Kit de referência da persona DBA na imersão de modernização do SIFAP.**

![Persona](https://img.shields.io/badge/Persona-DBA-171717?style=flat-square) ![Dupla 4](https://img.shields.io/badge/Dupla-4%20%C2%B7%20Qualidade-404040?style=flat-square) ![Estágio 3](https://img.shields.io/badge/Est%C3%A1gio-3%20%C2%B7%20Implementa%C3%A7%C3%A3o-737373?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que assume a persona DBA na imersão |
| **Foco** | Modelagem de dados, migrações Flyway, otimização de consultas e auditoria de injeção de SQL |
| **Fase do SDLC** | Estágio 3 — Implementação (schema + migrações) |
| **Resultado esperado** | Schema PostgreSQL 16 consistente com as entidades JPA e dados iniciais de teste |

Leia primeiro: [PERSONA.md](PERSONA.md).

---

## Conceito

O DBA (Database Administrator) é responsável pela camada de dados do SIFAP 2.0. Na modernização do legado, isso significa traduzir os quatro DDMs do Adabas, com seus campos MU (multiple-value) e PE (periodic), para um schema relacional normalizado no PostgreSQL 16, escrever migrações Flyway idempotentes e proteger a integridade dos dados durante todo o projeto.

Por que isso importa: o modelo de dados é a base das entidades JPA do Developer e da infraestrutura provisionada por DevOps. Um schema frágil ou migrações irreversíveis comprometem todo o Estágio 3.

## Kit de persona

Todos os artefatos ativos ficam no diretório `.github/` da raiz do repositório. Esta pasta serve como referência; edite os arquivos em `.github/` quando houver necessidade de manutenção.

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, estágios, prompts e rubricas do DBA |
| `.github/agents/dba.agent.md` | Agente | Modelagem de dados, migrações e auditoria de SQL |
| `.github/prompts/persona-dba-migration.prompt.md` | Prompt | `/migration` |
| `.github/prompts/persona-dba-query-audit.prompt.md` | Prompt | `/query-audit` |
| `.github/instructions/database.instructions.md` | Instruções | Convenções de banco de dados |

> [!TIP]
> Se a pessoa facilitadora solicitar uma configuração MCP local e este kit tiver `mcp.json`, copie somente esse arquivo para `.vscode/mcp.json`.

## Onde ficam os artefatos ativos

- Agentes: `.github/agents/`
- Prompts: `.github/prompts/persona-*.prompt.md`
- Skills: `.github/skills/`
- Instruções: `.github/instructions/`

## Boas práticas

- [ ] **Meça o impacto dos índices nas duas direções.** Os índices aceleram leituras e tornam escritas mais lentas; meça ambos os efeitos antes de criar um índice.
- [ ] **Use expand-contract nas migrações.** As alterações de schema devem permanecer compatíveis por pelo menos duas implantações consecutivas.
- [ ] **Detecte consultas N+1 antes do ambiente de staging.** Elas são bugs de desempenho, não melhorias opcionais.
- [ ] **Valide os backups por meio da restauração.** Um backup que nunca foi restaurado não é confiável.

## Exemplo do SIFAP

No Estágio 1, o DBA lê o DDM `BENEFIC.ddm` e mapeia os campos necessários à feature para possíveis tabelas relacionadas. No Estágio 3, escreve a migração Flyway correspondente, define índices somente quando as consultas confirmadas os justificam e prepara os dados necessários aos testes de integração do QA Engineer.

## Referências

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Use the Index, Luke — Markus Winand](https://use-the-index-luke.com/)
- [High Performance MySQL / PostgreSQL — Schwartz et al.](https://www.oreilly.com/)
- [Azure Database for PostgreSQL Best Practices](https://learn.microsoft.com/azure/postgresql/)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Visão geral das personas](../OVERVIEW.md)<br/><sub>Tabela das 10 personas e suas duplas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil completo da persona DBA.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
