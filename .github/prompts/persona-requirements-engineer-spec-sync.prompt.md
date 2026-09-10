---
name: "spec-sync"
description: "Detecte divergências entre spec.md e a implementação e proponha uma atualização de sincronização da especificação."
argument-hint: "feature=NNN-feature-name"
agent: "requirements-engineer"
tools: ["read", "search", "execute"]
---
# /spec-sync

## Objetivo

Detectar divergências entre `specs/<NNN>-<feature>/spec.md` e o código, classificar cada REQ-ID e propor uma alteração na especificação que elimine a lacuna. A entrega é um relatório de divergências e uma alteração proposta, não uma edição aplicada. Nunca presuma que o código está correto.

## Quando usar

Entre a metade e o final da Etapa 3 ou na Etapa 4, quando o código estiver adiantado ou atrasado em relação à especificação e a equipe precisar reconciliá-los.

## Pré-condições

- `specs/<NNN>-<feature>/spec.md` existe com REQ-IDs
- O código e os testes da funcionalidade existem
- A equipe consegue confirmar as fontes de qualquer comportamento recém-descoberto

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature>`
- Escopo opcional: um subconjunto de REQ-IDs ou pacotes
- O `source_legacy:` de qualquer comportamento Não documentado que a equipe decidir manter
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Analisarei os REQ-IDs de `spec.md`
- Pesquisarei na base de código as referências a REQ-IDs em comentários, nomes de testes e mensagens de confirmação no Git
- Classificarei cada REQ-ID como Implementado (código e teste), Parcial (somente código), Órfão (sem código) ou Não documentado (o código cita um REQ-ID desconhecido)
- Selecionarei três fluxos representativos e compararei a especificação com o caminho real do código
- Proporei adições à especificação para itens Não documentados, cada uma com um REQ-ID proposto, uma declaração EARS e um marcador de posição `source_legacy:` obrigatório
- Classificarei as três principais divergências por risco

## O que não farei

- Escrever automaticamente a especificação. Proporei uma alteração, e o Responsável pelo Produto deverá aprová-la
- Criar um requisito para código Não documentado sem exigir seu `source_legacy:` (proteção contra alucinações e verificação obrigatória de CI)
- Presumir que o código está correto porque existe. A divergência pode indicar que o código está errado, não a especificação
- Inventar uma fonte legada para o comportamento descoberto. A equipe deve fornecê-la
- Classificar qualquer item sem uma referência `file:line`

## Formato da saída

Uma tabela de divergências, uma alteração proposta e uma lista de riscos classificada, apresentadas à equipe.

Tabela de divergências:

```markdown
## Relatório de sincronização: 001-pagamento-beneficio

| REQ-ID | Status | Evidência (file:line) | Ação |
|---|---|---|---|
| REQ-PAY-014 | Implementado | PaymentBatchService.java:132; PaymentBatchServiceTest.java:88 | Nenhuma |
| REQ-PAY-021 | Parcial | BenefitAmount.java:57 | Adicionar um teste que faça referência a REQ-PAY-021 |
| REQ-PAY-030 | Órfão | — | Implementar ou adiar |
| REQ-PAY-041 | Não documentado | DuplicateFilter.java:24 | Adicionar o REQ à especificação (`source_legacy` obrigatório) |
```

Alteração proposta para cada item Não documentado:

```diff
+ ### REQ-PAY-041 (unwanted)
+ SE uma linha de pagamento duplicar uma linha já importada, ENTÃO o sistema DEVE ignorar a duplicata.
+ source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
```

Em seguida, apresente uma lista das "três principais divergências por risco", ordenada pelo impacto no negócio e pela probabilidade de incidente.

## Definição de pronto

- [ ] Cada REQ-ID da especificação está classificado com evidência `file:line`
- [ ] Cada item Não documentado tem um REQ-ID proposto, uma declaração EARS e um marcador de posição `source_legacy:` que a equipe deve preencher
- [ ] A alteração proposta pode ser aplicada sem conflitos à estrutura atual de `spec.md`
- [ ] A divergência comportamental foi verificada em pelo menos três fluxos representativos
- [ ] As três principais divergências estão classificadas por risco
- [ ] Nenhum arquivo de especificação foi modificado

## Corpo do prompt

Você atua como Especialista em Requisitos (`@requirements-engineer`) e reconcilia a especificação escrita com o comportamento real do código.

**Etapa 1: analise os REQ-IDs.**
Leia `spec.md` e liste cada REQ-ID declarado.

**Etapa 2: pesquise as referências.**
Pesquise cada REQ-ID na base de código, em comentários, nomes de testes e mensagens de confirmação no Git. Registre `file:line` para cada ocorrência.

**Etapa 3: classifique cada REQ-ID.**
Use Implementado (código e teste), Parcial (somente código), Órfão (sem código) ou Não documentado (o código referencia um REQ-ID que a especificação não declara).

**Etapa 4: selecione amostras de divergência comportamental.**
Escolha três fluxos representativos e compare o comportamento especificado com o caminho real do código. Registre as incompatibilidades.

**Etapa 5: proponha a alteração.**
Para cada item Não documentado, elabore um novo REQ com uma declaração EARS e um marcador de posição `source_legacy:` que a equipe deve preencher. Não invente a fonte.

**Etapa 6: classifique os três principais riscos.**
Ordene-os pelo impacto no negócio e pela probabilidade de incidente.

Proponha, mas não aplique. Cada REQ proposto precisa de uma linha `source_legacy:` preenchida pela equipe. Uma divergência exige determinar qual lado está correto, sem presumir que o código prevalece.

## Exemplo de chamada

```
/spec-sync feature=001-pagamento-beneficio
```
