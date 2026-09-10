---
name: "design-modular-monolith"
description: "Registra em plan.md somente o projeto do Monólito Modular necessário à funcionalidade selecionada."
argument-hint: "feature=NNN-feature-name"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /design-modular-monolith

## Objetivo

Registrar em `specs/<NNN>-<feature>/plan.md` somente as decisões de projeto que liberam a primeira implementação. Não criar arquitetura genérica, endpoints, contratos nem diagramas sem evidências da funcionalidade.

## Quando usar

Depois que `/write-ears-spec` produzir `specs/<NNN>-<feature>/spec.md`, com `source_legacy:` em cada REQ-ID, e a equipe declarar uma questão concreta de projeto que bloqueie a primeira tarefa, ainda na branch `spec/<NNN>-<feature>`.

> [!NOTE]
> Não use para projetar o sistema inteiro, adicionar módulos sem requisito ou trabalhar antes da especificação. Planeje a menor estrutura necessária.

## Pré-condições

- `spec.md` existe e cada REQ-ID tem `source_legacy:`
- A equipe confirmou o escopo e declarou a questão de projeto

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature-name>`
- A questão concreta que bloqueia a primeira tarefa
- Restrições de dados, integração ou contrato

## O que farei

- Lerei `spec.md`, `plan.md` existente e `02-modern-spec/scope-decisions.md`
- Solicitarei evidências para limites, integrações e contratos não descritos
- Descreverei a menor estrutura de módulos, dados e comunicação necessária
- Criarei diagrama ou contrato somente se resolver uma questão concreta
- Relacionarei cada decisão aos REQ-IDs e decisões de apoio

## O que não farei

- Sugerir microsserviços, escrever código ou preencher requisitos e decisões não confirmados
- Colocar `spec.md`, `plan.md` ou `tasks.md` em `02-modern-spec/`
- Exigir quantidade fixa de módulos, diagramas ou contratos

## Formato da saída

```markdown
# Plano — <NNN>-<feature>

## Módulos (Monólito Modular)

| Módulo | Responsabilidade | Dados próprios (DDM) | Interface em processo | Atende ao REQ-ID |
|---|---|---|---|---|
| `<module>` | <what it owns> | `<DDM>.ddm` | `<Interface>` | REQ-NNN |

## Questões de projeto em aberto
- P: <question the feature evidence does not answer yet> — responsável: <name>, status: open
```

> [!NOTE]
> Adicione um `flowchart` Mermaid somente quando ele resolver uma questão concreta e referencie-o em `plan.md`.

## Definição de pronto

- [ ] `plan.md` descreve somente o necessário à funcionalidade
- [ ] Toda decisão tem evidência ou questão explícita em aberto
- [ ] Artefatos de apoio estão vinculados
- [ ] As duplas 3 e 4 podem iniciar a primeira tarefa sem criar escopo adicional

## Corpo do prompt

Você é `@architect`. Há um `spec.md` apoiado por evidências e uma questão que bloqueia a primeira tarefa. Planeje somente o necessário.

**Etapa 1 — Ler o estado atual.**
Abra `spec.md`, qualquer `plan.md` e `02-modern-spec/scope-decisions.md`. Confirme `source_legacy:` em cada REQ-ID. Se faltar, interrompa e devolva o requisito à equipe.

**Etapa 2 — Declarar a questão.**
Registre a pergunta concreta, por exemplo, “qual módulo possui os dados PAYMENT e como o módulo de benefícios os lê?”. Se faltarem evidências de limite, integração ou contrato, registre uma questão em aberto.

**Etapa 3 — Projetar a menor estrutura.**
Descreva módulo em linguagem de negócio, DDMs ou tabelas exclusivos, interface em processo e REQ-IDs atendidos. Nunca use HTTP entre serviços.

**Etapa 4 — Adicionar diagrama ou contrato somente quando necessário.**
Crie `flowchart` Mermaid ou contrato de interface apenas se resolver a pergunta. Não desenhe o sistema inteiro nem defina endpoints sem requisito.

**Etapa 5 — Relacionar e escrever.**
Vincule decisões e REQ-IDs e escreva em `specs/<NNN>-<feature>/plan.md`. Mantenha os artefatos Spec-Kit em `specs/<NNN>-<feature>/`. Se faltar tempo, reduza o escopo.

## Exemplo de chamada

```text
/design-modular-monolith feature=001-benefit-calculation
```

Espere `specs/001-benefit-calculation/plan.md` somente com módulos, dados próprios e interfaces em processo necessários à primeira tarefa, relacionados a REQ-IDs, e questões pendentes.
