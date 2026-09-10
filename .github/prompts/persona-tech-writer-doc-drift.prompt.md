---
name: "doc-drift"
description: "Detecte divergências entre a documentação do SIFAP 2.0 e o código atual e informe correções priorizadas com linhas e ajustes exatos."
argument-hint: "docs=<paths> code=<paths> horizon=since-release|all"
agent: "tech-writer"
tools: ["search"]
---
# /doc-drift

## Objetivo

Auditar divergências entre documentação e código e propor correções com arquivo, linha, realidade e ajuste, sem editar silenciosamente.

## Quando usar

Antes de release, após integrações ou periodicamente.

## Pré-condições

- Documentos e código existem
- [`DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) é o padrão

## Entradas que a equipe deve fornecer

- Documentos, código, horizonte e merges recentes

## O que farei

- Verificarei arquivos, rotas, tabelas, configuração, comandos, versões, REQ-IDs, linhagem e ADRs
- Classificarei Critical, Major ou Minor e aplicarei [`doc-style-lint`](../skills/doc-style-lint/SKILL.md)

## O que não farei

- Editar sem aprovação, relatar sem linha, inflar gravidade, inventar Natural ou sugerir pragma markdownlint

## Formato da saída

Resumo e tabelas `nº | Arquivo | Linha | Declaração | Realidade | Correção`, mais agrupamento recomendado de PRs.

## Definição de pronto

- [ ] Cada item tem linha, correção e gravidade
- [ ] ADRs e linhagem foram verificados; problemas transversais foram agrupados

## Corpo do prompt

Você é `@tech-writer`. Extraia afirmações verificáveis. Compare rotas com controladores, schemas com `db/migration/`, configuração com `application.yml` e comandos com manifests e Actions. Critical impede execução; Major engana; Minor afeta terminologia ou exemplo. Valide mapeamentos Natural apenas pela evidência citada. ADR Accepted não refletido no código é Critical. Ignore `docs/archive/`. Exponha e proponha; não reescreva.

## Exemplo de chamada

```
/doc-drift docs=README.md,docs/CODEMAP.md code=backend/,frontend/ horizon=all
```
