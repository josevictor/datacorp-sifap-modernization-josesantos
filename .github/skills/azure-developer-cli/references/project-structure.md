# Estrutura do projeto e `azure.yaml`

## Estrutura de repositório recomendada

Use isto como padrão, não como motivo para reorganizar um repositório que já é coerente:

```text
.
|-- .azure/                         # Estado local gerado do ambiente AZD; ignorado
|-- .devcontainer/                  # Ambiente de desenvolvimento reproduzível opcional
|-- .github/
|   |-- workflows/
|       |-- azure-dev.yml           # Fluxo automatizado opcional do GitHub Actions
|-- infra/
|   |-- main.bicep                  # Ponto de entrada da orquestração Bicep
|   |-- main.parameters.json        # Mapeamento de parâmetros do ambiente AZD para Bicep
|   |-- modules/
|       |-- core/                   # Recursos compartilhados da plataforma
|       |-- app/                    # Recursos específicos da aplicação
|-- scripts/
|   |-- azd/                        # Scripts auxiliares de ganchos e implantação
|-- src/
|   |-- api/                        # Serviço implantável de forma independente
|   |-- web/                        # Serviço implantável de forma independente
|-- tests/
|-- .gitignore
|-- azure.yaml
|-- README.md
```

Para Terraform, use uma estrutura convencional em `infra`:

```text
infra/
|-- main.tf
|-- providers.tf
|-- variables.tf
|-- outputs.tf
|-- provider.conf.json              # Configuração da estrutura remota do AZD, quando usada
|-- modules/
```

### Regras de estrutura

- Coloque `azure.yaml` na raiz do projeto.
- Mantenha o código-fonte da aplicação independente dos recursos de implantação.
- Mantenha o ponto de entrada da IaC enxuto e mova os detalhes dos recursos para módulos.
- Organize os módulos por responsabilidade ou ciclo de vida, não em um arquivo arbitrário por recurso.
- Mantenha os scripts de ganchos fora de `infra`, a menos que um script pertença exclusivamente a uma camada de infraestrutura.
- Evite versionar árvores de código-fonte específicas de ambiente, como `infra/dev`, `infra/test` e `infra/prod`. Use parâmetros.
- Mantenha os testes conforme as convenções normais da linguagem. Não os mova apenas para se adequar a este exemplo.
- Inclua `.devcontainer` somente quando for mantido e testado.

## Estrutura básica de `azure.yaml`

Adicione a diretiva de esquema para validação no editor:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json
name: sample-app

infra:
  provider: bicep
  path: ./infra
  module: main

services:
  api:
    project: ./src/api
    language: ts
    host: appservice
  web:
    project: ./src/web
    dist: dist
    language: ts
    host: staticwebapp
```

O bloco `infra` explícito é útil quando a clareza importa, embora Bicep, `infra` e `main` sejam os padrões.

## Lista de verificação do design do manifesto

### Configuração de nível superior

- `name` usa letras minúsculas, começa e termina com um caractere alfanumérico e contém somente caracteres alfanuméricos e hifens.
- `metadata.template` identifica o modelo de origem e a versão quando o repositório é distribuído como modelo.
- `infra.provider`, `infra.path` e `infra.module` correspondem ao repositório real.
- `requiredVersions` é usado quando o projeto depende de uma versão mínima do AZD ou de uma extensão.
- `workflows` substitui os padrões somente quando a ordem da implantação realmente exigir.
- `state.remote` é configurado no escopo do projeto quando as equipes compartilham ambientes do AZD.

### Serviços

- Um serviço representa código de aplicação implantável, não um banco de dados, Key Vault ou outro recurso compartilhado.
- Os nomes dos serviços são curtos, significativos e estáveis.
- `project` aponta para a raiz do serviço e usa um caminho relativo.
- As configurações de `language`, `host`, `dist`, contêiner e compilação remota correspondem à forma de compilação do serviço.
- Um serviço do Azure Container Apps usa `project` ou `image`, nunca ambos.
- `resourceName` é definido somente quando a descoberta padrão do AZD pela tag `azd-service-name` não está disponível ou é ignorada intencionalmente.
- As dependências usam relações `uses` compatíveis, em vez de premissas implícitas.
- As variáveis de ambiente usam substituições ou saídas de IaC, em vez de valores fixos de ambiente.

### Recursos e infraestrutura

- Os recursos compartilhados do Azure permanecem na IaC.
- Os módulos de serviço e os nomes de serviço do AZD ficam alinhados para tornar previsível a descoberta de recursos.
- Nomes personalizados de grupos de recursos incluem a identidade do ambiente e cumprem as restrições de nomenclatura do Azure.
- As camadas de infraestrutura são reservadas para unidades provisionadas de forma independente, escopos diferentes ou dependências mediadas por ganchos.
- As dependências entre camadas são explícitas com `dependsOn` quando o AZD não puder deduzi-las.

### Fluxos automatizados e ganchos

- `pipeline.variables` contém configurações não secretas.
- `pipeline.secrets` é usado somente quando o fluxo automatizado precisa armazenar o valor resolvido, em vez de uma referência do Key Vault.
- Ganchos da raiz tratam o trabalho de todo o projeto; ganchos de serviço tratam um serviço.
- Scripts de ganchos usam interpretadores de comandos explícitos e caminhos portáteis.
- Ganchos não duplicam testes da aplicação nem comportamentos declarativos da IaC.

## Requisitos do README para um projeto AZD reutilizável

Documente:

1. Arquitetura e serviços implantados no Azure.
2. Pré-requisitos locais, incluindo AZD e ferramentas específicas do provedor.
3. Requisitos de autenticação.
4. Como criar ou selecionar um ambiente.
5. Variáveis não secretas obrigatórias e como defini-las.
6. Como fornecer segredos sem expor seus valores.
7. Como executar, testar, provisionar, implantar, monitorar e solucionar problemas.
8. Recursos que devem gerar custos.
9. Como fazer a limpeza com segurança.
10. Dependências beta ou em versão prévia, incluindo recursos do Terraform ou de fluxos automatizados quando aplicável.

Não coloque IDs reais de assinatura, IDs de locatário (`tenant`), nomes de segredos que revelem sistemas sensíveis nem pontos de extremidade de produção em documentação reutilizável.
