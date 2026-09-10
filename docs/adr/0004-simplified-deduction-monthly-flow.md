# ADR-0004: Manter a dedução simplificada no fluxo mensal e `CALCDSCT` como recálculo sob demanda

> **Trilha:** [Kit do Time](../../README.md) › [Documentação](../README.md) › [ADRs](README.md) › **ADR-0004**

| Campo | Valor |
|---|---|
| **Status** | proposed |
| **Data** | 2026-09-10 |
| **Autores** | Pessoa Desenvolvedora — José Santos |
| **Substitui** | N/A |

> [!IMPORTANT]
> Este ADR propõe a resolução da questão `SIFAP-M-09`. A parte técnica está
> fundamentada em evidência de código. A ratificação depende da Coordenação de
> Benefícios, porque a decisão define qual valor chega à pessoa beneficiária.
> A pendência está registrada em
> [`pending-decisions.md`](../pending-decisions.md).

---

## Contexto

A questão `SIFAP-M-09` registra que o SIFAP possui duas rotinas de desconto com
resultados diferentes para o mesmo valor bruto:

| Bruto | `CALCBENF.CALC-DISC` | `CALCDSCT` |
|---|---|---|
| `400,00` | `0,00` | `12,00` (3%) |
| `500,00` | `0,00` | `15,00` (3%) |
| `600,00` | `18,00` (3%) | `30,00` (5%) |

`CALCBENF` aplica 3% somente **acima** de 500,00
(`CALCBENF.NSN:357-366`). `CALCDSCT` aplica 3% **até** 500,00 e alíquotas
crescentes acima disso (`CALCDSCT.NSP:62-69`). Nenhuma é subconjunto da outra.

A documentação de 2012 afirma que o batch mensal invoca a rotina detalhada:

> "Após o cálculo, os descontos são aplicados pela invocação de CALCDSCT (a
> partir da versão 4.0)"
>
> — `legacy-docs/BUSINESS-RULES-2012.md:220`

**O código contradiz essa afirmação.** A leitura do caminho de produção mostra:

1. `SIFAPJ01`, o job mensal agendado no Control-M, executa um único passo
   Natural, com `BATCHPGT` como único programa em `CMSYNIN`
   (`SIFAPJ01.jcl:70-77`). Não há passo para `CALCDSCT`.
2. `SIFAPJ02` executa apenas `BATCHREL` e `RELPGT`, ambos relatórios
   (`SIFAPJ02.jcl:66-72`, `SIFAPJ02.jcl:95-102`).
3. `BATCHPGT` calcula a dedução **inline**, com a regra simplificada, e grava
   o pagamento com esse total (`BATCHPGT.NSP:455-484`).
4. Em seguida, `BATCHPGT` gera o arquivo de remessa bancária `CMWKF01` usando
   o líquido simplificado (`BATCHPGT.NSP:489-500`).
5. `CALCDSCT` é um programa **interativo**: solicita CPF e número do pagamento
   por tela (`CALCDSCT.NSP:71-75`). Não recebe PDA e não é adequado a
   invocação por `CALLNAT`.

A conclusão é que a documentação descreve uma integração que não existe no
código. O valor que chega ao banco é o da dedução simplificada.

---

## Decisão

Proponho **não integrar** `CALCDSCT` ao fluxo mensal de geração de pagamento.

O sistema moderno preserva os dois caminhos como eles existem em produção:

1. **Geração mensal** mantém a dedução simplificada de `CALCBENF`, já
   implementada em `PaymentCalculationService`. É a regra cujo resultado é
   efetivamente pago.
2. **Recálculo de descontos** permanece como caso de uso separado, disparado
   por operador para um pagamento específico, exposto em
   `POST /api/v1/payments/{paymentId}/discount-calculations` e implementado em
   `DiscountApplicationService`.

Em consequência, a tarefa `T116` da feature 002 é encerrada como **não será
feita**, e não como pendência indefinida.

As duas rotinas não são versões concorrentes da mesma regra: operam em
momentos distintos, por gatilhos distintos. Tratá-las como alternativas
excludentes era um erro de leitura da documentação de 2012, não uma ambiguidade
real do código.

---

## Inconsistência herdada que esta decisão não resolve

Preservar o comportamento observado mantém um problema real do legado:
`CALCDSCT` atualiza `AMT-DISC-TOTAL` e `AMT-NET` de um pagamento **depois** de
`BATCHPGT` já ter gerado a remessa bancária com o líquido simplificado.

O registro do pagamento passa a divergir do valor efetivamente transmitido ao
banco. Não há, no código lido, nenhum mecanismo que regenere a remessa ou
concilie a diferença.

Esta decisão não corrige a divergência, porque corrigi-la exigiria criar regra
nova. O ponto fica registrado para a Coordenação de Benefícios avaliar como
item próprio.

---

## Alternativas consideradas

| Alternativa | Por que foi rejeitada |
|---|---|
| Substituir a dedução simplificada por `CALCDSCT` no fluxo mensal | Alteraria o líquido de toda a base. Beneficiários com bruto de até 500,00 passariam a ter desconto onde hoje não têm — exatamente a faixa de menor renda. Nenhuma evidência de código sustenta que essa seja a regra vigente. |
| Seguir a documentação de 2012 como fonte de verdade | O código de produção a contradiz em ponto verificável: o job mensal não executa `CALCDSCT`. Em conflito entre documentação e código executado, o código prevalece. |
| Somar as duas deduções | Nenhuma evidência sugere acumulação; produziria valores que nenhuma das rotinas gera isoladamente. |
| Manter `SIFAP-M-09` aberto indefinidamente | A dúvida técnica sobre "qual rotina o batch usa" está resolvida por evidência. Manter tudo em aberto confunde a questão respondida com a decisão de negócio remanescente. |

---

## Consequências

- **Mais fácil:** a modernização preserva o comportamento observável do
  legado, o que torna a comparação de resultados entre sistemas verificável.
- **Mais fácil:** `T116` deixa de bloquear a feature 002, que passa a estar
  completa.
- **Mais difícil:** o sistema moderno herda duas regras de desconto
  divergentes, o que exige explicação a cada nova pessoa no time.
- **Riscos:** se a intenção real da área de negócio sempre foi usar a rotina
  detalhada, o sistema moderno perpetua um desconto subaplicado desde 1999.
- **Riscos:** a divergência entre pagamento registrado e remessa transmitida
  continua existindo após um recálculo manual.
- **Mitigações:** ambas as rotinas estão implementadas e testadas de forma
  isolada; adotar a detalhada no fluxo mensal exige apenas trocar a chamada em
  `PaymentCalculationService`, com o serviço já pronto.
- **Mitigações:** a inconsistência da remessa fica registrada neste ADR e em
  [`mysteries-found.md`](../../01-archaeology/mysteries-found.md).

---

## O que precisa de ratificação humana

A Coordenação de Benefícios precisa confirmar:

1. Se a dedução simplificada é a regra oficial vigente ou um defeito tolerado
   por 27 anos.
2. Se a divergência entre pagamento recalculado e remessa já transmitida é
   conhecida e aceita pela operação.

Enquanto não houver ratificação, o status deste ADR permanece `proposed` e
`SIFAP-M-09` permanece aberto quanto à decisão de negócio, ainda que a questão
técnica esteja resolvida.

---

## Relacionados

- REQ-IDs: `REQ-008`, `REQ-010` a `REQ-019`
- ADRs: N/A
- Questões: `SIFAP-M-09` em
  [`mysteries-found.md`](../../01-archaeology/mysteries-found.md)
- Arquivos-fonte do legado:
  - `01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN:357-366`
  - `01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP:62-69`
  - `01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP:71-75`
  - `01-archaeology/legacy-sifap/natural-programs/BATCHPGT.NSP:455-500`
  - `01-archaeology/legacy-sifap/natural-programs/SIFAPJ01.jcl:70-77`
  - `01-archaeology/legacy-sifap/legacy-docs/BUSINESS-RULES-2012.md:220`

---

## Referências

- [`specs/002-calculo-descontos/spec.md`](../../specs/002-calculo-descontos/spec.md)
- [`specs/002-calculo-descontos/plan.md`](../../specs/002-calculo-descontos/plan.md)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [ADR-0003](0003-postgres-compose-instead-of-testcontainers.md)<br/><sub>PostgreSQL do Compose nos testes.</sub> | [ADRs — Índice](README.md)<br/><sub>Índice das decisões registradas.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
