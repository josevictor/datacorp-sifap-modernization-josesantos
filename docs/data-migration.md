# Migração da base legada — Adabas FNR 150 → PostgreSQL

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Migração de dados**

Projeto e implementação da carga do cadastro de beneficiários e do histórico de
pagamentos do Adabas (`DBID 057 / FNR 150` e `152`) para o sistema modernizado.

| Campo | Valor |
|---|---|
| **Escopo** | **A — somente os campos que o sistema moderno usa** (11 de 69 no cadastro) |
| **Origem** | `legacy-seed-data/{beneficiary,payment}.dat` + layouts |
| **Destino** | `beneficiary` e `payment` (migrações `V1`, `V5`, `V11`) |
| **Volume** | Laboratório: 500 + 2.000 registros · Produção (FDT): 4.201.884 · 3,4 GB |
| **Situação** | **Implementada e executada no laboratório** — ver "Implementação" |

---

## Origem dos dados

O diretório [`legacy-seed-data/`](../01-archaeology/legacy-seed-data/) contém a
extração sintética do laboratório, com quatro arquivos de largura fixa e seus
layouts no estilo `ADACMP`:

| Arquivo | Registros | Bytes/registro | Arquivo Adabas |
|---|---:|---:|---|
| `beneficiary.dat` | 500 | 1.739 | 150 BENEFICIARY |
| `payment.dat` | 2.000 | 855 | 152 PAYMENT |
| `social-program.dat` | 6 | 361 | 151 SOCIAL-PROGRAM |
| `audit.dat` | 200 | 4.995 | 153 AUDIT |

Os dados são **100% sintéticos** e determinísticos: o gerador usa semente fixa
(`19970512`), então a extração é reproduzível.

> [!IMPORTANT]
> O volume do laboratório é de 500 registros, mas a FDT de produção declara
> **4.201.884**. O procedimento de carga é dimensionado para o volume de
> produção — em 500 registros qualquer abordagem funciona, inclusive as
> erradas. Validar em lote pequeno não prova que a carga suporta 4,2 milhões.

---

## Formato do arquivo

**Os `.dat` não são texto.** Esta é a restrição que define todo o procedimento
de carga, e ignorá-la é o erro mais provável.

Cada registro ocupa uma linha de largura fixa, mas os campos combinam três
codificações distintas:

| Formato | Codificação | Exemplo no layout |
|---|---|---|
| `A` | ASCII, preenchido com espaços à direita | `AB NUM-CPF A 11` |
| `N` | ASCII, dígitos com zeros à esquerda | `AF DT-BIRTH N 8` |
| `P` | **BCD binário compactado**, com nibble de sinal | `CH AMT-FAMILY-INCOME P 9,2` → 5 bytes |

Um campo `P 9,2` não ocupa 9 bytes: são 9 dígitos mais o nibble de sinal (`C`
positivo, `D` negativo), empacotados a dois por byte, resultando em **5 bytes**.
O valor `400,00` é escalado para `40000`, alinhado à direita em nove dígitos
como `000040000` e gravado como `0x00 0x00 0x40 0x00 0x0C`, não como o texto
`400.00`.

> [!CAUTION]
> O alinhamento à direita nos nove dígitos é fácil de errar. `0x00 0x00 0x04
> 0x00 0x0C` **não** é `400,00`: decodifica para `40,00`, porque desloca o
> dígito significativo uma casa. O erro é de fator 10 e não gera exceção — o
> valor resultante continua sendo um benefício plausível. A conferência
> autoritativa é `pack_p()` em
> [`generate_seed.py`](../01-archaeology/legacy-seed-data/generate_seed.py).

**Consequências diretas:**

1. `COPY ... FROM` **não** consegue ler o arquivo. Não há delimitador, e os
   bytes binários não são texto válido em nenhuma codificação.
2. Abrir os `.dat` em editor mostra lixo nas colunas de valor, e salvar o
   arquivo o corrompe.
3. A extração exige um passo de decodificação antes do banco: ler por offset
   fixo conforme o layout e converter os campos `P` para decimal.

O corte de registros por `\n` é seguro para ferramentas de linha: nenhum byte
`0x0A` pode ocorrer dentro de um campo `P`, porque exigiria o nibble `A`, que
não pertence ao alfabeto de dígitos e sinais usado no empacotamento. **Isso não
vale para `bytes.splitlines()` do Python**, que quebra também em `0x0C`, `0x1C`
e `0x1D` — bytes que ocorrem naturalmente em campos compactados. Veja a etapa 1
do procedimento.

---


## Mapeamento de campos

Escopo A: as 11 colunas que a aplicação lê hoje.

| Coluna moderna | Campo legado | Formato legado | Observação |
|---|---|---|---|
| `id` | — | — | UUID gerado; o legado usa ISN |
| `cpf` | `AB NUM-CPF` | `A 11` `DE,UQ` | Sem formatação. Sempre presente (não é `NU`) |
| `full_name` | `AC FULL-NAME` | `A 60` `NU` | **Pode vir vazio** |
| `birth_date` | `AF DT-BIRTH` | `U 8` `DE,NU` | `YYYYMMDD`. **Pode vir vazio ou `99999999`** |
| `status` | `CE STAT-BENEFICIARY` | `A 1` `DE,FI` | `A`/`S`/`C`/`I`/`D` |
| `program_code` | `CA COD-PROGRAM` | `A 4` `DE` | |
| `family_income` | `CH AMT-FAMILY-INCOME` | `P 9,2` `NU` | Packed 5 bytes. Precisão **idêntica** a `NUMERIC(9,2)` |
| `dependent_count` | `CK QTY-DEPEND` | `U 2` `NU` | **Criado em 2013** — ver risco 2 |
| `region_code` | `BJ COD-REGION` | `A 2` `DE` | Alfanumérico usado como número — ver risco 1 |
| `nis` | `AM NUM-NIS` | `U 11` `DE,UQ,NU` | **Criado em 2001**. Unicidade parcial — ver `V11` |
| `docs_ok` | `CL IND-DOCS-OK` | `A 1` `FI` | **Criado em 2012** — ver risco 3 |

Fidelidade numérica confirmada: a FDT declara `CH` como packed de 5 bytes com
remark `9,2 PACKED`, ou seja, 9 dígitos totais e 2 decimais. `NUMERIC(9,2)`
cobre exatamente o mesmo domínio, sem perda nem truncamento.

---

## Regras de conversão

### Sentinelas → `NULL` ou valor neutro

O legado não usa `NULL`. Cada sentinela precisa de decisão explícita:

| Sentinela | Campo | Conversão |
|---|---|---|
| `0` | `AF DT-BIRTH` | Rejeitar o registro: sem data não há cálculo de idade |
| `99999999` | `AF DT-BIRTH` | Rejeitar o registro (data desconhecida) |
| `0` | `AM NUM-NIS` | Manter `0` — já significa "ausente" no modelo moderno |
| vazio | `AC FULL-NAME` | Rejeitar: a coluna é `NOT NULL` e o nome aparece na consulta |

### Campos com supressão de nulos (`NU`)

`NU` significa que o campo vazio **não ocupa espaço e não entra no índice**. No
arquivo descomprimido isso aparece como brancos (campos `A`) ou zeros (campos
`U`/`P`), nunca como marcador de nulo. A carga não pode distinguir "vazio" de
"zero legítimo" senão pelo domínio de cada campo.

### Datas

Todos os campos de data do `BENEFIC` são `YYYYMMDD` de 8 dígitos. **A janela de
século não se aplica a esta tabela** — a divergência conhecida entre `BATCHPGT`
e `VALELEG` é de períodos de referência, não de datas cadastrais.

---

## Riscos do escopo A

O escopo A migra 11 de 69 campos. Três consequências exigem ciência de quem
decide, porque não são perdas neutras.

> [!NOTE]
> Os riscos 2 e 3 **não são exercitados pelos dados do laboratório**. O gerador
> preenche `IND-DOCS-OK` sempre com `S` ou `N`, nunca em branco, e mantém
> `QTY-DEPEND` coerente com o grupo periódico. Isso significa que uma carga bem
> sucedida no laboratório **não demonstra** que esses casos estão tratados: os
> dados sintéticos não contêm a população anterior a 2012/2013 que os produz.
> A ausência de erro no laboratório é ausência de evidência, não evidência de
> ausência.

### Risco 1 — `region_code` fora de domínio aborta a folha

`BJ COD-REGION` é `A 2` e o `VALELEG` o move para `#COD-REGION (N2)`. Um valor
não numérico causa erro de execução, e no `BATCHPGT` o `ON ERROR` faz
`BACKOUT TRANSACTION` + `TERMINATE 12` — **a folha mensal inteira é abortada**.

O `Remark` do DDM declara o domínio `01-05 OR 99`, mas o código aceita `1..25`.
Os dois discordam. **A extração do laboratório decide a favor do DDM:** as 500
linhas usam apenas `01`, `02`, `03`, `04`, `05` e `99`, e nenhum valor entre
`06` e `25` aparece. É a primeira evidência baseada em dados de que as vinte
posições intermediárias da tabela de fatores nunca foram alcançadas.

A carga **deve rejeitar** qualquer valor que não seja numérico ou esteja fora
de `01-05` e `99`, em vez de deixá-lo entrar e derrubar a primeira geração de
pagamento.

O sistema moderno já é imune (captura `NumberFormatException` e usa fator
neutro), mas dado sujo continua sendo dado sujo.

### Risco 2 — `dependent_count` é sistematicamente incorreto para cadastros antigos

`CK QTY-DEPEND` foi criado em **2013**. Cadastros anteriores têm o campo vazio,
que a carga leria como `0`. Os dependentes reais desses beneficiários estão no
grupo periódico `DA GRP-DEPEND` (1:10) — **que o escopo A não migra**.

Como `dependent_count` alimenta a validação de elegibilidade, o efeito é
concreto: beneficiários com dependentes reais entram na base moderna com zero e
podem ser recusados indevidamente.

Só há duas saídas honestas: derivar `dependent_count` da contagem de ocorrências
ativas de `GRP-DEPEND` durante a carga (recomendado — não exige tabela nova,
apenas ler o PE na origem), ou aceitar o erro conscientemente.

### Risco 3 — `docs_ok` tem três estados na origem e dois no destino

`CL IND-DOCS-OK` foi criado em **2012** e é `FI` (armazenamento fixo, sem
supressão). Cadastros anteriores carregam **branco**, um terceiro estado que o
domínio `S`/`N` não prevê. A coluna moderna é `NOT NULL DEFAULT 'S'`.

- Converter branco → `'S'` concede elegibilidade documental a quem nunca foi verificado.
- Converter branco → `'N'` bloqueia cadastros válidos anteriores a 2012.

**Não há escolha tecnicamente correta**; é decisão de negócio e precisa de
registro em ADR.

### Risco 4 — recalcular um pagamento migrado não reproduz o valor migrado

Os dados do laboratório trazem `payment.dat` com valores já calculados. **Eles
não podem ser reproduzidos pelo cálculo do sistema moderno**, e a diferença não
é de arredondamento.

O gerador da extração usa uma tabela de fatores por macrorregião; o `BATCHPGT`,
reproduzido em `PaymentCalculationService`, usa a tabela de 27 posições:

| Região | Extração | `BATCHPGT` / sistema moderno |
|---|---:|---:|
| `01` | 1,3500 | 1,3500 |
| `02` | 1,4000 | 1,3200 |
| `03` | 1,1800 | 1,3000 |
| `04` | 1,1000 | 1,2800 |
| `05` | 1,0500 | 1,3100 |
| `99` | 1,0000 | 1,0000 |

Só as regiões `01` e `99` coincidem. Para as demais, o valor bruto recalculado
diverge do valor migrado — em `05`, cerca de 25%.

**Isto não invalida nenhum dos dois lados.** O gerador é uma ferramenta de
laboratório que produz dados internamente consistentes; não é o sistema legado.
Mas a consequência operacional é concreta: **qualquer conferência que compare
o pagamento migrado com o pagamento recalculado vai acusar divergência em massa**,
e quem executar a carga precisa saber disso antes de interpretar o resultado
como defeito do cálculo.

Encaminhamento: migrar valores históricos **como dados**, sem recalculá-los. O
cálculo vale para períodos novos, gerados pelo sistema moderno.

### Não é risco: óbito

`IA IND-DEATH` e `IB DT-DEATH` existem no DDM e **não** estão no esquema
moderno. Verifiquei o `VALELEG`: sua `VIEW OF BENEFIC` não declara nenhum dos
dois. **O legado também não bloqueia pagamento por óbito.** Omiti-los é fiel ao
comportamento atual — mas trata-se de um defeito do legado sendo preservado, e
vale registrar como questão aberta em vez de deixar implícito.

---

## Implementação

A carga foi implementada em Java, no pacote `com.datacorp.sifap.migration`, e
executada com sucesso no laboratório. O procedimento SQL descrito adiante
permanece como referência para o volume de produção.

| Componente | Responsabilidade |
|---|---|
| `FixedWidthLayout` | Deriva offsets do layout por soma acumulada e confere contra `RECORD-BYTES` |
| `PackedDecimalDecoder` | Decodifica BCD, rejeitando nibble inválido |
| `FixedWidthReader` | Enquadra registros por largura fixa, nunca por linha |
| `LegacyBeneficiaryReader` / `LegacyPaymentReader` | Mapeiam os campos do escopo |
| `BeneficiaryImportService` / `PaymentImportService` | Validam, colocam em quarentena e gravam em lotes |
| `LegacyImportRunner` | Orquestra as duas cargas, na ordem correta |

Execução, desligada por padrão para que subir a aplicação nunca escreva dados:

```shell
SIFAP_LEGACY_IMPORT_ENABLED=true docker compose up -d --build backend
```

Resultado registrado no laboratório:

```
Beneficiarios: lidos=500  carregados=500  ignorados=0 recusados=0
Pagamentos:    lidos=2000 carregados=2000 ignorados=0 recusados=0
```

**Zero recusas é a evidência de que os offsets estão corretos.** Um leiaute
deslocado quase sempre produz situação, região ou período fora do domínio, e
nada disso apareceu em 2.500 registros.

A carga é idempotente: beneficiários pelo CPF, pagamentos pelo par
`(cpf, período)`. Reexecutar reporta os registros como ignorados, sem duplicar.

> [!IMPORTANT]
> A ordem importa. Pagamentos exigem o beneficiário já carregado, porque um
> histórico órfão não é alcançável pela consulta, que parte do cadastro.

---

## Procedimento de carga em escala de produção

As quatro etapas a seguir descrevem a carga no volume de produção, onde 4,2
milhões de registros exigem staging, lotes retomáveis e reconciliação em SQL.
No laboratório, a implementação Java descrita acima cumpre o mesmo papel com as
mesmas garantias.

Nenhuma etapa escreve direto em `beneficiary`.

### 1. Decodificação e staging bruto

O arquivo é lido por offset fixo conforme `layout-beneficiary.txt`, com os
campos `P` convertidos de BCD para decimal. Só depois o resultado vai para a
área de transferência, com **todas as colunas em texto** e sem constraint
alguma — o objetivo é que a carga nunca falhe por conversão de tipo: dado
inválido precisa ser observável, não fatal.

```sql
CREATE UNLOGGED TABLE staging_beneficiary_raw (
    line_number  BIGINT PRIMARY KEY,
    registration TEXT,  -- AA NUM-REGISTRATION: chave de reconciliação
    cpf          TEXT,
    full_name    TEXT,
    birth_date   TEXT,
    status       TEXT,
    program_code TEXT,
    family_income TEXT,
    dependent_count TEXT,
    region_code  TEXT,
    nis          TEXT,
    docs_ok      TEXT
);
```

`UNLOGGED` porque a tabela é descartável e evita o custo de WAL em 4,2 milhões
de linhas.

Os offsets do escopo A, derivados do layout por soma acumulada das larguras:

| Campo | Offset | Bytes | Formato |
|---|---:|---:|---|
| `AA NUM-REGISTRATION` | 0 | 11 | `N` |
| `AB NUM-CPF` | 11 | 11 | `A` |
| `AC FULL-NAME` | 22 | 60 | `A` |
| `AF DT-BIRTH` | 202 | 8 | `N` |
| `AM NUM-NIS` | 247 | 11 | `N` |
| `BG UF` | 451 | 2 | `A` |
| `BJ COD-REGION` | 468 | 2 | `A` |
| `CA COD-PROGRAM` | 470 | 4 | `A` |
| `CE STAT-BENEFICIARY` | 498 | 1 | `A` |
| `CH AMT-FAMILY-INCOME` | 510 | **5** | `P 9,2` |
| `CK QTY-DEPEND` | 521 | 2 | `N` |
| `CL IND-DOCS-OK` | 523 | 1 | `A` |

> [!WARNING]
> Os offsets acima devem ser **derivados programaticamente do layout** antes da
> execução, nunca copiados desta tabela nem calculados à mão. O layout é a
> fonte de verdade: uma mudança de largura em qualquer campo anterior desloca
> todos os seguintes, e um deslocamento silencioso produz dados plausíveis e
> errados.
>
> Este aviso não é teórico. A primeira versão desta tabela foi escrita à mão e
> continha offsets incorretos a partir de `AN NUM-BENEFIT`, com desvio de 54
> bytes — o suficiente para ler a renda familiar a partir do meio de outro
> campo sem gerar erro algum.

### Codificação do decimal compactado

Cada byte de um campo `P` carrega dois nibbles. O último nibble é o sinal: `C`
positivo, `D` negativo. Para decodificar, converta os bytes para hexadecimal,
descarte o nibble de sinal e aplique a escala declarada:

```python
def unpack_p(raw: bytes, decimals: int) -> Decimal:
    nibbles = ''.join(f"{b:02x}" for b in raw)
    return Decimal(nibbles[:-1]) / (10 ** decimals)
```

> [!CAUTION]
> Não use `bytes.splitlines()` do Python para separar os registros. Além de
> `\n`, esse método também quebra em `\v`, `\f`, `\x1c`, `\x1d` e `\x1e` — e os
> bytes `0x0C`, `0x1C` e `0x1D` **ocorrem naturalmente** em campos compactados
> (`0x1C` é o dígito `1` seguido do sinal positivo). Um registro seria partido
> ao meio silenciosamente. Leia por largura fixa de 1.740 bytes, isto é, os
> 1.739 do registro mais o `\n`.
>
> Separar por `\n` com ferramentas de linha, como `grep`, **é** seguro: o byte
> `0x0A` exigiria o nibble `A`, que não pertence ao alfabeto de dígitos e
> sinais usado no empacotamento.


`AA NUM-REGISTRATION` **não vira coluna de negócio**, mas precisa existir aqui:
sem ele não há como reconciliar, reexecutar nem fazer carga incremental contra a
origem. É a chave de auditoria da migração, não um campo do domínio.

### 2. Quarentena

Toda linha que viole uma regra vai para uma tabela de rejeitados **com o motivo**,
em vez de abortar o lote:

```sql
CREATE TABLE staging_beneficiary_rejected (
    line_number BIGINT PRIMARY KEY,
    registration TEXT,
    reason TEXT NOT NULL
);
```

Regras de rejeição: CPF ausente ou não numérico; nome vazio; data de nascimento
`0`, `99999999` ou inválida; `region_code` fora de `01-05`/`99`; `status` fora
de `A/S/C/I/D`; NIS não zero já usado por outro registro.

### 3. Transformação em lotes

A carga percorre a staging em faixas de `line_number`, nunca em uma transação
única. Um `INSERT ... SELECT` de 4,2 milhões de linhas mantém um bloqueio longo
e não é retomável após falha.

```sql
INSERT INTO beneficiary (
    id, cpf, full_name, birth_date, status, program_code,
    family_income, dependent_count, region_code, nis, docs_ok
)
SELECT
    gen_random_uuid(),
    r.cpf,
    r.full_name,
    r.birth_date::INTEGER,
    r.status,
    r.program_code,
    r.family_income::NUMERIC(9, 2),
    r.dependent_count::INTEGER,
    r.region_code,
    r.nis::BIGINT,
    r.docs_ok
FROM staging_beneficiary_raw r
WHERE r.line_number BETWEEN :lote_inicio AND :lote_fim
  AND NOT EXISTS (
      SELECT 1 FROM staging_beneficiary_rejected q
      WHERE q.line_number = r.line_number
  )
ON CONFLICT (cpf) DO NOTHING;
```

`ON CONFLICT (cpf) DO NOTHING` torna cada lote **idempotente**: reexecutar uma
faixa após falha não duplica nem quebra. Combinado com a faixa de
`line_number`, a carga é retomável do ponto de interrupção.

### 4. Reconciliação

A carga só é aceita se as contagens fecharem:

```sql
SELECT
    (SELECT count(*) FROM staging_beneficiary_raw)      AS lidos,
    (SELECT count(*) FROM staging_beneficiary_rejected) AS rejeitados,
    (SELECT count(*) FROM beneficiary)                  AS carregados;
```

`lidos = rejeitados + carregados`. Qualquer diferença indica conflito silencioso
de CPF e exige investigação antes da liberação. O total lido deve ainda bater
com a contagem declarada da origem — 500 no laboratório, 4.201.884 em produção
conforme a FDT. Divergência aqui significa extração incompleta, não erro de
carga.

Um cheque adicional é barato e detecta erro de offset, que é a falha mais
perigosa porque não gera exceção: se a decodificação estiver deslocada, os
valores continuam plausíveis mas pertencem a outro campo.

```sql
-- Nenhuma renda pode ser negativa, e o teto do laboratório é modesto.
-- Resultado não vazio indica offset deslocado, não dado ruim.
SELECT count(*) FROM beneficiary
WHERE family_income < 0 OR family_income > 100000;
```

---

## Divergência de metadados no NIS

O layout da extração declara `AM NUM-NIS` como `DE,UQ`, **sem** `NU`, enquanto
a FDT de produção declara `DE,UQ,NU`. O gerador reflete o layout: todos os 500
registros têm NIS válido, nenhum zerado.

**A FDT prevalece.** Ela descreve o arquivo físico de produção; o layout
descreve a extração de laboratório. A migração `V11` implementa a semântica da
FDT com índice único parcial, que é compatível com os dois casos: aceita a
população totalmente preenchida do laboratório e a população mista de produção,
onde os cadastros anteriores a 2001 não têm NIS.

---

## Decisões pendentes

| # | Decisão | Quem decide |
|---|---|---|
| 1 | `docs_ok` em branco (pré-2012) → `'S'` ou `'N'` | Negócio + ADR |
| 2 | Derivar `dependent_count` de `GRP-DEPEND` ou aceitar zero em cadastros pré-2013 | Negócio |
| 3 | Preservar `AA NUM-REGISTRATION` como coluna de auditoria em `beneficiary` | Arquitetura |
| 4 | Registrar a ausência de bloqueio por óbito como questão aberta | Negócio |

---

## Referências

- [`legacy-seed-data/`](../01-archaeology/legacy-seed-data/) — extração sintética e layouts `ADACMP`
- [`layout-beneficiary.txt`](../01-archaeology/legacy-seed-data/layout-beneficiary.txt) — **fonte de verdade dos offsets**
- [`generate_seed.py`](../01-archaeology/legacy-seed-data/generate_seed.py) — gerador determinístico; `pack_p` documenta o empacotamento BCD
- [`BENEFIC.ddm`](../01-archaeology/legacy-sifap/adabas-ddms/BENEFIC.ddm) — visão lógica dos 69 campos
- [`FDT-150-BENEFICIARY.txt`](../01-archaeology/legacy-sifap/adabas-ddms/FDT-150-BENEFICIARY.txt) — leiaute físico, volumes e janela de unload
- [`README.md`](../01-archaeology/legacy-sifap/adabas-ddms/README.md) — seção "Armadilhas conhecidas neste corpus"
- [`V11__enforce_nis_uniqueness_when_present.sql`](../backend/src/main/resources/db/migration/V11__enforce_nis_uniqueness_when_present.sql) — unicidade parcial do NIS

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Decisões pendentes](pending-decisions.md)<br/><sub>Itens 5 a 7 são as decisões abertas desta carga.</sub> | [Mistérios encontrados](../01-archaeology/mysteries-found.md)<br/><sub>Questões abertas do sistema legado.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
