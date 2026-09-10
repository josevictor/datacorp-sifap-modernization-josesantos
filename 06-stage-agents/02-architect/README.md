# @architect — Estágio 2: Especificação

> **Trilha:** [Kit do time](../../README.md) › [Agentes de estágio](../README.md) › **@architect**

**O agente `@architect` transforma as evidências coletadas no Estágio 1 em uma especificação moderna rastreável e usa o GitHub Spec-Kit para produzir `spec.md`, `plan.md` e `tasks.md`.**

| Campo | Valor |
|---|---|
| **Público-alvo** | Dupla de Arquitetura (Enterprise Architect + Software Architect) durante o Estágio 2 |
| **Pré-requisitos** | Handoff do Estágio 1 com catálogo de regras e entradas `source_legacy:` disponíveis |
| **Tempo estimado** | 14:00–15:00 |
| **Estágio** | Estágio 2 — Especificação |
| **Resultado esperado** | `spec.md`, `plan.md` e `tasks.md` em `specs/<NNN>-<feature>/`, aprovados pelo Product Owner |

![Estágio 2](https://img.shields.io/badge/Est%C3%A1gio-2%20%C2%B7%20Especifica%C3%A7%C3%A3o-171717?style=flat-square)
![Abordagem analítica](https://img.shields.io/badge/Abordagem-Anal%C3%ADtica-404040?style=flat-square)

---

## Quando usar

Use este agente depois que o time tiver descobertas do legado e precisar transformá-las em uma especificação moderna. O `@architect` ajuda a definir bounded contexts, escrever requisitos EARS, registrar ADRs e preparar a implementação.

- **Liderança:** Software Architect
- **Apoio direto:** Requirements Engineer, Enterprise Architect, Product Owner e Technical Lead
- **Pré-requisito obrigatório:** evidência do Estágio 1 com `source_legacy:` para cada regra

---

## O que o agente faz

- Transforma regras de negócio catalogadas em requisitos EARS com `source_legacy:`
- Compara alternativas de bounded context e identifica prós e contras
- Gera ADRs com contexto, opções, decisão, consequências e riscos
- Executa `/speckit.specify`, `/speckit.clarify` e `/speckit.plan` com base na especificação
- Identifica lacunas na especificação antes da implementação

---

## O que o agente NÃO faz

- Não aceita um requisito sem evidência do legado ou justificativa `[GREENFIELD]`
- Não escreve código de implementação (essa é a função do `@builder`)
- Não preenche campos ou fluxos ambíguos sem uma resolução explícita
- Não decide o escopo sem a validação do Product Owner

---

## Entradas

| Entrada | Local |
|---|---|
| Catálogo de regras do Estágio 1 | `01-archaeology/business-rules-catalog.md` |
| Mapa de dependências | `01-archaeology/dependency-map.md` |
| Questões em aberto | `01-archaeology/mysteries-found.md` |
| Relatório de descoberta | `01-archaeology/discovery-report.md` |
| Checklist de exploração do legado | `01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md` |

---

## Saídas esperadas

| Artefato | Local |
|---|---|
| Especificação da feature | `specs/<NNN>-<feature>/spec.md` |
| Plano técnico | `specs/<NNN>-<feature>/plan.md` |
| Lista de tarefas implementáveis | `specs/<NNN>-<feature>/tasks.md` |
| Decisões de escopo de apoio | `02-modern-spec/` (somente apoio, não é um segundo local de especificação) |

---

## Como selecionar o agente no GitHub Copilot

- [ ] **Abra o GitHub Copilot** no VS Code (`Ctrl+Alt+I` / `Cmd+Alt+I`).
- [ ] **Selecione `@architect`** no seletor de agentes.
- [ ] **Abra o catálogo de regras do Estágio 1** no editor.
- [ ] **Cole o prompt de abertura** abaixo e pressione Enter.

```text
Estou iniciando o Estágio 2 — Especificação.
Temos um relatório de descoberta, catálogo de regras, glossário, DDMs e mapa de dependências.
Ajude a transformar evidências confirmadas em `spec.md`, `plan.md` e
`tasks.md` para uma feature fina. Não preencha requisitos nem a arquitetura
sem uma fonte e registre as questões em aberto separadamente.
```

---

## Exemplos de prompts

| Situação | Prompt útil |
|---|---|
| Regra de negócio bruta | "Confirme a fonte desta regra antes de propor um requisito EARS com `source_legacy:`." |
| Fronteira incerta de bounded context | "Compare 2 ou 3 bounded contexts possíveis e apresente prós e contras." |
| Decisão de arquitetura | "Gere um ADR com contexto, opções, decisão, consequências e riscos." |
| Plano técnico | "Prepare `/speckit.plan` considerando Modular Monolith, JPA e PostgreSQL." |

---

## Definição de pronto

- [ ] `spec.md`, `plan.md` e `tasks.md` existem em `specs/<NNN>-<feature>/`.
- [ ] Todo requisito tem `source_legacy:` apontando para `.NSP`, `.NSN` ou `.ddm`, ou `[GREENFIELD]` com uma justificativa.
- [ ] As decisões de escopo de apoio estão em `02-modern-spec/`.
- [ ] O Product Owner revisou e aprovou o escopo durante o handoff das 15:00.

---

## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| Requisito sem `source_legacy:` | Regra deduzida sem evidência do legado | Retorne ao catálogo do Estágio 1 e encontre a referência de linha |
| A arquitetura é complexa demais para o tempo disponível | A ambição excede o escopo da imersão | Prefira decisões simples e testáveis que possam ser implementadas em uma hora |
| ADR misturado com opinião sem estrutura | O registro não tem estrutura | Use o modelo: contexto, opções, decisão e consequências |
| A especificação não tem critério de aceitação | O requisito não é testável | Todo requisito precisa de pelo menos um cenário verificável |

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [@archaeologist](../01-archaeologist/README.md)<br/><sub>Estágio 1: leia o sistema legado Natural/Adabas.</sub> | [@builder](../03-builder/README.md)<br/><sub>Estágio 3: crie a implementação rastreável.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
