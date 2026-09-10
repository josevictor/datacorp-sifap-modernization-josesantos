---
name: "archaeology-kickoff"
description: "Inicia a Etapa 1, orienta a equipe pelo diretório legado e produz um inventário inicial."
argument-hint: "path=01-archaeology/legacy-sifap/"
agent: "archaeologist"
model: Claude Opus 5 (copilot)
tools: ["read", "search", "edit"]
---
# /archaeology-kickoff

## Objetivo

Orientar a equipe pela base de código legada com um inventário de cima para baixo antes da leitura de qualquer programa. Esta é a primeira atividade da Etapa 1: mapear o terreno antes de investigar.

## Quando usar

No início da Etapa 1, imediatamente após a equipe receber acesso ao diretório `01-archaeology/legacy-sifap/`.

## Pré-condições

- O diretório `01-archaeology/legacy-sifap/` está disponível no espaço de trabalho; ele faz parte do kit e não depende de um script de configuração
- A equipe ainda não abriu programas individuais

## Entradas que a equipe deve fornecer

- O caminho do diretório legado, normalmente `01-archaeology/legacy-sifap/`
- A confirmação de que a equipe ainda não começou a ler arquivos individuais; este prompt serve para orientação, não para leitura aprofundada

## O que farei

- Percorrerei recursivamente `01-archaeology/legacy-sifap/` e listarei todos os diretórios
- Contarei os arquivos por extensão (`.NSN`, `.cpy`, `.ddm`, `.map` e quaisquer outras)
- Classificarei programas por prefixos de nomenclatura, por exemplo, `BN-*` para batch e `PG-*` para online
- Sinalizarei os três itens que aparentarem ser incomuns pelo tamanho do nome, tamanho do arquivo ou localização
- Proporei uma ordem de leitura baseada na classificação

## O que não farei

- Abrir ou ler arquivos de programas individuais; isso ocorrerá em prompts posteriores
- Informar o que os programas fazem; a equipe fará essa descoberta de modo independente
- Inventar explicações para convenções de nomenclatura; marcarei prefixos sem explicação como desconhecidos
- Referenciar detalhes internos específicos do sistema; trabalharei somente com o que a estrutura de diretórios revelar

## Formato da saída

Um arquivo Markdown em `01-archaeology/inventory.md` com:

```markdown
# Inventário do legado — [Nome da equipe]
## Estrutura de diretórios
## Quantidade de arquivos por tipo
## Padrões de nomenclatura
## Itens incomuns (três principais)
## Ordem de leitura proposta
```

## Definição de pronto

- [ ] O arquivo de inventário existe e documenta a estrutura de diretórios
- [ ] As contagens estão corretas e podem ser verificadas por outra pessoa da equipe com `find`
- [ ] Pelo menos três padrões de nomenclatura foram identificados com suas contagens
- [ ] Três itens que aparentam ser incomuns foram sinalizados com caminhos e motivos
- [ ] A ordem de leitura proposta foi justificada por padrões de nomenclatura ou posição estrutural

## Corpo do prompt

Você é `@archaeologist` e inicia com a equipe uma orientação da Etapa 1. A equipe acabou de receber a base de código legada e ainda não abriu arquivos.

Execute as etapas seguintes na ordem. Não omita nenhuma.

**Etapa 1 — Mapear a árvore de diretórios.**
Liste todos os diretórios e subdiretórios no caminho legado fornecido. Exiba a árvore e conte o total de diretórios.

**Etapa 2 — Contar arquivos por extensão.**
Informe a quantidade de cada extensão encontrada (`.NSN`, `.cpy`, `.ddm`, `.map`, `.txt`, `.md` ou outra). Apresente a tabela `| Extensão | Quantidade | Finalidade provável |`. Em “Finalidade provável”, use apenas conhecimento geral de Natural/Adabas, por exemplo, `.NSN` = programa-fonte Natural, `.cpy` = copycode e `.ddm` = Data Definition Module. Não suponha o conteúdo de arquivos específicos.

**Etapa 3 — Identificar padrões de nomenclatura.**
Examine os nomes sem abrir os arquivos. Agrupe-os pelo prefixo formado pelos primeiros dois ou três caracteres antes de delimitadores como `-`, `_` ou um dígito. Para padrões com dois ou mais arquivos, apresente `| Prefixo | Quantidade | Hipótese |`. Baseie a hipótese somente em conhecimento geral das convenções Natural. Se o padrão não estiver claro, use `Desconhecido — investigar na próxima etapa`.

**Etapa 4 — Sinalizar itens incomuns.**
Identifique os três itens mais incomuns: maior arquivo, aninhamento mais profundo, padrão de nome único ou extensão única. Informe caminho, motivo e ação sugerida para investigação.

**Etapa 5 — Propor uma ordem de leitura.**
Priorize: (a) pontos de entrada batch, normalmente reconhecíveis por prefixos; (b) arquivos DDM, para compreender os dados antes do código; e (c) programas mais conectados, cujos nomes apareçam como argumentos em outros nomes de arquivo e sugiram relações CALLNAT. Declare que se trata de hipótese e que a ordem mudará quando a equipe rastrear dependências.

**Etapa 6 — Gerar o inventário.**
Escreva o inventário completo em `01-archaeology/inventory.md` com o formato acima. Inclua a data, um placeholder para o nome da equipe e uma observação de que esta é a primeira análise, que será revisada durante a leitura dos arquivos.

Não abra arquivos para ler o conteúdo. Este prompt atua somente sobre nomes e estrutura de diretórios. Se a equipe pedir a leitura de um arquivo, encaminhe-a para `/extract-business-rules` ou `/map-dependencies`.

## Exemplo de chamada

```
/archaeology-kickoff path=01-archaeology/legacy-sifap/
```
