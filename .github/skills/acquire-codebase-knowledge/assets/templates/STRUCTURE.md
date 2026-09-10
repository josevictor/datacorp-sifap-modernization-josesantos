# Estrutura da base de código

## Seções principais (obrigatórias)

### 1) Mapa de nível superior

Liste somente os diretórios e arquivos relevantes de nível superior.

| Caminho | Finalidade | Evidência |
|------|---------|----------|
| [caminho/] | [finalidade] | [fonte] |

### 2) Pontos de entrada

- Entrada principal do ambiente de execução: [ARQUIVO]
- Pontos de entrada secundários (processo em segundo plano/CLI/tarefas): [ARQUIVOS ou NENHUM]
- Como a entrada é selecionada (script/configuração): [NOTA]

### 3) Limites dos módulos

| Limite | O que pertence aqui | O que não deve estar aqui |
|----------|-------------------|------------------------|
| [módulo/camada] | [responsabilidade] | [lógica proibida] |

### 4) Regras de nomenclatura e organização

- Padrão de nomes de arquivos: [kebab/camel/Pascal + exemplos]
- Padrão de organização dos diretórios: [funcionalidade/camada/domínio]
- Convenções de nomes alternativos de importação ou caminhos: [REGRA]

### 5) Evidências

- [path/to/root-tree-source]
- [path/to/entry-config]
- [path/to/key-module]

## Seções ampliadas (opcionais)

Adicione somente quando a complexidade do repositório exigir:

- Mapas detalhados de subdiretórios por funcionalidade/camada
- Detalhes da ordem de componentes intermediários/inicialização
- Limites entre a estrutura gerada e o código-fonte
- Mapas da estrutura de espaços de trabalho do monorepositório
