---
name: "generate-docs"
description: "Gere um documento voltado a pessoas desenvolvedoras (README, runbook, referência de API ou estrutura de ADR) para um módulo do SIFAP 2.0, fiel ao código e ao guia de estilo da documentação."
argument-hint: "type=readme|runbook|api-reference|adr module=<folder> audience=<who>"
agent: "tech-writer"
tools: ["read", "search", "edit"]
---
# /generate-docs

## Objetivo

Gerar README, runbook, referência de API ou estrutura de ADR concisa, navegável e fiel ao código, sem marketing.

## Quando usar

Nas Etapas 3 ou 4, quando houver código suficiente ou documentação desatualizada.

## Pré-condições

- Módulo e fontes da verdade existem
- [`DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) rege conteúdo fora de `.github/`

## Entradas que a equipe deve fornecer

- `type`, módulo, público e REQ-IDs

## O que farei

- Lerei manifests, configuração, controladores, OpenAPI e migrações
- Usarei frontmatter `title`, `audience`, `last_reviewed`, `owner`, `linked_reqs`
- Verificarei comandos, limites, links e data
- Aplicarei [`doc-style-lint`](../skills/doc-style-lint/SKILL.md) e [`adr-draft`](../skills/adr-draft/SKILL.md) para ADR

## O que não farei

- Inventar domínio, endpoint, módulo ou linhagem; usar marketing, emoji, cor saturada ou pragma markdownlint
- Criar requisito ou decisão

## Formato da saída

- README: `<module-folder>/README.md`
- Runbook: `docs/runbooks/<short-slug>.md`
- API: `docs/api/<service>/<endpoint-slug>.md`
- ADR: `docs/adr/<NNNN>-<title>.md`

## Definição de pronto

- [ ] Frontmatter completo; comandos executáveis
- [ ] README ≤ 80 linhas e ADR ≤ duas páginas
- [ ] Dois links relacionados, linhagem confirmada e rodapé de navegação

## Corpo do prompt

Você é `@tech-writer`. Escolha o template pelo objetivo do leitor. Leia o código, não a memória. Cite strings exatas. Respeite limites e verifique cada comando no repositório. Vincule README a CODEMAP, spec e runbook; runbook a painéis e alertas; ADRs relacionados entre si. Use data atual. Execute revisão de estilo: voz ativa, alertas GFM, Mermaid neutro, sem pragma. Termos de domínio podem ficar em pt-BR, mas as explicações permanecem em inglês. Documente realidade atual e planos separadamente.

## Exemplo de chamada

```
/generate-docs type=runbook module=backend/disburse audience="on-call SRE"
```
