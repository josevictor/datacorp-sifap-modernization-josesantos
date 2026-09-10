# Fontes de orientação de arquitetura (para decisões de direcionamento do projeto)

Registro de fontes para usar a orientação oficial de arquitetura do Azure **somente em decisões de direcionamento do projeto**.

> **As URLs deste documento indicam onde pesquisar.**
> Não trate o conteúdo dessas URLs como fatos fixos.
> Não as use para decidir SKU, versão da API, região, disponibilidade de modelos ou mapeamento de PE. Essas decisões usam exclusivamente `azure-dynamic-sources.md`.

---

## Separação por finalidade

| Finalidade | Documento | Itens que podem ser decididos |
|---------|----------------|-----------------|
| **Decisões de direcionamento do projeto** | Este documento (architecture-guidance-sources) | Padrões de arquitetura, práticas recomendadas, direcionamento da combinação de serviços e projeto dos limites de segurança |
| **Verificação das especificações de implantação** | `azure-dynamic-sources.md` | Versão da API, SKU, região, disponibilidade de modelos, `groupId` de PE e valores reais das propriedades |

**O que NÃO pode ser decidido com este documento:**

- Versão da API
- Nomes/preços de SKUs
- Disponibilidade regional
- Nomes/versões/tipos de implantação de modelos
- Mapeamento de `groupId` de PE / DNS Zone
- Valores específicos das propriedades dos recursos

---

## Fontes principais

Destinos de consulta específica para decisões de direcionamento do projeto.

| ID | Documento | URL | Finalidade |
|----|----------|-----|---------|
| A1 | Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/ | Central de entrada para encontrar documentos específicos de cada domínio |
| A2 | Well-Architected Framework | https://learn.microsoft.com/en-us/azure/architecture/framework/ | Princípios de segurança, confiabilidade, desempenho, custo e operações |
| A3 | Cloud Adoption Framework / Landing Zone | https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/ | Governança empresarial, topologia de rede e estrutura de assinaturas |
| A4 | Arquitetura de IA/ML do Azure | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/ | Central de arquiteturas de referência para cargas de trabalho de IA/ML |
| A5 | Arquitetura de referência básica de chat do Foundry | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/basic-azure-ai-foundry-chat | Estrutura básica de assistente de conversa baseada no Foundry |
| A6 | Arquitetura de referência de linha de base para chat do AI Foundry | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-openai-e2e-chat | Linha de base empresarial para assistente de conversa do Foundry (inclui isolamento de rede) |
| A7 | Guia de projeto de soluções RAG | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide | Guia de projeto do padrão RAG |
| A8 | Visão geral do Microsoft Fabric | https://learn.microsoft.com/en-us/fabric/get-started/microsoft-fabric-overview | Visão geral da plataforma Fabric e compreensão das cargas de trabalho |
| A9 | Governança/adoção do Fabric | https://learn.microsoft.com/en-us/power-bi/guidance/fabric-adoption-roadmap-governance | Governança e roteiro de adoção do Fabric |

## Fontes secundárias (somente para acompanhamento)

Não são destinos de consulta direta. Use-as somente para acompanhar alterações.

| Documento | URL | Observações |
|----------|-----|-------|
| Azure Updates | https://azure.microsoft.com/en-us/updates/ | Alterações de serviços e anúncios de novas funcionalidades. Não é destino de consulta específica |

---

## Gatilho de consulta: quando pesquisar

Os documentos de orientação de arquitetura **não são consultados em toda solicitação**. Faça consultas específicas somente quando os gatilhos abaixo se aplicarem.

### Condições de gatilho

0. **Quando o tipo de carga de trabalho é identificado na Fase 1 (automático)**
   - Consulte previamente a arquitetura de referência relevante para ajustar a profundidade das perguntas.
   - O gatilho é automático, mesmo sem menção a "prática recomendada" etc.
   - Finalidade: incluir nas perguntas os pontos de decisão baseados na arquitetura oficial, além de especificações de SKU/região.
1. **Quando a pessoa pede uma justificativa para o direcionamento do projeto**
   - Palavras-chave como "prática recomendada", "arquitetura de referência", "estrutura recomendada", "linha de base", "bem arquitetada", "zona de destino (landing zone)" e "padrão empresarial".
2. **Quando os limites de arquitetura de uma nova combinação de serviços são ambíguos**
   - Relações entre serviços que não podem ser determinadas pelos arquivos de referência ou por service-gotchas.
3. **Quando é necessário projetar segurança/governança empresarial**
   - Estrutura de assinaturas, topologia de rede e padrões de zona de destino (landing zone).

### Quando os gatilhos não se aplicam

- Criação simples de recursos (perguntas sobre SKU, versão da API ou região) → use somente `azure-dynamic-sources.md`
- Combinações de serviços já cobertas nos pacotes de domínio → priorize os arquivos de referência
- Verificação de valores de propriedades do Bicep → use `service-gotchas.md` ou a referência do Bicep no Microsoft Docs

---

## Limite de consultas

| Cenário | Número máximo de consultas |
|----------|----------------|
| Padrão (quando o gatilho dispara) | **Até dois** documentos de orientação de arquitetura |
| Consulta adicional permitida quando | Há conflitos entre documentos, permanece uma incerteza central do projeto ou a pessoa pede justificativa mais profunda |
| Perguntas simples sobre especificações de implantação | **0** (sem consultar orientação de arquitetura) |

---

## Regra de decisão por tipo de pergunta

| Tipo de pergunta | Documentos a consultar | Pontos de decisão a extrair | Documentos que NÃO devem ser consultados |
|--------------|-------------------|----------------------------------|----------------------|
| RAG / assistente de conversa / aplicativo Foundry | A5 ou A6 + A7 | Nível de isolamento da rede, método de autenticação (identidade gerenciada ou chave), estratégia de indexação (envio, `push`, ou consulta, `pull`) e escopo do monitoramento | Não percorra todo o Architecture Center |
| Segurança / governança / zona de destino empresarial | A2 + A3 | Estrutura de assinaturas, topologia de rede central e raios (`hub-spoke`), modelo de identidade/governança e limite de segurança | Documentos do domínio de IA/ML são desnecessários |
| Plataforma de dados do Fabric | A8 + A9 | Modelo de capacidade (critérios de seleção da SKU), nível de governança e limite dos dados (separação de espaços de trabalho, workspaces, etc.) | Documentos de IA são desnecessários |
| Combinação ambígua de serviços (padrão incerto) | A1 (encontre na central o documento de domínio mais próximo) + esse documento | Principais pontos de decisão identificados no documento | Não percorra todos os subdocumentos |
| Valores simples para criação de recursos (SKU/API/região) | Nenhuma consulta | — | Toda a orientação de arquitetura |
| Arquitetura geral de IA/ML | A4 (central) + arquitetura de referência mais próxima | Isolamento da computação, limite dos dados e abordagem de disponibilização do modelo | Não percorra tudo |

---

## Regra de contingência para URLs

1. Use URLs `en-us` do Learn por padrão.
2. Se uma URL específica retornar 404, redirecionamento ou estiver obsoleta → use a página da central superior.
   - Exemplo: se A5 falhar → pesquise "foundry chat" em A4 (central de IA/ML).
3. Se também não encontrar na central superior → pesquise palavras-chave do título em A1 (página principal do Architecture Center).
4. **Não trate o conteúdo de uma URL como regra fixa somente porque a URL existe.**

---

## Proibição de varredura completa

- Não percorra amplamente os subdocumentos do Architecture Center.
- Consulte especificamente somente um ou dois documentos relacionados, conforme a regra do tipo de pergunta.
- Mesmo nos documentos consultados, use somente as seções relevantes; não leia o documento inteiro.
- São proibidos consultas ilimitadas, seguimento recursivo de links e enumeração de subpáginas.
