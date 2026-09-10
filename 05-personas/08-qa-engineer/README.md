# QA Engineer — Kit do Copilot

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › **QA Engineer**

**Kit de referência da persona QA Engineer na imersão de modernização do SIFAP.**

![Persona](https://img.shields.io/badge/Persona-QA%20Engineer-171717?style=flat-square) ![Dupla 4](https://img.shields.io/badge/Dupla-4%20%C2%B7%20Qualidade-404040?style=flat-square) ![Estágios 3 e 4](https://img.shields.io/badge/Est%C3%A1gios-3%20e%204-737373?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que assume a persona QA Engineer na imersão |
| **Foco** | Geração de testes a partir de especificações EARS, cobertura de comportamentos críticos e manutenção do pipeline verde |
| **Fase do SDLC** | Estágio 3 — Implementação; Estágio 4 — Evolução |
| **Resultado esperado** | Suíte de testes aprovada, pipeline de CI verde e rastreabilidade garantida da especificação aos testes |

Leia primeiro: [PERSONA.md](PERSONA.md).

---

## Conceito

O QA Engineer transforma requisitos EARS em testes executáveis. Na modernização do SIFAP (Sistema de Fiscalização e Administração de Pagamentos), esta persona valida a equivalência funcional entre o comportamento legado em Natural e o código moderno em Java 21, garantindo que cada REQ-ID tenha pelo menos um teste verificável e que o pipeline de CI do GitHub Actions permaneça verde.

Por que isso importa: testes ausentes ou frágeis impedem que o time enxergue regressões. Na modernização de legado, somente testes rastreáveis aos requisitos comprovam a equivalência funcional entre o comportamento antigo e o novo.

## Kit de persona

Todos os artefatos ativos ficam no diretório `.github/` da raiz do repositório. Esta pasta serve como referência; edite os arquivos em `.github/` quando houver necessidade de manutenção.

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, estágios, prompts e rubricas do QA Engineer |
| `.github/agents/qa-engineer.agent.md` | Agente | Geração de testes, análise de cobertura e gates de qualidade |
| `.github/prompts/persona-qa-engineer-create-tests.prompt.md` | Prompt | `/create-tests` |
| `.github/prompts/persona-qa-engineer-coverage-gaps.prompt.md` | Prompt | `/coverage-gaps` |
| `.github/prompts/persona-qa-engineer-test-strategy.prompt.md` | Prompt | `/test-strategy` |
| `.github/instructions/tests.instructions.md` | Instruções | Convenções de testes |

> [!TIP]
> Se a pessoa facilitadora solicitar uma configuração MCP local e este kit tiver `mcp.json`, copie somente esse arquivo para `.vscode/mcp.json`.

## Onde ficam os artefatos ativos

- Agentes: `.github/agents/`
- Prompts: `.github/prompts/persona-*.prompt.md`
- Skills: `.github/skills/`
- Instruções: `.github/instructions/`

## Boas práticas

- [ ] **Siga a pirâmide de testes.** Priorize mais testes unitários, uma quantidade moderada de testes de integração e menos testes de ponta a ponta.
- [ ] **Trate um teste instável como bug.** Isole, corrija ou remova o teste; nunca o ignore.
- [ ] **Garanta que cada asserção comprove um comportamento.** Cobertura de linhas sem uma asserção significativa não valida o domínio.
- [ ] **Rastreie os testes até os requisitos.** Cada teste deve referenciar um REQ-ID em um comentário inline.

## Exemplo do SIFAP

No Estágio 2, o QA Engineer valida se cada requisito EARS em `spec.md` tem critérios de aceitação testáveis. No Estágio 3, escreve testes JUnit 5 e Testcontainers para os cenários confirmados na especificação e nas evidências do legado. Cada método de teste cita o REQ-ID correspondente.

## Referências

- [Google Testing Blog](https://testing.googleblog.com/)
- [xUnit Test Patterns — Gerard Meszaros](http://xunitpatterns.com/)
- [Software Testing ISTQB](https://www.istqb.org/)
- [Property-Based Testing — jqwik/fast-check](https://jqwik.net/)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Visão geral das personas](../OVERVIEW.md)<br/><sub>Tabela das 10 personas e suas duplas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil completo da persona QA Engineer.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
