---
name: "generate-adr"
description: "Elabora um Registro de Decisão de Arquitetura (ADR) para uma escolha de projeto específica feita pela equipe."
argument-hint: "title=\"Map Adabas MU fields to JSONB vs ElementCollection\""
agent: "architect"
tools: ["read", "search", "edit"]
---
# /generate-adr

## Objetivo

Criar um Architecture Decision Record (ADR) formal para uma escolha específica, registrando opções, trade-offs avaliados, decisão e consequências.

## Quando usar

Quando houver pelo menos duas opções viáveis durante a Etapa 2 ou posteriormente.

## Pré-condições

- A equipe identificou a decisão
- Existem pelo menos duas opções; uma única opção não exige ADR

## Entradas que a equipe deve fornecer

- Título da decisão
- No mínimo duas opções
- Restrições da especificação EARS ou dos contextos delimitados

## O que farei

- Estruturarei a decisão no formato MADR
- Listarei prós e contras específicos do contexto
- Apresentarei a análise para a equipe decidir
- Registrarei decisão, data, justificativa e consequências positivas e negativas

## O que não farei

- Decidir pela equipe
- Escrever ADR com uma só opção
- Usar trade-offs genéricos ou inventar métricas e benchmarks

## Formato da saída

Um arquivo `02-modern-spec/ADRs/adr-NNN-<slug>.md`:

```markdown
# ADR-NNN: [Título]
- Status: Proposto (até validação explícita da equipe)
- Data: [YYYY-MM-DD]
- Contexto: ...
- Decisão: ...
- Opções consideradas:
  ## Opção 1: ...
  ## Opção 2: ...
- Consequências:
  - Positivas: ...
  - Negativas: ...
- Requisitos relacionados: REQ-NNN
```

Consulte [`02-modern-spec/templates/ADR.template.md`](../../02-modern-spec/templates/ADR.template.md).

## Definição de pronto

- [ ] O ADR segue MADR e contém todas as seções
- [ ] Há pelo menos duas opções com prós e contras específicos
- [ ] Decisão e data estão claras
- [ ] Consequências positivas e negativas foram registradas
- [ ] REQ-IDs relacionados estão listados quando aplicáveis

## Corpo do prompt

Você é `@architect`. A equipe precisa documentar uma decisão arquitetural.

**Etapa 1 — Esclarecer a decisão.**
Pergunte: qual é a decisão, por que precisa ser tomada agora e quais opções estão em avaliação. Se houver uma opção, pergunte quais alternativas foram rejeitadas e explique que um ADR com uma só opção é um padrão, não uma decisão.

**Etapa 2 — Reunir o contexto.**
Consulte `specs/<NNN>-<feature>/spec.md`, `02-modern-spec/bounded-contexts.md` e `01-archaeology/discovery-report.md`.

**Etapa 3 — Analisar cada opção.**
Registre descrição prática, até três prós, até três contras, risco e esforço relativo, sempre específicos ao contexto.

**Etapa 4 — Apresentar e solicitar a decisão.**
Pergunte qual opção a equipe escolhe e peça o motivo em uma frase. Não sugira padrão.

**Etapa 5 — Documentar.**
Use título `ADR-NNN`, status Proposed até validação, data atual, contexto, decisão, todas as opções, consequências e REQ-IDs.

**Etapa 6 — Numerar e arquivar.**
Verifique `02-modern-spec/ADRs/`, use o próximo número e escreva `adr-NNN-<slug>.md`, com slug em kebab-case. Crie o diretório se necessário.

## Exemplo de chamada

```
/generate-adr title="Map Adabas MU fields to JSONB vs ElementCollection"
```
