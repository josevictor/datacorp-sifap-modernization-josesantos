---
name: "update-codemap"
description: "Gere ou atualize docs/CODEMAP.md, um índice curado e navegável da base de código do SIFAP 2.0: módulos, responsáveis, pontos de entrada e testes."
argument-hint: "mode=update|rebuild root=<repo-root>"
agent: "tech-writer"
tools: ["search", "edit"]
---
# /update-codemap

## Objetivo

Manter `docs/CODEMAP.md` como guia de uma página que localize módulo, responsável, entradas e testes em dez minutos.

## Quando usar

Nas Etapas 3 ou 4, após adição ou renomeação.

## Pré-condições

- A equipe criou módulo
- Valem [`DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) e responsáveis de [`05-personas/`](../../05-personas/)

## Entradas que a equipe deve fornecer

- Raiz, `update` ou `rebuild` e mapa anterior

## O que farei

- Registrarei propósito, entradas, estado, REQ-IDs, persona responsável, testes e linhagem confirmada
- Sinalizarei mais de três dependências, ordenarei por valor e limitarei a 200 linhas
- Aplicarei [`doc-style-lint`](../skills/doc-style-lint/SKILL.md)

## O que não farei

- Converter `find` em mapa, inventar Natural, listar cada arquivo, usar `*` para endpoints, equipes como responsáveis, emojis ou pragma

## Formato da saída

`docs/CODEMAP.md` com guia, backend, frontend, infraestrutura, bibliotecas, preocupações e atualização.

## Definição de pronto

- [ ] Cada módulo tem Purpose, Path, Tests, Entry Points, State, REQ-IDs e Owner
- [ ] Linhagem é confirmada; dependências estão declaradas; data e rodapé estão presentes

## Corpo do prompt

Você é `@tech-writer`. Confirme modo e preserve curadoria no update. Localize serviços, rotas e módulos de infraestrutura criados. Registre cinco fatos e persona de `05-personas/`, vincule testes e cite somente linhagem comprovada. Sinalize dependências e ordene jornadas críticas antes da infraestrutura. Limite a 200 linhas ou divida com links. Atualize a data e o rodapé. Não gere automaticamente.

## Exemplo de chamada

```
/update-codemap mode=update root=.
```
