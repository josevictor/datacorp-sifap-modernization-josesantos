# ADR-0001: Fonte única de verdade para instruções de agentes (sem AGENTS.md na raiz)

> **Trilha:** [Kit do Time](../../README.md) › [Documentação](../README.md) › [ADRs](README.md) › **ADR-0001**

| Campo | Valor |
|---|---|
| **Status** | accepted |
| **Data** | 2026-08-17 |
| **Autores** | Auditoria do harness |
| **Substitui** | N/A |

---

## Contexto

O GitHub Copilot lê vários tipos de arquivos de instruções personalizadas. Este repositório já fornece `.github/copilot-instructions.md` (para todo o repositório) e os arquivos `.github/instructions/*.instructions.md` com escopo por caminho. Ele **não** tem um `AGENTS.md` na raiz, e surgiu a dúvida sobre adicionar um, pois tanto a convenção aberta [agents.md](https://agents.md/) quanto o Copilot CLI leem `AGENTS.md`.

O risco a considerar é o desvio. Um segundo arquivo de instruções para todo o repositório pode divergir silenciosamente do primeiro, fazendo com que os agentes recebam orientações contraditórias conforme o arquivo carregado por cada superfície. A skill harness-engineering (`.github/skills/harness-engineering/SKILL.md`) é explícita: "Adicione o menor harness útil. Prefira atualizar arquivos existentes a adicionar orientações duplicadas."

Dois fatos determinam a decisão.

**1. Cobertura das superfícies — `AGENTS.md` não amplia o alcance aqui.** Toda superfície do Copilot que lê `AGENTS.md` também lê `.github/copilot-instructions.md`:

| Superfície | Lê `.github/copilot-instructions.md` | Lê `AGENTS.md` |
|---|---|---|
| Copilot CLI (ferramenta opcional de terminal deste repositório) | Sim | Sim |
| VS Code — Copilot Chat | Sim | Sim |
| VS Code — agente na nuvem / revisão de código | Sim | Sim |
| GitHub.com — agente na nuvem | Sim | Sim |
| GitHub.com — revisão de código | Sim | Sim |
| GitHub.com — Copilot Chat | Sim | Não |

A própria saída de `/help` do Copilot CLI lista `AGENTS.md` e `.github/copilot-instructions.md` como locais respeitados. O Copilot Chat no GitHub.com lê `.github/copilot-instructions.md`, mas **não** `AGENTS.md`; portanto, o arquivo para todo o repositório é o único respeitado por todas as superfícies.

**2. Precedência — o arquivo do repositório já tem prioridade sobre `AGENTS.md`.** Quando mais de um arquivo se aplica, todos são fornecidos ao Copilot, mas, em caso de conflito, a ordem é (da maior para a menor prioridade): pessoal → `.github/instructions/**` específico por caminho → **`.github/copilot-instructions.md` para todo o repositório** → **`AGENTS.md` do agente** → organização. Portanto, um novo `AGENTS.md` nunca venceria uma divergência com o arquivo existente; apenas poderia se desviar dele. Arquivos `AGENTS.md` aninhados são aceitos (vence o mais próximo na árvore), o que multiplicaria a superfície de desvio em vez de reduzi-la.

## Decisão

**Não** adicionaremos um `AGENTS.md` na raiz (nem `CLAUDE.md` / `GEMINI.md`). `.github/copilot-instructions.md` permanece a fonte única de verdade para instruções de agentes em todo o repositório, complementada por `.github/instructions/*.instructions.md` com escopo por caminho. A seção "Strict Rules" de `.github/copilot-instructions.md` agora proíbe adicionar um arquivo concorrente de instruções na raiz, aplicando a regra no ponto em que uma pessoa colaboradora poderia violá-la.

## Alternativas consideradas

| Alternativa | Por que foi rejeitada |
|---|---|
| Adicionar um `AGENTS.md` completo que espelhe as instruções | Duplicação pura de um arquivo que já é lido universalmente; duas fontes de verdade para todo o repositório se afastariam, exatamente a regressão que esta auditoria existe para evitar. |
| Adicionar um `AGENTS.md` mínimo que apenas aponte para `.github/copilot-instructions.md` | Adiciona um arquivo a manter para um benefício quase nulo: toda superfície que o lê já lê o destino, e o repositório proíbe assistentes que não sejam o Copilot, eliminando o valor entre ferramentas que é a principal vantagem de `AGENTS.md`. Ainda seria um link sujeito a ficar inválido. |

## Consequências

- **Mais fácil:** um único local para editar; nenhuma conciliação entre dois arquivos para todo o repositório; nenhuma superfície recebe orientações conflitantes.
- **Mais difícil:** uma pessoa colaboradora que espera um `AGENTS.md` precisa aprender a convenção. Isso é mitigado pela Strict Rule explícita e por este ADR.
- **Riscos:** se o GitHub tornar `AGENTS.md` o único arquivo lido por uma superfície obrigatória, esta decisão precisará ser revista.
- **Mitigações:** a Strict Rule aponta para este documento; a verificação de desvio das primitivas do Copilot (`.github/scripts/validate-copilot-primitives.py`, acompanhada separadamente) é o lugar natural para garantir "nenhum `AGENTS.md` avulso na raiz" caso uma aplicação ativa seja desejada depois.

## Relacionados

- REQ-IDs: N/A
- ADRs: N/A
- Arquivos de instruções: `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`

## Referências

- GitHub Docs — Sobre a personalização das respostas do GitHub Copilot (precedência das instruções personalizadas): <https://docs.github.com/en/copilot/concepts/response-customization>
- GitHub Docs — Compatibilidade com diferentes tipos de instruções personalizadas (qual superfície lê cada arquivo): <https://docs.github.com/en/copilot/reference/custom-instructions-support>
- GitHub Docs — Como adicionar instruções personalizadas ao repositório (`AGENTS.md` aninhados, vence o mais próximo): <https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions>
- Convenção aberta agents.md: <https://agents.md/>

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [ADRs — Índice](README.md)<br/><sub>Índice das decisões registradas.</sub> | [Documentação](../README.md)<br/><sub>Índice dos recursos transversais do kit.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
