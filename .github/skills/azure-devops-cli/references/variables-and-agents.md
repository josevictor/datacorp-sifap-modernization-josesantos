# Variáveis de pipeline, grupos de variáveis e agentes

## Sumário

- [Variáveis de pipeline](#variáveis-de-pipeline)
- [Grupos de variáveis](#grupos-de-variáveis)
- [Pastas de pipeline](#pastas-de-pipeline)
- [Conjuntos de agentes](#conjuntos-de-agentes)
- [Filas de agentes](#filas-de-agentes)
- [Agentes](#agentes)

---

## Variáveis de pipeline

### Listar variáveis

```bash
az pipelines variable list --pipeline-id {pipeline-id}
```

### Criar variável

```bash
# Variável não secreta
az pipelines variable create \
  --name {var-name} \
  --value {var-value} \
  --pipeline-id {pipeline-id}

# Variável secreta
az pipelines variable create \
  --name {var-name} \
  --secret true \
  --pipeline-id {pipeline-id}

# Segredo com solicitação interativa
az pipelines variable create \
  --name {var-name} \
  --secret true \
  --prompt true \
  --pipeline-id {pipeline-id}
```

### Atualizar variável

```bash
az pipelines variable update \
  --name {var-name} \
  --value {new-value} \
  --pipeline-id {pipeline-id}

# Atualizar variável secreta
az pipelines variable update \
  --name {var-name} \
  --secret true \
  --value "{new-secret-value}" \
  --pipeline-id {pipeline-id}
```

### Excluir variável

```bash
az pipelines variable delete --name {var-name} --pipeline-id {pipeline-id} --yes
```

## Grupos de variáveis

### Listar grupos de variáveis

```bash
az pipelines variable-group list
az pipelines variable-group list --output table
```

### Exibir grupo de variáveis

```bash
az pipelines variable-group show --id {group-id}
```

### Criar grupo de variáveis

```bash
az pipelines variable-group create \
  --name {group-name} \
  --variables key1=value1 key2=value2 \
  --authorize true
```

### Atualizar grupo de variáveis

```bash
az pipelines variable-group update \
  --id {group-id} \
  --name {new-name} \
  --description "Descrição atualizada"
```

### Excluir grupo de variáveis

```bash
az pipelines variable-group delete --id {group-id} --yes
```

### Variáveis do grupo de variáveis

```bash
# Listar variáveis
az pipelines variable-group variable list --group-id {group-id}

# Criar variável não secreta
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name {var-name} \
  --value {var-value}

# Criar variável secreta (solicita o valor se ele não for fornecido)
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name {var-name} \
  --secret true

# Criar segredo com uma variável de ambiente
export AZURE_DEVOPS_EXT_PIPELINE_VAR_MySecret=secretvalue
az pipelines variable-group variable create \
  --group-id {group-id} \
  --name MySecret \
  --secret true

# Atualizar variável
az pipelines variable-group variable update \
  --group-id {group-id} \
  --name {var-name} \
  --value {new-value} \
  --secret false

# Excluir variável
az pipelines variable-group variable delete \
  --group-id {group-id} \
  --name {var-name}
```

## Pastas de pipeline

### Listar pastas

```bash
az pipelines folder list
```

### Criar pasta

```bash
az pipelines folder create --path 'folder/subfolder' --description "Minha pasta"
```

### Excluir pasta

```bash
az pipelines folder delete --path 'folder/subfolder'
```

### Atualizar pasta

```bash
az pipelines folder update --path 'old-folder' --new-path 'new-folder'
```

## Conjuntos de agentes

### Listar conjuntos de agentes

```bash
az pipelines pool list
az pipelines pool list --pool-type automation
az pipelines pool list --pool-type deployment
```

### Exibir conjunto de agentes

```bash
az pipelines pool show --pool-id {pool-id}
```

## Filas de agentes

### Listar filas de agentes

```bash
az pipelines queue list
az pipelines queue list --pool-name {pool-name}
```

### Exibir fila de agentes

```bash
az pipelines queue show --id {queue-id}
```

## Agentes

### Listar agentes do conjunto

```bash
az pipelines agent list --pool-id {pool-id}
```

### Exibir detalhes do agente

```bash
az pipelines agent show --agent-id {agent-id} --pool-id {pool-id}
```
