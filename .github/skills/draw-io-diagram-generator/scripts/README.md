# Programas auxiliares do draw.io

Programas auxiliares para trabalhar com arquivos de diagrama `.drawio` no projeto cxp-bu-order-ms.

## Requisitos

- Python 3.8+
- Sem dependências externas (usa somente a biblioteca padrão: `xml.etree.ElementTree`, `argparse`, `json`, `sys`, `pathlib`)

## Programas

### `validate-drawio.py`

Valida a estrutura XML de um arquivo `.drawio` conforme as restrições obrigatórias.

**Uso**

```bash
python scripts/validate-drawio.py <path-to-diagram.drawio>
```

**Exemplos**

```bash
# Validar um único arquivo
python scripts/validate-drawio.py docs/architecture.drawio

# Validar todos os arquivos drawio de um diretório
for f in docs/**/*.drawio; do python scripts/validate-drawio.py "$f"; done
```

**Verificações realizadas**

| Verificação | Descrição |
|-------|-------------|
| Células-raiz | Verifica se as células id="0" e id="1" estão presentes em cada página do diagrama |
| IDs exclusivos | Todos os valores de id de `mxCell` são exclusivos no diagrama |
| Conectividade das arestas | Cada aresta tem atributos `source` e `target` válidos que apontam para células existentes |
| Geometria | Cada célula de vértice tem um elemento filho `mxGeometry` |
| Cadeia de pais | O atributo `parent` de cada célula referencia um ID de célula existente |
| Boa formação do XML | O arquivo é um XML válido |

**Códigos de saída**

- `0`: validação aprovada
- `1`: um ou mais erros de validação encontrados (erros impressos na saída padrão, `stdout`)

---

### `add-shape.py`

Adiciona uma nova forma (célula de vértice) a um arquivo de diagrama `.drawio` existente.

**Uso**

```bash
python scripts/add-shape.py <diagram.drawio> <label> <x> <y> [options]
```

**Argumentos**

| Argumento | Obrigatório | Descrição |
|----------|----------|-------------|
| `diagram` | Sim | Caminho do arquivo `.drawio` |
| `label` | Sim | Rótulo de texto da nova forma |
| `x` | Sim | Coordenada X (pixels a partir do canto superior esquerdo) |
| `y` | Sim | Coordenada Y (pixels a partir do canto superior esquerdo) |

**Opções**

| Opção | Padrão | Descrição |
|--------|---------|-------------|
| `--width` | `120` | Largura da forma em pixels |
| `--height` | `60` | Altura da forma em pixels |
| `--style` | `"rounded=1;whiteSpace=wrap;html=1;"` | String de estilo do draw.io |
| `--diagram-index` | `0` | Índice da página do diagrama (base zero) |
| `--dry-run` | false | Imprime o XML da nova célula sem modificar o arquivo |

**Exemplos**

```bash
# Adicionar uma caixa arredondada básica
python scripts/add-shape.py docs/flowchart.drawio "Nova etapa" 400 300

# Adicionar uma forma com estilo personalizado
python scripts/add-shape.py docs/flowchart.drawio "Decisão" 400 400 \
  --width 160 --height 80 \
  --style "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"

# Visualizar sem gravar
python scripts/add-shape.py docs/architecture.drawio "Serviço X" 600 200 --dry-run
```

**Saída**

Imprime o ID da nova célula em caso de sucesso:

```
Forma id="auto_abc123" adicionada à página 0 de docs/flowchart.drawio
```

---

## Fluxos comuns

### Validar antes de confirmar no Git

```bash
# Validar todos os diagramas
find . -name "*.drawio" -not -path "*/node_modules/*" | \
  xargs -I{} python scripts/validate-drawio.py {}
```

### Adicionar rapidamente um nó de marcador de posição

```bash
python scripts/add-shape.py docs/architecture.drawio "TODO: Serviço" 800 400 \
  --style "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
```

### Verificar se um modelo é válido

```bash
python scripts/validate-drawio.py .github/skills/draw-io-diagram-generator/templates/flowchart.drawio
```
