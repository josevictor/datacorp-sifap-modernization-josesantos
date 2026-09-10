---
name: "map-dependencies"
description: "Mapeia dependências entre programas (CALLNAT, INCLUDE) e entre programas e dados (acesso a DDM) no escopo selecionado."
argument-hint: "scope=01-archaeology/legacy-sifap/natural-programs/ recursive=true"
agent: "archaeologist"
tools: ["read", "search", "edit"]
---
# /map-dependencies

## Objetivo

Construir um grafo de dependências de um escopo selecionado da base legada pelo rastreamento de chamadas CALLNAT, diretivas INCLUDE e padrões de acesso a dados DDM. Gerar um diagrama Mermaid em que cada aresta cita sua origem.

## Quando usar

Depois que a equipe concluir o inventário inicial e quiser compreender as relações entre programas e dados.

## Pré-condições

- `01-archaeology/inventory.md` existe
- `01-archaeology/legacy-sifap/` está acessível
- A equipe selecionou um escopo: programa, fluxo batch ou família de transações

## Entradas que a equipe deve fornecer

- O escopo: caminho de arquivo, diretório ou conjunto de arquivos
- Se o rastreamento será recursivo, seguindo os destinos CALLNAT, ou terá somente um nível

## O que farei

- Pesquisarei todas as declarações `CALLNAT`, `PERFORM` e `INCLUDE` no escopo
- Identificarei o subprograma de destino de cada CALLNAT e verificarei sua existência
- Pesquisarei `READ`, `FIND`, `GET`, `STORE`, `UPDATE`, `DELETE` e `HISTOGRAM`, com referências ao DDM ou arquivo de destino
- Construirei um grafo Mermaid com dependências entre programas e entre programas e dados
- Listarei referências quebradas a programas ausentes

## O que não farei

- Inventar conexões não presentes no código-fonte; toda aresta terá arquivo e linha
- Supor a função de um destino CALLNAT pelo nome; mapearei somente a aresta
- Pressupor estruturas; lerei o que realmente existe
- Seguir referências fora de `01-archaeology/legacy-sifap/`

## Formato da saída

Um arquivo Mermaid em `01-archaeology/dependency-map.mmd` e um arquivo de apoio em `01-archaeology/dependency-map.md`:

```markdown
# Mapa de dependências — [Descrição do escopo]
## Diagrama Mermaid
## Arestas entre programas
| Origem | Destino | Tipo | Arquivo | Linha |
## Arestas entre programas e dados
| Programa | DDM/arquivo | Operação | Arquivo | Linha |
## Referências quebradas
## Observações
```

## Definição de pronto

- [ ] O arquivo Mermaid existe e renderiza um grafo válido
- [ ] Cada nó corresponde a um arquivo real
- [ ] Cada aresta cita arquivo e linha de origem
- [ ] Referências quebradas estão listadas explicitamente
- [ ] Arestas de acesso a dados distinguem READ, FIND, STORE, UPDATE e DELETE

## Corpo do prompt

Você é `@archaeologist`. A equipe quer mapear dependências em parte da base legada. Rastreie todas as relações entre programas e entre programas e dados.

**Etapa 1 — Identificar o escopo.**
Confirme se é um programa, um diretório ou um conjunto nomeado. Registre o limite e não pesquise fora dele sem solicitação explícita de rastreamento recursivo.

**Etapa 2 — Pesquisar CALLNAT.**
Para cada `CALLNAT`, extraia programa chamador, nome do subprograma de destino, linha e parâmetros passados, sem interpretá-los. Verifique se o destino existe em `01-archaeology/legacy-sifap/`; caso contrário, registre uma referência quebrada.

**Etapa 3 — Pesquisar INCLUDE.**
Para cada `INCLUDE`, extraia programa, nome do copycode e linha. Verifique se o copycode existe.

**Etapa 4 — Pesquisar PERFORM.**
Registre `PERFORM` como dependência interna. Não crie arestas no grafo entre programas, mas liste-as em seção separada.

**Etapa 5 — Pesquisar acesso a dados.**
Para `READ`, `FIND`, `GET`, `STORE`, `UPDATE`, `DELETE` e `HISTOGRAM`, extraia programa, DDM ou número do arquivo, operação, linha e descritor usado em FIND ou READ LOGICAL.

**Etapa 6 — Construir o grafo Mermaid.**
Use retângulos para programas, cilindros `[(name)]` para dados, setas sólidas “CALLNAT”, setas tracejadas “INCLUDE” e arestas para dados rotuladas com a operação. Preserve a paleta: preenchimento `#0f172a`, contorno `#334155`, texto `#e2e8f0`.

**Etapa 7 — Documentar referências quebradas e observações.**
Liste CALLNAT e INCLUDE cujos destinos não existam. Registre total de programas, total de arestas, programa mais conectado, DDM mais acessado e programas isolados.

**Etapa 8 — Escrever os arquivos.**
Escreva o diagrama em `01-archaeology/dependency-map.mmd` e a documentação em `01-archaeology/dependency-map.md`.

Toda aresta deve citar arquivo e linha. Sem origem comprovada, não inclua a aresta. Não invente conexões.

## Exemplo de chamada

```
/map-dependencies scope=01-archaeology/legacy-sifap/natural-programs/ recursive=true
```
