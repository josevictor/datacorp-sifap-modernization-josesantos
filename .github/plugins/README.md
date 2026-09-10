# Extensões (plugins) do Copilot

Este diretório empacota as **habilidades** e os **agentes** selecionados do
Copilot como extensões nomeadas e os expõe por meio de um **catálogo local
(marketplace)** de extensões
para que possam ser declarados em
[`.github/copilot/settings.json`](../copilot/settings.json).

## O que existe aqui

- Dez diretórios de extensões, cada um com um manifesto `plugin.json` e um `README.md`.
- [`marketplace.json`](marketplace.json) — um **catálogo de diretório** local
  chamado `datacorp-mm-team-kit`, que lista todas as dez extensões.

O conteúdo real das habilidades e dos agentes **não** é duplicado aqui. Ele é mantido
uma única vez no nível do repositório, em [`.github/skills/`](../skills/) e
[`.github/agents/`](../agents/). Cada `plugin.json` referencia esse conteúdo
compartilhado com caminhos relativos como `../../skills/<name>/` e
`../../agents/<name>.agent.md`.

## Duas camadas, uma fonte única da verdade

1. **Descoberta nativa (neste repositório).** O Copilot carrega automaticamente
   todas as habilidades em `.github/skills/` e todos os agentes em `.github/agents/`.
   Neste repositório, esses componentes já funcionam sem instalar nada.
2. **Empacotamento por extensões (para nomeação e reutilização).** As extensões
   agrupam os componentes compartilhados em conjuntos temáticos e os publicam
   pelo mecanismo oficial de catálogo (`marketplace`) / `enabledPlugins`.

## Catálogo

| Extensão | Conteúdo | Situação |
|--------|---------|--------|
| [`arch`](arch/) | — | somente catálogo (sem componentes neste kit) |
| [`azure-cloud-development`](azure-cloud-development/) | 3 habilidades | habilitada |
| [`chromium-control-canvas`](chromium-control-canvas/) | — | somente catálogo (sem componentes neste kit) |
| [`context-engineering`](context-engineering/) | 1 habilidade | habilitada |
| [`copilot-sdk`](copilot-sdk/) | 1 habilidade | habilitada |
| [`database-data-management`](database-data-management/) | 2 habilidades | habilitada |
| [`frontend-web-dev`](frontend-web-dev/) | 1 agente, 1 habilidade | habilitada |
| [`java-development`](java-development/) | 4 habilidades | habilitada |
| [`software-engineering-team`](software-engineering-team/) | 1 agente | habilitada |
| [`testing-automation`](testing-automation/) | 2 habilidades | habilitada |

Estes manifestos foram adaptados do catálogo `github/awesome-copilot`. Das 48
referências a componentes nos manifestos originais, 16 apontam para conteúdo
existente neste kit e foram mantidas; as outras 32 apontam para habilidades, agentes
ou extensões que não fazem parte deste kit e foram removidas. O README de cada
extensão lista exatamente o que foi removido.

## Como as extensões são habilitadas

A configuração declarativa fica em
[`.github/copilot/settings.json`](../copilot/settings.json):

```json
{
  "extraKnownMarketplaces": {
    "datacorp-mm-team-kit": {
      "source": { "source": "directory", "path": ".github/plugins" }
    }
  },
  "enabledPlugins": {
    "java-development@datacorp-mm-team-kit": true
  }
}
```

- `extraKnownMarketplaces` registra o catálogo de diretório local. O formato
  do valor (`{ "source": { "source": "directory", "path": ... } }`) é exatamente
  o que a CLI grava quando você registra um catálogo de diretório.
- As chaves de `enabledPlugins` são **especificações** de extensões no formato
  `name@marketplace` — nunca nomes isolados nem caminhos do sistema de arquivos.
  Somente as oito extensões que contêm componentes estão habilitadas; as duas
  entradas somente de catálogo são listadas no catálogo, mas não são
  habilitadas, pois habilitá-las não carregaria nada.

Para registrar o catálogo sob demanda a partir da raiz do repositório, use o
comando aceito pela CLI para uma origem de diretório (o prefixo explícito `./` é
obrigatório para que o caminho não seja interpretado como uma especificação
`owner/repo` do GitHub):

```bash
copilot plugin marketplace add ./.github/plugins
copilot plugin marketplace browse datacorp-mm-team-kit
```

## Limitações declaradas

- **Neste repositório, as extensões não adicionam nenhuma funcionalidade nova.**
  Tudo o que elas referenciam já é carregado pela descoberta nativa de
  `.github/skills/` e `.github/agents/`. A camada de extensões serve para
  documentação e empacotamento: ela registra quais componentes compartilhados
  formam cada conjunto e os expõe pelo mecanismo oficial de catálogo.
- **Extensões instaladas copiam somente seu próprio diretório.** Quando uma extensão é
  instalada de um catálogo, o Copilot copia o diretório dessa extensão — não a
  raiz do repositório. Como estes manifestos apontam para conteúdo compartilhado
  **fora** do diretório da extensão (`../../skills/...`, `../../agents/...`), esses
  componentes não são copiados na instalação e não aparecerão em outro
  repositório nem em uma instalação global. Isso foi verificado empiricamente:
  a instalação de uma extensão desse tipo relata sucesso, mas inclui zero habilidades.
  Para fornecer uma extensão autocontida, o conteúdo referenciado precisa ser
  incorporado ao diretório da extensão. Este kit deliberadamente não duplica esse
  conteúdo, pois ele é mantido uma única vez na raiz do repositório.
- **Execuções sem interface (headless) de `copilot -p` não aplicaram
  `extraKnownMarketplaces` do repositório.** Em uma sessão de solicitação
  (`prompt`) não interativa, somente os catálogos padrão foram carregados. As configurações
  declarativas são documentadas para sessões interativas e de agentes; a forma
  confiável e verificada de registrar o catálogo local é o comando
  `copilot plugin marketplace add ./.github/plugins` acima.

## Validação

```bash
# todos os manifestos e arquivos de configuração são interpretados como JSON
python3 -c "import json,glob; [json.load(open(f)) for f in \
  glob.glob('.github/plugins/*/plugin.json') + \
  ['.github/copilot/settings.json', '.github/plugins/marketplace.json']]"

# análise de Markdown (usa o arquivo .markdownlint-cli2.jsonc da raiz)
npx --yes markdownlint-cli2 ".github/plugins/**/*.md"
```

## Referências

- Extensões da Copilot CLI:
  <https://docs.github.com/copilot/concepts/agents/copilot-cli/about-cli-plugins>
- Criação de extensões:
  <https://docs.github.com/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating>
- Referência da Copilot CLI:
  <https://docs.github.com/copilot/how-tos/copilot-cli>
- Catálogo original: <https://github.com/github/awesome-copilot>
