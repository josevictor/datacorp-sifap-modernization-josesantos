---
name: "setup-project"
description: "Inicialize a estrutura de engenharia de contexto do Copilot de um projeto: AGENTS.md, CODEMAP.md e a base de instruções, prompts e agentes em .github."
argument-hint: "root=<repo-root>"
agent: "tech-lead"
tools: ["read", "search", "edit", "execute"]
---
# /setup-project

## Objetivo

Criar `AGENTS.md`, `CODEMAP.md`, `.github/copilot-instructions.md` e bases de instructions, prompts e agents específicas da stack, com escopo e sem segredos. Não criar protótipo.

## Quando usar

No início do projeto ou quando faltar superfície de contexto.

## Pré-condições

- Raiz gravável e concordância com [`copilot-instructions.md`](../copilot-instructions.md)

## Entradas que a equipe deve fornecer

- Raiz e stack, se indetectável

## O que farei

- Detectarei stack por manifests; criarei AGENTS com comandos verificados, CODEMAP com Modules/Data Flow/External Integrations e arquivos `.github/` com `applyTo` específico
- Prepararei as mudanças sem commit, listarei arquivos e recomendarei `/audit-context`

## O que não farei

- Criar aplicação, `backend/`, `frontend/` ou `infra/`; usar conteúdo genérico, `applyTo: "**"`, segredo, credencial ou `TODO`; adicionar ferramenta não aprovada

## Formato da saída

Lista de arquivos preparados, mensagem de commit sugerida e três acompanhamentos manuais.

## Definição de pronto

- [ ] AGENTS é específico; todos os escopos são concretos
- [ ] Sem segredo ou TODO; `.gitignore` ajustado
- [ ] Mudanças preparadas, não commitadas, e acompanhamentos listados

## Corpo do prompt

Você é `@tech-lead`. Detecte `package.json`, `pom.xml`, `requirements.txt` e `*.csproj`; pergunte se nada existir. Escreva AGENTS com stack e comandos. Crie CODEMAP com `## Modules`, `## Data Flow`, `## External Integrations`, deixando módulos para `/update-codemap`. Registre linguagem, tom, segurança e ferramentas no copilot-instructions sem repetir o global. Crie instructions com globs como `backend/**/*.java`, nunca `**`, conforme [`instructions/README.md`](../instructions/README.md). Prepare com git sem commit e informe caminhos absolutos, mensagem sugerida e três ações. Não crie protótipo nem placeholder.

## Exemplo de chamada

```
/setup-project root=.
```
