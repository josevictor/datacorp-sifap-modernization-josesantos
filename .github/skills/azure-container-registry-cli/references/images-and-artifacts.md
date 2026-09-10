# Imagens e artefatos

## Sumário

- [Importar imagens (cópia no servidor)](#importar-imagens-cópia-no-servidor)
- [Repositórios e tags](#repositórios-e-tags)
- [Manifestos](#manifestos)
- [Remover tag versus excluir](#remover-tag-versus-excluir)
- [Limpar imagens antigas (acr purge)](#limpar-imagens-antigas-acr-purge)
- [Bloquear imagens](#bloquear-imagens)
- [Política de retenção e exclusão reversível](#política-de-retenção-e-exclusão-reversível)
- [Armazenamento temporário de artefatos (pull-through cache)](#armazenamento-temporário-de-artefatos-pull-through-cache)
- [Uso do armazenamento](#uso-do-armazenamento)

---

## Importar imagens (cópia no servidor)

Prefira esta opção a baixar e enviar com `docker pull` + `docker push`: ela não usa armazenamento local e mantém intactos os manifestos de várias arquiteturas:

```bash
# De um registro público
az acr import --name {registry} --source mcr.microsoft.com/hello-world:latest
az acr import --name {registry} --source docker.io/library/nginx:1.27 --image nginx:1.27

# De outro ACR no mesmo locatário (por ID de recurso, sem exigir credenciais)
az acr import --name {registry} \
  --source app:v1 \
  --registry /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.ContainerRegistry/registries/{src-registry}

# De um registro privado com credenciais
az acr import --name {registry} --source private.example.com/app:v1 \
  --username {user} --password {password}

# Sobrescreve uma tag existente
az acr import --name {registry} --source docker.io/library/nginx:1.27 --image nginx:1.27 --force
```

## Repositórios e tags

```bash
az acr repository list --name {registry} --output table

# Tags, das mais recentes para as mais antigas, com digest e timestamps
az acr repository show-tags --name {registry} --repository app \
  --orderby time_desc --detail --output table

az acr repository show --name {registry} --image app:v1        # atributos da tag
az acr repository show --name {registry} --repository app      # atributos do repositório
```

## Manifestos

```bash
# Metadados de todos os manifestos de um repositório (digest, tags, tamanho e timestamps)
az acr manifest list-metadata --registry {registry} --name app --output table

# Metadados/conteúdo bruto de um manifesto
az acr manifest show-metadata --registry {registry} --name app:v1
az acr manifest show --registry {registry} --name app@sha256:{digest}

# Localiza manifestos sem tag (órfãos)
az acr manifest list-metadata --registry {registry} --name app \
  --query "[?tags==null].digest" --output tsv
```

## Remover tag versus excluir

```bash
# Remove uma tag: somente a tag é removida; manifesto + camadas permanecem (download pelo digest)
az acr repository untag --name {registry} --image app:v1

# Exclui por tag: remove todo o manifesto e TODAS as outras tags que apontam para ele
az acr repository delete --name {registry} --image app:v1 --yes

# Exclui por digest (preciso)
az acr repository delete --name {registry} --image app@sha256:{digest} --yes

# Exclui um repositório inteiro
az acr repository delete --name {registry} --repository app --yes
```

⚠️ A exclusão por tag remove o manifesto subjacente. Outras tags da mesma imagem também desaparecem. Se quiser retirar somente o nome de uma tag, remova a tag primeiro.

## Limpar imagens antigas (acr purge)

`acr purge` é executado como uma ACR Task (contêiner `mcr.microsoft.com/acr/acr-cli`):

```bash
# SEMPRE faça primeiro uma simulação
az acr run --registry {registry} \
  --cmd "acr purge --filter 'app:.*' --ago 30d --untagged --dry-run" /dev/null

# Exclui tags com mais de 30 dias que correspondem à regex, além de manifestos sem tag
az acr run --registry {registry} \
  --cmd "acr purge --filter 'app:.*' --ago 30d --untagged" /dev/null

# Mantém as cinco tags mais recentes, independentemente da idade
az acr run --registry {registry} \
  --cmd "acr purge --filter 'app:.*' --ago 0d --keep 5 --untagged" /dev/null

# Agenda como tarefa noturna
az acr task create --registry {registry} --name purge-old-images \
  --cmd "acr purge --filter 'app:.*' --ago 30d --untagged" \
  --context /dev/null --schedule "0 3 * * *"
```

`--filter` recebe `repository:tag-regex` e pode ser repetido para vários repositórios.

⚠️ `--untagged` ignora `--ago`: ele exclui **todos** os manifestos sem tag, inclusive os criados há instantes (imagens durante o envio e artefatos de referência). Omita `--untagged` se manifestos recentes sem tag precisarem permanecer. O limite de idade aplica-se somente às imagens com tag que correspondem a `--filter`.

## Bloquear imagens

Impeça a sobrescrita ou exclusão de tags críticas (por exemplo, versões lançadas):

```bash
# Somente leitura: não pode ser sobrescrita nem excluída
az acr repository update --name {registry} --image app:v1 --write-enabled false

# Não pode ser excluída, mas ainda pode ser sobrescrita
az acr repository update --name {registry} --image app:v1 --delete-enabled false

# Desbloqueia
az acr repository update --name {registry} --image app:v1 --write-enabled true --delete-enabled true
```

## Política de retenção e exclusão reversível

São duas políticas distintas que **não podem ser ativadas ao mesmo tempo**. A política de retenção exige **Premium**. A exclusão reversível (versão prévia) está disponível em **todas as camadas**, mas não oferece suporte a registros com replicação geográfica nem com cache de artefatos.

```bash
# Política de retenção (Premium): exclui manifestos sem tag após N dias (0 = imediatamente)
az acr config retention update --registry {registry} \
  --status enabled --days 7 --type UntaggedManifests
az acr config retention show --registry {registry}

# Exclusão reversível (versão prévia, todas as camadas): recupera artefatos em 1-90 dias
az acr config soft-delete update --registry {registry} --status enabled --days 7
az acr repository list-deleted --name {registry}
az acr manifest restore --registry {registry} --name app:v1
```

## Armazenamento temporário de artefatos (pull-through cache)

Armazene temporariamente no registro as imagens de origem (Docker Hub, MCR, GHCR, quay.io e ECR Public). Isso evita limites de taxa e centraliza a procedência:

```bash
# Opcional: credenciais para a origem autenticada (os segredos ficam no Key Vault)
az acr credential-set create --registry {registry} --name dockerhub-creds \
  --login-server docker.io \
  --username-id https://{vault}.vault.azure.net/secrets/dh-user \
  --password-id https://{vault}.vault.azure.net/secrets/dh-pass

# Regra de armazenamento temporário: docker.io/library/* -> {registry}.azurecr.io/dockerhub/*
az acr cache create --registry {registry} --name dockerhub-cache \
  --source-repo "docker.io/library/*" --target-repo "dockerhub/*" \
  --cred-set dockerhub-creds

az acr cache list --registry {registry} --output table
```

Depois, `docker pull {registry}.azurecr.io/dockerhub/nginx:1.27` busca a imagem pelo armazenamento temporário.

## Uso do armazenamento

```bash
# Armazenamento consumido versus cota da SKU (Basic 10 GB/Standard 100 GB/Premium 500 GB inclusos)
az acr show-usage --name {registry} --output table
```

As camadas são desduplicadas e compartilhadas entre os repositórios. `show-usage` informa o armazenamento real faturável.
