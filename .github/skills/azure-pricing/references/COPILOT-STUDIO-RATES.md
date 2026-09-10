# Copilot Studio: tarifas de cobrança e estimativa

> Fonte: [Tarifas e gerenciamento de cobrança](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)
> Estimador: [Estimador de uso de agentes da Microsoft](https://microsoft.github.io/copilot-studio-estimator/)
> Guia de licenciamento: [Guia de licenciamento do Copilot Studio](https://go.microsoft.com/fwlink/?linkid=2320995)

## Tarifa do Copilot Credit

**1 Copilot Credit = $0.01 USD**

## Tarifas de cobrança (registro instantâneo em cache, atualizado em março de 2026)

**IMPORTANTE: sempre prefira obter as tarifas atuais nas URLs de origem abaixo. Use esta tabela somente como alternativa se a consulta à Web não estiver disponível.**

| Funcionalidade | Tarifa | Unidade |
|---|---|---|
| Resposta clássica | 1 | por resposta |
| Resposta generativa | 2 | por resposta |
| Ação do agente | 5 | por ação (gatilhos, raciocínio aprofundado, transições de tópico, uso do computador) |
| Fundamentação no grafo do locatário | 10 | por mensagem |
| Ações de fluxo do agente | 13 | por 100 ações de fluxo |
| Ferramentas de texto e IA generativa (básicas) | 1 | por 10 respostas |
| Ferramentas de texto e IA generativa (padrão) | 15 | por 10 respostas |
| Ferramentas de texto e IA generativa (premium) | 100 | por 10 respostas |
| Ferramentas de processamento de conteúdo | 8 | por página |

### Observações

- **Respostas clássicas**: respostas predefinidas e escritas manualmente. São estáticas e só mudam quando quem as criou as atualiza.
- **Respostas generativas**: geradas dinamicamente por modelos de IA (GPTs). Adaptam-se ao contexto e às fontes de conhecimento.
- **Fundamentação no grafo do locatário**: geração aumentada por recuperação (RAG) no Microsoft Graph de todo o locatário, incluindo dados externos por conectores. É opcional por agente.
- **Ações do agente**: etapas como gatilhos, raciocínio aprofundado e transições de tópico visíveis no mapa de atividades. Inclui agentes que usam computador (Computer-Using Agents).
- **Ferramentas de texto e IA generativa**: ferramentas de instrução incorporadas aos agentes. Há três camadas (básica, padrão e premium), conforme o modelo de linguagem subjacente.
- **Ações de fluxo do agente**: sequências predefinidas de ações de fluxo executadas sem raciocínio ou orquestração do agente em cada etapa.

### Cobrança de modelos de raciocínio

Ao usar um modelo com capacidade de raciocínio:

```
Custo total = tarifa da funcionalidade por operação + ferramentas de texto e IA generativa (premium) a cada 10 respostas
```

Exemplo: uma resposta generativa que usa um modelo de raciocínio custa **2 créditos** (resposta generativa) **+ 10 créditos** (premium por resposta, rateado de 100/10).

## Fórmula de estimativa

### Entradas

| Parâmetro | Descrição |
|---|---|
| `users` | Quantidade de usuários finais |
| `interactions_per_month` | Média mensal de interações por usuário |
| `knowledge_pct` | Percentual de respostas provenientes de fontes de conhecimento (0 a 100) |
| `tenant_graph_pct` | Entre as respostas de conhecimento, percentual que usa fundamentação no grafo do locatário (0 a 100) |
| `tool_prompt` | Média de chamadas à ferramenta de instrução por sessão |
| `tool_agent_flow` | Média de chamadas a fluxos do agente por sessão |
| `tool_computer_use` | Média de chamadas de uso do computador por sessão |
| `tool_custom_connector` | Média de chamadas a conectores personalizados por sessão |
| `tool_mcp` | Média de chamadas MCP (Model Context Protocol) por sessão |
| `tool_rest_api` | Média de chamadas à API REST por sessão |
| `prompts_basic` | Média de usos de instruções básicas de IA por sessão |
| `prompts_standard` | Média de usos de instruções padrão de IA por sessão |
| `prompts_premium` | Média de usos de instruções premium de IA por sessão |

### Cálculo

```
total_sessions = users × interactions_per_month

── Créditos de conhecimento ──
tenant_graph_credits    = total_sessions × (knowledge_pct/100) × (tenant_graph_pct/100) × 10
generative_answer_credits = total_sessions × (knowledge_pct/100) × (1 - tenant_graph_pct/100) × 2
classic_answer_credits  = total_sessions × (1 - knowledge_pct/100) × 1

── Créditos de ferramentas do agente ──
tool_calls = total_sessions × (prompt + computer_use + custom_connector + mcp + rest_api)
tool_credits = tool_calls × 5

── Créditos de fluxo do agente ──
flow_calls = total_sessions × tool_agent_flow
flow_credits = ceil(flow_calls / 100) × 13

── Créditos de modificação de prompt ──
basic_credits    = ceil(total_sessions × prompts_basic / 10) × 1
standard_credits = ceil(total_sessions × prompts_standard / 10) × 15
premium_credits  = ceil(total_sessions × prompts_premium / 10) × 100

── Total ──
total_credits = knowledge + tools + flows + prompts
cost_usd = total_credits × 0.01
```

## Exemplos de cobrança (da documentação da Microsoft)

### Agente de suporte ao cliente

- 4 respostas clássicas + 2 respostas generativas por sessão
- 900 clientes/dia
- **Diário**: `[(4×1) + (2×2)] × 900 = 7.200 créditos`
- **Mensal (30 dias)**: cerca de 216.000 créditos = **cerca de $2.160**

### Agente de desempenho de vendas (fundamentado no grafo do locatário)

- 4 respostas generativas + 4 respostas fundamentadas no grafo do locatário por sessão
- 100 usuários não licenciados
- **Diário**: `[(4×2) + (4×10)] × 100 = 4.800 créditos`
- **Mensal (30 dias)**: cerca de 144.000 créditos = **cerca de $1.440**

### Agente de processamento de pedidos

- 4 chamadas de ação por gatilho (autônomo)
- **Por gatilho**: `4 × 5 = 20 créditos`

## Tipos de agentes para funcionários e clientes

| Tipo de agente | Incluído no M365 Copilot? |
|---|---|
| Voltado a funcionários (BtoE) | Respostas clássicas, respostas generativas e fundamentação no grafo do locatário estão incluídas sem custo quando o usuário tem uma licença do Microsoft 365 Copilot |
| Voltado a clientes/parceiros | Todo o uso é cobrado normalmente |

## Aplicação do limite excedente

- Acionada ao atingir **125%** da capacidade pré-paga
- Os agentes personalizados são desativados (as conversas em andamento continuam)
- Uma notificação por email é enviada à administração do locatário
- Resolução: realocar capacidade, comprar mais ou ativar o pagamento conforme o uso

## URLs de fontes atuais

Para obter as tarifas mais recentes, consulte estas páginas:

- [Tarifas e gerenciamento de cobrança](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)
- [Licenciamento do Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing)
- [Guia de licenciamento do Copilot Studio (PDF)](https://go.microsoft.com/fwlink/?linkid=2320995)
