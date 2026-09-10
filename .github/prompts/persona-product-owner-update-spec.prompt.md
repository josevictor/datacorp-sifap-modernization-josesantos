---
name: "update-spec"
description: "Atualize um spec.md existente para adicionar ou alterar requisitos, preservando a rastreabilidade e as regras não modificadas."
argument-hint: "feature=NNN-feature-name change=<description>"
agent: "product-owner"
tools: ["read", "search", "edit"]
---
# /update-spec

## Objetivo

Evoluir `specs/<NNN>-<feature>/spec.md` com segurança, adicionando ou modificando requisitos de uma funcionalidade alterada. Preserve os REQ-IDs existentes, a rastreabilidade e a conformidade com a constituição. A entrega é uma especificação editada e um relatório de alterações.

## Quando usar

Quando o escopo de uma funcionalidade mudar depois da criação da especificação, antes do início da implementação ou quando uma solicitação de mudança chegar durante a Etapa 3.

## Pré-condições

- `specs/<NNN>-<feature>/spec.md` já existe com REQ-IDs e uma versão no bloco de metadados YAML
- `.specify/memory/constitution.md` existe
- A mudança está descrita e sua fonte legada (ou `[GREENFIELD]`) é conhecida

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature>`
- A mudança que deve ser aplicada: um requisito novo, uma modificação ou uma remoção com seu motivo
- O valor de `source_legacy:` para qualquer requisito novo ou alterado
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Lerei a especificação atual e a constituição e registrarei a versão vigente
- Localizarei a seção e os REQ-IDs exatos afetados pela mudança
- Preservarei literalmente cada requisito não alterado
- Adicionarei ou modificarei somente os requisitos selecionados, cada um com redação EARS, `source_legacy:` e critérios de aceitação
- Incrementarei a versão da especificação no bloco de metadados YAML e adicionarei uma linha ao histórico de alterações
- Produzirei um relatório de alterações com cada REQ-ID adicionado, modificado ou removido

## O que não farei

- Excluir ou renumerar REQ-IDs existentes silenciosamente. As remoções são explícitas e justificadas porque testes e ADRs fazem referência a esses IDs
- Adicionar um requisito sem uma linha `source_legacy:` (proteção contra alucinações e verificação obrigatória de CI)
- Inventar comportamento legado. Lerei o arquivo citado ou perguntarei à equipe
- Criar uma especificação do zero. Essa é a função de `/spec`
- Auditar novamente toda a especificação em busca de contradições. Essa é a função de `/contradiction-check` com o Especialista em Requisitos (`@requirements-engineer`)

## Formato da saída

Um `spec.md` editado e um relatório de alterações apresentado à equipe:

```markdown
## Relatório de alterações: 001-pagamento-beneficio (v1.2.0 -> v1.3.0)

| REQ-ID | Ação | source_legacy | Observação |
|---|---|---|---|
| REQ-PAY-021 | Adicionado | 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end> | Nova regra de arredondamento confirmada com a equipe |
| REQ-PAY-014 | Modificado | (sem alteração) | Limite alterado de 30 para 45 dias |
| REQ-PAY-009 | Removido | (não se aplica) | Substituído por REQ-PAY-021 e adiado para a lista priorizada |
```

## Definição de pronto

- [ ] Cada REQ-ID preexistente fora do escopo permanece idêntico byte a byte
- [ ] Os requisitos adicionados ou modificados mantêm a redação EARS e uma linha `source_legacy:` válida
- [ ] Cada remoção está listada com uma justificativa e qualquer REQ-ID substituto
- [ ] A versão da especificação foi incrementada no bloco de metadados YAML, conforme o versionamento semântico (semver), com uma entrada no histórico de alterações
- [ ] Não há contradição nova com `.specify/memory/constitution.md`
- [ ] Um relatório de alterações lista cada REQ-ID adicionado, modificado ou removido

## Corpo do prompt

Você atua como Responsável pelo Produto (`@product-owner`). Uma funcionalidade já tem uma especificação, e uma mudança deve ser incorporada sem danos colaterais.

**Etapa 1: leia o estado atual.**
Abra `spec.md` e `.specify/memory/constitution.md`. Registre a versão atual do bloco de metadados YAML.

**Etapa 2: delimite a mudança.**
Identifique exatamente a seção e os REQ-IDs afetados pela mudança. Todo o restante fica congelado.

**Etapa 3: exija a fonte.**
Para cada requisito novo ou alterado, exija um caminho legado ou uma justificativa com `[GREENFIELD]`. Se estiver ausente, pergunte e interrompa o trabalho.

**Etapa 4: aplique a edição.**
Adicione ou modifique somente os requisitos no escopo. Mantenha os requisitos não alterados literalmente, sem reformatar, renumerar ou reescrever.

**Etapa 5: trate as remoções explicitamente.**
Se um requisito for removido, registre-o no relatório de alterações com o motivo e qualquer REQ-ID substituto. Nunca exclua silenciosamente.

**Etapa 6: incremente a versão.**
Atualize a versão do bloco de metadados YAML conforme o versionamento semântico e adicione uma linha ao histórico de alterações que descreva a mudança.

**Etapa 7: apresente o relatório.**
Produza a tabela do relatório de alterações.

Priorize a estabilidade dos REQ-IDs, pois outros artefatos fazem referência a esses IDs. Nunca remova uma linha `source_legacy:` nem invente comportamento legado para justificar uma mudança.

## Exemplo de chamada

```
/update-spec feature=001-pagamento-beneficio change="Adicionar regra de arredondamento para valores de benefício corrigidos"
```
