---
name: "azure-resource-health-diagnose"
description: "Use quando a pessoa informar que um recurso implantado do Azure está com falha, degradação, limitação ou indisponibilidade, ou pedir sua investigação. Diagnostica um recurso específico pelos logs, métricas e telemetria e produz um plano de correção priorizado. Requer que o recurso esteja implantado e emitindo telemetria. Os gatilhos incluem \"recurso não íntegro\", \"solucionar problemas do Azure\", \"por que isto está falhando\", \"diagnosticar limitação\" e \"investigar recurso degradado\"."
---
# Integridade de recursos do Azure e diagnóstico de problemas

Este fluxo de trabalho analisa um recurso específico do Azure para avaliar sua integridade, diagnosticar problemas por logs e telemetria e desenvolver um plano de correção.

> [!NOTE]
> Esta habilidade depende do **servidor MCP do Azure** (ou da CLI `az`) e exige que o recurso de destino esteja implantado e emitindo telemetria. Quando ambos estiverem disponíveis, prefira as ferramentas MCP do Azure (`azmcp-*`) à CLI do Azure.

## Quando usar

- "Nosso App Service está retornando erros 500. Faça o diagnóstico."
- "Investigue por que este Cosmos DB está sendo limitado."
- "A conta de armazenamento parece degradada. Encontre a causa raiz."
- "Solucione os problemas desta VM e forneça um plano de correção."

## Pré-requisitos

- Servidor MCP do Azure configurado e autenticado.
- Recurso de destino do Azure identificado (nome e, opcionalmente, grupo de recursos/assinatura).
- O recurso deve estar implantado e em execução para gerar logs e telemetria.

## Etapas do fluxo de trabalho

### Etapa 1: Obter as práticas recomendadas do Azure

Obtenha práticas recomendadas de diagnóstico e solução de problemas com a ferramenta de práticas recomendadas do Azure. Concentre-se em monitoramento de integridade, análise de logs e padrões de resolução de problemas. Use-os para orientar o diagnóstico e as recomendações de correção.

### Etapa 2: Descoberta e identificação do recurso

1. **Localize o recurso**:
   - Se apenas um nome for fornecido, pesquise nas assinaturas (`azmcp-subscription-list` ou `az resource list --name <resource-name>`).
   - Se houver várias correspondências, peça que a pessoa especifique a assinatura ou o grupo de recursos.
   - Colete tipo e status do recurso, local, tags, configuração e dependências.
2. **Detecte o tipo de recurso** para escolher os diagnósticos adequados:

| Tipo de recurso | Diagnósticos principais |
|---|---|
| Web Apps / Function Apps | Logs da aplicação, métricas de desempenho, rastreamento de dependências |
| Virtual Machines | Logs do sistema, contadores de desempenho, diagnóstico de inicialização |
| Cosmos DB | Métricas de solicitações, limitação, estatísticas de partições |
| Storage Accounts | Logs de acesso, métricas de desempenho, disponibilidade |
| SQL Database | Desempenho de consultas, logs de conexão, utilização de recursos |
| Application Insights | Telemetria da aplicação, exceções, dependências |
| Key Vault | Logs de acesso, status de certificados, uso de segredos |
| Service Bus | Métricas de mensagens, filas de mensagens mortas, taxa de transferência |

### Etapa 3: Avaliação do status de integridade

1. **Verificação básica de integridade**: estado de provisionamento e status operacional, disponibilidade do serviço, alterações recentes de implantação ou configuração e utilização atual (CPU, memória e armazenamento).
2. **Indicadores específicos do serviço**:

| Tipo de recurso | Indicadores de integridade |
|---|---|
| Web Apps | Códigos de resposta HTTP, tempos de resposta, tempo de atividade |
| Bancos de dados | Taxa de sucesso das conexões, desempenho das consultas, impasses |
| Storage | Percentual de disponibilidade, taxa de sucesso das solicitações, latência |
| VMs | Diagnóstico de inicialização, métricas do sistema operacional convidado, conectividade de rede |
| Functions | Taxa de sucesso, duração e frequência de erros das execuções |

### Etapa 4: Análise de logs e telemetria

1. **Encontre as fontes de monitoramento**: identifique espaços de trabalho do Log Analytics (`azmcp-monitor-workspace-list`), instâncias associadas do Application Insights e tabelas de logs relevantes (`azmcp-monitor-table-list`).
2. **Execute consultas de diagnóstico** com `azmcp-monitor-log-query` e escolha a KQL conforme o tipo de recurso.

Análise geral de erros:

```kql
union isfuzzy=true
    AzureDiagnostics,
    AppServiceHTTPLogs,
    AppServiceAppLogs,
    AzureActivity
| where TimeGenerated > ago(24h)
| where Level == "Error" or ResultType != "Success"
| summarize ErrorCount=count() by Resource, ResultType, bin(TimeGenerated, 1h)
| order by TimeGenerated desc
```

Análise de desempenho:

```kql
Perf
| where TimeGenerated > ago(7d)
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 1h)
| where avg_CounterValue > 80
```

Consultas específicas da aplicação:

```kql
requests
| where timestamp > ago(24h)
| where success == false
| summarize FailureCount=count() by resultCode, bin(timestamp, 1h)
| order by timestamp desc
```

3. **Reconheça padrões**: erros ou anomalias recorrentes, correlação com alterações de implantação/configuração, tendências de degradação do desempenho e falhas em dependências ou serviços externos.

### Etapa 5: Classificação dos problemas e análise de causa raiz

1. **Classifique a gravidade**:

| Gravidade | Significado |
|---|---|
| Crítica | Serviço indisponível, perda de dados, violação de segurança |
| Alta | Degradação do desempenho, falhas intermitentes, alta taxa de erros |
| Média | Avisos, configuração abaixo do ideal, pequenos problemas de desempenho |
| Baixa | Alertas informativos, oportunidades de otimização |

2. **Determine a categoria da causa raiz**: problema de configuração, restrição de recursos (CPU/memória/disco/limitação), problema de rede, problema da aplicação (falha, vazamento de memória, consulta ineficiente), dependência externa ou problema de segurança (falha de autenticação, expiração de certificado).
3. **Avalie o impacto**: usuários e sistemas afetados, implicações para integridade e segurança dos dados e prioridades de tempo de recuperação.

### Etapa 6: Gerar um plano de correção

1. **Ações imediatas** (Crítica): correções emergenciais para restaurar a disponibilidade, soluções temporárias e procedimentos de escalonamento.
2. **Correções de curto prazo** (Alta/Média): ajustes de configuração, dimensionamento de recursos, correções de software e melhorias de monitoramento.
3. **Melhorias de longo prazo**: alterações de arquitetura para resiliência, medidas preventivas e documentação.
4. **Etapas de implementação**: itens priorizados com comandos específicos da CLI do Azure, testes/validação, planos de reversão e monitoramento após a alteração.

### Etapa 7: Confirmação da pessoa e geração do relatório

Apresente um resumo e condicione a correção à aprovação da pessoa:

```text
Avaliação da integridade do recurso do Azure

Visão geral do recurso:
- Recurso: [Nome] ([Tipo])
- Status: [Íntegro/Aviso/Crítico]
- Local: [Região]
- Última análise: [Timestamp]

Problemas identificados:
- Críticos: X problemas que exigem atenção imediata
- Altos: Y problemas que afetam o desempenho ou a confiabilidade
- Médios: Z problemas para otimização
- Baixos: N itens informativos

Principais problemas:
1. [Tipo do problema]: [Descrição] - Impacto: [Alto/Médio/Baixo]

Plano de correção:
- Ações imediatas: X itens
- Correções de curto prazo: Y itens
- Melhorias de longo prazo: Z itens
- Tempo estimado para resolução: [Prazo]

Prosseguir com o plano de correção detalhado? (s/n)
```

Após a aprovação, gere o relatório detalhado com o modelo de saída abaixo.

## Tratamento de erros

| Situação | Ação |
|---|---|
| Recurso não encontrado | Solicite o nome e o local exatos |
| Problemas de autenticação | Oriente a configuração da autenticação do Azure |
| Permissões insuficientes | Liste as funções RBAC somente leitura necessárias |
| Nenhum log disponível | Sugira ativar as configurações de diagnóstico e aguardar os dados |
| Tempo limite das consultas | Divida a análise em janelas de tempo menores |
| Lacunas específicas do serviço | Forneça uma avaliação genérica de integridade e registre as limitações |

## Modelo de saída

A habilidade escreve um relatório de integridade. Abaixo do título H1 (`Relatório de integridade do recurso do Azure: <resource>`), ele contém:

````markdown
## Resumo executivo

<overview of health status and key findings>

## Métricas de integridade

- Disponibilidade: X% nas últimas 24 h
- Taxa de erros: X% nas últimas 24 h
- Utilização de recursos: percentuais de CPU/memória/armazenamento

## Problemas identificados

### Problemas críticos

- <Issue>: causa raiz, impacto no negócio, ação imediata

### Problemas de alta prioridade

- <Issue>: causa raiz, impacto na confiabilidade, correção recomendada

## Plano de correção

### Fase 1: ações imediatas (0 a 2 horas)

```bash
<Azure CLI commands to restore service, with explanations>
```

### Fase 2: correções de curto prazo (2 a 24 horas)

```bash
<Azure CLI commands for reliability improvements>
```

### Fase 3: melhorias de longo prazo (1 a 4 semanas)

```bash
<Azure CLI and configuration changes>
```

## Etapas de validação

- [ ] Verificar a resolução do problema pelos logs
- [ ] Confirmar as melhorias de desempenho
- [ ] Testar a funcionalidade da aplicação
- [ ] Atualizar o monitoramento e os alertas
````

## Critérios de qualidade

- [ ] O status de integridade do recurso foi avaliado com precisão a partir de logs, métricas e telemetria.
- [ ] Todos os problemas significativos foram identificados e classificados por gravidade.
- [ ] A análise de causa raiz foi concluída para cada constatação Crítica e Alta.
- [ ] O plano de correção fornece etapas específicas da CLI do Azure, com validação e reversão.
- [ ] Os problemas estão priorizados por impacto no negócio, com recomendações de monitoramento e prevenção.
- [ ] As ações detalhadas de correção só são executadas após confirmação explícita da pessoa.
