# Fase 4: agente de implantação

Este arquivo contém as instruções detalhadas da Fase 4. Leia-o e siga-o quando a implantação for aprovada após a conclusão da Fase 3 (revisão de código).

---

**🚨🚨🚨 Ordem de execução obrigatória da Fase 4: nunca pule nenhuma etapa 🚨🚨🚨**

Execute as cinco etapas abaixo **rigorosamente na ordem**. Nenhuma etapa pode ser omitida.
Mesmo que a pessoa peça "implante", "pode seguir", "faça" etc., sempre comece pela Etapa 1.

```
Etapa 1: verificar os pré-requisitos (az login, assinatura, grupo de recursos)
    ↓
Etapa 2: análise de alterações, what-if (az deployment group what-if) ← execução obrigatória
    ↓
Etapa 3: gerar o diagrama de visualização (02_arch_diagram_preview.html) ← geração obrigatória
    ↓
Etapa 4: implantação real após a confirmação final (az deployment group create)
    ↓
Etapa 5: gerar o diagrama do resultado da implantação (03_arch_diagram_result.html)
```

**Nunca faça o seguinte:**

- Executar `az deployment group create` diretamente, sem a análise de alterações (`what-if`)
- Pular a geração do diagrama de visualização (`02_arch_diagram_preview.html`)
- Prosseguir com a implantação sem apresentar o resultado da análise de alterações
- Fornecer somente comandos `az` para execução manual

---

## Etapa 1: verificar os pré-requisitos

```powershell
# Verifica a instalação e a autenticação da CLI az
az account show 2>&1
```

Se não houver autenticação, peça para executar `az login`.
O agente nunca deve inserir nem armazenar credenciais diretamente.

Crie o grupo de recursos:

```powershell
az group create --name "<RG_NAME>" --location "<LOCATION>"  # Local confirmado na Fase 1
```

→ Após confirmar o sucesso, siga para a próxima etapa

## Etapa 2: validação (`validate`) → análise de alterações (`what-if`), 🚨 obrigatória

**Não pule esta etapa. Sempre a execute, independentemente da urgência da solicitação.**

**Etapa 2-A: executar primeiro o validate (pré-validação rápida)**

A análise de alterações (`what-if`) pode **ficar travada indefinidamente sem mensagens de erro** quando há violações de Azure Policy, erros de referência de recursos etc.
Para evitar isso, **sempre execute a validação (`validate`) primeiro**. Ela retorna erros rapidamente.

```powershell
# validate: detecta rapidamente violações de política, erros de esquema e problemas de parâmetros
az deployment group validate `
  --resource-group "<RG_NAME>" `
  --parameters main.bicepparam
```

- **Validação bem-sucedida** → siga para a Etapa 2-B (análise de alterações)
- **Falha na validação** → analise as mensagens, corrija o Bicep, compile e valide novamente
  - Violação de Azure Policy (`RequestDisallowedByPolicy`) → reflita no Bicep os requisitos da política (por exemplo, `azureADOnlyAuthentication: true`)
  - Erro de esquema → corrija a versão da API ou as propriedades
  - Erro de parâmetro → corrija o arquivo de parâmetros

**Etapa 2-B: executar a análise de alterações (`what-if`)**

Execute a análise de alterações após a aprovação da validação.

**Escolha o método de passagem de parâmetros:**

- Se todos os parâmetros `@secure()` tiverem valores padrão → use `.bicepparam`
- Se parâmetros `@secure()` exigirem entrada → use `--template-file` + arquivo de parâmetros JSON

```powershell
# Método 1: usa .bicepparam (quando todos os parâmetros @secure() têm valores padrão)
az deployment group what-if `
  --resource-group "<RG_NAME>" `
  --parameters main.bicepparam

# Método 2: usa arquivo de parâmetros JSON (quando parâmetros @secure() exigem entrada)
az deployment group what-if `
  --resource-group "<RG_NAME>" `
  --template-file main.bicep `
  --parameters main.parameters.json `
  --parameters secureParam='value'
```

→ Resuma e apresente o resultado da análise de alterações.

**⏱️ Método de execução e tratamento do tempo limite da análise de alterações:**

A análise de alterações valida recursos no servidor do Azure. A duração depende do serviço e da região.
**Sempre execute com `initial_wait: 300` (cinco minutos).** Se não terminar nesse prazo, o tempo limite será atingido automaticamente.

```powershell
# Sempre define initial_wait: 300 ao chamar a ferramenta powershell
# mode: "sync", initial_wait: 300
az deployment group what-if `
  --resource-group "<RG_NAME>" `
  --parameters main.bicepparam
```

**Concluída em cinco minutos** → prossiga normalmente (resumo → diagrama de visualização → confirmação da implantação)

**Não concluída em cinco minutos (tempo limite)** → interrompa imediatamente com `stop_powershell` e ofereça opções:

```
ask_user({
  question: "A análise de alterações (what-if) não terminou em cinco minutos. A resposta do servidor do Azure está atrasada. Como você deseja prosseguir?",
  choices: [
    "Tentar novamente (Recomendado)",
    "Pular a análise de alterações e implantar diretamente"
  ]
})
```

**Se "Tentar novamente" for selecionado:** execute o mesmo comando com `initial_wait: 300`. Faça no máximo duas tentativas.
**Se "Pular a análise de alterações e implantar diretamente" for selecionado:**

- Gere o diagrama de visualização com base no rascunho da Fase 1
- Informe os riscos:
  > **⚠️ Implantação sem análise prévia de alterações (`what-if`).** Podem ocorrer alterações inesperadas nos recursos. Verifique-as no portal do Azure após a implantação.

**Nunca faça o seguinte:**

- Executar sem definir `initial_wait`, causando espera indefinida
- Permitir que o agente decida arbitrariamente que "a análise de alterações é opcional" e a pule
- Passar automaticamente à implantação após atingir o tempo limite, sem perguntar
- Pular a análise de alterações porque "a implantação é mais rápida"

## Etapa 3: diagrama de visualização baseado no resultado da análise de alterações, 🚨 obrigatório

**Não pule esta etapa. Sempre gere o diagrama de visualização quando a análise de alterações for bem-sucedida.**

Gere novamente o diagrama usando os recursos reais do resultado da análise de alterações (nomes, tipos, locais e quantidades).
Mantenha inalterado o rascunho da Fase 1 (`01_arch_diagram_draft.html`) e gere `02_arch_diagram_preview.html`.
O rascunho pode ser reaberto a qualquer momento.

```
## Arquitetura que será implantada (com base na análise de alterações)

[Link do diagrama interativo: 02_arch_diagram_preview.html]
(Rascunho do projeto: 01_arch_diagram_draft.html)

Recursos que serão criados (N itens):
[Tabela de resumo da análise de alterações]

Implantar estes recursos? (Sim/Não)
```

Siga para a Etapa 4 após a confirmação. **Não prossiga com a implantação sem o diagrama de visualização.**

## Etapa 4: implantação real

Execute somente após a revisão do diagrama, do resultado da análise de alterações e da aprovação da implantação.
**Use o mesmo método de passagem de parâmetros da análise de alterações.**

```powershell
$deployName = "deploy-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Método 1: usa .bicepparam
az deployment group create `
  --resource-group "<RG_NAME>" `
  --parameters main.bicepparam `
  --name $deployName `
  2>&1 | Tee-Object -FilePath deployment.log

# Método 2: usa arquivo de parâmetros JSON
az deployment group create `
  --resource-group "<RG_NAME>" `
  --template-file main.bicep `
  --parameters main.parameters.json `
  --name $deployName `
  2>&1 | Tee-Object -FilePath deployment.log
```

Monitore periodicamente o progresso durante a implantação:

```powershell
az deployment group show `
  --resource-group "<RG_NAME>" `
  --name "<DEPLOYMENT_NAME>" `
  --query "{status:properties.provisioningState, duration:properties.duration}" `
  -o table
```

## Tratamento de falhas na implantação

Quando a implantação falha, alguns recursos podem permanecer no estado `Failed`. Reimplantar nesse estado causa erros como `AccountIsNotSucceeded`.

**⚠️ A exclusão de recursos é destrutiva. Sempre explique a situação e obtenha aprovação antes de executar.**

```
[Nome do recurso] falhou durante a implantação.
Para reimplantar, primeiro exclua os recursos com falha.

Excluir e reimplantar? (Sim/Não)
```

Após a aprovação, exclua os recursos com falha e reimplante.

**🔹 Tratamento de recursos excluídos de forma reversível (evitar bloqueio da reimplantação):**

Quando um grupo de recursos é excluído após uma falha, Cognitive Services (Foundry), Key Vault etc. permanecem em **exclusão reversível (`soft-delete`)**.
Reimplantar com o mesmo nome causa erros `FlagMustBeSetForRestore` e `Conflict`.

**Sempre verifique antes da reimplantação:**

```powershell
# Verifica Cognitive Services em exclusão reversível
az cognitiveservices account list-deleted -o table

# Verifica Key Vault em exclusão reversível
az keyvault list-deleted -o table
```

**Opções de resolução:**

```
ask_user({
  question: "Foram encontrados recursos em exclusão reversível (soft-delete) de uma implantação anterior. Como você deseja tratá-los?",
  choices: [
    "Limpar e reimplantar (Recomendado): excluir definitivamente e criar novos recursos",
    "Reimplantar em modo de restauração: recuperar os recursos existentes"
  ]
})
```

**Cuidado: Key Vault com `enablePurgeProtection: true`:**

- Não pode ser limpo definitivamente (aguarde o término do período de retenção)
- Não pode ser recriado com o mesmo nome
- **Solução: altere o nome do Key Vault** e reimplante (por exemplo, adicione uma marca de data e hora à semente de `uniqueString()`)
- Explique a situação e oriente a alteração do nome

## Etapa 5: implantação concluída, gerar o diagrama com os recursos reais e relatar

Após concluir a implantação, consulte os recursos realmente implantados e gere o diagrama final.

**Etapa 1: consultar os recursos implantados**

```powershell
az resource list --resource-group "<RG_NAME>" --output json
```

**Etapa 2: gerar o diagrama com os recursos reais**

Extraia nomes, tipos, SKUs e pontos de extremidade dos recursos e gere o diagrama final com o mecanismo integrado.
Tenha cuidado com os nomes dos arquivos para não sobrescrever diagramas anteriores:

- `01_arch_diagram_draft.html`: rascunho do projeto (manter)
- `02_arch_diagram_preview.html`: visualização da análise de alterações (manter)
- `03_arch_diagram_result.html`: versão final do resultado da implantação

Preencha o JSON `services` do diagrama com as informações reais:

- `name`: nome real do recurso (por exemplo, `foundry-duru57kxgqzxs`)
- `sku`: SKU real
- `details`: valores reais, como pontos de extremidade e local

**Etapa 3: relatar**

```
## Implantação concluída

[Diagrama interativo da arquitetura: 03_arch_diagram_result.html]
(Rascunho do projeto: 01_arch_diagram_draft.html | Visualização da análise de alterações: 02_arch_diagram_preview.html)

Recursos criados (N itens):
[Nomes, tipos e pontos de extremidade extraídos dinamicamente do resultado real]

## Próximas etapas
1. Verifique os recursos no portal do Azure
2. Verifique o estado da conexão do Private Endpoint
3. Consulte orientações de configuração adicionais, se necessário

## Comando de limpeza (se necessário)
az group delete --name <RG_NAME> --yes --no-wait
```

---

## Tratamento de solicitações de alteração após a implantação

**Quando houver uma solicitação de adição, alteração ou exclusão após a implantação, NÃO vá diretamente para o Bicep/implantação.**
Sempre retorne à Fase 1 e atualize primeiro a arquitetura.

**Processo:**

1. **Confirme a intenção**: pergunte primeiro se a pessoa quer adicionar à arquitetura implantada:

   ```
   Você quer adicionar uma VM à arquitetura implantada?
   Configuração atual: [Resumo dos serviços implantados]
   ```

2. **Retorne à Fase 1 e aplique a Regra de Confirmação das Alterações**
   - Use o resultado existente (`03_arch_diagram_result.html`) como referência do estado atual
   - Verifique os campos obrigatórios dos novos serviços (SKU, rede, disponibilidade regional etc.)
   - Confirme itens em aberto por `ask_user`
   - Verifique os fatos (consulta ao Microsoft Docs + validação cruzada)

3. **Gere o diagrama atualizado**
   - Combine os recursos implantados e os novos recursos em `04_arch_diagram_update_draft.html`
   - Apresente o diagrama e obtenha confirmação:

   ```
   ## Arquitetura atualizada

   [Diagrama interativo: 04_arch_diagram_update_draft.html]
   (Resultado da implantação anterior: 03_arch_diagram_result.html)

   **Alterações:**
   - Adicionados: [Lista de novos serviços]
   - Removidos: [Lista de serviços removidos] (se houver)

   Prosseguir com esta configuração?
   ```

4. **Após a confirmação, execute as Fases 2 → 3 → 4 na ordem**
   - Adicione incrementalmente os módulos dos novos recursos ao Bicep existente
   - Revisão → análise de alterações (`what-if`) → implantação incremental

**Nunca faça o seguinte:**

- Ir diretamente para a geração de Bicep sem atualizar o diagrama após uma solicitação de alteração
- Ignorar o estado da implantação existente e criar novos recursos isoladamente
- Prosseguir sem confirmar se os recursos devem ser adicionados à arquitetura existente
