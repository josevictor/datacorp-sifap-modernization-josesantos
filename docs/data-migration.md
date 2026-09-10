# Migração da base legada — Adabas FNR 150 → PostgreSQL

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Migração de dados**

Projeto da carga do cadastro de beneficiários do Adabas (`DBID 057 / FNR 150`)
para a tabela `beneficiary` do sistema modernizado.

| Campo | Valor |
|---|---|
| **Escopo** | **A — somente os campos que o sistema moderno usa** (11 de 69) |
| **Origem** | `BENEFIC.ddm` + `FDT-150-BENEFICIARY.txt` |
| **Destino** | `beneficiary` (migrações `V1`, `V5`, `V11`) |
| **Volume** | 4.201.884 registros · 3,4 GB comprimidos · 7,3 GB descomprimidos |
| **Situação** | **Projeto. Não executável hoje** — ver "Premissa" |

---

## Premissa: não há dados no repositório

Este repositório contém apenas **descrições de esquema** — os `.ddm` e a listagem
FDT. Não há extração, arquivo flat nem dump do Adabas. Os 4,2 milhões de
registros vivem no ambiente de produção legado, e o visualizador é externo e
somente leitura.

Portanto **este documento não é executado hoje**. Ele define o mapeamento, as
regras de conversão e o procedimento de carga, para que a execução seja
mecânica quando um arquivo do `ADAULD`/`ADADCU` for disponibilizado.

Segundo a FDT, a janela estimada de extração é de **~90 minutos** (42 min de
leitura sequencial + descompressão para 7,3 GB).

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

### Risco 1 — `region_code` fora de domínio aborta a folha

`BJ COD-REGION` é `A 2` e o `VALELEG` o move para `#COD-REGION (N2)`. Um valor
não numérico causa erro de execução, e no `BATCHPGT` o `ON ERROR` faz
`BACKOUT TRANSACTION` + `TERMINATE 12` — **a folha mensal inteira é abortada**.

O `Remark` do DDM declara o domínio `01-05 OR 99`, mas o código aceita `1..25`.
Os dois discordam. A carga **deve rejeitar** qualquer valor que não seja
numérico ou esteja fora de `01-25` e `99`, em vez de deixá-lo entrar e derrubar
a primeira geração de pagamento.

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

### Não é risco: óbito

`IA IND-DEATH` e `IB DT-DEATH` existem no DDM e **não** estão no esquema
moderno. Verifiquei o `VALELEG`: sua `VIEW OF BENEFIC` não declara nenhum dos
dois. **O legado também não bloqueia pagamento por óbito.** Omiti-los é fiel ao
comportamento atual — mas trata-se de um defeito do legado sendo preservado, e
vale registrar como questão aberta em vez de deixar implícito.

---

## Procedimento de carga

Quatro etapas. Nenhuma escreve direto em `beneficiary`.

### 1. Staging bruto

Tabela de área de transferência com **todas as colunas em texto**, sem
constraint alguma. O objetivo é que a carga nunca falhe por conversão de tipo:
dado inválido precisa ser observável, não fatal.

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
de linhas. Carregada via `COPY`.

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
`0`, `99999999` ou inválida; `region_code` fora de `01-25`/`99`; `status` fora
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
com os 4.201.884 registros informados pela FDT — divergência aqui significa
extração incompleta, não erro de carga.

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
