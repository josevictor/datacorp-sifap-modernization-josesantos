# Referência do esquema XML do draw.io

Referência completa do formato de arquivo `.drawio` (XML mxGraph). Use-a ao gerar, analisar ou validar arquivos de diagrama.

---

## Estrutura de nível superior

Todo arquivo `.drawio` é um XML com esta estrutura-raiz:

```xml
<!-- Defina modified com o timestamp ISO 8601 atual ao gerar um novo arquivo -->
<mxfile host="Electron" modified=""
        agent="draw.io" version="26.0.0" type="device">
  <diagram id="<id-exclusivo>" name="<Nome da página>">
    <mxGraphModel ...attributes...>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Todas as células de conteúdo entram aqui -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Atributos de `<mxfile>`

| Atributo | Obrigatório | Padrão | Descrição |
| ----------- | ---------- | --------- | ------------- |
| `host` | Não | `"app.diagrams.net"` | Editor de origem (`"Electron"` para desktop/VS Code) |
| `modified` | Não | — | Timestamp ISO 8601 |
| `agent` | Não | — | String do agente de usuário |
| `version` | Não | — | Versão do draw.io |
| `type` | Não | `"device"` | Tipo de armazenamento |

### Atributos de `<diagram>`

| Atributo | Obrigatório | Descrição |
| ----------- | ---------- | ------------- |
| `id` | Sim | Identificador exclusivo da página (qualquer string) |
| `name` | Sim | Rótulo da aba exibido no editor |

### Atributos de `<mxGraphModel>`

| Atributo | Tipo | Padrão | Descrição |
| ----------- | ------ | --------- | ------------- |
| `dx` | int | `1422` | Deslocamento da rolagem no eixo X |
| `dy` | int | `762` | Deslocamento da rolagem no eixo Y |
| `grid` | `0`/`1` | `1` | Exibir grade |
| `gridSize` | int | `10` | Tamanho do ajuste à grade em px |
| `guides` | `0`/`1` | `1` | Exibir guias de alinhamento |
| `tooltips` | `0`/`1` | `1` | Habilitar dicas de ferramenta |
| `connect` | `0`/`1` | `1` | Habilitar setas de conexão ao passar o cursor |
| `arrows` | `0`/`1` | `1` | Exibir setas direcionais |
| `fold` | `0`/`1` | `1` | Habilitar expansão/recolhimento de grupos |
| `page` | `0`/`1` | `1` | Exibir limite da página |
| `pageScale` | float | `1` | Escala de zoom da página |
| `pageWidth` | int | `1169` | Largura da página em px (A4 em paisagem) |
| `pageHeight` | int | `827` | Altura da página em px (A4 em paisagem) |
| `math` | `0`/`1` | `0` | Habilitar renderização matemática LaTeX |
| `shadow` | `0`/`1` | `0` | Sombra global nas formas |

**Tamanhos comuns de página (px a 96 dpi):**

| Formato | Largura | Altura |
| -------- | ------- | -------- |
| A4 em paisagem | `1169` | `827` |
| A4 em retrato | `827` | `1169` |
| A3 em paisagem | `1654` | `1169` |
| Carta em paisagem | `1100` | `850` |
| Carta em retrato | `850` | `1100` |
| Tela (16:9) | `1654` | `931` |

---

## Células reservadas (sempre obrigatórias)

```xml
<mxCell id="0" />                 <!-- Célula-raiz: nunca omita nem adicione atributos -->
<mxCell id="1" parent="0" />     <!-- Camada-padrão: todas as células são filhas desta -->
```

Essas duas células DEVEM ser as primeiras entradas dentro de `<root>`. Os IDs `0` e `1` são reservados e não podem ser usados por nenhuma outra célula.

---

## Elemento de vértice (forma)

```xml
<mxCell
  id="2"
  value="Texto do rótulo"
  style="rounded=1;whiteSpace=wrap;html=1;"
  vertex="1"
  parent="1">
  <mxGeometry x="200" y="160" width="120" height="60" as="geometry" />
</mxCell>
```

### Atributos de vértice de `<mxCell>`

| Atributo | Obrigatório | Tipo | Descrição |
| ----------- | ---------- | ------ | ------------- |
| `id` | Sim | string | Identificador exclusivo neste diagrama |
| `value` | Sim | string | Texto do rótulo (HTML permitido se o estilo tiver `html=1`) |
| `style` | Sim | string | String de estilo key=value delimitada por ponto e vírgula |
| `vertex` | Sim | `"1"` | Deve ser `"1"` para declarar uma forma |
| `parent` | Sim | string | ID da célula-pai (`"1"` para a camada-padrão) |

### Atributos de vértice de `<mxGeometry>`

| Atributo | Obrigatório | Tipo | Descrição |
| ----------- | ---------- | ------ | ------------- |
| `x` | Sim | float | Borda esquerda da forma (px a partir da origem da tela) |
| `y` | Sim | float | Borda superior da forma (px a partir da origem da tela) |
| `width` | Sim | float | Largura da forma em px |
| `height` | Sim | float | Altura da forma em px |
| `as` | Sim | `"geometry"` | Sempre `"geometry"` |

---

## Elemento de aresta (conector)

```xml
<mxCell
  id="5"
  value="Rótulo"
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;"
  edge="1"
  source="2"
  target="3"
  parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Atributos de aresta de `<mxCell>`

| Atributo | Obrigatório | Tipo | Descrição |
| ----------- | ---------- | ------ | ------------- |
| `id` | Sim | string | Identificador exclusivo |
| `value` | Sim | string | Rótulo do conector (string vazia quando não houver rótulo) |
| `style` | Sim | string | String de estilo (consulte Estilos de aresta) |
| `edge` | Sim | `"1"` | Deve ser `"1"` para declarar um conector |
| `source` | Não | string | ID do vértice de origem |
| `target` | Não | string | ID do vértice de destino |
| `parent` | Sim | string | ID da célula-pai (normalmente `"1"`) |

### Atributos de aresta de `<mxGeometry>`

| Atributo | Obrigatório | Tipo | Descrição |
| ----------- | ---------- | ------ | ------------- |
| `relative` | Não | `"1"` | Sempre `"1"` para arestas |
| `as` | Sim | `"geometry"` | Sempre `"geometry"` |

### Aresta com deslocamento de rótulo

```xml
<mxGeometry x="-0.1" y="10" relative="1" as="geometry">
  <mxPoint as="offset" />
</mxGeometry>
```

O `x` na geometria relativa move o rótulo ao longo da aresta (-1 a 1). `y` é o deslocamento perpendicular em px.

### Aresta com pontos de passagem manuais (pontos de controle)

```xml
<mxGeometry relative="1" as="geometry">
  <Array as="points">
    <mxPoint x="340" y="80" />
    <mxPoint x="340" y="200" />
  </Array>
</mxGeometry>
```

---

## Diagramas com várias páginas

```xml
<mxfile>
  <diagram id="page-1" name="Visão geral">
    <mxGraphModel>...</mxGraphModel>
  </diagram>
  <diagram id="page-2" name="Detalhes">
    <mxGraphModel>...</mxGraphModel>
  </diagram>
</mxfile>
```

Cada `<diagram>` é uma página/aba separada. Os IDs das células têm o escopo do próprio `<diagram>`. O mesmo valor de ID pode aparecer em páginas diferentes sem conflito.

---

## Células de camada

As camadas substituem a camada-padrão `id="1"`. As células são atribuídas a uma camada por meio de `parent`:

```xml
<mxCell id="0" />
<mxCell id="1" value="Plano de fundo" parent="0" />        <!-- camada 1 -->
<mxCell id="layer2" value="Serviços" parent="0" />         <!-- camada 2 -->
<mxCell id="layer3" value="Conectores" parent="0" />       <!-- camada 3 -->

<!-- Atribua a camada por meio do atributo parent -->
<mxCell id="10" value="API" ... parent="layer2">
  <mxGeometry ... />
</mxCell>
```

Alterne a visibilidade da camada:

```xml
<mxCell id="layer2" value="Serviços" parent="0" visible="0" />
```

---

## Contêiner de raias (`swimlane`)

```xml
<!-- Contêiner de raias (swimlane) -->
<mxCell id="swim1" value="Processo" style="shape=pool;startSize=30;horizontal=1;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="800" height="340" as="geometry" />
</mxCell>

<!-- Raia 1 (filha do contêiner swimlane) -->
<mxCell id="lane1" value="Cliente" style="swimlane;startSize=30;"
        vertex="1" parent="swim1">
  <mxGeometry x="0" y="30" width="800" height="150" as="geometry" />
</mxCell>

<!-- Forma dentro da raia (filha da raia) -->
<mxCell id="step1" value="Fazer pedido" style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="lane1">
  <mxGeometry x="80" y="50" width="120" height="60" as="geometry" />
</mxCell>
```

> **Importante**: as células dentro de uma raia (`swimlane`) têm `parent` definido com o **ID da raia**, não `"1"`.
> As coordenadas dentro das raias são **relativas à origem da raia**.

---

## Células de grupo

```xml
<!-- Contêiner de grupo invisível -->
<mxCell id="group1" value="" style="group;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry" />
</mxCell>

<!-- Filhos relativos à origem do grupo -->
<mxCell id="child1" value="A" style="rounded=1;" vertex="1" parent="group1">
  <mxGeometry x="20" y="20" width="100" height="60" as="geometry" />
</mxCell>
```

---

## Rótulos HTML

Quando o estilo contém `html=1`, `value` pode conter HTML:

```xml
<mxCell value="&lt;b&gt;OrderService&lt;/b&gt;&lt;br&gt;&lt;i&gt;:8080&lt;/i&gt;"
        style="rounded=1;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="60" as="geometry" />
</mxCell>
```

O HTML deve usar escapes XML:

- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`
- `"` → `&quot;`

Tags HTML comuns compatíveis: `<b>`, `<i>`, `<u>`, `<br>`, `<font color="#hex">`, `<span style="...">`, `<hr/>`

---

## Dica de ferramenta / Metadados

```xml
<mxCell value="Nome do serviço" tooltip="Processa pedidos" style="..." vertex="1" parent="1">
  <mxGeometry ... />
</mxCell>
```

---

## Regras de geração de IDs

| Regra | Detalhe |
| ------ | -------- |
| IDs `0` e `1` | Reservados, sempre a raiz e a camada-padrão |
| Todos os outros IDs | Devem ser exclusivos em seu `<diagram>` |
| Padrão seguro | Inteiros sequenciais a partir de `2` ou strings UUID |
| Entre páginas | Os IDs não precisam ser exclusivos entre páginas `<diagram>` diferentes |

**Exemplo seguro de ID sequencial:**

```text
id="2", id="3", id="4", ...
```

**Exemplo no estilo UUID:**

```text
id="a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

---

## Sistema de coordenadas

- A origem `(0, 0)` fica no **canto superior esquerdo** da tela
- `x` aumenta **para a direita**
- `y` aumenta **para baixo**
- Todas as unidades estão em **pixels**

---

## Espaçamento recomendado

| Contexto | Valor |
| --------- | ------- |
| Espaço mínimo entre formas | `40px` |
| Espaço confortável | `80px` |
| Preenchimento interno da raia (`swimlane`) | `20px` |
| Margem da borda da página | `40px` |
| Folga para roteamento de conectores | `10px` |

---

## Arquivo `.drawio` válido mínimo

```xml
<mxfile host="Electron" modified="2026-03-25T00:00:00.000Z" version="26.0.0">
  <diagram id="main" name="Page-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827"
                  math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## Regras de validação

### Obrigatórias

- [ ] As células `id="0"` e `id="1"` estão sempre presentes como os dois primeiros filhos de `<root>`
- [ ] Nenhuma outra célula usa `id="0"` ou `id="1"`
- [ ] Todos os valores de `id` são exclusivos em cada `<diagram>`
- [ ] Cada `<mxCell>` tem exatamente um filho `<mxGeometry>`
- [ ] `<mxGeometry>` tem o atributo `as="geometry"`
- [ ] Células de vértice têm `vertex="1"`; células de aresta têm `edge="1"`
- [ ] Os IDs `source`/`target` das arestas referenciam IDs de vértices existentes no mesmo diagrama
- [ ] Filhos de uma raia (`swimlane`) têm `parent` definido com o ID da raia, não `"1"`
- [ ] O HTML nos atributos `value` usa escapes XML

### Recomendadas

- [ ] As formas não se sobrepõem, salvo intencionalmente (use espaço ≥40 px)
- [ ] Os rótulos das arestas são curtos (≤4 palavras)
- [ ] As células de camada têm nomes descritivos em `value`
- [ ] Todas as formas cabem nos limites de `pageWidth` × `pageHeight`
