---
name: "migration"
description: "Produza uma migração Flyway versionada e reversível para PostgreSQL 16, com etapas seguras em operação, preenchimento em lotes e script de reversão."
argument-hint: "req=REQ-NNN change=<natural-language-change>"
agent: "dba"
tools: ["read", "search", "edit", "execute"]
---
# /migration

## Objetivo

Produzir uma migração Flyway para **PostgreSQL 16** referente a uma alteração de esquema que seja (a) idempotente, (b) reversível, (c) segura para execução enquanto a aplicação atende ao tráfego e (d) rastreada até um `REQ-ID` em `specs/<NNN>-<feature>/spec.md`. A entrega contém uma migração de avanço versionada, um preenchimento em lotes quando necessário e um roteiro de reversão correspondente. Todos devem ser testados em uma cópia instantânea do ambiente de homologação.

> [!WARNING]
> Alterações destrutivas (excluir ou renomear uma coluna, alterar um tipo ou adicionar `NOT NULL`) nunca seguem em uma única implantação. Expanda, migre e depois contraia.

## Quando usar

Durante as Etapas 3 ou 4, quando uma tarefa em `plan.md` exigir uma alteração de esquema ou ao mapear um DDM do Adabas para sua primeira tabela PostgreSQL. Execute após registrar a alteração no plano. Nunca use este prompt para inventar um esquema.

## Pré-condições

- A alteração está presente em `specs/<NNN>-<feature>/plan.md`. Caso contrário, ela passa primeiro por uma revisão de arquitetura
- `specs/<NNN>-<feature>/spec.md` contém o `REQ-ID` e a declaração EARS atendidos pela alteração
- Uma pasta `db/migration/` existe no módulo do servidor ou será criada por esta migração
- Uma cópia instantânea do banco de dados de destino no ambiente de homologação está disponível para testes

## Entradas que a equipe deve fornecer

- A alteração solicitada em linguagem natural
- O `REQ-ID` vinculado e sua declaração EARS
- A escala dos dados: contagem de linhas das tabelas afetadas e consultas por segundo (QPS) no pico
- A janela de implantação: indisponibilidade zero obrigatória ou uma janela de manutenção permitida
- A referência do legado, se houver: o DDM do Adabas em `01-archaeology/legacy-sifap/adabas-ddms/` que origina este mapeamento
- Peça à pessoa usuária qualquer informação ausente

## O que farei

- Confirmarei se a alteração está em `plan.md` e depois escolherei uma versão Flyway `Vyyyymmddhhmm__short_description.sql`
- Projetarei uma sequência segura durante a operação: coluna anulável, preenchimento em lotes e restrições por último
- Mapearei fielmente os formatos do Adabas (decimal compactado do Natural `P9.2` / DDM `P 9,2` → `NUMERIC(9,2)`, `MU` → tabela filha ou JSONB, `PE` → tabela filha, superdescriptor ou descritor composto → índice composto)
- Escreverei um preenchimento idempotente separado para tabelas grandes e aplicarei as restrições somente após sua conclusão
- Escreverei a reversão `*.undo.sql` correspondente e documentarei os efeitos colaterais de replicação, `VACUUM` e armazenamento temporário de planos
- Testarei o avanço e a reversão em uma cópia instantânea do ambiente de homologação e colarei a saída

## O que não farei

- Projetar um esquema que não esteja em `plan.md`. Alterações não planejadas voltam para a revisão de arquitetura
- Adicionar `NOT NULL DEFAULT`, excluir ou renomear uma coluna de uma tabela grande e muito acessada em uma única instrução, pois isso reescreve ou bloqueia a tabela
- Entregar uma migração de avanço sem a reversão correspondente
- Criar um índice sem `CONCURRENTLY` ou preencher uma tabela inteira em uma transação
- Armazenar PII (CPF ou valores de benefícios) em uma nova coluna sem sinalizá-la e adicionar um `COMMENT` à coluna
- Escrever lógica de negócio no banco de dados (procedimentos armazenados). A lógica fica em Java
- Presumir o significado ou o conteúdo de um campo do Adabas. Mapeio somente o formato indicado pela equipe no DDM

## Formato da saída

```markdown
### Metadados da migração
Versão `V202603171430__add_reviewed_at.sql` · REQ-031 · segura durante a operação: sim · ~2 min para 4 milhões de linhas.

### Avanço: V202603171430__add_reviewed_at.sql
-- REQ-031: Enquanto um pagamento estiver em análise, o sistema deverá registrar a marca temporal da análise.
-- Segura durante a operação: adição anulável + índice CONCURRENTLY; sem reescrita da tabela.
ALTER TABLE payment ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ;
CREATE INDEX CONCURRENTLY idx_payment_reviewed_at ON payment (reviewed_at);
COMMENT ON COLUMN payment.reviewed_at IS 'Marca temporal da análise; não é PII.';

### Preenchimento (separado e idempotente): lotes de 5 mil
-- Execute fora da migração; faça commit entre os lotes até que nenhuma linha permaneça.

### Reversão: V202603171430__add_reviewed_at.undo.sql
DROP INDEX CONCURRENTLY IF EXISTS idx_payment_reviewed_at;
ALTER TABLE payment DROP COLUMN IF EXISTS reviewed_at;

### Coordenação com a aplicação
Implante o componente de escrita que preenche reviewed_at após esta migração. Os componentes de leitura aceitam NULL até o preenchimento ser concluído.

### Registro de riscos
Bloqueio: nenhum (CONCURRENTLY). Replicação: a criação do índice aumenta o atraso; monitore. Cache de planos: invalidado ao adicionar a coluna.
```

## Definição de pronto

- [ ] Os roteiros de avanço e reversão estão em `db/migration/`
- [ ] O roteiro de avanço é idempotente (`IF NOT EXISTS`, `IF EXISTS`)
- [ ] Nenhum bloqueio `ACCESS EXCLUSIVE` ocorre em uma tabela muito acessada sem uma nota explícita sobre a janela de manutenção
- [ ] O preenchimento processa mais de 100 mil linhas em lotes de mil a 10 mil, com um commit entre os lotes
- [ ] O `REQ-ID` vinculado e a declaração EARS aparecem em um comentário no início do arquivo
- [ ] A saída de `flyway migrate` e `flyway undo` em uma cópia instantânea do ambiente de homologação está incluída
- [ ] O plano de coordenação com a aplicação está declarado explicitamente

## Corpo do prompt

Você é `@dba`. A equipe precisa transformar uma alteração de esquema em uma migração segura e reversível. Leia [`safe-migration`](../skills/safe-migration/SKILL.md) antes de começar. Essa habilidade define o padrão expandir/migrar/contrair e a lista de verificação prévia.

**Etapa 1: confirme se a alteração está planejada.**
Verifique se a alteração aparece em `plan.md`. Caso contrário, pare e encaminhe-a para a revisão de arquitetura. A migração segue o plano, nunca o contrário. Registre o `REQ-ID` e a declaração EARS.

**Etapa 2: escolha a versão e mapeie os tipos.**
Nomeie o arquivo como `Vyyyymmddhhmm__short_description.sql`. Ao mapear um DDM do Adabas, converta os formatos fielmente: decimal compactado do Natural `P9.2` / DDM `P 9,2` → `NUMERIC(9,2)` (valores monetários usam `NUMERIC`, nunca `FLOAT`); `MU` → uma tabela filha ou JSONB; `PE` → uma tabela filha; um superdescriptor ou descritor composto → um índice composto. Na imagem de laboratório Natural CE 9.3.3, as especificações de formato Natural usam ponto como separador decimal. Portanto, `P9.2` significa nove dígitos inteiros mais dois dígitos fracionários. Formatos com vírgula, como `P9,2`, falham com `NAT0165` nas declarações de origem. Consulte [`natural-adabas`](../instructions/natural-adabas.instructions.md).

**Etapa 3: projete a migração para execução durante a operação.**
Prefira etapas aditivas que não bloqueiem: adicione uma coluna anulável, faça o preenchimento e adicione as restrições por último. Crie índices com `CREATE INDEX CONCURRENTLY`, sem `IF NOT EXISTS`, que exige uma proteção separada. Evite operações `ALTER TABLE` que exijam um bloqueio `ACCESS EXCLUSIVE` em uma tabela muito acessada. Se uma delas for inevitável, agende uma janela de manutenção e registre essa necessidade.

**Etapa 4: planeje o preenchimento.**
Para dados não triviais, escreva um preenchimento idempotente separado que processe de mil a 10 mil linhas por lote, com um `commit` entre os lotes. Nunca faça o preenchimento dentro da migração quando a tabela tiver mais de 100 mil linhas.

**Etapa 5: aplique as restrições após o preenchimento.**
Adicione `NOT NULL`, `CHECK`, chaves estrangeiras e índices únicos somente depois que os dados estiverem consistentes.

**Etapa 6: escreva a reversão.**
Associe cada migração de avanço a um arquivo `Vyyyymmddhhmm__short_description.undo.sql` que restaure o esquema anterior, mesmo a partir de um estado intermediário.

**Etapa 7: documente os efeitos colaterais e teste.**
Registre a divergência dos slots de replicação, as implicações para `VACUUM`, a invalidação do armazenamento temporário de planos e qualquer código da aplicação que precise ser entregue em conjunto. Restaure a cópia instantânea do ambiente de homologação, execute `flyway migrate`, verifique, execute `flyway undo`, verifique novamente e cole a saída.

Nunca insira lógica de negócio no banco de dados. Mascare CPF e valores de benefícios. Sinalize cada nova coluna de PII para o Engenheiro DevOps e o Líder Técnico.

## Exemplo de chamada

```
/migration req=REQ-031 change="adicionar uma marca temporal de análise anulável à tabela de pagamentos"
```
