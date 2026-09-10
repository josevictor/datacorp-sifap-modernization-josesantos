---
name: "write-github-issue"
description: "Escreve uma issue de alta qualidade no GitHub, pronta para o Copilot Agent na nuvem."
argument-hint: "feature=\"<scoped-work>\" context=<context> reqs=REQ-XXX"
agent: "evolution"
tools: ["read", "search", "edit", "github/*"]
---
# /write-github-issue

## Objetivo

Criar issue estruturada para execução autônoma pelo Copilot Agent, com critérios claros, caminhos e rastreabilidade por REQ-ID.

## Quando usar

No início da Etapa 4, para trabalho delegável.

## Pré-condições

- Há protótipo da Etapa 3, `spec.md` EARS e trabalho específico

## Entradas que a equipe deve fornecer

- Funcionalidade ou correção, REQ-IDs, contexto e arquivos prováveis

## O que farei

- Estruturarei Context, Acceptance Criteria, Affected Files, Testing Approach e Out of Scope
- Copiarei REQ-IDs sem inventar comportamento e sugerirei labels e assignee

## O que não farei

- Publicar, escrever issue vaga, delegar decisão arquitetural ou correção de segurança, ou omitir testes

## Formato da saída

```markdown
# Issue: [Título]
## Contexto
## Critérios de aceitação
## Arquivos provavelmente afetados
## Abordagem de testes
## Fora do escopo
## Labels
## Requisitos relacionados
```

Grave em `04-evolution/issues/<slug>.md`.

## Definição de pronto

- [ ] As cinco seções existem
- [ ] Critérios são testáveis
- [ ] Há REQ-ID ou declaração justificada de comportamento novo
- [ ] Caminhos e testes estão indicados
- [ ] Cabe em um PR

## Corpo do prompt

Você é `@evolution`.

**Etapa 1 — Entender.** Pergunte o que fazer, qual contexto, se atende `REQ-NNN` ou comportamento novo e quais arquivos.

**Etapa 2 — Contexto.** Descreva estado atual e desejado e vincule EARS.

**Etapa 3 — Critérios.** Copie critérios verificáveis de `spec.md`. Se faltarem, registre a lacuna sem inventar resposta.

**Etapa 4 — Arquivos.** Liste os que serão modificados, criados e apenas consultados.

**Etapa 5 — Testes.** Indique testes unitários, de integração e existentes a atualizar, seguindo padrões locais.

**Etapa 6 — Fora do escopo.** Declare exclusões, como esquema, autenticação ou frontend, para impedir ampliação.

**Etapa 7 — Metadados.** Sugira `enhancement` ou `bug`, contexto e `copilot-agent`.

**Etapa 8 — Rascunho.** Gere `<slug>` em kebab-case. Lembre que a equipe deve revisar e publicar manualmente pela interface ou `gh issue create`.

## Exemplo de chamada

```
/write-github-issue feature="<scoped-work>" context=<context> reqs=REQ-XXX
```
