# Referência de estilos do draw.io

Referência completa do atributo `style` em elementos `<mxCell>`. Os estilos são pares `key=value` delimitados por ponto e vírgula.

---

## Formato de estilo

```text
style="key1=value1;key2=value2;key3=value3;"
```

- Chaves e valores diferenciam maiúsculas de minúsculas
- O ponto e vírgula final é opcional, mas recomendado
- Chaves desconhecidas são ignoradas silenciosamente
- Chaves ausentes usam os padrões do draw.io

---

## Chaves de estilo universais

Aplicam-se a todas as formas e arestas.

| Chave | Valores | Padrão | Descrição |
| ----- | -------- | --------- | ------------- |
| `fillColor` | `#hex` / `none` | `#FFFFFF` | Cor de preenchimento da forma (padrão do draw.io; use a paleta semântica nos diagramas do projeto) |
| `strokeColor` | `#hex` / `none` | `#000000` | Cor da borda/linha (padrão do draw.io; use a paleta semântica nos diagramas do projeto) |
| `fontColor` | `#hex` | `#000000` | Cor do texto |
| `fontSize` | inteiro | `11` | Tamanho da fonte em pt |
| `fontStyle` | máscara de bits (veja abaixo) | `0` | Negrito/itálico/sublinhado |
| `fontFamily` | string | `Helvetica` | Nome da família da fonte |
| `align` | `left`/`center`/`right` | `center` | Alinhamento horizontal do texto |
| `verticalAlign` | `top`/`middle`/`bottom` | `middle` | Alinhamento vertical do texto |
| `opacity` | 0–100 | `100` | Opacidade da forma (%) |
| `shadow` | `0`/`1` | `0` | Sombra projetada |
| `dashed` | `0`/`1` | `0` | Borda tracejada |
| `dashPattern` | por exemplo, `8 8` | — | Padrão personalizado de traços/espaços (px) |
| `strokeWidth` | float | `2` | Largura da borda/linha em px |
| `spacing` | inteiro | `2` | Preenchimento ao redor do texto (px) |
| `spacingTop` | inteiro | `0` | Preenchimento superior do texto |
| `spacingBottom` | inteiro | `0` | Preenchimento inferior do texto |
| `spacingLeft` | inteiro | `4` | Preenchimento esquerdo do texto |
| `spacingRight` | inteiro | `4` | Preenchimento direito do texto |
| `html` | `0`/`1` | `0` | Permitir HTML no rótulo |
| `whiteSpace` | `wrap`/`nowrap` | `nowrap` | Quebra de linha do texto |
| `overflow` | `visible`/`hidden`/`fill` | `visible` | Comportamento de transbordamento do texto |
| `rotatable` | `0`/`1` | `1` | Permitir rotação no editor |
| `movable` | `0`/`1` | `1` | Permitir movimentação no editor |
| `resizable` | `0`/`1` | `1` | Permitir redimensionamento no editor |
| `deletable` | `0`/`1` | `1` | Permitir exclusão no editor |
| `editable` | `0`/`1` | `1` | Permitir edição do rótulo no editor |
| `locked` | `0`/`1` | `0` | Bloquear toda a edição |
| `nolabel` | `0`/`1` | `0` | Ocultar totalmente o rótulo |
| `noLabel` | `0`/`1` | `0` | Nome alternativo de `nolabel` |
| `labelPosition` | `left`/`center`/`right` | `center` | Âncora horizontal do rótulo |
| `verticalLabelPosition` | `top`/`middle`/`bottom` | `middle` | Âncora vertical do rótulo |
| `imageAlign` | `left`/`center`/`right` | `center` | Alinhamento da imagem |

### Valores da máscara de bits `fontStyle`

| Valor | Efeito |
| ------- | -------- |
| `0` | Normal |
| `1` | Negrito |
| `2` | Itálico |
| `4` | Sublinhado |
| `8` | Tachado |

Combine por adição: `3` = negrito + itálico, `5` = negrito + sublinhado, `7` = negrito + itálico + sublinhado.

---

## Chaves de forma (somente vértices)

| Chave | Valores | Descrição |
| ----- | -------- | ------------- |
| `shape` | consulte o Catálogo de formas | Substituir a forma-padrão de retângulo |
| `rounded` | `0`/`1` | Cantos arredondados no retângulo |
| `arcSize` | 0–50 | Percentual do raio dos cantos (quando `rounded=1`) |
| `perimeter` | nome da função | Tipo de perímetro da conexão |
| `aspect` | `fixed` | Bloquear a proporção ao redimensionar |
| `rotation` | float | Rotação em graus |
| `fixedSize` | `0`/`1` | Impedir tamanho automático ao editar o rótulo |
| `container` | `0`/`1` | Tratar a forma como contêiner dos filhos |
| `collapsible` | `0`/`1` | Permitir alternância entre recolher/expandir |
| `startSize` | inteiro | Tamanho do cabeçalho na raia (`swimlane`) ou no contêiner (px) |
| `swimlaneHead` | `0`/`1` | Exibir cabeçalho da raia (`swimlane`) |
| `swimlaneBody` | `0`/`1` | Exibir corpo da raia (`swimlane`) |
| `fillOpacity` | 0–100 | Opacidade somente do preenchimento (independente de `opacity`) |
| `strokeOpacity` | 0–100 | Opacidade somente do traço |
| `gradientColor` | `#hex` / `none` | Cor final do gradiente |
| `gradientDirection` | `north`/`south`/`east`/`west` | Direção do gradiente |
| `sketch` | `0`/`1` | Estilo de desenho à mão livre |
| `comic` | `0`/`1` | Estilo de linha de quadrinhos/desenho animado |
| `glass` | `0`/`1` | Efeito de reflexo em vidro |

---

## Catálogo de formas

### Formas básicas

| Forma | String de estilo | Visual |
| ------- | ------------- | -------- |
| Retângulo (padrão) | *(nenhuma chave shape necessária)* | □ |
| Retângulo arredondado | `rounded=1;` | ▢ |
| Elipse / Círculo | `ellipse;` | ○ |
| Losango | `rhombus;` | ◇ |
| Triângulo | `triangle;` | △ |
| Hexágono | `shape=hexagon;` | ⬡ |
| Pentágono | `shape=mxgraph.basic.pentagon;` | ⬠ |
| Estrela | `shape=mxgraph.basic.star;` | ★ |
| Cruz | `shape=mxgraph.basic.x;` | ✕ |
| Nuvem | `shape=cloud;` | ☁ |
| Nota / Chamada | `shape=note;folded=1;` | 📝 |
| Documento | `shape=document;` | 📄 |
| Cilindro (banco de dados) | `shape=cylinder3;` | 🗄 |
| Fita | `shape=tape;` | — |
| Paralelogramo | `shape=parallelogram;perimeter=parallelogramPerimeter;` | ▱ |

### Formas de fluxograma (`mxgraph.flowchart.*`)

| Forma | String de estilo | Uso |
| ------- | ------------- | ---------- |
| Processo | `shape=mxgraph.flowchart.process;` | Processo padrão |
| Início/Fim (terminal) | `ellipse;` ou `shape=mxgraph.flowchart.terminate;` | Início/fim do fluxo |
| Decisão | `rhombus;` | Ramificação Sim/Não |
| Dados (E/S) | `shape=mxgraph.flowchart.io;` | Entrada/Saída |
| Processo predefinido | `shape=mxgraph.flowchart.predefined_process;` | Sub-rotina |
| Entrada manual | `shape=mxgraph.flowchart.manual_input;` | Entrada manual |
| Operação manual | `shape=mxgraph.flowchart.manual_operation;` | Etapa manual |
| Banco de dados | `shape=mxgraph.flowchart.database;` | Armazenamento de dados |
| Armazenamento interno | `shape=mxgraph.flowchart.internal_storage;` | Dados internos |
| Dados diretos | `shape=mxgraph.flowchart.direct_data;` | Armazenamento em tambor |
| Documento | `shape=mxgraph.flowchart.document;` | Documento |
| Vários documentos | `shape=mxgraph.flowchart.multi-document;` | Vários documentos |
| Conector na página | `ellipse;` (pequeno) | Conector de página |
| Conector fora da página | `shape=mxgraph.flowchart.off_page_connector;` | Referência fora da página |
| Preparação | `shape=mxgraph.flowchart.preparation;` | Inicialização |
| Atraso | `shape=mxgraph.flowchart.delay;` | Estado de espera |
| Exibição | `shape=mxgraph.flowchart.display;` | Exibição da saída |
| Ordenação | `shape=mxgraph.flowchart.sort;` | Operação de ordenação |
| Extração | `shape=mxgraph.flowchart.extract;` | Operação de extração |
| Mesclagem | `shape=mxgraph.flowchart.merge;` | Mesclar caminhos |
| Ou | `shape=mxgraph.flowchart.or;` | Porta OR |
| E | `shape=mxgraph.flowchart.and;` | Porta AND |
| Anotação | `shape=mxgraph.flowchart.annotation;` | Comentário/nota |

### Formas UML (`mxgraph.uml.*`)

| Forma | String de estilo | Uso |
| ------- | ------------- | ---------- |
| Ator | `shape=mxgraph.uml.actor;` | Ator de caso de uso |
| Limite | `shape=mxgraph.uml.boundary;` | Limite do sistema |
| Controle | `shape=mxgraph.uml.control;` | Objeto controlador |
| Entidade | `shape=mxgraph.uml.entity;` | Objeto de entidade |
| Componente | `shape=component;` | Caixa de componente |
| Pacote | `shape=mxgraph.uml.package;` | Pacote |
| Nota | `shape=note;` | Nota UML |
| Linha de vida | `shape=umlLifeline;startSize=40;` | Linha de vida da sequência |
| Ativação | `shape=umlActivation;` | Caixa de ativação |
| Destruir | `shape=mxgraph.uml.destroy;` | Marcador de destruição |
| Estado | `ellipse;` | Nó de estado |
| Estado inicial | `ellipse;fillColor=#000000;` | Estado inicial UML |
| Estado final | `shape=doubleEllipse;fillColor=#000000;` | Estado final UML |
| Bifurcação/Junção | `shape=mxgraph.uml.fork_or_join;` | Barra de bifurcação/junção |

### Formas de rede (`mxgraph.network.*`)

| Forma | String de estilo |
| ------- | ------------- |
| Servidor | `shape=server;` |
| Servidor de banco de dados | `shape=mxgraph.network.database;` |
| Firewall | `shape=mxgraph.cisco.firewalls.firewall;` |
| Roteador | `shape=mxgraph.cisco.routers.router;` |
| Comutador | `shape=mxgraph.cisco.switches.workgroup_switch;` |
| Nuvem | `shape=cloud;` |
| Internet | `shape=mxgraph.network.internet;` |
| Notebook | `shape=mxgraph.network.laptop;` |
| Computador | `shape=mxgraph.network.desktop;` |
| Dispositivo móvel | `shape=mxgraph.network.mobile;` |

### Formas AWS (`mxgraph.aws4.*`)

Use a biblioteca AWS4. Formas comuns:

| Forma | String de estilo |
| ------- | ------------- |
| EC2 | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;` |
| Lambda | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;` |
| S3 | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;` |
| RDS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;` |
| API Gateway | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;` |
| CloudFront | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudfront;` |
| Load Balancer | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.elb;` |
| SQS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;` |
| SNS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;` |
| DynamoDB | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;` |
| ECS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;` |
| EKS | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eks;` |
| VPC | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;` |
| Region | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;` |

### Formas do Azure (`mxgraph.azure.*`)

| Forma | String de estilo |
| ------- | ------------- |
| App Service | `shape=mxgraph.azure.app_service;` |
| Function App | `shape=mxgraph.azure.function_apps;` |
| SQL Database | `shape=mxgraph.azure.sql_database;` |
| Blob Storage | `shape=mxgraph.azure.blob_storage;` |
| API Management | `shape=mxgraph.azure.api_management;` |
| Service Bus | `shape=mxgraph.azure.service_bus;` |
| AKS | `shape=mxgraph.azure.aks;` |
| Container Registry | `shape=mxgraph.azure.container_registry_registries;` |

### Formas do GCP (`mxgraph.gcp2.*`)

| Forma | String de estilo |
| ------- | ------------- |
| Cloud Run | `shape=mxgraph.gcp2.cloud_run;` |
| Cloud Functions | `shape=mxgraph.gcp2.cloud_functions;` |
| Cloud SQL | `shape=mxgraph.gcp2.cloud_sql;` |
| Cloud Storage | `shape=mxgraph.gcp2.cloud_storage;` |
| GKE | `shape=mxgraph.gcp2.container_engine;` |
| Pub/Sub | `shape=mxgraph.gcp2.cloud_pubsub;` |
| BigQuery | `shape=mxgraph.gcp2.bigquery;` |

---

## Chaves de estilo de aresta

| Chave | Valores | Descrição |
| ----- | -------- | ------------- |
| `edgeStyle` | veja abaixo | Algoritmo de roteamento da conexão |
| `rounded` | `0`/`1` | Cantos arredondados em arestas ortogonais |
| `curved` | `0`/`1` | Segmentos de linha curvos |
| `orthogonal` | `0`/`1` | Forçar roteamento ortogonal |
| `jettySize` | `auto`/inteiro | Tamanho da projeção de origem/destino |
| `exitX` | 0.0–1.0 | Ponto X de saída da origem (0=esquerda, 0.5=centro, 1=direita) |
| `exitY` | 0.0–1.0 | Ponto Y de saída da origem (0=topo, 0.5=centro, 1=base) |
| `exitDx` | float | Deslocamento X da saída da origem (px) |
| `exitDy` | float | Deslocamento Y da saída da origem (px) |
| `entryX` | 0.0–1.0 | Ponto X de entrada do destino |
| `entryY` | 0.0–1.0 | Ponto Y de entrada do destino |
| `entryDx` | float | Deslocamento X da entrada do destino (px) |
| `entryDy` | float | Deslocamento Y da entrada do destino (px) |
| `endArrow` | consulte Tipos de seta | Ponta da seta no destino |
| `startArrow` | consulte Tipos de seta | Cauda da seta na origem |
| `endFill` | `0`/`1` | Ponta final da seta preenchida |
| `startFill` | `0`/`1` | Ponta inicial da seta preenchida |
| `endSize` | inteiro | Tamanho da ponta final da seta (px) |
| `startSize` | inteiro | Tamanho da ponta inicial da seta (px) |
| `labelBackgroundColor` | `#hex`/`none` | Preenchimento do fundo do rótulo |
| `labelBorderColor` | `#hex`/`none` | Cor da borda do rótulo |

### Valores de `edgeStyle`

| Valor | Roteamento | Quando usar |
| ------- | --------- | ---------- |
| `none` | Linha reta | Conexões diretas simples |
| `orthogonalEdgeStyle` | Curvas em ângulo reto | Fluxogramas, arquitetura |
| `elbowEdgeStyle` | Um único cotovelo | Diagramas direcionais limpos |
| `entityRelationEdgeStyle` | Roteamento no estilo ER | Diagramas ER |
| `segmentEdgeStyle` | Segmentado com alças | Roteamento com ajuste fino |
| `isometricEdgeStyle` | Grade isométrica | Diagramas isométricos |

### Tipos de seta (`endArrow` / `startArrow`)

| Valor | Forma | Uso |
| ------- | ------- | --------- |
| `block` | Triângulo preenchido | Seta direcionada padrão |
| `open` | Ponta aberta em V → | Seta aberta/leve |
| `classic` | Seta clássica | Seta-padrão do draw.io |
| `classicThin` | Clássica fina | Diagramas compactos |
| `none` | Sem ponta de seta | Linhas não direcionadas |
| `oval` | Ponto circular | Início de agregação |
| `diamond` | Losango vazado | Agregação |
| `diamondThin` | Losango fino | Diagramas estreitos |
| `ERone` | barra `\|` | Cardinalidade ER "um" |
| `ERmany` | Pé de galinha | Cardinalidade ER "muitos" |
| `ERmandOne` | `\|\|` | Um obrigatório em ER |
| `ERzeroToOne` | `o\|` | Zero ou um em ER |
| `ERzeroToMany` | `o<` | Zero ou muitos em ER |
| `ERoneToMany` | `\|<` | Um ou muitos em ER |

---

## Paleta de cores

### Cores semânticas (recomendadas para diagramas consistentes)

| Significado | Preenchimento | Traço | Uso |
| --------- | ------ | -------- | ------- |
| Pessoa usuária / Cliente | `#dae8fc` | `#6c8ebf` | Navegador, aplicativos cliente |
| Serviço / Processo | `#d5e8d4` | `#82b366` | Serviços do lado do servidor |
| Banco de dados / Armazenamento | `#f5f5f5` | `#666666` | Bancos de dados, arquivos |
| Decisão / Aviso | `#fff2cc` | `#d6b656` | Nós de decisão, alertas |
| Erro / Crítico | `#f8cecc` | `#b85450` | Caminhos de erro, pontos críticos |
| Externo / Parceiro | `#e1d5e7` | `#9673a6` | Terceiros, externos |
| Fila / Assíncrono | `#ffe6cc` | `#d79b00` | Filas de mensagens |
| Ponto de entrada / Intermediário (`proxy`) | `#dae8fc` | `#0050ef` | Pontos de entrada de API e intermediários (`proxies`) |

### Formas com fundo escuro

Para diagramas com tema escuro, use:

- Preenchimento: `#1e4d78` (azul-escuro), `#1a4731` (verde-escuro)
- Traço: `#4aa3df`, `#67ab9f`
- Fonte: `#ffffff`

---

## Exemplos completos de estilo

### Caixa azul arredondada

```text
rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
```

### Etapa de processo verde

```text
rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;
```

### Losango de decisão amarelo

```text
rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;
```

### Caixa de erro vermelha

```text
rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;
```

### Cilindro de banco de dados

```text
shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#f5f5f5;strokeColor=#666666;
```

### Contêiner de raias (`swimlane`)

```text
shape=pool;startSize=30;horizontal=1;fillColor=#f5f5f5;strokeColor=#999999;
```

### Raia (`swimlane`)

```text
swimlane;startSize=30;fillColor=#ffffff;strokeColor=#999999;
```

### Conector ortogonal

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;
```

### Seta direcionada (grossa)

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeWidth=2;
```

### Linha de dependência tracejada

```text
edgeStyle=orthogonalEdgeStyle;dashed=1;endArrow=open;endFill=0;strokeColor=#666666;
```

### Linha de relacionamento ER (um para muitos)

```text
edgeStyle=entityRelationEdgeStyle;html=1;endArrow=ERmany;startArrow=ERmandOne;endFill=1;startFill=1;
```

### Seta de herança UML (triângulo vazado)

```text
edgeStyle=orthogonalEdgeStyle;html=1;endArrow=block;endFill=0;
```

### Composição UML (losango preenchido)

```text
edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=1;endArrow=none;
```

### Agregação UML (losango aberto)

```text
edgeStyle=orthogonalEdgeStyle;html=1;startArrow=diamond;startFill=0;endArrow=none;
```

### Dependência UML (seta tracejada)

```text
edgeStyle=orthogonalEdgeStyle;dashed=1;html=1;endArrow=open;endFill=0;
```

### Conector invisível (para alinhamento)

```text
edgeStyle=none;strokeColor=none;endArrow=none;
```
