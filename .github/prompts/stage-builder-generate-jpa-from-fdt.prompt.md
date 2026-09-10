---
name: "generate-jpa-from-fdt"
description: "Gera classes de entidade JPA a partir de definições FDT do Adabas, usando JSONB para campos MU/PE."
argument-hint: "ddm=01-archaeology/legacy-sifap/adabas-ddms/<DDM>.ddm context=<context> package=<java.package> dateformat=<format>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /generate-jpa-from-fdt

## Objetivo

Analisar um DDM Adabas e gerar entidade JPA com tipos corretos, tratamento explícito de MU/PE e migração Flyway correspondente.

## Quando usar

No início da Etapa 3, ao preparar a camada de dados de um contexto delimitado.

## Pré-condições

- `02-modern-spec/bounded-contexts.md` identifica o proprietário do DDM
- O DDM está em `01-archaeology/legacy-sifap/adabas-ddms/`
- O pacote de destino foi definido

## Entradas que a equipe deve fornecer

- Caminho do DDM
- Contexto delimitado e pacote Java
- Formato de data legado, como `YYYYMMDD` compactado ou `YYYY-MM-DD` alfanumérico

## O que farei

- Analisarei FDT, mapearei campos Java/JPA, tratarei MU como JSONB ou `@ElementCollection` e PE como entidades `@OneToMany`
- Gerarei DDL PostgreSQL 16 em Flyway
- Marcarei nomes crípticos com FIXME

## O que não farei

- Inventar significado ou formato de data
- Criar stored procedures
- Omitir campos MU/PE

## Formato da saída

1. `src/main/java/[package]/domain/[EntityName].java`
2. `db/migration/V[NNN]__create_[table_name].sql`

## Definição de pronto

- [ ] A entidade compila e cobre todos os campos
- [ ] MU usa JSONB (`@JdbcTypeCode(SqlTypes.JSON)`) ou `@ElementCollection`
- [ ] PE usa entidade separada com `@OneToMany`
- [ ] A migração é DDL PostgreSQL 16 válido
- [ ] Nomes crípticos têm `// FIXME: confirm semantics` e são encaminhados como questões em aberto

## Corpo do prompt

Você é `@builder`. Crie uma entidade JPA a partir do DDM indicado.

**Etapa 1 — Analisar FDT.** Extraia nível, nome curto, nome longo, formato A/N/P/B/D/T, tamanho e DE/MU/PE/SU. Apresente uma tabela para revisão.

**Etapa 2 — Mapear tipos.**

| Adabas | Java | JPA | Observações |
|---|---|---|---|
| A(n) | `String` | `@Column(length = n)` | |
| N(n) sem decimais | `Long` ou `Integer` | `@Column` | Use `Long` para IDs |
| N(n.m) | `BigDecimal` | `@Column(precision=n, scale=m)` | Sempre use para valores monetários |
| P(n.m) | `BigDecimal` | `@Column(precision=n, scale=m)` | Decimal compactado |
| D | `LocalDate` | `@Column` | Confirme o formato |
| T | `LocalDateTime` | `@Column` | |
| B(n) | `byte[]` | `@Lob` | Raro |
| Campo MU | `List<T>` | JSONB ou `@ElementCollection` | A equipe escolhe |
| Grupo PE | `List<EmbeddedEntity>` | `@OneToMany` | Entidade separada |

Para MU, apresente JSONB, mais simples e menos consultável, e `@ElementCollection`, mais consultável e com tabela separada. A equipe escolhe.

**Etapa 3 — Tratar PE.** Crie entidade e tabela próprias, `@ManyToOne` para o pai, campos mapeados e índice de ocorrência.

**Etapa 4 — Tratar superdescritores.** Adicione índice composto:

```java
@Table(indexes = @Index(columnList = "field_a, field_b"))
```

**Etapa 5 — Marcar nomes crípticos.**

```java
/** FIXME: confirm semantics with the team for Adabas field XX */
@Column(name = "xx_value", length = 20)
private String xxValue;
```

Solicite que uma pessoa registre a questão em `mysteries-found.md` com `path:line`; não responda nem altere o status.

**Etapa 6 — Gerar Flyway.** Use snake_case, tipos correspondentes, JSONB escolhido, tabelas PE, chaves, índices e `CHECK` óbvios. Nomeie `V[NNN]__create_[table_name].sql`.

**Etapa 7 — Verificar compilação.** Compile e informe problemas.

## Exemplo de chamada

```
/generate-jpa-from-fdt ddm=01-archaeology/legacy-sifap/adabas-ddms/<DDM>.ddm context=<context> package=<java.package> dateformat=<format>
```
