# Fluxos de trabalho, práticas recomendadas e padrões de scripts

## Sumário

- [Fluxos de trabalho comuns](#fluxos-de-trabalho-comuns)
- [Práticas recomendadas](#práticas-recomendadas)
- [Tratamento de erros e padrões de repetição](#tratamento-de-erros-e-padrões-de-repetição)
- [Padrões de scripts para operações idempotentes](#padrões-de-scripts-para-operações-idempotentes)
- [Fluxos de trabalho reais](#fluxos-de-trabalho-reais)

---

## Fluxos de trabalho comuns

### Criar uma solicitação de pull a partir da ramificação atual

```bash
CURRENT_BRANCH=$(git branch --show-current)
az repos pr create \
  --source-branch $CURRENT_BRANCH \
  --target-branch main \
  --title "Funcionalidade: $(git log -1 --pretty=%B)" \
  --open
```

### Criar item de trabalho em caso de falha do pipeline

```bash
az boards work-item create \
  --title "A compilação $BUILD_BUILDNUMBER falhou" \
  --type bug \
  --org $SYSTEM_TEAMFOUNDATIONCOLLECTIONURI \
  --project $SYSTEM_TEAMPROJECT
```

### Baixar o artefato mais recente do pipeline

```bash
RUN_ID=$(az pipelines runs list --pipeline {pipeline-id} --top 1 --query "[0].id" -o tsv)
az pipelines runs artifact download \
  --artifact-name 'webapp' \
  --path ./output \
  --run-id $RUN_ID
```

### Aprovar e concluir a solicitação de pull

```bash
# Votar para aprovar
az repos pr set-vote --id {pr-id} --vote approve

# Concluir a solicitação de pull
az repos pr update --id {pr-id} --status completed
```

### Criar pipeline a partir do repositório local

```bash
# A partir do repositório Git local (detecta repositório, ramificação etc. automaticamente)
az pipelines create --name 'CI-Pipeline' --description 'Integração contínua'
```

### Atualizar itens de trabalho em massa

```bash
# Consultar itens e atualizar em um loop
for id in $(az boards query --wiql "SELECT ID FROM WorkItems WHERE State='New'" -o tsv); do
  az boards work-item update --id $id --state "Active"
done
```

## Práticas recomendadas

### Autenticação e segurança

```bash
# Usar o PAT de uma variável de ambiente (mais seguro)
export AZURE_DEVOPS_EXT_PAT=$MY_PAT
az devops login --organization $ORG_URL

# Encaminhar o PAT com segurança (evita o histórico do shell)
echo $MY_PAT | az devops login --organization $ORG_URL

# Definir padrões para evitar repetição
az devops configure --defaults organization=$ORG_URL project=$PROJECT

# Limpar credenciais após o uso
az devops logout --organization $ORG_URL
```

### Operações idempotentes

```bash
# Sempre usar --detect para detecção automática
az devops configure --defaults organization=$ORG_URL project=$PROJECT

# Verificar a existência antes da criação
if ! az pipelines show --id $PIPELINE_ID 2>/dev/null; then
  az pipelines create --name "$PIPELINE_NAME" --yaml-path azure-pipelines.yml
fi

# Usar --output tsv para processamento pelo interpretador de comandos
PIPELINE_ID=$(az pipelines list --query "[?name=='MyPipeline'].id" --output tsv)

# Usar --output json para acesso por código
BUILD_STATUS=$(az pipelines build show --id $BUILD_ID --query "status" --output json)
```

### Saída segura para scripts

```bash
# Suprimir avisos e erros
az pipelines list --only-show-errors

# Sem saída (útil para comandos que só precisam ser executados)
az pipelines run --name "$PIPELINE_NAME" --output none

# Formato TSV para scripts do interpretador de comandos (limpo, sem formatação)
az repos pr list --output tsv --query "[].{ID:pullRequestId,Title:title}"

# JSON com campos específicos
az pipelines list --output json --query "[].{Name:name, ID:id, URL:url}"
```

### Orquestração de pipeline

```bash
# Executar o pipeline e aguardar a conclusão
RUN_ID=$(az pipelines run --name "$PIPELINE_NAME" --query "id" -o tsv)

while true; do
  STATUS=$(az pipelines runs show --run-id $RUN_ID --query "status" -o tsv)
  if [[ "$STATUS" != "inProgress" && "$STATUS" != "notStarted" ]]; then
    break
  fi
  sleep 10
done

# Verificar o resultado
RESULT=$(az pipelines runs show --run-id $RUN_ID --query "result" -o tsv)
if [[ "$RESULT" == "succeeded" ]]; then
  echo "Pipeline concluído com sucesso"
else
  echo "O pipeline falhou com o resultado: $RESULT"
  exit 1
fi
```

### Gerenciamento de grupos de variáveis

```bash
# Criar grupo de variáveis de forma idempotente
VG_NAME="production-variables"
VG_ID=$(az pipelines variable-group list --query "[?name=='$VG_NAME'].id" -o tsv)

if [[ -z "$VG_ID" ]]; then
  VG_ID=$(az pipelines variable-group create \
    --name "$VG_NAME" \
    --variables API_URL=$API_URL API_KEY=$API_KEY \
    --authorize true \
    --query "id" -o tsv)
  echo "Grupo de variáveis criado com o ID: $VG_ID"
else
  echo "O grupo de variáveis já existe com o ID: $VG_ID"
fi
```

### Automação de conexões de serviço

```bash
# Criar conexão de serviço com um arquivo de configuração
cat > service-connection.json <<'EOF'
{
  "data": {
    "subscriptionId": "$SUBSCRIPTION_ID",
    "subscriptionName": "Minha assinatura",
    "creationMode": "Manual",
    "serviceEndpointId": "$SERVICE_ENDPOINT_ID"
  },
  "url": "https://management.azure.com/",
  "authorization": {
    "parameters": {
      "tenantid": "$TENANT_ID",
      "serviceprincipalid": "$SP_ID",
      "authenticationType": "spnKey",
      "serviceprincipalkey": "$SP_KEY"
    },
    "scheme": "ServicePrincipal"
  },
  "type": "azurerm",
  "isShared": false,
  "isReady": true
}
EOF

az devops service-endpoint create \
  --service-endpoint-configuration service-connection.json \
  --project "$PROJECT"
```

### Automação de solicitações de pull

```bash
# Criar solicitação de pull com itens de trabalho e revisores
PR_ID=$(az repos pr create \
  --repository "$REPO_NAME" \
  --source-branch "$FEATURE_BRANCH" \
  --target-branch main \
  --title "Funcionalidade: $(git log -1 --pretty=%B)" \
  --description "$(git log -1 --pretty=%B)" \
  --work-items $WORK_ITEM_1 $WORK_ITEM_2 \
  --reviewers "$REVIEWER_1" "$REVIEWER_2" \
  --required-reviewers "$LEAD_EMAIL" \
  --labels "enhancement" "backlog" \
  --open \
  --query "pullRequestId" -o tsv)

# Definir conclusão automática quando as políticas forem aprovadas
az repos pr update --id $PR_ID --auto-complete true
```

## Tratamento de erros e padrões de repetição

### Lógica de repetição para falhas transitórias

```bash
# Função de repetição para operações de rede
retry_command() {
  local max_attempts=3
  local attempt=1
  local delay=5

  while [[ $attempt -le $max_attempts ]]; do
    if "$@"; then
      return 0
    fi
    echo "A tentativa $attempt falhou. Nova tentativa em ${delay}s..."
    sleep $delay
    ((attempt++))
    delay=$((delay * 2))
  done

  echo "Todas as $max_attempts tentativas falharam"
  return 1
}

# Uso
retry_command az pipelines run --name "$PIPELINE_NAME"
```

### Verificar e tratar erros

```bash
# Verificar se o pipeline existe antes das operações
PIPELINE_ID=$(az pipelines list --query "[?name=='$PIPELINE_NAME'].id" -o tsv)

if [[ -z "$PIPELINE_ID" ]]; then
  echo "Pipeline não encontrado. Criando..."
  az pipelines create --name "$PIPELINE_NAME" --yaml-path azure-pipelines.yml
else
  echo "O pipeline existe com o ID: $PIPELINE_ID"
fi
```

### Validar entradas

```bash
# Validar parâmetros obrigatórios
if [[ -z "$PROJECT" || -z "$REPO" ]]; then
  echo "Erro: PROJECT e REPO devem estar definidos"
  exit 1
fi

# Verificar se a ramificação existe
if ! az repos ref list --repository "$REPO" --query "[?name=='refs/heads/$BRANCH']" -o tsv | grep -q .; then
  echo "Erro: a ramificação $BRANCH não existe"
  exit 1
fi
```

### Tratar erros de permissão

```bash
# Tentar a operação e tratar erros de permissão
if az devops security permission update \
  --id "$USER_ID" \
  --namespace "GitRepositories" \
  --project "$PROJECT" \
  --token "repoV2/$PROJECT/$REPO_ID" \
  --allow-bit 2 \
  --deny-bit 0 2>&1 | grep -q "unauthorized"; then
  echo "Erro: permissões insuficientes para atualizar as permissões do repositório"
  exit 1
fi
```

### Notificação de falha do pipeline

```bash
# Executar o pipeline e verificar o resultado
RUN_ID=$(az pipelines run --name "$PIPELINE_NAME" --query "id" -o tsv)

# Aguardar a conclusão
while true; do
  STATUS=$(az pipelines runs show --run-id $RUN_ID --query "status" -o tsv)
  if [[ "$STATUS" != "inProgress" && "$STATUS" != "notStarted" ]]; then
    break
  fi
  sleep 10
done

# Verificar o resultado e criar um item de trabalho em caso de falha
RESULT=$(az pipelines runs show --run-id $RUN_ID --query "result" -o tsv)
if [[ "$RESULT" != "succeeded" ]]; then
  BUILD_NUMBER=$(az pipelines runs show --run-id $RUN_ID --query "buildNumber" -o tsv)

  az boards work-item create \
    --title "A compilação $BUILD_NUMBER falhou" \
    --type Bug \
    --description "A execução $RUN_ID do pipeline falhou com o resultado: $RESULT\n\nURL: $ORG_URL/$PROJECT/_build/results?buildId=$RUN_ID"
fi
```

### Degradação controlada

```bash
# Tentar baixar o artefato e recorrer a uma fonte alternativa
if ! az pipelines runs artifact download \
  --artifact-name 'webapp' \
  --path ./output \
  --run-id $RUN_ID 2>/dev/null; then
  echo "Aviso: falha ao baixar da execução do pipeline. Recorrendo à fonte de cópia de segurança..."

  # Método alternativo de download
  curl -L "$BACKUP_URL" -o ./output/backup.zip
fi
```

## Padrões de scripts para operações idempotentes

### Padrão de criação ou atualização

```bash
# Garantir que o pipeline exista e atualizar se estiver diferente
ensure_pipeline() {
  local name=$1
  local yaml_path=$2

  PIPELINE=$(az pipelines list --query "[?name=='$name']" -o json)

  if [[ -z "$PIPELINE" ]]; then
    echo "Criando pipeline: $name"
    az pipelines create --name "$name" --yaml-path "$yaml_path"
  else
    echo "O pipeline existe: $name"
  fi
}
```

### Garantir o grupo de variáveis

```bash
# Criar grupo de variáveis com atualizações idempotentes
ensure_variable_group() {
  local vg_name=$1
  shift
  local variables=("$@")

  VG_ID=$(az pipelines variable-group list --query "[?name=='$vg_name'].id" -o tsv)

  if [[ -z "$VG_ID" ]]; then
    echo "Criando grupo de variáveis: $vg_name"
    VG_ID=$(az pipelines variable-group create \
      --name "$vg_name" \
      --variables "${variables[@]}" \
      --authorize true \
      --query "id" -o tsv)
  else
    echo "O grupo de variáveis existe: $vg_name (ID: $VG_ID)"
  fi

  echo "$VG_ID"
}
```

### Garantir a conexão de serviço

```bash
# Verificar se a conexão de serviço existe e criá-la se necessário
ensure_service_connection() {
  local name=$1
  local project=$2

  SC_ID=$(az devops service-endpoint list \
    --project "$project" \
    --query "[?name=='$name'].id" \
    -o tsv)

  if [[ -z "$SC_ID" ]]; then
    echo "Conexão de serviço não encontrada. Criando..."
    # Adicione aqui a lógica de criação
  else
    echo "A conexão de serviço existe: $name"
    echo "$SC_ID"
  fi
}
```

### Criação idempotente de itens de trabalho

```bash
# Criar o item de trabalho somente se não existir outro com o mesmo título
create_work_item_if_new() {
  local title=$1
  local type=$2

  WI_ID=$(az boards query \
    --wiql "SELECT ID FROM WorkItems WHERE [System.WorkItemType]='$type' AND [System.Title]='$title'" \
    --query "[0].id" -o tsv)

  if [[ -z "$WI_ID" ]]; then
    echo "Criando item de trabalho: $title"
    WI_ID=$(az boards work-item create --title "$title" --type "$type" --query "id" -o tsv)
  else
    echo "O item de trabalho existe: $title (ID: $WI_ID)"
  fi

  echo "$WI_ID"
}
```

### Operações idempotentes em massa

```bash
# Garantir que vários pipelines existam
declare -a PIPELINES=(
  "ci-pipeline:azure-pipelines.yml"
  "deploy-pipeline:deploy.yml"
  "test-pipeline:test.yml"
)

for pipeline in "${PIPELINES[@]}"; do
  IFS=':' read -r name yaml <<< "$pipeline"
  ensure_pipeline "$name" "$yaml"
done
```

### Sincronização de configuração

```bash
# Sincronizar grupos de variáveis a partir do arquivo de configuração
sync_variable_groups() {
  local config_file=$1

  while IFS=',' read -r vg_name variables; do
    ensure_variable_group "$vg_name" "$variables"
  done < "$config_file"
}

# Formato de config.csv:
# prod-vars,API_URL=prod.com,API_KEY=secret123
# dev-vars,API_URL=dev.com,API_KEY=secret456
```

## Fluxos de trabalho reais

### Configuração do pipeline de integração e entrega contínuas (CI/CD)

```bash
# Configurar o pipeline completo de integração e entrega contínuas (CI/CD)
setup_cicd_pipeline() {
  local project=$1
  local repo=$2
  local branch=$3

  # Criar grupos de variáveis
  VG_DEV=$(ensure_variable_group "dev-vars" "ENV=dev API_URL=api-dev.com")
  VG_PROD=$(ensure_variable_group "prod-vars" "ENV=prod API_URL=api-prod.com")

  # Criar pipeline de CI
  az pipelines create \
    --name "$repo-CI" \
    --repository "$repo" \
    --branch "$branch" \
    --yaml-path .azure/pipelines/ci.yml \
    --skip-run true

  # Criar pipeline de CD
  az pipelines create \
    --name "$repo-CD" \
    --repository "$repo" \
    --branch "$branch" \
    --yaml-path .azure/pipelines/cd.yml \
    --skip-run true

  echo "Configuração do pipeline de integração e entrega contínuas concluída"
}
```

### Criação automatizada de solicitação de pull

```bash
# Criar uma solicitação de pull da ramificação de funcionalidade com automação
create_automated_pr() {
  local branch=$1
  local title=$2

  # Obter informações da ramificação
  LAST_COMMIT=$(git log -1 --pretty=%B "$branch")
  COMMIT_SHA=$(git rev-parse "$branch")

  # Encontrar itens de trabalho relacionados
  WORK_ITEMS=$(az boards query \
    --wiql "SELECT ID FROM WorkItems WHERE [System.ChangedBy] = @Me AND [System.State] = 'Active'" \
    --query "[].id" -o tsv)

  # Criar solicitação de pull
  PR_ID=$(az repos pr create \
    --source-branch "$branch" \
    --target-branch main \
    --title "$title" \
    --description "$LAST_COMMIT" \
    --work-items $WORK_ITEMS \
    --auto-complete true \
    --query "pullRequestId" -o tsv)

  # Definir revisores obrigatórios
  az repos pr reviewer add \
    --id $PR_ID \
    --reviewers $(git log -1 --pretty=format:'%ae' "$branch") \
    --required true

  echo "Solicitação de pull #$PR_ID criada"
}
```

### Monitoramento e alertas do pipeline

```bash
# Monitorar o pipeline e alertar em caso de falha
monitor_pipeline() {
  local pipeline_name=$1
  local slack_webhook=$2

  while true; do
    # Obter a execução mais recente
    RUN_ID=$(az pipelines list --query "[?name=='$pipeline_name'] | [0].id" -o tsv)
    RUNS=$(az pipelines runs list --pipeline $RUN_ID --top 1)

    LATEST_RUN_ID=$(echo "$RUNS" | jq -r '.[0].id')
    RESULT=$(echo "$RUNS" | jq -r '.[0].result')

    # Verificar se houve falha ainda não processada
    if [[ "$RESULT" == "failed" ]]; then
      # Enviar alerta ao Slack
      curl -X POST "$slack_webhook" \
        -H 'Content-Type: application/json' \
        -d "{\"text\": \"O pipeline $pipeline_name falhou! ID da execução: $LATEST_RUN_ID\"}"
    fi

    sleep 300 # Verificar a cada 5 minutos
  done
}
```

### Gerenciamento de itens de trabalho em massa

```bash
# Atualizar itens de trabalho em massa com base em uma consulta
bulk_update_work_items() {
  local wiql=$1
  local updates=("$@")

  # Consultar itens de trabalho
  WI_IDS=$(az boards query --wiql "$wiql" --query "[].id" -o tsv)

  # Atualizar cada item de trabalho
  for wi_id in $WI_IDS; do
    az boards work-item update --id $wi_id "${updates[@]}"
    echo "Item de trabalho atualizado: $wi_id"
  done
}

# Uso: bulk_update_work_items "SELECT ID FROM WorkItems WHERE State='New'" --state "Active" --assigned-to "user@example.com"
```

### Automação de políticas de ramificação

```bash
# Aplicar políticas de ramificação a todos os repositórios
apply_branch_policies() {
  local branch=$1
  local project=$2

  # Obter todos os repositórios
  REPOS=$(az repos list --project "$project" --query "[].id" -o tsv)

  for repo_id in $REPOS; do
    echo "Aplicando políticas ao repositório: $repo_id"

    # Exigir uma quantidade mínima de aprovações
    az repos policy approver-count create \
      --blocking true \
      --enabled true \
      --branch "$branch" \
      --repository-id "$repo_id" \
      --minimum-approver-count 2 \
      --creator-vote-counts true

    # Exigir vinculação de itens de trabalho
    az repos policy work-item-linking create \
      --blocking true \
      --branch "$branch" \
      --enabled true \
      --repository-id "$repo_id"

    # Exigir validação da compilação
    BUILD_ID=$(az pipelines list --query "[?name=='CI'].id" -o tsv | head -1)
    az repos policy build create \
      --blocking true \
      --enabled true \
      --branch "$branch" \
      --repository-id "$repo_id" \
      --build-definition-id "$BUILD_ID" \
      --queue-on-source-update-only true
  done
}
```

### Implantação em vários ambientes

```bash
# Implantar em vários ambientes
deploy_to_environments() {
  local run_id=$1
  shift
  local environments=("$@")

  # Baixar artefatos
  ARTIFACT_NAME=$(az pipelines runs artifact list --run-id $run_id --query "[0].name" -o tsv)
  az pipelines runs artifact download \
    --artifact-name "$ARTIFACT_NAME" \
    --path ./artifacts \
    --run-id $run_id

  # Implantar em cada ambiente
  for env in "${environments[@]}"; do
    echo "Implantando em: $env"

    # Obter variáveis específicas do ambiente
    VG_ID=$(az pipelines variable-group list --query "[?name=='$env-vars'].id" -o tsv)

    # Executar o pipeline de implantação
    DEPLOY_RUN_ID=$(az pipelines run \
      --name "Deploy-$env" \
      --variables ARTIFACT_PATH=./artifacts ENV="$env" \
      --query "id" -o tsv)

    # Aguardar a implantação
    while true; do
      STATUS=$(az pipelines runs show --run-id $DEPLOY_RUN_ID --query "status" -o tsv)
      if [[ "$STATUS" != "inProgress" ]]; then
        break
      fi
      sleep 10
    done
  done
}
```
