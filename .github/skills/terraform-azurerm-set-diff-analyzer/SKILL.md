---
name: "terraform-azurerm-set-diff-analyzer"
description: "Use quando um plano do Terraform para recursos AzureRM mostrar muitas alterações, embora apenas um elemento tenha sido adicionado ou removido, para separar diferenças falsas positivas de ordenação de Set das alterações reais. Abrange Application Gateway, Load Balancer, Firewall, Front Door e NSG. Os gatilhos incluem \"ruído no terraform plan\", \"diferença de tipo Set\", \"todos os elementos alterados\", \"diferença espúria\" e \"filtrar falsos positivos na CI\"."
---
# Analisador de diferenças em conjuntos do Terraform AzureRM

Identifique **diferenças falsas positivas** em planos do Terraform causadas por atributos do tipo Set do provedor AzureRM e diferencie-as de alterações reais. A IaC deste kit usa Terraform (`azurerm ~> 3.x`), portanto esta habilidade se aplica diretamente à árvore `infra/` criada pela equipe no Estágio 3.

## Quando invocar

- "O `terraform plan` mostra dezenas de alterações, mas adicionei apenas uma regra de NSG."
- "Meu plano do Application Gateway diz que todas as regras de roteamento mudaram. Isso é real?"
- "Como evito que o ruído de ordenação de Set bloqueie a revisão do plano na CI?"
- "Quais destas diferenças do Load Balancer realmente modificarão o recurso?"

## Contexto

O tipo Set do Terraform compara elementos por posição, não por uma chave estável. Por isso, adicionar ou remover um elemento pode fazer todos aparecerem como "alterados". Esse comportamento geral do Terraform é especialmente visível em recursos AzureRM que dependem muito de atributos do tipo Set: Application Gateway, Load Balancer, Firewall, Front Door e NSG. Essas diferenças falsas positivas não alteram o recurso implantado, mas ocultam as mudanças reais e tornam a revisão do plano sujeita a erros.

## Pré-requisitos

- Python 3.8+ (somente a biblioteca padrão; sem pacotes de terceiros).

Se o Python não estiver disponível, instale-o pelo gerenciador de pacotes (`brew install python3`, `apt install python3`) ou pelo [python.org](https://www.python.org/downloads/).

## Uso básico

```bash
terraform plan -out=plan.tfplan                 # 1. capture o plano
terraform show -json plan.tfplan > plan.json    # 2. exporte-o como JSON
python scripts/analyze_plan.py plan.json        # 3. classifique as diferenças
```

O analisador lê o plano JSON, inspeciona atributos do tipo Set nos recursos AzureRM compatíveis e informa quais recursos mostram apenas alterações de ordem (falsos positivos) e quais têm adições, remoções ou modificações reais.

## Interpretação dos resultados

| Sinal | Significado | Ação |
|---|---|---|
| Alteração apenas de ordem em um atributo Set | Falso positivo, sem alteração real | Pode ser ignorado com segurança; registre na solicitação de pull |
| Elemento adicionado ou removido | Alteração real | Revise antes de executar `terraform apply` |
| Valor de atributo modificado | Alteração real | Revise antes de executar `terraform apply` |
| Recurso ausente da lista de compatibilidade | Não analisado | Inspecione manualmente |

Os recursos compatíveis e seus atributos do tipo Set estão em [references/azurerm_set_attributes.md](references/azurerm_set_attributes.md). As opções completas da interface de linha de comando (CLI), os formatos de saída, os códigos de saída e os exemplos de CI/CD estão em [scripts/README.md](scripts/README.md).

## Solução de problemas

| Problema | Solução |
|---|---|
| `python: command not found` | Use `python3` ou instale o Python 3.8+ |
| `ModuleNotFoundError` | O script usa apenas a biblioteca padrão; confirme que o Python 3.8+ está ativo |
| Um recurso não foi classificado | Confirme que ele aparece em `references/azurerm_set_attributes.md`; caso contrário, revise-o manualmente |

## Modelo de saída

Informe a classificação em uma tabela e acrescente um parecer de uma linha:

```markdown
## Análise de diferenças de Set — plan.json

| Recurso | Atributo Set | Parecer | Alterações reais |
|---|---|---|---|
| azurerm_application_gateway.main | request_routing_rule | Falso positivo (apenas ordem) | 0 |
| azurerm_network_security_group.web | security_rule | Alteração real | +1 / -0 |

Total: 2 recursos analisados, 1 falso positivo e 1 com alterações reais.
Parecer: revise a alteração da regra de NSG antes de aplicar o plano; a diferença do gateway pode ser ignorada com segurança.
```

## Critérios de qualidade

- [ ] Um plano JSON foi produzido com `terraform show -json` antes da análise.
- [ ] `scripts/analyze_plan.py` foi executado no plano JSON com Python 3.8+.
- [ ] Cada recurso sinalizado está classificado como falso positivo (apenas ordem) ou alteração real.
- [ ] As alterações reais são revisadas antes de `terraform apply`; os falsos positivos são documentados como seguros para ignorar.
- [ ] Todos os recursos fora da lista de compatibilidade foram revisados manualmente.
