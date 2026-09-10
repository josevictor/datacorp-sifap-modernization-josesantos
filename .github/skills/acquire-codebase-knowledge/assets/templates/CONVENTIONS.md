# Convenções de código

## Seções principais (obrigatórias)

### 1) Regras de nomenclatura

| Item | Regra | Exemplo | Evidência |
|------|------|---------|----------|
| Arquivos | [REGRA] | [EXEMPLO] | [ARQUIVO] |
| Funções/métodos | [REGRA] | [EXEMPLO] | [ARQUIVO] |
| Tipos/interfaces | [REGRA] | [EXEMPLO] | [ARQUIVO] |
| Constantes/variáveis de ambiente | [REGRA] | [EXEMPLO] | [ARQUIVO] |

### 2) Formatação e análise estática

- Formatador: [FERRAMENTA + ARQUIVO DE CONFIGURAÇÃO]
- Ferramenta de análise estática: [FERRAMENTA + ARQUIVO DE CONFIGURAÇÃO]
- Regras aplicadas mais relevantes: [REGRA_1], [REGRA_2], [REGRA_3]
- Comandos de execução: [COMANDOS]

### 3) Convenções de importações e módulos

- Agrupamento/ordem de importações: [REGRA]
- Política de nomes alternativos versus importações relativas: [REGRA]
- Política de exportações públicas/agrupadas: [REGRA]

### 4) Convenções de erros e registros

- Estratégia de erros por camada: [RESUMO BREVE]
- Estilo de registros e campos de contexto obrigatórios: [RESUMO]
- Regras de ocultação de dados sensíveis: [RESUMO]

### 5) Convenções de testes

- Regra de nome/localização dos arquivos de teste: [REGRA]
- Padrão da estratégia de simulações: [REGRA]
- Expectativa de cobertura: [REGRA ou TODO]

### 6) Evidências

- [path/to/lint-config]
- [path/to/format-config]
- [path/to/representative-source-file]

## Seções ampliadas (opcionais)

Adicione somente para bases de código grandes ou inconsistentes:

- Matriz de tratamento de erros específica por camada
- Opções de rigor específicas da linguagem
- Convenções de commits e branches específicas do repositório
- Violações conhecidas de convenções que precisam ser corrigidas
