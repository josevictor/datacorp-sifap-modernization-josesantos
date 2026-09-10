---
name: "azure-deployment-preflight"
description: "Use antes de implantar Bicep/ARM no Azure para executar validação da sintaxe do modelo, análise what-if e verificações de permissões. Acione quando mencionarem implantação no Azure, validação de arquivos Bicep, verificação de permissões de implantação, visualização prévia de alterações de infraestrutura, execução de what-if ou preparação para azd provision. Os gatilhos incluem \"pré-implantação\", \"what-if\", \"validar implantação\", \"azd provision --preview\" e \"permissões de implantação\"."
---
# Validação pré-implantação do Azure

Esta habilidade valida implantações Bicep antes da execução e oferece suporte aos fluxos da Azure CLI (`az`) e da Azure Developer CLI (`azd`).

> **Escopo do kit:** a IaC deste kit usa **Terraform (provedor do Azure `~> 3.x`)**. Bicep/ARM estão **fora do escopo** das entregas do kit. Use esta validação pré-implantação somente quando um projeto realmente usar Bicep/ARM. Para Terraform, use `terraform validate`/`terraform plan` e a habilidade `terraform-azurerm-set-diff-analyzer`.

## Quando usar

- "Valide minha implantação Bicep antes de executá-la."
- "Mostre uma prévia das alterações que `azd provision` fará."
- "Verifique se tenho permissão para implantar este modelo."
- "Execute um what-if na minha infraestrutura antes da implantação."

Momentos típicos: antes de implantar infraestrutura no Azure; durante a preparação ou revisão de arquivos Bicep; para visualizar as alterações de uma implantação; para verificar se as permissões são suficientes; ou antes de executar `azd up`, `azd provision` ou `az deployment`.

## Processo de validação

Siga estas etapas em ordem. Continue para a próxima mesmo que uma etapa anterior falhe e registre todos os problemas no relatório final.

### Etapa 1: detectar o tipo de projeto

Determine o fluxo de implantação verificando os indicadores do projeto:

1. **Verifique se é um projeto azd**: procure `azure.yaml` na raiz do projeto
   - Se encontrar → use o **fluxo azd**
   - Se não encontrar → use o **fluxo da CLI az**

2. **Localize os arquivos Bicep**: encontre todos os arquivos `.bicep` que precisam de validação
   - Em projetos azd: verifique primeiro o diretório `infra/` e depois a raiz do projeto
   - Em projetos independentes: use o arquivo especificado ou procure em locais comuns (`infra/`, `deploy/` e a raiz do projeto)

3. **Detecte automaticamente os arquivos de parâmetros**: para cada arquivo Bicep, procure arquivos de parâmetros correspondentes:
   - `<filename>.bicepparam` (parâmetros Bicep, preferencial)
   - `<filename>.parameters.json` (parâmetros JSON)
   - `parameters.json` ou `parameters/<env>.json` no mesmo diretório

### Etapa 2: validar a sintaxe do Bicep

Execute a Bicep CLI para verificar a sintaxe do modelo antes de tentar validar a implantação:

```bash
bicep build <bicep-file> --stdout
```

**O que registrar:**

- Erros de sintaxe com números de linha/coluna
- Mensagens de aviso
- Status de sucesso/falha da compilação

**Se a Bicep CLI não estiver instalada:**

- Registre o problema no relatório
- Continue para a Etapa 3 (o Azure validará a sintaxe durante o what-if)

### Etapa 3: executar a validação pré-implantação

Escolha a validação adequada conforme o tipo de projeto detectado na Etapa 1.

#### Para projetos azd (azure.yaml existe)

Use `azd provision --preview` para validar a implantação:

```bash
azd provision --preview
```

Se um ambiente for especificado ou houver vários ambientes:

```bash
azd provision --preview --environment <env-name>
```

#### Para Bicep independente (sem azure.yaml)

Determine o escopo da implantação pela declaração `targetScope` do arquivo Bicep:

| Escopo de destino | Comando |
|--------------|---------|
| `resourceGroup` (padrão) | `az deployment group what-if` |
| `subscription` | `az deployment sub what-if` |
| `managementGroup` | `az deployment mg what-if` |
| `tenant` | `az deployment tenant what-if` |

**Execute primeiro com o nível de validação Provider.**

Escopo do grupo de recursos (mais comum):

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

Escopo da assinatura:

```bash
az deployment sub what-if \
  --location <location> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

Escopo do grupo de gerenciamento:

```bash
az deployment mg what-if \
  --location <location> \
  --management-group-id <mg-id> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

Escopo do locatário (`tenant`):

```bash
az deployment tenant what-if \
  --location <location> \
  --template-file <bicep-file> \
  --parameters <param-file> \
  --validation-level Provider
```

**Estratégia alternativa:**

Se `--validation-level Provider` falhar com erros de permissão (RBAC), tente novamente com `ProviderNoRbac`:

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <bicep-file> \
  --validation-level ProviderNoRbac
```

Registre a alternativa no relatório. A pessoa pode não ter permissões completas de implantação.

### Etapa 4: registrar os resultados do what-if

Analise a saída do what-if para categorizar as alterações dos recursos:

| Tipo de alteração | Símbolo | Significado |
|-------------|--------|---------|
| Create | `+` | Um novo recurso será criado |
| Delete | `-` | O recurso será excluído |
| Modify | `~` | As propriedades do recurso serão alteradas |
| NoChange | `=` | O recurso não será alterado |
| Ignore | `*` | O recurso não foi analisado (limites atingidos) |
| Deploy | `!` | O recurso será implantado (alterações desconhecidas) |

Para recursos modificados, registre as alterações específicas das propriedades.

### Etapa 5: gerar o relatório

Crie um arquivo de relatório Markdown na **raiz do projeto** com o nome:

- `preflight-report.md`

Use a estrutura do modelo em [references/REPORT-TEMPLATE.md](references/REPORT-TEMPLATE.md).

**Seções do relatório:**

1. **Resumo**: status geral, data e hora, arquivos validados e escopo de destino
2. **Ferramentas executadas**: comandos executados, versões e níveis de validação usados
3. **Problemas**: todos os erros e avisos com severidade e correção
4. **Resultados do what-if**: recursos que serão criados/modificados/excluídos ou não serão alterados
5. **Recomendações**: próximas etapas práticas

## Informações obrigatórias

Antes de executar a validação, obtenha:

| Informação | Necessária para | Como obter |
|-------------|--------------|---------------|
| Grupo de recursos | `az deployment group` | Pergunte à pessoa ou verifique a configuração existente em `.azure/` |
| Assinatura | Todas as implantações | Execute `az account show` ou pergunte à pessoa |
| Local | Escopo de assinatura/grupo de gerenciamento/locatário | Pergunte à pessoa ou use o padrão da configuração |
| Ambiente | Projetos azd | Execute `azd env list` ou pergunte à pessoa |

Se faltar alguma informação obrigatória, solicite-a antes de prosseguir.

## Tratamento de erros

Consulte [references/ERROR-HANDLING.md](references/ERROR-HANDLING.md) para obter orientações detalhadas sobre tratamento de erros.

**Princípio fundamental:** continue a validação mesmo quando ocorrerem erros. Registre todos os problemas no relatório final.

| Tipo de erro | Ação |
|------------|--------|
| Sem autenticação | Registre no relatório e sugira `az login` ou `azd auth login` |
| Permissão negada | Use `ProviderNoRbac` como alternativa e registre no relatório |
| Erro de sintaxe do Bicep | Inclua todos os erros e continue com os outros arquivos |
| Ferramenta não instalada | Registre no relatório e ignore essa etapa de validação |
| Grupo de recursos não encontrado | Registre no relatório e sugira criá-lo |

## Requisitos de ferramentas

Esta habilidade usa as seguintes ferramentas:

- **Azure CLI** (`az`): versão 2.76.0+ recomendada para `--validation-level`
- **Azure Developer CLI** (`azd`): para projetos com `azure.yaml`
- **Bicep CLI** (`bicep`): para validação de sintaxe
- **Ferramentas MCP do Azure**: para consultar documentação e boas práticas

Verifique a disponibilidade das ferramentas antes de começar:

```bash
az --version
azd version
bicep --version
```

## Exemplo de fluxo de trabalho

1. Pessoa: "Valide minha implantação Bicep antes de executá-la"
2. O agente detecta `azure.yaml` → projeto azd
3. O agente encontra `infra/main.bicep` e `infra/main.bicepparam`
4. O agente executa `bicep build infra/main.bicep --stdout`
5. O agente executa `azd provision --preview`
6. O agente gera `preflight-report.md` na raiz do projeto
7. O agente resume as descobertas para a pessoa

## Modelo de saída

A habilidade grava `preflight-report.md` na raiz do projeto, seguindo [references/REPORT-TEMPLATE.md](references/REPORT-TEMPLATE.md). Abaixo do título de nível superior `Relatório de pré-implantação`, ele contém:

```markdown
## Resumo

- Status: APROVADO com avisos
- Data e hora: 2026-08-17T14:00:00Z
- Arquivos validados: infra/main.bicep
- Escopo de destino: resourceGroup (rg-sifap)

## Ferramentas executadas

| Ferramenta | Versão | Resultado |
|---|---|---|
| bicep build | 0.30.3 | sucesso |
| az deployment group what-if | 2.76.0 (Provider) | sucesso |

## Problemas

| Severidade | Local | Descoberta | Correção |
|---|---|---|---|
| Aviso | main.bicep:42 | O armazenamento permite acesso público a blobs | Defina allowBlobPublicAccess como false |

## Resultados do what-if

| Alteração | Quantidade | Recursos |
|---|---|---|
| Create (+) | 3 | storageAccount, appService, keyVault |
| Modify (~) | 1 | appServicePlan (B1 -> S1) |
| Delete (-) | 0 | nenhum |

## Recomendações

- Resolva o aviso de acesso público antes da implantação.
- Execute novamente com `--validation-level Provider` após a concessão do RBAC.
```

## Critérios de qualidade

- [ ] O tipo de projeto foi detectado (azd versus independente) e todos os arquivos `.bicep` foram localizados.
- [ ] A sintaxe do Bicep foi validada com `bicep build`, ou a ausência da ferramenta foi registrada no relatório.
- [ ] O what-if foi executado no escopo correto; uma falha de RBAC usou `ProviderNoRbac` como alternativa e foi registrada.
- [ ] Todas as alterações de criação/modificação/exclusão foram categorizadas, com detalhes das propriedades modificadas.
- [ ] `preflight-report.md` foi gravado na raiz do projeto com as cinco seções preenchidas.
- [ ] A validação continuou por todas as etapas e registrou todos os problemas, em vez de parar no primeiro erro.

## Documentação de referência

- [Referência dos comandos de validação](references/VALIDATION-COMMANDS.md)
- [Modelo de relatório](references/REPORT-TEMPLATE.md)
- [Guia de tratamento de erros](references/ERROR-HANDLING.md)
