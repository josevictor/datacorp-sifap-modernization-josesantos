# Tarefas — Geração mensal de pagamento

## Testes primeiro

- [x] T001 — Criar testes para aceitar/rejeitar períodos conforme `REQ-001`.
- [x] T002 — Criar testes para beneficiário ativo e inativo conforme `REQ-002`.
- [x] T003 — Criar testes para CPF válido, inválido e registro de rejeição conforme `REQ-003`.
- [x] T004 — Criar teste de integração que impeça duplicidade CPF + período conforme `REQ-004`.
- [x] T005 — Criar testes da fórmula de valor bruto e truncamento conforme `REQ-005`.
- [x] T006 — Criar testes de tipo de pagamento em dezembro e nos demais meses conforme `REQ-006`.
- [x] T007 — Criar testes de abono para programas tipo `A` e demais tipos conforme `REQ-007`.
- [x] T008 — Criar testes de líquido zero e líquido positivo conforme `REQ-008`.
- [x] T009 — Criar teste de integração de persistência com situação `G` conforme `REQ-009`.

## Implementação

- [x] T010 — Criar objetos de valor para período, CPF e dinheiro, vinculando validações a `REQ-001`, `REQ-003` e `REQ-005`.
- [x] T011 — Implementar o serviço de cálculo mensal com fatores e truncamento conforme `REQ-005` a `REQ-008`.
- [x] T012 — Implementar consulta de beneficiário e programa com rejeição de estados inválidos conforme `REQ-002`.
- [x] T013 — Implementar consulta de duplicidade e restrição persistente para CPF + período conforme `REQ-004`.
- [x] T014 — Implementar serviço de aplicação que coordene validação, cálculo e persistência conforme `REQ-001` a `REQ-009`.
- [x] T015 — Implementar o adaptador de entrada e respostas de sucesso, rejeição e ignorado conforme os critérios de aceitação.
- [x] T016 — Adicionar logs operacionais sem CPF exposto e tratamento de erros conforme as instruções de segurança.
- [x] T017 — Criar `backend/Dockerfile` para build e execução da aplicação Java 21 sem depender de Java ou Maven no host.
- [x] T018 — Criar Compose de desenvolvimento com serviços `backend` e `db`, usando PostgreSQL 16 em contêiner e variáveis vindas de `.env`.
- [x] T019 — Criar serviço ou perfil Compose de testes para executar os testes do backend em contêiner.
- [x] T020 — Documentar os comandos Docker de build, teste e execução no README do backend.

## Verificação

- [x] T021 — Executar os testes direcionados do backend via Docker/Compose.
- [x] T022 — Verificar cada `REQ-ID` contra seu teste correspondente.
- [x] T023 — Confirmar que `CALCDSCT`, região `99`, proporcionalidade e IPCA permanecem fora do escopo.
- [x] T024 — Executar a validação de rastreabilidade legada antes da revisão.
  Executada em 2026-09-10 sobre `specs/` inteiro junto com a feature `003`:
  43 `REQ-IDs` declarados, nenhuma falha de `source_legacy:`.
- [x] T025 — Confirmar que nenhum comando obrigatório da feature depende de banco, Java ou Maven instalados no host.

## Evidência de execução

Suíte executada em 2026-09-10 com
`docker compose --profile test run --rm backend-test`:

```text
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

| Classe de teste | Testes | Requisitos cobertos |
|---|---|---|
| `PaymentGenerationIntegrationTest` | 4 | `REQ-002`, `REQ-003`, `REQ-004`, `REQ-009` |
| `PaymentCalculationServiceTest` | 6 | `REQ-005`, `REQ-006`, `REQ-007`, `REQ-008` |
| `CpfValidatorTest` | 3 | `REQ-003` |
| `YearMonthPeriodTest` | 2 | `REQ-001` |

Os testes rodam contra o serviço `db-test`, um PostgreSQL 16 efêmero isolado
do banco de desenvolvimento. Sem esse isolamento, o seed de demonstração e os
pagamentos criados manualmente quebram as contagens verificadas.

Verificado manualmente com `docker compose up`:

| Item | Resultado |
|---|---|
| `GET /actuator/health` | `{"status":"UP"}` |
| `POST /api/v1/payments/monthly-generations` | `201` com `outcome=GENERATED` |
| Valor bruto do caso demo | `138.84`, idêntico ao cálculo de `CALCBENF.NSN` |
| Tipo de pagamento fora de dezembro | `N`, conforme `REQ-006` |
| Abono fora de dezembro | `0.00`, conforme `REQ-007` |

Conferência do caso demo (`CPF 52998224725`, período `202609`):

`100,00 × 1,3500 × 1,1000 × 0,8500 × 1,0000 × 1,1000 = 138,8475` truncado para `138,84`.
