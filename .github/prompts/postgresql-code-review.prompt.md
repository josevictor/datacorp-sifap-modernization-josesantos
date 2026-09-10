---
name: "postgresql-code-review"
description: "Revise SQL e esquema segundo boas práticas e antipadrões do PostgreSQL 16, delegando a lista de verificação à skill postgresql-code-review."
argument-hint: "selection=<sql-or-schema>"
agent: "dba"
tools: ["read", "search"]
---
# /postgresql-code-review

## Objetivo

Revisar SQL, esquema, funções e recursos de segurança do PostgreSQL (JSONB, matrizes, tipos personalizados e segurança em nível de linha, Row Level Security) em uma seleção ou em todo o projeto. Retornar um parecer com correções concretas. A lista de verificação completa está na habilidade [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md). Este prompt a aplica ao banco de dados do SIFAP 2.0 (PostgreSQL 16 por meio de JPA/Hibernate) sem repeti-la.

> [!IMPORTANT]
> Toda entrada da pessoa usuária concatenada em SQL é uma falha de injeção e resulta em rejeição automática. Vincule todos os parâmetros.

## Quando usar

Durante a revisão de código de uma migração, consulta, função ou alteração de esquema nas Etapas 3 ou 4, antes da mesclagem em `develop`.

## Pré-condições

- O SQL ou esquema em revisão está disponível (uma seleção, um arquivo de migração ou o projeto)
- As tabelas envolvidas e seus índices existentes são conhecidos ou podem ser consultados em `db/migration/`
- O destino é PostgreSQL 16

## Entradas que a equipe deve fornecer

- `selection`: o SQL, esquema ou migração a revisar (o padrão é a seleção ou o projeto atual)
- As tabelas envolvidas e todas as colunas de PII entre elas
- Peça à pessoa usuária qualquer informação ausente

## O que farei

- Aplicarei à seleção a lista de verificação da habilidade [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md)
- Verificarei as escolhas de tipos de dados (CITEXT, TIMESTAMPTZ, ENUM e JSONB), tipos de índice (GIN/GiST/parcial) e restrições
- Confirmarei se cada consulta está parametrizada e se cada coluna de PII está mascarada ou comentada
- Emitirei um parecer, Aprovada / Correção necessária / Rejeitada, com o SQL corrigido

## O que não farei

- Aprovar SQL com concatenação de cadeias de caracteres ou um parâmetro não vinculado
- Reescrever aqui o mapeamento da entidade JPA. As alterações de mapeamento voltam para o módulo responsável
- Tratar JSONB como uma cadeia de caracteres opaca ou ignorar operadores específicos do PostgreSQL
- Presumir que uma coluna contém ou não PII. Sinalizo tudo o que não estiver identificado

## Formato da saída

```markdown
### Parecer
Correção necessária: índice GIN ausente para uma consulta de contenção JSONB.

### Constatações
| # | Severidade | Constatação | Evidência |
|---|---|---|---|
| 1 | Alta | Filtro de status não parametrizado | `data->>'status' = '` + input |
| 2 | Média | Nenhum índice para `data @> ...` | Seq Scan em `orders` |

### SQL corrigido
CREATE INDEX idx_orders_data ON orders USING gin(data);
SELECT id FROM orders WHERE data @> :filter;
```

## Definição de pronto

- [ ] Um parecer está declarado: Aprovada / Correção necessária / Rejeitada
- [ ] Cada constatação tem severidade e evidência (arquivo/linha ou trecho de um plano)
- [ ] O SQL corrigido está parametrizado e pronto para uso
- [ ] Cada coluna de PII está mascarada ou contém um `COMMENT`

## Corpo do prompt

A habilidade [`postgresql-code-review`](../skills/postgresql-code-review/SKILL.md) define os antipadrões específicos do PostgreSQL e a lista de verificação de qualidade. Leia-a e depois aplique-a à seleção.

**Etapa 1: execute a análise estática.**
Rejeite a entrada concatenada da pessoa usuária. Sinalize `SELECT *` em tabelas largas, tipos genéricos quando houver tipos adequados do PostgreSQL e restrições ausentes.

**Etapa 2: aplique a habilidade.**
Percorra as áreas da habilidade: JSONB, matrizes, tipos/domínios personalizados, projeto de esquema, funções/gatilhos, extensões e RLS.

**Etapa 3: respeite as regras do conjunto.**
Confirme os recursos do PostgreSQL 16, o acesso parametrizado por JPA/Hibernate, as migrações com reversão segura em `backend/src/main/resources/db/migration/` e um `COMMENT` em cada coluna de PII.

**Etapa 4: emita o parecer.**
Declare Aprovada, Correção necessária ou Rejeitada com o SQL corrigido e as justificativas.

## Exemplo de chamada

```
/postgresql-code-review selection=backend/src/main/resources/db/migration/V3__payment.sql
```
