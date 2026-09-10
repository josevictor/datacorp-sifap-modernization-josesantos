---
name: "az-cost-optimize"
description: "Analise recursos do Azure e IaC Terraform para reduzir custos e abra issues de acompanhamento no GitHub, delegando o fluxo de trabalho à skill az-cost-optimize."
argument-hint: "rg=<resource-group> repo=<owner/name>"
agent: "devops-engineer"
tools: ["read", "search", "execute"]
---
# /az-cost-optimize

## Objetivo

Analisar os recursos implantados no Azure e a respectiva IaC Terraform, produzir recomendações de otimização de custos baseadas em evidências e abrir uma issue no GitHub para cada oportunidade, além de uma EPIC de coordenação. O fluxo de trabalho completo está na skill [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md). Este prompt o aplica ao kit SIFAP 2.0 sem repeti-lo.

> [!IMPORTANT]
> A IaC do kit usa somente Terraform. Considere as referências da skill a Bicep/ARM fora do escopo e nunca abra uma issue sobre uma economia que não esteja respaldada por preços validados.

## Quando usar

Durante a Etapa 4 (Evolução), depois que a equipe provisionar recursos do Azure e quiser acompanhar reduções de custos como issues do GitHub.

## Pré-condições

- A equipe está autenticada no Azure e no repositório GitHub de destino
- O Terraform do sistema moderno existe em `infra/` (criado pela equipe nas Etapas 3 ou 4)
- O grupo de recursos e a assinatura de destino são conhecidos

## Entradas que a equipe deve fornecer

- `rg`: o grupo de recursos do Azure de destino
- `repo`: o `owner/name` do repositório GitHub das issues
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Seguirei o fluxo de descoberta, métricas e recomendações da skill [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md)
- Lerei somente o Terraform em `infra/` como fonte da verdade da IaC
- Validarei cada custo atual e custo-alvo nos preços do Azure antes de recomendar
- Abrirei uma issue no GitHub para cada otimização e uma EPIC, usando a CLI `gh`

## O que não farei

- Analisar templates Bicep ou ARM, pois estão fora do escopo deste kit
- Inventar recursos ou economias quando não houver Terraform; informarei a situação e interromperei o trabalho
- Abrir issues antes de a equipe confirmar o resumo
- Recomendar uma alteração sem evidências validadas e sem considerar a reversão

## Formato da saída

```markdown
### Resumo
Recursos analisados: 7 · Atual: $X/mês · Economia potencial: $Y/mês · Oportunidades: 4

### Issues a criar
- [COST-OPT] Plano do App Service S3 → B2 — $X/mês (baixo risco)
- [EPIC] Otimização de custos do Azure — potencial de $Y/mês
```

## Definição de pronto

- [ ] Toda economia foi validada em relação ao SKU/nível do recurso e aos preços do Azure
- [ ] As recomendações referenciam o Terraform em `infra/`, não Bicep/ARM
- [ ] Uma issue por oportunidade e uma EPIC foram criadas via `gh` após a confirmação
- [ ] Cada issue contém evidências, risco e etapas de validação

## Corpo do prompt

A skill [`az-cost-optimize`](../skills/az-cost-optimize/SKILL.md) define o procedimento de descoberta, métricas, pontuação e criação de issues. Leia-a e aplique-a ao grupo de recursos de destino.

**Etapa 1 — Descobrir.**
Enumere os recursos em `rg` e leia o Terraform em `infra/` como configuração pretendida.

**Etapa 2 — Aplicar a skill.**
Colete métricas de uso, valide os custos atuais e gere recomendações pontuadas conforme a skill.

**Etapa 3 — Respeitar as regras do kit.**
Ignore Bicep/ARM. Se não houver Terraform, informe e interrompa o trabalho. Mantenha o GitHub como fonte da verdade.

**Etapa 4 — Confirmar e criar.**
Apresente o resumo, aguarde a aprovação e abra as issues e a EPIC com `gh`.

## Exemplo de chamada

```
/az-cost-optimize rg=sifap-prod-rg repo=my-org/sifap-2
```
