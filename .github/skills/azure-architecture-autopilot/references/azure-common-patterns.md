# Padrões comuns do Azure (estáveis)

Este arquivo contém somente **padrões quase imutáveis** recorrentes nos serviços do Azure.
Informações dinâmicas, como versão da API, SKU e região, não aparecem aqui → consulte `azure-dynamic-sources.md`.

---

## 1. Padrões de isolamento de rede

### Conjunto de três componentes do endpoint privado (Private Endpoint)

Todos os serviços que usam PE devem ter estes três componentes configurados:

1. **Private Endpoint**: colocado em pe-subnet
2. **Private DNS Zone** + **VNet Link** (`registrationEnabled: false`)
3. **DNS Zone Group**: vinculado ao PE

> Se qualquer componente estiver ausente, a resolução de DNS falhará mesmo com o PE presente, o que impedirá a conexão.

### Configurações obrigatórias da sub-rede de PE

```bicep
resource peSubnet 'Microsoft.Network/virtualNetworks/subnets' = {
  properties: {
    addressPrefix: peSubnetPrefix              // ← CIDR como parâmetro para evitar conflitos com redes existentes
    privateEndpointNetworkPolicies: 'Disabled'  // ← Obrigatório. A implantação do PE falha sem esta configuração
  }
}
```

### Padrão de publicNetworkAccess

Os serviços que usam PE devem incluir:

```bicep
properties: {
  publicNetworkAccess: 'Disabled'
  networkAcls: {
    defaultAction: 'Deny'
  }
}
```

---

## 2. Padrões de segurança

### Key Vault

```bicep
properties: {
  enableRbacAuthorization: true    // Não use o método de política de acesso (Access Policy)
  enableSoftDelete: true
  softDeleteRetentionInDays: 90
  enablePurgeProtection: true
}
```

### Identidade gerenciada (Managed Identity)

Quando serviços de IA acessarem outros recursos:

```bicep
identity: {
  type: 'SystemAssigned'  // ou 'UserAssigned'
}
```

### Informações confidenciais

- Use o decorador `@secure()`
- Não armazene texto não criptografado em arquivos `.bicepparam`
- Use referências do Key Vault

---

## 3. Convenções de nomenclatura (baseadas no CAF)

```
rg-{project}-{env}          Grupo de recursos (Resource Group)
vnet-{project}-{env}        Virtual Network
st{project}{env}             Storage Account (sem caracteres especiais; somente letras minúsculas e números)
kv-{project}-{env}           Key Vault
srch-{project}-{env}         AI Search
foundry-{project}-{env}      Cognitive Services (Foundry)
```

> Prevenção de colisões de nomes: recomenda-se usar `uniqueString(resourceGroup().id)`
>
> ```bicep
> param storageName string = 'st${uniqueString(resourceGroup().id)}'
> ```

---

## 4. Estrutura dos módulos Bicep

```
<project>/
├── main.bicep              # Orquestração: chamadas de módulos + passagem de parâmetros
├── main.bicepparam         # Valores específicos do ambiente (sem informações confidenciais)
└── modules/
    ├── network.bicep           # VNet, sub-rede
    ├── <service>.bicep         # Módulos por serviço
    ├── keyvault.bicep          # Key Vault
    └── private-endpoints.bicep # Todos os PEs + DNS Zone + VNet Link
```

### Gerenciamento de dependências

```bicep
// ✅ Correto: dependência implícita por referência de recurso
resource project '...' = {
  properties: {
    parentId: foundry.id  // referência a foundry → implanta foundry primeiro automaticamente
  }
}

// ❌ Evite: dependsOn explícito (use somente quando necessário)
```

---

## 5. Modelo Bicep comum de PE

```bicep
// ── Private Endpoint ──
resource pe 'Microsoft.Network/privateEndpoints@<fetch>' = {
  name: 'pe-${serviceName}'
  location: location
  properties: {
    subnet: { id: peSubnetId }
    privateLinkServiceConnections: [{
      name: 'pls-${serviceName}'
      properties: {
        privateLinkServiceId: serviceId
        groupIds: ['<groupId>']  // ← Varia conforme o serviço. Consulte service-gotchas.md
      }
    }]
  }
}

// ── Private DNS Zone ──
resource dnsZone 'Microsoft.Network/privateDnsZones@<fetch>' = {
  name: '<dnsZoneName>'  // ← Varia conforme o serviço
  location: 'global'
}

// ── VNet Link ──
resource vnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@<fetch>' = {
  parent: dnsZone
  name: '${dnsZone.name}-link'
  location: 'global'
  properties: {
    virtualNetwork: { id: vnetId }
    registrationEnabled: false  // ← Deve ser false
  }
}

// ── DNS Zone Group ──
resource dnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@<fetch>' = {
  parent: pe
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [{
      name: 'config'
      properties: { privateDnsZoneId: dnsZone.id }
    }]
  }
}
```

> `@<fetch>`: sempre verifique a versão estável mais recente da API no Microsoft Docs antes da implantação.
