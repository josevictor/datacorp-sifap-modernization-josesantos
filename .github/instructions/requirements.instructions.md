---
description: "Use ao escrever ou revisar requisitos, especificações EARS, critérios de aceitação, rastreabilidade e requisitos fundamentados na documentação."
applyTo: "docs/**/*.md,specs/**/*.md,02-modern-spec/**/*.md"
---

# Convenções de requisitos — EARS e rastreabilidade legada

Este arquivo é ativado quando você escreve ou revisa Markdown em `docs/`, `specs/` ou `02-modern-spec/`. Ele ensina a redigir requisitos em notação EARS, atribuir REQ-IDs e anexar a linha obrigatória `source_legacy:` imposta pela CI. Ele ensina a *forma* de um bom requisito, mas não decide *o que* exigir; isso vem da leitura do corpus legado pela própria equipe.

> [!IMPORTANT]
> Antes de escrever requisitos EARS, a dupla DEVE ter lido os programas Natural atribuídos (portão rígido; consulte [`LEGACY-EXPLORATION-CHECKLIST.md`](../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md) e [`natural-adabas.instructions.md`](natural-adabas.instructions.md)).

## Padrões EARS

Todo requisito formal usa um modelo EARS e a palavra-chave `DEVE` para comportamento obrigatório (`DEVERIA` para recomendações).

| Padrão | Modelo |
|---|---|
| Ubíquo | `O <sistema> DEVE <resposta>.` |
| Orientado a evento | `QUANDO <gatilho>, o <sistema> DEVE <resposta>.` |
| Orientado a estado | `ENQUANTO <estado>, o <sistema> DEVE <resposta>.` |
| Comportamento indesejado | `SE <condição>, ENTÃO o <sistema> DEVE <resposta>.` |
| Funcionalidade opcional | `ONDE <funcionalidade estiver presente>, o <sistema> DEVE <resposta>.` |

A skill [`ears-validate`](../skills/ears-validate/SKILL.md) detém o checklist de qualidade dessas declarações.

## Anatomia de um requisito

```markdown
### REQ-021 — Rejeitar cadastro duplicado de recurso

QUANDO um recurso for enviado com um identificador que já existe,
o sistema DEVE rejeitar a solicitação e retornar HTTP 409.

- source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L40-L88
- acceptance: Dado um recurso existente, Quando o mesmo identificador for enviado,
  Então a resposta será 409 e nenhum registro novo será criado.
```

## Formato de REQ-ID

Os IDs são exclusivos e assumem o formato `REQ-NNN` (`REQ-021`) ou `REQ-AREA-NNN` (`REQ-PAY-014`, `REQ-AUD-CORE-002`). O portão de rastreabilidade reconhece uma declaração somente quando o ID é um título (`### REQ-021 — …`) ou inicia um item em negrito/lista (`- **REQ-021**:`, `REQ-021 - …`, `REQ-021:`). Menções isoladas em outros trechos de prosa contam como referências, não declarações.

## Linha `source_legacy` obrigatória

O job `legacy-traceability` em [`spec-quality.yml`](../workflows/spec-quality.yml) **reprova o build** quando qualquer REQ-ID declarado em `specs/` não possui uma linha `source_legacy:` válida até 20 linhas após sua declaração. Um valor é válido quando for:

- Um path em `01-archaeology/legacy-sifap/natural-programs/` com extensão `.NSP`, `.NSN`, `.NSS`, `.NSA`, `.NSL`, `.NSC`, `.NSM` ou `.jcl`.
- Um path em `01-archaeology/legacy-sifap/adabas-ddms/` com extensão `.NSD`, `.ddm` ou `.txt`.
- `[GREENFIELD] <justificativa de uma linha>` (a justificativa não pode estar vazia).

Uma âncora de linha opcional `#L<start>` ou `#L<start>-L<end>` pode seguir o path, e o arquivo **deve realmente existir no disco**, pois o portão o lê. As aspas são opcionais, mas devem estar balanceadas.

```markdown
- source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/<DDM>.ddm#L12-L30
- source_legacy: "[GREENFIELD] não existe trilha de auditoria legada; necessária para conformidade"
```

> [!WARNING]
> Um `source_legacy:` que aponta para arquivo inexistente, diretório incorreto ou extensão não listada reprova no portão da mesma forma que uma linha ausente.

## Critérios de aceitação

Escreva critérios de aceitação no formato Dado/Quando/Então, um por comportamento, cada um testável e vinculado ao seu REQ-ID. Numere-os sequencialmente dentro da funcionalidade.

```markdown
- AC-021.1: Dado um identificador exclusivo, Quando enviado, Então a resposta será 201.
- AC-021.2: Dado um identificador duplicado, Quando enviado, Então a resposta será 409.
```

## Rastreabilidade de testes

O job não bloqueante `spec-traceability` informa REQ-IDs ainda não referenciados por testes. Cite o REQ-ID em um comentário de teste para manter implementação e especificação vinculadas (consulte [`tests.instructions.md`](tests.instructions.md)).

```java
// REQ-021: identificador duplicado retorna 409
@Test
void should_return_409_when_identifier_already_exists() { /* ... */ }
```

## Convenções

| Regra | Justificativa |
|---|---|
| Um modelo EARS por requisito | Redação inequívoca e testável |
| `DEVE` = obrigatório, `DEVERIA` = recomendado | Linguagem de obrigação consistente |
| IDs `REQ-NNN` / `REQ-AREA-NNN` exclusivos | Âncoras estáveis para testes e rastreabilidade |
| `source_legacy:` até 20 linhas após o ID | Passa no portão bloqueante de legado |
| Critérios de aceitação Dado/Quando/Então | Conversão direta em testes |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Cite um arquivo legado real (ou `[GREENFIELD]`) | Invente um path ou omita `source_legacy:` |
| Referencie a fonte por um intervalo de linhas `#L` | Afirme de memória o que o programa legado faz |
| Mantenha IDs exclusivos e declarados como títulos/itens de lista | Reutilize um ID ou o esconda no meio da frase |
| Escreva critérios de aceitação como Dado/Quando/Então | Deixe um requisito sem verificação testável |

## Lista de verificação antes de abrir uma PR

- [ ] Todo requisito usa um modelo EARS com `DEVE`/`DEVERIA`
- [ ] Todo REQ-ID é exclusivo e declarado como título ou item de lista/negrito
- [ ] Todo REQ-ID possui uma linha `source_legacy:` até 20 linhas depois, apontando para um arquivo real ou `[GREENFIELD]`
- [ ] Os paths legados usam os diretórios e extensões permitidos, com intervalos `#L` opcionais
- [ ] Os critérios de aceitação estão em Dado/Quando/Então e correspondem ao REQ-ID
- [ ] A dupla leu os programas legados citados antes de escrever os requisitos
