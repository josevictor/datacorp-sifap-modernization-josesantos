---
name: "write-ears-spec"
description: "Orienta a equipe no registro de requisitos EARS confirmados em spec.md, com rastreabilidade obrigatória."
argument-hint: "feature=NNN-feature-name rules=01-archaeology/business-rules-catalog.md"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /write-ears-spec

## Objetivo

Transformar somente regras confirmadas da Etapa 1 em requisitos EARS formais em `specs/<NNN>-<feature>/spec.md`. Questões em aberto permanecem como perguntas; não preencha requisitos, critérios ou arquitetura por suposição.

## Quando usar

No início da Etapa 2, após a Dupla 2 selecionar a funcionalidade restrita e concluir a transição H1, na branch `spec/<NNN>-<feature>` criada de `develop`.

> [!NOTE]
> Não use para explorar o legado, catalogar questões (`/catalog-mysteries`) ou projetar módulos (`/design-modular-monolith`). Registre somente requisitos com evidências confirmadas.

## Pré-condições

- `01-archaeology/business-rules-catalog.md` contém as evidências
- A equipe identificou `specs/<NNN>-<feature>/`
- A equipe leu cada origem legada citada

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature-name>`
- `rules=01-archaeology/business-rules-catalog.md`
- O subconjunto de regras **Confirmed** pertencente à funcionalidade
- Justificativa `[GREENFIELD]` confirmada para capacidades sem equivalente legado

## O que farei

- Confirmarei o escopo e registrarei adiamentos em `02-modern-spec/scope-decisions.md`
- Validarei a origem `.NSP`, `.NSN`, `.NSC`, `.NSA`, `.NSL`, `.jcl` ou `.ddm`
- Atribuirei REQ-ID exclusivo e `source_legacy:` com caminho e linhas; usarei `[GREENFIELD]` somente com justificativa fornecida
- Registrarei Dado/Quando/Então somente quando apoiado por evidência ou decisão de escopo
- Preservarei questões não validadas de `mysteries-found.md`, com todos os campos
- Manterei uma matriz de rastreabilidade

## O que não farei

- Criar requisito sem `source_legacy:` ou `[GREENFIELD]` justificado
- Promover, responder ou alterar o status de hipóteses e questões
- Exigir quantidade fixa de requisitos, diagramas C4, ADRs ou endpoints
- Colocar artefatos Spec-Kit em `02-modern-spec/`
- Inventar fatos de negócio do SIFAP

## Formato da saída

```markdown
### REQ-007 — Título imperativo curto do comportamento

SE <condição indesejada da regra confirmada>, ENTÃO o sistema DEVE <comportamento exigido>.

- source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAMA>.NSN:L<início>-L<fim>
- Aceitação (Dado/Quando/Então):
  - Dado <pré-condição apoiada pela evidência>
  - Quando <gatilho>
  - Então <resultado observável e testável>
```

Mantenha no mesmo `spec.md`:

| REQ-ID | Padrão EARS | source_legacy | Regra de origem | Arquivo de origem |
|---|---|---|---|---|
| REQ-007 | Indesejado | `<PROGRAMA>.NSN:L<início>-L<fim>` | Regra 4 | `business-rules-catalog.md` |

## Definição de pronto

- [ ] `spec.md` contém somente requisitos da funcionalidade
- [ ] Cada requisito tem formulação EARS, critério verificável e `source_legacy:` válido ou `[GREENFIELD]` justificado
- [ ] Questões em aberto permanecem fora dos requisitos e sem mudança de status
- [ ] A matriz relaciona cada REQ-ID às evidências revisadas

## Corpo do prompt

Você é `@architect`. Promova regras confirmadas da Etapa 1 a requisitos EARS formais sem inventar evidências.

**Etapa 1 — Confirmar o escopo.**
Liste somente linhas **Confirmed** atribuídas pela equipe à funcionalidade. Registre adiamentos em `scope-decisions.md`. Não inclua **Inferred** ou **Mystery**.

**Etapa 2 — Validar cada origem.**
Abra cada membro citado e confirme as linhas. Se a referência falhar, devolva a regra como questão em aberto. Nunca cite `.NSD`; não há esse arquivo no corpus.

**Etapa 3 — Escrever o requisito EARS.**
Atribua `REQ-NNN` e preserve os padrões necessários:

- Ubíquo: `O sistema DEVE...`
- Orientado a evento: `QUANDO [evento], o sistema DEVE...`
- Orientado a estado: `ENQUANTO [estado], o sistema DEVE...`
- Opcional: `ONDE [funcionalidade], o sistema DEVE...`
- Indesejado: `SE [condição indesejada], ENTÃO o sistema DEVE...`

Anexe `source_legacy:`. Para capacidade nova, use `[GREENFIELD]` seguido somente da justificativa fornecida pela equipe.

**Etapa 4 — Registrar critérios.**
Adicione Dado/Quando/Então somente para comportamento apoiado por evidências.

**Etapa 5 — Preservar questões em aberto.**
Copie itens não validados para “Questões em aberto”, preservando evidência `path:line`, impacto, hipótese não confirmada, pessoa responsável e status. Não responda nem altere.

**Etapa 6 — Construir a matriz.**
Mantenha a tabela `REQ-ID | EARS Pattern | source_legacy | Source Rule | Source File`.

**Etapa 7 — Escrever.**
Grave em `specs/<NNN>-<feature>/spec.md`. Não infle o escopo quando faltar tempo.

## Exemplo de chamada

```text
/write-ears-spec feature=001-benefit-calculation rules=01-archaeology/business-rules-catalog.md
```

Espere um `spec.md` com requisitos EARS apoiados por evidências, `source_legacy:`, matriz de rastreabilidade e questões em aberto preservadas.
