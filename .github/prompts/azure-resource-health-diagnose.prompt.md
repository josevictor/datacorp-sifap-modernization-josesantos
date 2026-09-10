---
name: "azure-resource-health-diagnose"
description: "Diagnostique a integridade de um recurso do Azure com base em logs e telemetria e produza um plano de remediação, delegando o fluxo de trabalho à skill azure-resource-health-diagnose."
argument-hint: "resource=<name> rg=<resource-group>"
agent: "devops-engineer"
tools: ["read", "search", "execute"]
---
# /azure-resource-health-diagnose

## Objetivo

Avaliar a integridade de um recurso do Azure, diagnosticar problemas com base em logs e telemetria e produzir um plano de remediação priorizado. O fluxo completo está na skill [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md). Este prompt o aplica ao kit SIFAP 2.0 sem repeti-lo.

> [!NOTE]
> Diagnostique antes de alterar: classifique os problemas por gravidade e confirme qualquer correção em relação ao Terraform em `infra/`.

## Quando usar

Durante a Etapa 4 (Evolução), quando um recurso implantado no Azure apresentar comportamento inesperado e a equipe precisar de um diagnóstico estruturado antes de agir.

## Pré-condições

- A equipe está autenticada no Azure
- O recurso está implantado e emitindo logs ou telemetria
- As configurações de diagnóstico encaminham os logs a um espaço de trabalho acessível do Log Analytics

## Entradas que a equipe deve fornecer

- `resource`: o nome do recurso e, se conhecidos, seu grupo de recursos e sua assinatura
- O sintoma observado e quando começou
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Seguirei o fluxo de avaliação de integridade e análise de logs da skill [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md)
- Priorizarei os tipos de recurso do kit: Azure Database for PostgreSQL 16 e serviços Spring Boot conteinerizados
- Classificarei os problemas como Critical, High, Medium ou Low e relacionarei cada um à causa raiz
- Produzirei um plano de remediação em fases, com etapas de validação e reversão

## O que não farei

- Aplicar uma remediação antes do diagnóstico e da confirmação da equipe
- Recomendar uma alteração manual que divirja do Terraform em `infra/`
- Ignorar Managed Identity; sinalizarei recursos que ainda usem chaves compartilhadas ou strings de conexão
- Exagerar a certeza quando faltarem logs; registrarei a limitação

## Formato da saída

```markdown
### Avaliação de integridade — payment-db (Azure Database for PostgreSQL)
Status: Warning · Analisado em: <timestamp>

### Problemas
| Gravidade | Problema | Causa raiz |
|---|---|---|
| High | Falhas de conexão | Limite máximo de conexões esgotado |

### Remediação em fases
1. Imediata — aumentar o limite de conexões ou adicionar pooling
2. Curto prazo — adequar o nível de computação via Terraform
```

## Definição de pronto

- [ ] O estado de integridade foi declarado com métricas de apoio
- [ ] Os problemas foram classificados por gravidade, cada um com uma causa raiz
- [ ] O plano de remediação está dividido em fases, com validação e reversão
- [ ] Toda correção está expressa em relação ao Terraform em `infra/`

## Corpo do prompt

A skill [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md) define os diagnósticos específicos por tipo de recurso e as consultas KQL. Leia-a e aplique-a ao recurso de destino.

**Etapa 1 — Identificar.**
Localize o recurso, seu tipo e suas dependências.

**Etapa 2 — Aplicar a skill.**
Execute as verificações de integridade e as consultas de logs ou telemetria conforme a skill e reconheça os padrões de falha.

**Etapa 3 — Respeitar as regras do kit.**
Priorize PostgreSQL 16 e serviços Spring Boot, sinalize autenticação que não use Managed Identity e vincule as correções ao Terraform em `infra/`.

**Etapa 4 — Planejar.**
Classifique os problemas e produza o plano de remediação em fases. Aguarde confirmação antes de agir.

## Exemplo de chamada

```
/azure-resource-health-diagnose resource=payment-db rg=sifap-prod-rg
```
