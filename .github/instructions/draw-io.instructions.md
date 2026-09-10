---
description: "Use ao criar, editar ou revisar diagramas draw.io e XML mxGraph em arquivos .drawio, .drawio.svg ou .drawio.png."
applyTo: "**/*.drawio,**/*.drawio.svg,**/*.drawio.png"
---

# Diagramas draw.io — Convenções e restrições

Este arquivo é ativado quando você abre ou edita um arquivo `.drawio`, `.drawio.svg` ou `.drawio.png`. Ele define as restrições de estrutura, estilo e nomenclatura que todo diagrama deste repositório deve cumprir para ser renderizado na primeira tentativa no VS Code com a extensão `hediet.vscode-drawio` e permanecer consistente em todo o kit. Ele ensina as invariantes que um arquivo de diagrama deve manter, mas não apresenta o passo a passo de construção. O procedimento de autoria, as receitas XML por tipo, os modelos e o script de validação ficam na [skill `draw-io-diagram-generator`](../skills/draw-io-diagram-generator/SKILL.md). Leia-a antes de gerar ou reestruturar um diagrama e não duplique suas etapas aqui.

## Invariantes de estrutura

Estas invariantes são inegociáveis; um diagrama que viola qualquer uma delas é renderizado em branco ou corrompido.

- `id="0"` e `id="1"` são as **duas primeiras células** de todo `<diagram>`, nessa ordem, e nunca são reutilizadas para conteúdo.
- Todo `id` de célula é **exclusivo dentro da página do diagrama** (os IDs podem se repetir em páginas distintas).
- Todo vértice (`vertex="1"`) possui um filho `<mxGeometry ... as="geometry">` com `x`, `y`, `width` e `height`.
- Toda aresta (`edge="1"`) aponta `source`/`target` para IDs de vértices existentes **ou**, em arestas flutuantes como linhas de vida de diagramas de sequência, contém `<mxPoint as="sourcePoint">` e `<mxPoint as="targetPoint">` dentro de `<mxGeometry>`.
- Toda célula, exceto `id="0"`, possui um `parent` que resolve para um ID existente.
- Os filhos de um contêiner (swimlane, tabela) usam coordenadas **relativas ao pai**, não ao canvas.

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  <!-- toda outra célula define parent como um ID existente -->
</root>
```

> [!WARNING]
> Um arquivo que abre em branco no VS Code quase sempre não possui as células raiz `id="0"`/`id="1"` ou contém uma aresta cujo ID `source`/`target` não resolve. Verifique primeiro essas duas invariantes.

## Paleta de cores semântica

Use uma única paleta em todo o repositório para que a cor de uma forma sempre tenha o mesmo significado. `fillColor` forma par com seu `strokeColor` correspondente.

| Papel | fillColor | strokeColor |
|---|---|---|
| Primário / informação (padrão) | `#dae8fc` | `#6c8ebf` |
| Sucesso / início / positivo | `#d5e8d4` | `#82b366` |
| Alerta / decisão | `#fff2cc` | `#d6b656` |
| Erro / fim / perigo | `#f8cecc` | `#b85450` |
| Neutro / interface | `#f5f5f5` | `#666666` |
| Externo / parceiro | `#e1d5e7` | `#9673a6` |

## Convenções de arquivo, nomenclatura e layout

| Aspecto | Convenção |
|---|---|
| Extensão | `.drawio` para diagramas versionados; `.drawio.svg` quando o arquivo for incorporado em Markdown |
| Nome do arquivo | `kebab-case`, por exemplo, `payment-flow.drawio`, `database-schema.drawio` |
| Local | Ao lado do código documentado pelo diagrama, em `docs/` ou `architecture/` |
| Grade | Alinhe todas as coordenadas à grade de 10 px (valores divisíveis por 10) |
| Espaçamento | 40–60 px entre formas da mesma linha; 80–120 px entre linhas de camadas |
| Tamanho da página | A4 horizontal padrão, `1169 × 827` px |
| Densidade | No máximo 40 células por página; divida sistemas maiores em várias páginas `<diagram>` |
| Título | Adicione uma célula de texto de título no início de cada página |

## Validação

Antes do commit, execute o verificador `validate-drawio.py` documentado na [skill `draw-io-diagram-generator`](../skills/draw-io-diagram-generator/SKILL.md). Depois, abra o arquivo no VS Code para confirmar a renderização. A skill detém a invocação exata e a tabela de solução de problemas; este arquivo detém as invariantes impostas pelo verificador.

## Convenções

| Regra | Justificativa |
|---|---|
| `id="0"` e `id="1"` são as duas primeiras células de cada página | O draw.io as trata como raiz reservada; sem elas, o arquivo não é renderizado |
| Todo estilo de vértice inclui `whiteSpace=wrap;html=1` | Os rótulos quebram linhas e renderizam HTML de modo consistente, sem transbordar |
| Os conectores usam `edgeStyle=orthogonalEdgeStyle` | O roteamento limpo em ângulos retos mantém os diagramas legíveis |
| A paleta de cores semântica é usada de modo consistente | Uma cor possui o mesmo significado em todo diagrama |
| Os nomes dos arquivos de diagrama usam `kebab-case` e ficam ao lado do código | Os diagramas são fáceis de encontrar e comparar no controle de versão |
| As etapas e receitas de autoria ficam na skill, não aqui | Uma única fonte de procedimento evita desvios entre duas cópias |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Coloque primeiro `id="0"` e `id="1"` e depois as células de conteúdo | Reutilize `0` ou `1` em uma forma ou omita-os |
| Aponte toda aresta para IDs de vértices existentes ou use pontos flutuantes | Deixe `source`/`target` de uma aresta pendente |
| Reutilize a paleta de cores semântica | Invente cores ad hoc para cada diagrama |
| Aponte para a skill no fluxo de autoria | Copie para este arquivo as receitas passo a passo da skill |
| Mantenha as coordenadas dos filhos relativas ao contêiner | Use coordenadas do canvas em células dentro de uma swimlane |
| Divida um diagrama denso entre páginas | Comprima mais de 40 células em uma página |

## Lista de verificação antes de abrir uma PR

- [ ] `<mxCell id="0" />` e `<mxCell id="1" parent="0" />` são as duas primeiras células de toda página
- [ ] Todos os IDs de células são exclusivos dentro do diagrama, e todo `parent` resolve
- [ ] Todo `source`/`target` de aresta resolve, ou a aresta usa `sourcePoint`/`targetPoint`
- [ ] Todo vértice possui `<mxGeometry as="geometry">`, e os filhos dos contêineres usam coordenadas relativas
- [ ] A paleta de cores semântica e o estilo de vértice `whiteSpace=wrap;html=1` são aplicados de modo consistente
- [ ] O arquivo usa `kebab-case`, fica em `docs/` ou `architecture/` e possui uma célula de título por página
- [ ] O verificador `validate-drawio.py` da skill passa, e o arquivo é renderizado no VS Code
