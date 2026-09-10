# Referência para estimativa de custos

Fórmulas e padrões para converter preços unitários do Azure em estimativas de custo mensais e anuais.

## Cálculos padrão baseados em tempo

### Horas por mês

O Azure usa **730 horas/mês** como período de cobrança padrão (365 dias × 24 horas / 12 meses).

```
Custo mensal = preço unitário por hora × 730
Custo anual  = custo mensal × 12
```

### Multiplicadores comuns

| Período | Horas | Cálculo |
|--------|-------|-------------|
| 1 hora | 1 | Preço unitário |
| 1 dia | 24 | Preço unitário × 24 |
| 1 semana | 168 | Preço unitário × 168 |
| 1 mês | 730 | Preço unitário × 730 |
| 1 ano | 8.760 | Preço unitário × 8.760 |

## Fórmulas específicas por serviço

### Máquinas virtuais (computação)

```
Custo mensal = preço por hora × 730
```

Para VMs executadas apenas no horário comercial (8 h/dia, 22 dias/mês):

```
Custo mensal = preço por hora × 176
```

### Azure Functions

```
Custo de execução = preço por execução × quantidade de execuções
Custo de computação = preço por GB-s × (memória em GB × tempo de execução em segundos × quantidade de execuções)
Total mensal = custo de execução + custo de computação
```

Franquia gratuita: 1 milhão de execuções e 400.000 GB-s por mês.

### Azure Blob Storage

```
Custo de armazenamento = preço por GB × armazenamento em GB
Custo de transação = preço por 10.000 operações × (operações / 10.000)
Custo de saída = preço por GB × saída em GB
Total mensal = custo de armazenamento + custo de transação + custo de saída
```

### Azure Cosmos DB

#### Taxa de transferência provisionada

```
Custo mensal = (RU/s / 100) × preço por 100 RU/s × 730
```

#### Sem servidor

```
Custo mensal = (total de RUs consumidas / 1.000.000) × preço por 1 milhão de RUs
```

### Azure SQL Database

#### Modelo DTU

```
Custo mensal = preço por DTU × DTUs × 730
```

#### Modelo vCore

```
Custo mensal = preço do vCore × vCores × 730 + preço do armazenamento por GB × armazenamento em GB
```

### Azure Kubernetes Service (AKS)

```
Custo mensal = preço da VM do nó × 730 × quantidade de nós
```

O plano de controle é gratuito na camada Standard.

### Azure App Service

```
Custo mensal = preço do plano × 730 (para planos com preço por hora)
```

Ou use o preço mensal fixo para planos de camada fixa.

### Azure OpenAI

```
Custo mensal = (tokens de entrada / 1.000) × preço de entrada por mil tokens
              + (tokens de saída / 1.000) × preço de saída por mil tokens
```

## Comparação entre reserva e pagamento conforme o uso

Ao apresentar opções de preço, sempre mostre a comparação:

```
| Modelo de preço | Custo mensal | Custo anual | Economia em relação ao pagamento conforme o uso (PAYG) |
|---------------|-------------|-------------|------------------|
| Pagamento conforme o uso | $X | $Y | — |
| Reserva de 1 ano | $A | $B | Z% |
| Reserva de 3 anos | $C | $D | W% |
| Plano de economia (1 ano) | $E | $F | V% |
| Plano de economia (3 anos) | $G | $H | U% |
| Spot (se disponível) | $I | N/D | T% |
```

Fórmula do percentual de economia:

```
Economia % = ((preço PAYG - preço reservado) / preço PAYG) × 100
```

## Modelo de tabela de resumo de custos

Sempre apresente os resultados neste formato:

```markdown
| Serviço | SKU | Região | Preço unitário | Unidade | Estimativa mensal | Estimativa anual |
|---------|-----|--------|-----------|------|-------------|-------------|
| Virtual Machines | Standard_D4s_v5 | East US | $0.192/h | 1 hora | $140.16 | $1,681.92 |
```

## Dicas

- Sempre esclareça o **padrão de uso** antes de estimar (24 horas por dia, horário comercial ou uso esporádico).
- Para **armazenamento**, pergunte sobre o volume de dados esperado e os padrões de acesso.
- Para **bancos de dados**, pergunte sobre os requisitos de taxa de transferência (RU/s, DTUs ou vCores).
- Para serviços **sem servidor**, pergunte sobre a quantidade e a duração esperadas das invocações.
- Arredonde a exibição para duas casas decimais.
- Informe que os preços estão em **USD**, salvo especificação em contrário.
