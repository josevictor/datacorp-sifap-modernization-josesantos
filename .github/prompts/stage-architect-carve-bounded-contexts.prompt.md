---
name: "carve-bounded-contexts"
description: "Avalia as hipóteses de limites da Etapa 1 e define contextos delimitados para o Monólito Modular."
argument-hint: "report=01-archaeology/discovery-report.md"
agent: "architect"
tools: ["read", "search", "edit"]
---
# /carve-bounded-contexts

## Objetivo

Transformar as hipóteses de limites do relatório da Etapa 1 em contextos delimitados avaliados e decididos. Cada contexto recebe nome, responsabilidades, dados próprios e regras de comunicação.

## Quando usar

No início da Etapa 2, logo após a revisão de `01-archaeology/discovery-report.md`.

## Pré-condições

- O relatório existe e contém pelo menos três hipóteses
- A equipe revisou o relatório e está pronta para decidir

## Entradas que a equipe deve fornecer

- O caminho do relatório de descoberta
- Restrições ou preferências adicionais

## O que farei

- Lerei as hipóteses e avaliarei cada uma por coesão, acoplamento e frequência de mudança
- Apresentarei a análise à equipe e registrarei rejeições com justificativa
- Formalizarei os contextos aceitos com nomes, responsabilidades e propriedade dos dados

## O que não farei

- Decidir automaticamente; a decisão final é da equipe
- Propor microsserviços; o destino é um Monólito Modular
- Inventar contexto de negócio ou omitir critérios de avaliação

## Formato da saída

Um arquivo `02-modern-spec/bounded-contexts.md`:

```markdown
# Mapa de contextos delimitados
## Critérios de avaliação
## Avaliação das hipóteses
### [Nome da hipótese] — ACEITA / REJEITADA
## Contextos delimitados finais
### [Nome do contexto]
- Responsabilidade:
- Dados próprios (DDMs/tabelas):
- Interface pública:
- Motivo para ser um contexto separado:
## Comunicação entre contextos
## Diagrama Mermaid do mapa de contextos
```

## Definição de pronto

- [ ] Cada hipótese foi avaliada pelos três critérios
- [ ] Rejeições têm justificativa
- [ ] Entre dois e cinco contextos foram definidos com nomes de negócio
- [ ] Cada contexto tem responsabilidade, dados próprios e interface pública
- [ ] Um diagrama Mermaid mostra as relações e os caminhos de comunicação

## Corpo do prompt

Você é `@architect`. A equipe inicia a Etapa 2 e precisa definir contextos delimitados para o Monólito Modular.

**Etapa 1 — Ler o relatório.**
Extraia cada hipótese, seus programas, DDMs e justificativa.

**Etapa 2 — Avaliar três critérios.**

- **Coesão**: as regras representam a mesma capacidade de negócio? Consulte regras confirmadas em `01-archaeology/business-rules-catalog.md`.
- **Acoplamento**: quantas dependências cruzam o limite? Conte as arestas em `01-archaeology/dependency-map.md`. Baixo acoplamento fortalece a hipótese.
- **Frequência de mudança**: use padrões de nomes e chamadas como aproximações. Programas fortemente conectados provavelmente mudam juntos.

Apresente High/Medium/Low para cada critério.

**Etapa 3 — Solicitar a decisão.**
Apresente placar, recomendação e justificativa. Pergunte: “A equipe aceita esta recomendação? Caso contrário, o que mudaria?” Registre a justificativa de qualquer decisão diferente.

**Etapa 4 — Formalizar contextos aceitos.**
Para cada um, registre nome de negócio confirmado, responsabilidade, DDMs ou tabelas exclusivas, operações públicas em assinaturas ou eventos e uma frase que relacione o limite aos critérios.

**Etapa 5 — Definir a comunicação.**
Registre direção, mecanismo (chamada em processo por interface, evento de domínio ou tipo de kernel compartilhado) e dados trocados. A comunicação é em processo, nunca HTTP entre serviços.

**Etapa 6 — Desenhar o mapa.**
Crie um diagrama Mermaid com caixas e setas rotuladas. Preserve a paleta `#0f172a`, `#334155`, `#e2e8f0`.

**Etapa 7 — Escrever a saída.**
Escreva em `02-modern-spec/bounded-contexts.md`.

## Exemplo de chamada

```
/carve-bounded-contexts report=01-archaeology/discovery-report.md
```
