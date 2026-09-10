# @evolution — Estágio 4: Evolução

> **Trilha:** [Kit do time](../../README.md) › [Agentes de estágio](../README.md) › **@evolution**

**O agente `@evolution` orienta o time a transformar o trabalho local do Estágio 3 em uma entrega revisável: Issues bem escritas para o modo Agent do Copilot, revisão de PR, registros de CI/CD e relatório de experiência.**

| Campo | Valor |
|---|---|
| **Público-alvo** | Technical Lead (líder), DevOps Engineer, Tech Writer, Developer e QA Engineer |
| **Pré-requisitos** | Handoff do Estágio 3 com backend/frontend funcionando e testes relevantes |
| **Tempo estimado** | 16:10–16:50 |
| **Estágio** | Estágio 4 — Evolução |
| **Resultado esperado** | Issue criada ou rascunhada, PR revisado ou próximo passo registrado e relatório de experiência concluído |

![Estágio 4](https://img.shields.io/badge/Est%C3%A1gio-4%20%C2%B7%20Evolu%C3%A7%C3%A3o-171717?style=flat-square)
![Abordagem operacional](https://img.shields.io/badge/Abordagem-Operacional-404040?style=flat-square)

---

## Quando usar

Use este agente quando o protótipo existir e o time precisar transformar o trabalho local em uma entrega revisável: Issues, PRs, CI/CD, IaC, runbook e relatório final.

- **Liderança:** Technical Lead
- **Apoio direto:** DevOps Engineer, Tech Writer, Developer e QA Engineer
- **Pré-requisito obrigatório:** protótipo com backend/frontend funcionando e testes relevantes

---

## O que o agente faz

- Ajuda a estruturar Issues pequenas e revisáveis para o modo Agent do Copilot
- Orienta a revisão de PR com ênfase em bugs, riscos, regressões e testes ausentes
- Cria ou ajusta workflows do GitHub Actions e IaC somente quando forem relevantes para a entrega
- Converte comandos isolados em um runbook de operações
- Produz o relatório de experiência do modo Agent (`agent-experience-report.md`)

---

## O que o agente NÃO faz

- Não delega uma Issue vaga ao modo Agent; exige contexto, escopo e critérios de aceitação
- Não aprova um PR gerado por IA sem revisão humana explícita
- Não cria novas features no Estágio 4; adiciona-as ao backlog
- Não oculta pendências; documenta os riscos e registra o próximo passo

---

## Entradas

| Entrada | Local |
|---|---|
| Backend/frontend do Estágio 3 | `backend/`, `frontend/` |
| Pendências conhecidas | Notas do handoff do Estágio 3 |
| `spec.md` da feature | `specs/<NNN>-<feature>/spec.md` |
| ADRs e plano técnico | `02-modern-spec/` ou `docs/adr/` |

---

## Saídas esperadas

| Artefato | Local |
|---|---|
| Issue para o modo Agent | GitHub Issues do repositório |
| Revisão de PR (se disponível) | GitHub Pull Requests |
| Workflow de CI/CD (se relevante) | `.github/workflows/` |
| Runbook (se relevante) | `docs/runbook.md` |
| Relatório de experiência do Agent | `04-evolution/agent-experience-report.md` |

---

## Como selecionar o agente no GitHub Copilot

- [ ] **Abra o GitHub Copilot** no VS Code (`Ctrl+Alt+I` / `Cmd+Alt+I`).
- [ ] **Selecione `@evolution`** no seletor de agentes.
- [ ] **Abra a lista de pendências do Estágio 3** no editor.
- [ ] **Cole o prompt de abertura** abaixo e pressione Enter.

```text
Estou iniciando o Estágio 4 — Evolução.
Temos um protótipo com backend, frontend e testes.
Ajude a revisar uma Issue pequena para o Copilot Agent e registrar o resultado
da delegação. Não invente requisitos, arquitetura nem critérios.
```

---

## Exemplos de prompts

| Situação | Prompt útil |
|---|---|
| Issue para o modo Agent | "Escreva uma Issue pequena com contexto, arquivos relevantes, critérios de aceitação e itens fora do escopo." |
| Revisão de PR | "Revise este PR e priorize bugs, riscos, regressões e testes ausentes." |
| CI/CD | "Crie um workflow do GitHub Actions para build, teste e validação do Terraform." |
| Runbook | "Transforme estes comandos em um runbook para uma nova pessoa do time de operações." |
| Relatório final | "Escreva o `agent-experience-report` com o que funcionou, o que falhou e o que aprendemos." |

---

## Definição de pronto

- [ ] Uma Issue pequena foi criada ou deixada como rascunho revisável com contexto, escopo e critérios de aceitação.
- [ ] Um PR disponível recebeu revisão humana; se não houver PR, o próximo passo está documentado.
- [ ] O status de CI/IaC foi registrado sem criar infraestrutura apenas para cumprir uma meta.
- [ ] O relatório de experiência do modo Agent está completo.

---

## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| O modo Agent produz um resultado fora do escopo | Issue vaga sem critérios explícitos | Reescreva a Issue com contexto, arquivos relevantes e itens fora do escopo |
| PR gerado por IA integrado sem revisão | Confiança excessiva no resultado do Agent | Revise-o exatamente como revisaria um PR humano |
| Uma nova feature aparece no fim | Controle de escopo insuficiente | Adicione-a ao backlog; não a implemente no Estágio 4 |
| Pendências ocultadas para proteger a demo | Receio de avaliação | Documente o risco e a solução temporária; o objetivo é a transparência |

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [@builder](../03-builder/README.md)<br/><sub>Estágio 3: crie a implementação rastreável.</sub> | [Agentes de estágio — visão geral](../README.md)<br/><sub>Visão geral dos 4 agentes e do cronograma da imersão.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
