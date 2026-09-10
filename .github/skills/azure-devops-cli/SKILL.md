---
name: "azure-devops-cli"
description: "Use ao gerenciar recursos do Azure DevOps pela CLI: projetos, repositórios, pipelines, compilações, solicitações de pull, itens de trabalho, artefatos e pontos de extremidade de serviço. Aplica-se somente quando uma equipe se integra a uma organização existente do Azure DevOps. Os gatilhos incluem \"az devops\", \"az pipelines\", \"az boards\", \"az repos\" e \"automação do Azure DevOps\"."
---
# Azure DevOps CLI

Gerencie recursos do Azure DevOps com a CLI do Azure e a extensão `azure-devops`.

> [!NOTE]
> A fonte oficial deste kit para trabalho, código e integração contínua (CI) é o **GitHub** (GitHub Issues, GitHub Pull Requests, GitHub Actions e GitHub Projects). Use esta habilidade somente quando uma equipe também precisar operar uma organização existente do Azure DevOps. Não migre o fluxo de trabalho do kit para o Azure DevOps.

## Quando usar

- "Crie uma solicitação de pull em nosso repositório do Azure DevOps pela CLI."
- "Coloque uma execução de pipeline na fila e acompanhe seu status sem abrir o portal."
- "Atualize itens de trabalho em massa com um script."
- "Liste as políticas de ramificação de nosso repositório do Azure DevOps."

## Pré-requisitos

Instale a CLI do Azure e a extensão do Azure DevOps:

```bash
brew install azure-cli                                     # macOS
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash     # Linux
az extension add --name azure-devops
```

## Autenticação

Autentique-se com um token de acesso pessoal (Personal Access Token, PAT) e defina os padrões para não repetir `--org`/`--project`:

```bash
export AZURE_DEVOPS_EXT_PAT="<your-pat>"
az devops login --organization https://dev.azure.com/{org}
az devops configure --defaults organization=https://dev.azure.com/{org} project={project}
az devops configure --list
```

> [!WARNING]
> Nunca fixe um PAT em um script, confirmação no repositório ou comando que será registrado. Forneça-o pela variável de ambiente `AZURE_DEVOPS_EXT_PAT` (ou por um cofre de segredos) e limite-o às permissões mínimas necessárias.

> [!NOTE]
> Substitua a URL legada `https://{org}.visualstudio.com` por `https://dev.azure.com/{org}`.

## Estrutura da CLI

```text
az devops          Comandos principais do DevOps
├── admin          Administração (banner)
├── extension      Gerenciamento de extensões
├── project        Projetos de equipe
├── security       Operações de segurança (grupo, permissão)
├── service-endpoint   Conexões de serviço
├── team           Equipes
├── user           Usuários
├── wiki           Wikis
├── configure      Definir padrões
├── invoke         Invocar a API REST
├── login / logout Autenticar / limpar credenciais

az pipelines       Azure Pipelines
├── agent / pool / queue   Agentes, conjuntos e filas
├── build          Compilações
├── folder         Pastas de pipelines
├── release        Lançamentos
├── runs           Execuções de pipelines
└── variable / variable-group   Variáveis e grupos

az boards          Azure Boards
├── area           Caminhos de área
├── iteration      Iterações
└── work-item      Itens de trabalho

az repos           Azure Repos
├── import         Importações Git
├── policy         Políticas de ramificação
├── pr             Solicitações de pull
└── ref            Referências Git

az artifacts       Azure Artifacts
└── universal      Pacotes universais
```

## Arquivos de referência

Leia o arquivo de referência relevante para a tarefa. Cada arquivo contém a sintaxe completa dos comandos e exemplos de seu domínio.

| Arquivo | Quando ler | Abrange |
|---|---|---|
| [references/repos-and-prs.md](references/repos-and-prs.md) | Repositórios, ramificações, solicitações de pull e políticas de ramificação | Repositórios, importação, solicitações de pull (criação/listagem/votação/revisores/políticas), referências Git e políticas de ramificação |
| [references/pipelines-and-builds.md](references/pipelines-and-builds.md) | Pipelines, compilações, lançamentos e artefatos | Criação, leitura, atualização e exclusão (CRUD) de pipelines, execuções, compilações, lançamentos, obtenção e envio de artefatos |
| [references/boards-and-iterations.md](references/boards-and-iterations.md) | Itens de trabalho, ciclos e caminhos de área | Itens de trabalho (WIQL/criação/atualização/relações), caminhos de área e iterações da equipe |
| [references/variables-and-agents.md](references/variables-and-agents.md) | Variáveis de pipeline e conjuntos de agentes | Variáveis de pipeline, grupos de variáveis, pastas de pipelines e conjuntos/filas de agentes |
| [references/org-and-security.md](references/org-and-security.md) | Projetos, equipes, usuários, permissões e wikis | Projetos, extensões, equipes, usuários, grupos/permissões de segurança, pontos de extremidade de serviço, wikis e administração |
| [references/advanced-usage.md](references/advanced-usage.md) | Formatação da saída e consultas JMESPath | Formatos de saída, consultas JMESPath, argumentos globais, parâmetros comuns e apelidos Git |
| [references/workflows-and-patterns.md](references/workflows-and-patterns.md) | Scripts de automação, práticas recomendadas, tratamento de erros | Fluxos comuns, práticas recomendadas, tratamento de erros, padrões de scripts, exemplos reais |
| [references/long-comments-on-windows.md](references/long-comments-on-windows.md) | Falhas no Windows com valores longos de `--discussion`, `--description` ou `--content` | O limite de 8.191 caracteres do `cmd.exe` no `az.cmd`, detecção do interpretador de comandos e três soluções verificadas (`azps.ps1`, `--file-path` nativo, `az devops invoke --in-file`) |

## Modelo de saída

Entregue uma sequência de comandos executável e os identificadores retornados:

```bash
az repos pr create \
  --repository sifap \
  --source-branch feature/import-report \
  --target-branch main \
  --title "Adicionar relatório de importação" \
  --description "Implementa REQ-042" \
  --output table
az pipelines run --name sifap-ci --branch feature/import-report --output table
```

Resuma o resultado:

```text
Solicitação de pull: !128 sifap feature/import-report -> main (ativa)
Pipeline: execução #345 de sifap-ci colocada na fila em feature/import-report
```

## Critérios de qualidade

- [ ] `az devops configure --list` mostra a organização e o projeto padrão pretendidos.
- [ ] O PAT é fornecido por `AZURE_DEVOPS_EXT_PAT` ou por um cofre de segredos, nunca fixado nem registrado.
- [ ] Os comandos especificam `--output table`/`--output json` explicitamente para que os resultados possam ser processados.
- [ ] Valores longos de `--description`/`--discussion` no Windows usam uma das soluções documentadas.
- [ ] A ação foi verificada (ID da solicitação de pull, da execução ou do item de trabalho retornado), em vez de ser considerada bem-sucedida sem comprovação.
