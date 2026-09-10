# Tarefas — Consulta de beneficiário

Ordem de execução com testes antes da implementação de cada regra. Todas as
tarefas rodam por Docker, conforme o plano técnico.

## Backend — esquema e consulta

- [x] T301 — Criar a migração `V8__create_audit_trail.sql` com as colunas que o
  sistema moderno consegue preencher, sem campos legados sem equivalente.
- [x] T302 — Criar `AuditTrail` e `AuditTrailRepository`.
- [x] T303 — Escrever os testes de `CpfMask` cobrindo `AC-037.1` e `AC-037.2`,
  incluindo a decisão de não replicar o ramo inseguro do legado.
- [x] T304 — Implementar `CpfMask`.
- [x] T305 — Escrever os testes de `BeneficiaryStatus` cobrindo `AC-038.1` a
  `AC-038.3`, incluindo a situação desconhecida.
- [x] T306 — Implementar `BeneficiaryStatusDescription`.
- [x] T307 — Acrescentar `findByNis` a `BeneficiaryRepository` e a consulta de
  histórico ordenada por período decrescente a `PaymentRepository`.

## Backend — serviço e endpoint

- [x] T308 — Escrever os testes de `REQ-034` a `REQ-036`, cobrindo busca por
  CPF, busca por NIS, não encontrado e CPF inválido sem acesso ao cadastro.
- [x] T309 — Escrever os testes de `REQ-039` a `REQ-041`, cobrindo o corte em
  doze, a ordenação decrescente e a ausência de pagamentos.
- [x] T310 — Escrever os testes de `REQ-042`, cobrindo a gravação da trilha na
  consulta bem-sucedida e a ausência de registro quando nada é encontrado.
- [x] T311 — Implementar `BeneficiaryQueryService` e os contratos de resposta.
- [x] T312 — Implementar `BeneficiaryQueryController` com
  `GET /api/v1/beneficiaries`, exigindo exatamente um critério.
- [x] T313 — Criar o seed `V9__seed_demo_payment_history.sql` com um
  beneficiário de mais de doze pagamentos fora de ordem cronológica, para
  exercitar `REQ-039` e `REQ-040` de ponta a ponta.

## Frontend

- [x] T314 — Criar o módulo `frontend/` com Next.js 15, TypeScript strict,
  Tailwind e Vitest, sem biblioteca de estado.
- [x] T315 — Acrescentar os serviços `frontend` e `frontend-test` ao
  `compose.yaml`, mantendo a execução por Docker.
- [x] T316 — Implementar o cliente de API e os contratos em `lib/`.
- [x] T317 — Implementar a página de consulta como Server Component, com o
  formulário isolado em Client Component.
- [x] T318 — Implementar a exibição do cadastro e do histórico, atendendo à
  base de acessibilidade do plano.
- [x] T319 — Escrever os testes de componente em Vitest, cobrindo a máscara
  exibida, a descrição da situação e a mensagem de ausência de pagamentos.

## Validação

- [x] T320 — Executar a suíte do backend por Docker e confirmar que as features
  `001` a `003` seguem verdes.
  **Evidência (2026-09-10):** `docker compose --profile test run --rm
  backend-test` → 108 testes, `BUILD SUCCESS`. Eram 77 antes desta feature.
- [x] T321 — Executar a suíte do frontend por Docker.
  **Evidência (2026-09-10):** `docker compose --profile test run --rm
  frontend-test` → 10 testes em 2 arquivos, todos verdes.
- [ ] T322 — Validar manualmente a consulta por CPF e por NIS com o ambiente
  em pé.
- [x] T323 — Confirmar que todo `REQ-ID` desta feature aparece em ao menos um
  comentário inline de teste.
- [x] T324 — Executar a validação de rastreabilidade legada.
  **Evidência (2026-09-10):** varredura de `specs/`, `02-modern-spec/` e
  `docs/` sem falhas de `source_legacy:`; validador de primitivas aprovado.

## Limitações conhecidas

| Limitação | Motivo |
|---|---|
| A trilha de auditoria não identifica quem consultou | Não há autenticação nesta feature; `USR-EVENT` do legado não tem equivalente. A trilha registra que houve acesso, não por quem. |
| O endereço do beneficiário não é exibido | O DDM tem os campos, mas a base moderna não os armazena. |
| Não há paginação do histórico | O legado corta em doze sem navegação. |
| `next@15.1.6` tem CVE conhecida | Atualização adiada por decisão registrada em `docs/pending-decisions.md`. O frontend só roda em `localhost`, sem dados reais; a atualização é obrigatória antes de qualquer exposição. |

## Divergências deliberadas em relação ao legado

| Comportamento legado | Decisão | Motivo |
|---|---|---|
| Máscara revela os três primeiros dígitos quando o CPF tem menos de 11 | Não replicado | Falha de privacidade marcada como `KNOWN INCONSISTENCY` no próprio código; o ramo é inalcançável na base moderna |
| Histórico rotulado "últimos 12" sem ordenar por período | Corrigido em `REQ-040` | O rótulo e o código legado discordam entre si; não há contrato a preservar |
