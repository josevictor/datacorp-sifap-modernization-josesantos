# Agente revisor de Bicep

Revisa o código Bicep gerado e corrige automaticamente os problemas encontrados.

## Ordem da revisão

### Etapa 1: compilação do Bicep (execute primeiro)

Compile o Bicep de fato **antes** de usar a lista de verificação. Não declare aprovação com base somente em inspeção visual.

```powershell
az bicep build --file main.bicep 2>&1
```

Colete todos os avisos (`WARNING`) e erros (`ERROR`) do resultado da compilação. Esses dados fundamentam a revisão.

### Etapa 2: corrigir erros e avisos de compilação

Corrija os problemas encontrados na compilação:

- **Erro (`ERROR`)** → corrija e compile novamente
- **Aviso (`WARNING`)** → trate conforme os critérios abaixo

**🚨 Critérios de tratamento de avisos (`WARNING`): não force correções desnecessárias**

Avisos não bloqueiam a implantação. Tentar resolvê-los muitas vezes introduz erros de implantação. Use estes critérios:

| Tipo de aviso (`WARNING`) | Ação | Motivo |
|---|---|---|
| BCP081 (tipo não definido) | **Mantenha como está** (se a versão da API for a mais recente confirmada no Microsoft Docs) | As definições locais de tipo da CLI do Bicep ainda não foram atualizadas. Não afeta a implantação |
| BCP035 (propriedade ausente) | **Avalie com cuidado**: consulte o Microsoft Docs para confirmar se a propriedade é obrigatória; caso contrário, mantenha como está | Adicionar propriedades pode causar falhas de implantação por incompatibilidade (por exemplo, `computeMode`) |
| BCP187 (tipo de sku/kind não verificado) | **Mantenha como está** | Os valores confirmados no Microsoft Docs funcionarão corretamente na implantação |
| no-hardcoded-env-urls | **Mantenha como está** | Os nomes de DNS Zone inevitavelmente exigem valores fixos |

**Nunca faça o seguinte:**

- Não use versões anteriores da API para resolver avisos (mantenha a versão estável mais recente)
- Não adicione propriedades sem confirmação no Microsoft Docs para resolver avisos
- Não force correções para chegar a "zero avisos"

**Princípio: documente os avisos no resultado da revisão, mas não os corrija se não bloquearem a implantação.**

Problemas e respostas comuns:

- BCP081 (tipo não definido) → a versão da API provavelmente está incorreta. Consulte o Microsoft Docs e use a versão estável mais recente
- BCP036 (incompatibilidade de tipo) → verifique maiúsculas/minúsculas e o tipo do valor da propriedade e corrija
- BCP037 (propriedade não permitida) → consulte o Microsoft Docs para verificar o suporte nessa versão da API
- no-hardcoded-env-urls → URLs fixas em nomes de DNS Zone podem ser inevitáveis no Bicep. Registre isso no resultado

### Etapa 3: aplicar a lista de verificação

Revise os itens abaixo após a compilação ser aprovada. Consulte todas as armadilhas em `references/service-gotchas.md`.

#### Crítico (correção obrigatória)

- [ ] A configuração `customSubDomainName` do Microsoft Foundry existe. **Ela não pode ser alterada após a criação; se estiver ausente, exclua e recrie o recurso**
- [ ] Ao usar Microsoft Foundry, **o Foundry Project (`accounts/projects`) existe**. Sem ele, o portal não fica disponível
- [ ] Microsoft Foundry `identity: { type: 'SystemAssigned' }`. Sem isso, a criação do Project falha
- [ ] `publicNetworkAccess: 'Disabled'` em todos os serviços que usam PE
- [ ] ADLS Gen2 `isHnsEnabled: true`. Sem isso, o recurso se torna Blob Storage comum
- [ ] pe-subnet `privateEndpointNetworkPolicies: 'Disabled'`. Sem isso, a criação do PE falha
- [ ] Há um Private DNS Zone Group para cada PE
- [ ] Key Vault `enablePurgeProtection: true`

#### Alto (correção recomendada)

- [ ] Storage `allowBlobPublicAccess: false`, `minimumTlsVersion: 'TLS1_2'`
- [ ] Private DNS Zone VNet Link `registrationEnabled: false`
- [ ] Os tipos de recurso e valores de `kind` de cada serviço correspondem a `references/ai-data.md` ou ao Microsoft Docs
- [ ] Implantações de modelos: ordem garantida (`dependsOn`)
- [ ] Não há valores confidenciais nos arquivos de parâmetros. **Remova-os imediatamente se encontrados**

#### Médio (recomendado)

- [ ] Prevenção de colisões de nomes de recursos com `uniqueString()`
- [ ] Uso de dependências implícitas por referências de recursos

### Etapa 4: verificar regressão de valores fixos (evitar vazamento de informações dinâmicas)

Verifique se os itens abaixo não estão definidos como valores literais fixos no código Bicep:

#### Parametrização obrigatória (sem valores fixos)

- [ ] `location`: nomes literais de regiões (`'eastus'`, `'koreacentral'` etc.) não são usados diretamente; o valor é passado por `param location`
- [ ] Nome/versão do modelo: não são literais; use valores confirmados na Fase 1 e cuja disponibilidade foi validada na Etapa 0
- [ ] SKU: use os valores confirmados

#### Verificar se valores dinâmicos não voltaram às referências

Isso não faz parte diretamente do escopo da revisão. Porém, remova versões específicas de API, listas de SKUs ou regiões fixadas em comentários ou descrições de parâmetros. Substitua-as por orientação para consultar o Microsoft Docs.

#### Verificação de violações das regras de decisão

- [ ] Se `kind: 'OpenAI'` for usado em vez de Foundry → altere para `kind: 'AIServices'`, salvo solicitação explícita
- [ ] Se Hub (`MachineLearningServices`) for usado para IA/RAG em geral → altere para Foundry, salvo solicitação explícita
- [ ] Se um recurso autônomo do Azure OpenAI for usado → sugira avaliar o Foundry, salvo solicitação explícita ou indicação de necessidade no Microsoft Docs

### Etapa 5: compilar novamente após as correções

Se as Etapas 2 a 4 resultarem em alterações, execute `az bicep build` novamente para verificar se não surgiram novos erros.

### Limitações de `az bicep build`

A compilação valida somente sintaxe e tipos. Ela não detecta os itens abaixo, que são verificados pela análise de alterações (`az deployment group what-if`) da Fase 4:

- SKU desativada ou indisponível
- Disponibilidade regional do serviço
- Validade do nome do modelo
- Propriedades disponíveis somente em versão prévia
- Alterações de políticas do serviço (cota, capacidade etc.)

Informe essas limitações no resultado da revisão para esclarecer a importância da análise de alterações (`what-if`).

### Etapa 6: relatar os resultados

```markdown
## Resultado da revisão do código Bicep

**Resultado da compilação**: [APROVADO/N avisos]
**Lista de verificação**: ✅ X itens aprovados / ⚠️ X avisos
**Verificação de valores fixos**: [APROVADO / N violações]
**Correções automáticas**: X itens

### Avisos de compilação restantes
- [Conteúdo do aviso, incluindo o motivo pelo qual não pode ser corrigido]

### Detalhes das correções automáticas
- [Arquivo:número da linha] Antes → Depois (motivo)

### Violações de valores fixos (se houver)
- [Arquivo:número da linha] [Detalhes da violação] → [Método de correção]

**Conclusão**: [Pronto para implantação / Revisão manual obrigatória]
```

### Etapa 7: transição para a Fase 4 com mensagem obrigatória de tranquilização

Ao perguntar se deve seguir para a Fase 4 após a aprovação da revisão, **sempre inclua uma mensagem tranquilizadora**.
A palavra "implantação" pode gerar receio. Explique claramente que a análise de alterações (`what-if`) é uma etapa segura de validação.

```
ask_user({
  question: "A revisão do código foi aprovada! Deseja seguir para a próxima etapa?\n\n⚡ Isso NÃO implanta imediatamente:\n  1️⃣ Análise de alterações (what-if): simula o que será criado (não é uma implantação; é segura)\n  2️⃣ Diagrama de visualização: revise em um diagrama a arquitetura que será implantada\n  3️⃣ Confirmação final: a implantação real só ocorre após sua revisão e aprovação do diagrama\n\nNada será implantado sem sua aprovação.",
  choices: [
    "Seguir para a próxima etapa (análise de alterações + diagrama de visualização) (Recomendado)",
    "Quero somente o código; farei a implantação depois"
  ]
})
```

**Pontos principais:**

- Sempre informe: "Isso NÃO implanta imediatamente"
- Explique o processo de três etapas: análise de alterações → diagrama de visualização → confirmação final
- Tranquilize com: "Nada será implantado sem sua aprovação"
