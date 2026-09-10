---
name: "test-strategy"
description: "Use ao elaborar uma estratégia de testes, escolher o formato da pirâmide de testes, definir metas de cobertura ou avaliar investimentos em testes nas camadas unitária, de integração e de ponta a ponta (E2E). Os gatilhos incluem \"estratégia de testes\", \"pirâmide de testes\", \"meta de cobertura\", \"E2E versus integração\" e \"investimento em testes\"."
---
# Estratégia de testes

## Quando invocar

- "Elabore uma estratégia de testes para..."
- "Qual deve ser a proporção de testes unitários, de integração e de ponta a ponta (E2E)?"
- "Qual é a meta de cobertura adequada?"
- "Audite nossa pirâmide de testes."

## Fluxo de trabalho

1. **Faça o inventário** do código testado: módulos, APIs públicas, integrações externas e fluxos críticos.
2. **Classifique o risco** por módulo (P0 / P1 / P2) com base no raio de impacto de uma falha.
3. **Distribua a pirâmide**: use inicialmente 70% de testes unitários, 20% de integração e 10% E2E; justifique os desvios.
4. **Defina metas de cobertura**: linha de base de 80% de cobertura de linhas e 90% para módulos P0, acompanhando a cobertura de ramificações separadamente.
5. **Defina o orçamento de testes instáveis**: taxa máxima de 1%; qualquer valor acima disso aciona a quarentena.
6. **Escolha as ferramentas por camada**: unitária (Vitest/JUnit/pytest), integração (Testcontainers) e E2E (Playwright).
7. **Produza a saída**: um documento de estratégia de uma página com metas, ferramentas, limites de cobertura e regras de quarentena por camada.

## Heurísticas

- Se um teste E2E puder ser reescrito como testes de integração e contrato, faça isso. Testes E2E são caros e instáveis.
- Testes de contrato são melhores que objetos simulados para tudo que cruza os limites de um serviço.
- Testes de mutação (Stryker, PIT) são a única forma honesta de detectar testes que não comprovam nada.

## Antipadrões

- Pirâmide invertida: muitos testes E2E lentos sobre poucos testes unitários.
- Um único número global de cobertura, sem meta superior para módulos P0.
- Limites de serviço simulados que nunca detectam uma falha real de integração.
- Cobertura tratada como objetivo, não como indicador de confiança.

## Modelo de saída

```markdown
## Estratégia de testes - <sistema ou módulo>

| Camada | Distribuição-alvo | Ferramentas | Meta de cobertura |
|---|---|---|---|
| Unitária | 70% | JUnit 5 / Vitest | 80% de linhas (90% para P0) |
| Integração | 20% | Testcontainers | fluxos críticos |
| E2E | 10% | Playwright | principais jornadas de usuário |

**Orçamento de testes instáveis**: <=1% (acima disso, quarentena)
**Classificação de risco**: P0 <módulos> / P1 <módulos> / P2 <módulos>
```

## Critérios de qualidade

- [ ] Cada módulo está classificado por risco (P0/P1/P2) e tem uma meta de cobertura.
- [ ] A distribuição da pirâmide está definida por camada, e os desvios de 70/20/10 estão justificados.
- [ ] Cada camada indica sua ferramenta e seu limite.
- [ ] Há um orçamento de testes instáveis e uma regra de quarentena definidos.

## Referências

- [Google Testing Blog - Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html)
- [ISTQB Foundation Syllabus](https://www.istqb.org/certifications/certified-tester-foundation-level)
- [Martin Fowler - Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
