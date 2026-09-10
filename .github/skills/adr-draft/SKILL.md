---
name: "adr-draft"
description: "Use ao elaborar Registros de Decisão de Arquitetura, avaliar alternativas ou documentar compromissos técnicos. Os gatilhos incluem \"ADR\", \"decisão de arquitetura\", \"compromisso\", \"escolher entre\" e \"por que escolhemos\"."
---
# Rascunho de ADR

## Quando usar

- "Elabore um ADR para a escolha do PostgreSQL em vez do MongoDB."
- "Documente nossa decisão de adotar uma arquitetura orientada a eventos."
- "Revise o ADR-007, pois precisamos substituí-lo."

## Quando escrever um ADR

Escreva um ADR quando uma decisão:

- For difícil ou cara de reverter.
- Afetar mais de uma equipe.
- Restringir escolhas futuras (dependência de tecnologia).
- Provavelmente for questionada em seis meses.

Não escreva um ADR para uma refatoração local ou uma alteração reversível de configuração.

## Dicas de redação

- Escreva no presente ("Usamos X").
- Inclua pelo menos duas alternativas rejeitadas.
- Cite consequências que você sabe que serão difíceis. Isso será útil no futuro.
- Substitua, nunca exclua. O histórico agrega valor.

## Antipadrões

- ADRs escritos posteriormente para justificar uma decisão já tomada.
- Um ADR que agrupa cinco decisões sem relação entre si.
- Ausência de uma seção de alternativas, o que indica que não houve análise de compromissos.
- Status mantido como "proposto" durante meses.

## Modelo de saída

Salve o ADR em `docs/adr/NNNN-<slug>.md`. O modelo canônico do repositório é [`docs/adr/0000-template.md`](../../../docs/adr/0000-template.md); a estrutura resumida é:

```markdown
# ADR-NNN: <Título da decisão no imperativo>

**Status**: proposto | aceito | substituído pelo ADR-NNN | descontinuado
**Data**: YYYY-MM-DD
**Responsáveis pela decisão**: <nomes>
**Tags de contexto**: segurança, desempenho, custo

## Contexto
De dois a quatro parágrafos. Qual é o fator determinante? Quais restrições se aplicam?

## Decisão
Um parágrafo. "Vamos <decisão>."

## Alternativas consideradas
- **Opção A**: <resumo>. Prós: ... Contras: ...
- **Opção B**: <resumo>. Prós: ... Contras: ...
- **Opção C (escolhida)**: <resumo>. Prós: ... Contras: ...

## Consequências
### Positivas
- ...
### Negativas
- ...
### Neutras
- ...

## Acompanhamentos
- [ ] Atualizar REQ-NNN
- [ ] Migrar <sistema>
- [ ] Revisar no T<N>

## Referências
- Fonte 1
- Fonte 2
```

## Critérios de qualidade

- [ ] O ADR tem as seções Contexto, Decisão, Alternativas consideradas e Consequências.
- [ ] Pelo menos duas alternativas rejeitadas estão documentadas com seus compromissos.
- [ ] O status está definido (proposto, aceito, substituído ou descontinuado), não em branco.
- [ ] O arquivo está salvo como `docs/adr/NNNN-<slug>.md` e vinculado aos REQ-IDs afetados.
