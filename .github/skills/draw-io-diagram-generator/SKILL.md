---
name: "draw-io-diagram-generator"
description: "Use ao criar, editar ou gerar arquivos de diagrama draw.io (.drawio, .drawio.svg, .drawio.png). Abrange criação de XML mxGraph, bibliotecas de formas, strings de estilo, fluxogramas, arquitetura de sistemas, diagramas de sequência, diagramas ER, diagramas de classes UML, topologia de rede, estratégia de disposição, extensão hediet.vscode-drawio do VS Code e o fluxo completo do agente, da solicitação ao arquivo pronto para abrir."
---
# Gerador de diagramas draw.io

Esta habilidade permite gerar, editar e validar arquivos de diagrama draw.io (`.drawio`) com a estrutura XML mxGraph correta. Todos os arquivos gerados abrem imediatamente na [extensão draw.io para VS Code](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) (`hediet.vscode-drawio`), sem exigir correções manuais. Você também pode abrir os arquivos no aplicativo web ou desktop do draw.io.

| Seção | Finalidade |
|---|---|
| Quando usar | Frases de gatilho e tipos de diagrama compatíveis |
| Pré-requisitos | Extensão e ferramentas Python opcionais |
| Fluxo passo a passo do agente | Da solicitação à disposição, ao XML e ao arquivo validado |
| Receitas por tipo de diagrama | Trechos de fluxograma, arquitetura, sequência, ER e UML |
| Várias páginas e edição | Arquivos com várias páginas e edições seguras em diagramas existentes |
| Modelo de saída | Artefato `.drawio` exato a entregar |
| Critérios de qualidade | Verificações estruturais antes da entrega |
| Referências | Modelos, referências e scripts incluídos |

---

## Quando usar

- "Crie um diagrama de arquitetura de sistema para estes serviços."
- "Desenhe um fluxograma deste processo de aprovação."
- "Gere um diagrama ER a partir destas tabelas."
- "Transforme esta sequência de chamadas de API em um diagrama de sequência."

Qualquer solicitação para produzir ou modificar um arquivo `.drawio`, `.drawio.svg` ou `.drawio.png` carrega esta habilidade. Frases de gatilho relacionadas incluem "projetar um diagrama de sequência", "fazer um diagrama de classes UML", "criar um diagrama ER", "documentar a arquitetura", "mostrar o modelo de dados" e "visualizar o fluxo".

> [!NOTE]
> Os arquivos gerados são renderizados na **extensão draw.io para VS Code** (`hediet.vscode-drawio`), o editor usado pela imersão para diagramas. Se ela não estiver instalada, o arquivo `.drawio` continuará válido. Nesse caso, abra-o no aplicativo web ou desktop do draw.io. Os programas auxiliares em Python armazenados em `scripts/` são opcionais e exigem Python 3.8+.

**Tipos de diagrama compatíveis**

| Tipo de diagrama | Modelo disponível | Descrição |
|---|---|---|
| Fluxograma | `assets/templates/flowchart.drawio` | Fluxos de processo com decisões e ramificações |
| Arquitetura de sistema | `assets/templates/architecture.drawio` | Arquitetura de serviços em várias camadas |
| Diagrama de sequência | `assets/templates/sequence.drawio` | Linhas de vida de atores e fluxos de mensagens temporizados |
| Diagrama ER | `assets/templates/er-diagram.drawio` | Tabelas de banco de dados com relacionamentos |
| Diagrama de classes UML | `assets/templates/uml-class.drawio` | Classes, interfaces, enums e relacionamentos |
| Topologia de rede | (usar biblioteca de formas) | Roteadores, servidores, firewalls e sub-redes |
| Fluxo de trabalho BPMN | (usar biblioteca de formas) | Eventos, tarefas e elementos de decisão (`gateways`) de processos de negócio |
| Mapa mental | (manual) | Tópico central com ramificações radiais |

---

## Pré-requisitos

- Se estiver usando a integração com o VS Code, instale a **extensão draw.io para VS Code**, cujo ID é `hediet.vscode-drawio`. Instale-a com:

  ```text
  ext install hediet.vscode-drawio
  ```

- **Extensões de arquivo compatíveis**: `.drawio`, `.drawio.svg`, `.drawio.png`
- **Python 3.8+** (opcional): para os programas de validação e inserção de formas em `scripts/`

---

## Fluxo passo a passo do agente

Siga estas etapas na ordem em todas as tarefas de geração de diagramas.

### Etapa 1: entender a solicitação

Pergunte ou deduza:

1. **Tipo de diagrama**: que tipo de diagrama? (fluxograma, arquitetura, UML, ER, sequência, rede...)
2. **Entidades / atores**: quais são os principais componentes, atores, classes ou tabelas?
3. **Relacionamentos**: como se conectam? Em qual direção? Com qual cardinalidade?
4. **Caminho de saída**: onde o arquivo `.drawio` deve ser salvo?
5. **Arquivo existente**: criaremos um arquivo ou editaremos um existente?

Se a solicitação for ambígua, deduza pelo contexto o tipo de diagrama mais adequado (por exemplo, "mostrar as tabelas" → diagrama ER; "mostrar o fluxo da chamada de API" → diagrama de sequência).

### Etapa 2: selecionar um modelo ou começar do zero

- **Use um modelo** quando o tipo de diagrama corresponder a um modelo em `assets/templates/`. Copie a estrutura e substitua os valores dos placeholders.
- **Comece do zero** para disposições novas. Inicie com a estrutura mínima válida:

```xml
<!-- Defina modified="" com o timestamp ISO 8601 atual ao gerar um novo arquivo -->
<mxfile host="Electron" modified="" version="26.0.0">
  <diagram id="page-1" name="Page-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827"
                  math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Suas células entram aqui -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

> **Regra**: os IDs `0` e `1` são SEMPRE obrigatórios e devem ser as duas primeiras células. Nunca os reutilize.

### Etapa 3: planejar a disposição

Antes de gerar o XML, esboce o posicionamento lógico:

- Organize em **linhas** ou **camadas** (use raias, chamadas `swimlane` no draw.io, para representar as camadas)
- **Espaçamento horizontal**: 40–60 px entre formas na mesma linha
- **Espaçamento vertical**: 80–120 px entre linhas de camadas
- Tamanho-padrão das formas: `120x60` px para caixas de processo, `160x80` px para swimlanes
- Tela-padrão: A4 em paisagem = `1169 x 827` px

### Etapa 4: gerar o XML mxGraph

**Célula de vértice** (todas as formas):

```xml
<mxCell id="unique-id" value="Rótulo"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

**Célula de aresta** (todos os conectores):

```xml
<mxCell id="edge-id" value="Rótulo (opcional)"
        style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="source-id" target="target-id" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**Regras críticas**:

- Cada ID de célula deve ser **globalmente exclusivo** no arquivo
- Cada vértice deve ter um filho `mxGeometry` com `x`, `y`, `width`, `height`, `as="geometry"`
- Cada aresta deve ter `source` e `target` correspondentes a IDs de vértices existentes. **Exceção**: arestas flutuantes (por exemplo, linhas de vida de diagramas de sequência) usam `sourcePoint`/`targetPoint` dentro de `<mxGeometry>`; consulte a receita de diagrama de sequência
- O `parent` de cada célula deve referenciar um ID de célula existente
- Use `html=1` no estilo quando o rótulo contiver HTML (`<b>`, `<i>`, `<br>`)
- Use escape nos caracteres XML especiais dos rótulos: `&` => `&amp;`, `<` => `&lt;`, `>` => `&gt;`

### Etapa 5: aplicar os estilos corretos

Use a paleta de cores semântica padrão para manter a consistência:

| Finalidade | fillColor | strokeColor |
|---|---|---|
| Principal / Informação | `#dae8fc` | `#6c8ebf` |
| Sucesso / Início | `#d5e8d4` | `#82b366` |
| Aviso / Decisão | `#fff2cc` | `#d6b656` |
| Erro / Fim | `#f8cecc` | `#b85450` |
| Neutro | `#f5f5f5` | `#666666` |
| Externo / Parceiro | `#e1d5e7` | `#9673a6` |

Strings de estilo comuns por tipo de diagrama:

| Finalidade | String de estilo |
|---|---|
| Caixa de processo arredondada (fluxograma) | `rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;` |
| Losango de decisão | `rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;` |
| Terminal de início/fim | `ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;` |
| Cilindro de banco de dados | `shape=mxgraph.flowchart.database;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;` |
| Contêiner swimlane (camada) | `swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;` |
| Caixa de classe UML | `swimlane;fontStyle=1;align=center;startSize=40;fillColor=#dae8fc;strokeColor=#6c8ebf;` |
| Caixa de interface / estereótipo | `swimlane;fontStyle=3;align=center;startSize=40;fillColor=#f5f5f5;strokeColor=#666666;` |
| Contêiner de tabela ER | `shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;` |
| Conector ortogonal | `edgeStyle=orthogonalEdgeStyle;html=1;` |
| Relacionamento ER (pé de galinha) | `edgeStyle=entityRelationEdgeStyle;html=1;endArrow=ERmany;startArrow=ERone;` |

> Consulte `references/style-reference.md` para ver o catálogo completo de chaves de estilo e `references/shape-libraries.md` para ver todos os nomes de bibliotecas de formas.

### Etapa 6: salvar e validar

1. **Grave o arquivo** no caminho solicitado com a extensão `.drawio`
2. **Execute o validador** (opcional, mas recomendado):

   ```bash
   python .github/skills/draw-io-diagram-generator/scripts/validate-drawio.py <path-to-file.drawio>
   ```

3. **Informe à pessoa** como abrir o arquivo:
   > "Abra `<filename>` no VS Code. A extensão draw.io o renderizará automaticamente. Se preferir, você também pode usar o aplicativo web ou desktop do draw.io."
4. **Forneça uma breve descrição** do conteúdo do diagrama para que a pessoa saiba o que esperar.

---

## Receitas por tipo de diagrama

### Fluxograma

Elementos principais: Início (elipse) => Processo (retângulo arredondado) => Decisão (losango) => Fim (elipse)

```xml
<!-- Nó inicial -->
<mxCell id="start" value="Início"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="80" width="120" height="60" as="geometry" />
</mxCell>

<!-- Processo -->
<mxCell id="p1" value="Etapa do processo"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="200" width="120" height="60" as="geometry" />
</mxCell>

<!-- Decisão -->
<mxCell id="d1" value="Condição?"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="460" y="320" width="200" height="100" as="geometry" />
</mxCell>

<!-- Seta: start para p1 -->
<mxCell id="e1" value=""
        style="edgeStyle=orthogonalEdgeStyle;html=1;"
        edge="1" source="start" target="p1" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Diagrama de arquitetura (três camadas)

Use **contêineres de raias (`swimlane`)** para cada camada. Todas as caixas de serviço são filhas da respectiva raia.

```xml
<!-- Swimlane da camada -->
<mxCell id="tier1" value="Camada de cliente"
        style="swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="60" y="100" width="1050" height="130" as="geometry" />
</mxCell>

<!-- Serviço dentro da camada (parent="tier1", coordenadas relativas à camada) -->
<mxCell id="webapp" value="Aplicativo web"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="tier1">
  <mxGeometry x="80" y="40" width="120" height="60" as="geometry" />
</mxCell>
```

> Os conectores entre camadas usam coordenadas absolutas com `parent="1"`.

### Diagrama de sequência

Elementos principais: atores (parte superior), linhas de vida (linhas verticais tracejadas), caixas de ativação e setas de mensagem.

- Linhas de vida: `edge="1"` com `endArrow=none` e `dashed=1`, sem source/target. Use `sourcePoint`/`targetPoint` na geometria
- Mensagem síncrona: `endArrow=block;endFill=1`
- Mensagem de retorno: `endArrow=open;endFill=0;dashed=1`
- Autochamada: faça a aresta dar uma volta por dois pontos de Array à direita e retornar

**Trecho XML mínimo:**

```xml
<!-- Ator (figura humana) -->
<mxCell id="actorA" value="Cliente"
        style="shape=mxgraph.uml.actor;pointerEvents=1;dashed=0;whiteSpace=wrap;html=1;aspect=fixed;"
        vertex="1" parent="1">
  <mxGeometry x="110" y="80" width="60" height="80" as="geometry" />
</mxCell>

<!-- Caixa de serviço -->
<mxCell id="actorB" value="Servidor de API"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="480" y="100" width="160" height="60" as="geometry" />
</mxCell>

<!-- Linha de vida, aresta flutuante: usa sourcePoint/targetPoint, NÃO os atributos source/target -->
<mxCell id="lifA" value=""
        style="edgeStyle=none;dashed=1;endArrow=none;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="140" y="160" as="sourcePoint" />
    <mxPoint x="140" y="700" as="targetPoint" />
  </mxGeometry>
</mxCell>

<!-- Caixa de ativação (retângulo estreito na linha de vida) -->
<mxCell id="actA1" value=""
        style="fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="130" y="220" width="20" height="180" as="geometry" />
</mxCell>

<!-- Mensagem síncrona -->
<mxCell id="msg1" value="POST /orders"
        style="edgeStyle=elbowEdgeStyle;elbow=vertical;html=1;endArrow=block;endFill=1;"
        edge="1" source="actA1" target="actorB" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Mensagem de retorno (tracejada) -->
<mxCell id="msg2" value="201 Created"
        style="edgeStyle=elbowEdgeStyle;elbow=vertical;dashed=1;html=1;endArrow=open;endFill=0;"
        edge="1" source="actorB" target="actA1" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

> **Observação:** as linhas de vida são arestas flutuantes que usam `sourcePoint`/`targetPoint` em `<mxGeometry>`, em vez dos atributos `source`/`target`. Esse é o padrão do draw.io para diagramas de sequência.

### Diagrama ER

Use contêineres `shape=table` com `childLayout=tableLayout`. As linhas são células `shape=tableRow` com `portConstraint=eastwest`. As colunas dentro de cada linha são `shape=partialRectangle`.

As setas de relacionamento usam `edgeStyle=entityRelationEdgeStyle`:

- Um para um: `startArrow=ERone;endArrow=ERone`
- Um para muitos: `startArrow=ERone;endArrow=ERmany`
- Muitos para muitos: `startArrow=ERmany;endArrow=ERmany`
- Obrigatório: `ERmandOne`; opcional: `ERzeroToOne`

### Diagrama de classes UML

As caixas de classe são contêineres swimlane. Atributos e métodos são células de texto simples. Os divisores são filhos de swimlane com altura zero.

Estilos de seta por tipo de relacionamento:

| Relacionamento | String de estilo |
|---|---|
| Herança (extends) | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=0;` |
| Realização (implements) | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=block;endFill=0;` |
| Composição | `edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=1;endArrow=none;` |
| Agregação | `edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=0;endArrow=none;` |
| Dependência | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=open;endFill=0;` |
| Associação | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=open;endFill=0;` |

---

## Diagramas com várias páginas

Adicione vários elementos `<diagram>` para sistemas complexos:

```xml
<mxfile host="Electron" version="26.0.0">
  <diagram id="overview" name="Visão geral">
    <!-- mxGraphModel da visão geral -->
  </diagram>
  <diagram id="detail" name="Visão detalhada">
    <!-- mxGraphModel da visão detalhada -->
  </diagram>
</mxfile>
```

Cada página tem seu próprio espaço de nomes independente para os IDs das células. O mesmo valor de ID pode aparecer em páginas diferentes sem conflito.

---

## Editar diagramas existentes

Ao modificar um arquivo `.drawio` existente:

1. **Leia** primeiro o arquivo para entender os IDs, as posições e a hierarquia de pais das células existentes
2. **Identifique a página de destino do diagrama** pelo índice ou pelo atributo `name`
3. **Atribua novos IDs exclusivos** que não colidam com os IDs existentes
4. **Respeite a hierarquia de contêineres**: filhos de uma raia (`swimlane`) usam coordenadas relativas ao pai
5. **Verifique as arestas**: após reposicionar os nós, confirme se os IDs source/target das arestas continuam válidos

Use `scripts/add-shape.py` para adicionar com segurança uma única forma sem editar o XML bruto:

```bash
python .github/skills/draw-io-diagram-generator/scripts/add-shape.py docs/arch.drawio "Novo serviço" 700 380
```

---

## Práticas recomendadas

**Disposição**

- Alinhe as formas à grade de 10 px (todas as coordenadas divisíveis por 10)
- Agrupe formas relacionadas dentro de contêineres de raias (`swimlane`)
- Use um tópico de diagrama por página; use arquivos com várias páginas para sistemas complexos
- Mantenha 40 células ou menos por página para facilitar a leitura

**Rótulos**

- Adicione uma célula de texto de título (`text;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1`) no topo de cada página
- Sempre defina `whiteSpace=wrap;html=1` nas formas de vértice
- Mantenha os rótulos concisos, com três palavras ou menos por forma quando possível

**Consistência de estilo**

- Use de forma consistente em todo o projeto a paleta de cores semântica da etapa Aplicar os estilos corretos (Etapa 5)
- Prefira `edgeStyle=orthogonalEdgeStyle` para conectores limpos em ângulo reto
- Não insira HTML arbitrário em rótulos, salvo quando necessário

**Nomenclatura de arquivos**

- Use kebab-case: `order-service-flow.drawio`, `database-schema.drawio`
- Coloque os diagramas junto ao código que documentam: `docs/` ou `architecture/`

---

## Solução de problemas

| Problema | Causa provável | Correção |
|---|---|---|
| O arquivo abre em branco no VS Code | Célula id=0 ou id=1 ausente | Adicione as duas células-raiz antes das demais |
| A forma está na posição errada | Filho dentro de um contêiner; as coordenadas são relativas | Verifique `parent`; ajuste x/y em relação ao contêiner |
| A aresta não está visível | O ID source ou target não corresponde a nenhum vértice | Verifique se os dois IDs existem exatamente como escritos |
| O diagrama mostra "Compressed" ("Compactado") | mxGraphModel está codificado em base64 | Abra no aplicativo web do draw.io e use File > Export > XML (uncompressed), isto é, sem compactação |
| O estilo da forma não é renderizado | Erro de digitação no nome shape= | Consulte a string de estilo exata em `references/shape-libraries.md` |
| O rótulo mostra HTML escapado | html=0 em uma célula com rótulo HTML | Adicione `html=1;` ao estilo da célula |
| Os filhos do contêiner se sobrepõem à borda | A altura do contêiner é muito pequena | Aumente a altura do contêiner em mxGeometry |

---

## Modelo de saída

Entregue um arquivo `.drawio` completo e válido. O artefato mínimo e bem formado produzido por esta habilidade tem esta aparência:

```xml
<mxfile host="Electron" modified="2026-01-01T00:00:00.000Z" version="26.0.0">
  <diagram id="page-1" name="Visão geral">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827"
                  math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="title" value="Visão geral do sistema"
                style="text;html=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;"
                vertex="1" parent="1">
          <mxGeometry x="60" y="30" width="300" height="30" as="geometry" />
        </mxCell>
        <mxCell id="webapp" value="Aplicativo web"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
                vertex="1" parent="1">
          <mxGeometry x="80" y="100" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="api" value="Servidor de API"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
                vertex="1" parent="1">
          <mxGeometry x="320" y="100" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;html=1;"
                edge="1" source="webapp" target="api" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Junto ao arquivo, sempre forneça:

1. **Um resumo em uma frase** do que o diagrama mostra.
2. **Como abri-lo**:
   > "Abra `<filename>` no VS Code. A extensão draw.io o renderizará automaticamente. Se preferir, abra-o no aplicativo web ou desktop do draw.io."
3. **Como editá-lo** (se houver probabilidade de personalização):
   > "Clique em uma forma para selecioná-la. Clique duas vezes para editar o rótulo. Arraste para reposicionar."
4. **Status da validação**: informe se o programa validador foi executado e passou.

---

## Critérios de qualidade

Antes de entregar qualquer arquivo `.drawio` gerado, verifique:

- [ ] O arquivo começa com o elemento-raiz `<mxfile>`
- [ ] Cada `<diagram>` tem um atributo `id` não vazio
- [ ] `<mxCell id="0" />` é a primeira célula de cada diagrama
- [ ] `<mxCell id="1" parent="0" />` é a segunda célula de cada diagrama
- [ ] Todos os valores de `id` das células são exclusivos em cada diagrama
- [ ] Cada célula de vértice tem `vertex="1"` e um filho `<mxGeometry as="geometry">`
- [ ] Cada célula de aresta tem `edge="1"` e uma destas opções: (a) `source`/`target` apontando para IDs de vértices existentes; ou (b) `<mxPoint as="sourcePoint">` e `<mxPoint as="targetPoint">` em seu `<mxGeometry>` (aresta flutuante, usada para linhas de vida de diagramas de sequência)
- [ ] Cada célula (exceto id=0) tem um `parent` que aponta para um ID existente
- [ ] O estilo contém `html=1` para qualquer rótulo com tags HTML
- [ ] O XML está bem formado (sem tags abertas, nem `&`, `<`, `>` sem escape em valores de atributos)
- [ ] Existe uma célula de rótulo de título no topo de cada página

Execute o validador automatizado:

```bash
python .github/skills/draw-io-diagram-generator/scripts/validate-drawio.py <file.drawio>
```

---

## Referências

Todos os arquivos complementares estão em `.github/skills/draw-io-diagram-generator/`:

| Arquivo | Conteúdo |
|---|---|
| `references/drawio-xml-schema.md` | Referência completa de atributos mxfile / mxGraphModel / mxCell, sistema de coordenadas, células reservadas e regras de validação |
| `references/style-reference.md` | Todas as chaves de estilo com valores permitidos, chaves de estilo de vértices e arestas, catálogo de formas e paleta de cores semântica |
| `references/shape-libraries.md` | Todas as categorias de bibliotecas de formas (General, Flowchart, UML, ER, Network, BPMN, Mockup, K8s) com strings de estilo |
| `assets/templates/flowchart.drawio` | Modelo de fluxograma pronto para uso |
| `assets/templates/architecture.drawio` | Modelo de arquitetura de sistema com quatro camadas |
| `assets/templates/sequence.drawio` | Modelo de diagrama de sequência com três atores |
| `assets/templates/er-diagram.drawio` | Diagrama ER com três tabelas e relacionamentos em pé de galinha |
| `assets/templates/uml-class.drawio` | Interface + duas classes + enum com setas de relacionamento |
| `scripts/validate-drawio.py` | Programa em Python para validar a estrutura XML de qualquer arquivo .drawio |
| `scripts/add-shape.py` | Interface de linha de comando (CLI) em Python para adicionar uma nova forma a um diagrama existente |
| `scripts/README.md` | Como usar os programas auxiliares, com exemplos |
