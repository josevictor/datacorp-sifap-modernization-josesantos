---
name: "query-audit"
description: "Audite uma consulta SQL ou JPQL quanto a injeção, armadilhas de varredura sequencial e N+1, retornando um parecer, uma reescrita e uma justificativa baseada em EXPLAIN."
argument-hint: "query=<sql-or-jpql> tables=<table,table>"
agent: "dba"
tools: ["read", "search", "execute"]
---
# /query-audit

## Objetivo

Revisar uma consulta SQL, JPQL, Criteria ou QueryDSL destinada ao **PostgreSQL 16** para identificar risco de injeção, armadilhas de varredura sequencial, padrões N+1 e violações dos padrões de código do SIFAP. A entrega contém um parecer (Aprovada / Correção necessária / Rejeitada), uma consulta parametrizada reescrita, uma interpretação de `EXPLAIN ANALYZE` e, quando justificada, uma recomendação de índice encaminhada para `/migration`.

> [!WARNING]
> Toda concatenação da entrada da pessoa usuária em SQL é uma falha de injeção e resulta em rejeição automática. Vincule todos os parâmetros.

## Quando usar

Durante a revisão de código de um fluxo de acesso a dados nas Etapas 3 ou 4, ou quando uma consulta estiver lenta. Use antes que ela chegue a um ponto de acesso muito utilizado ou a um processamento em lote noturno em produção.

## Pré-condições

- O texto da consulta está disponível na forma original
- O esquema das tabelas envolvidas é conhecido ou pode ser consultado em `db/migration/`
- Uma cópia instantânea do ambiente de homologação com contagens realistas de linhas está disponível para executar `EXPLAIN ANALYZE`
- Os índices existentes nas tabelas envolvidas podem ser listados (`\d table_name`)

## Entradas que a equipe deve fornecer

- A consulta na forma original (SQL sem abstração, JPQL, Criteria API ou QueryDSL)
- O esquema das tabelas envolvidas ou uma referência às migrações em `db/migration/`
- Os índices existentes nessas tabelas e contagens realistas de linhas em produção
- O fluxo de código que faz a chamada: um ponto de acesso muito utilizado (por solicitação) ou um processamento em lote (noturno)
- Peça à pessoa usuária qualquer informação ausente

## O que farei

- Executarei a análise estática: rejeitarei entradas da pessoa usuária concatenadas em cadeias de caracteres e `SELECT *` em tabelas com muitas colunas; sinalizarei conversões que impeçam o uso do índice e funções em colunas indexadas
- Executarei a análise dinâmica: usarei `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` em uma cópia instantânea do ambiente de homologação e lerei o plano do início ao fim
- Sinalizarei `Seq Scan` em tabelas grandes com filtro seletivo, etapas `Sort` que um índice possa atender, `Nested Loop`s dispendiosos e divergências superiores a 10× entre estimativas e valores reais
- Verificarei N+1 (`JOIN FETCH` ausente), riscos de bloqueio e isolamento e parametrização completa
- Compararei a consulta com os padrões do SIFAP e emitirei um parecer com uma consulta reescrita
- Recomendarei um índice ausente e encaminharei sua criação para `/migration`

## O que não farei

- Aprovar uma consulta porque "ela é rápida em desenvolvimento". O ambiente de desenvolvimento tem milhares de linhas; a produção tem milhões
- Aprovar `SELECT *`, um parâmetro não vinculado ou `FOR UPDATE` em uma linha muito acessada sem fila ou espera progressiva
- Confiar em `EXPLAIN` sem `ANALYZE` ou adicionar um índice para cada consulta sem avaliar o custo de escrita
- Escrever aqui a migração do índice. Recomendo-a e encaminho o arquivo para `/migration`, o comando de migração do administrador de banco de dados (DBA)
- Alterar o esquema ou o mapeamento da entidade JPA. As alterações de mapeamento voltam para o módulo responsável
- Presumir que uma coluna contém ou não PII. Sinalizo tudo o que não estiver identificado e solicito um `COMMENT` para a coluna

## Formato da saída

```markdown
## Auditoria da consulta: busca de pagamentos por status

### Parecer
Correção necessária: Seq Scan em uma tabela com 4 milhões de linhas e filtro seletivo de status.

### Constatações
| # | Severidade | Constatação | Evidência |
|---|---|---|---|
| 1 | Alta | Seq Scan em `payment` | EXPLAIN: Seq Scan (actual rows = 4.0M) |
| 2 | Média | `SELECT *` em uma tabela larga | retorna 22 colunas; quatro são usadas |

### Consulta reescrita
SELECT id, status, reviewed_at FROM payment WHERE status = :status;

### Recomendação de índice (encaminhar para /migration)
CREATE INDEX CONCURRENTLY idx_payment_status ON payment (status) WHERE status <> 'CLOSED';

### EXPLAIN ANALYZE antes e depois
Antes: Seq Scan, 820 ms. Depois: Index Scan, 4 ms.

### Alteração obrigatória na aplicação
Vincular `:status`; selecionar somente as quatro colunas usadas.
```

## Definição de pronto

- [ ] Um parecer está declarado: Aprovada / Correção necessária / Rejeitada
- [ ] As constatações incluem severidade, evidência (arquivo/linha ou trecho de EXPLAIN) e uma recomendação
- [ ] A consulta reescrita está parametrizada, pronta para uso e sem concatenação de cadeias de caracteres
- [ ] Os resultados de `EXPLAIN ANALYZE` antes e depois estão incluídos, com tempos medidos
- [ ] Toda recomendação de índice é segura durante a operação (`CONCURRENTLY`) e foi encaminhada para `/migration`
- [ ] O acesso a PII está sinalizado e os comentários das colunas foram confirmados

## Corpo do prompt

Você é `@dba`. A equipe quer auditar uma consulta antes que ela chegue à produção. Leia [`query-optimization`](../skills/query-optimization/SKILL.md) antes de começar. Essa habilidade define o fluxo de diagnóstico, as heurísticas de projeto de índices e os antipadrões.

**Etapa 1: execute a análise estática.**
Rejeite como injeção de SQL toda concatenação de strings com a entrada da pessoa usuária. Rejeite `SELECT *` em uma tabela larga. Sinalize conversões implícitas (`varchar = bigint`) e funções em colunas indexadas que impeçam o uso do índice. Corrija-as ou adicione um índice de expressão somente quando houver evidências que o justifiquem.

**Etapa 2: execute a análise dinâmica.**
Execute `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` em uma cópia instantânea do ambiente de homologação. Leia o plano do início ao fim e sinalize: `Seq Scan` em uma tabela com mais de 10 mil linhas quando houver um filtro; `Sort` que um índice possa atender; `Nested Loop` com mais de aproximadamente mil linhas externas quando um `Hash Join` for mais econômico; e divergência superior a 10× entre a estimativa e o número real de linhas (estatísticas desatualizadas, execute `ANALYZE`).

**Etapa 3: verifique N+1.**
Se a consulta vier do JPA, procure uma instrução `JOIN FETCH` ou uma configuração de tamanho de lote ausente. Identifique também o laço principal no código da aplicação.

**Etapa 4: verifique os bloqueios e o isolamento.**
`SELECT ... FOR UPDATE` em uma tabela muito acessada exige uma fila ou espera progressiva. O isolamento padrão é `READ COMMITTED`; sinalize o uso injustificado de `SERIALIZABLE`.

**Etapa 5: confirme a parametrização.**
Cada valor fornecido pela pessoa usuária deve ser um parâmetro vinculado, nunca interpolado, mesmo quando vier de um fluxo "confiável". Essa é a proteção contra injeção da OWASP.

**Etapa 6: compare com os padrões do SIFAP.**
Use identificadores em `snake_case`, `TIMESTAMPTZ` para marcas temporais, `NUMERIC(15,2)` para valores monetários, nunca `FLOAT`, e um `COMMENT` em cada coluna de PII.

**Etapa 7: escreva a correção e classifique.**
Reescreva a consulta de forma parametrizada. Quando as evidências justificarem um novo índice, especifique-o com `CONCURRENTLY` e encaminhe sua migração para `/migration`. Declare o parecer: Aprovada, Correção necessária ou Rejeitada.

Nunca aprove uma consulta que divirja do mapeamento da entidade JPA, pois isso oculta um N+1 que reaparecerá. Se um mapeamento estiver incorreto, devolva-o ao módulo responsável em vez de mascará-lo no SQL.

## Exemplo de chamada

```
/query-audit query="SELECT * FROM payment WHERE status = 'OPEN'" tables=payment
```
