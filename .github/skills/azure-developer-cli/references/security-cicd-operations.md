# Segurança, ganchos, CI/CD e operações

## Tratamento de identidades e segredos

Use esta ordem de preferência:

1. Identidade gerenciada com RBAC de privilégio mínimo.
2. Federação de identidade da carga de trabalho para CI/CD.
3. Referência do Key Vault por meio de `azd env set-secret`.
4. Material secreto de curta duração somente quando não existir uma opção baseada em identidade.

Nunca:

- Armazene um segredo em texto simples em `.azure/<environment>/.env`.
- Versione arquivos de ambiente, credenciais, certificados ou estado do Terraform.
- Coloque segredos nas saídas da IaC.
- Exiba valores de ambiente indiscriminadamente em ganchos ou fluxos automatizados.
- Passe um segredo diretamente na linha de comando quando o interpretador de comandos ou o sistema de CI puder registrá-lo.
- Conceda funções amplas na assinatura quando o escopo do grupo de recursos ou do recurso for suficiente.

`azd env set-secret <name>` armazena uma referência do Key Vault no ambiente AZD. Resolva-a somente onde for necessário:

- Mapeie-a para um parâmetro Bicep `@secure()`.
- Use um mapeamento `secrets` do gancho para um processo do gancho.
- Escolha entre uma variável do fluxo automatizado que contenha a referência do Key Vault ou um segredo desse fluxo que contenha o valor resolvido.

Prefira a abordagem por referência quando a identidade do fluxo automatizado puder ler o Key Vault, pois a rotação não exigirá republicar um segredo resolvido desse fluxo.

## Ganchos

Use ganchos para validação, configuração gerada do ambiente de execução, preparação de dados, verificações rápidas ou coordenação do ciclo de vida que a IaC e o comportamento nativo do AZD não possam expressar.

### Regras para ganchos

- Prefira scripts externos a comandos longos em linha.
- Armazene os scripts em `scripts/azd`.
- Defina `shell: sh` ou `shell: pwsh` explicitamente.
- Forneça implementações `windows` e `posix` quando a sintaxe for diferente.
- Use caminhos relativos ao diretório de trabalho documentado do gancho.
- Torne os scripts idempotentes e seguros para novas execuções.
- Mantenha `continueOnError` como false, a menos que a operação sirva somente à observabilidade ou seja realmente opcional.
- Use comportamento não interativo em CI.
- Não instale dependências sem versão fixada a cada execução quando uma configuração reproduzível puder fazer isso uma vez.
- Não registre valores de segredos nem todas as variáveis de ambiente.
- Teste com `azd hooks run <hook-name>` antes de acoplar o gancho a uma implantação completa.

Exemplo:

```yaml
hooks:
  preprovision:
    windows:
      shell: pwsh
      run: ./scripts/azd/validate.ps1
      interactive: false
      continueOnError: false
    posix:
      shell: sh
      run: ./scripts/azd/validate.sh
      interactive: false
      continueOnError: false
```

Use ganchos da raiz para todo o projeto. Coloque ganchos específicos de um serviço na entrada desse serviço em `azure.yaml`.

## Fluxo de implantação

O ciclo de vida normal do AZD é:

1. Empacotar artefatos da aplicação.
2. Provisionar ou atualizar a infraestrutura.
3. Implantar artefatos da aplicação.

`azd up` é o fluxo combinado conveniente e é adequado para desenvolvimento rotineiro e implantações simples.

Use comandos separados quando:

- A revisão ou aprovação da infraestrutura precisar ocorrer antes da implantação.
- A aplicação for reimplantada com frequência sem alterações na infraestrutura.
- A solução de problemas exigir o isolamento de falhas de empacotamento, provisionamento ou implantação.
- Uma dependência complexa exigir uma ordem personalizada.

```text
azd package
azd provision -e <environment>
azd deploy -e <environment>
```

Personalize `workflows.up.steps` somente quando uma dependência real exigir outra ordem, como provisionar antes de uma compilação que precise de um ponto de extremidade gerado. Não personalize o fluxo apenas para reproduzir as convenções de nomenclatura de um fluxo automatizado.

## Dependências de ponta a ponta e entre vários serviços

- Mapeie as dependências dos serviços antes da implementação.
- Permita que Bicep ou Terraform tratem as dependências unidirecionais da infraestrutura.
- Use saídas de provisionamento para pontos de extremidade e nomes necessários durante a implantação.
- Use configuração do ambiente de execução, como Azure App Configuration ou um arquivo de configuração gerado, quando as configurações precisarem mudar sem nova compilação.
- Evite dependências circulares em tempo de compilação entre serviços de interface e da camada de servidor.
- Use ganchos ou um fluxo personalizado somente quando as saídas e a configuração do ambiente de execução não puderem resolver a dependência.
- Teste a estratégia separadamente em ambientes de desenvolvimento, teste e semelhantes à produção.

## CI/CD

### Projeto do fluxo automatizado

Um fluxo automatizado robusto separa:

1. Formatação, análise estática, compilação e testes da aplicação.
2. Formatação e validação estática da IaC.
3. Revisão de what-if ou plano no escopo correto.
4. Provisionamento com um ambiente AZD explícito.
5. Implantação.
6. Verificação rápida ou de integridade.
7. Procedimentos de aprovação para produção e de reversão/limpeza.

Use:

- `--no-prompt` em automações.
- Um `-e` ou `--environment` fixo.
- Ambientes protegidos e revisores obrigatórios para produção.
- Controles de concorrência para impedir gravações simultâneas em um ambiente.
- Identidades de privilégio mínimo limitadas ao ambiente de destino.
- Versões fixadas de ações e ferramentas, com um processo gerenciado de atualização.

### `azd pipeline config`

A documentação atual da Microsoft classifica `azd pipeline config` como beta. Antes de executá-lo:

- Revise a definição do fluxo automatizado incluída no modelo.
- Confirme o repositório, a organização, o ambiente, a assinatura e o modo de autenticação.
- Espere efeitos colaterais no repositório, na identidade, nas variáveis, nos segredos, no versionamento, no envio e no fluxo automatizado.
- Revise o fluxo de trabalho gerado e as alterações de permissões antes do uso em produção.
- Execute-o novamente quando `pipeline.variables` ou `pipeline.secrets` mudar.

Para o GitHub Actions, o AZD configura credenciais OIDC/federadas por padrão nos cenários compatíveis. A documentação atual informa que o fluxo automatizado do AZD com Terraform não oferece suporte a OIDC. Portanto, avalie explicitamente o compromisso de autenticação, em vez de recorrer silenciosamente a uma credencial de longa duração.

Para Terraform, configure o estado remoto protegido antes do fluxo automatizado.

## Validação e versão prévia

Execute verificações locais antes dos comandos que alteram o Azure:

### Bicep

```text
az bicep build --file infra/main.bicep
```

Use um what-if de implantação do Azure no escopo declarado pelo modelo. Não presuma o escopo do grupo de recursos.

### Terraform

```text
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
```

Use `terraform plan` somente após confirmar a estrutura remota, a chave do espaço de trabalho/estado, as variáveis e a identidade do Azure.

### AZD e aplicação

- Execute as verificações existentes da aplicação.
- Execute os ganchos relevantes de forma independente.
- Execute `azd package` para verificar os caminhos dos serviços e o empacotamento.
- Confirme se as saídas da IaC correspondem às variáveis consumidas durante a implantação.
- Verifique o nome do ambiente antes de provisionar, implantar ou excluir.

## Sequência de solução de problemas

1. Identifique se a falha ocorre no empacotamento, provisionamento, implantação, gancho, autenticação ou descoberta de recursos.
2. Execute novamente a menor fase com falha, em vez de `azd up`.
3. Verifique o ambiente selecionado e a assinatura, o locatário e a região esperados.
4. Verifique os caminhos, o provedor, os nomes dos serviços, os tipos de host e as tags de descoberta de recursos em `azure.yaml`.
5. Atualize as saídas do ambiente com `azd env refresh` quando o estado do Azure mudar em outro local.
6. Para Terraform, verifique a autenticação do AZD e da Azure CLI, além do estado remoto correto.
7. Para ganchos, execute o gancho diretamente e verifique o interpretador de comandos, o diretório de trabalho e as dependências de ambiente.
8. Use registros de depuração somente quando necessário e oculte valores sensíveis antes de compartilhá-los.

## Limpeza

- Confirme o ambiente exato antes de `azd down`.
- Explique que a limpeza pode excluir recursos que contêm dados.
- Preserve recursos compartilhados ou pertencentes a elementos externos.
- Para ambientes efêmeros, automatize a limpeza e inclua uma alternativa para execuções com falha do fluxo automatizado.
- Verifique a exclusão, em vez de presumir o sucesso do comando.
