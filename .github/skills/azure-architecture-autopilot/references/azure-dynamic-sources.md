# Registro de fontes dinâmicas do Azure

Este arquivo gerencia **somente as fontes (URLs) de informações que mudam com frequência**.
Os valores reais (versão da API, SKU, região etc.) não são registrados aqui.
Sempre consulte as URLs abaixo para verificar as informações mais recentes antes de gerar Bicep.

---

## 1. Versão da API do Bicep (consulta obrigatória)

Referência do Bicep no Microsoft Docs por serviço. Verifique a `apiVersion` estável mais recente nessas URLs antes de usá-la.

| Serviço | URL do Microsoft Docs |
|---------|-------------|
| CognitiveServices (Foundry/OpenAI) | https://learn.microsoft.com/en-us/azure/templates/microsoft.cognitiveservices/accounts |
| AI Search | https://learn.microsoft.com/en-us/azure/templates/microsoft.search/searchservices |
| Storage Account | https://learn.microsoft.com/en-us/azure/templates/microsoft.storage/storageaccounts |
| Key Vault | https://learn.microsoft.com/en-us/azure/templates/microsoft.keyvault/vaults |
| Virtual Network | https://learn.microsoft.com/en-us/azure/templates/microsoft.network/virtualnetworks |
| Private Endpoints | https://learn.microsoft.com/en-us/azure/templates/microsoft.network/privateendpoints |
| Private DNS Zones | https://learn.microsoft.com/en-us/azure/templates/microsoft.network/privatednszones |
| Fabric | https://learn.microsoft.com/en-us/azure/templates/microsoft.fabric/capacities |
| Data Factory | https://learn.microsoft.com/en-us/azure/templates/microsoft.datafactory/factories |
| Application Insights | https://learn.microsoft.com/en-us/azure/templates/microsoft.insights/components |
| ML Workspace (Hub) | https://learn.microsoft.com/en-us/azure/templates/microsoft.machinelearningservices/workspaces |

> **Sempre verifique também os recursos filhos**: recursos como `accounts/projects`, `accounts/deployments` e `privateDnsZones/virtualNetworkLinks` podem ter versões da API diferentes das do recurso pai. Siga os links dos recursos filhos na página do recurso pai para verificar.

### Serviços ausentes da tabela

A tabela inclui somente os serviços do escopo da v1. Para outros serviços, monte e consulte a URL neste formato:

```
https://learn.microsoft.com/en-us/azure/templates/microsoft.{provider}/{resourceType}
```

---

## 2. Disponibilidade de modelos (obrigatória ao usar modelos do Foundry/OpenAI)

Verifique se o modelo pode ser implantado na região de destino. Não dependa de conhecimento estático.

| Método de verificação | URL / comando |
|--------------------|---------------|
| Disponibilidade do modelo no Microsoft Docs | https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models |
| Interface de linha de comando (CLI) do Azure, para recursos existentes | `az cognitiveservices account list-models --name "<NAME>" --resource-group "<RG>" -o table` |

> Se o modelo não estiver disponível na região de destino → informe a pessoa e sugira regiões ou modelos alternativos disponíveis. Não faça substituições sem aprovação.

---

## 3. Mapeamento de endpoint privado (Private Endpoint) ao adicionar novos serviços

O Azure pode alterar os mapeamentos de `groupId` de PE e de DNS Zone. Ao adicionar novos serviços ou quando for necessário verificar:

| Método de verificação | URL |
|--------------------|-----|
| Documentação oficial da integração de DNS de PE | https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns |

> Os mapeamentos dos principais serviços em `service-gotchas.md` são estáveis, mas sempre confirme novamente na URL acima ao adicionar novos serviços.

---

## 4. Disponibilidade regional dos serviços

Verifique se um serviço específico está disponível em determinada região:

| Método de verificação | URL |
|--------------------|-----|
| Disponibilidade dos serviços do Azure por região | https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/ |

---

## 5. Azure Updates (fonte secundária)

As fontes abaixo servem **somente como referência**. A fonte principal é sempre a documentação oficial do Microsoft Docs.

| Fonte | URL | Finalidade |
|--------|-----|---------|
| Azure Updates | https://azure.microsoft.com/en-us/updates/ | Acompanhar alterações dos serviços |
| Novidades no Azure | Páginas oficiais What's New ("Novidades") de cada serviço no Microsoft Docs | Verificar alterações de funcionalidades |

---

## Regra de decisão: quando consultar?

| Tipo de informação | Consulta obrigatória? | Motivo |
|-----------------|-------------|-----------|
| Versão da API | **Sempre** | Muda com frequência; valores incorretos causam falha na implantação |
| Disponibilidade do modelo (nome, região) | **Sempre** | Varia por região e muda com frequência |
| Lista de SKUs | **Sempre** | Pode mudar por serviço |
| Disponibilidade regional | **Sempre** | O suporte regional de cada serviço muda com frequência. Sempre verifique se o serviço está disponível na região informada |
| `groupId` de PE e DNS Zone | Pode consultar `service-gotchas.md` para os principais serviços da v1; **deve consultar para novos serviços ou configurações complexas (Monitor etc.)** | Os principais mapeamentos são estáveis, mas serviços novos ou complexos apresentam riscos |
| Padrões de propriedades obrigatórias | Consulte primeiro os arquivos de referência | Quase imutáveis (`isHnsEnabled` etc.) |
