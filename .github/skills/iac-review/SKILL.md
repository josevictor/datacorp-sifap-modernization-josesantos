---
name: "iac-review"
description: "Use ao revisar Terraform, Bicep ou CloudFormation, verificar divergências ou fortalecer código de infraestrutura. Os gatilhos incluem \"revisar terraform\", \"revisar bicep\", \"revisão de IaC\", \"detecção de divergências\" e \"arquivo de estado\"."
---
# Revisão de IaC

## Quando usar

- "Revise este módulo Terraform."
- "Por que nosso plano mostra divergências?"
- "Este Bicep está pronto para produção?"

## Lista de verificação da revisão

### Estrutura

- [ ] Os módulos são **combináveis** e têm uma única responsabilidade (um módulo = um conjunto lógico, não um recurso).
- [ ] **Nenhum valor fixado no código**: parametrizar tudo com valores-padrão adequados.
- [ ] Entradas documentadas (regras `description`, `type` e `validation`) e saídas documentadas.
- [ ] Um **README** na raiz do módulo com um exemplo de uso.

### Estado e configurações de armazenamento remoto

- [ ] **Estado remoto** com bloqueio (S3+DynamoDB, Azure Storage com concessão de blob, GCS).
- [ ] O estado **nunca é registrado no histórico** do Git; `.gitignore` abrange `*.tfstate*`.
- [ ] O estado é separado por ambiente, sem acoplamento implícito entre ambientes.
- [ ] O IAM controla o acesso ao estado, não credenciais compartilhadas.

### Segurança

- [ ] Nenhum segredo no código nem nos valores-padrão das variáveis. Use Key Vault / Secrets Manager / SOPS.
- [ ] O IAM segue o princípio do menor privilégio, sem `*:*` nem `Resource: "*"`, salvo quando justificado.
- [ ] A criptografia em repouso e em trânsito está habilitada em todos os armazenamentos de dados.
- [ ] O acesso público é negado explicitamente, salvo quando intencional. Documente o acesso intencional no README do módulo.
- [ ] `tfsec` / `checkov` / `PSRule` não relatam constatações, ou as exceções estão documentadas.

### Segurança das alterações

- [ ] `terraform plan` é incluído nas solicitações de alteração (pull requests, ou PRs) como comentário (Atlantis / tfcmt / GitHub Actions).
- [ ] `prevent_destroy` está definido em recursos com estado (bancos de dados, KV e contas de armazenamento).
- [ ] As versões dos provedores (`provider`) estão **fixadas** (`~>` com versões principal e secundária explícitas).
- [ ] As versões dos módulos estão fixadas.
- [ ] Alterações destrutivas exigem uma segunda aprovação.

### Divergências

- [ ] Detecção agendada de divergências (`terraform plan -detailed-exitcode` diariamente ou Driftctl).
- [ ] Uma divergência cria automaticamente um tíquete e nunca permanece silenciosa.
- [ ] Nenhuma alteração manual no console sem posterior codificação.

## Constatações comuns

- **`count` usado em listas que podem ser reordenadas** → use `for_each` com chaves estáveis.
- **`depends_on` em todo lugar** → normalmente indica dependências implícitas ausentes; remova-o, salvo quando realmente necessário.
- **Fontes de dados usadas para valores disponíveis durante o planejamento** → chamadas de API desnecessárias e integração contínua (CI) instável.
- **Diferenças entre ambientes por interpolação de string com `terraform.workspace`** → abordagem frágil; use tfvars ou conjuntos separados.

## Modelo de saída

```markdown
## Revisão de IaC: <módulo ou conjunto>

| Área | Constatação | Severidade | Recomendação |
|---|---|---|---|
| Estado | Estado local, sem bloqueio | Alta | Mover para uma configuração de armazenamento remoto com bloqueio |
| Segurança | A conta de armazenamento permite acesso público | Alta | Definir public_network_access_enabled = false |
| Segurança das alterações | Versão do provedor não fixada | Média | Fixar com ~> major.minor |

**Constatações bloqueadoras**: <quantidade>
**Veredito**: aprovar / solicitar alterações
```

No modelo, `major.minor` identifica as versões principal e secundária.

## Critérios de qualidade

- [ ] `terraform fmt` e `terraform validate` passam, e o plano está anexado à solicitação de alteração (PR).
- [ ] Nenhum segredo aparece no código, nas variáveis ou no estado; os segredos usam Key Vault ou Secrets Manager.
- [ ] As versões de provedores e módulos estão fixadas; os recursos com estado definem `prevent_destroy`.
- [ ] `tfsec` ou `checkov` não relata constatações, ou todas as exceções estão documentadas.
- [ ] Todos os recursos têm os marcadores (`tags`) `project`, `environment` e `owner`.

## Referências

- [Guia de estilo do Terraform](https://developer.hashicorp.com/terraform/language/style)
- [Módulos verificados do Azure](https://azure.github.io/Azure-Verified-Modules/)
- [tfsec](https://aquasecurity.github.io/tfsec/), [checkov](https://www.checkov.io/)
