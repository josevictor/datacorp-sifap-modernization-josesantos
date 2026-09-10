# Enterprise Architect: kit do Copilot

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › **Enterprise Architect**

**Inventário do kit do Copilot para a persona Enterprise Architect.** Lista os artefatos ativos, onde estão localizados em `.github/` e as boas práticas específicas deste papel.

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que atua como Enterprise Architect na imersão |
| **Dupla** | 2 · Arquitetura (com o Software Architect) |
| **Fase do SDLC** | Arquitetura → Design → Segurança |
| **Pré-requisitos** | Leitura de [PERSONA.md](PERSONA.md) concluída |
| **Resultado esperado** | Kit validado e prompts acessíveis no GitHub Copilot |

> [!IMPORTANT]
> Leia [PERSONA.md](PERSONA.md) antes de continuar. O perfil explica a missão, o handoff e as rubricas de avaliação.

---

## Conceito

O Enterprise Architect enxerga o sistema dentro de seu ecossistema. No SIFAP (Sistema de Fiscalização e Administração de Pagamentos), isso significa mapear dependências externas, como SIAFI, Banco do Brasil, INCRA e MDA, e garantir que a arquitetura-alvo respeite os contratos existentes. O EA sabe onde estão os contratos, quais são frágeis e quais podem ser alterados sem desencadear uma sequência de efeitos imprevistos.

---

## Kit da persona

| **Artefato** | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, handoff, prompts e rubrica |
| `.github/agents/enterprise-architect.agent.md` | Agente | Arquitetura e segurança |
| `.github/prompts/persona-enterprise-architect-create-constitution.prompt.md` | Prompt | `/create-constitution` |
| `.github/prompts/persona-enterprise-architect-create-adr.prompt.md` | Prompt | `/create-adr` |
| `.github/prompts/persona-enterprise-architect-architecture-review.prompt.md` | Prompt | `/architecture-review` |
| `.github/instructions/security.instructions.md` | Instruções | Convenções de segurança |
| `.github/instructions/infrastructure.instructions.md` | Instruções | Convenções de IaC |
| `hooks.json` | Hooks | Bloqueios de edição para `.specify/memory/constitution.md` |

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

- Use C4 L1/L2 para a visão executiva e L3/L4 para a implementação.
- Toda decisão arquitetural precisa de um ADR com contexto, decisão e consequências.
- Prefira uma arquitetura previsível e operável em produção.
- Use os pilares do Azure Well-Architected como gates de revisão, não como um checklist tardio.

---

## Referências

- [Modelo C4: Simon Brown](https://c4model.com/)
- [Microsoft Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/)
- [Registros de decisão de arquitetura](https://adr.github.io/)
- [Centro de Arquitetura do Azure](https://learn.microsoft.com/azure/architecture/)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [OVERVIEW](../OVERVIEW.md)<br/><sub>Tabela das 10 personas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil desta persona.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
