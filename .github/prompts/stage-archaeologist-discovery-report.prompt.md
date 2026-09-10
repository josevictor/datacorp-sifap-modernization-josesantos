---
name: "discovery-report"
description: "Sintetiza os resultados da Etapa 1 em um único relatório de descoberta, pronto para a transição à Etapa 2."
argument-hint: "team=\"Team 07\""
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /discovery-report

## Objetivo

Reunir todos os artefatos da Etapa 1 em um único relatório de descoberta para a transição à Etapa 2. O relatório deve ser autossuficiente: qualquer pessoa deve compreender as descobertas sem abrir os artefatos individuais.

## Quando usar

Ao final da Etapa 1, depois que a equipe concluir inventário, extração de regras de negócio, mapeamento de dependências e catálogo de questões em aberto.

## Pré-condições

Os quatro artefatos da Etapa 1 devem existir:

- `01-archaeology/inventory.md`, gerado por `/archaeology-kickoff`
- `01-archaeology/business-rules-catalog.md`, gerado por `/extract-business-rules`
- `01-archaeology/dependency-map.md`, gerado por `/map-dependencies`
- `01-archaeology/mysteries-found.md`, gerado por `/catalog-mysteries`

Se algum artefato estiver ausente ou vazio, o agente recusará a geração e listará o que falta.

## Entradas que a equipe deve fornecer

- Confirmação de que os quatro artefatos estão completos ou reconhecimento das lacunas
- O nome da equipe para o cabeçalho

## O que farei

- Verificarei se os quatro artefatos existem e não estão vazios
- Escreverei um resumo executivo de, no máximo, cinco frases
- Organizarei as descobertas nas categorias “confirmado” e “em risco”
- Proporei de três a cinco hipóteses de limites de contexto delimitado com base em agrupamentos de dependências
- Listarei questões em aberto junto às lacunas de maior risco, sem interpretá-las

## O que não farei

- Gerar o relatório se faltar algum artefato; listarei o que é necessário
- Definir contextos delimitados; proporei hipóteses para avaliação do arquiteto
- Preencher lacunas com suposições; o que não foi descoberto continuará desconhecido
- Adicionar análises que não estejam nos artefatos; sintetizarei, sem fazer novas descobertas

## Formato da saída

Um arquivo Markdown em `01-archaeology/discovery-report.md`:

```markdown
# Relatório de descoberta — Etapa 1
## Resumo executivo (máximo de cinco frases)
## O que sabemos (confirmado)
### Regras de negócio (somente confirmadas)
### Dependências (arestas verificadas)
### Estruturas de dados (DDMs documentados)
## O que introduz risco
### Questões em aberto que aguardam validação humana
### Regras com evidências fracas
## Hipóteses de limites recomendadas
### Hipótese 1: [Nome] — [justificativa em uma linha]
...
## Artefatos de origem
## Aprovação da equipe
```

## Definição de pronto

- [ ] O relatório existe e tem menos de três páginas impressas
- [ ] O resumo executivo tem no máximo cinco frases
- [ ] Cada declaração em “O que sabemos” referencia um artefato por caminho relativo
- [ ] Questões sem validação humana aparecem com evidência `path:line` e status
- [ ] Foram propostas de três a cinco hipóteses de limites, cada uma com nome e justificativa em uma linha
- [ ] As hipóteses estão identificadas como hipóteses, não como decisões

## Corpo do prompt

Você é `@archaeologist`. A Etapa 1 está terminando. A equipe precisa de um documento único com tudo o que descobriu, pronto para uso por `@architect` na Etapa 2.

**Etapa 1 — Verificar as entradas.**
Verifique estes quatro arquivos em `01-archaeology/`: `inventory.md`, `business-rules-catalog.md`, `dependency-map.md` e `mysteries-found.md`. Se algum estiver ausente ou vazio, interrompa imediatamente, liste os artefatos faltantes e informe qual prompt deve ser executado. Não produza relatório parcial.

**Etapa 2 — Escrever o resumo executivo.**
Leia os quatro artefatos e escreva no máximo cinco frases que respondam: qual o tamanho da base legada; quantas regras confirmadas foram encontradas; qual o nível de conexão do sistema; qual a maior questão de risco para a Etapa 2; e qual a confiança da equipe na modernização, alta, média ou baixa, com base nas evidências.

**Etapa 3 — Construir “O que sabemos”.**
Extraia somente regras “confirmadas” do catálogo, com candidatas à notação EARS e referências. Liste arestas verificadas entre programas e entre programas e dados, com totais. Resuma as estruturas DDM documentadas no inventário. Toda declaração deve citar o artefato, por exemplo, `[Consulte business-rules-catalog.md, Regra nº 3](../../01-archaeology/business-rules-catalog.md)`.

**Etapa 4 — Construir “O que introduz risco”.**
Extraia do catálogo de questões em aberto somente as linhas cujo status não registre validação humana. Preserve pergunta, evidência `path:line`, impacto, hipótese não confirmada, pessoa responsável e status. Não adicione resposta, caminho de resolução ou interpretação. Extraia também regras “inferidas”, apoiadas apenas pelo código; elas não estão confirmadas e geram risco se fundamentarem requisitos.

**Etapa 5 — Propor hipóteses de limites.**
Analise o mapa de dependências em busca de agrupamentos de programas fortemente conectados internamente e pouco conectados aos demais. Para cada hipótese, forneça nome em linguagem de negócio, programas, DDMs pertencentes e justificativa em uma linha. Proponha de três a cinco hipóteses e rotule-as explicitamente. `@architect` avaliará e decidirá na Etapa 2.

**Etapa 6 — Listar os artefatos de origem.**
Ao final, liste os quatro artefatos com caminhos relativos.

**Etapa 7 — Adicionar aprovação da equipe.**
Adicione: “Revisado por: [nomes], Data: [data], Confiança: [alta/média/baixa].” Deixe os campos para a equipe preencher.

Escreva o relatório em `01-archaeology/discovery-report.md`. Ele deve ser autossuficiente e ter menos de três páginas impressas.

## Exemplo de chamada

```
/discovery-report team="Team 07"
```
