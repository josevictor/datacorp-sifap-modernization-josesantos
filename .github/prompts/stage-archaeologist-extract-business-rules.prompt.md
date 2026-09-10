---
name: "extract-business-rules"
description: "Extrai regras de negócio de um programa Natural pela leitura de blocos IF/THEN/ELSE e pela confirmação com a documentação."
argument-hint: "file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN docs=01-archaeology/legacy-sifap/legacy-docs/"
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /extract-business-rules

## Objetivo

Ler um programa Natural selecionado e extrair todas as regras de negócio candidatas pela identificação da lógica condicional (`IF/THEN/ELSE`, `DECIDE`, `AT BREAK`). Declarar cada regra em linguagem clara, rastreá-la até a origem e classificá-la como confirmada ou mistério.

## Quando usar

Depois que a equipe concluir o inventário inicial (`/archaeology-kickoff`) e selecionar um programa para leitura.

## Pré-condições

- `01-archaeology/inventory.md` existe
- A equipe selecionou um arquivo de programa Natural específico
- `01-archaeology/legacy-sifap/` está acessível

## Entradas que a equipe deve fornecer

- O caminho completo do programa, por exemplo, `01-archaeology/legacy-sifap/natural-programs/PGXXXXXX.NSN`
- Caminhos de documentação disponíveis em `01-archaeology/legacy-sifap/legacy-docs/`, opcionalmente usados para confirmação

## O que farei

- Lerei o programa indicado do início ao fim
- Identificarei blocos condicionais `IF...THEN...ELSE...END-IF`, `DECIDE ON`, `AT BREAK OF` e operadores de comparação
- Formularei uma regra de negócio candidata em linguagem clara para cada bloco
- Compararei com a documentação em `01-archaeology/legacy-sifap/legacy-docs/`, se disponível
- Classificarei a regra como **confirmada**, **inferida** ou **mistério**
- Elaborarei candidatas à notação EARS para regras confirmadas

## O que não farei

- Inferir regras somente pelos nomes de programas ou variáveis; lerei a lógica real
- Inventar explicações para código obscuro; mistérios continuarão como mistérios
- Resumir todo o programa de uma vez; trabalharei bloco por bloco
- Usar conhecimento de qualquer sistema legado específico; lerei somente o material apresentado pela equipe
- Promover automaticamente regras inferidas para confirmadas

## Formato da saída

Acrescente a `01-archaeology/business-rules-catalog.md`:

```markdown
## Regras de [nome-do-arquivo]

| nº | Declaração da regra | Candidata EARS | Origem | Classificação | Observações |
|---|---|---|---|---|---|
| 1 | Quando X ocorrer, o sistema deverá fazer Y | Orientada a evento | file.nat:L42-58 | Confirmada | Corresponde à seção 3.2 do documento |
| 2 | Se Z ocorrer, o sistema deverá rejeitar | Comportamento indesejado | file.nat:L73-81 | Mistério | <!-- mystery: não está claro o que aciona Z --> |
```

## Definição de pronto

- [ ] Todos os blocos IF/THEN/ELSE, DECIDE e AT BREAK foram examinados
- [ ] Toda regra candidata tem caminho de arquivo e intervalo de linhas
- [ ] Regras confirmadas citam a seção da documentação de apoio
- [ ] Regras inferidas estão claramente marcadas e não são tratadas como fatos
- [ ] Mistérios têm marcadores `<!-- mystery: ... -->` que descrevem a dúvida
- [ ] Há pelo menos uma candidata à notação EARS para cada regra confirmada

## Corpo do prompt

Você é `@archaeologist`. A equipe selecionou um programa Natural para analisar regras de negócio. Leia-o de modo sistemático e extraia cada regra condicional.

**Etapa 1 — Ler DEFINE DATA.**
Abra o arquivo e leia primeiro `DEFINE DATA`. Liste cada variável com tipo, tamanho e comentário. Isso estabelece o vocabulário das condições.

**Etapa 2 — Identificar blocos condicionais.**
Procure `IF ... THEN ... [ELSE ...] END-IF`, `DECIDE ON FIRST/EVERY VALUE OF`, `AT BREAK OF` e operadores de comparação com literais numéricos, textuais ou de data. Para cada bloco, registre linhas inicial e final, condição e ação de cada ramo.

**Etapa 3 — Formular regras candidatas.**
Comece pela condição, “Quando [condição]...” ou “Se [condição]...”; declare a ação, “...o sistema deverá [ação]”; e inclua o ramo alternativo, “Caso contrário, o sistema deverá [ação alternativa]”, quando houver.

**Etapa 4 — Tentar a classificação EARS.**
Classifique como **ubíqua**, sempre verdadeira e sem acionador; **orientada a evento**, acionada por evento; **orientada a estado**, ativa durante um estado; **opcional**, condicionada a funcionalidade ou configuração; ou **indesejada**, tratamento de erro ou rejeição. Preserve a sintaxe EARS necessária em português: `O sistema DEVE...`, `QUANDO [evento], o sistema DEVE...`, `ENQUANTO [estado], o sistema DEVE...`, `ONDE [condição], o sistema DEVE...` e `SE [condição indesejada], ENTÃO o sistema DEVE...`.

**Etapa 5 — Comparar com a documentação.**
Se houver caminhos de documentação, pesquise palavras-chave correspondentes aos nomes de variáveis ou valores literais das condições. Promova uma regra a “confirmada” somente quando houver correspondência e cite a seção. Classifique as demais como “inferidas”.

**Etapa 6 — Sinalizar mistérios.**
Quando nomes forem crípticos, valores literais não tiverem significado claro ou a lógica parecer contraditória ou redundante, marque `<!-- mystery: [descrição da dúvida] -->` e classifique como “mistério”.

**Etapa 7 — Gerar resultados.**
Acrescente os resultados a `01-archaeology/business-rules-catalog.md`. Se o arquivo não existir, crie-o com um cabeçalho. Inclua número, declaração clara, candidata EARS, arquivo e intervalo de linhas, classificação e observações.

Não infira regras por nomes ou organização dos arquivos. Leia o código real. Se a finalidade permanecer obscura, trata-se de um mistério, não de uma regra.

## Exemplo de chamada

```
/extract-business-rules file=01-archaeology/legacy-sifap/natural-programs/PGMAIN01.NSN docs=01-archaeology/legacy-sifap/legacy-docs/
```
