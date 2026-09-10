# Runbook operacional

![Tipo: runbook](https://img.shields.io/badge/Tipo-Manual%20operacional-171717?style=flat-square)
![Responsável: DevOps](https://img.shields.io/badge/Respons%C3%A1vel-DevOps-737373?style=flat-square)

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Runbook**

**Guia operacional para executar, verificar e diagnosticar o ambiente da imersão.**

| Campo | Valor |
|---|---|
| **Público-alvo** | DevOps Engineer e o time inteiro |
| **Pré-requisitos** | Setup local concluído conforme [`00-SETUP.md`](../00-SETUP.md) |
| **Resultado esperado** | Ambiente local funcionando, CI compreensível e escalonamento correto |

---

## Verificações iniciais (primeiro uso)

- [ ] **Verifique os pré-requisitos** — execute cada linha e confirme que nenhum erro ocorre:

```bash
git --version
java -version
node --version
docker --version
specify version
```

> [!NOTE]
> O kit não inclui um protótipo pronto. Quando o time criar `backend/`, `frontend/` e, se necessário, `infra/`, registre aqui os comandos reais de execução.

Depois de criar o protótipo, documente:

| Serviço | URL / Comando |
|---|---|
| Health do backend | — |
| Swagger UI | — |
| Frontend local | — |
| Credenciais da demonstração | — |

---

## Rotina diária

- [ ] **Verifique o estado do repositório:**

```bash
git status
```

- [ ] **Execute os testes do backend** (quando `backend/` existir):

```bash
cd backend && ./mvnw test
```

- [ ] **Execute os testes do frontend** (quando `frontend/` existir):

```bash
cd frontend && npm test
```

---

## CI — Entenda os fluxos de trabalho

A CI é executada automaticamente em pushes para `main`, `develop`, `spec/**` e `impl/**`.

| Arquivo de fluxo de trabalho | O que verifica | Quando é executado |
|---|---|---|
| `ci.yml` | Backend `mvn verify`, frontend lint + test + typecheck, Terraform fmt + validate | Em cada push e PR |
| `spec-quality.yml` | markdownlint e rastreabilidade dos REQ-IDs | Quando arquivos `.md` ou `specs/` mudam |

- [ ] **Quando a CI falhar** — abra a aba Actions no GitHub, selecione a execução que falhou e leia o log.
- [ ] **Corrija localmente** — reproduza o erro com os comandos do protótipo criado pelo time antes de fazer outro push.

---

## Azure — Estágio 4

O Estágio 4 é o momento em que o time aplica o Terraform a uma assinatura de sandbox fornecida pelos facilitadores.

> [!CAUTION]
> Cada time tem uma única cota de assinatura. Marque todos os recursos com `team=workshop-XX` ou `apply` falhará.

```bash
cd infra
terraform init
terraform plan -var-file=envs/dev/terraform.tfvars
terraform apply -var-file=envs/dev/terraform.tfvars
```

---

## Problemas comuns

| Sintoma | Causa provável | Correção | Como confirmar |
|---|---|---|---|
| O ambiente local trava | A porta 5432, 8080 ou 3000 já está em uso | Execute `lsof -i :5432` e encerre o processo | O serviço inicia sem erro de porta |
| `mvn verify` falha no Testcontainers | O Docker não está em execução | Inicie o Docker Desktop | Os testes passam na próxima execução |
| `pnpm test` falha nos snapshots | O componente foi alterado intencionalmente | Execute `pnpm test -- -u` para atualizar os snapshots | Os testes passam após a atualização |
| `terraform apply` é rejeitado | O recurso não tem a tag `team=` | Adicione a tag ao recurso que falhou | `terraform plan` não apresenta erros de validação |
| O GitHub Actions não consegue acessar o Azure | Divergência na declaração do subject OIDC | Execute `az ad sp create-for-rbac` novamente para o time | O fluxo de trabalho passa na próxima execução |

---

## Quando escalar para o facilitador

- [ ] O build falha há mais de 20 minutos sem solução.
- [ ] A assinatura do Azure parece estar suspensa.
- [ ] Uma ação irreversível foi executada por engano, como `terraform destroy`.

Use o formato de escalonamento em três linhas descrito em [`00-TEAM-FLOW.md §4`](../00-TEAM-FLOW.md).

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [FAQ](FAQ.md)<br/><sub>Perguntas frequentes.</sub> | [Solução de problemas](troubleshooting.md)<br/><sub>Erros comuns e soluções.</sub> |

<sub>[Voltar ao índice do kit](README.md)</sub>
