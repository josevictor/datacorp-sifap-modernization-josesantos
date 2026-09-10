# Redes e replicação geográfica

## Sumário

- [Replicação geográfica](#replicação-geográfica)
- [Redundância de zona](#redundância-de-zona)
- [Pontos de extremidade privados (Private Link)](#pontos-de-extremidade-privados-private-link)
- [Regras de rede pública](#regras-de-rede-pública)
- [Pontos de extremidade de dados dedicados](#pontos-de-extremidade-de-dados-dedicados)
- [Registro conectado](#registro-conectado)
- [Fluxos de transferência de registros](#fluxos-de-transferência-de-registros)

Replicação geográfica, pontos de extremidade privados, regras de rede de IP público, pontos de extremidade de dados dedicados, registros conectados e fluxos de transferência exigem a SKU **Premium**. A redundância de zona é automática em todas as camadas.

---

## Replicação geográfica

Um registro, um servidor de autenticação e imagens fornecidas pela região mais próxima:

```bash
az acr replication create --registry {registry} --location westeurope
az acr replication list --registry {registry} --output table
az acr replication show --registry {registry} --name westeurope
az acr replication delete --registry {registry} --name westeurope

# Status do ponto de extremidade regional (útil para depurar notificação HTTP/replicação)
az acr replication update --registry {registry} --name westeurope --region-endpoint-enabled true
```

Os envios são replicados automaticamente. Os clientes continuam baixando imagens de `{registry}.azurecr.io`, e o Traffic Manager roteia para a réplica mais próxima.

## Redundância de zona

A redundância de zona é **ativada automaticamente para todos os registros, em todas as camadas (Basic/Standard/Premium), nas regiões compatíveis com zonas de disponibilidade**. Nenhuma opção, SKU ou ação é necessária, e ela não pode ser desativada. As réplicas geográficas nas regiões compatíveis também têm redundância de zona por padrão.

Não dependa da propriedade `zoneRedundancy` nem da opção legada `--zone-redundancy`: a propriedade é um artefato descontinuado que pode exibir `Disabled` mesmo quando o registro tem redundância de zona completa. Registros em regiões sem suporte a zonas de disponibilidade são a única exceção. Migre-os (por meio de `az acr import` ou de um fluxo de transferência) para uma região compatível.

## Pontos de extremidade privados (Private Link)

```bash
# 1. Desativa políticas de rede na sub-rede, se necessário, e cria o ponto de extremidade
az network private-endpoint create --resource-group {rg} --name {registry}-pe \
  --vnet-name {vnet} --subnet {subnet} \
  --private-connection-resource-id $(az acr show --name {registry} --query id --output tsv) \
  --group-ids registry \
  --connection-name {registry}-pe-conn

# 2. DNS privado para resolver {registry}.azurecr.io como IP privado
az network private-dns zone create --resource-group {rg} --name privatelink.azurecr.io
az network private-dns link vnet create --resource-group {rg} \
  --zone-name privatelink.azurecr.io --name {registry}-dns-link --virtual-network {vnet} --registration-enabled false
az network private-endpoint dns-zone-group create --resource-group {rg} \
  --endpoint-name {registry}-pe --name default \
  --private-dns-zone privatelink.azurecr.io --zone-name registry

# 3. Opcionalmente, desativa por completo o acesso público
az acr update --name {registry} --public-network-enabled false

# Gerencia aprovações de conexão
az acr private-endpoint-connection list --registry-name {registry} --output table
az acr private-endpoint-connection approve --registry-name {registry} --name {connection}
```

Notas:

- Cada ponto de extremidade privado cria registros para o registro **e** seus pontos de extremidade de dados (`{registry}.{region}.data.azurecr.io`). Registros com replicação geográfica precisam de um registro de dados por região.
- Com o acesso público desativado, os agentes padrão do ACR Tasks não conseguem acessar o registro. Use um conjunto de agentes dedicado anexado a uma sub-rede da VNet ou ative serviços confiáveis **e** a política de desvio de rede para tarefas (consulte abaixo).

## Regras de rede pública

Restrinja o acesso público a IPs específicos em vez de tornar o acesso totalmente privado (ou antes de fazê-lo):

```bash
# Nega por padrão e depois permite intervalos específicos
az acr update --name {registry} --default-action Deny
az acr network-rule add --name {registry} --ip-address 203.0.113.0/24
az acr network-rule list --name {registry}
az acr network-rule remove --name {registry} --ip-address 203.0.113.0/24

# Permite serviços confiáveis do Azure (por exemplo, Defender, ACI e importação de imagem) no firewall
az acr update --name {registry} --allow-trusted-services true
```

⚠️ **Desde 1º de junho de 2025, somente `--allow-trusted-services` NÃO é suficiente para ACR Tasks que usam uma identidade gerenciada atribuída pelo sistema**. Sem a política de desvio de rede para tarefas, as execuções recebem erros 403 em registros com restrição de rede. Ative-a explicitamente:

```bash
az resource update \
  --namespace Microsoft.ContainerRegistry --resource-type registries \
  --name {registry} --resource-group {rg} \
  --api-version 2025-06-01-preview \
  --set properties.networkRuleBypassAllowedForTasks=true
```

Alternativas que evitam completamente o desvio: execute as tarefas em um conjunto de agentes anexado à VNet ou execute `acr purge` localmente com o [binário acr-cli](https://github.com/azure/acr-cli). Tarefas que usam uma identidade atribuída pelo usuário não são afetadas.

## Pontos de extremidade de dados dedicados

Forneça aos downloads de camadas FQDNs estáveis e específicos do registro (`{registry}.{region}.data.azurecr.io`) em vez de pontos de extremidade de armazenamento compartilhados. Isso simplifica as regras de firewall no cliente:

```bash
az acr update --name {registry} --data-endpoint-enabled true
az acr show-endpoints --name {registry}
```

## Registro conectado

Espelho local/na borda de IoT de um registro da nuvem:

```bash
# O registro pai deve ter um ponto de extremidade de dados dedicado
az acr update --name {registry} --data-endpoint-enabled true

az acr connected-registry create --registry {registry} --name {connected-name} \
  --repository "app" "hello-world" \
  --mode ReadOnly            # ou ReadWrite

az acr connected-registry list --registry {registry} --output table
az acr connected-registry get-settings --registry {registry} --name {connected-name} \
  --parent-protocol https --generate-password 1
az acr connected-registry deactivate --registry {registry} --name {connected-name}
```

## Fluxos de transferência de registros

Mova imagens entre nuvens/locatários desconectados por meio de blobs de armazenamento (extensão `acrtransfer`):

```bash
az extension add --name acrtransfer

# Exporta do registro de origem para um contêiner de armazenamento (token SAS no Key Vault)
az acr export-pipeline create --resource-group {rg} --registry {src-registry} \
  --name export-pipe \
  --secret-uri https://{vault}.vault.azure.net/secrets/{sas-secret} \
  --storage-container-uri https://{account}.blob.core.windows.net/{container}

# Importa no destino
az acr import-pipeline create --resource-group {rg} --registry {dst-registry} \
  --name import-pipe \
  --secret-uri https://{vault}.vault.azure.net/secrets/{sas-secret} \
  --storage-container-uri https://{account}.blob.core.windows.net/{container}

# Executa uma exportação
az acr pipeline-run create --resource-group {rg} --registry {src-registry} \
  --pipeline export-pipe --name run1 --pipeline-type export \
  --artifacts app:v1 app:v2 --storage-blob transfer-blob-1
```

Para cópias simples na mesma nuvem, prefira `az acr import` (consulte `images-and-artifacts.md`).
