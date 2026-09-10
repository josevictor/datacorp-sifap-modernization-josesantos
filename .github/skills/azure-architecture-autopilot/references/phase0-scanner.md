# Fase 0: examinador de recursos existentes

Este arquivo contém as instruções detalhadas da Fase 0. Leia-o e siga-o quando houver uma solicitação de análise de recursos existentes do Azure (Caminho B).

Os resultados aparecem em um diagrama de arquitetura. Solicitações posteriores de modificação em linguagem natural seguem para a Fase 1.

> **🚨 Regra do caminho de armazenamento das saídas**: salve todas as saídas (JSON do exame, HTML do diagrama e código Bicep) em **uma pasta de projeto no diretório de trabalho atual (cwd)**. NUNCA salve em `~/.copilot/session-state/`. Esse diretório é temporário e pode ser excluído ao encerrar a sessão.

---

## Etapa 1: autenticação no Azure e seleção do escopo

### 1-A: verificar a autenticação no Azure

```powershell
az account show 2>&1
```

- Se houver autenticação → siga para a Etapa 1-B
- Se não houver autenticação → peça para executar `az login`

### 1-B: selecionar assinaturas (aceita seleção múltipla)

```powershell
az account list --output json
```

Apresente a lista de assinaturas como opções de `ask_user`. **É possível selecionar várias assinaturas:**

```
ask_user({
  question: "Selecione as assinaturas do Azure que deseja analisar. Para selecionar várias, adicione uma por vez.",
  choices: [
    "sub-002 (Assinatura padrão atual) (Recomendado)",
    "sub-001",
    "Analisar todas as assinaturas acima"
  ]
})
```

- Uma assinatura selecionada → examine somente essa assinatura
- "Analisar todas" selecionado → examine todas as assinaturas
- Para adicionar assinaturas → use `ask_user` novamente

### 1-C: selecionar o escopo (aceita vários RGs)

```
ask_user({
  question: "Qual escopo de recursos do Azure você deseja analisar?",
  choices: [
    "Especificar um grupo de recursos (Recomendado)",
    "Selecionar vários grupos de recursos",
    "Todos os grupos de recursos da assinatura atual"
  ]
})
```

- **Grupo de recursos (RG) específico** → selecione na lista ou informe manualmente
- **Vários RGs** → repita `ask_user` para adicionar um por vez. Pare quando a pessoa disser que terminou.
  Como alternativa, aceite vários RGs separados por vírgulas (por exemplo, `rg-prod, rg-dev, rg-network`)
- **Assinatura inteira** → `az group list` → examine todos os RGs (avise que muitos recursos podem exigir tempo)

**É possível combinar várias assinaturas e vários RGs:**

- rg-prod da assinatura A + rg-network da assinatura B → examine ambos e apresente um único diagrama

---

## Hierarquia do diagrama: exibição de várias assinaturas/RGs

**Uma assinatura + um RG**: somente o limite da VNet
**Vários RGs (mesma assinatura)**: limite tracejado para cada RG
**Várias assinaturas**: limite em dois níveis, assinatura > RG

Passe as informações de hierarquia no JSON do diagrama:

**Adicione os campos `subscription` e `resourceGroup` ao JSON `services`:**

```json
{
  "id": "foundry",
  "name": "foundry-xxx",
  "type": "ai_foundry",
  "subscription": "sub-002",
  "resourceGroup": "rg-prod",
  "details": [...]
}
```

**Passe a hierarquia pelo parâmetro `--hierarchy`:**

```
--hierarchy '[{"subscription":"sub-002","resourceGroups":["rg-prod","rg-dev"]},{"subscription":"sub-001","resourceGroups":["rg-network"]}]'
```

Com essas informações, o script do diagrama:

- Vários RGs → representa cada RG como um agrupamento com limite tracejado (rótulo: nome do RG)
- Várias assinaturas → aninha os limites de RG em limites maiores de assinatura
- Exibe os limites da VNet dentro do RG ao qual ela pertence

---

## Etapa 2: examinar recursos

**🚨 Princípios para a saída da interface de linha de comando (CLI) az:**

- A saída da CLI az deve **sempre ser salva em arquivo** e lida com `view`. A saída direta do terminal pode ser truncada.
- Agrupe **no máximo três comandos az** por chamada do PowerShell. Muitos comandos podem exceder o tempo limite.
- Use `--query` JMESPath para extrair somente os campos necessários e reduzir a saída.

```powershell
# ✅ Abordagem correta: salva em arquivo e depois lê
az resource list -g "<RG>" --query "[].{name:name,type:type,kind:kind,location:location}" -o json | Set-Content -Path "$outDir/resources.json"

# ❌ Abordagem incorreta: saída direta no terminal (pode ser truncada)
az resource list -g "<RG>" -o json
```

### 2-A: listar todos os recursos e apresentar

```powershell
$outDir = "<project-name>/azure-scan"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

# Etapa 1: lista básica de recursos (nome, tipo, kind e local)
az resource list -g "<RG>" --query "[].{name:name,type:type,kind:kind,location:location,id:id}" -o json | Set-Content "$outDir/resources.json"
```

**🚨 Imediatamente após ler resources.json, apresente a tabela completa de recursos:**

```
📋 Lista de recursos de rg-<RG> (N recursos)

┌─────────────────────────┬──────────────────────────────────────────────┬─────────────────┐
│ Nome                    │ Tipo                                         │ Local           │
├─────────────────────────┼──────────────────────────────────────────────┼─────────────────┤
│ my-storage              │ Microsoft.Storage/storageAccounts             │ koreacentral    │
│ my-keyvault             │ Microsoft.KeyVault/vaults                    │ koreacentral    │
│ ...                     │ ...                                          │ ...             │
└─────────────────────────┴──────────────────────────────────────────────┴─────────────────┘

⏳ Obtendo informações detalhadas...
```

Apresente **primeiro** essa tabela. Não deixe a pessoa esperando sem saber quais recursos existem.

### 2-B: consulta detalhada dinâmica baseada em resources.json

**Determine dinamicamente os comandos de consulta conforme os tipos encontrados em resources.json.**

Não use uma lista fixa de comandos. Execute somente os comandos dos tipos presentes em resources.json, conforme a tabela.

**Mapeamento de tipo → comando de consulta detalhada:**

| Tipo em resources.json | Comando de consulta detalhada | Arquivo de saída |
|---|---|---|
| `Microsoft.Network/virtualNetworks` | `az network vnet list -g "<RG>" --query "[].{name:name,addressSpace:addressSpace.addressPrefixes,subnets:subnets[].{name:name,prefix:addressPrefix,pePolicy:privateEndpointNetworkPolicies}}" -o json` | `vnets.json` |
| `Microsoft.Network/privateEndpoints` | `az network private-endpoint list -g "<RG>" --query "[].{name:name,subnetId:subnet.id,targetId:privateLinkServiceConnections[0].privateLinkServiceId,groupIds:privateLinkServiceConnections[0].groupIds,state:provisioningState}" -o json` | `pe.json` |
| `Microsoft.Network/networkSecurityGroups` | `az network nsg list -g "<RG>" --query "[].{name:name,location:location,subnets:subnets[].id,nics:networkInterfaces[].id}" -o json` | `nsg.json` |
| `Microsoft.CognitiveServices/accounts` | `az cognitiveservices account list -g "<RG>" --query "[].{name:name,kind:kind,sku:sku.name,endpoint:properties.endpoint,publicAccess:properties.publicNetworkAccess,location:location}" -o json` | `cognitive.json` |
| `Microsoft.Search/searchServices` | `az search service list -g "<RG>" --query "[].{name:name,sku:sku.name,publicAccess:properties.publicNetworkAccess,semanticSearch:properties.semanticSearch,location:location}" -o json 2>$null` | `search.json` |
| `Microsoft.Compute/virtualMachines` | `az vm list -g "<RG>" --query "[].{name:name,size:hardwareProfile.vmSize,os:storageProfile.osDisk.osType,location:location,nicIds:networkProfile.networkInterfaces[].id}" -o json` | `vms.json` |
| `Microsoft.Storage/storageAccounts` | `az storage account list -g "<RG>" --query "[].{name:name,sku:sku.name,kind:kind,hns:properties.isHnsEnabled,publicAccess:properties.publicNetworkAccess,location:location}" -o json` | `storage.json` |
| `Microsoft.KeyVault/vaults` | `az keyvault list -g "<RG>" --query "[].{name:name,location:location}" -o json 2>$null` | `keyvault.json` |
| `Microsoft.ContainerService/managedClusters` | `az aks list -g "<RG>" --query "[].{name:name,kubernetesVersion:kubernetesVersion,sku:sku,agentPoolProfiles:agentPoolProfiles[].{name:name,count:count,vmSize:vmSize},networkProfile:networkProfile.networkPlugin,location:location}" -o json` | `aks.json` |
| `Microsoft.Web/sites` | `az webapp list -g "<RG>" --query "[].{name:name,kind:kind,sku:appServicePlan,state:state,defaultHostName:defaultHostName,httpsOnly:httpsOnly,location:location}" -o json` | `webapps.json` |
| `Microsoft.Web/serverFarms` | `az appservice plan list -g "<RG>" --query "[].{name:name,sku:sku.name,tier:sku.tier,kind:kind,location:location}" -o json` | `appservice-plans.json` |
| `Microsoft.DocumentDB/databaseAccounts` | `az cosmosdb list -g "<RG>" --query "[].{name:name,kind:kind,databaseAccountOfferType:databaseAccountOfferType,locations:locations[].locationName,publicAccess:publicNetworkAccess}" -o json` | `cosmosdb.json` |
| `Microsoft.Sql/servers` | `az sql server list -g "<RG>" --query "[].{name:name,fullyQualifiedDomainName:fullyQualifiedDomainName,publicAccess:publicNetworkAccess,location:location}" -o json` | `sql-servers.json` |
| `Microsoft.Databricks/workspaces` | `az databricks workspace list -g "<RG>" --query "[].{name:name,sku:sku.name,url:workspaceUrl,publicAccess:parameters.enableNoPublicIp.value,location:location}" -o json 2>$null` | `databricks.json` |
| `Microsoft.Synapse/workspaces` | `az synapse workspace list -g "<RG>" --query "[].{name:name,sqlAdminLogin:sqlAdministratorLogin,publicAccess:publicNetworkAccess,location:location}" -o json 2>$null` | `synapse.json` |
| `Microsoft.DataFactory/factories` | `az datafactory list -g "<RG>" --query "[].{name:name,publicAccess:publicNetworkAccess,location:location}" -o json 2>$null` | `adf.json` |
| `Microsoft.EventHub/namespaces` | `az eventhubs namespace list -g "<RG>" --query "[].{name:name,sku:sku.name,location:location}" -o json` | `eventhub.json` |
| `Microsoft.Cache/redis` | `az redis list -g "<RG>" --query "[].{name:name,sku:sku.name,port:port,sslPort:sslPort,publicAccess:publicNetworkAccess,location:location}" -o json` | `redis.json` |
| `Microsoft.ContainerRegistry/registries` | `az acr list -g "<RG>" --query "[].{name:name,sku:sku.name,adminUserEnabled:adminUserEnabled,publicAccess:publicNetworkAccess,location:location}" -o json` | `acr.json` |
| `Microsoft.MachineLearningServices/workspaces` | `az resource show --ids "<ID>" --query "{name:name,sku:sku,kind:kind,location:location,publicAccess:properties.publicNetworkAccess,hbiWorkspace:properties.hbiWorkspace,managedNetwork:properties.managedNetwork.isolationMode}" -o json` | `mlworkspace.json` |
| `Microsoft.Insights/components` | `az monitor app-insights component show -g "<RG>" --app "<NAME>" --query "{name:name,kind:kind,instrumentationKey:instrumentationKey,workspaceResourceId:workspaceResourceId,location:location}" -o json 2>$null` | `appinsights-<NAME>.json` |
| `Microsoft.OperationalInsights/workspaces` | `az monitor log-analytics workspace show -g "<RG>" -n "<NAME>" --query "{name:name,sku:sku.name,retentionInDays:retentionInDays,location:location}" -o json` | `log-analytics-<NAME>.json` |
| `Microsoft.Network/applicationGateways` | `az network application-gateway list -g "<RG>" --query "[].{name:name,sku:sku,location:location}" -o json` | `appgateway.json` |
| `Microsoft.Cdn/profiles` / `Microsoft.Network/frontDoors` | `az afd profile list -g "<RG>" --query "[].{name:name,sku:sku.name,location:location}" -o json 2>$null` | `frontdoor.json` |
| `Microsoft.Network/azureFirewalls` | `az network firewall list -g "<RG>" --query "[].{name:name,sku:sku,threatIntelMode:threatIntelMode,location:location}" -o json` | `firewall.json` |
| `Microsoft.Network/bastionHosts` | `az network bastion list -g "<RG>" --query "[].{name:name,sku:sku.name,location:location}" -o json` | `bastion.json` |

**Processo de consulta dinâmica:**

1. Leia `resources.json`
2. Extraia os valores distintos do campo `type`
3. Execute **somente os comandos dos tipos correspondentes** na tabela (ignore tipos ausentes)
4. Para um tipo ausente da tabela → use a consulta genérica: `az resource show --ids "<ID>" --query "{name:name,sku:sku,kind:kind,location:location,properties:properties}" -o json`
5. Execute comandos em lotes de dois ou três (não execute todos de uma vez)

### 2-C: consultar implantações de modelos (quando houver Cognitive Services)

```powershell
# Consulta as implantações de modelos de cada recurso Cognitive Services
az cognitiveservices account deployment list --name "<NAME>" -g "<RG>" --query "[].{name:name,model:properties.model.name,version:properties.model.version,sku:sku.name}" -o json | Set-Content "$outDir/<NAME>-deployments.json"
```

### 2-D: consultar NIC + IP público (quando houver VMs)

```powershell
az network nic list -g "<RG>" --query "[].{name:name,subnetId:ipConfigurations[0].subnet.id,privateIp:ipConfigurations[0].privateIPAddress,publicIpId:ipConfigurations[0].publicIPAddress.id}" -o json | Set-Content "$outDir/nics.json"
az network public-ip list -g "<RG>" --query "[].{name:name,ip:ipAddress,sku:sku.name}" -o json | Set-Content "$outDir/public-ips.json"
```

Da VNet:

- `addressSpace.addressPrefixes` → CIDR
- `subnets[].name`, `subnets[].addressPrefix` → informações da sub-rede
- `subnets[].privateEndpointNetworkPolicies` → políticas de PE

---

## Etapa 3: inferir relações entre recursos

Infira automaticamente **relações (conexões)** entre os recursos examinados para criar o JSON `connections`.

### Regras de inferência de relações

**🚨 Com poucas linhas de conexão, o diagrama perde o sentido. Infira o máximo possível de relações.**

#### Inferência confirmada (verificável diretamente por IDs/propriedades)

| Tipo de relação | Método de inferência | Tipo de conexão |
|---|---|---|
| PE → serviço | Extraia o ID do serviço de `privateLinkServiceId` do PE | `private` |
| PE → VNet | Extraia a VNet de `subnet.id` do PE | (Representada pelo limite da VNet) |
| Foundry → Project | Recurso pai de `accounts/projects` | `api` |
| VM → NIC → sub-rede | Infira VNet/sub-rede de `subnet.id` da NIC | (Limite da VNet) |
| NSG → sub-rede | Verifique as sub-redes conectadas em `subnets[].id` do NSG | `network` |
| NSG → NIC | Verifique as VMs conectadas em `networkInterfaces[].id` do NSG | `network` |
| NIC → IP público | Verifique o PIP em `publicIPAddress.id` da NIC | (Incluído em details) |
| Databricks → VNet | Configuração de injeção de VNet do Workspace | (Limite da VNet) |

#### Inferência razoável (padrões comuns entre serviços no mesmo RG)

| Tipo de relação | Condição de inferência | Tipo de conexão |
|---|---|---|
| Foundry → AI Search | Ambos no mesmo RG → infira conexão RAG | `api` (rótulo: "Pesquisa RAG") |
| Foundry → Storage | Ambos no mesmo RG → infira conexão de dados | `data` (rótulo: "Dados") |
| AI Search → Storage | Ambos no mesmo RG → infira conexão de indexação | `data` (rótulo: "Indexação") |
| Serviço → Key Vault | Key Vault no mesmo RG → infira gerenciamento de segredos | `security` (rótulo: "Segredos") |
| VM → Foundry/Search | VM + serviços de IA no mesmo RG → infira chamadas de API | `api` (rótulo: "API") |
| DI → Foundry | Document Intelligence + Foundry no mesmo RG → infira OCR/extração | `api` (rótulo: "OCR/Extração") |
| ADF → Storage | ADF + Storage no mesmo RG → infira fluxo de dados | `data` (rótulo: "Fluxo") |
| ADF → SQL | ADF + SQL no mesmo RG → infira fonte de dados | `data` (rótulo: "Fonte") |
| Databricks → Storage | Ambos no mesmo RG → infira conexão de lago de dados | `data` (rótulo: "Lago de dados") |

#### Confirmação após a inferência

Apresente a lista de conexões inferidas e solicite confirmação:

```
> **⏳ As relações entre os recursos foram inferidas**. Verifique se estão corretas.

Conexões inferidas:
- Foundry → AI Search (Pesquisa RAG)
- Foundry → Storage (Dados)
- VM → Foundry (Chamada de API)
- Document Intelligence → Foundry (OCR/Extração)

Está correto? Informe se quiser adicionar ou remover conexões.
```

#### Relações que não podem ser inferidas

Algumas conexões podem não ser inferidas por essas regras. Permita a adição livre de conexões.

### Consulta de implantações de modelos (quando houver recursos Foundry)

```powershell
az cognitiveservices account deployment list --name "<FOUNDRY_NAME>" -g "<RG>" --query "[].{name:name,model:properties.model.name,version:properties.model.version,sku:sku.name}" -o json
```

Adicione o nome, a versão e a SKU do modelo de cada implantação a `details` do nó Foundry.

---

## Etapa 4: conversão para JSON services/connections

Converta os resultados para o formato de entrada do mecanismo integrado.

### Mapeamento de tipo de recurso → tipo do diagrama

| Tipo de recurso do Azure | Tipo do diagrama |
|---|---|
| `Microsoft.CognitiveServices/accounts` (kind: AIServices) | `ai_foundry` |
| `Microsoft.CognitiveServices/accounts` (kind: OpenAI) | `openai` |
| `Microsoft.CognitiveServices/accounts` (kind: FormRecognizer) | `document_intelligence` |
| `Microsoft.CognitiveServices/accounts` (kind: TextAnalytics etc.) | `ai_foundry` (padrão) |
| `Microsoft.CognitiveServices/accounts/projects` | `ai_foundry` |
| `Microsoft.Search/searchServices` | `search` |
| `Microsoft.Storage/storageAccounts` | `storage` |
| `Microsoft.KeyVault/vaults` | `keyvault` |
| `Microsoft.Databricks/workspaces` | `databricks` |
| `Microsoft.Sql/servers` | `sql_server` |
| `Microsoft.Sql/servers/databases` | `sql_database` |
| `Microsoft.DocumentDB/databaseAccounts` | `cosmos_db` |
| `Microsoft.Web/sites` | `app_service` |
| `Microsoft.ContainerService/managedClusters` | `aks` |
| `Microsoft.Web/sites` (kind: functionapp) | `function_app` |
| `Microsoft.Synapse/workspaces` | `synapse` |
| `Microsoft.Fabric/capacities` | `fabric` |
| `Microsoft.DataFactory/factories` | `adf` |
| `Microsoft.Compute/virtualMachines` | `vm` |
| `Microsoft.Network/privateEndpoints` | `pe` |
| `Microsoft.Network/virtualNetworks` | (Representada pelo limite da VNet; não incluída em services) |
| `Microsoft.Network/networkSecurityGroups` | `nsg` |
| `Microsoft.Network/bastionHosts` | `bastion` |
| `Microsoft.OperationalInsights/workspaces` | `log_analytics` |
| `Microsoft.Insights/components` | `app_insights` |
| Outro | `default` |

### Regras de construção do JSON services

```json
{
  "id": "nome do recurso (minúsculas, sem caracteres especiais)",
  "name": "nome real do recurso",
  "type": "determinado pela tabela acima",
  "sku": "SKU real (se disponível)",
  "private": true/false,  // true se houver um PE conectado
  "details": ["propriedade1", "propriedade2", ...]
}
```

**Informações a incluir em details:**

- URL do ponto de extremidade
- Detalhes de SKU/camada
- kind (AIServices, OpenAI, etc.)
- Lista de implantações de modelos (Foundry)
- Principais propriedades (`isHnsEnabled`, `semanticSearch` etc.)
- Região

### Informações da VNet → parâmetro `--vnet-info`

Se uma VNet for encontrada, exiba-a no rótulo do limite por `--vnet-info`:

```
--vnet-info "10.0.0.0/16 | pe-subnet: 10.0.1.0/24 | <region>"
```

### Geração de nós de PE

Se houver PEs, adicione cada PE como nó separado e conecte-o ao serviço correspondente com o tipo `private`:

```json
{"id": "pe_<serviceId>", "name": "PE: <serviceName>", "type": "pe", "details": ["groupId: <groupId>", "<status>"]}
```

---

## Etapa 5: gerar e apresentar o diagrama

Nome do arquivo do diagrama: `<project-name>/00_arch_current.html`

Use o nome do RG examinado como nome padrão do projeto:

```
ask_user({
  question: "Escolha um nome de projeto. Ele será o nome da pasta dos resultados.",
  choices: ["<RG-name>", "azure-analysis"]
})
```

Após gerar o diagrama, apresente:

```
## Arquitetura atual do Azure

[Diagrama interativo: 00_arch_current.html]

Recursos examinados (N no total):
[Tabela de resumo por tipo]

O que você deseja alterar?
- 🔧 Melhorar o desempenho ("está lento", "aumentar a taxa de transferência")
- 💰 Otimizar custos ("reduzir custos", "baratear")
- 🔒 Reforçar a segurança ("adicionar PE", "bloquear acesso público")
- 🌐 Alterar a rede ("separar a VNet", "adicionar Bastion")
- ➕ Adicionar/remover recursos ("adicionar uma VM", "excluir isto")
- 📊 Monitorar ("configurar logs", "adicionar alertas")
- 🤔 Diagnosticar ("esta arquitetura está adequada?", "o que está errado?")
- Ou somente obter o diagrama e encerrar
```

---

## Etapa 6: conversar sobre modificações → transição para a Fase 1

Quando houver solicitação de modificações, siga para a Fase 1 (`phase1-advisor.md`).
Esse é o **ponto de entrada do Caminho B**, que usa os resultados existentes como linha de base.

### Tratamento de solicitações em linguagem natural: padrões de perguntas de esclarecimento

Faça perguntas para tornar solicitações vagas mais específicas:

**🔧 Desempenho**

| Solicitação | Exemplo de pergunta de esclarecimento |
|---|---|
| "Está lento" / "A resposta demora" | "Qual serviço está lento? Devemos aumentar a SKU ou mudar a região?" |
| "Quero aumentar a taxa de transferência" | "De qual serviço? Devemos escalar horizontalmente ou aumentar DTU/RU?" |
| "A indexação do AI Search está lenta" | "Devemos adicionar partições ou usar a SKU S2?" |

**💰 Custo**

| Solicitação | Exemplo de pergunta de esclarecimento |
|---|---|
| "Quero reduzir custos" | "De qual serviço? Devemos reduzir a SKU ou remover recursos sem uso?" |
| "Quanto custa?" | Consulte os preços no Microsoft Docs e estime com base nas SKUs atuais |
| "É um ambiente de desenvolvimento, deixe barato" | "Quais serviços devem mudar para as camadas Free/Basic?" |

**🔒 Segurança**

| Solicitação | Exemplo de pergunta de esclarecimento |
|---|---|
| "Reforce a segurança" | "Devemos adicionar PEs aos serviços sem PE, verificar RBAC e desabilitar publicNetworkAccess?" |
| "Bloqueie o acesso público" | "Devemos aplicar PE + publicNetworkAccess: Disabled a todos os serviços?" |
| "Gerencie as chaves" | "Devemos adicionar Key Vault e conectá-lo com identidade gerenciada (Managed Identity)?" |

**🌐 Rede**

| Solicitação | Exemplo de pergunta de esclarecimento |
|---|---|
| "Adicione PE" | "A qual serviço? Devemos adicionar a todos de uma vez?" |
| "Separe a VNet" | "Quais sub-redes devem ser separadas? Devemos adicionar NSGs?" |
| "Adicione Bastion" | "Para adicionar Azure Bastion ao acesso à VM, informe o CIDR da sub-rede." |

**➕ Adicionar/remover recursos**

| Solicitação | Exemplo de pergunta de esclarecimento |
|---|---|
| "Adicione uma VM" | "Quantas? Qual SKU? Na mesma VNet? Qual sistema operacional?" |
| "Adicione Fabric" | "Qual SKU? Qual é o e-mail do administrador?" |
| "Exclua isto" | "Confirma a remoção de [nome do recurso]? Os PEs conectados também serão removidos." |

**📊 Monitoramento/operações**

| Solicitação | Exemplo de pergunta de esclarecimento |
|---|---|
| "Quero ver os registros" | "Devemos adicionar um Log Analytics Workspace e conectar as configurações de diagnóstico (Diagnostic Settings)?" |
| "Configure alertas" | "Para quais métricas: CPU, taxa de erros ou tempo de resposta?" |
| "Anexe Application Insights" | "A qual serviço: App Service ou Function App?" |

**🔄 Migração/alterações**

| Solicitação | Exemplo de pergunta de esclarecimento |
|---|---|
| "Mude a região" | "Para qual região? Verificarei a disponibilidade de todos os serviços." |
| "Troque SQL por Cosmos" | "Qual tipo de API do Cosmos DB (SQL/MongoDB/Cassandra)? Também posso fornecer um guia de migração." |
| "Troque Foundry por Hub" | "O Hub é adequado quando é necessário treinar ML/modelos de código aberto. Vamos verificar o caso de uso." |

**🤔 Diagnóstico/perguntas**

| Solicitação | Exemplo de pergunta de esclarecimento |
|---|---|
| "O que está errado?" | Analise a configuração atual (`publicNetworkAccess` aberto, PE desconectado, SKU inadequada etc.) e sugira melhorias |
| "Esta arquitetura está adequada?" | Revise com a estrutura bem arquitetada (Well-Architected Framework): segurança, confiabilidade, desempenho, custo e operações |
| "O PE está conectado corretamente?" | Verifique com `az network private-endpoint show` e relate |
| "Quero somente o diagrama" | Não siga para a Fase 1; forneça o caminho de 00_arch_current.html e encerre |

Após finalizar as modificações:

1. Aplique a Regra de Confirmação das Alterações da Fase 1
2. Verifique os fatos (validação cruzada no Microsoft Docs)
3. Gere o diagrama atualizado (`01_arch_diagram_draft.html`)
4. Após a confirmação → siga para as Fases 2 a 4

---

## Otimização do desempenho do exame

- Se houver mais de 50 recursos, avise: "Há muitos recursos; o exame pode demorar."
- Execute primeiro `az resource list` para contar os recursos e depois faça as consultas detalhadas
- Consulte primeiro os principais serviços (Foundry, Search, Storage, Key Vault, VNet e PE); obtenha somente informações básicas dos demais com `az resource show`
- Informe o progresso:
  > **⏳ Examinando recursos**: M de N recursos concluídos

---

## Tratamento de recursos sem suporte

Para tipos ausentes do mapeamento do diagrama:

- Exiba com o tipo `default` (ícone de interrogação)
- Inclua o nome e o tipo do recurso em `details`
- Apresente o recurso, mas não tente inferir relações
