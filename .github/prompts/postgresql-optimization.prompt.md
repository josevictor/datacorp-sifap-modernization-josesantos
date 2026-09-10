---
name: "postgresql-optimization"
description: "Otimize consultas, índices e esquema do PostgreSQL 16 com recursos específicos do PostgreSQL, delegando o fluxo de trabalho à skill postgresql-optimization."
argument-hint: "selection=<sql-or-query>"
agent: "dba"
tools: ["read", "search", "execute"]
---
# /postgresql-optimization

## Objetivo

Otimizar uma consulta, um índice ou um esquema lento do PostgreSQL usando recursos específicos do PostgreSQL. Fundamentar cada recomendação com um `EXPLAIN ANALYZE` medido. O fluxo completo está na habilidade [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md). Este prompt o aplica ao banco de dados do SIFAP 2.0 (PostgreSQL 16 por meio de JPA/Hibernate) sem repeti-lo.

> [!IMPORTANT]
> Nenhuma recomendação é entregue sem um `EXPLAIN ANALYZE` de antes e depois. Um plano é uma evidência, não uma opinião.

## Quando usar

Durante as Etapas 3 ou 4, quando uma consulta estiver lenta, um relatório exceder o tempo limite ou um esquema precisar de ajustes com contagens realistas de linhas.

## Pré-condições

- A consulta ou o esquema que será otimizado está disponível
- Uma cópia instantânea do ambiente de homologação com contagens realistas de linhas está acessível para executar `EXPLAIN ANALYZE`
- Os índices existentes nas tabelas envolvidas podem ser listados
- O destino é PostgreSQL 16

## Entradas que a equipe deve fornecer

- `selection`: a consulta ou o esquema que será otimizado
- As tabelas envolvidas, seus índices e contagens realistas de linhas
- Peça à pessoa usuária qualquer informação ausente

## O que farei

- Aplicarei à seleção o fluxo de otimização da habilidade [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md)
- Lerei `EXPLAIN (ANALYZE, BUFFERS)` do início ao fim e identificarei o custo dominante
- Recomendarei o tipo de índice correto (GIN/GiST/parcial/de cobertura) ou a reescrita da consulta com evidências
- Expressarei as alterações de índice como migrações seguras durante a operação e na reversão

## O que não farei

- Recomendar um índice sem avaliar seu custo de escrita ou adicionar um para cada consulta
- Confiar em `EXPLAIN` sem `ANALYZE` ou otimizar com dados da escala de desenvolvimento
- Concatenar a entrada da pessoa usuária em SQL ou desalinhar o mapeamento JPA
- Aplicar um `CREATE INDEX` bloqueante em uma tabela muito acessada. Uso `CONCURRENTLY`

## Formato da saída

```markdown
### Gargalo
Seq Scan em `payment` (4 milhões de linhas) para um filtro seletivo de status.

### Recomendação
CREATE INDEX CONCURRENTLY idx_payment_status ON payment (status) WHERE status <> 'CLOSED';

### EXPLAIN ANALYZE
Antes: Seq Scan, 820 ms. Depois: Index Scan, 4 ms.
```

## Definição de pronto

- [ ] O gargalo dominante está nomeado e fundamentado por evidências do plano
- [ ] A recomendação está fundamentada por um `EXPLAIN ANALYZE` de antes e depois
- [ ] Todos os índices usam uma migração segura durante a operação (`CONCURRENTLY`) e na reversão
- [ ] As consultas permanecem parametrizadas e consistentes com o mapeamento JPA

## Corpo do prompt

A habilidade [`postgresql-optimization`](../skills/postgresql-optimization/SKILL.md) define o fluxo de diagnóstico, as heurísticas de índice e o conjunto de recursos do PostgreSQL. Leia-a e depois aplique-a à seleção.

**Etapa 1: faça a medição.**
Execute `EXPLAIN (ANALYZE, BUFFERS)` em uma cópia instantânea do ambiente de homologação e leia o plano do início ao fim.

**Etapa 2: aplique a habilidade.**
Use a habilidade para escolher a correção: tipo de índice, reescrita da consulta, operador JSONB/de matriz, função de janela ou particionamento.

**Etapa 3: respeite as regras do conjunto.**
Use PostgreSQL 16, mantenha o mapeamento JPA sincronizado e entregue alterações de índice como migrações `CONCURRENTLY` em `db/migration/`.

**Etapa 4: comprove o resultado.**
Execute `EXPLAIN ANALYZE` novamente e cole os tempos de antes e depois.

## Exemplo de chamada

```
/postgresql-optimization selection="SELECT * FROM payment WHERE status = 'OPEN'"
```
