# Geração mensal de pagamento

## Visão geral

Esta feature moderniza o recorte de geração mensal de um pagamento para um
beneficiário ativo. O escopo preserva a validação de CPF, a prevenção de
duplicidade por CPF e período, o cálculo mensal observado no fluxo do batch e
o registro do pagamento gerado. A rotina detalhada de descontos de
`CALCDSCT.NSP`, a correção retroativa por IPCA e as regras ainda não validadas
humanamente ficam fora desta feature.

## História de usuário

Como operador do processamento mensal, quero gerar no máximo um pagamento
válido por beneficiário e período, para que o arquivo de pagamentos não
contenha duplicidades e mantenha os valores calculados pelo legado.

## Requisitos funcionais

### REQ-001 (orientado a evento) — Validar o período

QUANDO uma solicitação de geração informar um período, o sistema DEVE rejeitá-la
quando o mês do período não estiver entre 01 e 12.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN#L176-L181

**Critérios de aceitação**

- AC-001.1: Dado o período `202609`, quando a geração for solicitada, então o período deve ser aceito.
- AC-001.2: Dado o período `202613`, quando a geração for solicitada, então a geração deve ser rejeitada com erro de período inválido.

### REQ-002 (orientado a estado) — Processar somente beneficiário ativo

ENQUANTO a situação cadastral do beneficiário for diferente de `A`, o sistema
DEVE ignorar o beneficiário e não criar pagamento.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/BATCHPGT.NSP#L258-L271

**Critérios de aceitação**

- AC-002.1: Dado um beneficiário com situação `A`, quando o lote o processar, então ele deve seguir para validação e cálculo.
- AC-002.2: Dado um beneficiário com situação diferente de `A`, quando o lote o processar, então nenhum pagamento deve ser criado.

### REQ-003 (orientado a evento) — Validar CPF

QUANDO o lote iniciar o processamento de um beneficiário, o sistema DEVE
validar o CPF e rejeitar o beneficiário quando a validação retornar código
diferente de zero.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/BATCHPGT.NSP#L276-L295

**Critérios de aceitação**

- AC-003.1: Dado um CPF válido, quando o lote processar o beneficiário, então o beneficiário não deve ser rejeitado pela validação de CPF.
- AC-003.2: Dado um CPF inválido, quando o lote processar o beneficiário, então nenhum pagamento deve ser criado e a rejeição deve ser registrada no arquivo de erros equivalente a `CMWKF02`.

### REQ-004 (indesejado) — Impedir pagamento duplicado

SE já existir pagamento para a combinação de CPF e período, ENTÃO o sistema
DEVE ignorar o beneficiário e não criar outro pagamento para essa combinação.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/BATCHPGT.NSP#L297-L305
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/PAYMENT.ddm#L139-L145

**Critérios de aceitação**

- AC-004.1: Dado que não existe pagamento para CPF e período, quando o lote processar o beneficiário, então a geração deve poder prosseguir.
- AC-004.2: Dado que já existe pagamento para CPF e período, quando o lote processar o beneficiário, então a quantidade de pagamentos para essa combinação deve permanecer inalterada.

### REQ-005 (orientado a evento) — Calcular o valor bruto mensal

QUANDO o beneficiário e o programa forem válidos, o sistema DEVE calcular o
valor bruto mensal multiplicando o valor-base pelos fatores regional, familiar,
de renda, etário e pelo ajuste do programa.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN#L260-L276
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm#L43-L70

**Critérios de aceitação**

- AC-005.1: Dado um beneficiário e programa válidos com fatores conhecidos, quando o cálculo for executado, então o bruto deve ser o produto dos fatores e do valor-base conforme a fórmula legada.
- AC-005.2: Dado um valor calculado com mais de duas casas decimais, quando o resultado for persistido, então ele deve ser truncado para duas casas.

### REQ-006 (orientado a evento) — Calcular pagamento de dezembro

QUANDO o período for dezembro, o sistema DEVE adicionar o valor de dezembro ao
benefício mensal e marcar o tipo de pagamento como `D`.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN#L280-L292

**Critérios de aceitação**

- AC-006.1: Dado um período cujo mês seja `12`, quando o cálculo for executado, então o tipo de pagamento deve ser `D`.
- AC-006.2: Dado um período cujo mês não seja `12`, quando o cálculo for executado, então o tipo de pagamento deve ser `N`.

### REQ-007 (orientado a evento) — Aplicar abono de programa tipo A

QUANDO o período for dezembro e o programa for do tipo `A`, o sistema DEVE
adicionar ao bruto um abono equivalente a 15% do benefício-base calculado.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN#L294-L302
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm#L23-L28

**Critérios de aceitação**

- AC-007.1: Dado um programa tipo `A` e período de dezembro, quando o cálculo for executado, então o abono deve ser 15% do benefício-base calculado, truncado para duas casas.
- AC-007.2: Dado um programa que não seja tipo `A` e período de dezembro, quando o cálculo for executado, então o abono deve ser zero.

### REQ-008 (indesejado) — Evitar líquido negativo

SE o total de descontos exceder o valor bruto, ENTÃO o sistema DEVE retornar
valor líquido igual a zero.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/CALCBENF.NSN#L307-L316

**Critérios de aceitação**

- AC-008.1: Dado um bruto menor ou igual aos descontos, quando o líquido for calculado, então o líquido deve ser zero.
- AC-008.2: Dado um bruto maior que os descontos, quando o líquido for calculado, então o líquido deve ser a diferença truncada para duas casas.

### REQ-009 (orientado a evento) — Persistir pagamento gerado

QUANDO o cálculo terminar com sucesso, o sistema DEVE persistir um pagamento
com CPF, programa, período, valores calculados, data de geração, tipo de
pagamento e situação `G`.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/BATCHPGT.NSP#L433-L457
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/PAYMENT.ddm#L19-L42

**Critérios de aceitação**

- AC-009.1: Dado um cálculo bem-sucedido, quando o lote persistir o resultado, então deve existir um pagamento com situação `G`.
- AC-009.2: Dado um pagamento persistido, quando seus dados forem consultados, então CPF, programa, período, bruto, desconto, líquido, tipo e data devem corresponder ao resultado do cálculo.

## Fora de escopo

- Escolher entre o desconto simplificado de `CALCBENF` e o detalhado de `CALCDSCT`; questão `SIFAP-M-09`.
- Remover a fórmula duplicada no batch; questão `SIFAP-M-10`.
- Definir proporcionalidade do décimo-terceiro; questão `SIFAP-M-11`.
- Definir o significado de região `99`; questão `SIFAP-M-12`.
- Correção retroativa por IPCA.
- Regras completas de elegibilidade, cadastro, conciliação e auditoria detalhada.

## Rastreabilidade

| Requisito | Origem catalogada |
|---|---|
| REQ-001 a REQ-009 | [business-rules-catalog.md](../../01-archaeology/business-rules-catalog.md) |

**Prioridade**: P0 para REQ-001, REQ-002, REQ-003, REQ-004 e REQ-009; P1 para REQ-005 a REQ-008.  
**Status**: proposed.
