---
name: "refactor"
description: "Melhore a estrutura interna protegida por testes aprovados sem alterar o comportamento observável nem romper a rastreabilidade por REQ-ID."
argument-hint: "target=<file-or-package> smell=<code-smell>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /refactor

## Objetivo

Melhorar a estrutura interna do código existente sem alterar seu funcionamento. Uma mudança que altera o comportamento não é uma refatoração. Ela pertence a `/implement` ou `/fix-bug`. O resultado mantém todos os testes existentes aprovados com os mesmos nomes e todos os vínculos de `REQ-ID` intactos: um problema estrutural, uma transformação, uma solicitação de integração.

> [!WARNING]
> Se qualquer saída, asserção ou assinatura pública mudar, não se trata de uma refatoração. Pare e use `/implement` ou `/fix-bug`.

## Quando usar

Use quando um problema estrutural identificado estiver atrasando a equipe e o alvo tiver uma rede de segurança de testes aprovados, ou puder recebê-la rapidamente. Execute em uma ramificação dedicada `impl/<NNN>-<feature>`, separada de qualquer trabalho de funcionalidade ou correção de defeito.

## Pré-condições

- O arquivo, pacote ou componente alvo existe e compila
- Os testes atuais passam, ou testes de caracterização podem ser adicionados primeiro
- Nenhum `/fix-bug` está pendente no mesmo código. Os defeitos são corrigidos antes da refatoração, a partir de uma base limpa
- Todas as restrições em `plan.md` ou nos ADRs, por exemplo, "os controladores permanecem enxutos", são conhecidas

## Entradas que a equipe deve fornecer

- O arquivo, pacote ou componente alvo
- A motivação: o problema estrutural observado (`Long Method`, método longo; `Duplication`, duplicação; `Primitive Obsession`, obsessão por primitivos; `Feature Envy`, inveja de funcionalidade; entre outros)
- Todas as restrições de `plan.md` ou dos ADRs que limitem a mudança
- A cobertura de testes atual da área (execute um relatório de cobertura se ela for desconhecida)
- Solicite à pessoa usuária qualquer item ausente.

## O que farei

- Confirmarei a rede de segurança. Se a cobertura de linhas estiver abaixo de 80%, escreverei primeiro testes de caracterização
- Identificarei precisamente o problema estrutural pelo catálogo e citarei uma ou duas linhas como evidência
- Escolherei uma transformação de Fowler adequada e a aplicarei como uma única etapa que preserva o comportamento
- Executarei os testes antes e depois de cada microetapa, mantendo a suíte aprovada em cada registro de alteração
- Moverei cada anotação `@implements REQ-NNN` com seu método, sem alterações

## O que não farei

- Refatorar sem testes. Isso é uma reescrita com outro nome
- Alterar o comportamento sob o pretexto de refatorar. Se qualquer saída ou asserção mudar, o trabalho será inválido
- Fazer "pequenas melhorias" no código vizinho. Permanecerei estritamente no problema estrutural identificado
- Renomear ou remodelar uma API pública sem um plano de migração ou descontinuação
- Combinar uma refatoração com uma funcionalidade ou correção de defeito na mesma solicitação de integração
- Inventar um comportamento novo que a especificação não descreva. Farei somente mudanças estruturais; dúvidas sobre requisitos seguem para `/update-spec`

## Formato da saída

```markdown
### Problema estrutural identificado
`Long Method` (método longo): `FeeService.calculate()` ocupa 74 linhas em três ramificações aninhadas.

### Refatoração escolhida
`Extract Method` (extrair método): mover cada ramificação para `applyExemption`, `applyCeiling` e `applyRounding`.

### Diferenças
<before/after for every touched file>

### Resultados dos testes
`./mvnw test` → 12 aprovados (com os mesmos nomes anteriores).

### Observação sobre a preservação do comportamento
API pública inalterada. Nenhuma cláusula `throws` nova. Nenhuma migração de banco de dados. Nenhuma variável de ambiente nova.

### Mensagem do registro de alteração
refactor(fees): extrair as etapas de cálculo da tarifa

Divide calculate() em três métodos privados. Sem alteração de comportamento.
Referências: REQ-031
```

## Definição de pronto

- [ ] Todos os testes aprovados anteriormente continuam aprovados, com os mesmos nomes
- [ ] Nenhuma mudança na API pública, exceção nova ou dependência nova
- [ ] A cobertura não diminui
- [ ] Um problema estrutural, uma transformação, uma solicitação de integração
- [ ] Todas as anotações `@implements REQ-NNN` permanecem presentes e corretas
- [ ] A mensagem do registro de alteração usa o tipo `refactor:` e declara "sem alteração de comportamento"

## Corpo do prompt

Você é `@implementer`. A equipe quer uma melhoria estrutural que preserve o comportamento. Leia a habilidade [`refactor-safely`](../skills/refactor-safely/SKILL.md) antes de começar. Ela define os procedimentos de rede de segurança, pequenas etapas e testes de caracterização.

**Etapa 1: confirme a rede de segurança.**
Verifique a cobertura de linhas do alvo. Se estiver abaixo de 80%, escreva testes de caracterização que fixem o comportamento atual, inclusive suas peculiaridades, antes de mudar qualquer coisa. Refatorar sem testes é reescrever.

**Etapa 2: identifique o problema estrutural com precisão.**
Escolha no catálogo: `Long Method` (método longo), `Large Class` (classe grande), `Primitive Obsession` (obsessão por primitivos), `Data Clumps` (aglomerados de dados), `Feature Envy` (inveja de funcionalidade), `Shotgun Surgery` (cirurgia dispersa) ou `Divergent Change` (mudança divergente). Cite uma ou duas linhas como evidência. A solicitação "deixe mais limpo" será rejeitada.

**Etapa 3: escolha uma transformação de Fowler.**
Escolha a transformação correspondente, como `Extract Method` (extrair método), `Extract Class` (extrair classe), `Replace Conditional with Polymorphism` (substituir condicional por polimorfismo) ou `Introduce Parameter Object` (introduzir objeto de parâmetro). Aplique exatamente uma transformação por registro de alteração.

**Etapa 4: execute os testes antes de alterar qualquer coisa.**
Confirme que os testes passam. Se algum falhar ou for ignorado, corrija isso primeiro. Nunca refatore uma compilação quebrada.

**Etapa 5: aplique a transformação.**
Prefira as ferramentas de refatoração do ambiente de desenvolvimento integrado (IDE): `Extract` (extrair), `Rename` (renomear) e `Move` (mover). As edições manuais devem preservar as assinaturas dos métodos, exceto quando a transformação for `Change Function Declaration` (alterar declaração da função) com um plano de migração.

**Etapa 6: execute os testes após cada microetapa.**
A suíte deve permanecer aprovada em cada registro de alteração. Se ela falhar e você não souber o motivo, reverta e dê uma etapa menor. Mova cada anotação `@implements REQ-NNN` com seu método.

**Etapa 7: pare quando o problema estrutural desaparecer.**
Não refatore o código vizinho. Cada chamada corresponde a uma conversa, uma solicitação de integração e um problema estrutural.

Se uma alteração real de comportamento ou um requisito novo surgir durante a refatoração, pare e encaminhe para `/implement`, `/fix-bug` ou `/update-spec`. Não incorpore isso a esta mudança.

## Exemplo de chamada

```
/refactor target=backend/src/main/java/com/example/app/fees/FeeService.java smell=long-method
```
