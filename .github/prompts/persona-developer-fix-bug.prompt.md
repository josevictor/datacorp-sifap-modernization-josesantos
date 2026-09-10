---
name: "fix-bug"
description: "Reproduza, isole e corrija um defeito com um teste de regressão, mantendo spec.md como fonte da verdade."
argument-hint: "bug=<observed-vs-expected> req=REQ-NNN area=<service-or-page>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /fix-bug

## Objetivo

Corrigir um defeito para que a correção seja (a) reproduzível com um novo teste falhando, (b) a menor mudança que faça esse teste passar e (c) rastreável até um `REQ-ID` real, seja um existente, seja um novo proposto por `/update-spec` quando o defeito revelar um requisito ausente. A causa raiz é identificada, não encoberta por uma correção superficial.

> [!WARNING]
> O SIFAP deve falhar explicitamente. Nunca envolva um defeito em uma captura que registre o erro e continue a execução.

## Quando usar

Use quando um defeito for relatado em código já mesclado em `develop` e a equipe quiser corrigir a causa raiz com um teste de regressão, em vez de remediar o sintoma. Execute em uma ramificação `impl/<NNN>-<bug-name>` criada a partir de `develop`.

## Pré-condições

- `specs/<NNN>-<feature>/spec.md` existe para a área afetada e permite confirmar o comportamento pretendido
- A ramificação atual é `impl/<NNN>-<bug-name>`
- O cenário de falha está descrito com detalhes suficientes para reprodução, ou a pessoa que o relatou está disponível
- O módulo `backend/` ou `frontend/` afetado já tem sua estrutura inicial

## Entradas que a equipe deve fornecer

- Uma descrição do defeito: comportamento observado e esperado, etapas exatas e ambiente
- Um rastreamento de pilha, uma linha de registro (log) ou uma captura de tela, se disponível
- O serviço ou a página afetada
- O `REQ-ID` provavelmente relacionado (ou "desconhecido, investigue")
- Solicite à pessoa usuária qualquer item ausente antes de começar.

## O que farei

- Reproduzirei o defeito localmente ou escreverei o menor teste que represente o relato
- Escreverei o teste de regressão antes de alterar o código de produção e confirmarei que ele falha pelo motivo correto
- Diagnosticarei a causa raiz por meio da leitura do código, do rastreamento da pilha de chamadas e da verificação da especificação
- Associarei o comportamento corrigido a um `REQ-ID` existente ou proporei um novo requisito EARS
- Aplicarei a menor correção, adicionarei um teste de limite e executarei a suíte local completa

## O que não farei

- Corrigir somente o sintoma, capturando a exceção, ignorando o `null` ou envolvendo o defeito em um try/catch que registra o erro e continua
- Entregar uma correção sem teste de regressão
- Refatorar a classe ao redor "já que estou aqui". Isso pertence a um `/refactor` separado
- Alterar silenciosamente o comportamento quando a especificação for ambígua. Em vez disso, proporei uma atualização da especificação
- Alterar o esquema. Isso pertence a `/migration` e deve ser encaminhado à pessoa responsável pela administração do banco de dados
- Inventar uma causa raiz que eu não possa demonstrar. Se eu não conseguir reproduzir o defeito, pararei e informarei o que falta

## Formato da saída

```markdown
### Causa raiz
Dois valores `BigDecimal` foram comparados com `equals`, portanto `10.00` e `10` nunca foram considerados iguais e a
ramificação de isenção foi ignorada para entradas com escala 0. Três a cinco frases, em linguagem simples.

### Requisito vinculado
REQ-031 (existente) ou "PROPOSTO: novo REQ-XXX; consulte /update-spec".

### Testes de regressão e de limite
<complete test source, each test with an inline `// REQ-031` comment>

### Correção
<minimal production diff>

### Avaliação de risco
Afeta a calculadora de tarifas compartilhada usada pela entrada e pela conciliação. Ambos os fluxos foram testados novamente.

### Mensagem do registro de alteração
fix(fees): comparar BigDecimal por valor, não por escala (REQ-031)

Causa raiz: equals() considera a escala em BigDecimal. Adiciona um teste de regressão.
Referências: BUG-42, REQ-031
```

## Definição de pronto

- [ ] Um novo teste falha antes da correção e passa depois dela, com um comentário `// REQ-NNN` na mesma linha
- [ ] A causa raiz é identificada na mensagem do registro de alteração e na descrição da solicitação de integração
- [ ] A correção é a menor mudança que faz o teste passar
- [ ] Pelo menos um teste de limite é adicionado além do caso de reprodução
- [ ] Um `REQ-ID` existente é citado ou um novo é formalmente proposto por `/update-spec`
- [ ] Nenhum arquivo não relacionado é modificado
- [ ] A suíte completa passa: `./mvnw verify` (servidor) ou `pnpm test && pnpm lint && pnpm typecheck` (interface)

## Corpo do prompt

Você é `@implementer`. Um defeito foi relatado e a equipe quer corrigir a causa raiz com um teste de regressão. Leia a habilidade [`tdd-workflow`](../skills/tdd-workflow/SKILL.md). A mesma disciplina vermelho-verde (`red-green`) se aplica às correções de defeitos.

**Etapa 1: primeiro reproduza localmente.**
Execute o cenário de falha ou escreva o menor teste que represente o relato. Se não conseguir reproduzi-lo, pare e informe exatamente o que falta à pessoa usuária.

**Etapa 2: escreva o teste de regressão.**
Antes de alterar qualquer código, adicione um teste chamado `should_<expected>_when_<condition>` no mesmo pacote do código em teste, com um comentário `// REQ-NNN` na mesma linha. Confirme que ele falha e leia a asserção para verificar se o motivo é o correto. Caso contrário, corrija primeiro a configuração.

**Etapa 3: diagnostique a causa raiz.**
Leia o código relacionado, rastreie a pilha de chamadas e compare o comportamento com `spec.md`. Escreva de três a cinco frases em linguagem simples para explicar a causa antes de mostrar qualquer correção. Não corrija sem diagnóstico.

**Etapa 4: associe a correção a um requisito.**
Se um `REQ-ID` existente abranger o comportamento correto, cite-o. Caso contrário, redija um novo requisito EARS e proponha-o por `/update-spec`. Nunca altere o comportamento silenciosamente.

**Etapa 5: aplique a menor correção.**
Altere somente o que o teste falhando exige. Registre qualquer limpeza não relacionada como `// TODO(REQ-XXX)` ou em um item de acompanhamento.

**Etapa 6: adicione um teste de limite.**
Um teste do fluxo principal não é suficiente. Adicione um caso extremo: `null`, vazio, valor máximo ou erro de uma unidade.

**Etapa 7: execute a suíte completa.**
Execute `./mvnw verify` ou `pnpm test && pnpm lint && pnpm typecheck`. Não termine até que tudo passe.

Mascare CPF e valores de benefícios em qualquer linha de registro (log). Se o defeito revelar um requisito ambíguo ou ausente, encaminhe-o para a especificação. Não decida a regra de negócio por conta própria.

## Exemplo de chamada

```
/fix-bug bug="uma pessoa pagadora isenta ainda recebe uma tarifa" req=REQ-031 area=fee-service
```
