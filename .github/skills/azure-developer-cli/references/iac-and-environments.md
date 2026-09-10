# Infraestrutura como código e ambientes

## Escolha o provedor de forma intencional

### Bicep

Use Bicep quando:

- O projeto usar somente o Azure.
- A cobertura nativa de recursos do Azure e o suporte imediato à API forem importantes.
- A equipe quiser um modelo de implantação sem estado.
- O Azure Verified Modules abranger os padrões comuns de recursos.

O Bicep é o provedor de IaC padrão do AZD.

### Terraform

Use Terraform quando:

- O repositório já usar Terraform.
- A equipe tiver práticas estabelecidas de módulos, estado, políticas e revisão do Terraform.
- A infraestrutura entre provedores for um requisito real.

A documentação atual da Microsoft classifica o suporte do AZD ao Terraform como beta. Torne essa restrição visível e não migre um projeto para Terraform apenas por familiaridade.

## Estrutura do Bicep

Mantenha `main.bicep` como camada de orquestração:

```text
infra/
|-- main.bicep
|-- main.parameters.json
|-- modules/
|   |-- core/
|   |-- data/
|   |-- identity/
|   |-- observability/
|   |-- services/
```

### Práticas para Bicep

- Declare o `targetScope` da implantação de forma intencional.
- Use módulos para capacidades coesas e padrões repetidos.
- Prefira Azure Verified Modules quando atenderem ao requisito e a equipe aceitar seu modelo de versionamento.
- Fixe as versões dos módulos e revise as atualizações, em vez de deixá-las flutuar automaticamente.
- Adicione descrições e decoradores de validação aos parâmetros.
- Passe os parâmetros pelos módulos, em vez de ler variáveis de ambiente do AZD dentro de cada módulo.
- Use nomes determinísticos que respeitem as restrições de tamanho e caracteres de cada tipo de recurso.
- Use `uniqueString` com entradas de escopo estáveis quando a exclusividade global for necessária.
- Aplique tags consistentes de projeto, ambiente, proprietário e custo quando a política permitir.
- Use identidades gerenciadas e atribuições de função com escopo restrito.
- Evite chaves e strings de conexão quando o acesso baseado em identidade estiver disponível.
- Produza os IDs, nomes e pontos de extremidade dos recursos exigidos pelas fases posteriores.
- Nunca produza valores de segredos. As saídas de implantação são copiadas para o ambiente do AZD.

### Fluxo de parâmetros

Use `main.parameters.json` para mapear valores do ambiente AZD para o Bicep:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environmentName": {
      "value": "${AZURE_ENV_NAME}"
    },
    "location": {
      "value": "${AZURE_LOCATION}"
    }
  }
}
```

Faça a correspondência desses valores no ponto de entrada:

```bicep
@description('Nome estavel do ambiente de implantacao do AZD.')
@minLength(1)
param environmentName string

@description('Regiao principal do Azure para esta implantacao.')
param location string
```

Use as saídas como contrato entre o provisionamento e as fases posteriores do AZD:

```bicep
output SERVICE_API_ENDPOINT_URL string = api.outputs.endpoint
```

Escolha nomes de saída estáveis, pois serviços, ganchos e fluxos automatizados podem consumi-los como variáveis de ambiente.

Ao usar segredos do ambiente AZD com Bicep:

- Marque a entrada do Bicep com `@secure()`.
- Mapeie a referência do segredo do AZD por meio de `main.parameters.json`.
- Não produza o valor seguro.
- Observe que a documentação atual do AZD informa que arquivos `.bicepparam` não oferecem suporte a segredos de ambiente.

## Estrutura e estado do Terraform

### Práticas para Terraform

- Defina `infra.provider: terraform` explicitamente em `azure.yaml`.
- Mantenha todos os arquivos `.tf` gerenciados pelo AZD no caminho de infraestrutura configurado.
- Fixe as versões do Terraform e dos provedores e versione o arquivo de bloqueio de dependências.
- Use módulos com entradas e saídas claras.
- Marque variáveis e saídas sensíveis como `sensitive`, mas lembre-se de que os valores sensíveis ainda podem existir no estado.
- Não versione `.tfstate`, arquivos de plano, registros de falha nem credenciais do provedor.
- Evite dividir a responsabilidade pelo mesmo recurso do Azure entre o AZD e um módulo raiz não relacionado do Terraform.

### Autenticação

O provedor do Azure para Terraform usa a autenticação da Azure CLI por padrão e não usa o armazenamento temporário de credenciais do AZD. Prefira a configuração documentada de autenticação única:

```text
azd config set auth.useAzCliAuth true
az login
```

Caso contrário, `azd auth login` e `az login` serão obrigatórios.

### Estado remoto

Configure uma estrutura remota protegida (`backend`) antes de `azd pipeline config` ou de implantações colaborativas:

- Use uma conta de armazenamento dedicada e um contêiner privado quando adequado.
- Restrinja o acesso com RBAC e controles de rede.
- Ative proteções da plataforma, como controle de versão, exclusão reversível e bloqueios de recursos, conforme a política organizacional.
- Use uma chave de estado diferente para cada projeto e ambiente.
- Trate o estado como dado sensível.
- Não armazene chaves de acesso da estrutura remota no controle de versão.

O AZD lê as configurações da estrutura remota do Terraform em `infra/provider.conf.json` quando configurado conforme a integração oficial do Terraform.

## Estratégia de ambientes

O AZD armazena o estado local do ambiente em:

```text
.azure/
|-- config.json
|-- <environment-name>/
    |-- .env
    |-- config.json
```

Todo o diretório `.azure` deve permanecer fora do controle de versão.

### Nomenclatura

Use nomes que deixem claros a responsabilidade e o ciclo de vida:

- Compartilhado: `<project>-dev`, `<project>-test`, `<project>-prod`
- Pessoal: `<alias>-<purpose>` ou `<alias>-dev`
- Efêmero: `<project>-pr-<number>` quando a automação também garantir a limpeza

Mantenha o nome curto o suficiente para comportar recursos com limites restritivos de nomenclatura.

### Gerenciamento

Use comandos do AZD em vez de editar arquivos manualmente:

```text
azd env new <name>
azd env list
azd env select <name>
azd env set <key> <value>
azd env get-value <key>
azd env unset <key>
azd env refresh
```

Em automações e operações possivelmente destrutivas, defina o ambiente de forma explícita:

```text
azd provision -e <environment> --no-prompt
azd deploy -e <environment> --no-prompt
```

### Regras de configuração

- Mantenha uma base de código de IaC e varie o comportamento por meio de parâmetros.
- Mantenha os padrões não secretos em configurações revisadas ou na IaC, não em arquivos `.azure` versionados.
- Use `azd env set` para configurações não secretas específicas da implantação.
- Permita que as saídas da IaC preencham nomes e pontos de extremidade calculados dos recursos.
- Evite condicionais baseadas no nome do ambiente espalhadas pelos módulos. Prefira parâmetros explícitos de funcionalidade ou SKU.
- Use `azd env refresh` após outro agente alterar as saídas da implantação.
- Não presuma nos scripts qual é o ambiente selecionado atualmente.

## Ambientes compartilhados e remotos

Configure `state.remote` quando integrantes da equipe ou a automação precisarem de um ambiente AZD compartilhado:

```yaml
state:
  remote:
    backend: AzureBlobStorage
    config:
      accountName: <storage-account-name>
      containerName: <project-container-name>
```

O estado remoto do AZD sincroniza `.env` e o `config.json` do AZD. Ele é separado do estado remoto do Terraform. Um projeto Terraform com colaboração pelo AZD pode exigir ambos:

- Estado remoto do AZD para a configuração do ambiente.
- Estado remoto do Terraform para o estado da infraestrutura gerenciada.

Proteja os dois armazenamentos com RBAC de privilégio mínimo e configurações adequadas de proteção de dados.
