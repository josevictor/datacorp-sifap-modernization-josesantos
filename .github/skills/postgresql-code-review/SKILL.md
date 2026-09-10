---
name: "postgresql-code-review"
description: "Revisa SQL, esquemas e funções existentes do PostgreSQL quanto a antipadrões específicos, qualidade e segurança: operações JSONB, uso de arrays, tipos personalizados, projeto de esquema, otimização de funções e segurança no nível de linha (Row Level Security, RLS). Use quando a pessoa solicitar a revisão, auditoria ou avaliação crítica de código PostgreSQL existente ou de uma migração. Para criar ou otimizar novos recursos, use postgresql-optimization."
---
# Revisão de código PostgreSQL

Revisão especializada de código PostgreSQL para `${selection}` (ou para todo o projeto quando nada estiver selecionado). Concentra-se em práticas recomendadas, antipadrões e padrões de qualidade exclusivos do PostgreSQL, não em SQL genérico. Para criar ou ajustar novos recursos do PostgreSQL em vez de revisar os existentes, use [`postgresql-optimization`](../postgresql-optimization/SKILL.md).

> [!IMPORTANT]
> A camada de servidor do SIFAP 2.0 acessa o **PostgreSQL 16** por **JPA/Hibernate**. As consultas da aplicação devem usar JPQL, consultas derivadas do Spring Data ou parâmetros nativos vinculados, nunca SQL concatenado em textos. O esquema fica nas migrações do Flyway em `backend/src/main/resources/db/migration/`. Quando esta habilidade e [`database.instructions.md`](../../instructions/database.instructions.md) se sobrepuserem, o arquivo de instruções será autoritativo.

## Quando invocar

- "Revise esta migração quanto a antipadrões do PostgreSQL."
- "Audite nosso uso de JSONB e arrays."
- "Este esquema usa os tipos corretos do PostgreSQL?"
- "Verifique esta função PL/pgSQL e a política RLS antes da mesclagem."

## Áreas de revisão específicas do PostgreSQL

### Práticas recomendadas de JSONB

```sql
-- RUIM: uso ineficiente de JSONB
SELECT * FROM orders WHERE data->>'status' = 'shipped';  -- Sem suporte de índice

-- BOM: consultas JSONB indexáveis
CREATE INDEX idx_orders_status ON orders USING gin((data->'status'));
SELECT * FROM orders WHERE data @> '{"status": "shipped"}';

-- RUIM: aninhamento profundo sem avaliação
UPDATE orders SET data = data || '{"shipping":{"tracking":{"number":"123"}}}';

-- BOM: JSONB estruturado com validação
ALTER TABLE orders ADD CONSTRAINT valid_status
CHECK (data->>'status' IN ('pending', 'shipped', 'delivered'));
```

### Revisão de operações com arrays

```sql
-- RUIM: operações ineficientes com arrays
SELECT * FROM products WHERE 'electronics' = ANY(categories);  -- Sem índice

-- BOM: consultas em arrays indexados por GIN
CREATE INDEX idx_products_categories ON products USING gin(categories);
SELECT * FROM products WHERE categories @> ARRAY['electronics'];

-- RUIM: concatenação de arrays em loops
-- Isto seria ineficiente em uma função ou procedure

-- BOM: operações em lote com arrays
UPDATE products SET categories = categories || ARRAY['new_category']
WHERE id IN (SELECT id FROM products WHERE condition);
```

### Revisão do projeto de esquema PostgreSQL

```sql
-- RUIM: não usa recursos do PostgreSQL
CREATE TABLE users (
    id INTEGER,
    email VARCHAR(255),
    created_at TIMESTAMP
);

-- BOM: esquema otimizado para PostgreSQL
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email CITEXT UNIQUE NOT NULL,  -- E-mail sem diferenciação de caixa
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Adiciona índice GIN de JSONB para consultas de metadados
CREATE INDEX idx_users_metadata ON users USING gin(metadata);
```

### Tipos e domínios personalizados

```sql
-- RUIM: usa tipos genéricos para dados específicos
CREATE TABLE transactions (
    amount DECIMAL(10,2),
    currency VARCHAR(3),
    status VARCHAR(20)
);

-- BOM: tipos personalizados do PostgreSQL
CREATE TYPE currency_code AS ENUM ('USD', 'EUR', 'GBP', 'JPY');
CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');
CREATE DOMAIN positive_amount AS DECIMAL(10,2) CHECK (VALUE > 0);

CREATE TABLE transactions (
    amount positive_amount NOT NULL,
    currency currency_code NOT NULL,
    status transaction_status DEFAULT 'pending'
);
```

## Antipadrões específicos do PostgreSQL

### Antipadrões de desempenho

- **Evitar índices específicos do PostgreSQL**: não usar GIN/GiST para os tipos de dados adequados
- **Usar JSONB incorretamente**: tratar JSONB como um campo de string simples
- **Ignorar operadores de array**: usar operações ineficientes com arrays
- **Selecionar mal a chave de partição**: não aproveitar o particionamento do PostgreSQL de forma eficaz

### Problemas no projeto do esquema

- **Não usar tipos ENUM**: usar VARCHAR para conjuntos limitados de valores
- **Ignorar restrições**: não incluir restrições CHECK para validar dados
- **Usar tipos de dados incorretos**: usar VARCHAR em vez de TEXT ou CITEXT
- **Não estruturar JSONB**: usar JSONB sem estrutura e sem validação

### Problemas em funções e gatilhos

```sql
-- RUIM: função de gatilho ineficiente
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();  -- Deve usar TIMESTAMPTZ
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- BOM: função de gatilho otimizada
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Configura o gatilho para disparar somente quando necessário
CREATE TRIGGER update_modified_time_trigger
    BEFORE UPDATE ON table_name
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION update_modified_time();
```

## Revisão do uso de extensões do PostgreSQL

### Práticas recomendadas para extensões

```sql
-- Verifica se a extensão existe antes de criá-la
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Usa as extensões adequadamente
-- Geração de UUID
SELECT uuid_generate_v4();

-- Hash de senha
SELECT crypt('password', gen_salt('bf'));

-- Correspondência aproximada de texto
SELECT word_similarity('postgres', 'postgre');
```

## Revisão de segurança do PostgreSQL

### Row Level Security (RLS)

```sql
-- BOM: implementação de RLS
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_data_policy ON sensitive_data
    FOR ALL TO application_role
    USING (user_id = current_setting('app.current_user_id')::INTEGER);
```

### Gerenciamento de privilégios

```sql
-- RUIM: permissões excessivamente amplas
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;

-- BOM: permissões granulares
GRANT SELECT, INSERT, UPDATE ON specific_table TO app_user;
GRANT USAGE ON SEQUENCE specific_table_id_seq TO app_user;
```

## Lista de verificação da qualidade do código PostgreSQL

### Projeto do esquema

- [ ] Usa tipos de dados adequados do PostgreSQL (CITEXT, JSONB, arrays)
- [ ] Aproveita tipos ENUM para valores restritos
- [ ] Implementa restrições CHECK adequadas
- [ ] Usa TIMESTAMPTZ em vez de TIMESTAMP
- [ ] Define domínios personalizados para restrições reutilizáveis

### Considerações de desempenho

- [ ] Usa tipos de índice adequados (GIN para JSONB/arrays, GiST para intervalos)
- [ ] Usa operadores de contenção (@>, ?) nas consultas JSONB
- [ ] Usa operadores específicos do PostgreSQL nas operações com arrays
- [ ] Usa corretamente funções de janela e CTEs
- [ ] Usa funções específicas do PostgreSQL de forma eficiente

### Uso dos recursos do PostgreSQL

- [ ] Usa extensões quando adequado
- [ ] Implementa procedimentos armazenados em PL/pgSQL quando vantajoso
- [ ] Aproveita os recursos SQL avançados do PostgreSQL
- [ ] Usa técnicas de otimização específicas do PostgreSQL
- [ ] Implementa tratamento de erros adequado nas funções

### Segurança e conformidade

- [ ] Implementa Row Level Security (RLS) quando necessário
- [ ] Gerencia corretamente funções e privilégios
- [ ] Usa as funções de criptografia integradas do PostgreSQL
- [ ] Implementa trilhas de auditoria com recursos do PostgreSQL

## Diretrizes de revisão específicas do PostgreSQL

1. **Otimização dos tipos de dados**: confirme o uso adequado dos tipos específicos do PostgreSQL
2. **Estratégia de índices**: revise os tipos de índice e confirme o uso dos índices específicos do PostgreSQL
3. **Estrutura JSONB**: valide o projeto do esquema JSONB e os padrões de consulta
4. **Qualidade das funções**: revise a eficiência e as práticas recomendadas das funções PL/pgSQL
5. **Uso de extensões**: verifique o uso adequado das extensões do PostgreSQL
6. **Recursos de desempenho**: verifique o uso dos recursos avançados do PostgreSQL
7. **Implementação de segurança**: revise os recursos de segurança específicos do PostgreSQL

Concentre-se nos recursos exclusivos do PostgreSQL e confirme que o código aproveita suas particularidades, em vez de tratá-lo como um banco de dados SQL genérico.

## Modelo de saída

Entregue a revisão com um parecer, uma tabela de achados e o SQL corrigido pronto para colar.

```markdown
## Revisão de PostgreSQL — <arquivo ou seleção>

**Parecer**: Aprovado | Correção necessária | Rejeitado

| # | Gravidade | Achado | Evidência | Correção |
|---|---|---|---|---|
| 1 | Alta | Entrada da pessoa usuária concatenada no SQL | `... WHERE status = '` + input | Vincule `:status` por JPQL ou consulta nativa parametrizada |
| 2 | Média | Consulta de contenção JSONB sem índice GIN | Seq Scan em `orders` | `CREATE INDEX idx_orders_data ON orders USING gin(data)` |
| 3 | Baixa | VARCHAR usado para e-mail sem diferenciação de caixa | `email VARCHAR(255)` | Use `CITEXT` com uma restrição `CHECK` |

### SQL corrigido
CREATE INDEX idx_orders_data ON orders USING gin(data);
-- A consulta do repositório permanece parametrizada: WHERE data @> :filter
```

## Critérios de qualidade

- [ ] Há um parecer: Aprovado, Correção necessária ou Rejeitado.
- [ ] Cada achado tem gravidade e evidência concreta (arquivo/linha ou trecho do plano).
- [ ] Nenhuma entrada da pessoa usuária é concatenada no SQL; todos os parâmetros estão vinculados (JPQL, consulta derivada ou consulta nativa vinculada).
- [ ] Os tipos específicos do PostgreSQL, os tipos de índice (GIN/GiST/parcial) e as restrições `CHECK`/`ENUM`/domínio foram validados.
- [ ] Dados pessoais, como CPF ou valores de benefícios, estão mascarados nos registros de eventos ou documentados com um `COMMENT` de coluna.
- [ ] O SQL corrigido está pronto para colar, e todas as alterações de esquema podem ser revertidas com segurança (consulte [`database.instructions.md`](../../instructions/database.instructions.md)).
