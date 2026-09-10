# Agente gerador de Bicep

Recebe a especificação final da arquitetura na Fase 1 e gera modelos Bicep implantáveis.

## Etapa 0: verificar as especificações mais recentes (obrigatório antes de gerar Bicep)

Não fixe versões da API no código Bicep.
Sempre consulte a referência do Bicep no Microsoft Docs e confirme a `apiVersion` estável mais recente antes de usá-la.

### Etapas de verificação

1. Identifique a lista de serviços
2. Consulte a URL de cada serviço no Microsoft Docs com `web_fetch`
3. Confirme a versão estável mais recente da API
4. Escreva o Bicep com essa versão

### Verificação da disponibilidade de implantação do modelo (obrigatória para modelos Foundry/OpenAI)

Verifique se o modelo informado pode ser implantado na região de destino **antes de gerar Bicep**.
A disponibilidade varia por região e muda com frequência. Não dependa de conhecimento estático.

**Métodos de verificação (em ordem de prioridade):**

1. Consulte a disponibilidade no Microsoft Docs: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
2. Ou consulte diretamente pela CLI do Azure:

   ```powershell
   az cognitiveservices account list-models --name "<FOUNDRY_NAME>" --resource-group "<RG_NAME>" -o table
   ```

   (Quando o recurso Foundry já existir)

**Se o modelo não estiver disponível na região de destino:**

- Informe e sugira regiões disponíveis ou modelos alternativos
- Não substitua o modelo nem a região sem aprovação

### URLs do Microsoft Docs por serviço

O registro completo de URLs está em `references/azure-dynamic-sources.md`. Consulte-o ao pesquisar.
Os arquivos de referência ficam em `.github/skills/azure-architecture-autopilot/`.

> **Importante**: consulte a URL diretamente com `web_fetch` para confirmar a `apiVersion` estável mais recente. Não use sem verificação versões fixas de referências ou conversas anteriores.

> **Sempre verifique também os recursos filhos**: consulte as versões da API de recursos filhos (`accounts/projects`, `accounts/deployments`, `privateDnsZones/virtualNetworkLinks`, `privateEndpoints/privateDnsZoneGroups` etc.) na página do pai. As versões podem ser diferentes.

> **O mesmo princípio vale para erros/avisos**: se ocorrer um erro de versão da API na análise de alterações (`what-if`) ou na implantação, não trate a versão da mensagem como a mais recente. Consulte novamente o Microsoft Docs antes de corrigir.

---

## Princípios para consultar informações (estáveis versus dinâmicas)

### Sempre consultar (dinâmicas)

- Versão da API → consulte as URLs em `azure-dynamic-sources.md`
- Disponibilidade do modelo (nome, versão e região) → consulte
- Lista de SKUs/preços → consulte
- Disponibilidade regional → consulte

### Consultar primeiro as referências (estáveis)

- Padrões de propriedades obrigatórias (`isHnsEnabled`, `allowProjectManagement` etc.) → `service-gotchas.md`
- Mapeamentos de `groupId` de PE e DNS Zone (principais serviços) → `service-gotchas.md`
- Padrões comuns de PE, segurança e nomenclatura → `azure-common-patterns.md`
- Guia de configuração de serviços de IA/dados → `ai-data.md`

> Em caso de dúvida sobre uma informação estável, confirme-a novamente no Microsoft Docs. Não é necessário consultar todas as vezes.

---

## Fluxo de contingência para serviço desconhecido

Quando a solicitação incluir um serviço fora do escopo da v1 (`ai-data.md`):

1. **Informe**: "Este serviço está fora do escopo padrão da v1. Ele será gerado por melhor esforço com base no Microsoft Docs."
2. **Consulte a versão da API**: monte a URL no formato `https://learn.microsoft.com/en-us/azure/templates/microsoft.{provider}/{resourceType}` e consulte-a
3. **Identifique o tipo e as propriedades obrigatórias**: confirme-os na documentação consultada
4. **Verifique o mapeamento de PE**: consulte `https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns` para confirmar `groupId`/DNS Zone
5. **Aplique os padrões comuns**: use os padrões de segurança, rede e nomenclatura de `azure-common-patterns.md`
6. **Escreva o Bicep**: gere o módulo com base nas informações acima
7. **Encaminhe ao revisor**: valide a compilação com `az bicep build`

## Informações de entrada

As informações abaixo devem estar finalizadas ao concluir a Fase 1:

```
- services: [Lista de serviços + SKU]
- networking: Se private_endpoint é usado
- resource_group: Nome do grupo de recursos
- location: Local da implantação (confirmado na Fase 1)
- subscription_id: ID da assinatura do Azure
```

## Estrutura dos arquivos de saída

```
<project-name>/
├── main.bicep              # Orquestração principal: chamadas de módulos e passagem de parâmetros
├── main.bicepparam         # Arquivo de parâmetros: valores do ambiente, sem informações confidenciais
└── modules/
    ├── network.bicep           # VNet, Subnet (inclui pe-subnet)
    ├── ai.bicep                # Serviços de IA (configurados conforme os requisitos)
    ├── storage.bicep           # ADLS Gen2 (isHnsEnabled: true obrigatório)
    ├── fabric.bicep            # Microsoft Fabric Capacity (somente quando necessário)
    ├── keyvault.bicep          # Key Vault
    ├── monitoring.bicep        # Application Insights, Log Analytics (somente em configurações baseadas em Hub)
    └── private-endpoints.bicep # Todos os PEs + Private DNS Zones + VNet Links + DNS Zone Groups
```

## Responsabilidades dos módulos

### `network.bicep`

- VNet: recebe o CIDR como parâmetro para evitar conflitos com espaços de endereços existentes
- pe-subnet: exige `privateEndpointNetworkPolicies: 'Disabled'`
- Sub-redes adicionais: tratadas por parâmetros conforme necessário

### `ai.bicep`

- **Recurso Microsoft Foundry** (`Microsoft.CognitiveServices/accounts`, `kind: 'AIServices'`): recurso de IA de nível superior
  - `customSubDomainName: foundryName` obrigatório. **Não pode ser alterado após a criação. Se omitido, exclua e recrie o recurso**
  - `identity: { type: 'SystemAssigned' }` obrigatório
  - `allowProjectManagement: true` obrigatório
  - Implantação de modelo (`Microsoft.CognitiveServices/accounts/deployments`): feita no nível do recurso Foundry
- **⚠️ Foundry Project** (`Microsoft.CognitiveServices/accounts/projects`): **deve ser criado como recurso filho**
  - Tipo de recurso: `Microsoft.CognitiveServices/accounts/projects` (nunca crie como recurso `accounts` autônomo)
  - Use `parent: foundryAccount` no Bicep
  - Exemplo incorreto: criar um Project como conta `kind: 'AIServices'` separada → o portal não o reconhece
  - Exemplo correto:

    ```bicep
    resource foundryProject 'Microsoft.CognitiveServices/accounts/projects@<apiVersion>' = {
      parent: foundryAccount
      name: 'project-${uniqueString(resourceGroup().id)}'
      location: location
      kind: 'AIServices'
      properties: {}
    }
    ```

- **Azure AI Search**: configuração de classificação semântica (Semantic Ranking) e pesquisa vetorial
- Considere a opção baseada em Hub (`Microsoft.MachineLearningServices/workspaces`) somente mediante solicitação explícita ou necessidade de treinamento de ML/modelos de código aberto. Para cargas comuns de IA/RAG, Foundry (AIServices) é a opção padrão

**⛔ Propriedades proibidas de CognitiveServices:**

- `apiProperties.statisticsEnabled`: essa propriedade não existe. Nunca a use. Ela causa o erro `ApiPropertiesInvalid` na implantação
- `apiProperties.qnaAzureSearchEndpointId`: exclusiva do QnA Maker. Não use com Foundry
- Não adicione arbitrariamente propriedades não validadas a `properties.apiProperties`

### `storage.bicep`

- ADLS Gen2: `isHnsEnabled: true` ← **nunca omita esta propriedade**
- Contêineres: raw, processed, curated (ou conforme os requisitos)
- `allowBlobPublicAccess: false`, `minimumTlsVersion: 'TLS1_2'`

### `keyvault.bicep`

- `enableRbacAuthorization: true` (não use o modelo de política de acesso, Access Policy)
- `enableSoftDelete: true`, `softDeleteRetentionInDays: 90`
- `enablePurgeProtection: true`

### `monitoring.bicep`

- Log Analytics Workspace
- Application Insights (necessário somente para configurações baseadas em Hub; não é obrigatório para Foundry AIServices)

### `private-endpoints.bicep`

- Conjunto de três componentes para cada serviço:
  1. `Microsoft.Network/privateEndpoints` (colocado em pe-subnet)
  2. `Microsoft.Network/privateDnsZones` + VNet Link (`registrationEnabled: false`)
  3. `Microsoft.Network/privateEndpoints/privateDnsZoneGroups`
- Para os mapeamentos de DNS Zone de cada serviço, consulte `references/service-gotchas.md`

**⚠️ Regras de DNS de PE para Foundry/AIServices:**

- `groupId` do PE: `account`
- O DNS Zone Group deve incluir **duas zonas**:
  1. `privatelink.cognitiveservices.azure.com`
  2. `privatelink.openai.azure.com`
- Incluir somente uma causa falha de resolução de DNS nas chamadas à API OpenAI → erro de conexão

**⚠️ Regras de PE para ADLS Gen2 (`isHnsEnabled: true`):**

- Dois PEs obrigatórios:
  1. `blob` → `privatelink.blob.core.windows.net`
  2. `dfs` → `privatelink.dfs.core.windows.net`
- Sem o PE DFS, as operações do lago de dados (Data Lake), como criação de sistema de arquivos e manipulação de diretórios, falham

### `rbac.bicep` (ou incorporado a main.bicep)

**⚠️ Atribuição de função RBAC: nunca omita**

**Todo serviço com identidade gerenciada (Managed Identity, `identity.type: 'SystemAssigned'`) deve ter atribuições de função RBAC.**
Uma identidade sem funções atribuídas causa falhas de autenticação entre serviços.
Isso não é opcional. É um **item obrigatório**.
A revisão da Fase 3 relatará a omissão como CRÍTICA.

- Mapeamentos RBAC obrigatórios:

| Serviço de origem | Serviço de destino | Função | ID da definição da função |
|------------|-----------|------|-------------------|
| Foundry | Storage | `Storage Blob Data Contributor` | `ba92f5b4-2d11-453d-a403-e96b0029c9fe` |
| Foundry | AI Search | `Search Index Data Contributor` | `8ebe5a00-799e-43f5-93ac-243d3dce84a7` |
| Foundry | AI Search | `Search Service Contributor` | `7ca78c08-252a-4471-8644-bb5ff32d4ba0` |
| App Service | Key Vault | `Key Vault Secrets User` | `4633458b-17de-408a-b874-0445c86b69e6` |
| AKS (kubeletIdentity) | ACR | `AcrPull` | `7f951dda-4ed3-4680-a7ca-43fe172d538d` |
| Data Factory | Storage | `Storage Blob Data Contributor` | `ba92f5b4-2d11-453d-a403-e96b0029c9fe` |
| Data Factory | Key Vault | `Key Vault Secrets User` | `4633458b-17de-408a-b874-0445c86b69e6` |
| Databricks | Storage | `Storage Blob Data Contributor` | `ba92f5b4-2d11-453d-a403-e96b0029c9fe` |

> **Regra especial do AKS**: o AKS usa `identityProfile.kubeletidentity.objectId`, não `identity.principalId`.

```bicep
// Exemplo de RBAC: Foundry → Storage Blob Data Contributor
resource foundryStorageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, foundry.id, 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
    principalId: foundry.identity.principalId
    principalType: 'ServicePrincipal'
  }
}
```

### Regras do SQL Server

- **Gerenciamento de senha**: declare `@secure() param sqlAdminPassword string` em main.bicep e passe-o aos módulos
  - Não gere com `newGuid()` dentro dos módulos, pois a senha muda na reimplantação
  - Armazene como segredo do Key Vault para recuperá-la após a implantação
- **Método de autenticação**: use `administrators.azureADOnlyAuthentication: true` por padrão
  - Muitas políticas organizacionais (MCAPS etc.) bloqueiam autenticação SQL autônoma
  - Autenticação somente por AAD + identidade gerenciada (Managed Identity) é a configuração mais segura

### Tratamento de segredos de rede

- **Chave compartilhada do VPN Gateway**: `@secure() param vpnSharedKey string`; `@secure()` é obrigatório
- Nunca inclua chaves VPN em texto não criptografado em `.bicepparam`; forneça-as na implantação ou use uma referência do Key Vault
- A mesma regra se aplica às senhas SQL
- **Aplicável a**: chave compartilhada de VPN, chave de autorização do ExpressRoute, PSK de Wi-Fi e todos os outros segredos de rede
- Os parâmetros dos módulos também devem incluir o decorador `@secure()`

### ⚠️ Regras de consistência do isolamento de rede

- Ao definir `publicNetworkAccess: 'Disabled'`, você **também deve** criar o PE correspondente do serviço
- Definir publicNetworkAccess como Disabled sem PE deixa o serviço inacessível → inutilizável após a implantação
- O revisor da Fase 3 deve relatar essa inconsistência como **CRÍTICA**
- Ao encontrar a inconsistência, adicione um módulo de PE ou reverta publicNetworkAccess para Enabled

## Princípios obrigatórios de codificação

### Convenções de nomenclatura

```bicep
// Usa uniqueString para evitar colisões de nomes: sempre obrigatório
param foundryName string = 'foundry-${uniqueString(resourceGroup().id)}'
param searchName string = 'srch-${uniqueString(resourceGroup().id)}'
param storageName string = 'st${uniqueString(resourceGroup().id)}'  // Caracteres especiais não são permitidos
param keyVaultName string = 'kv-${uniqueString(resourceGroup().id)}'
```

> **⚠️ Recursos que exigem `customSubDomainName` (Foundry, Cognitive Services etc.) devem incluir `uniqueString()`.**
> Cadeias de texto estáticas (strings), por exemplo `'my-rag-chatbot'`, podem estar em uso por outro locatário e causar falhas.
> O mesmo vale para nomes do Foundry Project: `'project-${uniqueString(resourceGroup().id)}'`

### Isolamento de rede

```bicep
// Obrigatório para todos os serviços ao usar Private Endpoints
publicNetworkAccess: 'Disabled'
networkAcls: {
  defaultAction: 'Deny'
  ipRules: []
  virtualNetworkRules: []
}
```

### Gerenciamento de dependências

```bicep
// Usa dependências implícitas por referências de recursos em vez de dependsOn explícito
resource aiProject '...' = {
  properties: {
    hubResourceId: aiHub.id  // Referência a aiHub → aiHub é implantado primeiro automaticamente
  }
}
```

### Segurança

```bicep
// Usa referências do Key Vault para valores confidenciais; nunca armazena texto não criptografado nos parâmetros
@secure()
param adminPassword string  // Não insira valores em texto não criptografado em main.bicepparam
```

### Comentários do código

```bicep
// Recurso Microsoft Foundry: kind: 'AIServices'
// customSubDomainName: obrigatório e globalmente exclusivo. Não pode ser alterado após a criação; se omitido, exclua e recrie o recurso
// allowProjectManagement: true é obrigatório; sem ele, a criação do Foundry Project falha
// Substitua apiVersion pela versão mais recente consultada na Etapa 0
resource foundry 'Microsoft.CognitiveServices/accounts@<version fetched in Step 0>' = {
  kind: 'AIServices'
  properties: {
    customSubDomainName: foundryName
    allowProjectManagement: true
    ...
  }
}
```

### ⚠️ Validação da qualidade do código Bicep (obrigatória após a geração)

**Validação da declaração de módulos:**

- Verifique se a propriedade `name:` não está duplicada em cada bloco de módulo
- Exemplo correto: `name: 'deploy-sql'`
- Exemplo incorreto: `name: 'name: 'deploy-sql'` (`name:` duplicado → erro de compilação)

**Prevenção de propriedades duplicadas:**

- Repetir o nome de uma propriedade no mesmo bloco de recurso causa erro de compilação
- Isso é comum em recursos complexos como VPN Gateway (`gatewayType`), Firewall, AKS etc.
- Procure `BCP025: The property "xxx" is declared multiple times` na saída de `az bicep build`

**`az bicep build` deve ser executado:**

- Após gerar todos os arquivos Bicep, sempre execute `az bicep build --file main.bicep`
- Corrija os erros e compile novamente
- Avisos (`WARNING`, como BCP081) podem ser ignorados após verificar a versão da API no Microsoft Docs

## Estrutura básica de main.bicep

```bicep
// ============================================================
// Infraestrutura do Azure para [Nome do projeto]: main.bicep
// Gerado em: [Data]
// ============================================================

targetScope = 'resourceGroup'

// ── Parâmetros comuns ─────────────────────────────────────
param location string   // Local confirmado na Fase 1; não fixe o valor
param projectPrefix string
param vnetAddressPrefix string    // ← Confirme. Evita conflitos com redes existentes
param peSubnetPrefix string       // ← CIDR da sub-rede dedicada a PE dentro da VNet

// ── Rede ──────────────────────────────────────────────────
module network './modules/network.bicep' = {
  name: 'deploy-network'
  params: {
    location: location
    vnetAddressPrefix: vnetAddressPrefix
    peSubnetPrefix: peSubnetPrefix
  }
}

// ── Serviços de IA/dados ──────────────────────────────────
module ai './modules/ai.bicep' = {
  name: 'deploy-ai'
  params: {
    location: location
    // Adicione parâmetros separados se as regiões variarem por serviço; verifique-as no Microsoft Docs
  }
  dependsOn: [network]
}

// ── Armazenamento ─────────────────────────────────────────
module storage './modules/storage.bicep' = {
  name: 'deploy-storage'
  params: {
    location: location
  }
}

// ── Key Vault ─────────────────────────────────────────────
module keyVault './modules/keyvault.bicep' = {
  name: 'deploy-keyvault'
  params: {
    location: location
  }
}

// ── Private Endpoints (todos os serviços) ─────────────────
module privateEndpoints './modules/private-endpoints.bicep' = {
  name: 'deploy-private-endpoints'
  params: {
    location: location
    vnetId: network.outputs.vnetId
    peSubnetId: network.outputs.peSubnetId
    foundryId: ai.outputs.foundryId
    searchId: ai.outputs.searchId
    storageId: storage.outputs.storageId
    keyVaultId: keyVault.outputs.keyVaultId
  }
}

// ── Saídas ────────────────────────────────────────────────
output vnetId string = network.outputs.vnetId
output foundryEndpoint string = ai.outputs.foundryEndpoint
output searchEndpoint string = ai.outputs.searchEndpoint
```

## Estrutura básica de main.bicepparam

```bicep
using './main.bicep'

param location = '<Location confirmed in Phase 1>'
param projectPrefix = '<Project prefix>'
// Não insira valores confidenciais aqui; use referências do Key Vault
// Defina as regiões após verificar a disponibilidade de cada serviço no Microsoft Docs
```

### Tratamento de parâmetros @secure()

Quando um arquivo `.bicepparam` contém a diretiva `using`, não é possível usar opções `--parameters` adicionais com `az deployment`.
Por isso, os parâmetros `@secure()` devem seguir estas regras:

- **Defina um valor padrão quando possível**: `@secure() param password string = newGuid()`
- **Se parâmetros @secure() exigirem entrada**: gere também um arquivo JSON de parâmetros (`main.parameters.json`) em vez de usar `.bicepparam`
- **Nunca faça isto**: gerar um comando que use `.bicepparam` e `--parameters key=value` simultaneamente

## Lista de verificação de erros comuns

A lista completa está em `references/service-gotchas.md`. Resumo:

| Item | ❌ Incorreto | ✅ Correto |
|------|--------|----------|
| ADLS Gen2 | `isHnsEnabled` ausente | `isHnsEnabled: true` |
| Sub-rede de PE | Política não configurada | `privateEndpointNetworkPolicies: 'Disabled'` |
| Configuração de PE | Somente o PE foi criado | PE + DNS Zone + VNet Link + DNS Zone Group |
| Foundry | `kind: 'OpenAI'` | `kind: 'AIServices'` + `allowProjectManagement: true` |
| Foundry | `customSubDomainName` ausente | `customSubDomainName: foundryName`; não pode ser alterado após a criação |
| Foundry Project | Não criado | Sempre deve ser criado em conjunto com o recurso Foundry |
| Uso do Hub | Usado para IA comum | Somente mediante solicitação explícita ou necessidade de ML/modelos de código aberto |
| Rede pública | Não configurada | `publicNetworkAccess: 'Disabled'` |
| Nome do Storage | Contém hifens | Somente minúsculas + dígitos; recomenda-se `uniqueString()` |
| Versão da API | Copiada de valor anterior | Consulte o Microsoft Docs (dinâmica) |
| Região | Valor fixo | Parâmetro + verificação no Microsoft Docs (dinâmica) |

## Após concluir a geração

Ao concluir a geração do Bicep:

1. Apresente um resumo dos arquivos gerados e da função de cada um
2. Passe imediatamente para a Fase 3 (revisor de Bicep)
3. O revisor faz a revisão e as correções automáticas conforme `references/bicep-reviewer.md`
