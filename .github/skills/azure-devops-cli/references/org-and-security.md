# Organização, segurança e administração

## Sumário

- [Projetos](#projetos)
- [Gerenciamento de extensões](#gerenciamento-de-extensões)
- [Pontos de extremidade de serviço](#pontos-de-extremidade-de-serviço)
- [Equipes](#equipes)
- [Usuários](#usuários)
- [Grupos de segurança](#grupos-de-segurança)
- [Permissões de segurança](#permissões-de-segurança)
- [Wikis](#wikis)
- [Administração](#administração)
- [Extensões do DevOps](#extensões-do-devops)

---

## Projetos

### Listar projetos

```bash
az devops project list --organization https://dev.azure.com/{org}
az devops project list --top 10 --output table
```

### Criar projeto

```bash
az devops project create \
  --name myNewProject \
  --organization https://dev.azure.com/{org} \
  --description "Meu novo projeto do DevOps" \
  --source-control git \
  --visibility private
```

### Exibir detalhes do projeto

```bash
az devops project show --project {project-name} --org https://dev.azure.com/{org}
```

### Excluir projeto

```bash
az devops project delete --id {project-id} --org https://dev.azure.com/{org} --yes
```

## Gerenciamento de extensões

### Listar extensões

```bash
# Listar extensões disponíveis
az extension list-available --output table

# Listar extensões instaladas
az extension list --output table
```

### Gerenciar a extensão do Azure DevOps

```bash
# Instalar a extensão do Azure DevOps
az extension add --name azure-devops

# Atualizar a extensão do Azure DevOps
az extension update --name azure-devops

# Remover extensão
az extension remove --name azure-devops

# Instalar a partir de um caminho local
az extension add --source ~/extensions/azure-devops.whl
```

## Pontos de extremidade de serviço

### Listar pontos de extremidade de serviço

```bash
az devops service-endpoint list --project {project}
az devops service-endpoint list --project {project} --output table
```

### Exibir ponto de extremidade de serviço

```bash
az devops service-endpoint show --id {endpoint-id} --project {project}
```

### Criar ponto de extremidade de serviço

```bash
# Usar um arquivo de configuração
az devops service-endpoint create --service-endpoint-configuration endpoint.json --project {project}
```

### Excluir ponto de extremidade de serviço

```bash
az devops service-endpoint delete --id {endpoint-id} --project {project} --yes
```

## Equipes

### Listar equipes

```bash
az devops team list --project {project}
```

### Exibir equipe

```bash
az devops team show --team {team-name} --project {project}
```

### Criar equipe

```bash
az devops team create \
  --name {team-name} \
  --description "Descrição da equipe" \
  --project {project}
```

### Atualizar equipe

```bash
az devops team update \
  --team {team-name} \
  --project {project} \
  --name "{new-team-name}" \
  --description "Descrição atualizada"
```

### Excluir equipe

```bash
az devops team delete --team {team-name} --project {project} --yes
```

### Exibir integrantes da equipe

```bash
az devops team list-member --team {team-name} --project {project}
```

## Usuários

### Listar usuários

```bash
az devops user list --org https://dev.azure.com/{org}
az devops user list --top 10 --output table
```

### Exibir usuário

```bash
az devops user show --user {user-id-or-email} --org https://dev.azure.com/{org}
```

### Adicionar usuário

```bash
az devops user add \
  --email user@example.com \
  --license-type express \
  --org https://dev.azure.com/{org}
```

### Atualizar usuário

```bash
az devops user update \
  --user {user-id-or-email} \
  --license-type advanced \
  --org https://dev.azure.com/{org}
```

### Remover usuário

```bash
az devops user remove --user {user-id-or-email} --org https://dev.azure.com/{org} --yes
```

## Grupos de segurança

### Listar grupos

```bash
# Listar todos os grupos do projeto
az devops security group list --project {project}

# Listar todos os grupos da organização
az devops security group list --scope organization

# Listar com filtragem
az devops security group list --project {project} --subject-types vstsgroup
```

### Exibir detalhes do grupo

```bash
az devops security group show --group-id {group-id}
```

### Criar grupo

```bash
az devops security group create \
  --name {group-name} \
  --description "Descrição do grupo" \
  --project {project}
```

### Atualizar grupo

```bash
az devops security group update \
  --group-id {group-id} \
  --name "{new-group-name}" \
  --description "Descrição atualizada"
```

### Excluir grupo

```bash
az devops security group delete --group-id {group-id} --yes
```

### Participações no grupo

```bash
# Listar participações
az devops security group membership list --id {group-id}

# Adicionar integrante
az devops security group membership add \
  --group-id {group-id} \
  --member-id {member-id}

# Remover integrante
az devops security group membership remove \
  --group-id {group-id} \
  --member-id {member-id} --yes
```

## Permissões de segurança

### Listar espaços de nomes

```bash
az devops security permission namespace list
```

### Exibir detalhes do espaço de nomes

```bash
# Exibir permissões disponíveis em um espaço de nomes
az devops security permission namespace show --namespace "GitRepositories"
```

### Listar permissões

```bash
# Listar permissões de usuário/grupo e espaço de nomes
az devops security permission list \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project}

# Listar para um token específico (repositório)
az devops security permission list \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}"
```

### Exibir permissões

```bash
az devops security permission show \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}"
```

### Atualizar permissões

```bash
# Conceder permissão
az devops security permission update \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask "Pull,Contribute"

# Negar permissão
az devops security permission update \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask 0
```

### Redefinir permissões

```bash
# Redefinir bits de permissão específicos
az devops security permission reset \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" \
  --permission-mask "Pull,Contribute"

# Redefinir todas as permissões
az devops security permission reset-all \
  --id {user-or-group-id} \
  --namespace "GitRepositories" \
  --project {project} \
  --token "repoV2/{project}/{repository-id}" --yes
```

## Wikis

### Listar wikis

```bash
# Listar todas as wikis do projeto
az devops wiki list --project {project}

# Listar todas as wikis da organização
az devops wiki list
```

### Exibir wiki

```bash
az devops wiki show --wiki {wiki-name} --project {project}
az devops wiki show --wiki {wiki-name} --project {project} --open
```

### Criar wiki

```bash
# Criar wiki do projeto
az devops wiki create \
  --name {wiki-name} \
  --project {project} \
  --type projectWiki

# Criar wiki de código a partir do repositório
az devops wiki create \
  --name {wiki-name} \
  --project {project} \
  --type codeWiki \
  --repository {repo-name} \
  --mapped-path /wiki
```

### Excluir wiki

```bash
az devops wiki delete --wiki {wiki-id} --project {project} --yes
```

### Páginas da wiki

```bash
# Listar páginas
az devops wiki page list --wiki {wiki-name} --project {project}

# Exibir página
az devops wiki page show \
  --wiki {wiki-name} \
  --path "/page-name" \
  --project {project}

# Criar página
az devops wiki page create \
  --wiki {wiki-name} \
  --path "/new-page" \
  --content "# Nova página\n\nConteúdo da página aqui..." \
  --project {project}

# Atualizar página
az devops wiki page update \
  --wiki {wiki-name} \
  --path "/existing-page" \
  --content "# Página atualizada\n\nNovo conteúdo..." \
  --project {project}

# Excluir página
az devops wiki page delete \
  --wiki {wiki-name} \
  --path "/old-page" \
  --project {project} --yes
```

## Administração

### Gerenciamento de banners

```bash
# Listar banners
az devops admin banner list

# Exibir detalhes do banner
az devops admin banner show --id {banner-id}

# Adicionar novo banner
az devops admin banner add \
  --message "Manutenção do sistema agendada" \
  --level info  # info, warning, error

# Atualizar banner
az devops admin banner update \
  --id {banner-id} \
  --message "Mensagem atualizada" \
  --level warning \
  --expiration-date "2025-12-31T23:59:59Z"

# Remover banner
az devops admin banner remove --id {banner-id}
```

## Extensões do DevOps

Gerencie as extensões instaladas em uma organização do Azure DevOps (diferentes das extensões da CLI).

```bash
# Listar extensões instaladas
az devops extension list --org https://dev.azure.com/{org}

# Pesquisar extensões no Marketplace
az devops extension search --search-query "docker"

# Exibir detalhes da extensão
az devops extension show --ext-id {extension-id} --org https://dev.azure.com/{org}

# Instalar extensão
az devops extension install \
  --ext-id {extension-id} \
  --org https://dev.azure.com/{org} \
  --publisher {publisher-id}

# Ativar extensão
az devops extension enable \
  --ext-id {extension-id} \
  --org https://dev.azure.com/{org}

# Desativar extensão
az devops extension disable \
  --ext-id {extension-id} \
  --org https://dev.azure.com/{org}

# Desinstalar extensão
az devops extension uninstall \
  --ext-id {extension-id} \
  --org https://dev.azure.com/{org} --yes
```
