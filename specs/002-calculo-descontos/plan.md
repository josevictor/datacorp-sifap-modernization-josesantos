# Plano técnico — Cálculo detalhado de descontos

## Objetivo

Implementar a rotina de descontos de `CALCDSCT.NSP` em Java 21 e Spring Boot
3.3, preservando o comportamento observável dos requisitos `REQ-010` a
`REQ-019`. A implementação substitui o cálculo simplificado que hoje existe em
`PaymentCalculationService.simplifiedDiscount`, mantendo o truncamento
monetário e a ordem de aplicação do teto observados no legado.

## Limites do módulo

- **Entrada:** valor bruto do pagamento e lista de descontos registrados.
- **Domínio:** faixa de contribuição social, cálculo por tipo de desconto,
  vigência, teto de 30% e total truncado.
- **Persistência:** descontos vinculados ao pagamento e total gravado no
  pagamento.
- **Saída:** total de descontos aplicado ao valor líquido.
- **Não incluído:** cadastro de descontos, recálculo de pagamentos existentes,
  correção IPCA e a decisão de `SIFAP-M-09`.
- **Execução:** todos os comandos por Docker/Compose, sem Maven, Java ou
  PostgreSQL no host.

O módulo permanece dentro do pacote `com.datacorp.sifap.payments`. Descontos
não formam um contexto próprio: eles só existem como parte do cálculo de um
pagamento e compartilham o agregado `Payment`.

## Componentes planejados

1. **`DiscountType`:** enumeração dos tipos `J`, `P`, `I`, `S` e `A`, com o
   comportamento de cálculo associado a cada um.
2. **`PaymentDiscount`:** entidade do desconto registrado, com tipo, valor
   fixo, percentual, vigência e número do processo.
3. **`DiscountCalculationService`:** aplica contribuição social, itera os
   descontos vigentes e aplica o teto conforme `REQ-018`.
4. **`SocialContributionTable`:** tabela de faixas e alíquotas isolada do
   serviço, espelhando `#BAND-CONTRIB` e `#RATE-CONTRIB`.
5. **Migração Flyway `V3`:** cria a tabela `payment_discount`.
6. **Integração com o fluxo mensal:** bloqueada por `SIFAP-M-09`; ver a seção
   seguinte.

## Caso de uso separado em vez de integração ao fluxo mensal

`CALCDSCT.NSP` é um programa autônomo no legado: recebe um pagamento já
gerado, apura os descontos e atualiza `AMT-DISC-TOTAL`. Ele não é chamado por
`CALCBENF` nem por `BATCHPGT`.

A implementação preserva essa estrutura com
`POST /api/v1/payments/{paymentId}/discount-calculations`, atendido por
`DiscountApplicationService`. Isso entrega `REQ-019` sem decidir
`SIFAP-M-09`: o fluxo mensal continua usando a dedução simplificada de
`CALCBENF`, exatamente como no legado.

A substituição no fluxo mensal permanece como `T116` e depende de decisão
humana.

## Numeração das migrações

`db/migration` e `db/dev` compartilham o mesmo histórico do Flyway, então as
versões não podem colidir:

| Versão | Local | Conteúdo |
|---|---|---|
| `V1` | `db/migration` | Esquema da geração mensal |
| `V2` | `db/dev` | Dados de demonstração da geração |
| `V3` | `db/migration` | Tabela `payment_discount` |
| `V4` | `db/dev` | Dados de demonstração de descontos |

## Modelagem do grupo periódico

O legado usa um grupo periódico Adabas com até 8 ocorrências dentro do próprio
registro de pagamento. O equivalente relacional é uma tabela filha com chave
estrangeira para `payment`.

Não replicamos o limite de 8 ocorrências como restrição física: era uma
limitação do formato Adabas, não uma regra de negócio observada. O limite é
registrado como comentário na migração.

| Campo legado | Coluna moderna | Tipo |
|---|---|---|
| `TYPE-DISC` | `type` | `CHAR(1)` |
| `AMT-DISC` | `fixed_amount` | `NUMERIC(9,2)` |
| `PCT-DISC` | `percentage` | `NUMERIC(5,2)` |
| `DT-START-DISC` | `start_date` | `INTEGER` (`YYYYMMDD`) |
| `DT-END-DISC` | `end_date` | `INTEGER` (`YYYYMMDD`) |
| `NUM-CASE` | `case_number` | `VARCHAR(20)` |

As datas permanecem no formato numérico `YYYYMMDD` do legado para preservar a
semântica de `end_date = 0` como "sem término", conforme `REQ-012`.

## Dados e invariantes

- Todo cálculo monetário usa `Money`, com truncamento para duas casas.
- A contribuição social é obrigatória e independe dos descontos registrados.
- Bruto acima de `9.999,99` não casa nenhuma faixa e produz contribuição zero.
- O teto é `30%` do bruto, truncado, calculado uma única vez.
- O teto é avaliado a cada item cujo tipo não seja `J`, sobre o total
  acumulado, não sobre o item.
- Tipo desconhecido é ignorado sem interromper o processamento.
- O total final é truncado antes de ser persistido.

## Estratégia de testes

- Testes unitários por faixa de contribuição social, incluindo os limites
  exatos `500,00`, `500,01`, `1.000,00`, `2.000,00` e acima de `9.999,99`.
- Testes unitários por tipo de desconto, cobrindo valor fixo e percentual.
- Teste unitário confirmando que `I` ignora valor fixo e que `S` ignora ambos.
- Testes de vigência para `end_date` zero, passada e `start_date` futura.
- Teste que documenta o comportamento de `REQ-018` com `J` seguido de `S`.
- Teste de integração da persistência do total no pagamento.
- Cada teste cita o `REQ-ID` correspondente em comentário inline.
- PostgreSQL 16 do Compose para integração; não usar H2.

## Estratégia Docker

Reaproveita a infraestrutura da feature 001 sem alterações estruturais:

- `docker compose --profile test run --rm backend-test` para os testes.
- `docker compose up --build` para validação manual.
- A migração `V3` roda automaticamente pelo Flyway na subida.
- Dados de demonstração de descontos vão em `db/dev`, fora das migrações de
  produção.

## Riscos e decisões pendentes

| Risco | Mitigação |
|---|---|
| O teto pode reduzir desconto judicial, contrariando o comentário do legado | Preservar o comportamento observado, cobrir por teste explícito e manter o achado `BONUS` aberto. |
| Adoção desta rotina no fluxo mensal ainda não decidida (`SIFAP-M-09`) | Implementar o serviço isolado e integrá-lo por trás do ponto de extensão já existente, mantendo a decisão reversível. |
| Percentual do legado é `P3.2` e pode divergir de `NUMERIC(5,2)` | Validar faixa de valores na entrada e cobrir por teste de limite. |
| Ordem dos descontos altera o resultado | Definir ordenação estável e determinística na consulta, documentada na migração. |

## Ordem de implementação

1. Criar migração `V3` da tabela `payment_discount`.
2. Escrever testes unitários da tabela de contribuição social.
3. Implementar `SocialContributionTable` e o cálculo de contribuição.
4. Escrever testes unitários por tipo de desconto e vigência.
5. Implementar `DiscountType` e `PaymentDiscount`.
6. Implementar `DiscountCalculationService` com teto e truncamento.
7. Escrever teste do comportamento de `REQ-018`.
8. Integrar ao fluxo mensal substituindo o desconto simplificado.
9. Escrever teste de integração da persistência do total.
10. Executar a análise de rastreabilidade dos `REQ-ID`.
