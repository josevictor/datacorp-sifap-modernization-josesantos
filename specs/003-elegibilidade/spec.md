# Validação de elegibilidade

## Visão geral

Esta feature moderniza a rotina `VALELEG.NSN`, que decide se um beneficiário
pode receber pagamento por um programa social. A rotina integra o caminho de
produção da geração mensal: `BATCHPGT` a executa por `CALLNAT` antes do
cálculo e ignora o beneficiário quando o retorno é diferente de zero.

A feature `001-geracao-mensal-pagamento` gera pagamento sem essa validação.
Este recorte fecha a lacuna.

O escopo preserva o comportamento observado no código, incluindo o desvio da
região `99`, que permanece registrado como questão de negócio em aberto.

## História de usuário

Como operador do processamento mensal, quero que apenas beneficiários
elegíveis recebam pagamento, para que o arquivo mensal não contenha benefícios
concedidos fora das regras do programa.

## Requisitos funcionais

### REQ-020 (orientado a evento) — Recusar beneficiário inexistente

QUANDO a validação de elegibilidade for solicitada para um CPF que não exista
no cadastro, o sistema DEVE encerrar a validação com o código `2001`.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L84-L89

**Critérios de aceitação**

- AC-020.1: Dado um CPF ausente do cadastro, quando a validação for solicitada, então o resultado deve ter código `2001`.
- AC-020.2: Dado um CPF ausente do cadastro, quando a validação for solicitada, então nenhuma regra de programa deve ser avaliada.

### REQ-021 (orientado a evento) — Recusar programa inexistente

QUANDO a validação de elegibilidade referenciar um programa que não exista, o
sistema DEVE encerrar a validação com o código `2003`.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L100-L105
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm#L28-L28

**Critérios de aceitação**

- AC-021.1: Dado um programa ausente do cadastro, quando a validação for solicitada, então o resultado deve ter código `2003`.
- AC-021.2: Dado um beneficiário existente e um programa ausente, quando a validação for solicitada, então o código retornado deve ser `2003`, não `2001`.

### REQ-022 (indesejado) — Recusar programa inativo

SE a situação do programa for diferente de `A`, ENTÃO o sistema DEVE encerrar a
validação com o código `2004`.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L114-L118
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm#L41-L41

**Critérios de aceitação**

- AC-022.1: Dado um programa com situação `I`, quando a validação for solicitada, então o resultado deve ter código `2004`.
- AC-022.2: Dado um programa inativo e um beneficiário suspenso, quando a validação for solicitada, então o código retornado deve ser `2004`, porque o programa é avaliado primeiro.

### REQ-023 (indesejado) — Preservar o desvio da região especial

SE a região do beneficiário for `99`, ENTÃO o sistema DEVE declará-lo elegível
e encerrar a validação sem avaliar situação cadastral, faixa etária, teto de
renda, regras por tipo de programa ou código de elegibilidade.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L120-L128
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/BENEFIC.ddm#L69-L69

**Critérios de aceitação**

- AC-023.1: Dado um beneficiário de região `99` que violaria a faixa etária do programa, quando a validação for solicitada, então ele deve ser considerado elegível.
- AC-023.2: Dado um beneficiário de região `99` e um programa inativo, quando a validação for solicitada, então o resultado deve ser `2004`, porque o programa é avaliado antes do desvio.
- AC-023.3: Dado um beneficiário de região diferente de `99`, quando a validação for solicitada, então todas as regras seguintes devem ser avaliadas.

> Este requisito preserva comportamento observado, não regra de negócio
> validada. A decisão permanece aberta em `SIFAP-M-12`.

### REQ-024 (orientado a estado) — Recusar situação cadastral não ativa

ENQUANTO a situação cadastral do beneficiário for `S`, `C`, `D` ou `I`, o
sistema DEVE considerá-lo inelegível e registrar o motivo correspondente.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L133-L151
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/BENEFIC.ddm#L75-L77

**Critérios de aceitação**

- AC-024.1: Dado um beneficiário com situação `S`, quando a validação for solicitada, então ele deve ser inelegível com o motivo de suspensão.
- AC-024.2: Dado um beneficiário com situação `C` ou `D`, quando a validação for solicitada, então ele deve ser inelegível com o motivo de cancelamento ou desligamento.
- AC-024.3: Dado um beneficiário com situação `A`, quando a validação for solicitada, então nenhum motivo de situação cadastral deve ser registrado.

### REQ-025 (orientado a estado) — Aplicar faixa etária quando definida

ENQUANTO a idade mínima ou a idade máxima do programa for maior que zero, o
sistema DEVE considerar inelegível o beneficiário cuja idade estiver fora do
limite definido.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L156-L169
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm#L59-L60

**Critérios de aceitação**

- AC-025.1: Dado um programa com idade mínima `18` e um beneficiário de `17` anos, quando a validação for solicitada, então ele deve ser inelegível.
- AC-025.2: Dado um programa com idade mínima `0`, quando a validação for solicitada, então nenhum limite inferior deve ser aplicado.
- AC-025.3: Dado um programa com idade máxima `65` e um beneficiário de `65` anos, quando a validação for solicitada, então o limite superior não deve ser violado.

### REQ-026 (orientado a estado) — Aplicar teto de renda quando definido

ENQUANTO o teto de renda do programa for maior que zero, o sistema DEVE
considerar inelegível o beneficiário cuja renda familiar exceder esse teto.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L174-L180
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm#L58-L58

**Critérios de aceitação**

- AC-026.1: Dado um programa com teto `1.000,00` e renda familiar `1.000,01`, quando a validação for solicitada, então o beneficiário deve ser inelegível.
- AC-026.2: Dado um programa com teto `1.000,00` e renda familiar `1.000,00`, quando a validação for solicitada, então o teto não deve ser violado.
- AC-026.3: Dado um programa com teto `0`, quando a validação for solicitada, então nenhum teto de renda deve ser aplicado.

> O campo legado se chama `MAX-PERCAP-INCOME`, mas a comparação usa a renda
> familiar declarada, não a renda per capita. O comportamento observado é
> preservado e a divergência fica registrada no plano técnico.

### REQ-027 (orientado a evento) — Aplicar regras do programa assistencial

QUANDO o programa for do tipo `A`, o sistema DEVE considerar inelegível o
beneficiário com documentação incompleta e o beneficiário cuja renda familiar
exceder `600,00` sem possuir dependentes.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L186-L200
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/BENEFIC.ddm#L84-L84

**Critérios de aceitação**

- AC-027.1: Dado um programa tipo `A` e documentação diferente de `S`, quando a validação for solicitada, então o beneficiário deve ser inelegível.
- AC-027.2: Dado um programa tipo `A`, renda `700,00` e nenhum dependente, quando a validação for solicitada, então o beneficiário deve ser inelegível.
- AC-027.3: Dado um programa tipo `A`, renda `700,00` e um dependente, quando a validação for solicitada, então a regra de renda não deve torná-lo inelegível.

### REQ-028 (orientado a evento) — Aplicar idade mínima do programa previdenciário

QUANDO o programa for do tipo `P`, o sistema DEVE considerar inelegível o
beneficiário com idade inferior a 60 anos.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L201-L207

**Critérios de aceitação**

- AC-028.1: Dado um programa tipo `P` e um beneficiário de `59` anos, quando a validação for solicitada, então ele deve ser inelegível.
- AC-028.2: Dado um programa tipo `P` e um beneficiário de `60` anos, quando a validação for solicitada, então a regra de idade do tipo não deve torná-lo inelegível.

### REQ-029 (orientado a evento) — Aplicar faixa etária do programa de trabalho

QUANDO o programa for do tipo `T`, o sistema DEVE considerar inelegível o
beneficiário com idade inferior a 16 anos ou superior a 65 anos.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L208-L214

**Critérios de aceitação**

- AC-029.1: Dado um programa tipo `T` e um beneficiário de `15` anos, quando a validação for solicitada, então ele deve ser inelegível.
- AC-029.2: Dado um programa tipo `T` e um beneficiário de `66` anos, quando a validação for solicitada, então ele deve ser inelegível.
- AC-029.3: Dado um programa tipo `T` e um beneficiário de `40` anos, quando a validação for solicitada, então a regra de faixa do tipo não deve torná-lo inelegível.

### REQ-030 (indesejado) — Recusar tipo de programa desconhecido

SE o tipo do programa não for `A`, `P` nem `T`, ENTÃO o sistema DEVE considerar
o beneficiário inelegível.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L215-L219
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm#L31-L32

**Critérios de aceitação**

- AC-030.1: Dado um programa com tipo `X`, quando a validação for solicitada, então o beneficiário deve ser inelegível com o motivo de tipo desconhecido.
- AC-030.2: Dado um programa com tipo `X` e um beneficiário que atenda a todas as demais regras, quando a validação for solicitada, então ele ainda deve ser inelegível.

### REQ-031 (opcional) — Aplicar o código de elegibilidade do programa

ONDE o programa possuir código de elegibilidade preenchido, o sistema DEVE
exigir NIS cadastrado quando a primeira posição for `R` e DEVE exigir ao menos
um dependente quando a segunda posição for `D`.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L248-L262
source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm#L67-L67

**Critérios de aceitação**

- AC-031.1: Dado um código de elegibilidade iniciado por `R` e NIS igual a zero, quando a validação for solicitada, então o beneficiário deve ser inelegível.
- AC-031.2: Dado um código de elegibilidade com `D` na segunda posição e nenhum dependente, quando a validação for solicitada, então o beneficiário deve ser inelegível.
- AC-031.3: Dado um código de elegibilidade vazio, quando a validação for solicitada, então nenhuma dessas duas exigências deve ser aplicada.
- AC-031.4: Dado um código de elegibilidade com conteúdo nas posições 3 a 5, quando a validação for solicitada, então essas posições devem ser ignoradas.

### REQ-032 (orientado a evento) — Retornar o primeiro motivo de recusa

QUANDO o beneficiário for considerado inelegível por uma ou mais regras, o
sistema DEVE retornar o código `2010` acompanhado do primeiro motivo
registrado.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/VALELEG.NSN#L231-L237

**Critérios de aceitação**

- AC-032.1: Dado um beneficiário que viole apenas a faixa etária, quando a validação for solicitada, então o resultado deve ser `2010` com o motivo de idade.
- AC-032.2: Dado um beneficiário que viole situação cadastral e faixa etária, quando a validação for solicitada, então o motivo retornado deve ser o de situação cadastral, por ser avaliado primeiro.
- AC-032.3: Dado um beneficiário elegível, quando a validação for solicitada, então o código deve ser zero e não deve haver motivo.

### REQ-033 (orientado a evento) — Bloquear a geração mensal do inelegível

QUANDO a geração mensal processar um beneficiário cuja validação de
elegibilidade retornar código diferente de zero, o sistema DEVE ignorar o
beneficiário e não criar pagamento.

source_legacy: 01-archaeology/legacy-sifap/natural-programs/BATCHPGT.NSP#L369-L379

**Critérios de aceitação**

- AC-033.1: Dado um beneficiário inelegível, quando a geração mensal for solicitada, então nenhum pagamento deve ser criado.
- AC-033.2: Dado um beneficiário inelegível, quando a geração mensal for solicitada, então o resultado deve indicar que ele foi ignorado, não que houve erro de processamento.
- AC-033.3: Dado um beneficiário elegível, quando a geração mensal for solicitada, então o pagamento deve ser criado normalmente.

## Fora de escopo

- Definir o significado de negócio da região `99`; questão `SIFAP-M-12`.
- Implementar as regras que a documentação de 2012 atribui a `VALELEG` e que
  não existem no código: dados bancários, limite de dois programas
  simultâneos, atualização cadastral em 24 meses e auditoria bloqueante.
  Consulte o achado `BONUS` correspondente em `mysteries-found.md`.
- Unificar o cálculo de idade entre `BATCHPGT` e `VALELEG`; achado `BONUS`
  sobre a janela de século.
- Reconciliar a tabela de 27 regiões com o domínio do DDM; achado `BONUS`.
- Cadastro de beneficiários, programas e dependentes.
- Cruzamento com o CadÚnico, declarado ausente na documentação de 2012.

## Rastreabilidade

| Requisito | Origem catalogada |
|---|---|
| REQ-020 a REQ-032 | [business-rules-catalog.md](../../01-archaeology/business-rules-catalog.md), seção `VALELEG.NSN` |
| REQ-033 | [business-rules-catalog.md](../../01-archaeology/business-rules-catalog.md), seção `BATCHPGT.NSP`, regra 5 |

**Prioridade**: P0 para REQ-020, REQ-021, REQ-022, REQ-024 e REQ-033; P1 para
os demais.  
**Status**: proposed.
