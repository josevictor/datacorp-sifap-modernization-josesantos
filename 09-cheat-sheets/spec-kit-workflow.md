# Spec-Kit — cartão de referência

> **Trilha:** [Kit do Time](../README.md) › [Cartões de referência](README.md) › **Fluxo do Spec-Kit**

**O Spec-Kit é a ferramenta oficial do GitHub para Spec-Driven Development. Ele impõe a sequência `specify → clarify → plan → tasks → implement` e impede que o time pule direto para o código sem especificação.**

| Campo | Valor |
|---|---|
| **Público-alvo** | Requirements Engineer e Software Architect durante o Estágio 2 |
| **Pré-requisitos** | Spec-Kit instalado (`uv tool install specify-cli`) e `specify init` concluído |
| **Tempo estimado** | 2 min para consultar; aplicado ao longo de todo o Estágio 2 |
| **Estágio** | Estágio 2 — Especificação (e Estágio 3 para o `/speckit.implement`) |
| **Resultado esperado** | `spec.md`, `plan.md` e `tasks.md` em `specs/<NNN>-<feature>/` |

![Cartão 02 de 03](https://img.shields.io/badge/Cart%C3%A3o-02%20de%2003-171717?style=flat-square)
![Tema: Spec-Kit](https://img.shields.io/badge/Tema-Spec--Kit-404040?style=flat-square)

> Repositório oficial: <https://github.com/github/spec-kit>

---

## O que é o Spec-Kit e por que ele existe

O Spec-Kit (Specify CLI) é uma ferramenta de linha de comando e um conjunto de slash commands do Copilot que implementa o fluxo de Spec-Driven Development (SDD). SDD é a prática de escrever a especificação completa de uma funcionalidade — incluindo critérios de aceitação e rastreabilidade — antes de escrever qualquer código.

**Por que isso importa no SIFAP:** toda regra de negócio do legado Natural/Adabas precisa ser rastreável do código legado até um requisito moderno. Sem o Spec-Kit, essa rastreabilidade se perde em conversas de chat. Com ele, todo requisito inclui `source_legacy:` apontando para o arquivo e a linha do código original.

---

## Fluxo canônico

```mermaid
%%{init: {'theme':'neutral','themeVariables':{'fontFamily':'ui-sans-serif, system-ui, sans-serif','primaryColor':'#F5F5F5','primaryTextColor':'#171717','primaryBorderColor':'#171717','lineColor':'#525252','secondaryColor':'#FFFFFF','tertiaryColor':'#FAFAFA','background':'#FFFFFF'}}}%%
flowchart LR
    classDef step fill:#F5F5F5,stroke:#171717,color:#171717
    classDef result fill:#FFFFFF,stroke:#171717,color:#171717,stroke-width:2px

    P0["Constitution"]:::step --> P1["Specify"]:::step --> P2["Clarify"]:::step
    P2 --> P3["Plan"]:::step --> P4["Tasks"]:::step --> P5["Analyze"]:::step
    P5 --> P6["Implement"]:::result
```

| Momento | Comando | Entregável esperado |
|---|---|---|
| Antes da primeira funcionalidade | `/speckit.constitution` | `.specify/memory/constitution.md` |
| Estágio 2 | `/speckit.specify` | `specs/<NNN>-<feature>/spec.md` |
| Estágio 2 | `/speckit.clarify` | Perguntas resolvidas na spec |
| Estágio 2 | `/speckit.plan` | `specs/<NNN>-<feature>/plan.md` |
| Estágio 2 | `/speckit.tasks` | `specs/<NNN>-<feature>/tasks.md` |
| Estágio 3 | `/speckit.analyze` | Lacunas e inconsistências identificadas antes de codificar |
| Estágio 3 | `/speckit.implement` | Código guiado por spec + plan + tasks |

---

## Passo a passo executável

- [ ] **Nomeie a funcionalidade.** Use o formato `NNN-feature-name`.
- [ ] **Crie a spec com `/speckit.specify`.** Inclua user stories, critérios de aceitação e `source_legacy:`.
- [ ] **Resolva as perguntas com `/speckit.clarify`.** Não siga adiante com campos, regras ou fluxos ambíguos.
- [ ] **Gere o plano técnico com `/speckit.plan`.** O plano precisa identificar módulos, contratos, dados e riscos.
- [ ] **Quebre o plano em tarefas com `/speckit.tasks`.** Uma boa tarefa é pequena, testável e tem responsável claro.
- [ ] **Verifique a consistência com `/speckit.analyze`.** Corrija as lacunas antes da implementação.
- [ ] **Implemente com `/speckit.implement`.** O código precisa seguir `spec.md`, `plan.md` e `tasks.md`.

---

## Principais comandos do Copilot

| Comando | Uso |
|---|---|
| `/speckit.constitution` | Cria ou atualiza os princípios e regras do projeto |
| `/speckit.specify` | Cria a spec da funcionalidade com user stories e critérios |
| `/speckit.plan` | Gera o plano técnico a partir da spec |
| `/speckit.tasks` | Quebra o plano em tarefas implementáveis |
| `/speckit.implement` | Executa as tarefas de implementação |

## Comandos opcionais úteis

| Comando | Uso |
|---|---|
| `/speckit.clarify` | Resolve ambiguidades antes do plano técnico |
| `/speckit.analyze` | Analisa a consistência e a cobertura entre os artefatos |
| `/speckit.checklist` | Gera um checklist de qualidade para a spec |
| `/speckit.taskstoissues` | Converte tarefas em GitHub Issues |

---

## Os 6 padrões EARS

EARS (Easy Approach to Requirements Syntax) é uma notação padronizada para escrever requisitos verificáveis. Cada padrão define uma estrutura gramatical que o Copilot consegue reconhecer e validar.

| # | Padrão | Template | Exemplo de sintaxe |
|---|---|---|---|
| 1 | Ubiquitous | O sistema deve `[ação]` | O sistema deve `<ação verificável>` |
| 2 | Event-Driven | Quando `[X]`, o sistema deve `[ação]` | Quando `<evento>`, o sistema deve `<ação>` |
| 3 | State-Driven | Enquanto `[X]`, o sistema deve `[ação]` | Enquanto `<estado>`, o sistema deve `<ação>` |
| 4 | Optional | Onde `[escolha]`, o sistema deve `[ação]` | Onde `<opção>`, o sistema deve `<ação>` |
| 5 | Unwanted | O sistema não deve `[ação]` | O sistema não deve `<comportamento proibido>` |
| 6 | Complex | Enquanto `[X]`, quando `[Y]`, onde `[Z]`, o sistema deve `[ação]` | Combinação dos padrões 2, 3 e 4 |

---

## Estrutura mínima de um requisito do SIFAP

```yaml
REQ-XXX:
  pattern: <padrão EARS>
  text: "<requisito>"
  source_legacy: <arquivo:linhas ou [GREENFIELD] + justificativa>
  acceptance: "<cenário verificável>"
```

> [!WARNING]
> Um requisito sem `source_legacy:` não está pronto para o `/speckit.plan`. O job de CI `legacy-traceability` rejeita PRs que violam essa regra.

---

## Instalação e inicialização

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
specify version
```

Substitua `vX.Y.Z` pela versão mais recente em <https://github.com/github/spec-kit/releases>.

```bash
specify init . --integration copilot
```

No macOS e no Linux, os scripts ficam em `.specify/scripts/bash/`. As funcionalidades geradas pelos comandos ficam em `specs/<NNN>-<feature>/`.

> [!NOTE]
> Se os comandos `/speckit.*` não aparecerem no GitHub Copilot, rode `specify init . --integration copilot` de novo e recarregue o VS Code.

---

## Como adaptá-lo ao SIFAP

- Inclua `source_legacy:` em todo requisito derivado de um arquivo `.NSN` ou `.ddm`.
- Use `[GREENFIELD]` apenas quando não houver equivalente no legado, e justifique a decisão.
- Antes do `/speckit.plan`, valide o escopo com o Product Owner e o Software Architect.
- Antes do `/speckit.implement`, confirme que o `tasks.md` coloca os testes antes do código sempre que a mudança afetar uma regra de negócio.

---

## Referências

- [Spec-Kit no GitHub](https://github.com/github/spec-kit)
- [Documentação oficial](https://github.github.io/spec-kit/)
- [Guia de instalação](https://github.com/github/spec-kit/blob/main/docs/installation.md)
- [Spec-Driven Development](../07-concepts/01-spec-driven-development.md)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Copilot em 3 modos](copilot-3-modes.md)<br/><sub>Quando usar Ask, Plan ou Agent.</sub> | [Escolha de modelo](model-routing.md)<br/><sub>Quando usar Haiku, Sonnet ou Opus.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
