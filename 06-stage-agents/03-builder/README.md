# @builder — Estágio 3: Implementação

> **Trilha:** [Kit do time](../../README.md) › [Agentes de estágio](../README.md) › **@builder**

**O agente `@builder` executa a especificação do Estágio 2 e transforma requisitos EARS em código Java 21 + Spring Boot + Next.js 15 com testes rastreáveis e migrações Flyway.**

| Campo | Valor |
|---|---|
| **Público-alvo** | Developer (líder), Technical Lead, DBA e QA Engineer durante o Estágio 3 |
| **Pré-requisitos** | Handoff do Estágio 2 com `spec.md`, `plan.md`, `tasks.md` e um primeiro incremento priorizado |
| **Tempo estimado** | 15:00–16:10 |
| **Estágio** | Estágio 3 — Implementação |
| **Resultado esperado** | Backend e frontend compilam, os testes passam e os commits incluem `Implements REQ-...` |

![Estágio 3](https://img.shields.io/badge/Est%C3%A1gio-3%20%C2%B7%20Implementa%C3%A7%C3%A3o-171717?style=flat-square)
![Abordagem construtiva](https://img.shields.io/badge/Abordagem-Construtiva-404040?style=flat-square)

---

## Quando usar

Use este agente quando a especificação existir e o time precisar construir. O `@builder` não substitui o design. Ele executa `spec.md`, `plan.md` e `tasks.md` por meio de código, testes e rastreabilidade.

- **Liderança:** Developer
- **Apoio direto:** Technical Lead, DBA, QA Engineer e Software Architect
- **Pré-requisito obrigatório:** `spec.md`, `plan.md` e `tasks.md` existem, e o primeiro incremento está priorizado

---

## O que o agente faz

- Traduz regras Natural/Adabas para Java 21 com rastreabilidade por REQ-ID
- Gera entidades JPA a partir dos DDMs do Adabas e explica cada mapeamento
- Cria controllers REST em `/api/v1/...` com DTOs, Bean Validation e anotações OpenAPI
- Escreve testes JUnit 5 com Testcontainers para regras de negócio críticas
- Gera migrações Flyway idempotentes
- Cria páginas Next.js 15 App Router que consomem endpoints REST

---

## O que o agente NÃO faz

- Não escreve código sem um REQ-ID referenciado na especificação
- Não cria uma nova arquitetura; segue os ADRs e o plano técnico do Estágio 2
- Não registra CPF, valores de benefícios nem dados sensíveis em logs
- Não pula testes para avançar mais rápido; pelo menos o teste mínimo da regra crítica é obrigatório

---

## Entradas

| Entrada | Local |
|---|---|
| Especificação da feature | `specs/<NNN>-<feature>/spec.md` |
| Plano técnico | `specs/<NNN>-<feature>/plan.md` |
| Lista de tarefas | `specs/<NNN>-<feature>/tasks.md` |
| ADRs de arquitetura | `02-modern-spec/` ou `docs/adr/` |
| DDMs mapeados | `01-archaeology/business-rules-catalog.md` |

---

## Saídas esperadas

| Artefato | Local |
|---|---|
| Código do backend Java 21 | `backend/src/main/java/` |
| Migrações Flyway | `backend/src/main/resources/db/migration/` |
| Testes JUnit 5 | `backend/src/test/java/` |
| Código do frontend Next.js | `frontend/` |
| Commits rastreáveis | Mensagem: `Implements REQ-NNN: <short description>` |

---

## Como selecionar o agente no GitHub Copilot

- [ ] **Abra o GitHub Copilot** no VS Code (`Ctrl+Alt+I` / `Cmd+Alt+I`).
- [ ] **Selecione `@builder`** no seletor de agentes.
- [ ] **Abra `tasks.md`** e identifique a próxima tarefa a implementar.
- [ ] **Cole o prompt de abertura** abaixo e pressione Enter.

```text
Estou iniciando o Estágio 3 — Implementação.
Temos spec.md, plan.md, tasks.md, ADRs e um modelo de dados.
Ajude a implementar a próxima tarefa rastreável com Java 21 + Spring Boot,
PostgreSQL/JPA e Next.js, começando pelos testes das regras de negócio.
```

---

## Exemplos de prompts

| Situação | Prompt útil |
|---|---|
| Entidade JPA | "Gere a entidade a partir deste DDM e explique cada mapeamento." |
| Regra Natural | "Traduza esta regra para Java com nomes claros e um teste de equivalência." |
| Controller REST | "Crie um controller em `/api/v1/...` com DTOs, validação e OpenAPI." |
| Frontend | "Crie uma página Next.js App Router que consuma este endpoint sem expor segredos." |
| Testes | "Escreva um teste JUnit para REQ-NNN e adicione o comentário de rastreabilidade." |

---

## Definição de pronto

- [ ] O backend compila e `mvn test` (ou equivalente) passa.
- [ ] O frontend compila e `npm test` (ou equivalente) passa quando existe um frontend.
- [ ] O primeiro incremento da feature funciona dentro do escopo selecionado.
- [ ] Uma interface ou endpoint existe somente quando o escopo exige.
- [ ] As migrações Flyway são aplicadas sem erros em um banco de dados limpo.
- [ ] Os testes citam REQ-IDs em comentários inline.
- [ ] Os commits que implementam comportamento mencionam `Implements REQ-...`.

---

## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| Código sem REQ-ID | A tarefa começou sem consultar a especificação | Retorne a `tasks.md` e encontre o requisito correspondente |
| Nova decisão de arquitetura no Estágio 3 | Uma especificação incompleta chegou ao builder | Pause, resolva no Estágio 2 com `@architect` e depois retome |
| Teste ignorado por pressão de tempo | Pressão de entrega | Escreva pelo menos o teste mínimo da regra crítica antes do commit |
| CPF ou valor aparece nos logs | A política de dados foi ignorada | Mascare os logs; nunca registre `cpf`, `valor` ou `beneficio` diretamente |

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [@architect](../02-architect/README.md)<br/><sub>Estágio 2: especificação moderna com Spec-Kit.</sub> | [@evolution](../04-evolution/README.md)<br/><sub>Estágio 4: delegue, revise e registre o resultado.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
