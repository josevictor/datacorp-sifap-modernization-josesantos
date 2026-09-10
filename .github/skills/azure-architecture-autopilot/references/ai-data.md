# Pacote de domínio: IA/dados (v1)

Guia de configuração de serviços especializado em cargas de trabalho de IA/dados do Azure.
Escopo da v1: Foundry, AI Search, ADLS Gen2, Key Vault, Fabric, ADF e VNet/PE.

> Propriedades obrigatórias e erros comuns → `service-gotchas.md`
> Informações dinâmicas (versão da API, SKU e região) → `azure-dynamic-sources.md`
> Padrões comuns (PE, segurança e nomenclatura) → `azure-common-patterns.md`

---

## 1. Microsoft Foundry (CognitiveServices)

### Hierarquia de recursos

```
Microsoft.CognitiveServices/accounts (kind: 'AIServices')
├── /projects          — Foundry Project (obrigatório para acessar o portal)
└── /deployments       — Implantações de modelos (GPT-4o, incorporação vetorial, `embedding`, etc.)
```

### Estrutura principal do Bicep: 1. Microsoft Foundry (CognitiveServices)

```bicep
// Recurso Foundry
resource foundry 'Microsoft.CognitiveServices/accounts@<fetch>' = {
  name: foundryName
  location: location
  kind: 'AIServices'
  sku: { name: '<confirm with user>' }               // ← SKU confirmada após consulta ao Microsoft Docs na Fase 1
  identity: { type: 'SystemAssigned' }
  properties: {
    customSubDomainName: foundryName  // ← Obrigatório e globalmente exclusivo. Não pode ser alterado após a criação; se ausente, exclua e recrie
    allowProjectManagement: true
    publicNetworkAccess: 'Disabled'
    networkAcls: { defaultAction: 'Deny' }
  }
}

// Foundry Project: deve ser criado em conjunto com o Foundry
resource project 'Microsoft.CognitiveServices/accounts/projects@<fetch>' = {
  parent: foundry
  name: '${foundryName}-project'
  location: location
  sku: { name: '<same as parent>' }
  kind: 'AIServices'
  identity: { type: 'SystemAssigned' }
  properties: {}
}

// Implantação de modelo: no nível do recurso Foundry
resource deployment 'Microsoft.CognitiveServices/accounts/deployments@<fetch>' = {
  parent: foundry
  name: '<model-name>'                              // ← Confirmado na Fase 1
  sku: {
    name: '<deployment-type>'                        // ← GlobalStandard, Standard etc.; consulte o Microsoft Docs
    capacity: <confirm with user>                    // ← Unidades de capacidade; verifique o intervalo no Microsoft Docs
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: '<model-name>'                           // ← É obrigatório verificar a disponibilidade
      version: '<fetch>'                             // ← Consulte também a versão
    }
  }
}
```

> `@<fetch>`: verifique a versão da API nas URLs de `azure-dynamic-sources.md`.
> Nome/versão do modelo, tipo de implantação e capacidade: todos são dinâmicos. Confirme-os após consultar o Microsoft Docs na Fase 1.

---

## 2. Azure AI Search

### Estrutura principal do Bicep: 2. Azure AI Search

```bicep
resource search 'Microsoft.Search/searchServices@<fetch>' = {
  name: searchName
  location: location
  sku: { name: '<confirm with user>' }
  identity: { type: 'SystemAssigned' }
  properties: {
    hostingMode: 'default'
    publicNetworkAccess: 'disabled'
    semanticSearch: '<confirm with user>'    // disabled | free | standard; verifique no Microsoft Docs
  }
}
```

### Observações de projeto: 2. Azure AI Search

- Suporte a PE: SKU Basic ou superior (verifique as restrições mais recentes no Microsoft Docs)
- Classificador semântico (Semantic Ranker): ativado pela propriedade `semanticSearch` (`disabled` | `free` | `standard`); verifique o suporte por SKU no Microsoft Docs
- Pesquisa vetorial: disponível nas SKUs pagas (verifique no Microsoft Docs)
- Geralmente usado com o Foundry em configurações RAG

---

## 3. ADLS Gen2 (Storage Account)

### Estrutura principal do Bicep: 3. ADLS Gen2 (Storage Account)

```bicep
resource storage 'Microsoft.Storage/storageAccounts@<fetch>' = {
  name: storageName        // Somente letras minúsculas e números, sem hifens
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    isHnsEnabled: true                 // ← Nunca omita esta propriedade
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: 'Disabled'
    networkAcls: { defaultAction: 'Deny' }
  }
}

// Contêiner
resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@<fetch>' = {
  name: '${storage.name}/default/raw'
}
```

### Observações de projeto: 3. ADLS Gen2 (Storage Account)

- `isHnsEnabled` não pode ser alterado após a criação → recrie o recurso se a propriedade tiver sido omitida
- PE: o caso de uso pode exigir PEs `blob` e `dfs`
- Contêineres comuns: `raw`, `processed`, `curated`

---

## 4. Microsoft Fabric

### Estrutura principal do Bicep: 4. Microsoft Fabric

```bicep
resource fabric 'Microsoft.Fabric/capacities@<fetch>' = {
  name: fabricName
  location: location
  sku: { name: '<confirm with user>', tier: 'Fabric' }
  properties: {
    administration: {
      members: [ '<admin-email>' ]    // ← Obrigatório; sem este valor, a implantação falha
    }
  }
}
```

### Observações de projeto: 4. Microsoft Fabric

- Somente Capacity (capacidade) pode ser provisionado pelo Bicep
- Workspace (espaço de trabalho), Lakehouse (repositório analítico unificado), Warehouse (armazém de dados) etc. devem ser criados manualmente no portal
- Confirme o e-mail do administrador com `ask_user`

### Itens de confirmação obrigatória ao adicionar na Fase 1

Quando o Fabric for adicionado durante a conversa, confirme os itens abaixo por `ask_user` antes de atualizar o diagrama:

- [ ] **SKU/Capacity**: F2, F4, F8...; ofereça opções após consultar as SKUs disponíveis no Microsoft Docs
- [ ] **administration.members**: e-mail do administrador; sem ele, a implantação falha

> Não inclua arbitrariamente subcargas de trabalho (OneLake, fluxos de dados, Warehouse etc.) que não tenham sido especificadas. Somente Capacity pode ser provisionado pelo Bicep.

---

## 5. Azure Data Factory

### Estrutura principal do Bicep: 5. Azure Data Factory

```bicep
resource adf 'Microsoft.DataFactory/factories@<fetch>' = {
  name: adfName
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    publicNetworkAccess: 'Disabled'
  }
}
```

### Observações de projeto: 5. Azure Data Factory

- O ambiente de execução de integração auto-hospedado (Self-hosted Integration Runtime) exige configuração manual fora do Bicep
- Usado principalmente em cenários de ingestão de dados locais
- `groupId` do PE: `dataFactory`

---

## 6. AML / AI Hub (MachineLearningServices)

### Quando usar

```
Regra de decisão:
├─ IA/RAG em geral → use Foundry (AIServices)
└─ Treinamento de ML ou modelos de código aberto necessários → considere AI Hub
    └─ Somente mediante solicitação explícita
```

### Estrutura principal do Bicep: 6. AML / AI Hub (MachineLearningServices)

```bicep
resource hub 'Microsoft.MachineLearningServices/workspaces@<fetch>' = {
  name: hubName
  location: location
  kind: 'Hub'
  sku: { name: '<confirm with user>', tier: '<confirm with user>' }  // por exemplo, Basic/Basic; verifique as SKUs no Microsoft Docs
  identity: { type: 'SystemAssigned' }
  properties: {
    friendlyName: hubName
    storageAccount: storage.id
    keyVault: keyVault.id
    applicationInsights: appInsights.id    // Obrigatório para o Hub
    publicNetworkAccess: 'Disabled'
  }
}
```

### Dependências do AI Hub

Recursos adicionais necessários ao usar o Hub:

- Storage Account
- Key Vault
- Application Insights + Log Analytics Workspace
- Container Registry (opcional)

---

## 7. Combinações comuns de arquitetura de IA/dados

### Assistente de conversa RAG

```
Foundry (AIServices) + Project
├── <chat-model> (bate-papo)              — Confirmado após verificar a disponibilidade na Fase 1
├── <embedding-model> (incorporação vetorial) — Confirmado após verificar a disponibilidade na Fase 1
├── AI Search (vetorial + semântica)
├── ADLS Gen2 (armazenamento de documentos)
└── Key Vault (segredos)
+ Configuração completa de VNet/PE
```

### Plataforma de dados

```
Fabric Capacity (análise)
├── ADLS Gen2 (lago de dados)
├── ADF (ingestão)
└── Key Vault (segredos)
+ Configuração de VNet/PE
```
