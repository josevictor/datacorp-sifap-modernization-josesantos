# Tarefas — Cálculo detalhado de descontos

## Testes primeiro

- [x] T101 — Criar testes das quatro faixas de contribuição social e do limite superior sem faixa conforme `REQ-010`.
- [x] T102 — Criar testes do teto de 30% com truncamento conforme `REQ-011`.
- [x] T103 — Criar testes de vigência para data final zero, data final passada e data inicial futura conforme `REQ-012`.
- [x] T104 — Criar testes do desconto judicial com valor fixo, com percentual e sem aplicação de teto conforme `REQ-013`.
- [x] T105 — Criar testes dos descontos de alimentos e administrativo conforme `REQ-014`.
- [x] T106 — Criar testes do imposto retido confirmando que o valor fixo é ignorado conforme `REQ-015`.
- [x] T107 — Criar testes da contribuição sindical fixa em 1% conforme `REQ-016`.
- [x] T108 — Criar testes de tipo desconhecido ignorado sem interromper o processamento conforme `REQ-017`.
- [x] T109 — Criar teste que documente a limitação do total após item não judicial, incluindo o caso `J` seguido de `S`, conforme `REQ-018`.
- [x] T110 — Criar teste de integração da persistência do total truncado no pagamento conforme `REQ-019`.

## Implementação

- [x] T111 — Criar a migração Flyway `V3` da tabela `payment_discount` com ordenação determinística documentada.
- [x] T112 — Implementar `SocialContributionTable` com as faixas e alíquotas de `CALCDSCT` conforme `REQ-010`.
- [x] T113 — Implementar `DiscountType` com o comportamento de cálculo de cada tipo conforme `REQ-013` a `REQ-017`.
- [x] T114 — Implementar a entidade `PaymentDiscount` e seu repositório conforme o plano de modelagem.
- [x] T115 — Implementar `DiscountCalculationService` com contribuição social, vigência, teto e truncamento conforme `REQ-010` a `REQ-019`.
- [x] T116 — **Encerrada como "não será feita"**, conforme [ADR-0004](../../docs/adr/0004-simplified-deduction-monthly-flow.md). O job mensal `SIFAPJ01` não executa `CALCDSCT`; a rotina detalhada é interativa e não integra o caminho de produção. Substituir a dedução simplificada criaria regra nova.
- [x] T117 — Persistir o total de descontos no pagamento conforme `REQ-019`.
- [x] T118 — Adicionar dados de demonstração de descontos em `db/dev` para validação manual.

## Resolução de T116

`CALCBENF.CALC-DISC` aplica 3% **somente quando o bruto excede 500,00**
(`CALCBENF.NSN:357-366`). `CALCDSCT` aplica 3% na faixa **até 500,00** e
alíquotas de 5%, 7% e 9% acima disso (`CALCDSCT.NSP:62-69`).

A leitura do caminho de produção resolveu a questão técnica: o job mensal
`SIFAPJ01` executa apenas `BATCHPGT` (`SIFAPJ01.jcl:70-77`), que aplica a
dedução simplificada inline e gera a remessa bancária com esse líquido
(`BATCHPGT.NSP:455-500`). `CALCDSCT` é um programa interativo
(`CALCDSCT.NSP:71-75`) e não integra o fluxo mensal, apesar de a documentação
de 2012 afirmar o contrário.

A proposta registrada em
[ADR-0004](../../docs/adr/0004-simplified-deduction-monthly-flow.md) mantém os
dois caminhos separados, como em produção. `DiscountCalculationService`
permanece exposto pelo caso de uso de recálculo, sem alterar a geração mensal.

A ratificação de negócio de `SIFAP-M-09` continua pendente.

## Verificação

- [x] T119 — Executar os testes do backend via Docker/Compose.
- [x] T120 — Verificar cada `REQ-ID` de `REQ-010` a `REQ-019` contra seu teste correspondente.
- [x] T121 — Confirmar que o achado `BONUS` sobre o teto e o desconto judicial permanece aberto e não foi corrigido silenciosamente.
- [x] T122 — Confirmar que `SIFAP-M-09` continua registrado como decisão de negócio pendente.
- [x] T123 — Executar a validação de rastreabilidade legada antes da revisão.
  Executada em 2026-09-10 sobre `specs/` inteiro junto com a feature `003`:
  43 `REQ-IDs` declarados, nenhuma falha de `source_legacy:`.
- [x] T124 — Validar manualmente o fluxo mensal com descontos por
  `docker compose up --build`. Os casos semeados até a feature `003` produziam
  bruto entre `40,00` e `138,84`, sempre abaixo do limite de `500,00`, então a
  dedução nunca era exercitada de ponta a ponta. O seed `V7` acrescenta um
  caso com fatores neutros para tornar o valor conferível à mão.

  | Campo | Esperado | Obtido |
  |---|---|---|
  | `grossAmount` | `1150.00` | `1150.00` |
  | `discountAmount` | `34.50` | `34.50` |
  | `netAmount` | `1115.50` | `1115.50` |

  Bruto conferido manualmente:
  `1000,00 x 1,0000 (região 15) x 1,00 (sem dependentes) x 1,0000 (renda até
  300,00) x 1,15 (66 anos) x 1,0000 (sem reajuste) = 1150,00`. Dedução de 3%
  sobre o bruto, conforme `CALCBENF.NSN:357-366`.

## Evidência de execução

Suíte executada em 2026-09-10 com
`docker compose --profile test run --rm backend-test`:

```text
Tests run: 43, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

| Classe de teste | Requisitos cobertos |
|---|---|
| `DiscountCalculationServiceTest` | `REQ-010` a `REQ-018` |
| `DiscountApplicationIntegrationTest` | `REQ-010`, `REQ-011`, `REQ-018`, `REQ-019` |

A suíte cresceu de 15 para 43 testes sem regressão nas classes da feature 001.

## Dependências

- `T111` precede `T114`, `T115` e `T117`.
- `T112` e `T113` precedem `T115`.
- `T115` precede `T116` e `T117`.
- Todos os testes de `T101` a `T110` precedem a implementação correspondente.
- A feature 001 deve ter seus testes validados antes de `T116`, porque a
  substituição do desconto simplificado altera valores já cobertos por
  `REQ-008`.
