# Itens de trabalho, caminhos de área e iterações

## Sumário

- [Itens de trabalho (Boards)](#itens-de-trabalho-boards)
- [Caminhos de área](#caminhos-de-área)
- [Iterações](#iterações)

---

## Itens de trabalho (Boards)

### Consultar itens de trabalho

```bash
# Consulta WIQL
az boards query \
  --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] = 'Active'"

# Consulta com formato de saída
az boards query --wiql "SELECT * FROM WorkItems" --output table
```

### Exibir item de trabalho

```bash
az boards work-item show --id {work-item-id}
az boards work-item show --id {work-item-id} --open
```

### Criar item de trabalho

```bash
# Item de trabalho básico
az boards work-item create \
  --title "Corrigir falha de entrada" \
  --type Bug \
  --assigned-to user@example.com \
  --description "As pessoas não conseguem entrar com SSO"

# Com área e iteração
az boards work-item create \
  --title "Nova funcionalidade" \
  --type "User Story" \
  --area "Project\\Area1" \
  --iteration "Project\\Sprint 1"

# Com campos personalizados
az boards work-item create \
  --title "Task" \
  --type Task \
  --fields "Priority=1" "Severity=2"

# Com comentário de discussão
az boards work-item create \
  --title "Problema" \
  --type Bug \
  --discussion "Investigação inicial concluída"

# Para um corpo longo de --discussion no Windows, consulte references/long-comments-on-windows.md.
# Resumo: use azps.ps1 no PowerShell ou recorra a 'az devops invoke'
# com --in-file quando não houver uma opção --file-path nativa.

# Abrir no navegador após a criação
az boards work-item create --title "Bug" --type Bug --open
```

### Atualizar item de trabalho

```bash
# Atualizar estado, título e pessoa responsável
az boards work-item update \
  --id {work-item-id} \
  --state "Active" \
  --title "Título atualizado" \
  --assigned-to user@example.com

# Mover para outra área
az boards work-item update \
  --id {work-item-id} \
  --area "{ProjectName}\\{Team}\\{Area}"

# Alterar a iteração
az boards work-item update \
  --id {work-item-id} \
  --iteration "{ProjectName}\\Sprint 5"

# Adicionar comentário/discussão
az boards work-item update \
  --id {work-item-id} \
  --discussion "Trabalho em andamento"

# Comentário longo no Windows: leia o corpo em uma variável do PowerShell e chame
# azps.ps1 em vez de az.cmd ou recorra a 'az devops invoke' com --in-file.
# Orientações completas em references/long-comments-on-windows.md.
#
# Exemplo em PowerShell:
#   $body = Get-Content -Raw .\comment.md
#   azps.ps1 boards work-item update --id 1234 --discussion $body

# Atualizar com campos personalizados
az boards work-item update \
  --id {work-item-id} \
  --fields "Priority=1" "StoryPoints=5"
```

### Excluir item de trabalho

```bash
# Exclusão reversível (pode ser restaurada)
az boards work-item delete --id {work-item-id} --yes

# Exclusão permanente
az boards work-item delete --id {work-item-id} --destroy --yes
```

### Relações entre itens de trabalho

```bash
# Listar relações
az boards work-item relation list --id {work-item-id}

# Listar tipos de relação aceitos
az boards work-item relation list-type

# Adicionar relação
az boards work-item relation add --id {work-item-id} --relation-type parent --target-id {parent-id}

# Remover relação
az boards work-item relation remove --id {work-item-id} --relation-id {relation-id}
```

## Caminhos de área

### Listar áreas do projeto

```bash
az boards area project list --project {project}
az boards area project show --path "Project\\Area1" --project {project}
```

### Criar área

```bash
az boards area project create --path "Project\\NewArea" --project {project}
```

### Atualizar área

```bash
az boards area project update \
  --path "Project\\OldArea" \
  --new-path "Project\\UpdatedArea" \
  --project {project}
```

### Excluir área

```bash
az boards area project delete --path "Project\\AreaToDelete" --project {project} --yes
```

### Gerenciamento de áreas da equipe

```bash
# Listar áreas da equipe
az boards area team list --team {team-name} --project {project}

# Adicionar área à equipe
az boards area team add \
  --team {team-name} \
  --path "Project\\NewArea" \
  --project {project}

# Remover área da equipe
az boards area team remove \
  --team {team-name} \
  --path "Project\\AreaToRemove" \
  --project {project}

# Atualizar área da equipe
az boards area team update \
  --team {team-name} \
  --path "Project\\Area" \
  --project {project} \
  --include-sub-areas true
```

## Iterações

### Listar iterações do projeto

```bash
az boards iteration project list --project {project}
az boards iteration project show --path "Project\\Sprint 1" --project {project}
```

### Criar iteração

```bash
az boards iteration project create --path "Project\\Sprint 1" --project {project}
```

### Atualizar iteração

```bash
az boards iteration project update \
  --path "Project\\OldSprint" \
  --new-path "Project\\NewSprint" \
  --project {project}
```

### Excluir iteração

```bash
az boards iteration project delete --path "Project\\OldSprint" --project {project} --yes
```

### Iterações da equipe

```bash
# Listar iterações da equipe
az boards iteration team list --team {team-name} --project {project}

# Adicionar iteração à equipe
az boards iteration team add \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}

# Remover iteração da equipe
az boards iteration team remove \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}

# Listar itens de trabalho da iteração
az boards iteration team list-work-items \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}
```

### Iterações padrão e da lista priorizada

```bash
# Definir a iteração padrão da equipe
az boards iteration team set-default-iteration \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}

# Exibir a iteração padrão
az boards iteration team show-default-iteration \
  --team {team-name} \
  --project {project}

# Definir a iteração da lista priorizada da equipe
az boards iteration team set-backlog-iteration \
  --team {team-name} \
  --path "Project\\Sprint 1" \
  --project {project}

# Exibir a iteração da lista priorizada
az boards iteration team show-backlog-iteration \
  --team {team-name} \
  --project {project}

# Exibir a iteração atual
az boards iteration team show --team {team-name} --project {project} --timeframe current
```
