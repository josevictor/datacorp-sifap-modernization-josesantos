---
name: "playwright-generate-test"
description: "Gere um teste de ponta a ponta com Playwright a partir de um cenário usando Playwright MCP, delegando o procedimento à skill playwright-generate-test."
argument-hint: "scenario=\"<user flow to test>\""
agent: "qa-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /playwright-generate-test

## Objetivo

Explorar um fluxo de usuário descrito com Playwright MCP e produzir um teste de ponta a ponta TypeScript aprovado com `@playwright/test` para o frontend do SIFAP 2.0. O procedimento completo está na skill [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md). Este prompt o aplica ao frontend Next.js 15 sem repeti-lo.

> [!IMPORTANT]
> Não escreva código de teste somente com base no cenário. Primeiro execute o fluxo etapa por etapa com Playwright MCP e depois gere o teste a partir das etapas observadas.

## Quando usar

Durante as Etapas 3 ou 4, quando a equipe quiser um teste de regressão de ponta a ponta para um fluxo visível à pessoa usuária no frontend Next.js 15.

## Pré-condições

- A aplicação `frontend/` está em execução e acessível
- O Playwright e o servidor Playwright MCP estão disponíveis
- O cenário de teste foi descrito ou será fornecido quando solicitado

## Entradas que a equipe deve fornecer

- `scenario`: o fluxo de usuário a testar; solicite-o se estiver ausente
- A URL-base do frontend em execução
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Seguirei o procedimento de explorar e depois gerar da skill [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md)
- Conduzirei o cenário uma etapa por vez pelo Playwright MCP antes de escrever código
- Produzirei uma especificação TypeScript com `@playwright/test` no diretório `tests/` do frontend
- Executarei e ajustarei o teste até que passe

## O que não farei

- Gerar código de teste prematuramente somente com base no cenário
- Cobrir aqui o comportamento de unidade ou componente; isso permanece no Vitest + Testing Library
- Deixar um teste com falha ou instável
- Fixar segredos ou dados específicos de um ambiente na especificação

## Formato da saída

```markdown
### Gerado
`frontend/tests/payment-approval.spec.ts` — @playwright/test

### Execução
`npx playwright test payment-approval` → 1 passed
```

## Definição de pronto

- [ ] O fluxo foi explorado etapa por etapa com Playwright MCP antes da escrita do código
- [ ] A especificação usa `@playwright/test` e está no diretório `tests/` do frontend
- [ ] O teste passa e não é instável
- [ ] A cobertura de unidade ou componente permanece no Vitest + Testing Library

## Corpo do prompt

A skill [`playwright-generate-test`](../skills/playwright-generate-test/SKILL.md) define o procedimento de exploração e geração orientado por MCP. Leia-a e aplique-a ao cenário.

**Etapa 1 — Obter o cenário.**
Se nenhum cenário foi fornecido, solicite um. Confirme a URL do frontend.

**Etapa 2 — Aplicar a skill.**
Execute o cenário uma etapa por vez com Playwright MCP e gere a especificação `@playwright/test` a partir das etapas registradas.

**Etapa 3 — Respeitar as regras do kit.**
Use como destino o frontend Next.js 15 com App Router, salve a especificação em `frontend/tests/` e não inclua segredos no arquivo.

**Etapa 4 — Verificar.**
Execute o teste e ajuste-o até que passe.

## Exemplo de chamada

```
/playwright-generate-test scenario="approve a pending payment as an analyst"
```
