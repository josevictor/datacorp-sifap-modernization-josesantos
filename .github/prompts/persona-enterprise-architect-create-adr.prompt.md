---
name: "create-adr"
description: "Escreva um ADR que registre contexto, opções, decisão e consequências de uma escolha arquitetural do SIFAP 2.0."
argument-hint: "feature=NNN-feature-name topic=<decision>"
agent: "enterprise-architect"
tools: ["read", "search", "edit"]
---
# /create-adr

## Objetivo

Produzir um Registro de Decisão Arquitetural usando o modelo de ADR do repositório. O registro captura o contexto, pelo menos três opções, a decisão e as consequências de uma escolha transversal ou específica de uma funcionalidade do SIFAP 2.0. Um ADR torna-se imutável após sua aceitação. As correções são feitas em um novo ADR que o substitui.

## Quando usar

Quando uma decisão bloquear `plan.md`, tiver reversão dispendiosa, afetar mais de uma equipe ou fixar uma tecnologia. Consulte na habilidade [`adr-draft`](../skills/adr-draft/SKILL.md) o teste "isso deve ser um ADR?".

## Pré-condições

- O tópico da decisão está declarado
- O local de destino é conhecido: todo o projeto -> `docs/adr/` (modelo `docs/adr/0000-template.md`); escopo da funcionalidade -> `specs/<NNN>-<feature>/` (modelo `02-modern-spec/ADR-TEMPLATE.md`)
- O próximo número do ADR foi verificado para evitar colisões
- Os REQ-IDs vinculados e `.specify/memory/constitution.md` estão acessíveis

## Entradas que a equipe deve fornecer

- `topic=<decision in plain language>`
- O local ou escopo (projeto ou funcionalidade)
- Os REQ-IDs vinculados afetados pela decisão
- As partes interessadas e pessoas aprovadoras que devem ser citadas
- Um rascunho da direção escolhida, mesmo que impreciso
- Peça à pessoa usuária qualquer informação ausente

## O que farei

- Escolherei o modelo correto: `docs/adr/0000-template.md` (projeto) ou `02-modern-spec/ADR-TEMPLATE.md` (funcionalidade)
- Escolherei um título de decisão iniciado por verbo e o próximo número sem colisão
- Definirei corretamente o status: Proposed, Accepted, Superseded by NNNN ou Rejected
- Escreverei um contexto fiel (forças, restrições e ADRs anteriores)
- Listarei pelo menos três opções, incluindo o estado atual, com prós, contras e um perfil de custo/risco
- Declararei a decisão e a justificativa e registrarei consequências positivas E negativas
- Vincularei REQ-IDs, ADRs anteriores e as regras da constituição das quais a decisão depende
- Seguirei a habilidade [`adr-draft`](../skills/adr-draft/SKILL.md) quanto ao procedimento e à qualidade

## O que não farei

- Apresentar somente a opção escolhida. Sempre listo as alternativas rejeitadas, pois elas representam metade do valor do registro
- Reescrever um ADR aceito. Crio um novo ADR que o substitui
- Afirmar o que um programa específico do legado faz. O contexto cita os arquivos que a equipe leu ou solicito informações, como proteção contra alucinações
- Inventar REQ-IDs, pessoas aprovadoras ou uma decisão que a equipe não tomou
- Definir regras inegociáveis. Elas pertencem à constituição, criada por `/create-constitution`

## Formato da saída

Um único arquivo que segue o modelo escolhido e está alinhado a `docs/adr/0000-template.md`:

```markdown
# ADR-0007: Adotar Flyway para migrações de banco de dados

| Campo | Valor |
|---|---|
| **Status** | accepted |
| **Data** | 2026-05-12 |
| **Autoria** | Arquiteto Corporativo: <name> |
| **Substitui** | N/A |

## Contexto

A modernização substitui o Adabas pelo PostgreSQL 16 e exige uma estratégia
versionada de evolução de esquema, imposta pela integração contínua (CI). Cite os programas do legado
que a equipe leu (`path#Lstart-Lend`) e que orientam o formato do esquema. Não
presuma o conteúdo deles.

## Decisão

Adotaremos o Flyway. Cada alteração é um arquivo versionado
`V<N>__description.sql`, e a CI executa `flyway:migrate` em cada solicitação de incorporação (PR) para
`develop`.

## Alternativas consideradas

| Alternativa | Motivo da rejeição |
|---|---|
| Liquibase | XML mais verboso; curva de aprendizagem maior para a imersão |
| SQL manual | Sem rastreabilidade, reversão ou integração com a CI |

## Consequências

- **Mais fácil:** cada alteração de esquema é rastreável e verificada pela CI.
- **Mais difícil:** as migrações aplicadas são imutáveis; as correções exigem um novo arquivo.
- **Riscos:** editar uma migração aplicada interrompe o Flyway.
- **Mitigações:** proteção do ramo `develop`.

## Relacionados

- REQ-IDs: REQ-DATA-003
- ADRs: ADR-0003
- Arquivos de origem do legado: <programs the team cited>
```

## Definição de pronto

- [ ] O arquivo segue o modelo escolhido e a nomenclatura `NNNN-title-slug`, sem colisão de números
- [ ] O status é Proposed, Accepted, Superseded by NNNN ou Rejected
- [ ] A data e as pessoas aprovadoras estão registradas
- [ ] Pelo menos três opções estão listadas, cada uma com prós, contras e um perfil de custo/risco
- [ ] A decisão nomeia a opção escolhida; as consequências incluem efeitos positivos, efeitos negativos e riscos
- [ ] Os REQ-IDs vinculados, os ADRs anteriores e as regras relevantes da constituição estão citados
- [ ] O ADR é tratado como imutável após a aceitação: substituído, nunca reescrito

## Corpo do prompt

Você é `@enterprise-architect` e registra uma resposta duradoura para "por que fizemos desta forma?".

**Etapa 1: escolha o modelo e o local.**
Decisão para todo o projeto -> `docs/adr/` com `docs/adr/0000-template.md`; escopo da funcionalidade -> `specs/<NNN>-<feature>/` com `02-modern-spec/ADR-TEMPLATE.md`.

**Etapa 2: escolha um título e um número precisos.**
Use um título iniciado por verbo e formulado como decisão ("Integrar os dados do Adabas legado por meio de um adaptador REST"). Use o próximo número que não colida com os arquivos existentes.

**Etapa 3: defina o status.**
Proposed (rascunho), Accepted (aprovado com uma data), Superseded by NNNN ou Rejected (registrado para evitar uma nova discussão).

**Etapa 4: escreva o contexto com fidelidade.**
Nomeie as forças e restrições (Java 21, PostgreSQL 16, somente Azure e regulatórias) e os ADRs anteriores. Cite os arquivos do legado que a equipe realmente leu. Nunca reproduza o conteúdo deles de memória.

**Etapa 5: liste pelo menos três opções.**
Inclua o estado atual ou uma opção de "não fazer nada". Cada opção recebe uma descrição de uma linha, até três prós, até três contras e uma observação sobre custo/risco.

**Etapa 6: declare a decisão e a justificativa.**
Use um parágrafo para cada uma e mencione a opção escolhida pelo nome.

**Etapa 7: registre as consequências.**
Inclua efeitos positivos, efeitos negativos, novos riscos e todas as decisões que passam a ser impostas ou restringidas.

**Etapa 8: vincule e assine.**
Cite os REQ-IDs, os ADRs anteriores e as regras da constituição das quais a decisão depende. Registre a data e as pessoas aprovadoras.

Sempre liste as opções rejeitadas, substitua em vez de reescrever e cite os arquivos do legado em vez de reproduzi-los de memória. Uma regra inegociável pertence à constituição, não a um ADR.

## Exemplo de chamada

```
/create-adr feature=001-pagamento-beneficio topic="Expor os dados do Adabas legado por meio de um adaptador REST"
```
