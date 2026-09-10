---
name: "azure-role-selector"
description: "Use quando a pessoa perguntar qual função do Azure RBAC atribuir a uma identidade, como conceder permissões de privilégio mínimo ou como criar uma função personalizada quando nenhuma função interna for adequada. Recomenda a função interna mais restrita e gera a atribuição como Terraform (azurerm_role_assignment), a IaC deste kit. Os gatilhos incluem \"qual função do Azure\", \"privilégio mínimo\", \"atribuição de função\", \"definição de função personalizada\" e \"conceder permissões\"."
---
# Seletor de funções do Azure

Recomende a função do Azure RBAC de **privilégio mínimo** para uma identidade com base nas ações que ela precisa executar. Depois, expresse a atribuição como Terraform (`azurerm_role_assignment`), a IaC deste kit. Sempre prefira uma função interna no escopo mais restrito. Crie uma definição de função personalizada apenas quando nenhuma função interna for adequada.

Esta habilidade ensina como escolher e aplicar uma função. Ela não decide qual identidade ou escopo sua carga de trabalho precisa. Isso vem da especificação e da investigação da equipe.

> [!NOTE]
> Esta habilidade depende do **servidor MCP do Azure** (ou da CLI `az`) para consultar definições de função e gerar comandos de atribuição. Se nenhum deles estiver instalado, informe isso e use a documentação pública de funções internas do Azure.

## Quando usar

- "Qual função do Azure devo atribuir a esta identidade gerenciada?"
- "Conceda a esta entidade de serviço acesso somente leitura a uma conta de armazenamento, com privilégio mínimo."
- "Nenhuma função interna é adequada. Ajude-me a escrever uma definição de função personalizada."
- "Dê à identidade da aplicação permissão para ler segredos do Key Vault."

## Procedimento de seleção

1. **Registre as ações necessárias.** Liste as operações exatas que a identidade deve executar (por exemplo: ler blobs, listar segredos, enviar para uma fila). Separe `actions` do plano de controle de `dataActions` do plano de dados.
2. **Escolha o escopo mais restrito.** Faça a atribuição no menor escopo que atenda ao requisito: recurso antes de grupo de recursos, grupo de recursos antes de assinatura e assinatura antes de grupo de gerenciamento.
3. **Encontre uma função interna.** Use a ferramenta de documentação do MCP do Azure para encontrar a função interna cujas `actions`/`dataActions` cubram o requisito com o menor excesso. Prefira funções do plano de dados (por exemplo, `Storage Blob Data Reader`) a funções amplas de gerenciamento (`Contributor`).
4. **Use uma função personalizada apenas se necessário.** Quando nenhuma função interna for adequada, use a ferramenta `extension_cli_generate` do MCP do Azure para elaborar uma definição que liste somente as `actions`/`dataActions` necessárias e um `assignableScopes` explícito.
5. **Gere a atribuição.** Use a ferramenta `extension_cli_generate` do MCP do Azure para o comando `az role assignment create` e traduza-o para Terraform como entrega do kit.
6. **Prefira uma identidade gerenciada.** Para autenticação entre serviços, atribua a função a uma identidade gerenciada. Nunca distribua segredos, chaves ou cadeias de conexão.

## Tabela de decisão de privilégio mínimo

| Situação | Escolha |
|---|---|
| Uma função interna corresponde exatamente às ações | A função interna no escopo mais restrito |
| Uma função interna é próxima, mas ligeiramente ampla | Prefira a função interna, a menos que as permissões extras sejam sensíveis. Documente a diferença |
| Nenhuma função interna cobre as ações | Uma definição de função personalizada contendo apenas as ações necessárias |
| Um serviço do Azure precisa chamar outro serviço do Azure | Uma identidade gerenciada com uma atribuição de função, nunca um segredo |
| A identidade apenas lê dados | Uma função do plano de dados `... Data Reader`, não `Reader` nem `Contributor` |

> [!WARNING]
> Nunca atribua `Owner` nem `Contributor` no escopo da assinatura ou do grupo de gerenciamento a uma identidade de carga de trabalho. Essas funções incluem `Microsoft.Authorization/*`, que permite à identidade conceder mais acesso a si mesma.

## Bicep e ARM fora do escopo

Um trecho de atribuição de função em Bicep ou ARM (por meio das ferramentas `bicepschema` e `get_bestpractices` do MCP do Azure) é opcional e está **fora do escopo** das entregas deste kit. Produza Terraform. Use Bicep apenas para exploração ou comparação.

## Modelo de saída

Entregue a recomendação com um trecho de Terraform pronto para ser confirmado no repositório. Atribuições e definições de função não aceitam `tags`. Portanto, a regra de marcação do kit não se aplica a esses recursos.

```hcl
resource "azurerm_role_assignment" "app_blob_reader" {
  scope                = azurerm_storage_account.data.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}
```

Quando nenhuma função interna for adequada, entregue uma definição de função personalizada junto com a atribuição:

```hcl
resource "azurerm_role_definition" "read_one_container" {
  name        = "SIFAP Read Single Blob Container"
  scope       = azurerm_storage_account.data.id
  description = "Acesso somente leitura a um único contêiner de blobs, com privilégio mínimo."

  permissions {
    actions      = ["Microsoft.Storage/storageAccounts/blobServices/containers/read"]
    data_actions = ["Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read"]
    not_actions  = []
  }

  assignable_scopes = [azurerm_storage_account.data.id]
}
```

Resuma a escolha em texto:

```text
Função recomendada: Storage Blob Data Reader (interna)
Escopo: conta de armazenamento azurerm_storage_account.data (o mais restrito que funciona)
Entidade de segurança: identidade gerenciada app atribuída pelo usuário
Motivo: cobre a ação de leitura de blobs no plano de dados sem excesso; não é necessária uma função personalizada.
```

## Critérios de qualidade

- [ ] A função recomendada é a função interna mais restrita que cobre todas as ações necessárias.
- [ ] O escopo da atribuição é o menor que atende ao requisito.
- [ ] Uma função personalizada é proposta apenas quando nenhuma função interna é adequada e lista somente as ações necessárias, com `assignable_scopes` explícito.
- [ ] A atribuição está expressa como Terraform `azurerm_role_assignment` (Bicep/ARM fora do escopo).
- [ ] A autenticação entre serviços usa uma identidade gerenciada, nunca um segredo ou uma cadeia de conexão.
- [ ] Não há `Owner`/`Contributor` no escopo da assinatura ou do grupo de gerenciamento para uma identidade de carga de trabalho.

## Licença

O material incluído nesta habilidade é fornecido sob a [Licença MIT](LICENSE.txt).
