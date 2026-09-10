---
name: "tdd"
description: "Conduza um comportamento por um ciclo estrito de vermelho-verde-refatorar, produzindo registros de alteração separados para as fases vermelha (red), verde (green) e de refatoração (refactor)."
argument-hint: "behavior=<behavior> req=REQ-NNN target=<file-or-class>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /tdd

## Objetivo

Produzir um ciclo completo orientado por testes para um único comportamento, entregue em três registros de alteração separados: `red` (vermelho), `green` (verde) e `refactor` (refatoração). Nenhum código de produção é escrito sem um teste falhando, e nenhum primeiro teste é escrito para passar imediatamente. O comportamento deve corresponder a exatamente um critério de aceitação de um `REQ-ID`.

> [!NOTE]
> Um teste falhando por vez. Nunca mantenha dois estados `red` (vermelho). Se o primeiro teste for difícil de escrever, o projeto está revelando um problema.

## Quando usar

Use durante a Etapa 3 para descobrir ou fortalecer um comportamento pequeno, como uma lógica nova, um limite ou um caso extremo, quando o projeto ainda não estiver evidente e uma rede de segurança baseada em testes antecipados agregar mais valor.

## Pré-condições

- `specs/<NNN>-<feature>/spec.md` contém o `REQ-ID` e o critério de aceitação ao qual o comportamento corresponde
- A ramificação atual é `impl/<NNN>-<feature>`
- A estrutura de testes está disponível: JUnit 5 + AssertJ (Java) ou Vitest + Testing Library (TypeScript)
- O módulo alvo já tem sua estrutura inicial, ou este ciclo cria sua primeira classe

## Entradas que a equipe deve fornecer

- O comportamento a descobrir, em linguagem simples
- O `REQ-ID` vinculado em `specs/<NNN>-<feature>/spec.md`
- O arquivo ou a classe alvo (se não existir, informe isso. TDD também orienta o projeto, portanto sua criação é aceitável)
- Solicite à pessoa usuária qualquer item ausente.

## O que farei

- Escolherei o caso não trivial mais simples e escreverei um teste falhando que nomeie o comportamento
- Confirmarei que o teste falha pelo motivo correto e criarei o registro de alteração do estado vermelho (`red`)
- Escreverei o menor código de produção que faça o teste passar, confirmarei que toda a suíte está aprovada e criarei o registro de alteração
- Refatorarei no estado verde (`green`) com uma transformação de Fowler, manterei todos os testes aprovados e criarei o registro de alteração
- Informarei o comportamento descoberto, os três registros de alteração e o próximo teste a escrever

## O que não farei

- Escrever o teste e o código juntos. Isso é verificação, não TDD
- Manter dois testes falhando ao mesmo tempo ou ignorar a fase de refatoração (`refactor`)
- Alterar o comportamento sob o pretexto de refatorar. Se uma asserção mudar, o ciclo será inválido
- Testar métodos privados ou simular todas as dependências
- Inventar um critério de aceitação ausente da especificação. Se o comportamento não tiver `REQ-ID`, pararei e o encaminharei para `/update-spec` em vez de tentar adivinhar
- Implementar neste ciclo o próximo teste sugerido

## Formato da saída

```markdown
### Comportamento descoberto
Uma pessoa pagadora isenta de impostos recebe tarifa zero. (REQ-031, critério 2)

### Registros de alteração
| Fase | Mensagem | Arquivos | Resultado |
|---|---|---|---|
| red | `test(fees): red - tarifa zero para pessoa pagadora isenta` | `FeeServiceTest.java` | 1 falhando |
| green | `feat(fees): green - implementar REQ-031 (mínimo)` | `FeeService.java` | 12 aprovados |
| refactor | `refactor(fees): extrair a verificação de isenção` | `FeeService.java` | 12 aprovados |

### Arquivo de teste
<complete test source, with an inline `// REQ-031` comment>

### Código de produção
<complete source after the refactor phase>

### Sugestão para o próximo ciclo
Adicione um teste de limite: tarifa no limiar de isenção. (Não implementado aqui.)
```

## Definição de pronto

- [ ] Existem três registros de alteração separados: `test:` (`red`), `feat:` (`green`) e `refactor:`
- [ ] O registro da fase vermelha (`red`) é reproduzivelmente vermelho: acessá-lo faz a compilação falhar
- [ ] O registro da fase verde (`green`) contém o mínimo necessário para passar
- [ ] O registro da fase de refatoração (`refactor`) altera somente a estrutura. Os nomes dos testes e as asserções permanecem inalterados
- [ ] A suíte completa termina aprovada
- [ ] O comportamento corresponde a exatamente um critério de aceitação de um `REQ-ID`, citado por um comentário `// REQ-NNN` na mesma linha

## Corpo do prompt

Você é `@implementer`. A equipe quer descobrir um comportamento começando pelo teste. Leia a habilidade [`tdd-workflow`](../skills/tdd-workflow/SKILL.md) antes de começar. Ela define o ciclo, as regras e os antipadrões. Execute exatamente três fases e não as combine.

**Etapa 1: VERMELHO (`RED`), escreva o teste que falha.**
Escolha o caso não trivial mais simples, não o caso vazio nem o caso catastrófico. Nomeie o teste como `should_<expected>_when_<condition>` e adicione um comentário `// REQ-NNN` na mesma linha. Use Preparar-Agir-Verificar, com linhas em branco entre as seções.

**Etapa 2: VERMELHO (`RED`), confirme e crie o registro de alteração.**
Execute o teste. Confirme que ele falha e leia a mensagem para verificar se a causa é a esperada (asserção ou compilação, não um erro de configuração). Crie o registro com a mensagem `test(<scope>): red - <behavior>`.

**Etapa 3: VERDE (`GREEN`), escreva o menor código que passa.**
Escreva o mínimo de código de produção que faça o teste passar. No primeiro ciclo, é permitido simular com um valor fixo. Execute o teste isolado e depois a suíte completa. Ambos devem passar.

**Etapa 4: VERDE (`GREEN`), crie o registro de alteração.**
Crie o registro com a mensagem `feat(<scope>): green - implementar REQ-NNN (mínimo)`.

**Etapa 5: REFATORAÇÃO (`REFACTOR`), melhore no estado verde.**
Procure duplicação, nomes enganosos e obsessão por primitivos. Aplique uma transformação de Fowler: `Extract Method` (extrair método), `Rename` (renomear) ou `Inline Variable` (incorporar variável). Execute todos os testes após cada microetapa. Eles devem continuar aprovados.

**Etapa 6: REFATORAÇÃO (`REFACTOR`), crie o registro de alteração e pare.**
Crie o registro com a mensagem `refactor(<scope>): <description>`. Pare quando o projeto estiver adequado ao próximo ciclo, sem buscar perfeição.

**Etapa 7: relate e encaminhe.**
Declare o comportamento descoberto em uma frase, liste os três registros de alteração e identifique o próximo teste (limite, erro ou segunda variação) sem implementá-lo.

Nunca retorne `null`, nunca use `any` e mascare CPF ou valores de benefícios em qualquer linha de registro (log). Se o comportamento não corresponder a um `REQ-ID`, pare e encaminhe para `/update-spec`. Não invente o requisito.

## Exemplo de chamada

```
/tdd behavior="tarifa zero para pessoa pagadora isenta de impostos" req=REQ-031 target=FeeService
```
