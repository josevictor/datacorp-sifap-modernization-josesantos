---
name: "ears-validate"
description: "Use ao validar requisitos conforme os padrões da notação EARS. Os gatilhos incluem \"EARS\", \"revisão de requisitos\", \"qualidade de requisitos\", \"declaração com shall (deve)\" e \"REQ-ID\"."
---
# Validação EARS

## Quando usar

- "Revise estes requisitos quanto à conformidade com EARS."
- "Este requisito é testável?"
- "Classifique este requisito por padrão EARS."

## Padrões EARS

| Padrão | Modelo |
|---|---|
| Ubíquo | `O <sistema> DEVE <resposta>.` |
| Orientado a evento | `QUANDO <gatilho>, o <sistema> DEVE <resposta>.` |
| Orientado a estado | `ENQUANTO <estado>, o <sistema> DEVE <resposta>.` |
| Opcional | `ONDE <funcionalidade estiver incluída>, o <sistema> DEVE <resposta>.` |
| Indesejado | `SE <condição indesejada>, ENTÃO o <sistema> DEVE <mitigação>.` |
| Complexo | `ENQUANTO <estado>, QUANDO <gatilho>, o <sistema> DEVE <resposta>.` |

## Lista de verificação da validação

- [ ] Exatamente um padrão por requisito.
- [ ] Sujeito inequívoco ("o sistema", não "ele").
- [ ] Resposta observável e testável.
- [ ] Nenhum "e" oculto que combine dois requisitos em um só.
- [ ] Nenhum detalhe de implementação ("usar Redis"), somente comportamento.
- [ ] Inclui um REQ-ID no formato `REQ-NNN`.
- [ ] Inclui pelo menos um critério de aceitação.
- [ ] **Inclui um `source_legacy:` não vazio que aponte para `01-archaeology/legacy-sifap/natural-programs/*.NSN`, `01-archaeology/legacy-sifap/adabas-ddms/*.ddm` ou use o token `[GREENFIELD]` acompanhado da justificativa de uma nova implementação.**

## Defeitos comuns

| Defeito | Exemplo | Correção |
|---|---|---|
| Ambíguo | "O sistema deve ser rápido." | "QUANDO uma pessoa enviar um formulário, o sistema DEVE responder em até 500 ms." |
| Composto | "Entrar e enviar um e-mail." | Divida em dois requisitos. |
| Não testável | "O sistema deve ser fácil de usar." | Substitua por uma métrica mensurável de experiência do usuário (UX). |
| Passivo | "O login deve ser aceito." | "O sistema DEVE aceitar autenticação por nome de usuário e senha." |

## Modelo de saída

```markdown
### REQ-NNN (<padrão>)
<declaração EARS>

source_legacy: 01-archaeology/legacy-sifap/natural-programs/<FILE>.NSN#L<start>-L<end>
_(ou `[GREENFIELD] <justificativa>` quando não houver equivalente legado)_

**Critérios de aceitação**
- <critério 1>
- <critério 2>

**Rastreado de**: US-NNN, ADR-NNN
**Prioridade**: P0 / P1 / P2
**Status**: proposed / approved / implemented / verified
```

## Critérios de qualidade

- [ ] Cada requisito tem um REQ-ID exclusivo no formato `REQ-NNN`.
- [ ] Cada requisito está classificado em exatamente um padrão EARS.
- [ ] Cada requisito tem pelo menos um critério de aceitação testável.
- [ ] Cada requisito tem uma linha `source_legacy:` que aponta para um arquivo legado real ou usa `[GREENFIELD] <justificativa>`.
- [ ] A tarefa automatizada `legacy-traceability` em `.github/workflows/spec-quality.yml` passa na solicitação de alteração (PR).
