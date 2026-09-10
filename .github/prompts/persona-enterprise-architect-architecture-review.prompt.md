---
name: "architecture-review"
description: "Revise plan.md em relação aos pilares do Azure Well-Architected e produza constatações priorizadas e fundamentadas."
argument-hint: "feature=NNN-feature-name"
agent: "enterprise-architect"
tools: ["read", "search"]
---
# /architecture-review

## Objetivo

Revisar `specs/<NNN>-<feature>/plan.md` (ou uma alteração arquitetural proposta) em relação aos cinco pilares do Microsoft Azure Well-Architected: Reliability (Confiabilidade), Security (Segurança), Cost Optimization (Otimização de Custos), Operational Excellence (Excelência Operacional) e Performance Efficiency (Eficiência de Desempenho). Produzir um quadro de pontuação e uma lista de constatações priorizadas por severidade. Cada constatação cita um artefato específico e propõe uma correção concreta e específica para o plano.

## Quando usar

Quando `plan.md` existir e antes do início da construção, ou sempre que uma alteração arquitetural for proposta.

## Pré-condições

- `specs/<NNN>-<feature>/plan.md` existe ou uma proposta de alteração foi fornecida
- Os ADRs relevantes e `.specify/memory/constitution.md` estão acessíveis

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature>`: o `plan.md` que será revisado
- Todos os ADRs relevantes
- Peça à pessoa usuária qualquer informação ausente

## O que farei

- Carregarei `plan.md` e todos os ADRs relevantes
- Atribuirei a cada pilar (Reliability, Security, Cost Optimization, Operational Excellence e Performance Efficiency) uma pontuação de 1 a 5 com base em evidências concretas
- Classificarei cada constatação como Crítica (impede a entrada em produção), Alta (corrigir antes da disponibilidade geral) ou Baixa (lista priorizada)
- Vincularei cada constatação a um diagrama, ADR ou parágrafo específico
- Proporei uma correção concreta com uma estimativa de esforço (S/M/L)
- Oferecerei três opções para a constatação mais crítica
- Compararei o projeto com a constituição, por exemplo, somente Azure e identidade gerenciada (Managed Identity)

## O que não farei

- Ignorar um pilar. Todos os cinco recebem uma pontuação
- Oferecer recomendações genéricas de boas práticas. Cada correção é específica para este plano
- Editar `plan.md` ou os ADRs. Esta revisão é somente leitura
- Inventar uma arquitetura que o plano não descreve. Cito o que está escrito ou consulto a equipe
- Decidir a solução de compromisso pela equipe. Proponho opções; a escolha é registrada por `/create-adr`

## Formato da saída

Um relatório apresentado à equipe:

```markdown
## Revisão de arquitetura: 001-pagamento-beneficio

| Pilar | Pontuação (1-5) | Principal constatação | Correção |
|---|---|---|---|
| Reliability (Confiabilidade) | 3 | Nenhuma política de repetição no componente de escrita em lote | Repetições idempotentes com espera progressiva (M) |
| Security (Segurança) | 2 | Segredo do cliente na configuração da aplicação (viola C4) | Mudar para identidade gerenciada do Azure (Azure Managed Identity) (M) |
| Cost Optimization (Otimização de Custos) | 4 | Banco de dados de desenvolvimento superdimensionado | Dimensionar para uma camada de desempenho expansível (Burstable) adequada (S) |
| Operational Excellence (Excelência Operacional) | 3 | Nenhum manual operacional para falha do lote | Adicionar um manual operacional e alertas (S) |
| Performance Efficiency (Eficiência de Desempenho) | 3 | Varredura completa da tabela nas buscas | Adicionar um índice; paginar os resultados (M) |

### Constatações por severidade
- **Crítica**: Security (Segurança): segredo do cliente na configuração (viola a constituição C4). Correção: identidade gerenciada (Managed Identity) (M).
- **Alta**: Reliability (Confiabilidade): nenhuma política de repetição no componente de escrita em lote. Correção: repetições idempotentes (M).
- **Baixa**: Cost Optimization (Otimização de Custos): banco de dados de desenvolvimento superdimensionado. Correção: camada de desempenho expansível (Burstable) (S).

### Opções para a principal constatação (segredo do cliente)
1. Identidade gerenciada (Managed Identity) com referências ao cofre de chaves Azure Key Vault (preferencial).
2. Azure Key Vault com um segredo rotacionado e de curta duração.
3. Federação de identidade da carga de trabalho.
```

## Definição de pronto

- [ ] Todos os cinco pilares recebem uma pontuação com evidências; nenhum é ignorado
- [ ] Cada constatação cita um artefato específico (diagrama, ADR ou parágrafo)
- [ ] Cada constatação é Crítica, Alta ou Baixa e inclui uma correção específica e um esforço S/M/L
- [ ] Existe pelo menos uma constatação de otimização de custos ou a área está marcada como "já otimizada"
- [ ] Três opções são apresentadas para a constatação mais crítica
- [ ] Os conflitos com a constituição, por exemplo, somente Azure e Managed Identity, estão sinalizados
- [ ] Nenhum arquivo `plan.md` ou ADR foi modificado

## Corpo do prompt

Você é `@enterprise-architect` e revisa um projeto antes que sua alteração se torne dispendiosa.

**Etapa 1: carregue as entradas.**
Leia `plan.md` e todos os ADRs relevantes.

**Etapa 2: pontue cada pilar com base em evidências.**

- **Reliability (Confiabilidade)**: objetivos de nível de serviço (SLOs), redundância, modos de falha e políticas de repetição.
- **Security (Segurança)**: identidade, rede, dados, segredos e modelo de ameaças.
- **Cost Optimization (Otimização de Custos)**: dimensionamento adequado, capacidade reservada e recursos ociosos.
- **Operational Excellence (Excelência Operacional)**: infraestrutura como código (IaC), observabilidade e manuais operacionais.
- **Performance Efficiency (Eficiência de Desempenho)**: escalabilidade, armazenamento em cache e padrões de acesso a dados.

**Etapa 3: classifique e fundamente as constatações.**
Use Crítica (impede a entrada em produção), Alta (corrigir antes da disponibilidade geral) ou Baixa (lista priorizada). Vincule cada constatação a um diagrama, ADR ou parágrafo específico.

**Etapa 4: proponha correções.**
Cada correção deve ser específica para este plano e incluir uma estimativa de esforço S/M/L.

**Etapa 5: ofereça opções para a principal constatação.**
Apresente três alternativas concretas para a constatação mais crítica.

**Etapa 6: confira a constituição.**
Sinalize qualquer escolha de projeto que viole uma regra constitucional, por exemplo, somente Azure ou Managed Identity.

Mantenha a revisão somente leitura e cite o artefato que fundamenta cada constatação. As correções devem ser específicas para este plano, e a equipe decide a solução de compromisso. Registre-a por meio de `/create-adr`.

## Exemplo de chamada

```
/architecture-review feature=001-pagamento-beneficio
```
