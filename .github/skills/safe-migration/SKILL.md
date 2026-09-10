---
name: "safe-migration"
description: "Use ao planejar uma alteração de esquema durante a operação, uma migração sem indisponibilidade ou a reversão de uma implantação que alterou uma tabela. Os gatilhos incluem \"migração\", \"ALTER TABLE\", \"sem indisponibilidade\", \"expandir e contrair\" e \"preenchimento retroativo\"."
---
# Migração segura de esquema

## Quando invocar

- "Planeje a migração para adicionar a coluna X."
- "Podemos renomear esta coluna sem indisponibilidade?"
- "Como removemos esta tabela com segurança?"

## Padrão expandir, migrar e contrair

Cada alteração de esquema que afeta o tráfego ativo passa por **três implantações**, nunca apenas uma.

1. **Expandir**: adicione a nova estrutura ao lado da antiga (nova coluna anulável, nova tabela ou novo índice). Nenhuma leitura ou escrita a utiliza ainda.
2. **Migrar**: grave simultaneamente nas estruturas antiga e nova, faça o preenchimento retroativo das linhas históricas e altere as leituras para a nova estrutura por meio de uma chave de funcionalidade.
3. **Contrair**: remova a estrutura antiga somente depois que a nova for a fonte autoritativa por pelo menos um ciclo de lançamento.

## Regras práticas

- **Alterações aditivas são sempre seguras**: nova coluna anulável, novo índice (CONCURRENTLY / ONLINE) ou nova tabela.
- **Alterações destrutivas nunca ocorrem em uma única implantação**: excluir ou renomear coluna, alterar tipo, excluir tabela ou adicionar NOT NULL.
- **Preenchimentos retroativos são executados em lotes**, com LIMIT, pausas entre lotes e idempotência. Nunca execute `UPDATE whole_table SET …` de uma só vez.
- **Criação de índices**: `CREATE INDEX CONCURRENTLY` (Postgres), `ONLINE=ON` (MySQL 8 / SQL Server). Monitore a escalada de bloqueios.
- **Renomeações**: NÃO renomeie diretamente. Adicione uma nova coluna → faça escrita dupla → execute o preenchimento retroativo → altere as leituras → remova a coluna antiga.

## Lista de verificação prévia à implantação

- [ ] A migração tem planos de **avanço** e de **reversão** documentados.
- [ ] A duração foi estimada em uma **cópia de produção** (nunca estime no ambiente de desenvolvimento).
- [ ] O impacto de bloqueios foi avaliado (`pg_locks`, `SHOW ENGINE INNODB STATUS`, `sys.dm_tran_locks`).
- [ ] O tamanho do lote de preenchimento retroativo foi definido de acordo com o orçamento de atraso da réplica.
- [ ] Há monitoramento para atraso da réplica, transações longas e impasses (deadlocks).
- [ ] Uma chave de funcionalidade ou um fluxo de leitura dupla foi instalado antes da etapa de migração.

## Sinais de alerta: não implante

- Um único `ALTER TABLE` que bloqueia integralmente uma tabela grande.
- Uma migração acoplada à implantação da aplicação que não pode ser revertida independentemente.
- Uma etapa irreversível sem cópia de segurança.
- Um preenchimento retroativo que reescreve todas as linhas em uma única transação.

## Modelo de saída

```markdown
## Plano de migração - <alteração>

| Campo | Valor |
|---|---|
| Tipo de alteração | aditiva / destrutiva |
| Etapa do padrão | Expandir / Migrar / Contrair |
| Arquivo de migração | backend/src/main/resources/db/migration/V<N>__<desc>.sql |
| Plano de avanço | <DDL / preenchimento retroativo> |
| Plano de reversão | <como reverter independentemente da implantação da aplicação> |
| Impacto de bloqueios | <estimativa obtida em uma cópia de produção> |

### Preenchimento retroativo
- Tamanho do lote <linhas>, pausa <ms>, idempotente sim/não
```

## Critérios de qualidade

- [ ] As alterações destrutivas estão divididas entre implantações de expansão, migração e contração.
- [ ] Existem planos de avanço e reversão independentes da implantação da aplicação.
- [ ] Os índices são criados com `CREATE INDEX CONCURRENTLY`; nenhum bloqueio integral de tabela é implantado.
- [ ] Os preenchimentos retroativos são executados em lotes limitados e idempotentes, dentro do orçamento de atraso da réplica.
- [ ] A duração e o impacto de bloqueios foram estimados em uma cópia com tamanho de produção.

## Referências

- [Braintree - PostgreSQL at Scale: Safe Migrations](https://medium.com/paypal-tech/postgresql-at-scale-database-schema-changes-without-downtime-20d3749ed680)
- [GitHub - gh-ost online schema migration](https://github.com/github/gh-ost)
- [Martin Fowler - Evolutionary Database Design](https://martinfowler.com/articles/evodb.html)
