---
name: "impl-plan"
description: "Estruture o plan.md de uma funcionalidade em fases ordenadas por dependências, com marcadores de paralelismo, perfis de capacidade e critérios mensuráveis de saída."
argument-hint: "feature=NNN-feature-name"
agent: "software-architect"
tools: ["read", "search", "edit"]
---
# /impl-plan

## Objetivo

Organizar tarefas em `plan.md` por dependência, paralelismo seguro, perfil de capacidade e critérios mensuráveis, sem inventar escopo.

## Quando usar

Na Etapa 2, depois de `spec.md`, projeto inicial e `tasks.md`, antes da implementação.

## Pré-condições

- Cada REQ-ID tem `source_legacy:`
- O Monólito Modular e as tarefas estão definidos

## Entradas que a equipe deve fornecer

- Identificador e tarefas

## O que farei

- Criarei fases foundation, features e hardening
- Marcarei `[P]` somente com arquivos distintos e sem dependência de execução, comprovados por grep
- Usarei perfis deep reasoning, implementation ou mechanical conforme [`model-routing.md`](../../09-cheat-sheets/model-routing.md)
- Definirei saídas mensuráveis e riscos

## O que não farei

- Fixar modelo, inventar tarefa/REQ-ID, escrever código ou projetar arquitetura

## Formato da saída

Fases com `Task ID | Título | [P] | Perfil de capacidade | Esforço | Rastreia`, critérios e tabela de riscos.

## Definição de pronto

- [ ] Toda tarefa rastreia REQ-ID, dura até um dia e tem perfil
- [ ] `[P]` tem evidência; fases têm critérios; riscos têm mitigação

## Corpo do prompt

Você é `@software-architect`. Leia `spec.md`, `plan.md` e `tasks.md`. Ordene fundação, funcionalidades e robustecimento. Marque paralelismo apenas após verificar arquivos e dependências. Atribua perfil, nunca modelo. Defina testes, documentação e revisão verificáveis por fase. Registre riscos, sobretudo regra legada não confirmada. Decomponha tarefas acima de um dia.

## Exemplo de chamada

```
/impl-plan feature=014-registration
```
