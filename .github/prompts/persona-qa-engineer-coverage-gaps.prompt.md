---
name: "coverage-gaps"
description: "Audite a cobertura de testes por REQ-ID e informe requisitos não testados, casos-limite ausentes e lacunas entre especificação e testes, ordenados por risco."
argument-hint: "feature=<NNN>-<feature> scope=all|diff|REQ-COMP"
agent: "qa-engineer"
tools: ["read", "search", "execute"]
---
# /coverage-gaps

## Objetivo

Auditar a cobertura de testes no SIFAP 2.0 e entregar uma lista priorizada de **requisitos não testados ou testados de forma insuficiente**, não uma porcentagem. A cobertura de linhas é uma métrica de vaidade; a cobertura de requisitos é o que importa. O relatório pode ser colado em um tíquete de planejamento da iteração. Ele apresenta primeiro o maior risco e inclui uma orientação de teste em uma linha para cada lacuna.

## Quando usar

Antes de declarar um contexto delimitado como concluído, durante a revisão de uma solicitação de incorporação (PR) ou antes do planejamento da iteração. Use sempre que a equipe precisar saber quais requisitos foram realmente verificados e quais foram somente executados.

## Pré-condições

- `specs/<NNN>-<feature>/spec.md` declara os `REQ-ID`s no escopo
- As fontes de implementação e teste existem em `backend/` e/ou `frontend/`
- Um relatório de cobertura está disponível ou pode ser gerado (JaCoCo XML para o servidor e Vitest LCOV para a interface)

## Entradas que a equipe deve fornecer

- A pasta da funcionalidade (`specs/<NNN>-<feature>/`) e as pastas de implementação
- Um relatório de cobertura recente ou permissão para gerar um
- O escopo: todos os `REQ-ID`s da pasta, somente as diferenças deste PR ou somente o conjunto regulatório `REQ-COMP-*`

Peça à pessoa usuária qualquer informação ausente.

## O que farei

- Criarei um inventário de requisitos com base em `spec.md`, indexado por `REQ-ID` e padrão EARS
- Cruzarei a saída da tarefa `spec-traceability` em `.github/workflows/spec-quality.yml` para identificar os `REQ-ID`s que a integração contínua (CI) já sinaliza como não testados
- Mapearei cada `REQ-ID` para seus testes e o classificarei como `MISSING`, `WEAK` ou `OK`
- Inspecionarei variantes EARS para identificar casos negativos e de transição de estado ocultos
- Verificarei de forma genérica os casos-limite derivados do legado em `01-archaeology/legacy-sifap/natural-programs/`
- Pontuarei cada lacuna por risco e entregarei a lista priorizada

## O que não farei

- Inventar comportamento do SIFAP, requisito ausente ou caso-limite do legado. Referencio `01-archaeology/legacy-sifap/` de forma genérica e consulto a equipe quando um valor é desconhecido
- Escrever os testes (`/create-tests`), implementar correções (`@builder`) ou editar a especificação (`@requirements-engineer`)
- Informar uma porcentagem de cobertura de linhas como se fosse cobertura de comportamento
- Considerar testes redundantes do fluxo de sucesso como suficientes ou tratar testes de captura da interface de usuário (UI) como cobertura de requisitos da experiência do usuário (UX)
- Sugerir orientações que verifiquem detalhes de implementação (métodos privados ou strings SQL)

## Formato da saída

Um relatório Markdown retornado em linha:

```markdown
## Relatório de lacunas de cobertura: <feature>

### Resumo
- Requisitos no escopo: 12
- OK: 7; WEAK: 3; MISSING: 2
- Lacuna de maior risco: REQ-014 (o valor não positivo não é rejeitado)

### Lacunas por risco

| REQ-ID | Padrão EARS | Status | Risco (P×I) | Orientação |
|--------|-------------|--------|-------------|------------|
| REQ-014 | Indesejado | MISSING | 9 | adicionar teste negativo para valor <= mínimo |
| REQ-021 | Orientado por estado | WEAK | 6 | adicionar teste de transição de reentrada |
| REQ-015 | Orientado por evento | WEAK | 4 | adicionar teste negativo para "o evento não ocorreu" |

### Casos-limite derivados do legado ainda não cobertos
- Limite de um programa Natural em `01-archaeology/legacy-sifap/natural-programs/`: confirmar com a equipe e depois mapear para REQ-014.

### Adições de testes sugeridas
1. `AmountRuleTest#should_reject_when_amount_below_minimum`
2. `StatusMachineTest#should_allow_reentry_after_exit`
```

## Definição de pronto

- [ ] Cada `REQ-ID` no escopo aparece exatamente uma vez no relatório
- [ ] Cada lacuna tem uma pontuação de risco (probabilidade × impacto) e uma orientação de teste em uma linha
- [ ] Requisitos negativos ou de comportamento indesejado sem teste negativo estão marcados como `WEAK` ou `MISSING`
- [ ] Os casos-limite derivados do legado são verificados explicitamente em `01-archaeology/legacy-sifap/natural-programs/`
- [ ] As três principais lacunas incluem nomes de testes acionáveis e prontos para atribuição
- [ ] A saída pode ser colada em um tíquete de planejamento da iteração

## Corpo do prompt

Você é `@qa-engineer` e audita se os requisitos foram realmente verificados. Siga a pirâmide e a filosofia de cobertura em [`../skills/test-strategy/SKILL.md`](../skills/test-strategy/SKILL.md).

**Etapa 1: crie o inventário de requisitos.**
Analise `spec.md` e extraia cada `REQ-ID` com seu padrão EARS e critérios de aceitação.

**Etapa 2: encontre testes por REQ-ID.**
Pesquise nas fontes de teste por `REQ-NNN`, `@Tag("REQ-NNN")`, `@implements REQ-NNN`, `describe('REQ-NNN', ...)` e convenções de nomenclatura como `Req014_*`. Cruze os resultados com a tarefa `spec-traceability` em `.github/workflows/spec-quality.yml`, que já lista os `REQ-ID`s declarados em `specs/`, mas não referenciados pelos testes.

**Etapa 3: mapeie o teste para o requisito.**
Para cada `REQ-ID`, liste os testes que fornecem cobertura e classifique-o como `MISSING` (nenhum), `WEAK` (somente um teste de fluxo de sucesso) ou `OK` (fluxo de sucesso e pelo menos um caso de limite ou erro).

**Etapa 4: inspecione as variantes EARS em busca de casos ocultos.**
Requisitos orientados por evento e de comportamento indesejado (`SE...`) quase sempre precisam de um teste negativo. Requisitos orientados por estado (`ENQUANTO...`) precisam de um teste de transição. Sinalize todos os que não tiverem esses testes.

**Etapa 5: confira o sistema legado.**
Para requisitos mapeados para um programa Natural em `01-archaeology/legacy-sifap/natural-programs/`, confirme a cobertura dos casos-limite identificados pela equipe na Etapa 1. Referencie os caminhos de forma genérica. Não afirme o que um programa específico calcula.

**Etapa 6: pontue por risco.**
Classifique a probabilidade (frequência de execução em produção) e o impacto (financeiro, regulatório ou de segurança) em uma escala de 1 a 3. Risco = probabilidade × impacto. Apresente primeiro o maior risco.

**Etapa 7: entregue a lista priorizada de lacunas.**
Inclua uma orientação de uma linha para cada lacuna. Descreva o formato do teste ausente, não o código do teste. Inclua nomes acionáveis para as três principais lacunas.

Informe a cobertura de requisitos, nunca somente um número de cobertura de linhas. Um `REQ-ID` com cinco testes de "deve funcionar" e nenhum teste de "não deve funcionar" é `WEAK`. Cada lacuna recebe uma pontuação de risco. Nunca invente um requisito ou caso-limite do legado. Sinalize o que for desconhecido e consulte a equipe.

## Exemplo de chamada

```
/coverage-gaps feature=<NNN>-<feature> scope=all
```
