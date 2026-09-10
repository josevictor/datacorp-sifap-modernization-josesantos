# Repositórios e solicitações de pull

## Sumário

- [Repositórios](#repositórios)
- [Importação de repositório](#importação-de-repositório)
- [Solicitações de pull](#solicitações-de-pull)
- [Referências Git](#referências-git)
- [Políticas de repositório](#políticas-de-repositório)

---

## Repositórios

### Listar repositórios

```bash
az repos list --org https://dev.azure.com/{org} --project {project}
az repos list --output table
```

### Exibir detalhes do repositório

```bash
az repos show --repository {repo-name} --project {project}
```

### Criar repositório

```bash
az repos create --name {repo-name} --project {project}
```

### Excluir repositório

```bash
az repos delete --id {repo-id} --project {project} --yes
```

### Atualizar repositório

```bash
az repos update --id {repo-id} --name {new-name} --project {project}
```

## Importação de repositório

### Importar repositório Git

```bash
# Importar de um repositório Git público
az repos import create \
  --git-source-url https://github.com/user/repo \
  --repository {repo-name}

# Importar com autenticação
az repos import create \
  --git-source-url https://github.com/user/private-repo \
  --repository {repo-name} \
  --user {username} \
  --password {password-or-pat}
```

## Solicitações de pull

### Criar solicitação de pull

```bash
# Criação básica de solicitação de pull
az repos pr create \
  --repository {repo} \
  --source-branch {source-branch} \
  --target-branch {target-branch} \
  --title "Título da solicitação de pull" \
  --description "Descrição da solicitação de pull" \
  --open

# Solicitação de pull com itens de trabalho
az repos pr create \
  --repository {repo} \
  --source-branch {source-branch} \
  --work-items 63 64

# Rascunho de solicitação de pull com revisores
az repos pr create \
  --repository {repo} \
  --source-branch feature/new-feature \
  --target-branch main \
  --title "Funcionalidade: nova operação" \
  --draft true \
  --reviewers user1@example.com user2@example.com \
  --required-reviewers lead@example.com \
  --labels "enhancement" "backlog"
```

### Listar solicitações de pull

```bash
# Todas as solicitações de pull
az repos pr list --repository {repo}

# Filtrar por status
az repos pr list --repository {repo} --status active

# Filtrar por pessoa criadora
az repos pr list --repository {repo} --creator {email}

# Saída como tabela
az repos pr list --repository {repo} --output table
```

### Exibir detalhes da solicitação de pull

```bash
az repos pr show --id {pr-id}
az repos pr show --id {pr-id} --open  # Abrir no navegador
```

### Atualizar solicitação de pull (concluir/abandonar/rascunho)

```bash
# Concluir solicitação de pull
az repos pr update --id {pr-id} --status completed

# Abandonar solicitação de pull
az repos pr update --id {pr-id} --status abandoned

# Definir como rascunho
az repos pr update --id {pr-id} --draft true

# Publicar o rascunho da solicitação de pull
az repos pr update --id {pr-id} --draft false

# Concluir automaticamente quando as políticas forem aprovadas
az repos pr update --id {pr-id} --auto-complete true

# Definir título e descrição
az repos pr update --id {pr-id} --title "Novo título" --description "Nova descrição"
```

### Obter localmente a solicitação de pull

```bash
# Obter a ramificação da solicitação de pull
az repos pr checkout --id {pr-id}

# Obter com um remoto específico
az repos pr checkout --id {pr-id} --remote-name upstream
```

### Votar na solicitação de pull

```bash
az repos pr set-vote --id {pr-id} --vote approve
az repos pr set-vote --id {pr-id} --vote approve-with-suggestions
az repos pr set-vote --id {pr-id} --vote reject
az repos pr set-vote --id {pr-id} --vote wait-for-author
az repos pr set-vote --id {pr-id} --vote reset
```

### Revisores da solicitação de pull

```bash
# Adicionar revisores
az repos pr reviewer add --id {pr-id} --reviewers user1@example.com user2@example.com

# Listar revisores
az repos pr reviewer list --id {pr-id}

# Remover revisores
az repos pr reviewer remove --id {pr-id} --reviewers user1@example.com
```

### Itens de trabalho da solicitação de pull

```bash
# Adicionar itens de trabalho à solicitação de pull
az repos pr work-item add --id {pr-id} --work-items {id1} {id2}

# Listar itens de trabalho da solicitação de pull
az repos pr work-item list --id {pr-id}

# Remover itens de trabalho da solicitação de pull
az repos pr work-item remove --id {pr-id} --work-items {id1}
```

### Políticas da solicitação de pull

```bash
# Listar políticas de uma solicitação de pull
az repos pr policy list --id {pr-id}

# Colocar a avaliação de política de uma solicitação de pull na fila
az repos pr policy queue --id {pr-id} --evaluation-id {evaluation-id}
```

## Referências Git

### Listar referências (ramificações)

```bash
az repos ref list --repository {repo}
az repos ref list --repository {repo} --query "[?name=='refs/heads/main']"
```

### Criar referência (ramificação)

```bash
az repos ref create --name refs/heads/new-branch --object-type commit --object {commit-sha}
```

### Excluir referência (ramificação)

```bash
az repos ref delete --name refs/heads/old-branch --repository {repo} --project {project}
```

### Bloquear/desbloquear ramificação

```bash
az repos ref lock --name refs/heads/main --repository {repo} --project {project}
az repos ref unlock --name refs/heads/main --repository {repo} --project {project}
```

## Políticas de repositório

### Listar todas as políticas

```bash
az repos policy list --repository {repo-id} --branch main
```

### Criar/atualizar/excluir política

```bash
# Criar a partir de um arquivo de configuração
az repos policy create --config policy.json

# Atualizar
az repos policy update --id {policy-id} --config updated-policy.json

# Excluir
az repos policy delete --id {policy-id} --yes
```

### Política de quantidade de aprovações

```bash
az repos policy approver-count create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --minimum-approver-count 2 \
  --creator-vote-counts true
```

### Política de build

```bash
az repos policy build create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --build-definition-id {definition-id} \
  --queue-on-source-update-only true \
  --valid-duration 720
```

### Política de vinculação de itens de trabalho

```bash
az repos policy work-item-linking create \
  --blocking true \
  --branch main \
  --enabled true \
  --repository-id {repo-id}
```

### Política de revisão obrigatória

```bash
az repos policy required-reviewer create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --required-reviewers user@example.com
```

### Política de estratégia de mesclagem

```bash
az repos policy merge-strategy create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --allow-squash true \
  --allow-rebase true \
  --allow-no-fast-forward true
```

### Política de diferenciação entre maiúsculas e minúsculas

```bash
az repos policy case-enforcement create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id}
```

### Política de comentário obrigatório

```bash
az repos policy comment-required create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id}
```

### Política de tamanho de arquivo

```bash
az repos policy file-size create \
  --blocking true \
  --enabled true \
  --branch main \
  --repository-id {repo-id} \
  --maximum-file-size 10485760  # 10 MB em bytes
```
