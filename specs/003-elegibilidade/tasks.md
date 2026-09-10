# Tarefas — Validação de elegibilidade

Ordem de execução com testes antes da implementação de cada regra. Todas as
tarefas rodam por Docker, conforme o plano técnico.

## Esquema

- [x] T201 — Criar a migração `V5__add_eligibility_columns.sql` com as colunas
  `nis` e `docs_ok` em `beneficiary` e `eligibility_code`, `age_min`, `age_max`
  e `max_income` em `social_program`, todas com padrão que desativa a regra.
- [x] T202 — Estender `Beneficiary` com `nis` e `docsOk`, expondo apenas os
  acessos necessários à validação.
- [x] T203 — Estender `SocialProgram` com `eligibilityCode`, `ageMin`,
  `ageMax` e `maxIncome`.

## Saídas antecipadas

- [x] T204 — Escrever os testes das saídas antecipadas para `REQ-020`,
  `REQ-021` e `REQ-022`, confirmando que as regras seguintes não são avaliadas.
  `REQ-020` e `REQ-021` são atendidos pelo tratamento de recurso não
  encontrado da feature `001`; ver o plano técnico.
- [x] T205 — Implementar `EligibilityStatus` e `EligibilityReason`.
- [x] T206 — Escrever o teste de `REQ-023` cobrindo `AC-023.1` a `AC-023.3`,
  com comentário apontando `SIFAP-M-12`.
- [x] T207 — Implementar o desvio da região `99` em método isolado e nomeado,
  para que a remoção futura seja localizada.

## Regras acumulativas

- [x] T208 — Escrever os testes de `REQ-024`, incluindo situação cadastral
  desconhecida permanecendo elegível.
- [x] T209 — Escrever os testes de `REQ-025` e `REQ-026` com os limites
  inclusivos e o valor zero desativando o limite.
- [x] T210 — Implementar as verificações de situação cadastral, faixa etária e
  teto de renda.
- [x] T211 — Escrever os testes de `REQ-027`, `REQ-028`, `REQ-029` e `REQ-030`
  com os limites exatos definidos no plano.
- [x] T212 — Implementar `ProgramTypeRule`.
- [x] T213 — Escrever os testes de `REQ-031`, incluindo código vazio e
  conteúdo ignorado nas posições 3 a 5.
- [x] T214 — Implementar `EligibilityCode`.
- [x] T215 — Escrever o teste de precedência de motivos para `REQ-032`.
- [x] T216 — Implementar `EligibilityValidationService` na ordem definida no
  plano técnico.

## Integração

- [x] T217 — Escrever o teste de integração de `REQ-033`, confirmando que o
  beneficiário inelegível não gera pagamento e é contado como ignorado.
- [x] T218 — Integrar a validação em `PaymentGenerationService`, antes do
  cálculo e depois da validação de CPF, espelhando a posição do `CALLNAT` no
  legado.
- [x] T219 — Criar a migração `V6` com dados de demonstração de elegibilidade
  em `db/dev`, cobrindo ao menos um caso elegível, um inelegível e um de
  região `99`.
- [x] T219a — Corrigir os fixtures das features `001` e `002` que usavam
  programa do tipo `P` com beneficiário de 46 anos, agora inelegível por
  `REQ-028`. Motivo registrado em comentário nos dois testes.

## Validação

- [x] T220 — Executar `docker compose --profile test run --rm backend-test` e
  confirmar a suíte verde. Resultado: 75 testes, `BUILD SUCCESS`.
- [x] T221 — Executar `docker compose down -v && docker compose up --build` e
  validar manualmente a geração bloqueada por inelegibilidade. Resultado nos
  quatro casos semeados por `V6`:

  | Caso | CPF | Resultado |
  |---|---|---|
  | Elegível, 66 anos | `39053344705` | `GENERATED`, bruto `84,52` |
  | Região `99`, viola quatro regras | `15350946056` | `GENERATED`, bruto `40,00` |
  | 46 anos em programa tipo `P` | `11144477735` | `IGNORED`, `PENSION_AGE_BELOW_MINIMUM` |
  | Regressão da feature `001` | `52998224725` | `GENERATED`, bruto `138,84` |

- [x] T222 — Confirmar que todo `REQ-ID` desta feature aparece em ao menos um
  comentário inline de teste. Lacuna encontrada e corrigida: `REQ-020` e
  `REQ-021` não tinham teste; cobertos em `PaymentGenerationIntegrationTest`.
  Resultado: 77 testes, `BUILD SUCCESS`.
- [x] T223 — Executar a validação de rastreabilidade legada do job de CI
  `legacy-traceability`. Resultado: 43 `REQ-IDs` declarados em `specs/`,
  nenhuma falha de `source_legacy:`. Todos os requisitos desta feature citam
  `VALELEG.NSN`, `BATCHPGT.NSP`, `BENEFIC.ddm` ou `SOCPROG.ddm` com intervalo
  de linhas e arquivo existente.

  O job informativo `spec-traceability` aponta apenas os `REQ-PORTAL-*`, cujos
  testes vivem em `site/tests` e são varridos pelo script oficial. Nenhum
  `REQ-ID` das features `001`, `002` ou `003` ficou sem teste. Esse job emite
  `::warning` e não bloqueia o merge; o bloqueante é `legacy-traceability`.
- [ ] T224 — Medir, em produção, quantos beneficiários ativos recebem hoje por
  programa cujo tipo os recusaria. Bloqueia a implantação, não os testes.

  Consulta pronta em [`impact-query.sql`](impact-query.sql). É somente leitura
  e fica fora de `db/migration` de propósito, para que o Flyway não a execute.
  Deve rodar contra uma cópia dos dados de produção, substituindo o ano do
  período a processar.

  Responsáveis: Coordenação de Benefícios, DBA e operação do batch. Questão
  registrada em
  [`scope-decisions.md`](../../02-modern-spec/scope-decisions.md) e em
  [`pending-decisions.md`](../../docs/pending-decisions.md).

  Decisão a tomar com o resultado em mãos:

  | Resultado | Encaminhamento sugerido |
  |---|---|
  | Zero afetados | Implantar sem ação adicional |
  | Poucos afetados | Tratar caso a caso antes da implantação |
  | Muitos afetados | Não implantar; a regra legada provavelmente não reflete a operação real e precisa de decisão de negócio |

  **A consulta está verificada.** Executada em 2026-09-10 contra o banco de
  desenvolvimento, com os cinco beneficiários semeados por `V2`, `V4`, `V6` e
  `V7`. Resultado idêntico ao previsto antes da execução:

  | `motivo_de_recusa` | `program_code` | `program_type` | `beneficiarios_afetados` |
  |---|---|---|---|
  | `IDADE_ABAIXO_DO_MINIMO_PREVIDENCIARIO` | `P002` | `P` | 1 |

  Os quatro comportamentos relevantes foram exercitados: detectou o único
  beneficiário violador (46 anos em programa tipo `P`), ignorou os três
  conformes, respeitou o desvio da região `99` e restringiu-se a cadastros
  ativos.

  O que falta é apenas a execução contra os dados de produção. A ferramenta
  não é mais uma incógnita.

## Regras não implementadas por ausência de evidência

As regras abaixo constam da documentação de 2012 e **não** existem no código
de `VALELEG`. Não são tarefas desta feature e não devem ser implementadas sem
decisão humana registrada.

| Regra documentada em 2012 | Situação |
|---|---|
| Validação de dados bancários | Ausente do código lido |
| Limite de dois programas simultâneos | Campo `BN-QT-PROG` não localizado |
| Atualização cadastral em até 24 meses | Campo `BN-DT-ULT-ATUAL` não localizado |
| Auditoria bloqueante do tipo `B` | Ausente do código lido |
| Cruzamento com o CadÚnico | O próprio documento declara o código não localizado |

Consulte o achado `BONUS` correspondente em
[`mysteries-found.md`](../../01-archaeology/mysteries-found.md).
