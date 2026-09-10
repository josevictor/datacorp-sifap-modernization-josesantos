---
name: "implement"
description: "Implemente uma única tarefa de tasks.md de ponta a ponta, com código de produção, testes e rastreabilidade por REQ-ID, sem ampliar o escopo."
argument-hint: "task=T-XXX feature=specs/<NNN>-<feature>"
agent: "implementer"
tools: ["read", "search", "edit", "execute"]
---
# /implement

## Objetivo

Implementar **exatamente uma tarefa** de `specs/<NNN>-<feature>/tasks.md` para que todos os critérios de aceitação vinculados sejam atendidos, o controle de qualidade local passe e cada mudança seja rastreável a um `REQ-ID`. O resultado contém código de produção e testes escritos juntos na mesma mudança, sem ampliar o escopo para tarefas vizinhas, sem refatorações não relacionadas e sem editar a própria especificação.

> [!IMPORTANT]
> Uma tarefa por chamada. Abra uma nova conversa para a próxima tarefa. Nunca agrupe tarefas "enquanto estiver no arquivo".

## Quando usar

Use durante a implementação da Etapa 3, quando `tasks.md` existir e a equipe tiver selecionado a próxima tarefa. Execute em uma ramificação `impl/<NNN>-<feature>` criada a partir de `develop`.

## Pré-condições

- `specs/<NNN>-<feature>/tasks.md` existe e contém a tarefa alvo com seus vínculos de `REQ-ID`
- `specs/<NNN>-<feature>/spec.md` contém as declarações EARS e os critérios de aceitação desses `REQ-IDs`
- `specs/<NNN>-<feature>/plan.md` identifica o pacote ou componente afetado pela tarefa
- A ramificação atual é `impl/<NNN>-<feature>`, não `develop` nem `main`
- A equipe já criou a estrutura inicial do módulo `backend/` ou `frontend/` alterado pela tarefa

## Entradas que a equipe deve fornecer

- O ID da tarefa, por exemplo, `T-017`, e a pasta da funcionalidade `specs/<NNN>-<feature>/`
- O conjunto de tecnologias alvo da tarefa: Java 21 + Spring Boot 3.3 ou Next.js 15 + TypeScript estrito
- Todas as decisões de escopo em `02-modern-spec/` que restrinjam a implementação
- Solicite à pessoa usuária qualquer item ausente antes de escrever código.

## O que farei

- Lerei o contrato da tarefa e copiarei seus `REQ-IDs` vinculados, suas dependências e seu marcador de complexidade
- Extrairei cada declaração EARS vinculada e seus critérios de aceitação para um bloco de comentário no arquivo em alteração
- Escreverei um teste falhando por critério de aceitação antes de qualquer código de produção
- Escreverei o menor código de produção que faça os testes passarem, seguindo os padrões do projeto
- Refatorarei com os testes aprovados e marcarei cada método público que atenda ao requisito com `@implements REQ-NNN`
- Executarei o controle de qualidade local e marcarei somente a tarefa implementada em `tasks.md`

## O que não farei

- Implementar uma segunda tarefa "enquanto estiver no arquivo". Cada chamada e cada conversa tratam de uma única tarefa
- Escrever os testes depois do código ou omitir um teste de qualquer critério de aceitação
- Inventar requisito, regra de negócio ou critério de aceitação ausente da especificação. Se um `REQ-ID` for ambíguo, pararei e perguntarei em vez de tentar adivinhar
- Alterar o esquema do banco de dados. Isso pertence a `/migration` e deve ser encaminhado à pessoa responsável pela administração do banco de dados. Também não editarei `spec.md`, pois isso pertence a `/update-spec` e deve ser encaminhado à pessoa Responsável pelo Produto
- Retornar `null`, usar `Optional` como tipo de parâmetro ou usar `any` em TypeScript
- Adicionar uma dependência sem um ADR ou alterar o `// TODO(REQ-XXX)` de outra tarefa

## Formato da saída

```markdown
### Arquivos alterados

| Arquivo | Papel |
|---|---|
| `backend/src/main/java/com/example/app/<feature>/<Feature>Service.java` | Produção: atende ao REQ-042 |
| `backend/src/test/java/com/example/app/<feature>/<Feature>ServiceTest.java` | Teste: um caso por critério de aceitação |
| `backend/src/main/java/com/example/app/<feature>/<Feature>Request.java` | Produção: tipo `record` de requisição com `@Valid` |

### Controle de qualidade
`./mvnw verify` → BUILD SUCCESS (18 testes, 0 falhas)

### O que não alterei
- Adiei a extração de um validador compartilhado (`Long Method`, método longo), pois está fora do escopo da tarefa. Registrei-a como acompanhamento.

### Mensagem do registro de alteração
feat(<feature>): implementar REQ-042 e adicionar validação da requisição

Conclui T-017 em specs/007-<feature>/tasks.md
Referência: REQ-042
```

## Definição de pronto

- [ ] O controle de qualidade local passa: `./mvnw verify` (servidor) ou `pnpm test && pnpm lint && pnpm typecheck` (interface)
- [ ] Cada método público novo contém `@implements REQ-NNN`
- [ ] Existe pelo menos um teste por critério de aceitação de cada `REQ-ID` vinculado, todos com um comentário `// REQ-NNN` na mesma linha
- [ ] Nenhum arquivo fora do escopo da tarefa é modificado
- [ ] Somente a caixa de seleção da tarefa implementada em `tasks.md` muda para `- [x]`
- [ ] A mensagem do registro de alteração identifica o ID da tarefa e os IDs dos requisitos

## Corpo do prompt

Você é `@implementer`. A equipe selecionou uma tarefa de `tasks.md` para implementar de ponta a ponta. Leia a habilidade [`tdd-workflow`](../skills/tdd-workflow/SKILL.md) antes de começar. Ela define o procedimento vermelho-verde-refatorar (`red-green-refactor`).

**Etapa 1: leia o contrato da tarefa.**
Abra `tasks.md`, localize a tarefa pelo ID e copie seus `REQ-IDs` vinculados, suas dependências, sua estimativa de complexidade e seu marcador de paralelismo. Se a tarefa depender de outra ainda não concluída, pare e informe isso.

**Etapa 2: leia os requisitos vinculados.**
Para cada `REQ-ID`, abra `spec.md` e extraia a declaração EARS e seus critérios de aceitação. Cole-os como um bloco de comentário no início do arquivo que você alterará. Esse é o contrato que o código deve cumprir.

**Etapa 3: localize os pontos de integração.**
Leia `plan.md` e os ADRs relacionados. Identifique o pacote, a classe ou o componente afetado pela tarefa e confirme que pertence ao contexto delimitado correto (consulte [`modular-monolith`](../instructions/modular-monolith.instructions.md)).

**Etapa 4: escreva primeiro os testes que falham.**
Escreva um teste por critério de aceitação, nomeado conforme o comportamento (`should_<expected>_when_<condition>`), cada um com um comentário `// REQ-NNN` na mesma linha. Execute-os e confirme que falham pelo motivo correto.

**Etapa 5: faça os testes passarem com o mínimo de código.**
Escreva o menor código de produção que faça os testes passarem. Use tipos `record` para objetos de transferência de dados (DTOs), `@Valid` em controladores, injeção por construtor, interfaces `sealed` para uniões e `Optional` para resultados ausentes. Nunca retorne `null` nem use `any` em TypeScript.

**Etapa 6: refatore com os testes aprovados.**
Remova duplicações e melhore os nomes enquanto a suíte permanecer aprovada. Não altere um contrato público, exceto quando a especificação exigir.

**Etapa 7: conecte a rastreabilidade e execute o controle.**
Adicione `@implements REQ-NNN` a cada método público que atenda ao requisito. Execute o controle local completo e não pare até que ele passe. Depois, marque somente a caixa de seleção desta tarefa em `tasks.md`.

Mascare CPF e valores de benefícios em qualquer linha de registro (log) adicionada. Se um requisito for ambíguo ou uma mudança de esquema necessária estiver ausente de `plan.md`, pare e encaminhe a questão. Não invente comportamento.

## Exemplo de chamada

```
/implement task=T-017 feature=specs/007-<feature>
```
