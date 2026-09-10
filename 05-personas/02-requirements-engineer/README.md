# Requirements Engineer — Kit do Copilot

> **Trilha:** [Kit do time](../../README.md) › [Personas](../OVERVIEW.md) › **Requirements Engineer**

**Inventário do kit do Copilot para a persona Requirements Engineer.** Lista os artefatos ativos, onde ficam em `.github/` e as boas práticas específicas dessa função.

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que atua como Requirements Engineer na imersão |
| **Dupla** | 1 · Visão (com Product Owner) |
| **Fase do SDLC** | Requisitos → Especificação |
| **Pré-requisitos** | Leitura de [PERSONA.md](PERSONA.md) concluída |
| **Resultado esperado** | Kit validado e prompts acessíveis no GitHub Copilot |

> [!IMPORTANT]
> Leia [PERSONA.md](PERSONA.md) antes de continuar. O perfil explica a missão, o handoff e as rubricas de avaliação.

---

## Conceito

Requirements Engineer é a pessoa responsável por transformar conversas e descobertas em requisitos formais e testáveis. No SIFAP (Sistema de Fiscalização e Administração de Pagamentos), as regras de negócio estão codificadas tacitamente em Natural, sem documentação atualizada. RE extrai essas regras, estrutura-as usando EARS (Easy Approach to Requirements Syntax) e garante a rastreabilidade do sistema legado até o requisito moderno.

---

## Kit da persona

| **Artefato** | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, handoff, prompts e rubrica |
| `.github/agents/requirements-engineer.agent.md` | Agent | Análise de requisitos |
| `.github/prompts/persona-requirements-engineer-spec-sync.prompt.md` | Prompt | `/spec-sync` |
| `.github/prompts/persona-requirements-engineer-contradiction-check.prompt.md` | Prompt | `/contradiction-check` |
| `.github/prompts/persona-requirements-engineer-ears-convert.prompt.md` | Prompt | `/ears-convert` |
| `.github/instructions/requirements.instructions.md` | Instruções | Convenções da documentação de requisitos |

---

## Onde ficam os artefatos

Os artefatos ativos estão consolidados no diretório `.github/` da raiz:

| **Tipo** | Caminho |
|---|---|
| Agentes | `.github/agents/` |
| Prompts | `.github/prompts/persona-*.prompt.md` |
| Skills | `.github/skills/` |
| Instruções | `.github/instructions/` |

Use esse diretório como referência. Os arquivos ativos ficam somente no diretório `.github/` da raiz. Edite-os nesse local quando houver necessidade de manutenção.

Se o kit incluir `mcp.json` e a pessoa facilitadora solicitar o MCP local, copie somente esse arquivo para `.vscode/mcp.json`.

---

## Boas práticas

- Use exclusivamente os padrões EARS; requisitos vagos devem ser quantificados.
- Cada `REQ-ID` deve ser único, imutável e rastreável a pelo menos um teste e uma tarefa.
- Faça uma verificação de contradições antes de aceitar novas especificações.
- Remova ou quantifique termos ambíguos como "adequado", "razoável" e "fácil de usar".

---

## Referências

- [EARS Notation — Alistair Mavin](https://alistairmavin.com/ears/)
- [IEEE 29148 — Requirements Engineering](https://www.iso.org/standard/72089.html)
- [ISO/IEC 25010 — Quality Model](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)
- [Writing Good Requirements — INCOSE](https://www.incose.org/)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Visão geral](../OVERVIEW.md)<br/><sub>Tabela das 10 personas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil desta persona.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
