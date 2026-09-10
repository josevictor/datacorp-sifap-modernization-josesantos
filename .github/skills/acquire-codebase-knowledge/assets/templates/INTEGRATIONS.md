# Integrações externas

## Seções principais (obrigatórias)

### 1) Inventário de integrações

| Sistema | Tipo (API/BD/fila/etc.) | Finalidade | Modelo de autenticação | Criticidade | Evidência |
|--------|---------------------------|---------|------------|-------------|----------|
| [nome] | [tipo] | [finalidade] | [autenticação] | [alta/média/baixa] | [arquivo] |

### 2) Armazenamentos de dados

| Armazenamento | Papel | Camada de acesso | Risco principal | Evidência |
|-------|------|--------------|----------|----------|
| [bd/memória cache/etc.] | [papel] | [módulo] | [risco] | [arquivo] |

### 3) Tratamento de segredos e credenciais

- Fontes de credenciais: [ambiente/gerenciador de segredos/configuração]
- Verificações de valores fixos: [resultado]
- Notas sobre rotação ou ciclo de vida: [conhecido/desconhecido]

### 4) Confiabilidade e comportamento em falhas

- Comportamento de novas tentativas/espera progressiva: [implementado/nenhum/parcial]
- Política de tempo limite: [onde está configurada]
- Comportamento de disjuntor ou alternativa: [se houver]

### 5) Observabilidade das integrações

- Registros em torno de chamadas externas: [sim/não + onde]
- Cobertura de métricas/rastreamento: [sim/não + onde]
- Lacunas de visibilidade: [lista]

### 6) Evidências

- [path/to/integration-wrapper]
- [path/to/config-or-env-template]
- [path/to/monitoring-or-logging-config]

## Seções ampliadas (opcionais)

Adicione somente quando necessário:

- Catálogo por ponto de extremidade
- Diagramas de sequência do fluxo de autenticação
- SLA/SLO por integração
- Notas sobre topologia de regiões/recuperação de falhas
