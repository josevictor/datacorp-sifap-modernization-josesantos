---
name: "spec"
description: "Elabore requisitos EARS em spec.md a partir de histórias de usuário, cada um com uma linha obrigatória de rastreabilidade ao legado."
argument-hint: "feature=NNN-feature-name stories=<path-or-inline>"
agent: "product-owner"
tools: ["read", "search", "edit"]
---
# /spec

## Objetivo

Transformar histórias de usuário confirmadas em requisitos EARS formais em `specs/<NNN>-<feature>/spec.md`. Cada requisito contém um REQ-ID exclusivo, um critério de aceitação Dado/Quando/Então e uma linha `source_legacy:` válida. Assim, a tarefa de integração contínua (CI) `legacy-traceability` passa no primeiro envio.

## Quando usar

No início da Etapa 2, depois que a dupla ler os programas Natural atribuídos (a BARREIRA OBRIGATÓRIA em `01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`) e a equipe concordar com uma funcionalidade restrita.

## Pré-condições

- `specs/<NNN>-<feature>/` existe (criado pela interface de linha de comando Specify, a Specify CLI)
- `.specify/memory/constitution.md` existe
- `01-archaeology/business-rules-catalog.md` contém as regras confirmadas e os intervalos de linhas das fontes
- A dupla leu os arquivos legados que pretende citar

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature>`: a pasta em `specs/`
- As histórias de usuário ou regras de negócio confirmadas que devem ser formalizadas (um caminho ou texto incorporado)
- Para cada história, a fonte legada: um caminho `01-archaeology/legacy-sifap/natural-programs/*.{NSP,NSN,NSS,NSA,NSL,NSC,NSM,jcl}` ou `01-archaeology/legacy-sifap/adabas-ddms/*.{NSD,ddm,txt}`, ou uma justificativa explícita com `[GREENFIELD]`
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Lerei `.specify/memory/constitution.md` e listarei as restrições relacionadas à funcionalidade
- Lerei cada arquivo legado citado antes de redigir qualquer requisito
- Refinarei histórias brutas com a habilidade [`user-story-refine`](../skills/user-story-refine/SKILL.md) (INVEST e fatias verticais)
- Classificarei cada requisito por padrão EARS com a habilidade [`ears-validate`](../skills/ears-validate/SKILL.md)
- Atribuirei REQ-IDs exclusivos no formato `REQ-<DOMAIN>-NNN`
- Anexarei uma linha `source_legacy:` a cada requisito
- Escreverei critérios de aceitação Dado/Quando/Então e marcarei os itens fora do escopo

## O que não farei

- Escrever um requisito EARS sem uma linha `source_legacy:`. Solicitarei a fonte ou um marcador `[GREENFIELD]` e interromperei o trabalho
- Inventar o conteúdo de um programa Natural ou campo DDM. Lerei o arquivo ou perguntarei à equipe, sem recorrer à memória
- Apontar `source_legacy:` para `legacy-docs/*.md`. A verificação obrigatória aceita somente caminhos em `natural-programs` e `adabas-ddms`, ou `[GREENFIELD]`
- Converter uma hipótese não validada ou pergunta em aberto em requisito
- Examinar toda a especificação em busca de contradições entre requisitos. Essa é a função de `/contradiction-check` com o Especialista em Requisitos (`@requirements-engineer`)

## Formato da saída

Anexe blocos EARS a `specs/<NNN>-<feature>/spec.md`. A verificação obrigatória de CI analisa a chave `REQ-ID:` e a linha `source_legacy:` localizada até 20 linhas depois dela.

```yaml
REQ-PAY-014:
  pattern: unwanted
  text: "SE uma linha de pagamento fizer referência a um beneficiário inativo, ENTÃO o sistema DEVE rejeitar a linha e registrar o motivo da rejeição."
  source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L<start>-L<end>
  acceptance:
    - "Dado um beneficiário inativo, quando o lote processar a linha, então a linha será rejeitada com o motivo INACTIVE_BENEFICIARY."
  priority: P0

REQ-AUTH-001:
  pattern: unwanted
  text: "SE uma pessoa usuária enviar credenciais inválidas três vezes consecutivas, ENTÃO o sistema DEVE bloquear a conta por 15 minutos."
  source_legacy: "[GREENFIELD] A autenticação e o bloqueio não têm equivalente no sistema legado orientado a lotes."
  acceptance:
    - "Dadas três tentativas consecutivas de autenticação sem sucesso, quando ocorrer uma quarta tentativa, então o sistema responderá com 423 Locked (conta bloqueada)."
  priority: P1
```

> [!NOTE]
> A redação acima é ilustrativa. Os tokens `<PROGRAM>` e `<start>`/`<end>` devem ser substituídos pelo arquivo e intervalo de linhas reais que a equipe leu. O modelo nunca os preenche de memória.

## Definição de pronto

- [ ] Cada história está expressa como um requisito EARS com exatamente um padrão
- [ ] Cada requisito tem um REQ-ID exclusivo no formato `REQ-<DOMAIN>-NNN` (ou `REQ-NNN`)
- [ ] Cada requisito tem uma linha `source_legacy:` válida até 20 linhas depois do REQ-ID (um caminho real em `natural-programs`/`adabas-ddms`, ou `[GREENFIELD]` com justificativa)
- [ ] Cada requisito tem pelo menos um critério de aceitação Dado/Quando/Então
- [ ] Nenhum requisito contradiz `.specify/memory/constitution.md`
- [ ] As premissas e os itens fora do escopo estão declarados explicitamente
- [ ] As perguntas em aberto permanecem como perguntas, não como requisitos

## Corpo do prompt

Você atua como Responsável pelo Produto (`@product-owner`). A equipe concordou com uma funcionalidade restrita e apresenta histórias de usuário para formalização.

**Etapa 1: confirme a funcionalidade e leia as restrições.**
Abra `specs/<NNN>-<feature>/spec.md` (se existir) e `.specify/memory/constitution.md`. Liste as regras constitucionais que restringem a funcionalidade.

**Etapa 2: exija uma fonte legada para cada história.**
Para cada história ou regra, exija um caminho em `natural-programs` ou `adabas-ddms` (de preferência com `#L<start>-L<end>`) ou uma justificativa explícita com `[GREENFIELD]`. Se a história não tiver nenhum dos dois, interrompa o trabalho e pergunte. Não a redija.

**Etapa 3: leia os arquivos legados citados.**
Abra cada arquivo `.NSP`, `.NSN`, `.ddm` ou `.txt` citado e confirme o comportamento antes de redigir o requisito. Nunca deduza uma regra pelo nome do arquivo.

**Etapa 4: refine as histórias.**
Aplique a habilidade [`user-story-refine`](../skills/user-story-refine/SKILL.md): INVEST, um resultado por história e fatias verticais.

**Etapa 5: formalize em EARS.**
Use os padrões da habilidade [`ears-validate`](../skills/ears-validate/SKILL.md). Use exatamente um padrão por requisito. Divida qualquer "e" oculto em requisitos separados.

**Etapa 6: atribua REQ-IDs e rastreabilidade.**
Atribua a cada requisito um `REQ-<DOMAIN>-NNN` exclusivo. Coloque a linha `source_legacy:` diretamente abaixo do REQ-ID e adicione critérios de aceitação Dado/Quando/Então.

**Etapa 7: sinalize e adie.**
Registre ambiguidades, contradições com a constituição e itens fora do escopo. Encaminhe uma análise completa de contradições para `/contradiction-check`.

Nenhum requisito é entregue sem uma linha `source_legacy:`. Caso contrário, a tarefa de CI `legacy-traceability` rejeita a solicitação de integração (PR), e `legacy-docs/*.md` não é uma fonte aceita. Nunca invente comportamento legado. Se você não leu o arquivo, informe isso e solicite a fonte.

## Exemplo de chamada

```
/spec feature=001-pagamento-beneficio stories=02-modern-spec/user-stories.md
```
