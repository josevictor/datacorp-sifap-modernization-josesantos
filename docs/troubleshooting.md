# Solução de problemas consolidada

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Solução de problemas**

**Um guia de diagnóstico e resolução dos erros mais comuns da imersão** — use `Ctrl+F` para pesquisar o sintoma.

| Campo | Valor |
|---|---|
| **Público-alvo** | O time inteiro |
| **Como usar** | Use `Ctrl+F` para pesquisar o sintoma. Se não o encontrar, consulte [FAQ.md](FAQ.md) |
| **Resultado esperado** | O problema é resolvido ao seguir os passos descritos |

---

## Sumário

- [Setup e ambiente](#setup-e-ambiente)
- [Copilot, agentes e personas](#copilot-agentes-e-personas)
- [Spec-Kit e EARS](#spec-kit-e-ears)
- [Backend — Java e Spring Boot](#backend--java-e-spring-boot)
- [Frontend — Next.js e Node](#frontend--nextjs-e-node)
- [Docker](#docker)
- [Git e GitHub](#git-e-github)
- [Terraform e Azure](#terraform-e-azure)
- [Plano B — indisponibilidade do Copilot](#plano-b--indisponibilidade-do-copilot)

---

## Setup e ambiente

### Ferramentas locais ausentes (Java, Node, Maven)

| Campo | Detalhes |
|---|---|
| **Sintoma** | Uma mensagem de erro "command not found" para `java`, `node` ou `mvn` |
| **Causa provável** | As ferramentas locais ainda não foram instaladas |
| **Correção** | Instale as versões especificadas em [`00-SETUP.md`](../00-SETUP.md) e valide-as com `java -version`, `node --version` e `git --version` |
| **Como confirmar** | Os três comandos retornam a versão esperada sem erros |

### "git: command not found" no terminal do VS Code (Mac)

| Campo | Detalhes |
|---|---|
| **Sintoma** | Ocorre um erro ao tentar executar qualquer comando `git` |
| **Causa provável** | As ferramentas de CLI do Xcode não estão instaladas |
| **Correção** | Execute `xcode-select --install` e siga o instalador |
| **Como confirmar** | `git --version` retorna uma versão sem erros |

---

## Copilot, agentes e personas

### O comando de barra não aparece no GitHub Copilot

| Campo | Detalhes |
|---|---|
| **Sintoma** | `/ears-convert`, `/tdd` ou outros comandos não aparecem nas sugestões |
| **Causa provável** | O VS Code não recarregou o diretório `.github/` consolidado, ou a janela foi aberta fora da raiz do repositório |
| **Correção** | Confirme que `.github/prompts/` contém arquivos e recarregue a janela: `Cmd+Shift+P` → _Developer: Reload Window_ |
| **Como confirmar** | Os comandos aparecem quando você digita `/` no GitHub Copilot |

> [!CAUTION]
> Nunca crie cópias paralelas de agentes, prompts ou skills fora de `.github/`. Essa é a única fonte ativa e não deve ser editada.

### "Não consigo selecionar `@archaeologist` no GitHub Copilot"

| Campo | Detalhes |
|---|---|
| **Sintoma** | O agente `@archaeologist` não aparece no seletor do GitHub Copilot |
| **Causa 1** | O diretório `06-stage-agents/` não está no workspace |
| **Causa 2** | A extensão GitHub Copilot Chat está desatualizada |
| **Correção** | Execute `ls 06-stage-agents/` para confirmar que o diretório está presente. Atualize a extensão na visualização Extensions do VS Code |
| **Como confirmar** | O agente aparece na lista suspensa do GitHub Copilot |

### O Copilot responde sem o contexto relevante

| Campo | Detalhes |
|---|---|
| **Sintoma** | Respostas genéricas sem relação com o SIFAP (Sistema de Fiscalização e Administração de Pagamentos) ou com o estágio atual |
| **Causa provável** | Nenhum agente de estágio está selecionado, ou o agente errado está selecionado |
| **Correção** | Confirme o estágio atual com o time e selecione o agente correspondente na lista suspensa do GitHub Copilot |
| **Como confirmar** | As respostas passam a mencionar o estágio e o contexto do sistema legado |

### "Quero usar o modo Plan, mas somente Ask está disponível"

| Campo | Detalhes |
|---|---|
| **Sintoma** | O modo Plan não está disponível |
| **Causa provável** | A extensão do Copilot está desatualizada |
| **Correção** | Atualize a extensão GitHub Copilot Chat no VS Code |
| **Como confirmar** | O modo Plan aparece no seletor de modos |

---

## Spec-Kit e EARS

### "`specify version` retorna command not found"

| Campo | Detalhes |
|---|---|
| **Sintoma** | Ocorre um erro ao executar qualquer comando `specify` |
| **Causa provável** | O Spec-Kit não está instalado |
| **Correção** | Execute os comandos abaixo |
| **Como confirmar** | `specify version` retorna um número de versão |

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify version
```

### A CI rejeitou o PR: `missing source_legacy`

| Campo | Detalhes |
|---|---|
| **Sintoma** | A CI bloqueia o pull request com um erro de rastreabilidade |
| **Causa provável** | Um ou mais requisitos EARS não incluem uma linha `source_legacy:` |
| **Correção** | Abra `specs/<NNN>-<feature>/spec.md`, localize os REQ-IDs sem `source_legacy:` e adicione o campo apontando para `01-archaeology/legacy-sifap/...#L<linha>` ou marcando-o como `[GREENFIELD] <motivo>` |
| **Como confirmar** | A CI passa na próxima execução |

Consulte [`07-concepts/05-ears-notation.md`](../07-concepts/05-ears-notation.md) para ver o formato correto.

### `/speckit.clarify` está fazendo perguntas demais

| Campo | Detalhes |
|---|---|
| **Sintoma** | O comando faz dez ou mais perguntas |
| **Causa** | Isso não é um problema: é o comportamento esperado |
| **Ação** | Responda a todas as perguntas. Cada resposta ajuda a evitar um bug futuro |

---

## Backend — Java e Spring Boot

### O backend não inicia — erro de conexão com o Postgres

| Campo | Detalhes |
|---|---|
| **Sintoma** | Ocorre um erro `Connection refused` ou semelhante quando o backend inicia |
| **Causa provável** | O Postgres não está em execução, ou a URL em `application.yml` está incorreta |
| **Correção** | Verifique `application.yml` e inicie o Postgres pelo método definido pelo time (local, Testcontainers ou Docker Compose) |
| **Como confirmar** | O backend inicia e responde em `/actuator/health` |

### Flyway: `Migration checksum mismatch`

| Campo | Detalhes |
|---|---|
| **Sintoma** | Ocorre um erro do Flyway quando o backend inicia |
| **Causa provável** | Um arquivo de migração existente foi editado depois de ser aplicado |
| **Correção** | Restaure a versão original usando `git log` e crie um novo arquivo `V<N+1>__descricao.sql` |
| **Como confirmar** | O backend inicia sem erros do Flyway |

> [!CAUTION]
> Nunca edite arquivos de migração que já foram aplicados (V1, V2, V3...). Sempre crie um novo arquivo com o próximo número de versão.

### Testcontainers: `Could not find a valid Docker environment`

| Campo | Detalhes |
|---|---|
| **Sintoma** | Os testes que usam Testcontainers falham com um erro de ambiente do Docker |
| **Causa provável** | O Docker não está em execução, ou o socket usa um caminho fora do padrão |
| **Correção (macOS)** | `export DOCKER_HOST=unix:///var/run/docker.sock` ou `export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock` |
| **Como confirmar** | Os testes passam na próxima execução |

---

## Frontend — Next.js e Node

### O frontend exibe `ECONNREFUSED localhost:8080`

| Campo | Detalhes |
|---|---|
| **Sintoma** | A página do frontend exibe um erro de conexão recusada |
| **Causa provável** | O backend não está em execução ou usa outra porta |
| **Correção** | Confirme que o backend está em execução e que a URL do frontend aponta para a porta correta |
| **Como confirmar** | A página carrega os dados normalmente |

### `Module not found: shadcn/ui`

| Campo | Detalhes |
|---|---|
| **Sintoma** | Ocorre um erro de módulo não encontrado quando o frontend inicia |
| **Causa provável** | As dependências não estão instaladas |
| **Correção** | `cd frontend && npm install` |
| **Como confirmar** | O frontend inicia sem erros de módulo |

---

## Docker

### `Cannot connect to the Docker daemon`

| Campo | Detalhes |
|---|---|
| **Sintoma** | Todos os comandos Docker falham com um erro do daemon |
| **Causa provável** | O Docker Desktop está parado |
| **Correção** | Abra o Docker Desktop e aguarde o serviço iniciar por completo |
| **Como confirmar** | `docker ps` retorna a lista de contêineres sem erros |

### `port is already allocated`

| Campo | Detalhes |
|---|---|
| **Sintoma** | O contêiner não inicia por causa de um conflito de porta |
| **Causa provável** | A porta 5432, 8080 ou 3000 já está em uso por outro processo |
| **Correção** | Execute `lsof -i :8080` para identificar e encerrar o processo, ou altere a porta na configuração local |
| **Como confirmar** | O contêiner inicia sem erro de porta |

### O Docker Desktop relata `Out of memory`

| Campo | Detalhes |
|---|---|
| **Sintoma** | Os contêineres falham ou ficam lentos, e aparece um aviso de memória |
| **Causa provável** | O limite de RAM alocado ao Docker Desktop é muito baixo |
| **Correção** | Docker Desktop → Settings → Resources → Memory → 8 GB ou mais |
| **Como confirmar** | Os contêineres iniciam e respondem normalmente |

---

## Git e GitHub

### Push rejeitado: `protected branch`

| Campo | Detalhes |
|---|---|
| **Sintoma** | `git push` é rejeitado com uma mensagem de branch protegida |
| **Causa provável** | Houve uma tentativa de push direto para `main` ou `develop` |
| **Correção** | Crie uma branch e abra um pull request. Consulte [`00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md) |
| **Como confirmar** | O pull request é criado com sucesso |

### Conflito de merge

| Campo | Detalhes |
|---|---|
| **Sintoma** | Marcadores `<<<<<<<` aparecem nos arquivos durante um merge ou rebase |
| **Causa provável** | Alguém alterou o mesmo arquivo em `develop` antes de você |
| **Correção** | Execute o bloco abaixo, resolva os conflitos manualmente e conclua o rebase |
| **Como confirmar** | `git status` não mostra mais arquivos com conflitos |

```bash
git fetch origin
git rebase origin/develop
# Resolva os conflitos nos arquivos que contêm marcadores
git add <file>
git rebase --continue
```

### Commit feito acidentalmente diretamente em `develop`

```bash
git reset --soft HEAD~1
git stash
git checkout -b nova-branch
git stash pop
git commit -m "..."
```

### `gh: command not found`

| Campo | Detalhes |
|---|---|
| **Sintoma** | Ocorre um erro ao usar qualquer comando `gh` |
| **Causa provável** | O GitHub CLI não está instalado |
| **Correção** | `brew install gh && gh auth login` |
| **Como confirmar** | `gh --version` retorna uma versão sem erros |

---

## Terraform e Azure

### `Error: building AzureRM Client`

| Campo | Detalhes |
|---|---|
| **Sintoma** | O Terraform falha ao inicializar o provider do Azure |
| **Causa provável** | A sessão do Azure CLI expirou ou não foi iniciada |
| **Correção** | Execute `az login` |
| **Como confirmar** | `terraform plan` é executado sem erros de autenticação |

### `terraform plan` mostra centenas de novos recursos

| Campo | Detalhes |
|---|---|
| **Sintoma** | A saída de `plan` lista muitos recursos para criar |
| **Causa** | O arquivo de estado está vazio: esse é o comportamento esperado na primeira execução |
| **Ação** | Revise o plano. Não execute `apply`. |

> [!CAUTION]
> A imersão autoriza somente `terraform plan`. Executar `terraform apply` cria recursos reais do Azure e gera custos imediatamente.

---

## Plano B — indisponibilidade do Copilot

Se o GitHub Copilot parar de responder por mais de cinco minutos:

> [!WARNING]
> Não espere passivamente. A imersão dura oito horas, e cada minuto ocioso tem um custo alto para o time.

- [ ] **Recarregue** — tente `Cmd+Shift+P` → _Reload Window_. Se o Copilot voltar, continue normalmente.
- [ ] **Trabalhe manualmente** — se ele continuar offline, volte aos modelos e artefatos que o time já produziu.
- [ ] **Estruture o próximo artefato** — use as evidências disponíveis sem inventar dados.
- [ ] **Documente no PR** — escreva: _"Concluído manualmente em X min (Copilot offline)"_. Isso sustenta o relatório do Estágio 4.
- [ ] **Coordene com a dupla que receberá** — combine que o artefato pode estar menos refinado que o habitual.

A CI continua validando as mudanças mesmo quando o Copilot está offline. O trabalho não para.

| Artefato sem Copilot | Próximo passo |
|---|---|
| EARS no Estágio 2 | Use as descobertas rastreáveis e o fluxo do [Spec-Kit](../09-cheat-sheets/spec-kit-workflow.md) |
| ADR no Estágio 2 | Preencha o [modelo de ADR](adr/0000-template.md) |
| Implementação no Estágio 3 | Revise os requisitos EARS priorizados, os DDMs e as decisões do time |
| Issue para o Agent no Estágio 4 | Escreva o contexto, os critérios de aceitação e a rastreabilidade da mudança |

---

## Quando nenhuma das soluções acima funcionar

| Tempo bloqueado | Ação |
|---|---|
| 5 min | Leia o erro novamente com atenção. Use o modo Ask do GitHub Copilot: _"O que significa este erro: `<cole o erro>`"_ |
| 10 min | Peça ajuda à sua dupla |
| 20 min | Levante a mão para o facilitador (regra da §6 do TEAM-FLOW) |
| 30 min | Pause esta tarefa e trabalhe em outra enquanto alguém ajuda |

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Kit em pt-BR](../README.md)<br/><sub>Ponto de entrada principal.</sub> | [FAQ](FAQ.md)<br/><sub>Perguntas frequentes.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
