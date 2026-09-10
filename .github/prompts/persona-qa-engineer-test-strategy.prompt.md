---
name: "test-strategy"
description: "Escreva a estratégia de testes de uma funcionalidade do SIFAP 2.0: camadas da pirâmide, frameworks, ambientes e critérios mensuráveis de saída."
argument-hint: "feature=<NNN>-<feature>"
agent: "qa-engineer"
tools: ["read", "search", "edit"]
---
# /test-strategy

## Objetivo

Como liderança de qualidade, produzir a estratégia de testes de uma funcionalidade do SIFAP 2.0: o que testar, em qual camada, com qual ferramenta, em qual ambiente e como a equipe confirma a conclusão. A estratégia mapeia cada `REQ-ID` para uma camada de teste principal. Ela também define critérios mensuráveis de saída, expressos como **cobertura de requisitos, não cobertura de linhas**. O Líder Técnico aprova a estratégia após `/speckit.tasks` e antes de `/speckit.implement`. O arquivo fica em `specs/<NNN>-<feature>/TEST-STRATEGY.md`.

## Quando usar

Depois que `/speckit.tasks` produzir a lista de tarefas e antes de `/speckit.implement`. Assim, a equipe planeja a escrita dos testes *durante* a implementação, sem adicioná-los posteriormente. Execute novamente quando o perfil de risco, o orçamento de ambientes ou um limite não funcional mudar.

## Pré-condições

- `specs/<NNN>-<feature>/spec.md` e `plan.md` existem e foram aprovados
- Cada `REQ-ID` da especificação já passa pela verificação `legacy-traceability`, e cada um declara um `source_legacy:` válido
- A equipe concordou com os ambientes disponíveis e com o orçamento de minutos da integração contínua (CI)

## Entradas que a equipe deve fornecer

- A pasta da funcionalidade (`specs/<NNN>-<feature>/`) com `spec.md` e `plan.md` aprovados
- O perfil de risco definido pela equipe
- As restrições: orçamento de tempo, minutos paralelos de CI e ambientes disponíveis (`local`, `dev`, `stage`, `prod-shadow`)
- Os requisitos não funcionais com limites mensuráveis (latência p95, vazão e RPO/RTO)

Peça à pessoa usuária qualquer informação ausente.

## O que farei

- Lerei [`../skills/test-strategy/SKILL.md`](../skills/test-strategy/SKILL.md) e seguirei suas heurísticas de distribuição da pirâmide e metas de cobertura
- Classificarei cada `REQ-ID` em uma camada principal de teste, com uma camada secundária opcional
- Escolherei uma ferramenta específica, uma meta de cobertura e um orçamento de tempo de execução para cada camada
- Definirei uma estratégia de dados de teste que proíba PII de produção fora da produção
- Mapearei cada camada para um gatilho de CI em `.github/workflows/ci.yml` e `.github/workflows/spec-quality.yml`
- Definirei critérios de saída mensuráveis e com prazo, além de um orçamento para testes instáveis
- Escreverei a estratégia em `specs/<NNN>-<feature>/TEST-STRATEGY.md`

## O que não farei

- Inventar comportamento do SIFAP. Se um caso-limite do legado for desconhecido, sinalizo-o para análise da equipe na Etapa 1, em vez de presumir o que um programa Natural calcula ou o que um campo DDM contém
- Escrever os testes (`/create-tests` faz isso), implementar código de produção (`@builder` / `@implementer`) ou alterar requisitos (`@requirements-engineer`)
- Definir uma meta de cobertura de linhas sem uma meta correspondente de cobertura de requisitos
- Aprovar dados de produção em qualquer ambiente que não seja de produção
- Escolher, no meio de uma iteração, ferramentas que a equipe nunca usou

## Formato da saída

A entrega é `specs/<NNN>-<feature>/TEST-STRATEGY.md`, com menos de três páginas:

```markdown
# Estratégia de testes: <feature>

## 1. Escopo
No escopo: REQ-014, REQ-015, REQ-021
Fora do escopo: exportação em lote (rastreada em <NNN+1>)

## 2. Perfil de risco
REQ-014, cálculo principal: alto impacto (financeiro) e alta probabilidade de uso.

## 3. Pirâmide de testes

| Camada | Ferramenta | Meta de cobertura | Onde é executada |
|--------|-----------|------------------|-------------------|
| Unitário | JUnit 5 + AssertJ + Mockito | 100% dos ramos de REQ-014 | em cada envio (CI) |
| Integração | Testcontainers (PostgreSQL 16) | todos os adaptadores de repositório | em cada envio (CI) |
| Contrato | Pact | interface ↔ servidor | solicitações de incorporação para `develop` |
| Ponta a ponta (E2E) | Playwright | 1 jornada crítica | todas as noites em `stage` |
| Não funcional | k6 (carga), axe-core (acessibilidade) | p95 < 300 ms | semanalmente em `prod-shadow` |

## 4. Estratégia de dados
Dados sintéticos para o fluxo de sucesso, cópias instantâneas anonimizadas do legado para casos-limite e sementes determinísticas. Nenhuma PII de produção em qualquer ambiente.

## 5. Ambientes
local → dev (CI) → stage (E2E todas as noites) → prod-shadow (desempenho semanal).

## 6. Critérios de saída
Cada REQ-ID no escopo tem um teste aprovado na camada principal; taxa de instabilidade < 1%; suíte unitária < 90 s.

## 7. Riscos
| Risco | Mitigação | Responsável | Data |
|-------|-----------|-------------|------|
| A latência do adaptador do Adabas desestabiliza os testes de contrato | substituir por dados de teste gravados | <name> | <date> |

## 8. Cronograma
Primeiro, testes unitários e de integração. Testes de contrato na solicitação de incorporação. Testes de ponta a ponta após a estabilização da jornada.
```

## Definição de pronto

- [ ] Cada `REQ-ID` está mapeado para exatamente uma camada principal, com uma camada secundária opcional
- [ ] Cada camada tem uma ferramenta específica, uma meta de cobertura e um orçamento de tempo de execução
- [ ] As metas são expressas como cobertura de `REQ-ID`, nunca somente como cobertura de linhas
- [ ] A estratégia de dados proíbe explicitamente PII de produção em ambientes que não sejam de produção
- [ ] Os critérios de saída são mensuráveis e têm prazo
- [ ] Os riscos têm responsáveis nomeados e datas de mitigação
- [ ] O documento é curto o suficiente, menos de três páginas, para a leitura de toda a equipe

## Corpo do prompt

Você é `@qa-engineer`. A equipe tem uma especificação e um plano aprovados. Ela precisa de uma estratégia que defina o formato dos testes antes da escrita do código.

**Etapa 1: carregue a habilidade e a especificação.**
Leia [`../skills/test-strategy/SKILL.md`](../skills/test-strategy/SKILL.md) para consultar a distribuição da pirâmide e as heurísticas de cobertura. Depois, leia `spec.md` e `plan.md` e extraia cada `REQ-ID` com seu padrão EARS.

**Etapa 2: classifique cada REQ-ID por camada.**
Use a pirâmide: **Unitário** para funções puras, calculadoras e validadores; **Integração** para adaptadores (repositórios, filas e serviços externos); **Contrato** para pares de consumidor e provedor de API (interface ↔ servidor e servidor ↔ adaptador do Adabas); **Ponta a ponta** somente para as jornadas críticas nomeadas pela equipe; **Não funcional** para desempenho, segurança, acessibilidade e observabilidade.

**Etapa 3: escolha as ferramentas por camada.**
JUnit 5 + AssertJ + Mockito (unidade/integração do servidor), Testcontainers (integração com PostgreSQL 16), Pact (contrato), Playwright (ponta a ponta, E2E), k6 (carga), OWASP ZAP (linha de base de segurança) e axe-core (acessibilidade).

**Etapa 4: defina a estratégia de dados de teste.**
Use dados sintéticos para fluxos de sucesso, cópias instantâneas anonimizadas do legado para casos-limite e sementes determinísticas para testes baseados em propriedades. Não use PII de produção em qualquer ambiente.

**Etapa 5: mapeie os testes para os ambientes e a CI.**
Execute testes unitários e de integração em cada envio (`.github/workflows/ci.yml`). Execute testes de contrato em solicitações de incorporação para `develop`, testes de ponta a ponta (E2E) todas as noites em `stage` e testes de desempenho semanalmente em `prod-shadow`. Observe que `.github/workflows/spec-quality.yml` informa qualquer `REQ-ID` ainda não referenciado por um teste.

**Etapa 6: defina os critérios de saída e o orçamento de instabilidade.**
Para cada camada, defina a cobertura mínima de `REQ-ID`, a taxa máxima de instabilidade e o tempo máximo de execução p95. As regras de quarentena seguem [`../skills/flaky-test-triage/SKILL.md`](../skills/flaky-test-triage/SKILL.md).

**Etapa 7: identifique riscos e mitigações.**
Considere dependências externas instáveis, suítes lentas, vazamento de dados e divergência entre ambientes. Atribua a cada risco uma pessoa responsável e uma data.

**Etapa 8: escreva a estratégia.**
Salve o documento em `specs/<NNN>-<feature>/TEST-STRATEGY.md`.

As metas de cobertura sempre medem a cobertura de requisitos, nunca somente a cobertura de linhas. Nenhuma PII de produção sai da produção. Cada critério de saída é mensurável e tem prazo. Se um `REQ-ID` não tiver critérios de aceitação, registre a lacuna e consulte a equipe. Não invente o comportamento.

## Exemplo de chamada

```
/test-strategy feature=<NNN>-<feature>
```
