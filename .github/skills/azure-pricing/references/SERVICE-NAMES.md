# Referência de nomes de serviços do Azure

O campo `serviceName` da API Azure Retail Prices **diferencia maiúsculas de minúsculas**. Use esta referência para encontrar o nome exato do serviço a ser usado nos filtros.

## Computação

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Virtual Machines | `Virtual Machines` |
| Azure Functions | `Functions` |
| Azure App Service | `Azure App Service` |
| Azure Container Apps | `Azure Container Apps` |
| Azure Container Instances | `Container Instances` |
| Azure Kubernetes Service | `Azure Kubernetes Service` |
| Azure Batch | `Azure Batch` |
| Azure Spring Apps | `Azure Spring Apps` |
| Azure VMware Solution | `Azure VMware Solution` |

## Armazenamento

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Azure Storage (Blob, Files, Queues, Tables) | `Storage` |
| Azure NetApp Files | `Azure NetApp Files` |
| Azure Backup | `Backup` |
| Azure Data Box | `Data Box` |

> **Observação**: Blob Storage, Files, Disk Storage e Data Lake Storage usam o mesmo nome de serviço `Storage`. Use `meterName` ou `productName` para diferenciá-los (por exemplo, `contains(meterName, 'Blob')`).

## Bancos de dados

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Azure Cosmos DB | `Azure Cosmos DB` |
| Azure SQL Database | `SQL Database` |
| Azure SQL Managed Instance | `SQL Managed Instance` |
| Azure Database for PostgreSQL | `Azure Database for PostgreSQL` |
| Azure Database for MySQL | `Azure Database for MySQL` |
| Azure Cache for Redis | `Redis Cache` |

## IA e aprendizado de máquina

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Azure AI Foundry Models (incl. OpenAI) | `Foundry Models` |
| Azure AI Foundry Tools | `Foundry Tools` |
| Azure Machine Learning | `Azure Machine Learning` |
| Azure Cognitive Search (AI Search) | `Azure Cognitive Search` |
| Azure Bot Service | `Azure Bot Service` |

> **Observação**: os preços do Azure OpenAI agora estão em `Foundry Models`. Use `contains(productName, 'OpenAI')` ou `contains(meterName, 'GPT')` para filtrar modelos específicos da OpenAI.

## Rede

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Azure Load Balancer | `Load Balancer` |
| Azure Application Gateway | `Application Gateway` |
| Azure Front Door | `Azure Front Door Service` |
| Azure CDN | `Azure CDN` |
| Azure DNS | `Azure DNS` |
| Azure Virtual Network | `Virtual Network` |
| Azure VPN Gateway | `VPN Gateway` |
| Azure ExpressRoute | `ExpressRoute` |
| Azure Firewall | `Azure Firewall` |

## Análise de dados

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Azure Synapse Analytics | `Azure Synapse Analytics` |
| Azure Data Factory | `Azure Data Factory v2` |
| Azure Stream Analytics | `Azure Stream Analytics` |
| Azure Databricks | `Azure Databricks` |
| Azure Event Hubs | `Event Hubs` |

## Integração

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Azure Service Bus | `Service Bus` |
| Azure Logic Apps | `Logic Apps` |
| Azure API Management | `API Management` |
| Azure Event Grid | `Event Grid` |

## Gerenciamento e monitoramento

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Azure Monitor | `Azure Monitor` |
| Azure Log Analytics | `Log Analytics` |
| Azure Key Vault | `Key Vault` |
| Azure Backup | `Backup` |

## Web

| Serviço | Valor de `serviceName` |
|---------|-------------------|
| Azure Static Web Apps | `Azure Static Web Apps` |
| Azure SignalR | `Azure SignalR Service` |

## Dicas

- Se não tiver certeza sobre o nome de um serviço, **filtre primeiro por `serviceFamily`** para descobrir valores válidos de `serviceName` na resposta.
- Exemplo: `serviceFamily eq 'Databases' and armRegionName eq 'eastus'` retorna todos os nomes de serviços de banco de dados.
- Alguns serviços têm várias entradas `serviceName` para camadas ou gerações diferentes.
