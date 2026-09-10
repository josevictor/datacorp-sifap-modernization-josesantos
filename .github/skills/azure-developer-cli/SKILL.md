---
name: "azure-developer-cli"
description: "Use ao projetar, criar, revisar, migrar ou solucionar problemas de projetos da Azure Developer CLI (azd) conforme as orientações atuais da Microsoft. Abrange azd, azure.yaml, modelos do AZD, Terraform (ou Bicep) em infra, ambientes e segredos do AZD, ganchos, fluxos de implantação e CI/CD gerenciado pelo azd. Os gatilhos incluem \"azd\", \"azure.yaml\", \"ambiente azd\", \"pipeline azd\" e \"azd up\"."
---
# Boas práticas da Azure Developer CLI

Use esta habilidade para produzir projetos `azd` sustentáveis, seguros e cientes do ambiente. Prefira as convenções do repositório quando elas já forem coerentes e faça a menor alteração completa que melhore o projeto. Esta habilidade ensina a estruturar e operar um projeto `azd`, mas não decide a arquitetura da carga de trabalho.

> [!NOTE]
> Esta habilidade pressupõe que a **CLI `azd`** esteja instalada e autenticada. Este kit padroniza a IaC em **Terraform (`azurerm ~> 3.x`)**. Portanto, trate o Terraform como o provedor em `infra/` e leia as orientações sobre Bicep abaixo apenas como referência.

## Quando usar

- "Configure um novo projeto azd para nossos serviços da camada de servidor e da interface."
- "Revise nosso azure.yaml e a estrutura de infra em busca de problemas."
- "Migre este modelo azd do Bicep para o Terraform."
- "Por que `azd provision` falha em nosso ambiente de homologação?"

## Comece pela descoberta do repositório

Antes de editar:

1. Localize `azure.yaml`, o `infra.path` configurado, os projetos de código-fonte, os scripts de implantação, `.gitignore` e as definições dos fluxos automatizados.
2. Leia `azure.yaml` antes de deduzir os serviços ou o provedor de IaC.
3. Identifique se a tarefa é criar, migrar, revisar, implantar ou solucionar problemas.
4. Identifique o ambiente ativo somente quando uma operação específica do ambiente for necessária.
5. Leia a referência relevante:
   - Estrutura do repositório ou `azure.yaml`: [references/project-structure.md](references/project-structure.md)
   - Bicep, Terraform, parâmetros, saídas ou ambientes: [references/iac-and-environments.md](references/iac-and-environments.md)
   - Segredos, ganchos, CI/CD, implantação ou solução de problemas: [references/security-cicd-operations.md](references/security-cicd-operations.md)
   - Detalhes do produto que podem ter mudado: [references/official-docs.md](references/official-docs.md)

Não presuma o caminho padrão `infra`, o provedor Bicep padrão nem um único serviço quando `azure.yaml` indicar algo diferente.

## Aplique proteções de segurança

- Nunca versione `.azure`, arquivos `.env` de ambiente, credenciais, saídas de implantação com segredos, estado local do Terraform ou artefatos de implantação gerados.
- Nunca coloque segredos literais em `azure.yaml`, arquivos de parâmetros de IaC, ganchos, controle de versão, argumentos de comando que serão registrados ou saídas da IaC.
- Prefira identidades gerenciadas e RBAC. Use referências do Key Vault e `azd env set-secret` quando um segredo for inevitável.
- Antes de um comando capaz de criar, modificar ou excluir recursos do Azure, confirme o ambiente, a assinatura, o locatário (`tenant`), a região e o escopo esperado.
- Trate uma solicitação explícita para implantar, provisionar, destruir ou configurar um fluxo automatizado como aprovação para a ação nomeada. Caso contrário, pergunte antes de executar `azd up`, `azd provision`, `azd deploy`, `azd down` ou `azd pipeline config`.
- Não substitua Bicep por Terraform, Terraform por Bicep nem um serviço de hospedagem estabelecido, a menos que a pessoa solicite essa alteração arquitetural.
- Preserve os recursos e o estado pertencentes a elementos externos ao projeto `azd` atual.

## Use estes padrões

| Aspecto | Padrão preferencial |
| --- | --- |
| Manifesto do projeto | Um `azure.yaml` na raiz do repositório |
| Código da aplicação | `src/<service-name>` para cada serviço implantável de forma independente |
| Infraestrutura | `infra` com um ponto de entrada enxuto e módulos reutilizáveis |
| Provedor de IaC | Terraform neste kit; em outros casos, Bicep, a menos que o repositório ou a pessoa escolha Terraform |
| Ambientes de implantação | Ambientes nomeados separados para desenvolvimento, teste, homologação e produção |
| Estado local do AZD | `.azure/<environment-name>`, excluído do controle de versão |
| Estado de ambiente compartilhado | Ambientes remotos do AZD apoiados pelo Azure Blob Storage |
| Segredos | Primeiro identidade gerenciada/RBAC; depois referências do Key Vault |
| Scripts de automação | Scripts curtos e idempotentes em `scripts/azd` |
| Autenticação de CI | Federação de identidade da carga de trabalho/OIDC, quando houver suporte |
| Desenvolvimento rotineiro | `azd up` para fluxos simples; fases separadas para fluxos controlados |

## Fluxo de implementação

### 1. Modele a aplicação

- Defina uma entrada em `services` para cada componente implantável de forma independente.
- Mantenha estáveis as chaves dos serviços, pois elas participam da descoberta e da implantação dos recursos.
- Mapeie cada serviço para seus valores reais de `project`, `language` e `host`.
- Mantenha a infraestrutura compartilhada na IaC, em vez de inventar um serviço implantável fictício.
- Declare dependências com campos compatíveis de `azure.yaml`, em vez de depender da ordem dos arquivos.

### 2. Modele a infraestrutura

- Mantenha `main.bicep` ou `main.tf` como ponto de entrada da orquestração.
- Divida em módulos a infraestrutura reutilizável ou compreensível de forma independente.
- Parametrize valores específicos do ambiente. Não bifurque a árvore de IaC por ambiente.
- Produza somente valores estáveis e não secretos exigidos pela implantação ou configuração da aplicação.
- Use nomes determinísticos e tags consistentes que incluam o projeto e o ambiente.
- Adicione atribuições de função às identidades, em vez de distribuir chaves de serviço.
- Use camadas de infraestrutura somente quando escopos separados ou dependências de ciclo de vida as justificarem.

### 3. Modele os ambientes

- Use nomes previsíveis, como `<project>-dev` para ambientes compartilhados e `<alias>-dev` para ambientes pessoais.
- Use `azd env set`, `azd env unset` e `azd env set-secret` em vez de editar `.env` diretamente.
- Use `-e` ou `--environment` em scripts e automações para explicitar o destino.
- Use `azd env refresh` para sincronizar as saídas de implantação após outro agente alterar um ambiente.
- Configure o estado remoto do AZD quando uma equipe compartilhar o estado do ambiente.

### 4. Adicione ganchos somente para lacunas do ciclo de vida

- Prefira IaC declarativa e configuração nativa dos serviços a ganchos.
- Use ganchos da raiz para comportamentos de todo o projeto e ganchos de serviço para comportamentos específicos.
- Mantenha a lógica não trivial dos ganchos em scripts versionados em `scripts/azd`.
- Defina `shell` explicitamente. Forneça variantes `windows` e `posix` quando necessário.
- Torne os ganchos idempotentes, não interativos em CI e configure falha em caso de erro, a menos que a falha seja intencionalmente não bloqueante.
- Teste um gancho de forma independente com `azd hooks run <hook-name>`.

### 5. Crie CI/CD de forma intencional

- Mantenha a definição do fluxo automatizado com o modelo e revise as alterações geradas por `azd pipeline config`.
- Use credenciais federadas de curta duração quando houver suporte do provedor.
- Execute os testes e a validação de IaC antes do provisionamento.
- Use ambientes explícitos e `--no-prompt` na automação.
- Adicione ambientes de produção protegidos e critérios de aprovação.
- Para Terraform, configure o estado remoto protegido antes do fluxo automatizado e considere as limitações atuais de autenticação do AZD.

## Valide antes de concluir

Execute somente as verificações aplicáveis ao repositório:

```text
Aplicação: formatador, análise estática, verificação de tipos, compilação e testes existentes
Bicep:      az bicep build --file infra/main.bicep
Terraform:  terraform fmt -check -recursive
            terraform init -backend=false
            terraform validate
Ganchos do AZD: azd hooks run <hook-name>
Empacotamento: azd package
```

Para um what-if do Bicep ou um plano do Terraform, escolha o escopo e o ambiente de implantação corretos. Essas verificações podem autenticar no Azure ou ler o estado remoto. Portanto, siga as proteções de segurança.

Verifique se:

- Os caminhos de `azure.yaml` existem e as configurações dos serviços correspondem aos projetos de código-fonte.
- O ponto de entrada e o provedor de IaC estão de acordo com `azure.yaml`.
- As saídas de implantação obrigatórias correspondem às variáveis consumidas por serviços, ganchos e fluxos automatizados.
- `.gitignore` exclui `.azure`, segredos, estado local e artefatos gerados.
- Nenhum segredo aparece em conteúdo rastreado nem na saída de comandos.
- A documentação explica os pré-requisitos, a criação do ambiente, a implantação, a verificação e a limpeza.

## Informe o resultado

Informe:

- Os arquivos e comportamentos alterados.
- O provedor de IaC e as premissas de ambiente.
- As verificações realizadas.
- Todo comando que alteraria a nuvem e que não foi executado de forma intencional.
- Todo recurso beta ou em versão prévia do qual a solução depende.

Não afirme que a implantação foi bem-sucedida, a menos que o ambiente de destino tenha sido realmente implantado e verificado.

## Modelo de saída

Informe a alteração em um bloco de status curto:

```text
Revisão do projeto azd: sifap-modern
Alterado: azure.yaml (serviço web adicionado), infra/main.tf (módulo de armazenamento adicionado)
Provedor de IaC: Terraform (azurerm ~> 3.x); ambiente: sifap-dev
Verificações executadas: terraform fmt -check, terraform validate, azd package
Não executado: azd provision (alteraria o Azure); exige aprovação explícita
Recursos em versão prévia: nenhum
```

## Critérios de qualidade

- [ ] Os caminhos dos serviços em `azure.yaml` existem e as configurações correspondem aos projetos de código-fonte.
- [ ] O ponto de entrada e o provedor de IaC estão de acordo com `azure.yaml` (Terraform neste kit).
- [ ] As saídas de implantação obrigatórias correspondem às variáveis consumidas por serviços, ganchos e fluxos automatizados.
- [ ] `.gitignore` exclui `.azure`, segredos, estado local e artefatos gerados.
- [ ] Nenhum segredo aparece em conteúdo rastreado nem na saída de comandos; os segredos usam identidade gerenciada ou referências do Key Vault.
- [ ] As verificações aplicáveis são aprovadas (`terraform fmt -check`, `terraform validate`, o formatador, a análise estática e os testes do projeto).
- [ ] Nenhum comando que altera a nuvem foi executado sem aprovação explícita, e o sucesso só é declarado após verificação real.
