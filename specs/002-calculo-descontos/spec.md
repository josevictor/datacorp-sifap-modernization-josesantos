# Cálculo detalhado de descontos

## Visão geral

Esta feature moderniza a rotina de descontos de `CALCDSCT.NSP`, que hoje é
substituída no backend por uma dedução simplificada de 3%. O escopo cobre a
contribuição social obrigatória por faixa, o teto de 30% do valor bruto, a
vigência de cada desconto e os cinco tipos registrados no grupo periódico do
pagamento.

A feature preserva o comportamento observado, incluindo a ordem de aplicação
do teto. A decisão sobre substituir ou complementar a dedução simplificada
permanece registrada em `SIFAP-M-09` e continua aguardando validação humana;
esta especificação descreve a rotina detalhada, não decide sua adoção.

## História de usuário

Como operador do processamento mensal, quero que os descontos registrados no
pagamento sejam calculados com as faixas, os tipos e o teto do legado, para
que o valor líquido pago corresponda ao que o sistema atual produz.

## Requisitos funcionais

### REQ-010 (orientado a evento) — Aplicar contribuição social obrigatória

QUANDO o cálculo de descontos de um pagamento iniciar, o sistema DEVE aplicar
a contribuição social correspondente à primeira faixa cujo limite seja maior ou
igual ao valor bruto, usando as alíquotas de 3%, 5%, 7% e 9% para os limites
500,00, 1.000,00, 2.000,00 e 9.999,99.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L62-L69
source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L197-L205

**Critérios de aceitação**

- AC-010.1: Dado um bruto de `500,00`, quando os descontos forem calculados, então a contribuição social deve ser `15,00`.
- AC-010.2: Dado um bruto de `500,01`, quando os descontos forem calculados, então a contribuição social deve usar a alíquota de 5%.
- AC-010.3: Dado um bruto de `1.500,00`, quando os descontos forem calculados, então a contribuição social deve usar a alíquota de 7%.
- AC-010.4: Dado um bruto acima de `9.999,99`, quando os descontos forem calculados, então nenhuma faixa deve ser aplicada e a contribuição social deve ser zero.

### REQ-011 (orientado a evento) — Calcular o teto de descontos

QUANDO o cálculo de descontos iniciar, o sistema DEVE calcular o teto como 30%
do valor bruto, truncado para duas casas decimais.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L106-L110

**Critérios de aceitação**

- AC-011.1: Dado um bruto de `1.000,00`, quando o teto for calculado, então o teto deve ser `300,00`.
- AC-011.2: Dado um bruto de `138,84`, quando o teto for calculado, então o teto deve ser `41,65`.

### REQ-012 (indesejado) — Ignorar desconto fora de vigência

SE um desconto registrado tiver data final diferente de zero e anterior à data
corrente, OU data inicial posterior à data corrente, ENTÃO o sistema DEVE
ignorar esse desconto.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L116-L123

**Critérios de aceitação**

- AC-012.1: Dado um desconto com data final anterior à data corrente, quando os descontos forem calculados, então esse desconto não deve compor o total.
- AC-012.2: Dado um desconto com data final igual a zero, quando os descontos forem calculados, então esse desconto deve ser considerado vigente.
- AC-012.3: Dado um desconto com data inicial posterior à data corrente, quando os descontos forem calculados, então esse desconto não deve compor o total.

### REQ-013 (orientado a evento) — Calcular desconto judicial isento de teto

QUANDO um desconto do tipo `J` for processado, o sistema DEVE usar o valor fixo
quando ele for maior que zero, senão o percentual aplicado sobre o bruto, e
DEVE somá-lo ao total sem aplicar o teto nesse item.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L128-L137
source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L169-L174

**Critérios de aceitação**

- AC-013.1: Dado um desconto `J` com valor fixo `200,00`, quando ele for processado, então o total deve incluir `200,00`.
- AC-013.2: Dado um desconto `J` com valor fixo zero e percentual `10`, quando ele for processado sobre bruto `1.000,00`, então o total deve incluir `100,00`.
- AC-013.3: Dado um desconto `J` cujo valor ultrapasse o teto e nenhum outro desconto posterior, quando o total for apurado, então o total não deve ser limitado ao teto.

### REQ-014 (orientado a evento) — Calcular descontos de alimentos e administrativo

QUANDO um desconto do tipo `P` ou `A` for processado, o sistema DEVE usar o
valor fixo quando ele for maior que zero, senão o percentual aplicado sobre o
bruto.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L138-L146
source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L156-L164

**Critérios de aceitação**

- AC-014.1: Dado um desconto `P` com valor fixo `80,00`, quando ele for processado, então o total deve incluir `80,00`.
- AC-014.2: Dado um desconto `A` com valor fixo zero e percentual `5`, quando ele for processado sobre bruto `1.000,00`, então o total deve incluir `50,00`.

### REQ-015 (orientado a evento) — Calcular imposto retido na fonte

QUANDO um desconto do tipo `I` for processado, o sistema DEVE calculá-lo
exclusivamente como o percentual registrado aplicado sobre o valor bruto,
ignorando qualquer valor fixo.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L147-L151

**Critérios de aceitação**

- AC-015.1: Dado um desconto `I` com percentual `7,5` sobre bruto `1.000,00`, quando ele for processado, então o total deve incluir `75,00`.
- AC-015.2: Dado um desconto `I` com valor fixo preenchido e percentual `10`, quando ele for processado, então o valor fixo deve ser ignorado e o percentual aplicado.

### REQ-016 (orientado a evento) — Calcular contribuição sindical

QUANDO um desconto do tipo `S` for processado, o sistema DEVE calculá-lo como
1% do valor bruto, ignorando valor fixo e percentual registrados.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L152-L155

**Critérios de aceitação**

- AC-016.1: Dado um desconto `S` sobre bruto `1.000,00`, quando ele for processado, então o total deve incluir `10,00`.
- AC-016.2: Dado um desconto `S` com percentual registrado `9`, quando ele for processado, então a alíquota aplicada deve permanecer 1%.

### REQ-017 (indesejado) — Ignorar tipo de desconto desconhecido

SE o tipo de um desconto registrado não for `J`, `P`, `I`, `S` ou `A`, ENTÃO o
sistema DEVE ignorá-lo sem alterar o total e sem interromper o processamento
dos demais descontos.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L165-L166

**Critérios de aceitação**

- AC-017.1: Dado um desconto com tipo `X`, quando ele for processado, então o total não deve ser alterado.
- AC-017.2: Dado um desconto com tipo desconhecido seguido de um desconto válido, quando ambos forem processados, então o desconto válido deve compor o total.

### REQ-018 (orientado a evento) — Limitar o total ao teto após item não judicial

QUANDO um desconto de tipo diferente de `J` for processado e o total acumulado
ultrapassar o teto, o sistema DEVE reduzir o total ao valor do teto.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L169-L174

**Critérios de aceitação**

- AC-018.1: Dado um total acumulado acima do teto após um desconto `I`, quando o item for processado, então o total deve ser igual ao teto.
- AC-018.2: Dado um desconto `J` que eleve o total acima do teto seguido de um desconto `S`, quando ambos forem processados, então o total final deve ser igual ao teto, preservando o comportamento observado no legado.

### REQ-019 (orientado a evento) — Persistir o total de descontos

QUANDO todos os descontos registrados forem processados, o sistema DEVE
truncar o total para duas casas decimais e atualizar o total de descontos do
pagamento.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L179-L188
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/PAYMENT.ddm#L19-L42

**Critérios de aceitação**

- AC-019.1: Dado um total com mais de duas casas decimais, quando ele for persistido, então o valor gravado deve estar truncado para duas casas.
- AC-019.2: Dado um pagamento processado, quando ele for consultado, então o total de descontos deve corresponder ao valor apurado.

## Comportamento legado preservado deliberadamente

`REQ-018` reproduz uma ordem de aplicação do teto que pode reduzir valor
originado de um desconto judicial, embora `REQ-013` declare esse tipo isento.
O efeito ocorre porque o legado aplica o teto ao total acumulado dentro do
laço, a cada item não judicial, e não ao final do processamento.

A feature preserva esse comportamento por ser o observado em produção. A
questão está registrada como achado `BONUS` em
[mysteries-found.md](../../01-archaeology/mysteries-found.md) e aguarda
validação humana. Nenhuma correção deve ser introduzida sem essa decisão.

## Decisão sobre a integração ao fluxo mensal

As duas rotinas divergem na mesma faixa de valores:

| Bruto | `CALCBENF.CALC-DISC` | `CALCDSCT` |
|---|---|---|
| `400,00` | `0,00` | `12,00` (3%) |
| `500,00` | `0,00` | `15,00` (3%) |
| `600,00` | `18,00` (3%) | `30,00` (5%) |

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN#L357-L366
source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L62-L69

A divergência não representa ambiguidade sobre qual rotina o sistema executa.
O job mensal `SIFAPJ01` roda apenas `BATCHPGT`, que aplica a dedução
simplificada e gera a remessa bancária com esse líquido. `CALCDSCT` é um
programa interativo acionado por operador para um pagamento específico.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/SIFAPJ01.jcl#L70-L77
source_legacy: 01-archaeology/legacy-sifap/natural-programs/BATCHPGT.NSP#L455-L500
source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCDSCT.NSP#L71-L75

Esta feature preserva os dois caminhos separados, conforme
[ADR-0004](../../docs/adr/0004-simplified-deduction-monthly-flow.md). A
ratificação de negócio permanece pendente em `SIFAP-M-09`.

## Fora de escopo

- Ratificar de negócio se a dedução simplificada é a regra oficial; questão `SIFAP-M-09`, proposta em ADR-0004.
- Cadastro e manutenção dos descontos do grupo periódico.
- Correção retroativa por IPCA.
- Recálculo de pagamentos já gerados.

## Rastreabilidade

| Requisito | Origem catalogada |
|---|---|
| REQ-010 a REQ-019 | [business-rules-catalog.md](../../01-archaeology/business-rules-catalog.md) |

**Prioridade**: P0 para REQ-010, REQ-011, REQ-012 e REQ-019; P1 para REQ-013 a REQ-018.  
**Status**: proposed.
