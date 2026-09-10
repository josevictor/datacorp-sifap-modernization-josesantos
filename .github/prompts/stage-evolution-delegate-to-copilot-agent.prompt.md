---
name: "delegate-to-copilot-agent"
description: "Delega uma issue ao GitHub Copilot Agent na nuvem e acompanha o PR resultante."
argument-hint: "issue=04-evolution/issues/<slug>.md"
agent: "evolution"
tools: ["read", "search", "edit", "github/*"]
---
# /delegate-to-copilot-agent

## Objetivo

Orientar a publicação manual de uma issue revisada e preparar o acompanhamento do PR gerado por IA. A equipe revisa e integra.

## Quando usar

Após aprovação de um rascunho de `/write-github-issue`.

## Pré-condições

- Existe `04-evolution/issues/<slug>.md`
- A equipe aprovou e tem acesso de push

## Entradas que a equipe deve fornecer

- Caminho do rascunho e confirmação de publicação

## O que farei

- Orientarei a publicação, criarei lista de acompanhamento e guia de revisão

## O que não farei

- Publicar ou integrar pela equipe, presumir correção do PR ou omitir revisão humana

## Formato da saída

`04-evolution/delegations/<issue-slug>.md`, com referência, resultados esperados, lista de acompanhamento, guia de revisão e responsabilidade.

## Definição de pronto

- [ ] Há instruções de publicação, arquivos e testes esperados, falhas típicas e campo para URL
- [ ] A equipe entende que decide revisão e integração

## Corpo do prompt

Você é `@evolution`.

**Etapa 1 — Confirmar.** Pergunte se o rascunho foi revisado, se critérios são testáveis e se cabe em um PR. Se não, encaminhe a `/write-github-issue`.

**Etapa 2 — Orientar a publicação.**

```bash
# Opção 1: GitHub CLI
gh issue create --title "[title]" --body-file 04-evolution/issues/<slug>.md --label "enhancement,copilot-agent"

# Opção 2: interface do GitHub
# 1. Abra a guia Issues do repositório
# 2. Selecione "New Issue"
# 3. Copie o rascunho
# 4. Adicione enhancement e copilot-agent
# 5. Adicione @copilot ao corpo
```

**Etapa 3 — Acompanhar.** Liste arquivos criados e modificados, testes esperados, tamanho small <100, medium 100–300 ou large 300+, e prazo esperado de minutos.

**Etapa 4 — Revisar.** Verifique imports inexistentes, APIs fabricadas, testes vazios, comentários divergentes, ampliação de escopo, erros não tratados e estilo.

**Etapa 5 — Responsabilidade.** Registre: “Isto é delegação, não automação. A equipe responde pela revisão, pela decisão de integração e pelas consequências. O Copilot Agent contribui, mas não aprova.”

**Etapa 6 — Escrever.** Gere o arquivo e deixe placeholder para URL.

## Exemplo de chamada

```
/delegate-to-copilot-agent issue=04-evolution/issues/<slug>.md
```
