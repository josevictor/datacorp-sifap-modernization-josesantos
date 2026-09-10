# Plano técnico — Validação de elegibilidade

## Objetivo

Implementar `VALELEG.NSN` em Java 21 e Spring Boot 3.3, preservando o
comportamento observável dos requisitos `REQ-020` a `REQ-033`. A validação
passa a ser executada pela geração mensal antes do cálculo, fechando a lacuna
de fidelidade da feature `001`.

## Limites do módulo

- **Entrada:** CPF e código do programa.
- **Domínio:** ordem de avaliação, regras por tipo de programa, código de
  elegibilidade e acúmulo de motivos.
- **Persistência:** leitura de beneficiário e programa; nenhuma escrita nova.
- **Saída:** resultado de elegibilidade com código e primeiro motivo.
- **Não incluído:** cadastro, CadÚnico, auditoria e a decisão de `SIFAP-M-12`.
- **Execução:** todos os comandos por Docker/Compose.

O módulo permanece em `com.datacorp.sifap.payments`. A elegibilidade não forma
contexto próprio nesta etapa: ela só é consumida pela geração de pagamento e
compartilha os agregados `Beneficiary` e `SocialProgram`.

## A ordem de avaliação é comportamento observável

`VALELEG` não é um conjunto de regras independentes. A ordem determina o
resultado, porque três verificações encerram a rotina antecipadamente e porque
apenas o primeiro motivo acumulado é devolvido.

| Ordem | Verificação | Efeito |
|---|---|---|
| 1 | Beneficiário inexistente | Encerra com `2001` |
| 2 | Programa inexistente | Encerra com `2003` |
| 3 | Programa inativo | Encerra com `2004` |
| 4 | Região `99` | Encerra como elegível |
| 5 | Situação cadastral | Acumula motivo |
| 6 | Faixa etária do programa | Acumula motivo |
| 7 | Teto de renda | Acumula motivo |
| 8 | Regras por tipo de programa | Acumula motivo |
| 9 | Código de elegibilidade | Acumula motivo |
| 10 | Resultado | `2010` com o primeiro motivo |

A implementação preserva essa ordem explicitamente. Reordenar as verificações
mudaria a mensagem devolvida ao operador, ainda que a decisão final continuasse
a mesma.

## Componentes planejados

1. **`EligibilityStatus`:** resultado com código, elegibilidade e motivos
   acumulados, expondo apenas o primeiro conforme `REQ-032`.
2. **`EligibilityReason`:** enumeração dos motivos, espelhando as mensagens do
   legado sem replicar texto livre.
3. **`ProgramTypeRule`:** regras por tipo `A`, `P` e `T`, com o tipo
   desconhecido tratado como recusa.
4. **`EligibilityCode`:** interpreta as posições `R` e `D` do código de cinco
   caracteres, ignorando as demais.
5. **`EligibilityValidationService`:** orquestra a ordem acima.
6. **Migração Flyway `V5`:** adiciona as colunas ausentes.
7. **Integração em `PaymentGenerationService`:** conforme `REQ-033`.

## Campos ausentes no modelo atual

A feature `001` modelou apenas o necessário para o cálculo. A validação exige
campos que ainda não existem:

| Entidade | Coluna nova | Tipo | Origem |
|---|---|---|---|
| `beneficiary` | `nis` | `BIGINT` | `BENEFIC.ddm` `NUM-NIS` |
| `beneficiary` | `docs_ok` | `CHAR(1)` | `BENEFIC.ddm` `IND-DOCS-OK` |
| `social_program` | `eligibility_code` | `VARCHAR(5)` | `SOCPROG.ddm` `COD-ELIGIBILITY` |
| `social_program` | `age_min` | `SMALLINT` | `SOCPROG.ddm` `AGE-MIN` |
| `social_program` | `age_max` | `SMALLINT` | `SOCPROG.ddm` `AGE-MAX` |
| `social_program` | `max_income` | `NUMERIC(7,2)` | `SOCPROG.ddm` `MAX-PERCAP-INCOME` |

As colunas entram com valor padrão que desativa a regra correspondente, para
que os dados existentes mantenham o comportamento atual: `age_min`, `age_max`
e `max_income` em zero, e `nis` em zero. Isso reproduz a semântica legada, na
qual zero significa "sem limite".

## Numeração das migrações

`db/migration` e `db/dev` compartilham o histórico do Flyway:

| Versão | Local | Conteúdo |
|---|---|---|
| `V1` | `db/migration` | Esquema da geração mensal |
| `V2` | `db/dev` | Dados de demonstração da geração |
| `V3` | `db/migration` | Tabela `payment_discount` |
| `V4` | `db/dev` | Dados de demonstração de descontos |
| `V5` | `db/migration` | Colunas de elegibilidade |
| `V6` | `db/dev` | Dados de demonstração de elegibilidade |

## Divergências legadas preservadas deliberadamente

| Divergência | Decisão |
|---|---|
| `MAX-PERCAP-INCOME` é comparado com a renda familiar, não com a per capita | Preservar. Corrigir mudaria quem recebe benefício. Registrado em `REQ-026`. |
| Tipos `P` e `T` usam idades fixas no código, ignorando `AGE-MIN` e `AGE-MAX` do programa | Preservar. As duas verificações coexistem e ambas podem recusar. |
| Situação cadastral fora de `A`, `S`, `C`, `D` e `I` não gera motivo e permanece elegível | Preservar. O `IF` aninhado do legado não tem ramo final. |
| A região `99` dispensa as validações seguintes | Preservar. Questão `SIFAP-M-12`. |
| `VALELEG` recalcula a idade sem a janela de século aplicada por `BATCHPGT` | **Não preservar a divergência.** Ver a seção seguinte. |

## O cálculo de idade não replica a divergência do legado

No legado, `BATCHPGT` aplica a janela de século Y2K antes de calcular a idade e
envia o valor por PDA; `VALELEG` descarta esse parâmetro e recalcula a idade
direto de `DT-BIRTH`, sem a janela. Para cadastros ainda gravados como
`YYMMDD`, os dois programas obtêm idades diferentes no mesmo processamento.

A implementação moderna usa uma única fonte de idade, derivada de
`Beneficiary`. A divergência não é replicada por três razões:

1. Ela é consequência de um contrato de PDA não revisto, não de regra de
   negócio.
2. O modelo moderno armazena a data como `YYYYMMDD` completo, então a condição
   que dispara a janela não ocorre.
3. Replicá-la exigiria criar deliberadamente duas fontes de verdade, o mesmo
   antipadrão já rejeitado em `SIFAP-M-10`.

A divergência permanece registrada como achado `BONUS` para validação humana.

## Dados e invariantes

- A validação é somente leitura e não altera beneficiário nem programa.
- Motivos são acumulados na ordem de avaliação e apenas o primeiro é devolvido.
- Zero desativa limite em `age_min`, `age_max` e `max_income`.
- Código de elegibilidade vazio ou em branco desativa `REQ-031`.
- As posições 3 a 5 do código de elegibilidade são ignoradas.
- Comparações de idade e renda usam limites inclusivos, conforme o legado.

## Estratégia de testes

- Testes unitários por regra, com os limites exatos `59`/`60` para o tipo `P`,
  `15`/`16` e `65`/`66` para o tipo `T`, e `600,00`/`600,01` para o tipo `A`.
- Teste de cada saída antecipada, confirmando que as regras seguintes não são
  avaliadas.
- Teste confirmando que programa inativo tem precedência sobre a região `99`.
- Teste confirmando que a região `99` dispensa as regras seguintes, com
  comentário apontando `SIFAP-M-12`.
- Teste da precedência do motivo devolvido quando há mais de uma violação.
- Teste de situação cadastral desconhecida permanecendo elegível.
- Teste de integração confirmando que o inelegível não gera pagamento.
- Cada teste cita o `REQ-ID` correspondente em comentário inline.
- PostgreSQL 16 do Compose para integração, conforme ADR-0003.

## Estratégia Docker

- `docker compose --profile test run --rm backend-test` para os testes.
- `docker compose down -v && docker compose up --build` para validação manual.
- As migrações `V5` e `V6` rodam automaticamente na subida.

## Os padrões inertes não cobrem as regras por tipo de programa

A migração `V5` inicia `age_min`, `age_max`, `max_income` e `nis` em zero e
`docs_ok` em `S`, preservando o comportamento anterior para os dados já
cadastrados. Isso funciona para as regras parametrizadas pelo cadastro.

**Não funciona para as regras por tipo de programa.** `REQ-027` a `REQ-030`
usam limites fixos no código legado e passam a valer imediatamente, sem
parâmetro que as desative:

| Tipo | Efeito imediato |
|---|---|
| `A` | Recusa documentação diferente de `S` e renda acima de `600,00` sem dependentes |
| `P` | Recusa idade inferior a 60 anos |
| `T` | Recusa idade fora de 16 a 65 anos |
| Outro | Recusa sempre |

Consequência concreta observada durante a implementação: os testes das features
`001` e `002` usavam programas do tipo `P` com um beneficiário de 46 anos.
Todos passavam antes desta feature e passariam a falhar depois dela, porque o
legado genuinamente recusaria esse beneficiário. Os fixtures foram corrigidos
para o tipo `A`, e o motivo está registrado em comentário nos dois testes.

Antes de implantar, é necessário medir quantos beneficiários ativos hoje
recebem pagamento por um programa cujo tipo os recusaria. O número não pode ser
estimado a partir do repositório: depende dos dados de produção.

## Requisitos atendidos pelo comportamento já existente

`REQ-020` e `REQ-021` descrevem os códigos `2001` e `2003` do legado para
beneficiário e programa inexistentes. No sistema moderno, `PaymentGenerationService`
já resolve esses casos com `PaymentGenerationNotFoundException`, estabelecido na
feature `001`. A validação não repete a busca: ela recebe as entidades já
resolvidas.

Os códigos permanecem declarados em `EligibilityReason` para preservar a
rastreabilidade com o legado, mas o caminho observável é a resposta de
recurso não encontrado.

## Riscos e decisões pendentes

| Risco | Mitigação |
|---|---|
| A região `99` pode ser bypass indevido e esta feature o perpetua | Isolar em método próprio, cobrir por teste explícito e manter `SIFAP-M-12` aberto para reversão barata. |
| Adicionar validação pode reprovar beneficiários que hoje recebem pagamento | Migrar com limites em zero, preservando o comportamento atual até o cadastro ser preenchido. **Mitigação parcial:** as regras por tipo de programa não têm parâmetro que as desative e passam a valer de imediato. Ver a seção sobre padrões inertes. |
| Beneficiários ativos em programa cujo tipo os recusaria deixam de receber na primeira execução | Medir o volume em produção antes de implantar. O repositório não permite estimar o número. |
| A documentação de 2012 descreve regras inexistentes | Não implementar nada sem evidência no código; registrado como achado `BONUS`. |
| O nome `MAX-PERCAP-INCOME` induz a corrigir a comparação | Documentar no código e no requisito que a divergência é deliberada. |

## Ordem de implementação

1. Criar a migração `V5` com as colunas de elegibilidade.
2. Escrever os testes unitários das saídas antecipadas.
3. Implementar `EligibilityStatus` e `EligibilityReason`.
4. Escrever os testes unitários por tipo de programa.
5. Implementar `ProgramTypeRule` e `EligibilityCode`.
6. Implementar `EligibilityValidationService` na ordem definida.
7. Escrever o teste de precedência de motivos.
8. Integrar em `PaymentGenerationService` conforme `REQ-033`.
9. Escrever o teste de integração do bloqueio.
10. Executar a análise de rastreabilidade dos `REQ-ID`.
