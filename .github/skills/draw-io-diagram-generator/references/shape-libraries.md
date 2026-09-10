# Bibliotecas de formas do draw.io

Guia de referência para todas as bibliotecas de formas integradas. Habilite-as em `View > Shapes` ("Exibir > Formas") no editor draw.io ou no painel de formas da extensão do VS Code.

---

## Catálogo de bibliotecas

### Geral

**Habilitação**: sempre ativa por padrão

Formas comuns para qualquer tipo de diagrama.

| Forma | Chave de estilo | Uso |
| ------- | ----------- | --------- |
| Retângulo | *(padrão)* | Caixas, etapas, componentes |
| Retângulo arredondado | `rounded=1;` | Caixas de processo mais suaves |
| Elipse | `ellipse;` | Estados, início/fim |
| Triângulo | `triangle;` | Setas, portas |
| Losango | `rhombus;` | Decisões |
| Hexágono | `shape=hexagon;` | Rótulos, ícones técnicos |
| Nuvem | `shape=cloud;` | Serviços de nuvem |
| Cilindro | `shape=cylinder3;` | Bancos de dados |
| Nota | `shape=note;` | Anotações |
| Documento | `shape=document;` | Arquivos |
| Formas de seta | Vários `mxgraph.arrows2.*` | Direções do fluxo |
| Chamadas | `shape=callout;` | Balões de fala |

---

### Fluxograma

**Habilitação**: `View > Shapes > Flowchart`
**Prefixo da forma**: `mxgraph.flowchart.`

Símbolos-padrão de fluxograma ANSI/ISO.

| Símbolo | String de estilo | Nome ANSI |
| -------- | ------------- | ----------- |
| Início / Fim | `ellipse;` | Terminal |
| Processo (retângulo) | `rounded=1;` | Processo |
| Decisão | `rhombus;` | Decisão |
| E/S (paralelogramo) | `shape=mxgraph.flowchart.io;` | Dados |
| Processo predefinido | `shape=mxgraph.flowchart.predefined_process;` | Processo predefinido |
| Operação manual | `shape=mxgraph.flowchart.manual_operation;` | Operação manual |
| Entrada manual | `shape=mxgraph.flowchart.manual_input;` | Entrada manual |
| Banco de dados | `shape=mxgraph.flowchart.database;` | Armazenamento de acesso direto |
| Documento | `shape=mxgraph.flowchart.document;` | Documento |
| Vários documentos | `shape=mxgraph.flowchart.multi-document;` | Vários documentos |
| Conector na página | `ellipse;` (pequeno, 30×30) | Conector |
| Conector fora da página | `shape=mxgraph.flowchart.off_page_connector;` | Conector fora da página |
| Preparação | `shape=mxgraph.flowchart.preparation;` | Preparação |
| Atraso | `shape=mxgraph.flowchart.delay;` | Atraso |
| Exibição | `shape=mxgraph.flowchart.display;` | Exibição |
| Armazenamento interno | `shape=mxgraph.flowchart.internal_storage;` | Armazenamento interno |
| Ordenação | `shape=mxgraph.flowchart.sort;` | Ordenação |
| Extração | `shape=mxgraph.flowchart.extract;` | Extração |
| Mesclagem | `shape=mxgraph.flowchart.merge;` | Mesclagem |
| Ou | `shape=mxgraph.flowchart.or;` | Ou |
| Anotação | `shape=mxgraph.flowchart.annotation;` | Anotação |
| Cartão | `shape=mxgraph.flowchart.card;` | Cartão perfurado |

**Strings de estilo completas de exemplo para fluxogramas:**

```text
Processo:         rounded=1;whiteSpace=wrap;html=1;
Decisão:          rhombus;whiteSpace=wrap;html=1;
Início/Fim:       ellipse;whiteSpace=wrap;html=1;
Banco de dados:   shape=mxgraph.flowchart.database;whiteSpace=wrap;html=1;
Documento:        shape=mxgraph.flowchart.document;whiteSpace=wrap;html=1;
E/S (Dados):      shape=mxgraph.flowchart.io;whiteSpace=wrap;html=1;
```

---

### UML

**Habilitação**: `View > Shapes > UML`

#### Diagramas de caso de uso

| Forma | String de estilo |
| ------- | ------------- |
| Ator | `shape=mxgraph.uml.actor;whiteSpace=wrap;html=1;` |
| Caso de uso (elipse) | `ellipse;whiteSpace=wrap;html=1;` |
| Limite do sistema | `swimlane;startSize=30;whiteSpace=wrap;html=1;` |

#### Diagramas de classes

Use contêineres de raias (`swimlane`) para caixas de classe:

```xml
<!-- Contêiner da classe -->
<mxCell value="«interface»&#xa;IOrderService"
        style="swimlane;fontStyle=1;align=center;startSize=30;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="200" height="160" as="geometry" />
</mxCell>

<!-- Atributos (filhos da classe) -->
<mxCell value="+ id: string&#xa;+ status: string"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;overflow=hidden;html=1;"
        vertex="1" parent="classId">
  <mxGeometry y="30" width="200" height="60" as="geometry" />
</mxCell>

<!-- Linha separadora dos métodos -->
<mxCell value="" style="line;strokeWidth=1;fillColor=none;" vertex="1" parent="classId">
  <mxGeometry y="90" width="200" height="10" as="geometry" />
</mxCell>

<!-- Métodos (filhos da classe) -->
<mxCell value="+ create(): Order&#xa;+ cancel(): void"
        style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;overflow=hidden;html=1;"
        vertex="1" parent="classId">
  <mxGeometry y="100" width="200" height="60" as="geometry" />
</mxCell>
```

#### Setas de relacionamento UML

| Relacionamento | String de estilo |
| ------------- | ------------- |
| Herança (extends) | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=0;` |
| Implementação (implements) | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=block;endFill=0;` |
| Associação | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=open;endFill=0;` |
| Dependência | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=open;endFill=0;` |
| Agregação | `edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=0;endArrow=none;` |
| Composição | `edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=1;endArrow=none;` |

#### Diagrama de componentes

| Forma | String de estilo |
| ------- | ------------- |
| Componente | `shape=component;align=left;spacingLeft=36;whiteSpace=wrap;html=1;` |
| Interface (pirulito) | `ellipse;whiteSpace=wrap;html=1;aspect=fixed;` (círculo pequeno) |
| Porta | `shape=mxgraph.uml.port;` |
| Nó | `shape=mxgraph.uml.node;whiteSpace=wrap;html=1;` |
| Artefato | `shape=mxgraph.uml.artifact;whiteSpace=wrap;html=1;` |

#### Diagramas de sequência

| Forma | String de estilo |
| ------- | ------------- |
| Ator | `shape=mxgraph.uml.actor;whiteSpace=wrap;html=1;` |
| Linha de vida (objeto) | `shape=umlLifeline;startSize=40;whiteSpace=wrap;html=1;` |
| Caixa de ativação | `shape=umlActivation;whiteSpace=wrap;html=1;` |
| Mensagem síncrona | `edgeStyle=elbowEdgeStyle;elbow=vertical;html=1;endArrow=block;endFill=1;` |
| Mensagem assíncrona | `edgeStyle=elbowEdgeStyle;elbow=vertical;html=1;endArrow=open;endFill=0;` |
| Retorno | `edgeStyle=elbowEdgeStyle;elbow=vertical;dashed=1;html=1;endArrow=open;endFill=0;` |
| Autochamada | `edgeStyle=elbowEdgeStyle;elbow=vertical;exitX=1;exitY=0.3;entryX=1;entryY=0.5;html=1;` |

#### Diagramas de estados

| Forma | String de estilo |
| ------- | ------------- |
| Estado inicial (círculo sólido) | `ellipse;html=1;aspect=fixed;fillColor=#000000;strokeColor=#000000;` |
| Estado | `rounded=1;whiteSpace=wrap;html=1;arcSize=50;` |
| Estado final | `shape=doubleEllipse;fillColor=#000000;strokeColor=#000000;` |
| Transição | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=1;` |
| Bifurcação/Junção | `shape=mxgraph.uml.fork_or_join;html=1;fillColor=#000000;` |

---

### Entidade-relacionamento (diagramas ER)

**Habilitação**: `View > Shapes > Entity Relation`

#### Tabelas ER modernas (notação pé de galinha)

```xml
<!-- Contêiner da tabela -->
<mxCell id="tbl-orders" value="orders"
        style="shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="80" y="80" width="240" height="210" as="geometry" />
</mxCell>

<!-- Linha da coluna -->
<mxCell id="col-id" value=""
        style="shape=tableRow;horizontal=0;startSize=0;swimmilaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
        vertex="1" parent="tbl-orders">
  <mxGeometry y="30" width="240" height="30" as="geometry" />
</mxCell>

<!-- Célula do marcador PK -->
<mxCell value="PK" style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;fontStyle=1;overflow=hidden;"
        vertex="1" parent="col-id">
  <mxGeometry width="40" height="30" as="geometry" />
</mxCell>

<!-- Célula do nome da coluna -->
<mxCell value="id" style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;"
        vertex="1" parent="col-id">
  <mxGeometry x="40" width="140" height="30" as="geometry" />
</mxCell>

<!-- Célula do tipo de dados -->
<mxCell value="UUID" style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontStyle=2;"
        vertex="1" parent="col-id">
  <mxGeometry x="180" width="60" height="30" as="geometry" />
</mxCell>
```

#### Conectores de relacionamento ER (pé de galinha)

| Cardinalidade | String de estilo |
| ------------- | ------------- |
| Um para um | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERmandOne;startFill=1;endFill=1;` |
| Um para muitos | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERmany;startFill=1;endFill=1;` |
| Zero para muitos | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERzeroToMany;startFill=1;endFill=0;` |
| Zero para um | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERzeroToOne;startFill=1;endFill=0;` |
| Muitos para muitos | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmany;endArrow=ERmany;startFill=1;endFill=1;` |

---

### Rede / Infraestrutura

**Habilitação**: `View > Shapes > Networking`

| Forma | String de estilo |
| ------- | ------------- |
| Servidor genérico | `shape=server;html=1;whiteSpace=wrap;` |
| Servidor web | `shape=mxgraph.network.web_server;` |
| Servidor de banco de dados | `shape=mxgraph.network.database;` |
| Notebook | `shape=mxgraph.network.laptop;` |
| Computador | `shape=mxgraph.network.desktop;` |
| Telefone celular | `shape=mxgraph.network.mobile;` |
| Roteador | `shape=mxgraph.cisco.routers.router;` |
| Comutador | `shape=mxgraph.cisco.switches.workgroup_switch;` |
| Barreira de rede (`firewall`) | `shape=mxgraph.cisco.firewalls.firewall;` |
| Nuvem (genérica) | `shape=cloud;` |
| Internet | `shape=mxgraph.network.internet;` |
| Balanceador de carga | `shape=mxgraph.network.load_balancer;` |

---

### BPMN 2.0

**Habilitação**: `View > Shapes > BPMN`
**Prefixo da forma**: `shape=mxgraph.bpmn.*`

| Forma | String de estilo |
| ------- | ------------- |
| Evento inicial | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.ellipsePerimeter;symbol=general;verticalLabelPosition=bottom;` |
| Evento final | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.ellipsePerimeter;symbol=terminate;verticalLabelPosition=bottom;` |
| Tarefa | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.rectanglePerimeter;symbol=task;` |
| Gateway exclusivo | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.rhombusPerimeter;symbol=exclusiveGw;` |
| Gateway paralelo | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.rhombusPerimeter;symbol=parallelGw;` |
| Subprocesso | `shape=mxgraph.bpmn.shape;perimeter=mxPerimeter.rectanglePerimeter;symbol=subProcess;` |
| Fluxo de sequência | `edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=1;` |
| Fluxo de mensagens | `edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=block;endFill=0;` |
| Grupo de participantes (`Pool`) | `shape=pool;startSize=30;horizontal=1;` |
| Raia | `swimlane;startSize=30;` |

---

### Mockup / Wireframe

**Habilitação**: `View > Shapes > Mockup`

| Forma | String de estilo |
| ------- | ------------- |
| Botão | `shape=mxgraph.mockup.forms.button;` |
| Campo de entrada | `shape=mxgraph.mockup.forms.text1;` |
| Caixa de seleção | `shape=mxgraph.mockup.forms.checkbox;` |
| Lista suspensa | `shape=mxgraph.mockup.forms.comboBox;` |
| Janela do navegador | `shape=mxgraph.mockup.containers.browser;` |
| Tela de dispositivo móvel | `shape=mxgraph.mockup.containers.smartphone;` |
| Lista | `shape=mxgraph.mockup.containers.list;` |
| Tabela | `shape=mxgraph.mockup.containers.table;` |

---

### Kubernetes

**Habilitação**: `View > Shapes > Kubernetes`

| Recurso | String de estilo |
| ---------- | ------------- |
| Pod | `shape=mxgraph.kubernetes.pod;` |
| Deployment | `shape=mxgraph.kubernetes.deploy;` |
| Service | `shape=mxgraph.kubernetes.svc;` |
| Ingress | `shape=mxgraph.kubernetes.ing;` |
| ConfigMap | `shape=mxgraph.kubernetes.cm;` |
| Secret | `shape=mxgraph.kubernetes.secret;` |
| PersistentVolume | `shape=mxgraph.kubernetes.pv;` |
| Namespace | `shape=mxgraph.kubernetes.ns;` |
| Node | `shape=mxgraph.kubernetes.node;` |

---

## Habilitar bibliotecas no VS Code

As bibliotecas são habilitadas no editor draw.io (incorporado pelo VS Code):

1. Abra qualquer arquivo `.drawio` ou `.drawio.svg` no VS Code
2. Clique no ícone `+` no painel de formas (barra lateral esquerda) → `Search Shapes` ("Pesquisar formas") ou `More Shapes` ("Mais formas")
3. Marque a biblioteca que deseja ativar
4. As formas aparecem no painel para arrastar e soltar

As bibliotecas são armazenadas por pessoa nas configurações do draw.io (não por projeto).

---

## Criar uma biblioteca de formas personalizada

Uma biblioteca personalizada é um arquivo XML com extensão `.xml`, carregado por `File > Open Library` ("Arquivo > Abrir biblioteca"):

```xml
<mxlibrary>
  [
    {
      "xml": "&lt;mxCell value=\"Componente\" style=\"rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;\" vertex=\"1\"&gt;&lt;mxGeometry width=\"120\" height=\"60\" as=\"geometry\" /&gt;&lt;/mxCell&gt;",
      "w": 120,
      "h": 60,
      "aspect": "fixed",
      "title": "Meu componente"
    }
  ]
</mxlibrary>
```

Cada entrada de forma contém:

- `xml`: definição de célula com escapes XML
- `w` / `h`: largura/altura padrão
- `aspect`: `"fixed"` para bloquear a proporção
- `title`: nome exibido no painel
