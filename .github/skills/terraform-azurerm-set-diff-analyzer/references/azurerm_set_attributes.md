# Referência de atributos do tipo Set do AzureRM

Este documento apresenta uma visão geral e explica a manutenção de `azurerm_set_attributes.json`.

> **Última atualização**: 28 de janeiro de 2026

## Visão geral

`azurerm_set_attributes.json` é um arquivo de definição para atributos tratados como tipo Set pelo provedor AzureRM.
O script `analyze_plan.py` lê esse JSON para identificar "diferenças falsas positivas" em planos do Terraform.

### O que são atributos do tipo Set?

O tipo Set do Terraform é uma coleção que **não garante a ordem**.
Por isso, ao adicionar ou remover elementos, itens inalterados podem aparecer como "alterados".
Isso é chamado de "diferença falsa positiva".

## Estrutura do arquivo JSON

### Formato básico

```json
{
  "resources": {
    "azurerm_resource_type": {
      "attribute_name": "key_attribute"
    }
  }
}
```

- **key_attribute**: o atributo que identifica de maneira exclusiva os elementos do Set, como `name` ou `id`
- **null**: usado quando não há atributo-chave (compara o elemento inteiro)

### Formato aninhado

Quando um atributo Set contém outro atributo Set:

```json
{
  "rewrite_rule_set": {
    "_key": "name",
    "rewrite_rule": {
      "_key": "name",
      "condition": "variable",
      "request_header_configuration": "header_name"
    }
  }
}
```

- **`_key`**: o atributo-chave dos elementos Set nesse nível
- **Outras chaves**: definições dos atributos Set aninhados

### Exemplo: azurerm_application_gateway

```json
"azurerm_application_gateway": {
  "backend_address_pool": "name",           // Set simples (a chave é name)
  "rewrite_rule_set": {                     // Set aninhado
    "_key": "name",
    "rewrite_rule": {
      "_key": "name",
      "condition": "variable"
    }
  }
}
```

## Manutenção

### Como adicionar novos atributos

1. **Consulte a documentação oficial**
   - Procure o recurso no [Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
   - Verifique se o atributo está listado como "Set of ..."
   - Alguns recursos, como `azurerm_application_gateway`, têm atributos Set indicados explicitamente

2. **Consulte o código-fonte (mais confiável)**
   - Procure o recurso no [GitHub do provedor AzureRM](https://github.com/hashicorp/terraform-provider-azurerm)
   - Confirme `Type: pluginsdk.TypeSet` na definição do esquema
   - Identifique os atributos no `Schema` do Set que podem servir como `_key`

3. **Adicione ao JSON**

   ```json
   "azurerm_new_resource": {
     "set_attribute": "key_attribute"
   }
   ```

4. **Teste**

   ```bash
   # Verifique com um plano real
   python3 scripts/analyze_plan.py your_plan.json
   ```

### Como identificar atributos-chave

| Atributo-chave comum | Uso |
|---------------------|-------|
| `name` | Blocos nomeados (mais comum) |
| `id` | Referência ao ID do recurso |
| `location` | Localização geográfica |
| `address` | Endereço de rede |
| `host_name` | Nome do host |
| `null` | Quando não há chave (compara o elemento inteiro) |

## Ferramentas relacionadas

### analyze_plan.py

Analisa o JSON do plano do Terraform para identificar diferenças falsas positivas.

```bash
# Uso básico
terraform show -json plan.tfplan | python3 scripts/analyze_plan.py

# Ler de um arquivo
python3 scripts/analyze_plan.py plan.json

# Usar um arquivo de atributos personalizado
python3 scripts/analyze_plan.py plan.json --attributes /path/to/custom.json
```

## Recursos compatíveis

Consulte diretamente `azurerm_set_attributes.json` para ver os recursos compatíveis no momento:

```bash
# Listar recursos
jq '.resources | keys' azurerm_set_attributes.json
```

Principais recursos:

- `azurerm_application_gateway`: conjuntos de servidores de retaguarda, receptores (listeners), regras etc.
- `azurerm_firewall_policy_rule_collection_group`: coleções de regras
- `azurerm_frontdoor`: conjuntos de servidores de retaguarda e roteamento
- `azurerm_network_security_group`: regras de segurança
- `azurerm_virtual_network_gateway`: configuração de IP e do cliente VPN

## Observações

- O comportamento dos atributos pode variar conforme a versão do provedor ou da API
- Novos recursos e atributos precisam ser adicionados quando forem disponibilizados
- Definir todos os níveis de estruturas profundamente aninhadas melhora a precisão
