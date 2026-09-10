---
name: "user-story-refine"
description: "Use ao refinar itens da lista priorizada, dividir épicos ou validar critérios INVEST. Os gatilhos incluem \"refinar história\", \"dividir épico\", \"critérios de aceitação\", \"história de usuário\" e \"INVEST\"."
---
# Refinamento de histórias de usuário

## Quando invocar

- "Esta história é grande demais. Ajude-me a dividi-la."
- "Transforme esta descrição de funcionalidade em histórias de usuário com critérios de aceitação."
- "Verifique se estas histórias atendem ao INVEST."

## Entradas obrigatórias

- Descrição da funcionalidade ou do épico
- Persona ou tipo de usuário
- Objetivo de negócio atendido pela funcionalidade
- Restrições conhecidas (regulatórias, técnicas ou de UX)

## Etapas de refinamento

1. **Confirme o resultado**. Cada história deve responder: qual persona, qual resultado e por que ele importa.
2. **Aplique INVEST** (independente, negociável, valiosa, estimável, pequena e testável) a cada rascunho.
3. **Divida verticalmente**, nunca horizontalmente. Prefira divisões por etapa do fluxo, variação de dados, operação CRUD, fluxo de sucesso versus caso-limite, regra de negócio ou critério de aceitação.
4. **Escreva os critérios de aceitação no formato Dado/Quando/Então**. Inclua um fluxo de sucesso, um caso-limite e um fluxo de erro.
5. **Rastreie até um REQ-ID**. Cada história deve se vincular a pelo menos um requisito.

## Padrões de divisão

Use estes padrões quando uma história for grande demais para ser concluída em uma iteração:

| Padrão | Divida uma história por... | Exemplo |
|---|---|---|
| Etapas do fluxo | Cada etapa de um fluxo com várias etapas | Enviar versus revisar versus aprovar |
| Regra de negócio | Uma regra por história | Alíquota padrão versus alíquota de isenção |
| Variação de dados | Cada tipo ou formato de entrada | Endereço nacional versus internacional |
| Operação CRUD | Criar, ler, atualizar e excluir separadamente | Adicionar registro antes de editar registro |
| Sucesso versus limite | Fluxo de sucesso primeiro, depois casos-limite | Entrada válida antes da entrada rejeitada |
| Pesquisa exploratória | Separe a incerteza como uma pesquisa com tempo limitado | Primeiro, crie um protótipo da integração |

## Antipadrões

- Histórias escritas como tarefas ("Adicionar um botão").
- Critérios de aceitação que descrevem a interface em vez do comportamento.
- Divisões horizontais ("história da camada de servidor" + "história da interface" para a mesma funcionalidade).
- Ausência de vínculo com REQ-ID.

## Modelo de saída

```markdown
### US-NNN: <título curto>
**Como** <persona>
**Quero** <capacidade>
**Para** <resultado de negócio>

**Critérios de aceitação**
- Dado <contexto>, Quando <ação>, Então <resultado>
- Dado <caso-limite>, Quando <ação>, Então <resultado>

**Rastreia até**: REQ-001, REQ-042
**Esforço**: S / M / L
**Dependências**: US-NNN (se houver)
```

## Critérios de qualidade

- [ ] A história atende a todos os critérios INVEST.
- [ ] Os critérios de aceitação estão escritos em Dado/Quando/Então e cobrem o fluxo de sucesso, um caso-limite e o fluxo de erro.
- [ ] A história está dividida verticalmente, não por camada de arquitetura.
- [ ] A história rastreia até pelo menos um REQ-ID, e cada REQ-ID vinculado contém uma linha `source_legacy:` (imposta pela tarefa de CI `legacy-traceability`).
