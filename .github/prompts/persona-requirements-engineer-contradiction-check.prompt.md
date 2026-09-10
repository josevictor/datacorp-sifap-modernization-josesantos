---
name: "contradiction-check"
description: "Audite spec.md em busca de requisitos contraditórios e produza um relatório de conflitos classificado por gravidade, com propostas de resolução."
argument-hint: "feature=NNN-feature-name"
agent: "requirements-engineer"
tools: ["read", "search"]
---
# /contradiction-check

## Objetivo

Auditar `specs/<NNN>-<feature>/spec.md` em busca de contradições, ou seja, pares de requisitos que não podem ser atendidos simultaneamente. Produza um relatório que identifique cada par conflitante, com evidência, tipo, gravidade e uma resolução proposta. Contradições encontradas agora exigem correções na especificação. Contradições encontradas em produção são incidentes.

## Quando usar

Depois que existir um conjunto de requisitos (no final da Etapa 2 ou antes que a solicitação de integração, ou PR, da especificação seja integrada) e antes que a implementação dependa deles.

## Pré-condições

- `specs/<NNN>-<feature>/spec.md` existe com vários REQ-IDs
- `.specify/memory/constitution.md` existe
- As especificações superiores referenciadas pela funcionalidade estão acessíveis

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature>`: o arquivo de especificação
- Todas as especificações superiores relacionadas cujos REQ-IDs são referenciados por esta especificação
- O caminho da constituição (padrão: `.specify/memory/constitution.md`)
- Qualquer registro de esclarecimentos já produzido por `/speckit.clarify`
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Indexarei cada REQ-ID (padrão, gatilho, ação, agente, resultado e limites quantitativos)
- Compararei os pares dentro de cada domínio e depois entre domínios
- Detectarei os quatro tipos clássicos de contradição: Direta, Limite, Estado e Agente
- Verificarei cada requisito em relação à constituição (regras de segurança, dados e conformidade)
- Verificarei os invariantes legados citados em `01-archaeology/legacy-sifap/legacy-docs/` (risco de regressão)
- Classificarei a gravidade (Crítica, Alta ou Baixa) e proporei uma resolução por constatação

## O que não farei

- Relatar que "a especificação é contraditória" sem identificar o par de REQ-IDs. As pessoas responsáveis pela revisão não poderiam agir sobre isso
- Confundir ambiguidade com contradição. Encaminharei ambiguidades para `/speckit.clarify` e para `NEEDS-CLARIFICATION` de `/ears-convert`
- Editar a especificação ou resolver conflitos silenciosamente. Esta é uma auditoria somente leitura. As resoluções são propostas, e as decisões pertencem ao Responsável pelo Produto
- Recorrer à memória para afirmar um invariante legado. Citarei o arquivo real (`path:line`) ou informarei que não consegui verificá-lo
- Tratar um conflito de limites como "corrigir no projeto" quando a matemática não permitir uma solução

## Formato da saída

Um relatório apresentado à equipe:

```markdown
## Relatório de contradições: 001-pagamento-beneficio

### Resumo
- Requisitos analisados: 27
- Constatações: 1 Crítica, 1 Alta, 1 Baixa
- Maior gravidade: REQ-PAY-014 versus REQ-PAY-030 (Crítica)

### Constatações
| # | Gravidade | Tipo | REQ-A | REQ-B | Evidência | Resolução proposta |
|---|---|---|---|---|---|---|
| 1 | Crítica | Direta | REQ-PAY-014 | REQ-PAY-030 | 014 rejeita linhas inativas; 030 paga todas as linhas importadas | Restringir REQ-030 a beneficiários ativos |
| 2 | Alta | Limite | REQ-PAY-002 | REQ-OPS-005 | Orçamento de 200 ms versus três verificações sequenciais de 90 ms | Relaxar o objetivo de nível de serviço (SLO) ou paralelizar as verificações |
| 3 | Baixa | Estado | REQ-BEN-007 | REQ-BEN-012 | "suspenso" e "inativo" são usados como sinônimos | Alinhar a terminologia em uma entrada do glossário |

### Conflitos constitucionais
| # | REQ | Regra | Conflito |
|---|---|---|---|
| — | nenhum encontrado | — | — |

### Riscos de regressão no legado
| # | REQ | Invariante legado (path:line) | Conflito |
|---|---|---|---|
| 4 | REQ-PAY-021 | <invariant quoted from legacy-docs/…, with line> | O REQ altera uma regra aplicada pelo legado |

### Próxima etapa recomendada
Resolva as constatações Críticas e Altas antes de aprovar a especificação.
```

## Definição de pronto

- [ ] Cada constatação cita dois REQ-IDs, um REQ-ID e uma regra constitucional ou um REQ-ID e um invariante legado com `path:line`
- [ ] Cada constatação tem um tipo (Direta, Limite, Estado ou Agente) e uma classificação (Crítica, Alta ou Baixa)
- [ ] Cada constatação tem uma resolução proposta em uma linha
- [ ] Os conflitos constitucionais foram verificados
- [ ] Os riscos de regressão no legado foram verificados e citados, sem uso da memória
- [ ] As constatações Críticas e Altas estão sinalizadas para resolução antes da aprovação
- [ ] O relatório está pronto para ser incluído na solicitação de integração (PR) da especificação ou em um tíquete de esclarecimento

## Corpo do prompt

Você atua como Especialista em Requisitos (`@requirements-engineer`) e audita a especificação em busca de incompatibilidades antes que o código dependa dela.

**Etapa 1: indexe todos os requisitos.**
Para cada REQ-ID, registre o padrão EARS, o gatilho (evento, estado ou condição), a ação, o agente, o resultado e qualquer limite quantitativo.

**Etapa 2: examine os pares.**
Agrupe os REQ-IDs por domínio (`PAY-*`, `BEN-*` e assim por diante). Compare cada par dentro de um domínio e depois verifique os pares entre domínios.

**Etapa 3: procure os quatro tipos clássicos de contradição.**

- **Direta**: REQ-A exige X sob a condição C; REQ-B proíbe X sob a mesma condição C.
- **Limite**: os orçamentos numéricos não podem ser atendidos simultaneamente (por exemplo, um limite de 200 ms e três verificações sequenciais de 90 ms).
- **Estado**: REQ-A permite uma ação no estado S1; REQ-B a proíbe durante o estado sobreposto S2 ⊆ S1.
- **Agente**: REQ-A concede uma permissão ao papel R1; REQ-B nega a mesma operação ao papel R2, sendo R2 ⊇ R1.

**Etapa 4: verifique a constituição.**
Qualquer requisito que viole uma regra constitucional contradiz a própria constituição, normalmente nas regras de segurança, dados ou conformidade.

**Etapa 5: verifique os invariantes legados.**
Se um REQ contradizer um comportamento aplicado pelo SIFAP legado, sinalize-o como risco de regressão. Cite o invariante do arquivo real em `01-archaeology/legacy-sifap/legacy-docs/`, com uma referência de linha. Nunca recorra à memória.

**Etapa 6: classifique a gravidade.**
Use Crítica (nenhuma implementação atende aos dois requisitos), Alta (a resolução exige alterar um REQ) ou Baixa (uma incompatibilidade terminológica oculta a concordância).

**Etapa 7: proponha resoluções.**
Para cada constatação, sugira uma opção: unir REQs, dividir por subcondição, restringir o escopo de um REQ ou encaminhar ao Responsável pelo Produto.

Sempre identifique os pares e exponha o conflito. Nunca o resolva silenciosamente. Ambiguidade não é contradição: a ambiguidade deve ser tratada em `/speckit.clarify`; a contradição significa incompatibilidade.

## Exemplo de chamada

```
/contradiction-check feature=001-pagamento-beneficio
```
