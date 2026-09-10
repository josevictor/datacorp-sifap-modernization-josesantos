# Fase 1: consultor de arquitetura

Este arquivo contém as instruções detalhadas da Fase 1. Leia-o e siga-o ao entrar nessa fase por SKILL.md.
Usado no Caminho A (novo projeto) e no Caminho B (modificação após o exame da Fase 0).

---

## Entrada pelo Caminho B (após analisar recursos existentes)

O diagrama atual (`00_arch_current.html`) gerado na Fase 0 já existe.
Nesse caso, pule a confirmação do nome/lista de serviços em 1-1 e converse diretamente sobre modificações:

1. "O que você deseja alterar?": solicitação em linguagem natural
2. Aplique a Regra de Confirmação das Alterações: confirme campos obrigatórios em aberto
3. Verifique os fatos por validação cruzada no Microsoft Docs
4. Gere o diagrama atualizado (`01_arch_diagram_draft.html`)
5. Após a confirmação, siga para a Fase 2

---

**Objetivo desta fase**: identificar com precisão a necessidade e finalizar a arquitetura em conjunto.

### 1-1. Preparar o diagrama: coletar informações obrigatórias

Antes de desenhar, faça perguntas até confirmar todos os itens abaixo.
**Gere o diagrama somente após confirmar todos os itens.**

**Primeiro, confirme o nome do projeto:**

Ofereça um valor padrão por `ask_user`. Se a pessoa somente pressionar Enter, aplique o padrão; aceite também um nome personalizado.
Infira o padrão da solicitação (por exemplo, assistente de conversa RAG → `rag-chatbot`; plataforma de dados → `data-platform`).

```
ask_user({
  question: "Escolha um nome de projeto. Ele será usado na pasta do Bicep, no caminho do diagrama e no nome da implantação.",
  choices: ["<inferred-default>", "azure-project"]
})
```

O nome do projeto é usado na pasta de saída do Bicep, no caminho do diagrama, no nome da implantação etc.

**🔹 Pré-carregamento paralelo com a pergunta do nome do projeto (obrigatório):**

Enquanto `ask_user` aguarda a resposta sobre o nome, há tempo ocioso.
Use-o para **pré-carregar em paralelo as informações necessárias às próximas perguntas e à geração de Bicep**.

**Ferramentas a chamar simultaneamente com ask_user:**

```
// Chama ask_user e as ferramentas abaixo simultaneamente em uma única resposta
[1] ask_user: pergunta sobre o nome do projeto

[2] view: carrega arquivos de referência (obtém previamente informações estáveis)
    - references/service-gotchas.md
    - references/ai-data.md
    - references/azure-dynamic-sources.md
    - references/architecture-guidance-sources.md

[3] web_fetch: consulta previamente a orientação de arquitetura (quando identificar a carga)
    - Até duas consultas específicas conforme architecture-guidance-sources.md

[4] web_fetch: consulta o Microsoft Docs dos serviços mencionados (obtém informações dinâmicas)
    - Por exemplo, Foundry → versão da API e disponibilidade de modelos
    - Por exemplo, AI Search → lista de SKUs
    - Usa padrões de URL de azure-dynamic-sources.md
```

**Benefícios**: enquanto a pessoa digita o nome, as informações são carregadas.
Assim, perguntas sobre SKU/região já apresentam opções precisas após a confirmação do nome.
Isso reduz bastante a espera em comparação com a execução sequencial.

**Observações:**

- Pré-carregue somente informações independentes do nome do projeto
- Execute `web_fetch` somente para serviços mencionados na solicitação inicial (sem suposições)
- NÃO verifique a CLI do Azure (`az account show`) agora; faça isso ao finalizar a arquitetura

**🔹 Uso da orientação de arquitetura (ajuste da profundidade das perguntas):**

Extraia **pontos de decisão do projeto** dos documentos consultados no pré-carregamento
e incorpore-os naturalmente às perguntas seguintes.

**Finalidade**: não tratar somente de especificações como SKU/região,
mas refletir nas perguntas os **pontos de decisão** recomendados pela orientação oficial.

**Exemplo: solicitação de "assistente de conversa RAG":**

- Consulte Baseline Foundry Chat Architecture (A6)
- Extraia os pontos de decisão recomendados:
  → Nível de isolamento da rede (totalmente privada ou híbrida?)
  → Método de autenticação (identidade gerenciada, Managed Identity, ou chave de API?)
  → Estratégia de ingestão (indexação por envio, `push`, ou por consulta, `pull`?)
  → Escopo do monitoramento (Application Insights é necessário?)
- Inclua esses pontos naturalmente nas perguntas

**Observações:**

- Extraia da orientação **"pontos a perguntar"**, não "respostas"
- Especificações como SKU/versão da API/região continuam sendo determinadas somente por `azure-dynamic-sources.md`
- Limite de consulta: dois documentos, sem varredura completa

**Itens de confirmação obrigatória:**

- [ ] Nome do projeto (padrão: `azure-project`)
- [ ] Lista de serviços (quais serviços do Azure usar)
- [ ] SKU/camada de cada serviço
- [ ] Método de rede (uso de Private Endpoint)
- [ ] Local da implantação (região)

**Princípios das perguntas:**

- Não repita perguntas sobre informações já mencionadas
- Não pergunte detalhes de implementação ausentes do diagrama (método de indexação, volume de consultas etc.)
- Não faça muitas perguntas de uma vez; pergunte de modo conciso somente os principais itens em aberto
- Para padrões óbvios (por exemplo, PE habilitado), presuma e somente confirme. Porém, o local SEMPRE exige confirmação
- **Ao perguntar sobre SKUs, modelos ou opções, apresente TODAS as opções verificadas no Microsoft Docs e a URL correspondente.** Não filtre opções arbitrariamente

**🔹 Seleção de SKU de VM/recurso: pré-verificação regional obrigatória**

**Antes** de perguntar sobre SKUs de VM ou outro recurso, consulte quais estão realmente disponíveis na região de destino.
Se uma SKU estiver bloqueada por restrições de capacidade regionais, a implantação falhará.

**Método de verificação da SKU de VM:**

```powershell
# Consulta somente SKUs de VM disponíveis sem restrições na região de destino
az vm list-skus --location "<LOCATION>" --size Standard_D2 --resource-type virtualMachines `
  --query "[?restrictions==``[]``].name" -o tsv
```

**Princípios:**

- Não inclua SKUs não verificadas nas opções
- Não recomende "SKUs comuns" de memória. Verifique pela CLI az ou pelo Microsoft Docs
- Inclua somente SKUs verificadas nas opções de `ask_user`
- Mesmo para SKUs informadas, verifique a disponibilidade antes de prosseguir

**Esse princípio se aplica a VMs e a TODOS os recursos sujeitos a restrições de capacidade (Fabric Capacity etc.).**

**🔹 Princípio de exploração de serviços: é proibido "listar de memória"**

Quando houver uma pergunta sobre uma categoria ("Quais opções de Spark existem?", "Quais são as opções de fila de mensagens?") ou for necessário explorar uma funcionalidade:

**NUNCA faça isto:**

- Não consulte e liste somente duas ou três URLs lembradas de memória
- Não afirme definitivamente: "No Azure, X tem A e B"

**FAÇA isto:**

1. **Explore a categoria inteira com web_search**: pesquise no nível da categoria, como `"Azure managed Spark options site:learn.microsoft.com"`, para descobrir os serviços
2. **Compare com o escopo da v1**: verifique se serviços da v1 (Foundry, Fabric, AI Search, ADLS Gen2 etc.) pertencem à categoria. Exemplo: "Spark" → a carga de Engenharia de Dados (Data Engineering) do Microsoft Fabric também oferece Spark
3. **Consulte especificamente as opções descobertas**: busque no Microsoft Docs informações precisas para comparação
4. **Apresente todas as opções**: faça uma comparação abrangente, sem omissões

**Exemplo: pergunta "Quais instâncias de Spark estão disponíveis?":**

```
Abordagem incorreta: consultar somente as URLs de Databricks + Synapse → comparar somente dois
Abordagem correta: web_search("Azure managed Spark options") → descobrir Databricks, Synapse, Fabric Spark e HDInsight
            → verificar a v1: Fabric faz parte do escopo e oferece Spark → DEVE ser incluído
            → consultar cada serviço no Microsoft Docs → apresentar a tabela completa
```

Esse princípio vale para categorias e para solicitações de "alternativas", "outras opções", "comparação" etc.

**🔹 Ferramenta ask_user: uso obrigatório**

Para perguntas com opções, use `ask_user`. A ferramenta permite selecionar com as setas ou digitar uma resposta personalizada.

**Regras de uso de ask_user:**

- Perguntas com duas ou mais opções **DEVEM** usar ask_user (não as liste como texto)
- **Passe `choices` como array de strings (`["A", "B"]`)**. Uma string (`"A, B"`) causa erro
- Coloque a opção recomendada primeiro e acrescente `(Recomendado)`
- Inclua referências nas opções, por exemplo: `"Standard S1 - Recomendada para produção. Ref.: https://..."`
- **Faça somente uma pergunta por chamada**. Para vários itens, chame ask_user sequencialmente
- Há no máximo quatro opções. Se houver cinco ou mais, inclua as três ou quatro mais comuns (também é possível digitar outra)
- Para seleção múltipla, divida em perguntas separadas

**Itens que exigem ask_user:**

- Seleção do local da implantação (região)
- Seleção de SKU/camada
- Seleção de modelo (chat, embedding etc.)
- Seleção do método de rede
- Seleção de assinatura (Fase 1, Etapa 2)
- Seleção de Resource Group (Fase 1, Etapa 3)
- Qualquer outra pergunta que exija uma escolha

**Exemplos de uso:**

```
// O nome do projeto é texto livre; portanto, ask_user não é usado
// SKU, região etc. com opções definidas usam ask_user:

// 1. Pergunta sobre SKU
ask_user({
  question: "Selecione a SKU do AI Search. Ref.: https://learn.microsoft.com/en-us/azure/search/search-sku-tier",
  choices: [
    "Standard S1 - Recomendada para produção (Recomendado)",
    "Basic - Para desenvolvimento/testes, até 15 índices",
    "Standard S2 - Produção com alto tráfego",
    "Free - Avaliação gratuita, 50 MB de armazenamento"
  ]
})

// 2. Pergunta sobre região (chamada separada; somente uma pergunta por chamada)
ask_user({
  question: "Selecione a região do Azure para a implantação. Ref.: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models",
  choices: [
    "Korea Central - Região da Coreia, aceita a maioria dos serviços (Recomendado)",
    "East US - Leste dos EUA, aceita todos os modelos de IA",
    "Japan East - Leste do Japão, próximo da Coreia"
  ]
})
```

> **Observação**: os valores de SKU e região acima são somente ilustrativos. Ao perguntar, componha dinamicamente as opções com as informações mais recentes do Microsoft Docs obtidas por `web_fetch`. Não fixe valores.

**Exemplo: informações insuficientes:**

```
Pessoa: "Quero criar um assistente de conversa RAG com um modelo GPT no Foundry e AI Search."

→ Confirmado: Microsoft Foundry, Azure AI Search
→ Em aberto: nome do projeto, modelo específico, modelo de embedding, rede (PE?), SKU e local

O agente primeiro confirma o nome por ask_user (padrão: rag-chatbot).
Depois oferece opções para cada item em aberto com ask_user.
Inclua URLs do Microsoft Docs nas opções para consulta direta.
```

**🚨🚨🚨 [BLOQUEIO RÍGIDO] Coleta da especificação concluída → geração do diagrama obrigatória 🚨🚨🚨**

**Assim que todos os itens estiverem confirmados, execute as etapas abaixo NA ORDEM. Pular qualquer uma deixa a Fase 1 incompleta.**

1. Componha o **JSON services + JSON connections** com a lista confirmada
2. Use o mecanismo integrado para gerar **`<project-name>/01_arch_diagram_draft.html`**
3. Abra-o automaticamente no navegador com `Start-Process`
4. Apresente-o no **formato de relatório** abaixo, incluindo obrigatoriamente uma **tabela detalhada**
5. Pergunte: **"Você deseja alterar ou adicionar algo?"**
6. Se não houver alterações → passe à transição para a Fase 2 (ask_user com orientação)

**NUNCA faça isto:**

- ❌ Não gerar o diagrama e perguntar: "A arquitetura está confirmada. Podemos seguir?"
- ❌ Adiar a geração para a Fase 2 ou posterior
- ❌ Dizer: "Criarei o diagrama depois"
- ❌ Declarar a arquitetura confirmada somente porque a coleta terminou
- ❌ Gerar o diagrama sem apresentar a tabela de configuração
- ❌ Pular a pergunta sobre alterações e ir diretamente para a Fase 2

**Condição de validação**: não é permitida a entrada na Fase 2 sem gerar `01_arch_diagram_draft.html`.

**Formato do relatório após concluir o diagrama (TODAS as seções são OBRIGATÓRIAS):**

```
## Diagrama de arquitetura

[Link do diagrama interativo, aberto automaticamente no navegador]

### Configuração confirmada

| Serviço | Tipo | SKU/camada | Detalhes |
|---------|------|----------|---------|
| [Nome do serviço] | [Tipo de recurso do Azure] | [SKU] | [Configuração principal: modelo, capacidade etc.] |
| ... | ... | ... | ... |

**Rede**: [VNet + Private Endpoint / pública etc.]
**Local**: [região confirmada]
```

**Após apresentar o relatório, use imediatamente `ask_user` com opções:**

```
ask_user({
  question: "O diagrama de arquitetura e a configuração estão prontos. O que você deseja fazer?",
  choices: [
    "Está correto: seguir para a geração do código Bicep (Recomendado)",
    "Quero modificar a arquitetura",
    "Adicionar mais serviços"
  ]
})
```

- Se escolher "seguir" → passe à transição para a Fase 2 (colete assinatura/RG)
- Se escolher "modificar" ou "adicionar" → aplique as alterações, gere novamente e reapresente

**🚨 A tabela de configuração NÃO é opcional.** Ela permite verificar visualmente o que foi confirmado antes de prosseguir.

### 1-2. Gerar o diagrama HTML interativo

Use o **mecanismo de diagramas integrado** (scripts Python incluídos na habilidade) para criar o HTML interativo.
Não é necessário executar `pip install`, pois os scripts estão em `scripts/` e não exigem rede nem instalação de pacotes.
Mais de 605 ícones oficiais do Azure estão incluídos.

**Convenção de nomes dos diagramas:**

Todos os diagramas são gerados na pasta do projeto Bicep (`<project-name>/`).
Prefixos numerados por estágio organizam os arquivos, sem sobrescrever os anteriores.

| Estágio | Nome do arquivo | Quando é gerado |
|-------|-----------|----------------|
| Rascunho do projeto da Fase 1 | `01_arch_diagram_draft.html` | Ao confirmar o projeto da arquitetura |
| Visualização da análise de alterações (`what-if`) da Fase 4 | `02_arch_diagram_preview.html` | Após validar a análise de alterações |
| Resultado da implantação da Fase 4 | `03_arch_diagram_result.html` | Após concluir a implantação real |

**Descoberta do caminho do módulo integrado e do Python:**

**🚨 Verifique os caminhos do Python e do módulo integrado uma vez no pré-carregamento da Fase 1 e reutilize-os. NÃO repita a descoberta.**

```powershell
# ─── Etapa 1: descoberta do caminho do Python ───
# ⚠️ Get-Command python pode encontrar o atalho da Windows Store; por isso, primeiro pesquisa no sistema de arquivos
$PythonCmd = $null

# Prioridade 1: descoberta direta do caminho real de instalação (mais confiável)
$PythonExe = Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notlike '*WindowsApps*' } |
  Select-Object -First 1 -ExpandProperty FullName
if ($PythonExe) { $PythonCmd = $PythonExe }

# Prioridade 2: pesquisa em Program Files
if (-not $PythonCmd) {
  $PythonExe = Get-ChildItem -Path "$env:ProgramFiles\Python*", "$env:ProgramFiles(x86)\Python*" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue |
    Select-Object -First 1 -ExpandProperty FullName
  if ($PythonExe) { $PythonCmd = $PythonExe }
}

# Prioridade 3: pesquisa no PATH (somente se não for um atalho da Windows Store)
if (-not $PythonCmd) {
  foreach ($cmd in @('python3', 'py')) {
    $found = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($found -and $found.Source -notlike '*WindowsApps*') { $PythonCmd = $cmd; break }
  }
}

if (-not $PythonCmd) {
  Write-Host ""
  Write-Host "O Python não está instalado ou não foi encontrado no PATH." -ForegroundColor Red
  Write-Host ""
  Write-Host "Instale-o por um destes métodos:" -ForegroundColor Yellow
  Write-Host "  1. winget install Python.Python.3.12"
  Write-Host "  2. Baixe em https://www.python.org/downloads/"
  Write-Host "  3. Pesquise 'Python 3.12' na Microsoft Store e instale"
  Write-Host ""
  Write-Host "Após instalar, reinicie o terminal e tente novamente."
  return
}

# ─── Etapa 2: descoberta do caminho do script integrado (sem pip install) ───
# Prioridade 1: pasta local do skill no projeto
$ScriptsDir = Get-ChildItem -Path ".github\skills\azure-architecture-autopilot" -Filter "cli.py" -Recurse -ErrorAction SilentlyContinue |
  Where-Object { $_.Directory.Name -eq 'scripts' } |
  Select-Object -First 1 -ExpandProperty DirectoryName
# Prioridade 2: pasta global do skill
if (-not $ScriptsDir) {
  $ScriptsDir = Get-ChildItem -Path "$env:USERPROFILE\.copilot\skills\azure-architecture-autopilot" -Filter "cli.py" -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Directory.Name -eq 'scripts' } |
    Select-Object -First 1 -ExpandProperty DirectoryName
}

# ─── Etapa 3: geração do diagrama (método CLI, execução direta do script) ───
$OutputFile = "<project-name>\01_arch_diagram_draft.html"

& $PythonCmd "$ScriptsDir\cli.py" `
  --services '<services_JSON>' `
  --connections '<connections_JSON>' `
  --title "Título da arquitetura" `
  --vnet-info "10.0.0.0/16 | pe-subnet: 10.0.1.0/24" `
  --output $OutputFile

# Abre automaticamente no navegador após gerar
Start-Process $OutputFile
```

**O método da interface de programação de aplicações (API) Python também está disponível (alternativa):**

Quando o JSON for muito grande, chame diretamente a API Python para evitar o limite dos argumentos da CLI.
Adicione a pasta scripts a `sys.path` para importar o módulo integrado:

```python
import sys, os
# Adiciona a pasta scripts ao caminho do Python (usa o módulo integrado sem pip install)
scripts_dir = r"<absolute path to scripts folder>"  # Valor de $ScriptsDir encontrado na Etapa 2
sys.path.insert(0, scripts_dir)

from generator import generate_diagram

services = [...]   # JSON services
connections = [...] # JSON connections

html = generate_diagram(
    services=services,
    connections=connections,
    title="Título da arquitetura",
    vnet_info="10.0.0.0/16 | pe-subnet: 10.0.1.0/24",
    hierarchy=None  # Usado somente com várias assinaturas/RGs
)

with open("<project-name>/01_arch_diagram_draft.html", "w", encoding="utf-8") as f:
    f.write(html)
```

**🔹 Critérios para escolher entre a interface de linha de comando (CLI) e a API Python:**

| Cenário | Método | Motivo |
|----------|--------|--------|
| Dez serviços ou menos | CLI (`python scripts/cli.py`) | Simples e rápido |
| Mais de dez serviços ou uso de hierarquia | API Python (adição a sys.path) | Evita o limite de tamanho dos argumentos da CLI |
| Diagramas com várias assinaturas/RGs | API Python + parâmetro `hierarchy` | Representa a estrutura hierárquica |

**Lista completa dos tipos de serviço compatíveis:**

Disponível nos arquivos de referência integrados em `references/`.
Os valores aceitos aparecem abaixo, na seção de formato do JSON `services`.

> **Ordem da geração**: (1) verificar o caminho do Python → (2) verificar o caminho do módulo integrado → (3) compor o JSON services/connections → (4) executar. Se o Python não estiver instalado, oriente a instalação antes de compor o JSON.

> **🚨 Abertura automática do diagrama (sem exceções)**: todo HTML gerado pelo mecanismo integrado **DEVE** ser aberto no navegador. Sempre execute `Start-Process` ao gerar novamente um diagrama. A geração e a abertura ocorrem juntas no mesmo bloco do PowerShell.
>
> **Quando isso se aplica (inclui, mas não se limita a todos estes casos):**
>
> - Rascunho do projeto da Fase 1 (`01_arch_diagram_draft.html`)
> - Nova geração após a Confirmação das Alterações
> - Visualização da análise de alterações (`what-if`) da Fase 4 (`02_arch_diagram_preview.html`)
> - Resultado da implantação da Fase 4 (`03_arch_diagram_result.html`)
> - Alterações após a implantação (`04_arch_diagram_update_draft.html`)
> - Qualquer outro caso de nova geração do diagrama

**Formato do JSON services:**

Composto dinamicamente com base na lista confirmada de serviços. Estrutura:

```json
[
  {"id": "uniqueID", "name": "Nome de exibição do serviço", "type": "iconType", "sku": "SKU", "private": true/false,
   "details": ["Linha de detalhe 1", "Linha de detalhe 2"]}
]
```

| Campo | Obrigatório | Tipo | Descrição |
|-------|----------|------|-------------|
| `id` | Sim | string | Identificador exclusivo (formato kebab-case) |
| `name` | Sim | string | Nome exibido no diagrama |
| `type` | Sim | string | Tipo do serviço (selecione na lista abaixo) |
| `sku` | | string | Informações de SKU/camada |
| `private` | | boolean | Endpoint privado (Private Endpoint) conectado (padrão: false) |
| `details` | | string[] | Informações adicionais da barra lateral |
| `subscription` | | string | Nome da assinatura (obrigatório com hierarquia) |
| `resourceGroup` | | string | Nome do grupo de recursos (obrigatório com hierarquia) |

**Tipo de serviço: referência canônica**

> ⚠️ **CRÍTICO**: sempre use o **tipo canônico** da tabela. NÃO use nomes de recursos ARM do Azure (por exemplo, `private_endpoints`, `storage_accounts`, `data_factories`). O gerador normaliza variantes comuns, mas os tipos canônicos garantem ícones, detecção de PE e cores corretos.

| Categoria | Tipo canônico | Recurso do Azure | Ícone |
|----------|---------------|----------------|------|
| **IA** | `ai_foundry` | Microsoft.CognitiveServices/accounts (kind: AIServices) | AI Foundry |
| | `openai` | Microsoft.CognitiveServices/accounts (kind: OpenAI) | Azure OpenAI |
| | `ai_hub` | Foundry Project | AI Studio |
| | `search` | Microsoft.Search/searchServices | Cognitive Search |
| | `document_intelligence` | Microsoft.CognitiveServices/accounts (kind: FormRecognizer) | Form Recognizer |
| | `aml` | Microsoft.MachineLearningServices/workspaces | Machine Learning |
| **Dados** | `fabric` | Microsoft.Fabric/capacities | Microsoft Fabric |
| | `adf` | Microsoft.DataFactory/factories | Data Factory |
| | `storage` | Microsoft.Storage/storageAccounts | Storage Account |
| | `adls` | ADLS Gen2 (Storage with HNS) | Data Lake |
| | `cosmos_db` | Microsoft.DocumentDB/databaseAccounts | Cosmos DB |
| | `sql_database` | Microsoft.Sql/servers/databases | SQL Database |
| | `sql_server` | Microsoft.Sql/servers | SQL Server |
| | `databricks` | Microsoft.Databricks/workspaces | Databricks |
| | `synapse` | Microsoft.Synapse/workspaces | Synapse Analytics |
| | `redis` | Microsoft.Cache/redis | Redis Cache |
| | `stream_analytics` | Microsoft.StreamAnalytics/streamingjobs | Stream Analytics |
| | `postgresql` | Microsoft.DBforPostgreSQL/flexibleServers | PostgreSQL |
| | `mysql` | Microsoft.DBforMySQL/flexibleServers | MySQL |
| **Segurança** | `keyvault` | Microsoft.KeyVault/vaults | Key Vault |
| | `sentinel` | Microsoft.SecurityInsights | Sentinel |
| **Computação** | `appservice` | Microsoft.Web/sites | App Service |
| | `function_app` | Microsoft.Web/sites (kind: functionapp) | Function App |
| | `vm` | Microsoft.Compute/virtualMachines | Virtual Machine |
| | `aks` | Microsoft.ContainerService/managedClusters | AKS |
| | `acr` | Microsoft.ContainerRegistry/registries | Container Registry |
| | `container_apps` | Microsoft.App/containerApps | Container Apps |
| | `static_web_app` | Microsoft.Web/staticSites | Static Web App |
| | `spring_apps` | Microsoft.AppPlatform/Spring | Spring Apps |
| **Rede** | `pe` | Microsoft.Network/privateEndpoints | Private Endpoint |
| | `vnet` | Microsoft.Network/virtualNetworks | VNet |
| | `nsg` | Microsoft.Network/networkSecurityGroups | NSG |
| | `firewall` | Microsoft.Network/azureFirewalls | Firewall |
| | `bastion` | Microsoft.Network/bastionHosts | Bastion |
| | `app_gateway` | Microsoft.Network/applicationGateways | App Gateway |
| | `front_door` | Microsoft.Cdn/profiles (Front Door) | Front Door |
| | `vpn` | Microsoft.Network/virtualNetworkGateways | VPN Gateway |
| | `load_balancer` | Microsoft.Network/loadBalancers | Load Balancer |
| | `nat_gateway` | Microsoft.Network/natGateways | NAT Gateway |
| | `cdn` | Microsoft.Cdn/profiles | CDN |
| **IoT** | `iot_hub` | Microsoft.Devices/IotHubs | IoT Hub |
| | `digital_twins` | Microsoft.DigitalTwins/digitalTwinsInstances | Digital Twins |
| **Integração** | `event_hub` | Microsoft.EventHub/namespaces | Event Hub |
| | `event_grid` | Microsoft.EventGrid/topics | Event Grid |
| | `apim` | Microsoft.ApiManagement/service | API Management |
| | `service_bus` | Microsoft.ServiceBus/namespaces | Service Bus |
| | `logic_apps` | Microsoft.Logic/workflows | Logic Apps |
| **Monitoramento** | `log_analytics` | Microsoft.OperationalInsights/workspaces | Log Analytics |
| | `appinsights` | Microsoft.Insights/components | App Insights |
| | `monitor` | Azure Monitor | Monitor |
| **Outros** | `jumpbox`, `user`, `devops` | — | Especial |

**Ao usar Private Endpoints: nó de PE obrigatório**

Se houver Private Endpoints, adicione obrigatoriamente um nó de PE ao JSON `services` para cada serviço. Inclua também os vínculos de PE em `connections`.

```json
// Adiciona o nó de PE correspondente a cada serviço
{"id": "pe_serviceID", "name": "PE: NomeDoServiço", "type": "pe", "details": ["groupId: groupIDCorrespondente"]}

// Adiciona a conexão serviço → PE em connections
{"from": "serviceID", "to": "pe_serviceID", "label": "", "type": "private"}
```

**🚨🚨🚨 Conexões de PE e de lógica de negócio são distintas: inclua AMBAS 🚨🚨🚨**

Conexões de PE (`"type": "private"`) representam o isolamento de rede, mas NÃO mostram o **fluxo de dados/chamadas de API** real entre serviços.

**Inclua os dois tipos de conexão:**

1. **Conexões de lógica de negócio**: fluxo real entre serviços (tipos api, data e security)
2. **Conexões de PE**: isolamento de rede entre serviço ↔ PE (tipo private)

```json
// ✅ Exemplo correto: Function App → Foundry
// 1) Lógica de negócio: Function App chama Foundry para bate-papo/incorporação vetorial
{"from": "func_app", "to": "foundry", "label": "Bate-papo RAG + incorporação vetorial", "type": "api"}
// 2) Conexão de PE: Private Endpoint do Foundry
{"from": "foundry", "to": "pe_foundry", "label": "", "type": "private"}

// ❌ Exemplo incorreto: somente conexão de PE, sem conexão de lógica de negócio
{"from": "foundry", "to": "pe_foundry", "label": "", "type": "private"}
// → Sem linha entre Function App e Foundry; o fluxo da arquitetura não fica visível
```

**NUNCA faça isto:**

- Não crie somente conexões de PE omitindo as de lógica de negócio
- Não conecte `from`/`to` da lógica de negócio aos nós de PE (use o **ID real do serviço**, não o PE)
- Não presuma que "a linha aparecerá porque o PE existe"

O `groupId` do PE varia por serviço. Consulte a tabela de mapeamento em `references/service-gotchas.md`.

> **Convenção de nomes dos serviços**: use os nomes oficiais mais recentes do Azure. Em caso de dúvida, consulte o Microsoft Docs.
> Para tipos e propriedades principais, consulte `references/ai-data.md`.

**Formato do JSON connections:**

```json
[
  {"from": "serviceA_ID", "to": "serviceB_ID", "label": "Descrição da conexão", "type": "api|data|security|private"}
]
```

**Tipos de conexão:**

| type | Cor | Estilo | Uso |
|------|-------|-------|---------|
| `api` | Azul | Sólido | Chamadas de API, consultas |
| `data` | Verde | Sólido | Fluxo de dados, indexação |
| `security` | Laranja | Tracejado | Segredos, autenticação |
| `private` | Roxo | Tracejado | Conexões de Private Endpoint |
| `network` | Cinza | Sólido | Roteamento de rede |
| `default` | Cinza | Sólido | Outros |

**🔹 Princípio multilíngue do diagrama:**

- `name`, `details` em services e `label` em connections são escritos **no idioma da pessoa**
- Exemplo: `"label": "Pesquisa RAG"`, `"label": "Ingestão de dados"`
- Nomes oficiais dos serviços do Azure (Microsoft Foundry, AI Search etc.) permanecem no idioma oficial

**🔹 Nó da VNet: NÃO adicionar ao JSON services**

- A VNet aparece automaticamente como **limite roxo tracejado** (quando há PEs)
- Adicionar um nó separado de VNet a services duplica o limite e causa confusão
- O rótulo do limite na barra lateral apresenta as informações necessárias (CIDR e sub-redes)

Forneça o caminho completo do arquivo HTML gerado.

### 1-3. Finalizar a arquitetura pela conversa

A arquitetura é finalizada incrementalmente. Ao receber alterações, NÃO repita todas as perguntas. **Aplique somente as alterações ao estado confirmado** e gere o diagrama novamente.

**⚠️ Regra de Confirmação das Alterações: verificação obrigatória ao adicionar/alterar serviços**

Adicionar ou alterar um serviço não é uma "atualização simples". Isso **reabre os campos obrigatórios em aberto desse serviço**.

**Processo:**

1. Compare o estado confirmado com a nova solicitação
2. Identifique os campos obrigatórios dos novos serviços (`domain-packs` ou Microsoft Docs)
3. Consulte no Microsoft Docs a disponibilidade/opções regionais
4. Se houver campos em aberto, **pergunte primeiro por ask_user**
5. **Gere novamente somente após concluir a confirmação**

**NUNCA faça isto:**

- Não finalize a atualização com campos obrigatórios em aberto
- Não adicione arbitrariamente subcomponentes/cargas não mencionados (por exemplo, OneLake e fluxo de dados a uma solicitação do Fabric)
- Não presuma vagamente SKU/modelo, como "SKU F", sem confirmação

**Não repita perguntas sobre serviços já confirmados.** Confirme somente itens em aberto dos serviços adicionados/alterados.

---

**🚨🚨🚨 [Princípio prioritário] Verificação imediata de fatos durante o projeto 🚨🚨🚨**

**A Fase 1 confirma uma "arquitetura viável".**
**Antes de refletir qualquer solicitação no diagrama, verifique se ela é possível consultando diretamente o Microsoft Docs por `web_fetch`.**

**Direcionamento do projeto versus especificações de implantação: caminhos separados**

| Tipo de decisão | Caminho de referência | Exemplos |
|--------------|----------------|----------|
| **Direcionamento do projeto** (padrões, práticas recomendadas, combinações) | `references/architecture-guidance-sources.md` → consulta específica | "Qual é a estrutura RAG recomendada?", "Qual é a linha de base empresarial?" |
| **Especificações de implantação** (versão da API, SKU, região, modelo, PE) | `references/azure-dynamic-sources.md` → Microsoft Docs | "Qual é a versão da API?", "Este modelo está disponível em Korea Central?" |

- **O direcionamento vem da orientação de arquitetura; os valores reais vêm das fontes dinâmicas.** Não misture os caminhos.
- NÃO use orientação de arquitetura para determinar SKU, versão da API ou região.
- **NÃO percorra todos os subdocumentos do Architecture Center.** Consulte especificamente no máximo dois documentos relevantes.
- Consulte gatilhos, limites e regras em `architecture-guidance-sources.md`.

**Esse princípio se aplica a TODAS as solicitações:**

- Adicionar/alterar modelo → verifique existência e disponibilidade regional
- Adicionar/alterar serviço → verifique disponibilidade regional
- Alterar SKU → verifique validade e suporte às funcionalidades
- Solicitar funcionalidade → verifique se há suporte
- Combinar serviços → verifique a possibilidade de integração
- **Qualquer outra solicitação** → verifique no Microsoft Docs

**Resultados da verificação no Microsoft Docs:**

- **Possível** → reflita no diagrama
- **Impossível** → explique imediatamente e sugira alternativas disponíveis

**Processo de verificação de fatos: validação cruzada obrigatória**

Não faça somente uma consulta.
**Sempre faça validação cruzada com outras páginas/fontes do Microsoft Docs.**

> **Restrição do ambiente GHCP**: subagentes (explore/task/general-purpose) NÃO têm `web_fetch`/`web_search`.
> Portanto, o agente principal DEVE fazer **diretamente** as verificações no Microsoft Docs.

```
[1ª verificação] O agente principal consulta diretamente a página principal pelo web_fetch
    ↓
[2ª verificação] O agente principal consulta outra página relacionada para validação cruzada
    - Exemplo, disponibilidade do modelo → 1ª: modelos / 2ª: disponibilidade regional ou preços
    - Exemplo, versão da API → 1ª: referência do Bicep / 2ª: referência da API REST
    - Compare os resultados e sinalize divergências
    ↓
[Consolidação] Se as verificações coincidirem, responda
    - Se divergirem: resolva com consultas adicionais ou informe claramente a incerteza
```

**Padrões de qualidade da verificação: seja minucioso**

- Ao consultar uma página, **verifique TODAS as seções, guias e condições relevantes**
- Para modelos, verifique **TODOS os tipos de implantação**, incluindo Global Standard, Standard, Provisioned, Data Zone etc. Não conclua "sem suporte" com base em somente um tipo
- Para SKUs, verifique **integralmente** as funcionalidades compatíveis
- Em páginas grandes, consulte as seções relevantes **várias vezes**
- Em caso de dúvida, consulte outras páginas. **NUNCA responda por suposição**

**NUNCA faça isto:**

- Não adicione ao diagrama sem verificar
- Não adie com "verificarei durante a geração do Bicep" ou "será validado na implantação"
- Não dependa da memória nem diga "deve funcionar". **Consulte diretamente o Microsoft Docs**
- Não conclua após leitura parcial
- Não finalize com uma só consulta. **Faça validação cruzada**

**🚫 Regras de uso de subagentes:**

**Subagentes no GHCP = ferramenta `task`:**

- `agent_type: "explore"`: tarefas somente leitura, como explorar código e pesquisar arquivos (**sem web_fetch/web_search**)
- `agent_type: "task"`: execução de comandos como CLI az e bicep build
- `agent_type: "general-purpose"`: tarefas de alto nível, como geração complexa de Bicep

> **⚠️ Restrição dos subagentes**: NENHUM subagente pode usar `web_fetch` ou `web_search`.
> O agente principal DEVE fazer diretamente consultas ao Microsoft Docs, versões da API, disponibilidade de modelos etc.

**Critérios para primeiro plano versus segundo plano:**

- **Se o resultado for necessário antes da próxima etapa → `mode: "sync"` (padrão)**
  - Exemplo: consultar SKUs antes de oferecer opções; verificar o modelo antes do diagrama
  - Executar em segundo plano deixaria a pessoa aguardando sem atividade
- **Se houver outro trabalho independente durante a espera → `mode: "background"`**
  - Exemplo: consultar simultaneamente várias páginas para validação cruzada

**Execute a maioria das verificações em primeiro plano (`mode: "sync"`)**, pois o resultado é necessário à próxima pergunta.

**Como fazer validação cruzada em paralelo:**

```
// Executa a 1ª e a 2ª verificação simultaneamente (diretamente pelo agente principal)
[Simultaneamente] Consulta a página principal pelo web_fetch (1ª)
[Simultaneamente] Consulta outra página relacionada pelo web_fetch (2ª)
// Compara os resultados e procura divergências
// Exemplo: disponibilidade do modelo → páginas de modelos + disponibilidade regional em paralelo
```

**NUNCA faça isto:**

- Não execute em segundo plano se o resultado for necessário e depois fique ocioso
- Não delegue web_fetch/web_search a subagentes
- Não tente ler diretamente arquivos internos dos subagentes

---

**⚠️ Importante: NÃO execute comandos no interpretador de comandos até haver aprovação explícita para a próxima etapa.**
Consultas ao Microsoft Docs por `web_fetch` são a única exceção.

Após confirmar a arquitetura (sem alterações no diagrama), pergunte se deve seguir.

**🚨 Pré-requisitos da transição para a Fase 2: TODOS devem ser atendidos antes da pergunta**

1. `01_arch_diagram_draft.html` foi **gerado** com o mecanismo integrado
2. O diagrama foi **aberto no navegador** e **apresentado** no relatório com a **tabela de configuração**
3. Foi feita a pergunta **"Você deseja alterar ou adicionar algo?"**, sem alterações pendentes, e houve **confirmação final**

**Se QUALQUER condição não for atendida, NÃO siga para a Fase 2.**
Se o diagrama não existir, **gere-o agora** conforme 1-2.
Se a tabela não tiver sido apresentada, **apresente-a agora** antes de perguntar sobre alterações.

**Conforme o pré-carregamento paralelo, execute `az account list` e `az group list` com ask_user para preparar previamente as opções de assinatura/RG.**

```
// Chama simultaneamente na mesma resposta:
[1] ask_user: "A arquitetura está confirmada! Podemos seguir?"
[2] powershell: az account show 2>&1              (verifica previamente o login)
[3] powershell: az account list --output json      (prepara opções de assinatura)
[4] powershell: az group list --output json        (prepara opções de grupo de recursos)
```

Formato de exibição de ask_user:

```
A arquitetura está confirmada! Podemos seguir?

✅ Arquitetura confirmada: [resumo]

As próximas etapas são:
1. [Geração de código Bicep]: a IA escreve o código IaC automaticamente
2. [Revisão de código]: revisão automática de segurança e práticas recomendadas
3. [Implantação no Azure]: criação real dos recursos (opcional)

Podemos seguir? Se quiser somente o código, sem implantação, informe.
```

Após a aprovação, colete as informações nesta ordem.
**Como `az account show` + `az account list` + `az group list` já foram executados, apresente imediatamente as opções de assinatura/RG.**

**Etapa 1: verificar a autenticação no Azure**

O resultado de `az account show` já está disponível. Não faça outra chamada.

- Se houver autenticação → siga para a Etapa 2
- Se não houver autenticação → oriente:

  ```
  É necessário entrar pela CLI do Azure. Execute este comando no terminal:
  az login
  Informe quando terminar.
  ```

**Etapa 2: selecionar a assinatura**

O resultado de `az account list` já está disponível. Não faça outra chamada.

Ofereça até quatro assinaturas como opções de `ask_user`.
Se houver cinco ou mais, inclua as três ou quatro mais usadas (também é possível digitar outra).
Após a seleção, execute `az account set --subscription "<ID>"`.

**Etapa 3: confirmar o grupo de recursos**

O resultado de `az group list` já está disponível. Não faça outra chamada.

Ofereça até quatro grupos de recursos existentes como opções de `ask_user`.
Use um grupo existente sem alterações. Se for informado um nome novo, crie-o na implantação da Fase 4.

**Itens de confirmação obrigatória:**

- [ ] Lista de serviços e SKUs
- [ ] Método de rede (uso de Private Endpoint)
- [ ] ID da assinatura (confirmado na Etapa 2)
- [ ] Nome do grupo de recursos (confirmado na Etapa 3)
- [ ] Local (confirmado e com disponibilidade regional verificada no Microsoft Docs)

---

## 🚨 Lista de conclusão da Fase 1: verificação obrigatória antes da Fase 2

Antes de sair da Fase 1, verifique **TODOS** os itens. Se algum estiver incompleto, NÃO siga.

| Nº | Item | Método de verificação |
|---|------|---------------------|
| 1 | Especificações obrigatórias confirmadas | Nome, serviços, SKUs, região e rede confirmados |
| 2 | Fatos verificados | Validação cruzada feita no Microsoft Docs |
| 3 | **Diagrama gerado** | `01_arch_diagram_draft.html` gerado com o mecanismo integrado |
| 4 | **Tabela apresentada** | Tabela detalhada de Serviço/Tipo/SKU/Detalhes no relatório |
| 5 | **Diagrama revisado** | Abertura no navegador + relatório + pergunta sobre alterações |
| 6 | Aprovação final | Confirmação sem alterações e seleção para seguir |

**⚠️ NÃO pergunte o item 6 enquanto os itens 3 a 5 estiverem incompletos.** Fluxo: diagrama → tabela → alterações → confirmação → próxima etapa.

---

## Encaminhamento à Fase 2: agente gerador de Bicep

Após a aprovação, leia `references/bicep-generator.md` e gere o modelo Bicep.
Como alternativa, delegue a um subagente.

**Princípio de tratamento de informações confidenciais (NUNCA viole):**

- NUNCA peça senhas de VM, chaves de API ou outros valores confidenciais no chat e NUNCA os armazene nos parâmetros
- Se a revisão encontrar valores confidenciais em texto não criptografado em `main.bicepparam`, remova-os imediatamente

**🔹 Valores confidenciais informados, como senhas de VM: validação de complexidade obrigatória**

Ao receber uma senha administrativa de VM ou semelhante, valide a complexidade **antes** de enviá-la ao Azure.
As VMs do Azure devem atender a TODAS as condições:

- 12 caracteres ou mais
- Conter pelo menos três destes grupos: maiúsculas, minúsculas, números e caracteres especiais

**Se a validação falhar:** NÃO tente implantar; peça imediatamente outra senha:
> **⚠️ A senha não atende aos requisitos de complexidade do Azure.** Ela deve ter pelo menos 12 caracteres e conter três destes grupos: maiúsculas, minúsculas, números e caracteres especiais.

**NUNCA faça isto:**

- Não avise apenas que "talvez não atenda" e tente implantar. **BLOQUEIE**
- Não envie ao Azure sem validar a complexidade

**🚨 Princípio de compatibilidade entre parâmetros `@secure()` e `.bicepparam`:**

Quando `.bicepparam` tem a diretiva `using './main.bicep'`, NÃO é possível usar opções `--parameters` adicionais com `az deployment group what-if/create`.
Portanto, trate parâmetros `@secure()` assim:

1. **Parâmetros `@secure()` DEVEM ter valores padrão**: use funções Bicep como `newGuid()` e `uniqueString()`

   ```bicep
   @secure()
   param sqlAdminPassword string = newGuid()  // Gerado automaticamente na implantação; armazene no Key Vault se necessário
   ```

2. **Se houver parâmetros `@secure()` que exigem valores informados:**
   - NÃO use `.bicepparam`; combine `--template-file` + `--parameters`
   - Ou gere um arquivo JSON separado (`main.parameters.json`)

   ```powershell
   # Quando .bicepparam não puder ser usado, substitua-o por um arquivo de parâmetros JSON
   az deployment group what-if `
     --template-file main.bicep `
     --parameters main.parameters.json `
     --parameters sqlAdminPassword='user-input-value'
   ```

3. **NÃO use `.bicepparam` e `--parameters` simultaneamente no comando de implantação**

   ```
   ❌ az deployment group create --parameters main.bicepparam --parameters key=value
   ✅ az deployment group create --parameters main.bicepparam
   ✅ az deployment group create --template-file main.bicep --parameters main.parameters.json --parameters key=value
   ```

**Critérios de decisão:**

- Todos os parâmetros `@secure()` têm valores padrão (`newGuid` etc.) → pode usar `.bicepparam`
- Algum parâmetro `@secure()` exige entrada → use JSON em vez de `.bicepparam`

**Quando a consulta ao Microsoft Docs falhar:**

- Se `web_fetch` falhar por limite de taxa etc., informe:

  ```
  ⚠️ Falha ao consultar a versão da API no Microsoft Docs. Será usada a última versão estável conhecida.
  Recomenda-se confirmar a versão mais recente antes da implantação.
  Deseja continuar?
  ```

- NÃO prossiga silenciosamente com uma versão fixa sem aprovação

**Referências anteriores à geração do Bicep:**

- `references/service-gotchas.md`: propriedades obrigatórias, erros comuns e mapeamento de `groupId` de PE/DNS Zone
- `references/ai-data.md`: guia de serviços de IA/dados (domínio v1)
- `references/azure-common-patterns.md`: padrões de PE, segurança e nomenclatura
- `references/azure-dynamic-sources.md`: registro de URLs do Microsoft Docs
- Para outros serviços, consulte diretamente o Microsoft Docs para verificar tipos, propriedades e PEs

**Estrutura de saída:**

```
<project-name>/
├── main.bicep              # Orquestração principal
├── main.bicepparam         # Parâmetros (valores específicos do ambiente)
└── modules/
    ├── network.bicep       # VNet, Subnet (inclui sub-rede de Private Endpoint)
    ├── ai.bicep            # Serviços de IA (conforme os requisitos)
    ├── storage.bicep       # ADLS Gen2 (isHnsEnabled: true)
    ├── fabric.bicep        # Microsoft Fabric (se necessário)
    ├── keyvault.bicep      # Key Vault
    └── private-endpoints.bicep  # Todos os PEs + DNS Zones
```

**Princípios obrigatórios do Bicep:**

- Parametrize todos os nomes: `param openAiName string = 'oai-${uniqueString(resourceGroup().id)}'`
- Serviços privados DEVEM ter `publicNetworkAccess: 'Disabled'`
- Defina `privateEndpointNetworkPolicies: 'Disabled'` em pe-subnet
- Private DNS Zone + VNet Link + DNS Zone Group: os três são obrigatórios
- Com Microsoft Foundry, **crie também o Foundry Project (`accounts/projects`)**; sem ele, o portal não funciona
- ADLS Gen2 DEVE ter `isHnsEnabled: true` (a omissão cria Blob Storage comum)
- Armazene segredos no Key Vault e referencie-os por parâmetros `@secure()`
- Adicione comentários em português do Brasil que expliquem a finalidade de cada seção

Após concluir a geração, passe imediatamente à Fase 3.

---

## Encaminhamento à Fase 3: agente revisor de Bicep

Revise conforme `references/bicep-reviewer.md`.

**⚠️ Ponto principal: NÃO faça somente inspeção visual e declare aprovação. Execute `az bicep build` para verificar a compilação real.**

```powershell
az bicep build --file main.bicep 2>&1
```

1. Erros/avisos de compilação → corrija
2. Lista de verificação → corrija
3. Compile novamente
4. Relate os resultados, incluindo a compilação

Consulte as listas e os procedimentos detalhados em `references/bicep-reviewer.md`.

Após a revisão, apresente os resultados antes da Fase 4 e **oriente as próximas etapas**.

**🚨 Formato obrigatório do relatório ao concluir a Fase 3:**

```
## Revisão do código Bicep concluída

[Resumo da revisão no formato da Etapa 6 de bicep-reviewer.md]

---

**Próxima etapa: Fase 4 (implantação no Azure)**

Revisão concluída. As próximas etapas são:
1. **Análise de alterações (`what-if`)**: visualiza os recursos planejados sem alterações reais
2. **Diagrama de visualização**: arquitetura baseada no resultado da análise de alterações (`02_arch_diagram_preview.html`)
3. **Implantação real**: cria os recursos no Azure após a confirmação

Prosseguir com a implantação? Se quiser somente o código, informe.
```

**NUNCA faça isto:**

- Não conclua a Fase 3 fornecendo apenas `az deployment group create`, sem orientação
- Não implante diretamente sem análise de alterações nem peça que a pessoa execute os comandos
- Não pule as etapas da Fase 4 (análise de alterações → diagrama de visualização → implantação)
