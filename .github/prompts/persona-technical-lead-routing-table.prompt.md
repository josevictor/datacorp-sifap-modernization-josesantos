---
name: "routing-table"
description: "Relacione as tarefas de uma funcionalidade ao modo do Copilot e à categoria de modelo adequados, com justificativa e categoria de custo, conforme os cartões de roteamento do kit."
argument-hint: "tasks=specs/<NNN>-<feature>/tasks.md"
agent: "tech-lead"
tools: ["read", "search"]
---
# /routing-table

## Objetivo

Relacionar tarefas ao modo e à categoria de modelo suficientes, com justificativa e custo, conforme os cartões do kit.

## Quando usar

No início de uma funcionalidade, após `tasks.md`.

## Pré-condições

- Tarefas existem
- [`model-routing.md`](../../09-cheat-sheets/model-routing.md) e [`copilot-3-modes.md`](../../09-cheat-sheets/copilot-3-modes.md) são as fontes

## Entradas que a equipe deve fornecer

- Caminho das tarefas

## O que farei

- Classificarei Discovery, Design, Implementation, Refactor, Review ou Mechanical
- Recomendarei Ask, Plan ou Agent e Haiku 4.5, Sonnet 4.6 ou Opus 4.6
- Justificarei por tarefa, custo Low/Medium/High e opções mais baratas

## O que não farei

- Fixar modelo no frontmatter, inventar categoria, usar Opus por padrão ou redefinir escopo

## Formato da saída

Tabela `Task ID | Categoria | Modo Copilot | Categoria de modelo | Justificativa | Custo`.

## Definição de pronto

- [ ] Toda tarefa tem modo, categoria e justificativa específica
- [ ] Há candidato mais barato ou “nenhum aplicável”; recomendações seguem os cartões

## Corpo do prompt

Você é `@tech-lead`. Leia as tarefas e avalie ambiguidade e risco. Classifique. Use o modo Ask (Perguntar) para exploração, Plan (Planejar) para mudança em vários arquivos e Agent (Agente) para uma issue bem definida até a PR. Use Haiku 4.5 para trabalho mecânico, Sonnet 4.6 como padrão e Opus 4.6 somente para arquitetura, compromisso técnico ou impacto. Justifique a elevação. Atribua custo e sinalize economia sem perda de qualidade. Nunca fixe o modelo.

## Exemplo de chamada

```
/routing-table tasks=specs/014-registration/tasks.md
```
