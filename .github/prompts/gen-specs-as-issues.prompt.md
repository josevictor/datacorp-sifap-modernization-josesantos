---
name: "gen-specs-as-issues"
description: "Identifique lacunas entre o comportamento legado do SIFAP e a especificação moderna, priorize-as e abra issues no GitHub fundamentadas em EARS e com rastreabilidade ao legado."
argument-hint: "area=<focus-area> repo=<owner/name>"
agent: "requirements-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /gen-specs-as-issues

## Objetivo

Encontrar comportamentos ausentes ou insuficientemente especificados na modernização do SIFAP 2.0, priorizá-los e transformar os principais itens em issues detalhadas no GitHub. Cada issue é uma especificação EARS com um REQ-ID exclusivo e uma linha `source_legacy:` obrigatória. Assim, todo requisito permanece rastreável do código Natural/Adabas legado ao sistema moderno.

> [!IMPORTANT]
> O job de CI `legacy-traceability` rejeita requisitos sem uma linha `source_legacy:`. Toda issue aberta por este comando deve citar um artefato legado ou apresentar justificativa como `[GREENFIELD]`.

## Quando usar

Durante a Etapa 2 (especificação) ou a Etapa 4 (evolução), quando a equipe precisar converter lacunas observadas em uma lista priorizada e rastreável de especificações.

## Pré-condições

- A dupla leu os programas legados pertinentes, conforme o HARD GATE em [`LEGACY-EXPLORATION-CHECKLIST.md`](../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md)
- A especificação moderna em `02-modern-spec/` e qualquer conteúdo em `specs/` estão disponíveis para comparação
- A equipe está autenticada no repositório GitHub de destino

## Entradas que a equipe deve fornecer

- `area`: a área de foco ou o contexto delimitado a analisar, por exemplo, inspeção de pagamentos
- `repo`: o `owner/name` do repositório GitHub das issues
- Os programas legados pertinentes à área em `01-archaeology/legacy-sifap/`
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Compararei o comportamento legado da área de foco com a especificação moderna e listarei as lacunas
- Pontuarei cada lacuna por impacto e risco e selecionarei os itens prioritários
- Escreverei cada issue como requisito EARS conforme [`requirements.instructions.md`](../instructions/requirements.instructions.md)
- Atribuirei um REQ-ID exclusivo e uma linha `source_legacy:` e abrirei as issues via CLI `gh`

## O que não farei

- Escrever um requisito sem uma linha `source_legacy:` ou sem uma justificativa explícita `[GREENFIELD]`
- Inventar comportamento ausente tanto no sistema legado quanto na especificação moderna
- Abrir issues antes de a equipe confirmar a lista priorizada
- Atribuir uma branch `spec/` a trabalho de implementação; estas são issues de especificação da Etapa 2 em `spec/<NNN>-<feature>`

## Formato da saída

```markdown
### Análise de lacunas — <area>
Lacunas encontradas: 6 · Selecionadas para registro: 3

### Issues a criar
- [SPEC][REQ-014] Quando um pagamento exceder o limite diário, o sistema deve sinalizá-lo para revisão
  source_legacy: 01-archaeology/legacy-sifap/natural-programs/SIFAP-P.NSP
  branch: spec/014-daily-limit-review
```

## Definição de pronto

- [ ] Cada lacuna selecionada foi escrita em notação EARS com um REQ-ID exclusivo
- [ ] Cada issue contém uma linha `source_legacy:` ou uma justificativa `[GREENFIELD]`
- [ ] Cada issue indica uma branch `spec/<NNN>-<feature>`
- [ ] As issues foram criadas via `gh` somente após a confirmação da equipe

## Corpo do prompt

Você produz uma lista de especificações priorizada e rastreável. As regras de notação EARS e REQ-ID estão em [`requirements.instructions.md`](../instructions/requirements.instructions.md). Use a habilidade [`ears-validate`](../skills/ears-validate/SKILL.md) para verificar cada declaração antes do registro.

**Etapa 1 — Estabelecer a referência.**
Leia os programas legados de `area` em `01-archaeology/legacy-sifap/` e a especificação moderna em `02-modern-spec/`. Confirme que a etapa obrigatória de leitura no [checklist](../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md) foi cumprida.

**Etapa 2 — Encontrar e pontuar lacunas.**
Liste comportamentos presentes no sistema legado, mas ausentes ou vagos na especificação moderna. Pontue-os por impacto e risco e selecione os principais.

**Etapa 3 — Escrever requisitos EARS.**
Para cada lacuna selecionada, escreva uma declaração EARS, atribua o próximo REQ-ID e adicione a linha `source_legacy:` que aponta para o artefato legado. Valide com [`ears-validate`](../skills/ears-validate/SKILL.md).

**Etapa 4 — Confirmar e registrar.**
Apresente a lista com as branches `spec/<NNN>-<feature>` propostas. Após a aprovação, abra as issues com `gh`.

## Exemplo de chamada

```
/gen-specs-as-issues area="payment inspection" repo=my-org/sifap-2
```
