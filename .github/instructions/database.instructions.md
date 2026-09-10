---
description: "Use ao escrever repositórios de banco de dados, migrações, mudanças de schema, consultas SQL, índices e alterações de dados seguras para rollback."
applyTo: "backend/src/main/java/**/infrastructure/**,backend/src/main/resources/db/migration/**"
---

# Convenções de banco de dados — Migrações Flyway e repositórios

Este arquivo é ativado quando você edita código de persistência em `backend/src/main/java/**/infrastructure/**` ou migrações Flyway em `backend/src/main/resources/db/migration/**`. Ele ensina higiene de migrações, segurança de consultas em repositórios, indexação e mudanças de schema seguras para rollback no PostgreSQL 16. O mapeamento de entidades e de FDT para JPA pertence a [`modular-monolith.instructions.md`](modular-monolith.instructions.md); a leitura do FDT Adabas que origina um schema pertence a [`natural-adabas.instructions.md`](natural-adabas.instructions.md).

## Migrações Flyway

As migrações são versionadas, somente de avanço e imutáveis após o merge. Nomeie-as `V<n>__<snake_case_description>.sql`. Faça uma mudança lógica por arquivo. Todos os identificadores usam `snake_case`.

```sql
-- V1__create_resource.sql
CREATE TABLE resource (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    label       VARCHAR(120) NOT NULL,
    amount      NUMERIC(15, 2) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX ux_resource_label ON resource (label);
```

> [!WARNING]
> Nunca edite uma migração já executada em um banco de dados compartilhado. O Flyway valida seu checksum e falhará. Corrija adiante com uma nova migração `V<n+1>__`.

## Valores monetários e precisão

Campos monetários e decimais compactados correspondem a `NUMERIC(precision, scale)` no PostgreSQL e `BigDecimal` no Java. Nunca use `float`, `double`, `real` ou `money`.

```sql
amount NUMERIC(15, 2) NOT NULL -- corresponde a BigDecimal com escala 2
```

## Repositórios

Os repositórios são interfaces Spring Data. Use métodos de consulta derivados ou `@Query` com JPQL e **parâmetros nomeados**. Nunca concatene strings, pois isso permite injeção de SQL.

```java
interface ResourceRepository extends JpaRepository<Resource, UUID> {

    Optional<Resource> findByLabel(String label);

    @Query("select r from Resource r where r.amount >= :floor")
    List<Resource> findAllAtOrAbove(@Param("floor") BigDecimal floor);
}
```

- Não use `@Transactional` em repositórios; o serviço é responsável pelo limite da transação.
- Retorne `Optional<T>` para buscas únicas, nunca `null`.
- Em consultas nativas, ainda associe parâmetros (`:name` / `?1`); nunca interpole strings.

## Índices e restrições

Declare unicidade, chaves estrangeiras e índices na migração, não no código da aplicação. Indexe as colunas usadas por seus repositórios em filtros e joins.

```sql
CREATE INDEX ix_payment_resource_id ON payment (resource_id);
ALTER TABLE payment
    ADD CONSTRAINT fk_payment_resource
    FOREIGN KEY (resource_id) REFERENCES resource (id);
```

## Mudança segura para rollback (expandir / contrair)

Nunca renomeie nem remova uma coluna na mesma release que implanta o código que a utiliza. Divida toda mudança incompatível entre releases para manter o rollback seguro.

| Fase | Migração | Release |
|---|---|---|
| Expandir | Adicione a nova coluna anulável ou tabela | N |
| Backfill | Copie os dados em lotes; faça gravação dupla na aplicação | N |
| Contrair | Remova a coluna/restrição antiga quando nada mais a ler | N+1 |

A skill [`safe-migration`](../skills/safe-migration/SKILL.md) detém o procedimento completo sem indisponibilidade e o checklist de backfill.

## Desempenho de consultas

Evite consultas N+1: busque associações com `@EntityGraph` ou `join fetch` em JPQL e verifique um plano real com `EXPLAIN ANALYZE`. A skill [`query-optimization`](../skills/query-optimization/SKILL.md) detém a análise de índices e planos.

```java
@EntityGraph(attributePaths = "payments")
List<Resource> findByLabelStartingWith(String prefix);
```

## Convenções

| Regra | Justificativa |
|---|---|
| `V<n>__snake_case.sql`, somente de avanço | Histórico determinístico e validado por checksum |
| Tabelas e colunas em `snake_case` | PostgreSQL idiomático e estável entre ferramentas |
| `NUMERIC` para dinheiro, `BigDecimal` no Java | Sem arredondamento binário de ponto flutuante em valores monetários |
| JPQL / consultas derivadas com parâmetros associados | Sem injeção de SQL e portável entre dialetos |
| Índices e FKs declarados em migrações | Schema reproduzível a partir do controle de versão |
| Expandir-contrair para mudanças incompatíveis | Toda implantação é segura para rollback |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Adicione uma nova migração `V<n+1>__` para corrigir o schema | Edite uma migração já aplicada |
| Associe todos os parâmetros | Concatene valores em SQL/JPQL |
| Mantenha `@Transactional` no serviço | Anote repositórios como transacionais |
| Faça backfill em lotes e depois contraia | Remova e recrie uma tabela ativa |

## Lista de verificação antes de abrir uma PR

- [ ] A migração segue `V<n>__snake_case.sql` e altera uma única coisa
- [ ] Nenhuma migração aplicada anteriormente foi editada
- [ ] Campos monetários/compactados usam `NUMERIC(p, s)` mapeado para `BigDecimal`
- [ ] Toda consulta associa parâmetros; não há concatenação de strings
- [ ] Novas colunas de filtro/join estão indexadas; as chaves estrangeiras estão declaradas
- [ ] Mudanças incompatíveis usam expandir → backfill → contrair entre releases
