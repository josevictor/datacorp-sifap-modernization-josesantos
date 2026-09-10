---
name: "review-agent-pr"
description: "Revisa um PR gerado pelo Copilot Agent na nuvem, com atenção explícita aos modos de falha típicos de IA."
argument-hint: "pr=<number> issue=<slug>"
agent: "evolution"
tools: ["read", "search", "edit", "execute", "github/*"]
---
# /review-agent-pr

## Objetivo

Revisar sistematicamente um PR do Copilot Agent conforme a issue e classificar falhas típicas de IA por gravidade.

## Quando usar

Quando o agente criar um PR delegado.

## Pré-condições

- PR, `04-evolution/issues/<slug>.md` e `04-evolution/delegations/<slug>.md` existem

## Entradas que a equipe deve fornecer

- Número ou branch do PR e slug da issue

## O que farei

- Lerei o diff, compararei critérios, examinarei falhas e produzirei revisão classificada

## O que não farei

- Aprovar, corrigir ou integrar; aceitar comportamento novo sem testes

## Formato da saída

`04-evolution/reviews/<pr-number>.md`, com critérios, varredura de falhas, constatações must-fix/should-fix/can-defer e recomendação.

## Definição de pronto

- [ ] Cada critério tem pass/fail/partial e evidência
- [ ] Sete verificações foram feitas com `file:line`
- [ ] Há classificação e recomendação merge/merge with fixes/reject
- [ ] Ausência de testes é must-fix

## Corpo do prompt

Você é `@evolution`.

**Etapa 1 — Carregar contexto.** Leia issue e lista de acompanhamento.

**Etapa 2 — Obter o diff.** Use somente `gh pr view <pr-number>` e `gh pr diff <pr-number>`. Não execute comandos de mutação. Liste arquivos e sinalize ampliação de escopo.

**Etapa 3 — Verificar critérios.** Classifique **Pass**, **Fail** ou **Partial**, sempre com código específico.

**Etapa 4 — Verificar sete falhas.** Imports inexistentes; APIs fabricadas; testes sem significado como `assertTrue(true)`; divergência comentário-código; ampliação de escopo; tratamento de erros ausente; e violações de estilo como DTOs sem records, injeção sem construtor, campos `@Autowired` ou retornos `null`.

**Etapa 5 — Classificar.** **Must fix**: bugs, segurança, testes quebrados ou ausentes e APIs alucinadas. **Should fix**: estilo, erros incompletos e Javadoc ausente. **Can defer**: melhorias menores e documentação.

**Etapa 6 — Recomendar.** Use **Merge**, **Merge with fixes** ou **Reject**, com justificativa.

**Etapa 7 — Escrever.** Gere o arquivo. Em PR não trivial, registre ao menos um ponto. Se realmente não houver falha, declare que não há must-fix e todos os critérios foram atendidos.

## Exemplo de chamada

```
/review-agent-pr pr=<number> issue=<slug>
```
