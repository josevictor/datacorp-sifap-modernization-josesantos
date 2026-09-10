# Armadilhas dos serviços (estáveis)

Resumo por serviço das **propriedades obrigatórias pouco intuitivas**, dos **erros comuns** e dos **mapeamentos de PE**.
Somente padrões quase imutáveis aparecem aqui. Valores dinâmicos, como versão da API, listas de SKUs e região, não estão incluídos.

---

## 1. Propriedades obrigatórias (a ausência causa falha na implantação ou problemas funcionais)

| Serviço | Propriedade obrigatória | Resultado da ausência | Observações |
|---------|------------------|-------------------|-------|
| ADLS Gen2 | `isHnsEnabled: true` | Torna-se Blob Storage comum. Não é reversível | Exige `kind: 'StorageV2'` |
| Storage Account | Nome sem caracteres especiais nem hifens | Falha na implantação | Somente letras minúsculas e números, de 3 a 24 caracteres |
| Foundry (AIServices) | `customSubDomainName: foundryName` | Não é possível criar o Project nem alterar após a criação → exclua e recrie o recurso | Valor globalmente exclusivo |
| Foundry (AIServices) | `allowProjectManagement: true` | Não é possível criar o Foundry Project | `kind: 'AIServices'` |
| Foundry (AIServices) | `identity: { type: 'SystemAssigned' }` | Falha na criação do Project | |
| Foundry Project | Deve ser criado em conjunto com o recurso Foundry | Não pode ser usado pelo portal | `accounts/projects` |
| Key Vault | `enableRbacAuthorization: true` | Risco de uso misto de política de acesso (Access Policy) | |
| Key Vault | `enablePurgeProtection: true` | Obrigatório em produção | |
| Fabric Capacity | `administration.members` obrigatório | Falha na implantação | E-mail do administrador |
| Sub-rede de PE | `privateEndpointNetworkPolicies: 'Disabled'` | Falha na implantação do PE | |
| DNS Zone de PE | `registrationEnabled: false` (VNet Link) | Possível conflito de DNS | |
| Configuração de PE | Conjunto de três componentes (PE + DNS Zone + VNet Link + Zone Group) | A resolução de DNS falha mesmo com o PE presente | |

---

## 2. Mapeamento de `groupId` de endpoint privado (PE) e DNS Zone (principais serviços)

Os mapeamentos abaixo são estáveis, mas confirme-os novamente no documento de integração de DNS de PE indicado em `azure-dynamic-sources.md` ao adicionar novos serviços.

| Serviço | groupId | Private DNS Zone |
|---------|---------|-----------------|
| Azure OpenAI / CognitiveServices | `account` | `privatelink.cognitiveservices.azure.com` |
| ⚠️ (adicional para Foundry/AIServices) | `account` | `privatelink.openai.azure.com` ← **As duas zonas devem estar no DNS Zone Group. Sem esta zona, a resolução de DNS da API OpenAI falha** |
| Azure AI Search | `searchService` | `privatelink.search.windows.net` |
| Storage (Blob/ADLS) | `blob` | `privatelink.blob.core.windows.net` |
| Storage (DFS/ADLS Gen2) | `dfs` | `privatelink.dfs.core.windows.net` |
| Key Vault | `vault` | `privatelink.vaultcore.azure.net` |
| Azure ML / AI Hub | `amlworkspace` | `privatelink.api.azureml.ms` |
| Container Registry | `registry` | `privatelink.azurecr.io` |
| Cosmos DB (SQL) | `Sql` | `privatelink.documents.azure.com` |
| Azure Cache for Redis | `redisCache` | `privatelink.redis.cache.windows.net` |
| Data Factory | `dataFactory` | `privatelink.datafactory.azure.net` |
| API Management | `Gateway` | `privatelink.azure-api.net` |
| Event Hub | `namespace` | `privatelink.servicebus.windows.net` |
| Service Bus | `namespace` | `privatelink.servicebus.windows.net` |
| Monitor (AMPLS) | ⚠️ Configuração complexa, consulte abaixo | ⚠️ Exige várias DNS Zones, consulte abaixo |

> **Observação sobre o ADLS Gen2**: quando `isHnsEnabled: true`, **os PEs `blob` e `dfs` são obrigatórios**.
>
> - Somente com o PE `blob`, a API Blob funciona, mas as operações do lago de dados (Data Lake), como criação de sistema de arquivos, manipulação de diretórios e protocolo `abfss://`, falham.
> - PE DFS: `groupId` `dfs`, DNS Zone `privatelink.dfs.core.windows.net`
>
> **⚠️ Observação sobre Azure Monitor Private Link (AMPLS)**: não é possível configurar Azure Monitor com um único PE e uma única DNS Zone. Ele se conecta pelo Azure Monitor Private Link Scope (AMPLS), e as **cinco DNS Zones** são obrigatórias:
>
> - `privatelink.monitor.azure.com`
> - `privatelink.oms.opinsights.azure.com`
> - `privatelink.ods.opinsights.azure.com`
> - `privatelink.agentsvc.azure-automation.net`
> - `privatelink.blob.core.windows.net` (para ingestão de dados do Log Analytics)
>
> Esse mapeamento é complexo e pode mudar. Sempre consulte e confirme o Microsoft Docs ao configurar um PE do Monitor:
> https://learn.microsoft.com/en-us/azure/azure-monitor/logs/private-link-configure

---

## 3. Lista de verificação de erros comuns

| Item | ❌ Exemplo incorreto | ✅ Exemplo correto |
|------|---------------------|-------------------|
| HNS do ADLS Gen2 | `isHnsEnabled` ausente ou `false` | `isHnsEnabled: true` |
| Sub-rede de PE | Política não configurada | `privateEndpointNetworkPolicies: 'Disabled'` |
| DNS Zone Group | Somente o PE foi criado | PE + DNS Zone + VNet Link + DNS Zone Group |
| Recurso Foundry | `kind: 'OpenAI'` | `kind: 'AIServices'` + `allowProjectManagement: true` |
| Recurso Foundry | `customSubDomainName` ausente | `customSubDomainName: foundryName`, não pode ser alterado após a criação |
| Foundry Project | Somente o Foundry existe, sem Project | Deve ser criado em conjunto |
| Autenticação do Key Vault | Política de acesso (Access Policy) | `enableRbacAuthorization: true` |
| Rede pública | Não configurada | `publicNetworkAccess: 'Disabled'` |
| Nome do Storage | `st-my-storage` | `stmystorage` ou `st${uniqueString(...)}` |
| Versão da API | Copiada de uma conversa ou erro anterior | Verifique a versão estável mais recente no Microsoft Docs |
| Região | Valor fixo (`'eastus'`) | Passe como parâmetro (`param location`) |
| Valores confidenciais | Texto não criptografado em `.bicepparam` | `@secure()` + referência do Key Vault |

---

## 4. Regras de decisão sobre relações entre serviços

São **regras de seleção padrão**, não determinações absolutas.

### Foundry versus Azure OpenAI versus AI Hub

```
Regras padrão:
├─ Cargas de trabalho de IA/RAG → use Microsoft Foundry (kind: 'AIServices')
│   ├─ Crie o recurso Foundry + Foundry Project em conjunto
│   └─ Implante o modelo no nível do recurso Foundry (accounts/deployments)
│
├─ Treinamento de ML/modelos de código aberto necessário → considere AI Hub (MachineLearningServices)
│   └─ Somente mediante solicitação explícita ou necessidade de recursos sem suporte no Foundry
│
└─ Recurso autônomo do Azure OpenAI →
    Considere somente mediante solicitação explícita ou
    quando a documentação oficial exigir um recurso separado
```

> Estas regras são um **guia de seleção padrão** que reflete as recomendações atuais da Microsoft.
> As relações entre produtos do Azure podem mudar. Consulte o Microsoft Docs em caso de dúvida.

### Monitoramento

```
Regras padrão:
├─ Foundry (AIServices) → Application Insights não é obrigatório
└─ AI Hub (MachineLearningServices) → Application Insights + Log Analytics são obrigatórios
```
