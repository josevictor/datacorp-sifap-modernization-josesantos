# @archaeologist — Estágio 1: Arqueologia

> **Trilha:** [Kit do time](../../README.md) › [Agentes de estágio](../README.md) › **@archaeologist**

**O agente `@archaeologist` orienta o time na leitura sistemática do código legado Natural/Adabas, extrai regras de negócio rastreáveis e mapeia dependências para definir o escopo do Estágio 2.**

| Campo | Valor |
|---|---|
| **Público-alvo** | Todo o time durante o Estágio 1, com todas as duplas trabalhando em paralelo |
| **Pré-requisitos** | `01-archaeology/legacy-sifap/` disponível no workspace |
| **Tempo estimado** | 11:00–12:00 + 13:30–14:00 |
| **Estágio** | Estágio 1 — Arqueologia |
| **Resultado esperado** | Catálogo de regras com fontes, DDMs mapeados, questões em aberto e escopo da feature definido |

![Estágio 1](https://img.shields.io/badge/Est%C3%A1gio-1%20%C2%B7%20Arqueologia-171717?style=flat-square)
![Abordagem investigativa](https://img.shields.io/badge/Abordagem-Investigativa-404040?style=flat-square)

---

## Quando usar

Use este agente enquanto o time lê o código legado. O `@archaeologist` ajuda o time a observar, catalogar e formular perguntas. Ele não escreve código moderno nem inventa regras de negócio.

- **Liderança:** Requirements Engineer
- **Apoio direto:** Tech Writer, Enterprise Architect e DBA
- **Pré-requisito obrigatório:** ler os programas Natural atribuídos antes de escrever qualquer especificação

---

## O que o agente faz

- Orienta a leitura linha a linha dos programas `.NSP` e `.NSN` e das estruturas DDM do Adabas
- Identifica entradas, processamento, saídas e regras de negócio em cada programa
- Mapeia dependências entre programas por meio de `CALLNAT`
- Sugere mapeamentos de campos DDM para PostgreSQL (MU, PE, DE)
- Registra evidências com caminhos de arquivo e referências de linha
- Identifica questões em aberto sem inventar respostas

---

## O que o agente NÃO faz

- Não lê código legado sem que o time abra o arquivo
- Não transforma uma hipótese em requisito confirmado
- Não sugere uma arquitetura moderna (essa é a função do `@architect` no Estágio 2)
- Não edita arquivos em `01-archaeology/legacy-sifap/` (somente leitura)

---

## Entradas

| Entrada | Local |
|---|---|
| Programas Natural atribuídos | `01-archaeology/legacy-sifap/natural-programs/*.{NSP,NSN}` |
| DDMs do Adabas | `01-archaeology/legacy-sifap/adabas-ddms/*.ddm` |
| Checklist de exploração | `01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md` |

---

## Saídas esperadas

| Artefato | Local |
|---|---|
| Catálogo de regras de negócio | `01-archaeology/business-rules-catalog.md` |
| Mapa de dependências (Mermaid) | `01-archaeology/dependency-map.md` |
| Lista de questões em aberto | `01-archaeology/mysteries-found.md` |
| Escopo da feature selecionada | `01-archaeology/discovery-report.md` |

---

## Como selecionar o agente no GitHub Copilot

- [ ] **Abra o GitHub Copilot** no VS Code (`Ctrl+Alt+I` / `Cmd+Alt+I`).
- [ ] **Selecione `@archaeologist`** no seletor de agentes.
- [ ] **Abra o primeiro programa Natural atribuído** no editor antes de enviar o primeiro prompt.
- [ ] **Cole o prompt de abertura** abaixo e pressione Enter.

```text
Estou iniciando o Estágio 1 — Arqueologia.
Temos código Natural/Adabas em 01-archaeology/legacy-sifap/.
Ajude o time a examinar os programas atribuídos e registrar apenas evidências
e questões em aberto para o escopo que selecionaremos. Não deduza respostas.
```

---

## Exemplos de prompts

| Situação | Prompt útil |
|---|---|
| Programa Natural desconhecido | "Leia este programa comigo e separe entrada, processamento, saída e regras de negócio." |
| DDM do Adabas | "Explique estes campos, identifique MU/PE/DE e sugira um mapeamento para PostgreSQL." |
| Regra ambígua | "Não invente uma resposta. Registre como um mistério com hipótese, evidência e impacto." |
| CALLNAT | "Mapeie quem chama quem e gere um diagrama Mermaid simples." |

---

## Definição de pronto

- [ ] A dupla leu integralmente todos os programas Natural atribuídos.
- [ ] Toda regra considerada para o escopo tem `source_legacy:` com arquivo e linha.
- [ ] O time consultou DDMs e dependências quando eles afetam a feature selecionada.
- [ ] As questões em aberto estão registradas sem respostas inventadas.
- [ ] O relatório de descoberta está pronto para o handoff das 14:00.

---

## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| O GitHub Copilot apresenta generalizações vagas | Nenhum arquivo está aberto no editor | Abra o arquivo `.NSP` ou `.NSN` e cite a seção específica no prompt |
| A regra de negócio não tem fonte | O time aceitou uma hipótese como fato | Marque-a como mistério até existir evidência no código |
| O time perde tempo detalhando áreas fora do escopo | Nenhuma decisão de escopo foi tomada | Selecione a feature fina antes das 12:00 e limite a leitura a ela |
| Arquivos legados são editados | Confusão sobre a função do estágio | `01-archaeology/legacy-sifap/` é somente leitura |

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Agentes de estágio — visão geral](../README.md)<br/><sub>Os 4 agentes, o cronograma e a matriz de responsabilidades.</sub> | [@architect](../02-architect/README.md)<br/><sub>Estágio 2: transforme evidências em uma especificação moderna.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
