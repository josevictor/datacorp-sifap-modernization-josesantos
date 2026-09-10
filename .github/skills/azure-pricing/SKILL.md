---
name: "azure-pricing"
description: "Use quando a pessoa perguntar sobre o custo de um serviço do Azure, quiser comparar preços de SKUs ou regiões, precisar de dados de preço para uma estimativa ou perguntar sobre preços do Copilot Studio e consumo de créditos por agentes. Obtém preços de varejo em tempo real da API pública Azure Retail Prices (sem autenticação) e estima créditos do Copilot Studio. Os gatilhos incluem \"preços do Azure\", \"quanto custa\", \"comparar preço de SKU\", \"estimativa de custo\" e \"créditos do Copilot Studio\". Para transformar uma carga de trabalho existente em itens de otimização de custos, use az-cost-optimize."
---
# Preços do Azure

Obtenha preços de varejo do Azure em tempo real pela API pública Azure Retail Prices. Não é necessária autenticação, apenas acesso HTTPS de saída a `prices.azure.com`.

> [!NOTE]
> Esta habilidade depende de acesso de saída à Web (a ferramenta integrada `web_fetch` ou equivalente) para alcançar `prices.azure.com`. Se o acesso à Web não estiver disponível, informe isso e use como alternativa as tarifas em cache nos arquivos de referência.

## Quando usar

- "Quanto custa uma VM Standard_D4s_v5 em East US?"
- "Compare os preços do Blob Storage entre regiões."
- "Forneça uma estimativa mensal para esta arquitetura."
- "Quantos Copilot Credits nosso agente consumirá por mês?"

## Ponto de extremidade da API

```text
GET https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview
```

Acrescente `$filter` como parâmetro de consulta usando a sintaxe de filtro OData. Sempre use `api-version=2023-01-01-preview` para incluir dados de planos de economia.

## Passo a passo

Se algum aspecto da solicitação não estiver claro, faça perguntas para identificar os campos e valores corretos do filtro antes de chamar a API.

1. **Identifique os campos do filtro** na solicitação (nome do serviço, região, SKU e tipo de preço).
2. **Converta a região** em um `armRegionName` em minúsculas e sem espaços (`East US` torna-se `eastus`; `West Europe`, `westeurope`). Consulte a lista completa em [references/REGIONS.md](references/REGIONS.md).
3. **Crie o texto do filtro** com os campos abaixo e consulte a URL.
4. **Processe a matriz `Items`** da resposta JSON. Cada item contém o preço e os metadados.
5. **Siga a paginação** por `NextPageLink` somente se precisar de mais de 1.000 resultados, o que raramente é necessário.
6. **Calcule as estimativas** com as fórmulas em [references/COST-ESTIMATOR.md](references/COST-ESTIMATOR.md) para produzir valores mensais e anuais.
7. **Apresente os resultados** em uma tabela resumida com serviço, SKU, região, preço unitário e estimativas mensal e anual.

## Campos filtráveis

| Campo | Tipo | Exemplo |
|---|---|---|
| `serviceName` | cadeia de caracteres (exata, diferencia maiúsculas de minúsculas) | `'Functions'`, `'Virtual Machines'`, `'Storage'` |
| `serviceFamily` | cadeia de caracteres (exata, diferencia maiúsculas de minúsculas) | `'Compute'`, `'Storage'`, `'Databases'`, `'AI + Machine Learning'` |
| `armRegionName` | cadeia de caracteres (exata, em minúsculas) | `'eastus'`, `'westeurope'`, `'southeastasia'` |
| `armSkuName` | cadeia de caracteres (exata) | `'Standard_D4s_v5'`, `'Standard_LRS'` |
| `skuName` | cadeia de caracteres (aceita `contains`) | `'D4s v5'` |
| `priceType` | cadeia de caracteres | `'Consumption'`, `'Reservation'`, `'DevTestConsumption'` |
| `meterName` | cadeia de caracteres (aceita `contains`) | `'Spot'` |

Use `eq` para igualdade, `and` para combinar condições e `contains(field, 'value')` para correspondências parciais.

## Exemplos de filtros

| Finalidade | Valor de `$filter` |
|---|---|
| Preços de consumo de Functions em East US | `serviceName eq 'Functions' and armRegionName eq 'eastus' and priceType eq 'Consumption'` |
| VMs D4s v5 em West Europe (consumo) | `armSkuName eq 'Standard_D4s_v5' and armRegionName eq 'westeurope' and priceType eq 'Consumption'` |
| Todos os preços de Storage em uma região | `serviceName eq 'Storage' and armRegionName eq 'eastus'` |
| Preço Spot de uma SKU específica | `armSkuName eq 'Standard_D4s_v5' and contains(meterName, 'Spot') and armRegionName eq 'eastus'` |
| Preço de reserva de um ano | `serviceName eq 'Virtual Machines' and priceType eq 'Reservation' and armRegionName eq 'eastus'` |
| Azure AI / OpenAI (Foundry Models) | `serviceName eq 'Foundry Models' and armRegionName eq 'eastus' and priceType eq 'Consumption'` |
| Azure Cosmos DB | `serviceName eq 'Azure Cosmos DB' and armRegionName eq 'eastus' and priceType eq 'Consumption'` |

## Exemplo completo de URL de consulta

```text
https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&$filter=serviceName eq 'Functions' and armRegionName eq 'eastus' and priceType eq 'Consumption'
```

Ao criar a URL, codifique os espaços como `%20` e as aspas como `%27`.

## Principais campos da resposta

```json
{
  "Items": [
    {
      "retailPrice": 0.000016,
      "unitPrice": 0.000016,
      "currencyCode": "USD",
      "unitOfMeasure": "1 Execution",
      "serviceName": "Functions",
      "skuName": "Premium",
      "armRegionName": "eastus",
      "meterName": "vCPU Duration",
      "productName": "Functions",
      "priceType": "Consumption",
      "isPrimaryMeterRegion": true,
      "savingsPlan": [
        { "unitPrice": 0.000012, "term": "1 Year" },
        { "unitPrice": 0.000010, "term": "3 Years" }
      ]
    }
  ],
  "NextPageLink": null,
  "Count": 1
}
```

Use somente os itens cujo `isPrimaryMeterRegion` seja `true`, a menos que a pessoa solicite medidores não primários.

## Valores de serviceFamily aceitos

`Analytics`, `Compute`, `Containers`, `Data`, `Databases`, `Developer Tools`, `Integration`, `Internet of Things`, `Management and Governance`, `Networking`, `Security`, `Storage`, `Web`, `AI + Machine Learning`.

## Dicas

- Os valores de `serviceName` diferenciam maiúsculas de minúsculas. Em caso de dúvida, filtre primeiro por `serviceFamily` para descobrir valores válidos de `serviceName`.
- Se os resultados estiverem vazios, amplie o filtro. Remova primeiro as restrições de `priceType` ou região.
- Os preços estão em USD, a menos que `currencyCode` seja definido na solicitação.
- Para preços de planos de economia, procure a matriz `savingsPlan` em cada item. Ela só está presente com `2023-01-01-preview`.
- Consulte nomes comuns de serviços e a capitalização correta em [references/SERVICE-NAMES.md](references/SERVICE-NAMES.md).

## Solução de problemas

| Problema | Solução |
|---|---|
| Resultados vazios | Amplie o filtro. Remova primeiro `priceType` ou `armRegionName` |
| Nome de serviço incorreto | Use o filtro `serviceFamily` para descobrir valores válidos de `serviceName` |
| Dados de plano de economia ausentes | Confirme que a URL contém `api-version=2023-01-01-preview` |
| Erros de URL | Verifique a codificação: espaços como `%20` e aspas como `%27` |
| Resultados demais | Adicione mais campos de filtro (região, SKU, priceType) para restringir a consulta |

## Estimativa de uso de agentes do Copilot Studio

Use esta seção quando a pessoa perguntar sobre preços do Copilot Studio, Copilot Credits ou custos de uso de agentes.

### Fatos principais

- **1 Copilot Credit = 0,01 USD.**
- Os créditos são agrupados em todo o locatário.
- Agentes voltados a funcionários licenciados para M365 Copilot recebem respostas clássicas, respostas generativas e fundamentação no grafo do locatário sem custo.
- A aplicação do excedente é acionada ao atingir 125% da capacidade pré-paga.

### Etapas da estimativa

1. **Colete as entradas**: tipo de agente (funcionário/cliente), quantidade de usuários, interações por mês, percentual de conhecimento, percentual do grafo do locatário e uso de ferramentas por sessão.
2. **Obtenha as tarifas de cobrança atuais** com a ferramenta de consulta à Web para que a estimativa use os preços atuais da Microsoft.
3. **Processe o conteúdo obtido** para extrair a tabela atual de tarifas de cobrança (créditos por tipo de funcionalidade).
4. **Calcule a estimativa**:
   - `total_sessions = users * interactions_per_month`
   - Créditos de conhecimento: aplique as tarifas de fundamentação no grafo do locatário, resposta generativa e resposta clássica.
   - Créditos de ferramentas do agente: aplique a tarifa de ação do agente por chamada de ferramenta.
   - Créditos de fluxo do agente: aplique a tarifa de fluxo a cada 100 ações.
   - Créditos de modificação de instrução: aplique as tarifas básica, padrão e premium a cada 10 respostas.
5. **Apresente os resultados** em uma tabela dividida por categoria, com o total de créditos e o custo estimado em USD.

### URLs de origem a consultar

| URL | Conteúdo |
|---|---|
| `https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management` | Tabela de tarifas, exemplos de cobrança e regras de excedente |
| `https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing` | Opções de licenciamento, inclusões do M365 Copilot, pré-pago comparado ao pagamento conforme o uso |

Consulte pelo menos a primeira URL (tarifas de cobrança) antes de calcular. Consulte [references/COPILOT-STUDIO-RATES.md](references/COPILOT-STUDIO-RATES.md) para obter um registro instantâneo em cache das tarifas, fórmulas e exemplos, usado como alternativa quando a consulta à Web não estiver disponível.

## Modelo de saída

Apresente os preços de varejo em uma tabela que informe a fonte e as premissas:

```markdown
## Preços do Azure: Standard_D4s_v5, eastus

| Serviço | SKU | Região | Preço unitário | Unidade | Estimativa mensal |
|---|---|---|---|---|---|
| Virtual Machines | Standard_D4s_v5 | eastus | $0.192 | 1 hora | ~$140 (730 h) |
| Virtual Machines | Standard_D4s_v5 (plano de economia de 1 ano) | eastus | $0.113 | 1 hora | ~$82 (730 h) |

Fonte: API Azure Retail Prices, api-version 2023-01-01-preview, consultada em 2026-08-17. Preços em USD. Considera 730 h/mês e somente isPrimaryMeterRegion.
```

## Critérios de qualidade

- [ ] A região é convertida em um `armRegionName` válido em minúsculas.
- [ ] O filtro usa `serviceName`/`serviceFamily` exatos e com a capitalização correta.
- [ ] Somente itens com `isPrimaryMeterRegion == true` são usados, salvo solicitação de medidores não primários.
- [ ] `api-version=2023-01-01-preview` é usada para disponibilizar dados de planos de economia quando relevantes.
- [ ] As estimativas mensais/anuais informam suas premissas (horas, quantidade) e citam a API e a data da consulta.
- [ ] A moeda é informada (USD, salvo especificação em contrário).
- [ ] As estimativas do Copilot Studio usam tarifas recém-consultadas ou informam explicitamente o uso do cache.
