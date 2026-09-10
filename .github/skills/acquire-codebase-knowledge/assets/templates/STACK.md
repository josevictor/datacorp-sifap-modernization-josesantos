# Conjunto de tecnologias

## Seções principais (obrigatórias)

### 1) Resumo do ambiente de execução

| Área | Valor | Evidência |
|------|-------|----------|
| Linguagem principal | [VALOR] | [CAMINHO_DO_ARQUIVO] |
| Ambiente de execução + versão | [VALOR] | [CAMINHO_DO_ARQUIVO] |
| Gerenciador de pacotes | [VALOR] | [CAMINHO_DO_ARQUIVO] |
| Sistema de módulos/compilação | [VALOR] | [CAMINHO_DO_ARQUIVO] |

### 2) Estruturas de software e dependências de produção

Liste somente dependências de produção de alto impacto (frameworks, dados, transporte e autenticação).

| Dependência | Versão | Papel no sistema | Evidência |
|------------|---------|----------------|----------|
| [NOME] | [VERSÃO] | [PAPEL] | [CAMINHO_DO_ARQUIVO] |

### 3) Ferramentas de desenvolvimento

| Ferramenta | Finalidade | Evidência |
|------|---------|----------|
| [FERRAMENTA] | [ANÁLISE ESTÁTICA/FORMATAÇÃO/TESTE/COMPILAÇÃO] | [CAMINHO_DO_ARQUIVO] |

### 4) Comandos principais

```bash
[comando de instalação]
[comando de compilação]
[comando de teste]
[comando de análise estática]
```

### 5) Ambiente e configuração

- Fontes de configuração: [LISTAR ARQUIVOS]
- Variáveis de ambiente obrigatórias: [VAR_1], [VAR_2], [TODO]
- Restrições de implantação/ambiente de execução: [NOTA BREVE]

### 6) Evidências

- [path/to/manifest]
- [path/to/runtime-config]
- [path/to/build-or-ci-config]

## Seções ampliadas (opcionais)

Adicione somente quando necessário para repositórios complexos:

- Taxonomia completa de dependências por categoria
- Opções detalhadas do compilador/ambiente de execução
- Matriz de ambientes (desenvolvimento/homologação/produção)
- Detalhes do gerenciador de processos e do ambiente de execução de contêineres
