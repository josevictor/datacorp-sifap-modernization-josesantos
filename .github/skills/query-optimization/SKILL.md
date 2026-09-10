---
name: "query-optimization"
description: "Use ao investigar consultas lentas, projetar índices ou revisar planos de execução. Os gatilhos incluem \"consulta lenta\", \"plano EXPLAIN\", \"índice\", \"ajuste de consulta\", \"N+1\" e \"varredura de tabela\"."
---
# Otimização de consultas

## Quando invocar

- "Esta consulta está lenta."
- "Por que ela não está usando o índice?"
- "Devo adicionar um índice em...?"
- "Revise esta saída do EXPLAIN."

## Fluxo de diagnóstico

1. **Meça antes de otimizar**: capture uma linha de base (latência p50/p95, linhas examinadas, linhas retornadas e leituras lógicas).
2. **Obtenha o plano**: `EXPLAIN (ANALYZE, BUFFERS)` no PostgreSQL, `EXPLAIN ANALYZE FORMAT=JSON` no MySQL 8 ou `SET STATISTICS IO, TIME ON` no SQL Server.
3. **Procure causas comuns**:

- **Varredura sequencial ou de tabela (Seq Scan / Table Scan)** em uma tabela grande com predicado seletivo → índice ausente
- **Estimativa de linhas com erro superior a 10×** → estatísticas desatualizadas; execute `ANALYZE`
- **Laço aninhado (Nested Loop) com muitas linhas externas** → deveria ser uma junção por hash ou mesclagem
- **Ordenação transferida para o disco** → `work_mem` muito baixo ou índice ausente para o ORDER BY
- **Filtro após a junção**, em vez de aplicação antecipada (pushdown) → reescreva a consulta ou adicione um índice para o predicado

4. **Proponha a menor alteração**: um índice, uma reescrita, uma atualização de estatísticas ou um ajuste de parâmetro.
5. **Valide**: execute ANALYZE novamente, confirme a alteração do plano e verifique a redução da latência. Nunca "implante e torça".

## Heurísticas para projeto de índices

- Coloque **primeiro as colunas de igualdade**, depois as de intervalo e, por fim, as de ordenação (regra ESR).
- Um **índice de cobertura** (colunas INCLUDE) evita consultas ao heap em consultas com muitas leituras.
- Um **índice parcial** atende a filtros muito seletivos em dados assimétricos (`WHERE status = 'pending'`).
- Cada índice acrescenta custo de escrita. Justifique todos eles.

## Antipadrões

- `SELECT *` em fluxos críticos: força acesso ao heap e impede índices de cobertura.
- `WHERE func(col) = x`: impede o uso do índice; armazene uma coluna calculada ou use um índice de expressão.
- N+1 do ORM: corrija no ORM com carregamento antecipado, não com um índice.
- "Adicionar um índice a cada coluna": desperdiça armazenamento e torna as escritas mais lentas.

## Modelo de saída

```markdown
## Otimização de consulta - <id da consulta>

| Campo | Antes | Depois |
|---|---|---|
| Latência p95 | <ms> | <ms> |
| Linhas examinadas | <n> | <n> |
| Plano | Seq Scan | Index Scan on <index> |

**Alteração**: índice / reescrita / ANALYZE / parâmetro
**DDL**: CREATE INDEX CONCURRENTLY <name> ON <table> (<cols>)
**Validação**: a nova execução de EXPLAIN (ANALYZE, BUFFERS) confirma o novo plano
```

## Critérios de qualidade

- [ ] Uma linha de base (p50/p95, linhas examinadas e plano) foi capturada antes de qualquer alteração.
- [ ] A alteração proposta é a menor que corrige o gargalo.
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` confirma a alteração do plano e a redução da latência.
- [ ] Cada novo índice está justificado em relação ao seu custo de escrita.

## Referências

- [Use The Index, Luke!](https://use-the-index-luke.com/)
- [PostgreSQL - Dicas de desempenho](https://www.postgresql.org/docs/current/performance-tips.html)
- [SQL Server - Query Store](https://learn.microsoft.com/sql/relational-databases/performance/monitoring-performance-by-using-the-query-store)
