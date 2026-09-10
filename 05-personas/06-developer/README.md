# Developer — Kit do Copilot

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › **Developer**

**Kit de referência para a persona Developer na imersão de modernização do SIFAP.**

![Persona](https://img.shields.io/badge/Persona-Developer-171717?style=flat-square) ![Dupla 3](https://img.shields.io/badge/Dupla-3%20%C2%B7%20Implementa%C3%A7%C3%A3o-404040?style=flat-square) ![Estágio 3](https://img.shields.io/badge/Est%C3%A1gio-3%20%C2%B7%20Implementa%C3%A7%C3%A3o-737373?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que assume a persona Developer na imersão |
| **Foco** | Implementação com Java 21 + Next.js 15, TDD e correção de bugs |
| **Fase do SDLC** | Estágio 3 — Implementação; Estágio 4 — Evolução |
| **Resultado esperado** | Backend + frontend da fatia priorizada com testes aprovados |

Leia primeiro: [PERSONA.md](PERSONA.md).

---

## Conceito

O Developer transforma especificações EARS em código executável. Na modernização do SIFAP (Sistema de Fiscalização e Administração de Pagamentos), essa persona traduz programas Natural e modelos DDM/Adabas para Java 21 com Spring Boot 3.3, JPA/Hibernate e PostgreSQL 16, além de implementar o frontend em Next.js 15 com TypeScript.

Por que isso importa: sem o Developer, os requisitos permanecem como texto. Essa persona transforma a prova de conceito em software testado e pronto para merge.

## Kit da persona

Todos os artefatos ativos ficam no diretório `.github/` da raiz do repositório. Esta pasta é uma referência; edite os arquivos em `.github/` quando houver necessidade de manutenção.

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, estágios, prompts e rubricas do Developer |
| `.github/agents/implementer.agent.md` | Agente | Implementação, TDD e correção de bugs |
| `.github/prompts/persona-developer-implement.prompt.md` | Prompt | `/implement` |
| `.github/prompts/persona-developer-fix-bug.prompt.md` | Prompt | `/fix-bug` |
| `.github/prompts/persona-developer-tdd.prompt.md` | Prompt | `/tdd` |
| `.github/prompts/persona-developer-refactor.prompt.md` | Prompt | `/refactor` |

> [!TIP]
> Se a pessoa facilitadora solicitar uma configuração MCP local e este kit tiver `mcp.json`, copie somente esse arquivo para `.vscode/mcp.json`.

## Onde ficam os artefatos ativos

- Agentes: `.github/agents/`
- Prompts: `.github/prompts/persona-*.prompt.md`
- Skills: `.github/skills/`
- Instruções: `.github/instructions/`

## Boas práticas

- [ ] **Escreva testes antes ou junto com o código.** Quando o design estiver claro, escreva primeiro o teste. Todo commit inclui testes.
- [ ] **Mantenha os PRs pequenos.** Trate um assunto por PR, revisável em cerca de 20 minutos.
- [ ] **Separe a refatoração das mudanças de comportamento.** Use commits distintos para cada intenção.
- [ ] **Comente o porquê, não o quê.** O código descreve o que faz; o comentário explica o motivo.

## Exemplo no SIFAP

No Estágio 3, o Developer recebe REQ-IDs de Requirements Engineer e o plano técnico de Software Architect. A tarefa concreta é implementar a feature fina descrita na especificação conforme as regras confirmadas nos programas Natural atribuídos, com testes rastreáveis aos REQ-IDs e integração com o schema criado pelas migrações Flyway de DBA.

## Referências

- [Clean Code — Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Refactoring — Martin Fowler](https://refactoring.com/)
- [Test-Driven Development — Kent Beck](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
- [GitHub Copilot Best Practices](https://docs.github.com/en/copilot)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Visão geral das personas](../OVERVIEW.md)<br/><sub>Tabela das 10 personas e suas duplas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil completo da persona Developer.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
