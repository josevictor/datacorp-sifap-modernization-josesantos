# Compilações e ACR Tasks

## Sumário

- [Compilação rápida (az acr build)](#compilação-rápida-az-acr-build)
- [Executar uma vez um comando ou tarefa com várias etapas (az acr run)](#executar-uma-vez-um-comando-ou-tarefa-com-várias-etapas-az-acr-run)
- [ACR Tasks (az acr task)](#acr-tasks-az-acr-task)
- [Gatilhos](#gatilhos)
- [YAML de tarefa com várias etapas](#yaml-de-tarefa-com-várias-etapas)
- [Conjuntos de agentes](#conjuntos-de-agentes)

---

## Compilação rápida (az acr build)

Compila no Azure e envia ao registro, sem exigir um serviço local em segundo plano do Docker:

```bash
# Compila a partir do diretório atual e envia a imagem
az acr build --registry {registry} --image app:v1 .

# Dockerfile personalizado, argumentos de compilação e plataforma de destino
az acr build --registry {registry} --image app:v1 \
  --file docker/Dockerfile.prod \
  --build-arg VERSION=1.2.3 \
  --platform linux/amd64 .

# Multiplataforma: cada compilação produz UMA imagem de arquitetura única para a plataforma de destino
az acr build --registry {registry} --image app:v1-arm64 --platform linux/arm64 .
# Para uma imagem realmente multiarch, compile uma vez por plataforma com tags específicas
# da arquitetura; depois, monte e envie uma lista de manifestos (docker manifest create/push
# ou docker buildx local)

# Compila diretamente de um repositório Git (sem clone local)
az acr build --registry {registry} --image app:v1 https://github.com/{org}/{repo}.git#{branch}:{folder}

# Compila sem fazer push (somente validação)
az acr build --registry {registry} --image app:test --no-push .
```

Notas:

- O contexto de compilação é enviado. Use `.dockerignore` para mantê-lo pequeno.
- Use uma tag com valor único por compilação (SHA do git ou ID da execução). Evite depender de `latest`.

## Executar uma vez um comando ou tarefa com várias etapas (az acr run)

```bash
# Executa um comando de contêiner no executor de tarefas do registro (contexto /dev/null = sem upload)
az acr run --registry {registry} --cmd '{registry}.azurecr.io/app:v1' /dev/null

# Executa um arquivo de tarefa com várias etapas no diretório atual
az acr run --registry {registry} --file acb.yaml .
```

## ACR Tasks (az acr task)

Definições de compilação persistentes que podem ser acionadas:

```bash
# Cria uma tarefa que compila a cada confirmação (commit) em main
az acr task create --registry {registry} --name build-app \
  --image "app:{{.Run.ID}}" \
  --context https://github.com/{org}/{repo}.git#main \
  --file Dockerfile \
  --git-access-token {pat} \
  --commit-trigger-enabled true \
  --base-image-trigger-enabled true

# Aciona, lista e inspeciona manualmente
az acr task run --registry {registry} --name build-app
az acr task list --registry {registry} --output table
az acr task list-runs --registry {registry} --name build-app --output table
az acr task logs --registry {registry} --name build-app        # execução mais recente
az acr task logs --registry {registry} --run-id {run-id}

# Atualiza/desativa/exclui
az acr task update --registry {registry} --name build-app --image "app:{{.Run.ID}}"
az acr task update --registry {registry} --name build-app --status Disabled
az acr task delete --registry {registry} --name build-app --yes
```

Variáveis úteis de execução para `--image`: `{{.Run.ID}}`, `{{.Run.Commit}}`, `{{.Run.Branch}}`, `{{.Run.Date}}`.

⚠️ Em **registros com ABAC** (`roleAssignmentMode` = `AbacRepositoryPermissions`), tarefas e compilações/execuções rápidas não têm acesso padrão ao registro de origem. Passe `--source-acr-auth-id [caller]` para `az acr build`/`az acr run` e `--source-acr-auth-id [system]` (ou o ID de recurso de uma identidade atribuída pelo usuário) para `az acr task create`/`update`. Depois, conceda a essa identidade as funções `Container Registry Repository ...`. Antes de referenciá-la, confirme se a tarefa realmente tem essa identidade: adicione `--assign-identity [system]` durante a criação ou execute `az acr task identity assign` em uma tarefa existente.

## Gatilhos

```bash
# Gatilho de temporizador (cron em UTC), por exemplo, recompilação noturna
az acr task timer add --registry {registry} --name build-app \
  --timer-name nightly --schedule "0 2 * * *"
az acr task timer list --registry {registry} --name build-app
az acr task timer remove --registry {registry} --name build-app --timer-name nightly
```

- **Gatilho de confirmação**: recompila após o envio para a ramificação monitorada (`--commit-trigger-enabled`).
- **Gatilho de imagem base**: recompila automaticamente quando a imagem base (por exemplo, uma imagem corrigida de `mcr.microsoft.com`) é atualizada (`--base-image-trigger-enabled`). É essencial para correções do sistema operacional e da estrutura de software.
- **Gatilho de temporizador**: agendamentos cron; também é a forma padrão de agendar a limpeza com `acr purge` (consulte `images-and-artifacts.md`).

Tarefas que acessam outros registros ou recursos do Azure podem usar uma identidade:

```bash
az acr task identity assign --registry {registry} --name build-app   # atribuída pelo sistema
az acr task credential add --registry {registry} --name build-app \
  --login-server {other-registry}.azurecr.io --use-identity [system]
```

## YAML de tarefa com várias etapas

`acb.yaml`: compila, testa e envia a imagem somente em caso de sucesso:

```yaml
version: v1.1.0
steps:
  - build: -t $Registry/app:{{.Run.ID}} -f Dockerfile .
  - cmd: $Registry/app:{{.Run.ID}} run-tests
  - push:
      - $Registry/app:{{.Run.ID}}
```

```bash
# Executa uma vez
az acr run --registry {registry} --file acb.yaml .

# Ou cria uma tarefa acionável a partir do YAML
az acr task create --registry {registry} --name build-test-push \
  --file acb.yaml \
  --context https://github.com/{org}/{repo}.git#main \
  --git-access-token {pat}
```

## Conjuntos de agentes

SKU Premium. Computação dedicada para tarefas, para ter mais CPU ou usar uma das duas formas compatíveis de executar tarefas em um registro com restrição de rede. A outra forma combina serviços confiáveis e a política de desvio de rede para tarefas. Consulte `networking-and-geo.md`:

```bash
az acr agentpool create --registry {registry} --name pool1 --tier S2   # S1/S2/S3/I6

# No cenário de firewall/VNet, o conjunto DEVE estar anexado a uma sub-rede que acesse
# o ponto de extremidade privado do registro; sem --subnet-id, ele executa fora da VNet
az acr agentpool create --registry {registry} --name pool1 --tier S2 \
  --subnet-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{vnet}/subnets/{subnet}

az acr agentpool list --registry {registry} --output table

# Direciona ao conjunto de agentes
az acr build --registry {registry} --agent-pool pool1 --image app:v1 .
az acr task create --registry {registry} --name build-app --agent-pool pool1 ...
```
