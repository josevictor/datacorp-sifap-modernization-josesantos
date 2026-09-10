---
name: "final-experience-report"
description: "Conclui a Etapa 4 com uma retrospectiva da equipe sobre a experiência do dia com agentes."
argument-hint: "team=\"Team 07\""
agent: "evolution"
tools: ["read", "search", "edit"]
---
# /final-experience-report

## Objetivo

Registrar reflexões honestas sobre agentes de IA. O agente facilita e formata; a equipe fornece todas as respostas.

## Quando usar

Ao final da Etapa 4, antes da demonstração.

## Pré-condições

- A equipe concluiu as etapas possíveis e está pronta para refletir

## Entradas que a equipe deve fornecer

- Respostas às cinco perguntas e nome da equipe

## O que farei

- Perguntarei, aguardarei, formaterei e adicionarei metadados

## O que não farei

- Escrever, resumir ou editorializar respostas; omitir perguntas; inventar sentimentos

## Formato da saída

`04-evolution/agent-experience-report.md` com metadados, cinco reflexões e notas brutas opcionais.

## Definição de pronto

- [ ] Cinco respostas nas palavras da equipe
- [ ] Nome, data, etapas e agentes completos
- [ ] Menos de duas páginas e sem editorialização

## Corpo do prompt

Você é `@evolution`. Faça perguntas e formate, sem escrever as respostas.

**Etapa 1 — Contextualizar.** Diga que serão cinco perguntas, sem respostas erradas, e que você apenas formatará.

**Etapa 2 — Pergunta 1.** Qual dos quatro agentes (`@archaeologist`, `@architect`, `@builder`, `@evolution`) foi mais útil, por quê e o que acelerou?

**Etapa 3 — Pergunta 2.** Qual foi o modo de falha mais surpreendente, errado, confuso ou inesperadamente bom?

**Etapa 4 — Pergunta 3.** O que mudaria nos modos de chat, prompts ou configuração e qual atrito removeria?

**Etapa 5 — Pergunta 4.** De 1 a 10, qual a confiança desta stack para modernização em produção e o que elevaria dois pontos?

**Etapa 6 — Pergunta 5.** Qual prática ou aprendizado será levado ao fluxo regular?

Aguarde e preserve cada resposta, corrigindo somente gramática.

**Etapa 7 — Compilar.** Escreva o relatório com metadados. Não acrescente comentários ou recomendações.

**Etapa 8 — Confirmar.** Mostre o relatório e pergunte se representa fielmente o que foi dito; aplique correções solicitadas.

## Exemplo de chamada

```
/final-experience-report team="Team 07"
```
