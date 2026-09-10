# Software Architect: kit do Copilot

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › **Software Architect**

**Inventário do kit do Copilot para a persona Software Architect.** Lista os artefatos ativos, onde estão localizados em `.github/` e as boas práticas específicas deste papel.

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que atua como Software Architect na imersão |
| **Dupla** | 2 · Arquitetura (com o Enterprise Architect) |
| **Fase do SDLC** | Design → Supervisão da Implementação |
| **Pré-requisitos** | Leitura de [PERSONA.md](PERSONA.md) concluída |
| **Resultado esperado** | Kit validado e prompts acessíveis no GitHub Copilot |

> [!IMPORTANT]
> Leia [PERSONA.md](PERSONA.md) antes de continuar. O perfil explica a missão, o handoff e as rubricas de avaliação.

---

## Conceito

O Software Architect é responsável pela estrutura interna do sistema. Esse papel define como os módulos são organizados, onde começam e terminam os bounded contexts (limites do Domain-Driven Design) e quais abstrações são expostas. No SIFAP (Sistema de Fiscalização e Administração de Pagamentos), esse papel produz o plano técnico que a equipe de implementação seguirá: `CODEMAP.md`, a estrutura de pacotes e os ADRs de design interno.

---

## Kit da persona

| **Artefato** | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, handoff, prompts e rubrica |
| `.github/agents/software-architect.agent.md` | Agente | Arquitetura de software |
| `.github/prompts/persona-software-architect-codemap.prompt.md` | Prompt | `/codemap` |
| `.github/prompts/persona-software-architect-impl-plan.prompt.md` | Prompt | `/impl-plan` |
| `.github/prompts/persona-software-architect-api-validate.prompt.md` | Prompt | `/api-validate` |
| `.github/instructions/backend.instructions.md` | Instruções | Convenções de backend |
| `.github/instructions/frontend.instructions.md` | Instruções | Convenções de frontend |

---

## Onde ficam os artefatos

Os artefatos ativos estão consolidados no diretório `.github/` da raiz:

| **Tipo** | Caminho |
|---|---|
| Agentes | `.github/agents/` |
| Prompts | `.github/prompts/persona-*.prompt.md` |
| Skills | `.github/skills/` |
| Instruções | `.github/instructions/` |

Use esse diretório como referência. Os arquivos ativos ficam somente no diretório `.github/` da raiz. Edite-os nesse local quando for necessária alguma manutenção.

Se o kit incluir `mcp.json` e a pessoa facilitadora solicitar MCP local, copie somente esse arquivo para `.vscode/mcp.json`.

---

## Boas práticas

- Prefira composição a herança, limites claros a abstrações genéricas e dados claros a código engenhoso.
- Contratos de API são um compromisso público. Quebre-os somente com versionamento e um guia de migração.
- Mantenha as regras de negócio fora do banco de dados e do framework.
- Um diretório `util` em crescimento geralmente indica a ausência de um bounded context.

---

## Referências

- [Arquitetura Limpa: Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design: Eric Evans](https://www.domainlanguage.com/ddd/)
- [Arquitetura Hexagonal: Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)
- [Guias de Arquitetura do Microsoft .NET](https://learn.microsoft.com/dotnet/architecture/)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [OVERVIEW](../OVERVIEW.md)<br/><sub>Tabela das 10 personas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil desta persona.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
