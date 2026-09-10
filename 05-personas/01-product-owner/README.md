# Product Owner — Kit do Copilot

> **Trilha:** [Kit do time](../../README.md) › [Personas](../OVERVIEW.md) › **Product Owner**

**Inventário do kit do Copilot para a persona Product Owner.** Lista os artefatos ativos, onde ficam em `.github/` e as boas práticas específicas dessa função.

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que atua como Product Owner na imersão |
| **Dupla** | 1 · Visão (com Requirements Engineer) |
| **Fase do SDLC** | Descoberta → Especificação → Aceitação |
| **Pré-requisitos** | Leitura de [PERSONA.md](PERSONA.md) concluída |
| **Resultado esperado** | Kit validado e prompts acessíveis no GitHub Copilot |

> [!IMPORTANT]
> Leia [PERSONA.md](PERSONA.md) antes de continuar. O perfil explica a missão, o handoff e as rubricas de avaliação.

---

## Conceito

Product Owner é a pessoa responsável por traduzir as necessidades de negócio em um escopo executável. Em um processo de modernização de legado como o do SIFAP (Sistema de Fiscalização e Administração de Pagamentos), essa função é crítica: sistemas legados acumulam regras implícitas que só fazem sentido quando alguém sabe "por que" elas existem. O PO conecta cada decisão técnica a evidências de negócio.

---

## Kit da persona

| **Artefato** | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, handoff, prompts e rubrica |
| `.github/agents/product-owner.agent.md` | Agent | Assistente de Product Owner para especificação, backlog e aceitação |
| `.github/prompts/persona-product-owner-spec.prompt.md` | Prompt | `/spec`, escreve uma seção de `specs/<NNN>-<feature>/spec.md` com base em histórias de usuário no formato EARS |
| `.github/prompts/persona-product-owner-update-spec.prompt.md` | Prompt | `/update-spec`, atualiza a especificação quando uma feature muda |
| `.github/prompts/persona-product-owner-acceptance-check.prompt.md` | Prompt | `/acceptance-check`, verifica se o código atende aos critérios de aceitação |
| `mcp.json` | MCP | Manifesto de servidores do GitHub + itens de trabalho do Azure DevOps |

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

- Escreva os requisitos em EARS para que cada frase seja testável.
- Mantenha cada história de usuário vinculada a um resultado mensurável.
- Marque as premissas explicitamente. Uma premissa oculta se torna um bug em produção.
- Trate `.specify/memory/constitution.md` como a fonte de verdade para os itens não negociáveis.

---

## Referências

- [EARS Notation — Alistair Mavin](https://alistairmavin.com/ears/)
- [Spec-Driven Development (Spec-Kit)](https://github.com/github/spec-kit)
- [User Story Mapping — Jeff Patton](https://www.jpattonassociates.com/user-story-mapping/)
- [GitHub Copilot for PMs](https://docs.github.com/en/copilot)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Visão geral](../OVERVIEW.md)<br/><sub>Tabela das 10 personas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil desta persona.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
