# Uso avançado: saída, consultas e parâmetros

## Sumário

- [Formatos de saída](#formatos-de-saída)
- [Consultas JMESPath](#consultas-jmespath)
- [Consultas JMESPath avançadas](#consultas-jmespath-avançadas)
- [Argumentos globais](#argumentos-globais)
- [Parâmetros comuns](#parâmetros-comuns)
- [Apelidos Git](#apelidos-git)
- [Como obter ajuda](#como-obter-ajuda)

---

## Formatos de saída

Todos os comandos aceitam vários formatos de saída:

```bash
# Formato de tabela (legível por pessoas)
az pipelines list --output table

# Formato JSON (padrão, legível por máquina)
az pipelines list --output json

# JSONC (JSON colorido)
az pipelines list --output jsonc

# Formato YAML
az pipelines list --output yaml

# YAMLC (YAML colorido)
az pipelines list --output yamlc

# Formato TSV (valores separados por tabulação)
az pipelines list --output tsv

# Nenhum (sem saída)
az pipelines list --output none
```

## Consultas JMESPath

Filtre e transforme a saída:

```bash
# Filtrar por nome
az pipelines list --query "[?name=='myPipeline']"

# Obter campos específicos
az pipelines list --query "[].{Name:name, ID:id}"

# Encadear consultas
az pipelines list --query "[?name.contains('CI')].{Name:name, ID:id}" --output table

# Obter o primeiro resultado
az pipelines list --query "[0]"

# Obter os primeiros N resultados
az pipelines list --query "[0:5]"
```

## Consultas JMESPath avançadas

### Filtragem e ordenação

```bash
# Filtrar por várias condições
az pipelines list --query "[?name.contains('CI') && enabled==true]"

# Filtrar por status e resultado
az pipelines runs list --query "[?status=='completed' && result=='succeeded']"

# Ordenar por data (decrescente)
az pipelines runs list --query "sort_by([?status=='completed'], &finishTime | reverse(@))"

# Obter os primeiros N itens após a filtragem
az pipelines runs list --query "[?result=='succeeded'] | [0:5]"
```

### Consultas aninhadas

```bash
# Extrair propriedades aninhadas
az pipelines show --id $PIPELINE_ID --query "{Name:name, Repo:repository.{Name:name, Type:type}, Folder:folder}"

# Consultar detalhes da compilação
az pipelines build show --id $BUILD_ID --query "{ID:id, Number:buildNumber, Status:status, Result:result, Requested:requestedFor.displayName}"
```

### Filtragem complexa

```bash
# Encontrar pipelines com um caminho YAML específico
az pipelines list --query "[?process.type.name=='yaml' && process.yamlFilename=='azure-pipelines.yml']"

# Encontrar solicitações de pull de uma pessoa revisora específica
az repos pr list --query "[?contains(reviewers[?displayName=='John Doe'].displayName, 'John Doe')]"

# Encontrar itens de trabalho com iteração e estado específicos
az boards work-item show --id $WI_ID --query "{Title:fields['System.Title'], State:fields['System.State'], Iteration:fields['System.IterationPath']}"
```

### Agregação

```bash
# Contar itens por status
az pipelines runs list --query "groupBy([?status=='completed'], &[result]) | {Succeeded: [?key=='succeeded'][0].count, Failed: [?key=='failed'][0].count}"

# Obter revisores únicos
az repos pr list --query "unique_by(reviewers[], &displayName)"

# Somar valores
az pipelines runs list --query "[?result=='succeeded'] | [].{Duration:duration} | [0].Duration"
```

### Transformação condicional

```bash
# Formatar datas
az pipelines runs list --query "[].{ID:id, Date:createdDate, Formatted:createdDate | format_datetime(@, 'yyyy-MM-dd HH:mm')}"

# Saída condicional
az pipelines list --query "[].{Name:name, Status:(enabled ? 'Enabled' : 'Disabled')}"

# Extrair com valores padrão
az pipelines show --id $PIPELINE_ID --query "{Name:name, Folder:folder || 'Raiz', Description:description || 'Sem descrição'}"
```

### Fluxos de trabalho complexos

```bash
# Encontrar as compilações de maior duração
az pipelines build list --query "sort_by([?result=='succeeded'], &queueTime) | reverse(@) | [0:3].{ID:id, Number:buildNumber, Duration:duration}"

# Obter estatísticas de solicitações de pull por pessoa revisora
az repos pr list --query "groupBy([], &reviewers[].displayName) | [].{Reviewer:@.key, Count:length(@)}"

# Encontrar itens de trabalho com vários itens filhos
az boards work-item relation list --id $PARENT_ID --query "[?rel=='System.LinkTypes.Hierarchy-Forward'] | [].{ChildID:url | split('/', @) | [-1]}"
```

## Argumentos globais

Disponíveis em todos os comandos:

| Parâmetro | Descrição |
|---|---|
| `--help` / `-h` | Exibir a ajuda do comando |
| `--output` / `-o` | Formato da saída (json, jsonc, none, table, tsv, yaml, yamlc) |
| `--query` | Texto de consulta JMESPath para filtrar a saída |
| `--verbose` | Aumentar o detalhamento dos logs |
| `--debug` | Exibir todos os logs de depuração |
| `--only-show-errors` | Exibir somente erros e suprimir avisos |
| `--subscription` | Nome ou ID da assinatura |
| `--yes` / `-y` | Ignorar prompts de confirmação |

## Parâmetros comuns

| Parâmetro | Descrição |
|---|---|
| `--org` / `--organization` | URL da organização do Azure DevOps (por exemplo, `https://dev.azure.com/{org}`) |
| `--project` / `-p` | Nome ou ID do projeto |
| `--detect` | Detectar automaticamente a organização pela configuração do Git |
| `--yes` / `-y` | Ignorar prompts de confirmação |
| `--open` | Abrir o recurso no navegador |
| `--subscription` | Assinatura do Azure (para recursos do Azure) |

## Apelidos Git

Depois de ativar os apelidos Git:

```bash
# Ativar apelidos Git
az devops configure --use-git-aliases true

# Usar comandos Git para operações do DevOps
git pr create --target-branch main
git pr list
git pr checkout 123
```

## Como obter ajuda

```bash
# Ajuda geral
az devops --help

# Ajuda de um grupo de comandos específico
az pipelines --help
az repos pr --help

# Ajuda de um comando específico
az repos pr create --help

# Pesquisar exemplos
az find "az repos pr create"
```
