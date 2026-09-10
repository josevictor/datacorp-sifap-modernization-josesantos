---
name: "acceptance-check"
description: "Produza um relatório de conformidade que relacione cada critério de aceitação de spec.md à respectiva implementação e ao teste."
argument-hint: "feature=NNN-feature-name"
agent: "product-owner"
tools: ["read", "search"]
---
# /acceptance-check

## Objetivo

Produzir um relatório de conformidade baseado em evidências. O relatório relaciona cada critério de aceitação Dado/Quando/Então em `specs/<NNN>-<feature>/spec.md` à implementação e ao teste correspondentes. Cada item recebe a classificação Aprovado, Lacuna ou Reprovado, com uma referência `file:line`.

## Quando usar

Durante o teste de aceitação pela pessoa usuária (UAT) ou a revisão do ciclo de trabalho, depois que a implementação e os testes da funcionalidade existirem.

## Pré-condições

- `specs/<NNN>-<feature>/spec.md` existe com REQ-IDs e critérios de aceitação
- O código e os testes da camada de serviços e/ou da interface acessada pelo navegador existem para a funcionalidade

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature>`
- Opcional: um subconjunto de REQ-IDs para verificação (padrão: todos)
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Extrairei cada REQ-ID e seus critérios Dado/Quando/Então da especificação
- Pesquisarei o código de implementação em `backend/` (camada de serviços) e `frontend/` (interface acessada pelo navegador) e citarei `file:line`
- Pesquisarei nos testes uma referência ao REQ-ID (o mesmo sinal relatado pela tarefa de integração contínua, ou CI, `spec-traceability`)
- Classificarei cada critério: Aprovado (código e teste encontrados), Lacuna (somente código, sem teste) ou Reprovado (sem código)
- Resumirei Lacunas e Reprovações como riscos priorizados

## O que não farei

- Afirmar que um critério foi aprovado sem citar o código E uma referência de teste
- Modificar código, testes ou a especificação. Esta é uma revisão somente leitura
- Inventar o comportamento de um código que não consigo localizar. Marcarei o item como Lacuna ou Reprovado e informarei o que falta
- Julgar se o requisito está correto ou é contraditório. Encaminharei essa análise para `/contradiction-check` com o Especialista em Requisitos (`@requirements-engineer`)

## Formato da saída

Um relatório apresentado à equipe:

```markdown
## Relatório de aceitação: 001-pagamento-beneficio

| REQ-ID | Critério (Dado/Quando/Então) | Implementação (file:line) | Teste (file:line) | Status |
|---|---|---|---|---|
| REQ-PAY-014 | Dado um beneficiário inativo, quando o lote for executado, então a linha será rejeitada | backend/.../PaymentBatchService.java:132 | backend/.../PaymentBatchServiceTest.java:88 | Aprovado |
| REQ-PAY-021 | Dado um valor corrigido, quando ele for persistido, então será arredondado para 2 casas decimais | backend/.../BenefitAmount.java:57 | — | Lacuna |
| REQ-PAY-030 | Dada uma linha duplicada, quando ela for enviada, então será ignorada | — | — | Reprovado |

### Principais riscos
1. REQ-PAY-030 (Reprovado): o tratamento de duplicidades não foi implementado e impede a liberação.
2. REQ-PAY-021 (Lacuna): o arredondamento foi implementado, mas não foi testado, o que cria risco de regressão.
```

## Definição de pronto

- [ ] Cada REQ-ID no escopo aparece no relatório
- [ ] Cada critério tem uma célula de Implementação e Teste, ou um travessão explícito com um motivo
- [ ] Cada status é Aprovado, Lacuna ou Reprovado e tem referências comprobatórias
- [ ] As Lacunas e Reprovações estão resumidas como riscos priorizados
- [ ] Nenhum arquivo de código, teste ou especificação foi modificado

## Corpo do prompt

Você atua como Responsável pelo Produto (`@product-owner`) e verifica a entrega em relação à especificação, não à intenção.

**Etapa 1: carregue a especificação.**
Leia `specs/<NNN>-<feature>/spec.md` e liste cada REQ-ID com seus critérios de aceitação.

**Etapa 2: localize as implementações.**
Pesquise o comportamento em `backend/` e `frontend/`. Prefira referências a REQ-IDs em Javadoc ou comentários. Se não houver, pesquise o comportamento. Cite `file:line`.

**Etapa 3: localize os testes.**
Pesquise a sequência textual do REQ-ID em `backend/src/test` e nos arquivos de teste em `frontend/`. É exatamente isso que a tarefa de CI `spec-traceability` procura. Cite `file:line`.

**Etapa 4: classifique.**
Aprovado = código e teste; Lacuna = código sem teste; Reprovado = sem código. Seja rigoroso: sem referência, não há aprovação.

**Etapa 5: resuma o risco.**
Liste primeiro as Reprovações e depois as Lacunas, começando pelo maior impacto no negócio.

Mantenha a revisão somente leitura e cite todas as evidências. Nunca alegue uma cobertura que você não possa indicar. Quando não encontrar o código, classifique como Lacuna ou Reprovado, nunca como suposição.

## Exemplo de chamada

```
/acceptance-check feature=001-pagamento-beneficio
```
