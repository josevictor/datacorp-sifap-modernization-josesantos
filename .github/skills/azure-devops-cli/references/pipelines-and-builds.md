# Pipelines, compilações e lançamentos

## Sumário

- [Pipelines](#pipelines)
- [Execuções de pipeline](#execuções-de-pipeline)
- [Compilações](#compilações)
- [Definições de compilação](#definições-de-compilação)
- [Lançamentos](#lançamentos)
- [Definições de lançamento](#definições-de-lançamento)
- [Pacotes universais (artefatos)](#pacotes-universais-artefatos)

---

## Pipelines

### Listar pipelines

```bash
az pipelines list --output table
az pipelines list --query "[?name=='myPipeline']"
az pipelines list --folder-path 'folder/subfolder'
```

### Criar pipeline

```bash
# A partir do contexto do repositório local (detecta as configurações automaticamente)
az pipelines create --name 'ContosoBuild' --description 'Pipeline do projeto Contoso'

# Com uma branch e um caminho YAML específicos
az pipelines create \
  --name {pipeline-name} \
  --repository {repo} \
  --branch main \
  --yaml-path azure-pipelines.yml \
  --description "Meu pipeline de CI/CD"

# Para um repositório do GitHub
az pipelines create \
  --name 'GitHubPipeline' \
  --repository https://github.com/Org/Repo \
  --branch main \
  --repository-type github

# Ignorar a primeira execução
az pipelines create --name 'MyPipeline' --skip-run true
```

### Exibir pipeline

```bash
az pipelines show --id {pipeline-id}
az pipelines show --name {pipeline-name}
```

### Atualizar pipeline

```bash
az pipelines update --id {pipeline-id} --name "Novo nome" --description "Descrição atualizada"
```

### Excluir pipeline

```bash
az pipelines delete --id {pipeline-id} --yes
```

### Executar pipeline

```bash
# Executar por nome
az pipelines run --name {pipeline-name} --branch main

# Executar por ID
az pipelines run --id {pipeline-id} --branch refs/heads/main

# Com parâmetros
az pipelines run --name {pipeline-name} --parameters version=1.0.0 environment=prod

# Com variáveis
az pipelines run --name {pipeline-name} --variables buildId=123 configuration=release

# Abrir os resultados no navegador
az pipelines run --name {pipeline-name} --open
```

## Execuções de pipeline

### Listar execuções

```bash
az pipelines runs list --pipeline {pipeline-id}
az pipelines runs list --name {pipeline-name} --top 10
az pipelines runs list --branch main --status completed
```

### Exibir detalhes da execução

```bash
az pipelines runs show --run-id {run-id}
az pipelines runs show --run-id {run-id} --open
```

### Artefatos do pipeline

```bash
# Listar artefatos de uma execução
az pipelines runs artifact list --run-id {run-id}

# Baixar artefato
az pipelines runs artifact download \
  --artifact-name '{artifact-name}' \
  --path {local-path} \
  --run-id {run-id}

# Enviar artefato
az pipelines runs artifact upload \
  --artifact-name '{artifact-name}' \
  --path {local-path} \
  --run-id {run-id}
```

### Tags de execução do pipeline

```bash
# Adicionar tag à execução
az pipelines runs tag add --run-id {run-id} --tags production v1.0

# Listar tags da execução
az pipelines runs tag list --run-id {run-id} --output table
```

## Compilações

### Listar compilações

```bash
az pipelines build list
az pipelines build list --definition {build-definition-id}
az pipelines build list --status completed --result succeeded
```

### Colocar compilação na fila

```bash
az pipelines build queue --definition {build-definition-id} --branch main
az pipelines build queue --definition {build-definition-id} --parameters version=1.0.0
```

### Exibir detalhes da compilação

```bash
az pipelines build show --id {build-id}
```

### Cancelar compilação

```bash
az pipelines build cancel --id {build-id}
```

### Tags de compilação

```bash
# Adicionar tag à compilação
az pipelines build tag add --build-id {build-id} --tags prod release

# Excluir tag da compilação
az pipelines build tag delete --build-id {build-id} --tag prod
```

## Definições de compilação

### Listar definições de compilação

```bash
az pipelines build definition list
az pipelines build definition list --name {definition-name}
```

### Exibir definição de compilação

```bash
az pipelines build definition show --id {definition-id}
```

## Lançamentos

### Listar lançamentos

```bash
az pipelines release list
az pipelines release list --definition {release-definition-id}
```

### Criar lançamento

```bash
az pipelines release create --definition {release-definition-id}
az pipelines release create --definition {release-definition-id} --description "Release v1.0"
```

### Exibir lançamento

```bash
az pipelines release show --id {release-id}
```

## Definições de lançamento

### Listar definições de lançamento

```bash
az pipelines release definition list
```

### Exibir definição de lançamento

```bash
az pipelines release definition show --id {definition-id}
```

## Pacotes universais (artefatos)

### Publicar pacote

```bash
az artifacts universal publish \
  --feed {feed-name} \
  --name {package-name} \
  --version {version} \
  --path {package-path} \
  --project {project}
```

### Baixar pacote

```bash
az artifacts universal download \
  --feed {feed-name} \
  --name {package-name} \
  --version {version} \
  --path {download-path} \
  --project {project}
```
