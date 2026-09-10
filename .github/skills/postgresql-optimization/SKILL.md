---
name: "postgresql-optimization"
description: "Cria e otimiza PostgreSQL usando seus recursos avançados: JSONB, tipos array, intervalo e geométricos, tipos personalizados, busca textual, funções de janela, indexação e extensões. Use quando a pessoa quiser escrever, ajustar ou acelerar consultas, esquemas ou o desempenho do PostgreSQL. Para revisar código existente, use postgresql-code-review."
---
# Desenvolvimento e otimização de PostgreSQL

Orientação especializada em PostgreSQL para `${selection}` (ou para todo o projeto quando nada estiver selecionado). Abrange recursos e padrões de otimização específicos do PostgreSQL: JSONB, arrays, intervalos, tipos geométricos, busca textual, funções de janela, indexação e o ecossistema de extensões. Para revisar código PostgreSQL existente em vez de criá-lo, use [`postgresql-code-review`](../postgresql-code-review/SKILL.md).

> [!IMPORTANT]
> A camada de servidor do SIFAP 2.0 executa o **PostgreSQL 16** por **JPA/Hibernate**. Crie consultas da aplicação com JPQL, consultas derivadas do Spring Data ou parâmetros nativos vinculados, nunca SQL concatenado em textos. As alterações de esquema são entregues como migrações somente de avanço do Flyway em `backend/src/main/resources/db/migration/`. Para análises genéricas de planos de execução e índices, consulte [`query-optimization`](../query-optimization/SKILL.md). Para a segurança das migrações, consulte [`database.instructions.md`](../../instructions/database.instructions.md). Esses arquivos são autoritativos quando houver sobreposição.

## Quando invocar

- "Escreva uma consulta rápida de contenção JSONB para esta tabela."
- "Acelere esta agregação; ela faz uma varredura sequencial."
- "Projete o índice adequado para este filtro e esta ordenação."
- "Modele isto com um tipo de intervalo e uma restrição de exclusão."

## Recursos específicos do PostgreSQL

### Operações JSONB

```sql
-- Consultas JSONB avançadas
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índice GIN para desempenho de JSONB
CREATE INDEX idx_events_data_gin ON events USING gin(data);

-- Consultas de contenção e path em JSONB
SELECT * FROM events
WHERE data @> '{"type": "login"}'
  AND data #>> '{user,role}' = 'admin';

-- Agregação JSONB
SELECT jsonb_agg(data) FROM events WHERE data ? 'user_id';
```

### Operações com arrays

```sql
-- Arrays do PostgreSQL
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    tags TEXT[],
    categories INTEGER[]
);

-- Consultas e operações com arrays
SELECT * FROM posts WHERE 'postgresql' = ANY(tags);
SELECT * FROM posts WHERE tags && ARRAY['database', 'sql'];
SELECT * FROM posts WHERE array_length(tags, 1) > 3;

-- Agregação de arrays
SELECT array_agg(DISTINCT category) FROM posts, unnest(categories) as category;
```

### Funções de janela e análise

```sql
-- Funções de janela avançadas
SELECT
    product_id,
    sale_date,
    amount,
    -- Totais acumulados
    SUM(amount) OVER (PARTITION BY product_id ORDER BY sale_date) as running_total,
    -- Médias móveis
    AVG(amount) OVER (PARTITION BY product_id ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg,
    -- Classificações
    DENSE_RANK() OVER (PARTITION BY EXTRACT(month FROM sale_date) ORDER BY amount DESC) as monthly_rank,
    -- Lag/Lead para comparações
    LAG(amount, 1) OVER (PARTITION BY product_id ORDER BY sale_date) as prev_amount
FROM sales;
```

### Busca textual

```sql
-- Busca textual do PostgreSQL
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    search_vector tsvector
);

-- Atualiza o vetor de busca
UPDATE documents
SET search_vector = to_tsvector('english', title || ' ' || content);

-- Índice GIN para desempenho da busca
CREATE INDEX idx_documents_search ON documents USING gin(search_vector);

-- Consultas de busca
SELECT * FROM documents
WHERE search_vector @@ plainto_tsquery('english', 'postgresql database');

-- Classifica os resultados
SELECT *, ts_rank(search_vector, plainto_tsquery('postgresql')) as rank
FROM documents
WHERE search_vector @@ plainto_tsquery('postgresql')
ORDER BY rank DESC;
```

## Ajuste de desempenho do PostgreSQL

### Otimização de consultas

```sql
-- EXPLAIN ANALYZE para análise de desempenho
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'::date
GROUP BY u.id, u.name;

-- Identifica consultas lentas em pg_stat_statements
SELECT query, calls, total_time, mean_time, rows,
       100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

### Estratégias de índices

```sql
-- Índices compostos para consultas com várias colunas
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Índices parciais para consultas filtradas
CREATE INDEX idx_active_users ON users(created_at) WHERE status = 'active';

-- Índices de expressão para valores calculados
CREATE INDEX idx_users_lower_email ON users(lower(email));

-- Índices de cobertura para evitar consultas à tabela
CREATE INDEX idx_orders_covering ON orders(user_id, status) INCLUDE (total, created_at);
```

### Gerenciamento de conexões e memória

```sql
-- Verifica o uso de conexões
SELECT count(*) as connections, state
FROM pg_stat_activity
GROUP BY state;

-- Monitora o uso de memória
SELECT name, setting, unit
FROM pg_settings
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem');
```

## Tipos de dados avançados do PostgreSQL

### Tipos e domínios personalizados

```sql
-- Cria tipos personalizados
CREATE TYPE address_type AS (
    street TEXT,
    city TEXT,
    postal_code TEXT,
    country TEXT
);

CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

-- Usa domínios para validar dados
CREATE DOMAIN email_address AS TEXT
CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Tabela que usa tipos personalizados
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email email_address NOT NULL,
    address address_type,
    status order_status DEFAULT 'pending'
);
```

### Tipos de intervalo

```sql
-- Tipos de intervalo do PostgreSQL
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    reservation_period tstzrange,
    price_range numrange
);

-- Consultas de intervalo
SELECT * FROM reservations
WHERE reservation_period && tstzrange('2024-07-20', '2024-07-25');

-- Exclui intervalos sobrepostos
ALTER TABLE reservations
ADD CONSTRAINT no_overlap
EXCLUDE USING gist (room_id WITH =, reservation_period WITH &&);
```

### Tipos geométricos

```sql
-- Tipos geométricos do PostgreSQL
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT,
    coordinates POINT,
    coverage CIRCLE,
    service_area POLYGON
);

-- Consultas geométricas
SELECT name FROM locations
WHERE coordinates <-> point(40.7128, -74.0060) < 10; -- Dentro de 10 unidades

-- Índice GiST para dados geométricos
CREATE INDEX idx_locations_coords ON locations USING gist(coordinates);
```

## Extensões e ferramentas do PostgreSQL

### Extensões úteis

```sql
-- Habilita extensões usadas com frequência
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";    -- Geração de UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";     -- Funções criptográficas
CREATE EXTENSION IF NOT EXISTS "unaccent";     -- Remove acentos do texto
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- Correspondência por trigramas
CREATE EXTENSION IF NOT EXISTS "btree_gin";    -- Índices GIN para tipos btree

-- Uso das extensões
SELECT uuid_generate_v4();                     -- Gera UUIDs
SELECT crypt('password', gen_salt('bf'));      -- Aplica hash às senhas
SELECT similarity('postgresql', 'postgersql'); -- Correspondência aproximada
```

### Consultas de monitoramento

```sql
-- Tamanho e crescimento do banco de dados
SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;

-- Tamanhos das tabelas e dos índices
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Estatísticas de uso dos índices
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0;  -- Índices não usados
```

### Dicas de otimização específicas do PostgreSQL

- **Use EXPLAIN (ANALYZE, BUFFERS)** para uma análise detalhada das consultas
- **Configure postgresql.conf** para a carga de trabalho (OLTP versus OLAP)
- **Use pool de conexões** (pgbouncer) em aplicações com alta concorrência
- **Execute VACUUM e ANALYZE regularmente** para obter o melhor desempenho
- **Particione tabelas grandes** com o particionamento declarativo do PostgreSQL 10+
- **Use pg_stat_statements** para monitorar o desempenho das consultas

## Monitoramento e manutenção

### Monitoramento do desempenho das consultas

```sql
-- Identifica consultas lentas
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Verifica o uso dos índices
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

### Manutenção do banco de dados

- **VACUUM e ANALYZE**: manutenção regular do desempenho
- **Manutenção de índices**: monitore e reconstrua índices fragmentados
- **Atualização de estatísticas**: mantenha atuais as estatísticas do planejador de consultas
- **Análise de registros de eventos**: revise regularmente os registros do PostgreSQL

## Padrões comuns de consulta

### Paginação

```sql
-- RUIM: OFFSET para conjuntos de dados grandes
SELECT * FROM products ORDER BY id OFFSET 10000 LIMIT 20;

-- BOM: paginação baseada em cursor
SELECT * FROM products
WHERE id > $last_id
ORDER BY id
LIMIT 20;
```

### Agregação

```sql
-- RUIM: agrupamento ineficiente
SELECT user_id, COUNT(*)
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY user_id;

-- BOM: otimizado com índice parcial
CREATE INDEX idx_orders_recent ON orders(user_id)
WHERE order_date >= '2024-01-01';

SELECT user_id, COUNT(*)
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY user_id;
```

### Consultas JSON

```sql
-- RUIM: consulta JSON ineficiente
SELECT * FROM users WHERE data::text LIKE '%admin%';

-- BOM: operadores JSONB e índice GIN
CREATE INDEX idx_users_data_gin ON users USING gin(data);

SELECT * FROM users WHERE data @> '{"role": "admin"}';
```

## Lista de verificação da otimização

### Análise de consultas

- [ ] Executar EXPLAIN ANALYZE em consultas caras
- [ ] Procurar varreduras sequenciais em tabelas grandes
- [ ] Verificar se os algoritmos de junção são adequados
- [ ] Revisar a seletividade da cláusula WHERE
- [ ] Analisar operações de ordenação e agregação

### Estratégia de índices

- [ ] Criar índices para colunas consultadas com frequência
- [ ] Usar índices compostos em buscas com várias colunas
- [ ] Considerar índices parciais para consultas filtradas
- [ ] Remover índices não usados ou duplicados
- [ ] Monitorar o inchaço e a fragmentação dos índices

### Revisão de segurança

- [ ] Usar exclusivamente consultas parametrizadas
- [ ] Implementar controles de acesso adequados
- [ ] Habilitar segurança no nível de linha quando necessário
- [ ] Auditar o acesso a dados sensíveis
- [ ] Usar métodos de conexão seguros

### Monitoramento de desempenho

- [ ] Configurar o monitoramento do desempenho das consultas
- [ ] Definir configurações adequadas de registro de eventos
- [ ] Monitorar o uso do pool de conexões
- [ ] Acompanhar o crescimento do banco e as necessidades de manutenção
- [ ] Configurar alertas de degradação de desempenho

## Recursos avançados do PostgreSQL

### Funções de janela

```sql
-- Totais acumulados e classificações
SELECT
    product_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY product_id ORDER BY order_date) as running_total,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY amount DESC) as rank
FROM sales;
```

### Expressões de tabela comuns (Common Table Expressions, CTEs)

```sql
-- Consultas recursivas para dados hierárquicos
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 1 as level
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

Forneça otimizações específicas e práticas do PostgreSQL que melhorem o desempenho, a segurança e a manutenibilidade das consultas e aproveitem seus recursos avançados.

## Modelo de saída

Informe cada otimização como antes/depois, com a alteração do plano e o DDL exato.

```markdown
## Otimização de PostgreSQL — <consulta ou objeto>

| Campo | Antes | Depois |
|---|---|---|
| Latência p95 | <ms> | <ms> |
| Plano | Seq Scan on `orders` | Index Scan on `idx_orders_data` |
| Linhas examinadas | <n> | <n> |

**Alteração**: índice | reescrita | tipo/restrição | configuração
**DDL**: CREATE INDEX idx_orders_data ON orders USING gin(data);
**Validação**: a nova execução de EXPLAIN (ANALYZE, BUFFERS) confirma o novo plano e a latência menor
```

## Critérios de qualidade

- [ ] Um plano e uma latência de referência foram capturados com `EXPLAIN (ANALYZE, BUFFERS)` antes de qualquer alteração.
- [ ] O recurso escolhido do PostgreSQL (JSONB, array, intervalo, busca textual ou função de janela) é adequado ao padrão de acesso.
- [ ] Os índices correspondem aos filtros, junções e ordenações; cada novo índice está justificado em relação ao custo de escrita.
- [ ] O acesso da aplicação permanece parametrizado (JPQL, consulta derivada ou nativa vinculada), sem SQL criado por textos.
- [ ] As alterações de esquema são migrações somente de avanço do Flyway e podem ser revertidas com segurança.
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` confirma a alteração do plano e a redução da latência.
