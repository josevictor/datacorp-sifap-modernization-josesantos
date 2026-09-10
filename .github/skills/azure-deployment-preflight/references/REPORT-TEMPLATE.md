# Modelo de relatório pré-implantação

Use esta estrutura de modelo ao gerar `preflight-report.md` na raiz do projeto.

---

## Modelo

````markdown
# Relatório de pré-implantação do Azure

**Gerado em:** {timestamp}
**Status:** {overall-status}

---

## Resumo

| Propriedade | Valor |
|----------|-------|
| **Arquivos de modelo** | {bicep-files} |
| **Arquivos de parâmetros** | {param-files-or-none} |
| **Tipo de projeto** | {azd-project | standalone-bicep} |
| **Escopo da implantação** | {resourceGroup | subscription | managementGroup | tenant} |
| **Destino** | {resource-group-name | subscription-name | mg-id} |
| **Nível de validação** | {Provider | ProviderNoRbac} |

### Resultados da validação

| Verificação | Status | Detalhes |
|-------|--------|---------|
| Sintaxe do Bicep | {✅ Aprovado | ❌ Reprovado | ⚠️ Avisos | ⏭️ Ignorado} | {details} |
| Análise what-if | {✅ Aprovado | ❌ Reprovado | ⏭️ Ignorado} | {details} |
| Verificação de permissões | {✅ Aprovado | ⚠️ Limitado | ❌ Reprovado} | {details} |

---

## Ferramentas executadas

### Comandos executados

| Etapa | Comando | Código de saída | Duração |
|------|---------|-----------|----------|
| 1 | `{command}` | {0 | non-zero} | {duration} |
| 2 | `{command}` | {0 | non-zero} | {duration} |

### Versões das ferramentas

| Ferramenta | Versão |
|------|---------|
| Azure CLI | {version} |
| Bicep CLI | {version} |
| Azure Developer CLI | {version-or-n/a} |

---

## Problemas

{if-no-issues}
✅ **Nenhum problema encontrado.** A implantação está pronta para prosseguir.
{end-if}

{if-issues-exist}
### Erros

{for-each-error}
#### ❌ {error-title}

- **Severidade:** Erro
- **Fonte:** {bicep-build | what-if | permissions}
- **Local:** {file-path}:{line}:{column} (se aplicável)
- **Mensagem:** {error-message}
- **Correção:** {suggested-fix}
- **Documentação:** {link-if-available}

{end-for-each}

### Avisos

{for-each-warning}
#### ⚠️ {warning-title}

- **Severidade:** Aviso
- **Fonte:** {source}
- **Mensagem:** {warning-message}
- **Recomendação:** {suggested-action}

{end-for-each}
{end-if}

---

## Resultados do what-if

{if-what-if-succeeded}

### Resumo das alterações

| Tipo de alteração | Quantidade |
|-------------|-------|
| 🆕 Criar | {count} |
| 📝 Modificar | {count} |
| 🗑️ Excluir | {count} |
| ✓ Sem alteração | {count} |
| ⚠️ Ignorar | {count} |

### Recursos a criar

{if-resources-to-create}
| Tipo de recurso | Nome do recurso |
|---------------|---------------|
| {type} | {name} |
{end-if}

{if-no-resources-to-create}
*Nenhum recurso será criado.*
{end-if}

### Recursos a modificar

{if-resources-to-modify}
#### {resource-type}/{resource-name}

| Propriedade | Valor atual | Novo valor |
|----------|---------------|-----------|
| {property-path} | {current} | {new} |

{end-if}

{if-no-resources-to-modify}
*Nenhum recurso será modificado.*
{end-if}

### Recursos a excluir

{if-resources-to-delete}
| Tipo de recurso | Nome do recurso |
|---------------|---------------|
| {type} | {name} |

> ⚠️ **Aviso:** os recursos listados para exclusão serão removidos permanentemente.
{end-if}

{if-no-resources-to-delete}
*Nenhum recurso será excluído.*
{end-if}

{end-if-what-if-succeeded}

{if-what-if-failed}
### Falha na análise what-if

A operação what-if não pôde ser concluída. Consulte a seção Problemas para obter detalhes.
{end-if}

---

## Recomendações

{generate-based-on-findings}

1. {recommendation-1}
2. {recommendation-2}
3. {recommendation-3}

---

## Próximas etapas

{if-all-passed}
A validação pré-implantação foi aprovada. Você pode prosseguir com a implantação:

**Para projetos azd:**
```bash
azd provision
# ou
azd up
```

**Para Bicep independente:**
```bash
az deployment group create \
  --resource-group {rg-name} \
  --template-file {bicep-file} \
  --parameters {param-file}
```
{end-if}

{if-issues-exist}
Resolva os problemas listados acima antes da implantação. Após as correções:

1. Execute novamente a validação pré-implantação para verificar as correções
2. Prossiga com a implantação quando todas as verificações forem aprovadas
{end-if}

---

*Relatório gerado pela habilidade de validação pré-implantação do Azure*
````

---

## Valores de status

### Status geral

| Status | Significado | Visual |
|--------|---------|--------|
| **Aprovado** | Todas as verificações foram bem-sucedidas; é seguro implantar | ✅ |
| **Aprovado com avisos** | As verificações foram bem-sucedidas, mas os avisos devem ser revisados | ⚠️ |
| **Reprovado** | Uma ou mais verificações falharam | ❌ |

### Status de cada verificação

| Status | Significado |
|--------|---------|
| ✅ Aprovado | Verificação concluída com sucesso |
| ❌ Reprovado | A verificação encontrou erros |
| ⚠️ Avisos | A verificação foi aprovada com avisos |
| ⏭️ Ignorado | A verificação foi ignorada (ferramenta indisponível etc.) |

---

## Exemplo de relatório

````markdown
# Relatório de pré-implantação do Azure

**Gerado em:** 2026-01-16T14:32:00Z
**Status:** ⚠️ Aprovado com avisos

---

## Resumo

| Propriedade | Valor |
|----------|-------|
| **Arquivos de modelo** | `infra/main.bicep` |
| **Arquivos de parâmetros** | `infra/main.bicepparam` |
| **Tipo de projeto** | projeto azd |
| **Escopo da implantação** | subscription |
| **Destino** | my-subscription |
| **Nível de validação** | Provider |

### Resultados da validação

| Verificação | Status | Detalhes |
|-------|--------|---------|
| Sintaxe do Bicep | ✅ Aprovado | Nenhum erro encontrado |
| Análise what-if | ⚠️ Avisos | Um recurso ignorado devido aos limites de modelos aninhados |
| Verificação de permissões | ✅ Aprovado | Permissões completas de implantação verificadas |

---

## Ferramentas executadas

### Comandos executados

| Etapa | Comando | Código de saída | Duração |
|------|---------|-----------|----------|
| 1 | `bicep build infra/main.bicep --stdout` | 0 | 1.2s |
| 2 | `azd provision --preview --environment dev` | 0 | 8.4s |

### Versões das ferramentas

| Ferramenta | Versão |
|------|---------|
| Azure CLI | 2.76.0 |
| Bicep CLI | 0.25.3 |
| Azure Developer CLI | 1.9.0 |

---

## Problemas

### Avisos

#### ⚠️ Limite de modelos aninhados atingido

- **Severidade:** Aviso
- **Fonte:** what-if
- **Mensagem:** Um recurso foi ignorado porque os limites de expansão de modelos aninhados foram atingidos
- **Recomendação:** Revise manualmente o recurso ignorado após a implantação

---

## Resultados do what-if

### Resumo das alterações

| Tipo de alteração | Quantidade |
|-------------|-------|
| 🆕 Criar | 3 |
| 📝 Modificar | 1 |
| 🗑️ Excluir | 0 |
| ✓ Sem alteração | 2 |
| ⚠️ Ignorar | 1 |

### Recursos a criar

| Tipo de recurso | Nome do recurso |
|---------------|---------------|
| Microsoft.Resources/resourceGroups | rg-myapp-dev |
| Microsoft.Storage/storageAccounts | stmyappdev |
| Microsoft.Web/sites | app-myapp-dev |

### Recursos a modificar

#### Microsoft.KeyVault/vaults/kv-myapp-dev

| Propriedade | Valor atual | Novo valor |
|----------|---------------|-----------|
| properties.sku.name | standard | premium |
| tags.environment | staging | dev |

### Recursos a excluir

*Nenhum recurso será excluído.*

---

## Recomendações

1. Revise o nome da conta de armazenamento `stmyappdev` para confirmar que atende aos requisitos de nomenclatura
2. Confirme se a atualização da SKU do Key Vault de standard para premium é intencional
3. Verifique o recurso ignorado do modelo aninhado após a implantação

---

## Próximas etapas

A validação pré-implantação foi aprovada com avisos. Revise os avisos acima e prossiga:

```bash
azd provision --environment dev
```

---

*Relatório gerado pela habilidade de validação pré-implantação do Azure*
````

---

## Orientações de formatação

1. **Use emojis consistentes** para facilitar a leitura visual
2. **Inclua números de linha** ao referenciar erros do Bicep
3. **Forneça correções práticas** para cada problema
4. **Inclua links para a documentação** quando disponível
5. **Ordene os problemas por severidade** (primeiro erros, depois avisos)
6. **Inclua exemplos de comandos** em Próximas etapas
