---
name: "azure-well-architected-review"
description: "Use quando a pessoa pedir uma revisão do Azure Well-Architected Framework, uma avaliação de arquitetura ou uma auditoria de confiabilidade, segurança, custo, desempenho ou excelência operacional de uma carga de trabalho do Azure. Revisa os cinco pilares do WAF em relação à IaC da carga de trabalho (Terraform neste kit; Bicep/ARM também podem ser lidos) e aos recursos implantados e abre itens no GitHub Issues para as constatações. Os gatilhos incluem \"revisão WAF\", \"Well-Architected\", \"avaliação de arquitetura\", \"auditoria de confiabilidade\" e \"revisão de segurança do Azure\"."
---
# Revisão do Azure Well-Architected

Este fluxo de trabalho executa uma revisão estruturada do Azure Well-Architected Framework (WAF) nos arquivos de IaC e na infraestrutura implantada de uma carga de trabalho. Ele identifica riscos nos cinco pilares do WAF e cria itens no GitHub Issues para acompanhar as correções.

> [!NOTE]
> A IaC deste kit é **Terraform (`azurerm ~> 3.x`)**. A revisão lê qualquer IaC existente (Terraform, Bicep ou ARM), mas os exemplos de correção são escritos em Terraform. Os trechos em Bicep/ARM são apenas ilustrativos e estão fora do escopo das entregas do kit. Esta habilidade também depende da autenticação da **CLI `az`** e do **servidor MCP do GitHub** (ou `gh`).

## Quando usar

- "Execute uma revisão Well-Architected em nossa carga de trabalho do Azure."
- "Audite esta arquitetura em busca de riscos de confiabilidade e segurança."
- "Estamos seguindo as práticas recomendadas do Azure nos cinco pilares?"
- "Abra itens no GitHub Issues para as lacunas do WAF em nossa infraestrutura."

## Pré-requisitos

- CLI do Azure (`az`) configurada e autenticada.
- Arquivos de IaC presentes no repositório (preferencialmente Terraform; Bicep ou ARM também podem ser lidos).
- Servidor MCP do GitHub (ou `gh`) configurado e autenticado.

## Etapas do fluxo de trabalho

### Etapa 1: Carregar a referência do Well-Architected Framework

Consulte as práticas recomendadas atuais do WAF do Azure:

- `https://learn.microsoft.com/en-us/azure/well-architected/`
- Guias dos serviços do Azure em uso (`https://learn.microsoft.com/en-us/azure/well-architected/service-guides/`)
- Orientações específicas relevantes para o tipo de carga de trabalho (SaaS, missão crítica, IA e semelhantes)

Se o servidor MCP `microsoft.docs.mcp` estiver disponível, use-o para consultar as listas de verificação mais recentes dos pilares e as recomendações específicas dos serviços.

### Etapa 2: Descobrir a IaC e a arquitetura

Defina o escopo da revisão e inventarie o código e o ambiente ativo:

1. **Confirme o escopo do Azure**: pergunte quais assinaturas e grupos de recursos estão no escopo ou infira-os dos parâmetros de IaC e confirme.
2. **Examine o repositório em busca de arquivos de IaC**:
   - Terraform: `**/*.tf` (provedores azurerm/azapi), a IaC principal deste kit
   - Bicep: `**/*.bicep`, `bicepconfig.json`
   - Modelos ARM: `**/azuredeploy*.json`, `**/*.template.json`, arquivos cujo `$schema` contenha `deploymentTemplate`
3. **Inventarie os recursos ativos** sempre, mesmo quando houver IaC: `az resource list --resource-group <rg> --output json` (ou em toda a assinatura), além de chamadas direcionadas a `az <service> show` para obter os detalhes de configuração necessários às verificações dos pilares.
4. **Compare a IaC com o inventário ativo**: sinalize desvios, como recursos presentes no Azure e ausentes da IaC (criados pelo portal), recursos definidos na IaC mas não implantados e diferenças de configuração. Registre as constatações de desvio para a Etapa 3. Em geral, elas correspondem ao pilar Excelência operacional.

Identifique os principais serviços do Azure em uso (computação, dados, rede, segurança e observabilidade) e gere um diagrama de arquitetura Mermaid.

### Etapa 3: Revisão por pilar

#### Pilar 1: Confiabilidade

- [ ] Zonas de disponibilidade ativadas para serviços zonais (VMs, VMSS, conjuntos de nós do AKS, App Service, SQL, Storage ZRS)
- [ ] SKUs de produção compatíveis com o SLA necessário (sem camadas Basic/Free em caminhos críticos)
- [ ] Cópia de segurança e restauração pontual do Azure SQL/Cosmos DB configuradas com retenção adequada
- [ ] Redundância geográfica configurada quando exigida pelo RPO (armazenamento GRS/RA-GRS, grupos de comutação por falha do SQL, Cosmos DB em várias regiões)
- [ ] Regras de dimensionamento automático configuradas para planos do App Service, VMSS e AKS (sem instância única fixa em produção)
- [ ] Investigações de integridade configuradas nos serviços de destino do Load Balancer/Application Gateway/Front Door
- [ ] Filas de mensagens mortas ativadas em filas/assinaturas do Service Bus e assinaturas do Event Grid
- [ ] Políticas de repetição com espera exponencial implementadas para tratar falhas transitórias
- [ ] Plano de recuperação de desastre definido (RTO/RPO documentados e comutação por falha testada)

#### Pilar 2: Segurança

- [ ] Identidades gerenciadas usadas em vez de entidades de serviço com segredos ou cadeias de conexão
- [ ] Nenhuma credencial, chave ou cadeia de conexão fixada na IaC ou no código
- [ ] Segredos armazenados no Azure Key Vault com autorização RBAC (não políticas de acesso)
- [ ] Contas de armazenamento negam acesso público a blobs e desativam o acesso por chave compartilhada quando possível
- [ ] Pontos de extremidade privados (ou, no mínimo, pontos de extremidade de serviço com regras de firewall) para serviços de dados PaaS
- [ ] NSGs restringem o tráfego de entrada às portas/CIDRs mínimos necessários (sem regras de permissão de `*` para `*`)
- [ ] TLS 1.2 ou superior aplicado em todos os pontos de extremidade (`minimumTlsVersion`, `httpsOnly`)
- [ ] Azure RBAC segue o privilégio mínimo (sem Owner/Contributor no escopo da assinatura para identidades de carga de trabalho)
- [ ] Microsoft Defender for Cloud ativado nos tipos de recurso relevantes (`az security pricing list`)
- [ ] Azure WAF (Application Gateway ou Front Door) configurado para pontos de extremidade Web públicos
- [ ] Configurações de diagnóstico enviam logs de segurança ao Log Analytics/Microsoft Sentinel

#### Pilar 3: Otimização de custos

- [ ] Reservas ou planos de economia avaliados para computação de uso constante (VMs, App Service, SQL)
- [ ] Políticas de ciclo de vida do armazenamento movem blobs para camadas de acesso esporádico/arquivo
- [ ] SKUs dimensionadas conforme a utilização real (sem VMs ou planos do App Service superdimensionados)
- [ ] Ambientes de desenvolvimento/teste usam agendas de desligamento automático e preços de Dev/Test quando elegíveis
- [ ] Azure Budgets e alertas de custo configurados (`az consumption budget list`)
- [ ] Discos gerenciados não anexados e IPs públicos órfãos identificados e removidos
- [ ] Camadas de consumo/sem servidor usadas para cargas com picos ou baixo volume (Functions, Container Apps, SQL sem servidor, identificado tecnicamente como SQL serverless)
- [ ] Retenção e limite de dados do Log Analytics ajustados para evitar excesso de ingestão

#### Pilar 4: Excelência operacional

- [ ] Toda a infraestrutura definida como IaC (sem alterações manuais pelo portal; atribuições de negação ou políticas quando viável)
- [ ] Estratégia consistente de tags aplicada a todos os recursos (responsável, ambiente, centro de custo)
- [ ] Alertas do Azure Monitor definidos para métricas principais e integridade do serviço
- [ ] Pipeline automatizado de implantação presente (GitHub Actions/Azure Pipelines, sem implantações manuais)
- [ ] Azure Activity Log e configurações de diagnóstico dos recursos direcionados ao Log Analytics
- [ ] Application Insights (ou equivalente OpenTelemetry) instrumentado para cargas de aplicações
- [ ] Atribuições do Azure Policy aplicam os padrões da organização (locais, SKUs e tags permitidos)
- [ ] Guias operacionais ou documentação operacional presentes

#### Pilar 5: Eficiência de desempenho

- [ ] SKUs de computação dimensionadas e validadas em relação aos requisitos de carga
- [ ] Cache implementado onde for benéfico (Azure Cache for Redis, cache de CDN/Front Door)
- [ ] Azure Front Door ou CDN usado para entrega global de conteúdo estático
- [ ] Dimensionamento automático baseado em métricas de carga, não em quantidades fixas de instâncias
- [ ] Camada de desempenho do banco de dados adequada (DTU ou vCore, conjuntos elásticos, dimensionamento automático de RU do Cosmos DB)
- [ ] Armazenamento premium/redundante por zona usado para cargas de disco sensíveis à latência
- [ ] Conjunto de conexões e padrões assíncronos usados em clientes de banco de dados e HTTP

### Etapa 4: Classificação de riscos

Classifique cada constatação:

| Risco | Significado |
|---|---|
| Alto | Vulnerabilidade de segurança, ponto único de falha, ausência de backup/recuperação |
| Médio | Confiabilidade abaixo do ideal, ineficiência de custos, preocupação com desempenho |
| Baixo | Desvio de prática recomendada, pequena oportunidade de otimização |

### Etapa 5: Confirmação da pessoa

Apresente o resumo e exija aprovação explícita antes de criar qualquer item no GitHub Issues:

```text
Resumo da revisão do Azure Well-Architected

Resultados da revisão:
- Arquivos de IaC analisados: X
- Serviços do Azure identificados: Y
- Total de constatações: Z
  - Risco alto: A (exige ação imediata)
  - Risco médio: B (deve ser tratado em breve)
  - Risco baixo: C (melhoria desejável)

Principais constatações de risco alto:
1. [Pilar]: [Constatação] - [Por que é importante]
2. [Pilar]: [Constatação] - [Por que é importante]

Isso criará Z itens individuais no GitHub Issues e 1 épico (EPIC).

Prosseguir com a criação dos itens no GitHub Issues? (s/n)
```

> [!IMPORTANT]
> Só prossiga para as Etapas 6 e 7 se a pessoa der uma resposta afirmativa explícita (por exemplo, "s" ou "sim"). Diante de uma resposta negativa, ambígua ou ausente, **não** crie itens no GitHub Issues. Exiba todas as constatações como Markdown formatado no console e pare.

### Etapa 6: Criar itens individuais para as constatações

Use os rótulos `well-architected` e o nome do pilar (por exemplo, `security`, `reliability`).

Título: `[WAF-<PILLAR>] <Brief Finding> - <Risk Level>`

Corpo:

````markdown
## Constatação Well-Architected: <Brief Title>

**Pilar**: <Name> | **Nível de risco**: <High/Medium/Low> | **Esforço**: <Low/Medium/High>

### Descrição
<Clear explanation of the finding and why it matters>

### Correção

Correção de IaC (preferencial, Terraform, a IaC deste kit):
```hcl
resource "azurerm_storage_account" "data" {
  name                            = "sifapdata"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "ZRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false

  tags = {
    project     = "sifap"
    environment = "prod"
    owner       = "platform-team"
  }
}
```

Alternativa com a CLI do Azure:
```bash
az storage account update --name <name> --resource-group <rg> \
  --min-tls-version TLS1_2 --allow-blob-public-access false --https-only true
```

### Referência do Azure
- <WAF best-practice link>
- <Microsoft Learn documentation link>

### Validação
- [ ] Alteração implementada em Terraform e aplicada
- [ ] Conformidade com o Azure Policy aprovada (se aplicável)
- [ ] Recomendação do Microsoft Defender for Cloud resolvida (se aplicável)

**Recomendação Well-Architected**: <WAF checklist item this maps to>
````

### Etapa 7: Criar o item EPIC de acompanhamento

Use os rótulos `well-architected` e `epic`.

Título: `[EPIC] Revisão do Azure Well-Architected - X constatações em 5 pilares`

Corpo: um resumo executivo com uma tabela por pilar (quantidade de constatações por pilar e nível de risco), um diagrama de arquitetura Mermaid, uma lista de verificação priorizada com links para todos os itens individuais (Alto, Médio e Baixo) e os critérios de sucesso:

- Todas as constatações de risco Alto resolvidas
- Constatações de risco Médio com planos de mitigação aceitos
- Nenhuma regressão nos alertas existentes do Azure Monitor nem na conformidade com o Azure Policy

## Tratamento de erros

| Situação | Ação |
|---|---|
| Nenhum arquivo de IaC encontrado | Limite a revisão à descoberta de recursos ativos por `az resource list` e registre a lacuna |
| Permissões insuficientes no Azure | Liste as funções somente leitura necessárias (Reader, Security Reader) |
| Falha na criação no GitHub | Exiba todas as constatações como Markdown formatado no console |

## Modelo de saída

Quando a criação de itens for ignorada (ou no resumo do console), entregue as constatações em uma tabela agrupada por pilar:

```markdown
## Revisão Well-Architected: <workload>

| Pilar | Constatação | Risco | Correção |
|---|---|---|---|
| Segurança | O Storage permite acesso público a blobs | Alto | Definir allow_nested_items_to_be_public = false |
| Confiabilidade | O App Service executa uma única instância | Médio | Ativar dimensionamento automático, com no mínimo 2 instâncias |
| Custo | O Log Analytics não tem limite de dados | Baixo | Definir um limite diário e uma política de retenção |

Totais: 1 Alto, 1 Médio e 1 Baixo nos 5 pilares.
Conclusão: trate a constatação de segurança de risco Alto antes do próximo lançamento.
```

## Critérios de qualidade

- [ ] Os cinco pilares do WAF foram revisados em relação à IaC e à infraestrutura ativa.
- [ ] Cada constatação está classificada por nível de risco e associada a um pilar.
- [ ] Cada constatação tem uma correção acionável em Terraform (Bicep/ARM apenas como ilustração).
- [ ] Os desvios entre a IaC e os recursos implantados foram registrados como constatações de Excelência operacional.
- [ ] Os itens no GitHub Issues só foram criados após aprovação explícita da pessoa. Caso contrário, as constatações foram exibidas no console.
- [ ] Um diagrama de arquitetura Mermaid e referências do Microsoft Learn estão incluídos.
