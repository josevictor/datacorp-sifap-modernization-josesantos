---
name: "create-constitution"
description: "Escreva .specify/memory/constitution.md, com as regras numeradas, testáveis e inegociáveis da funcionalidade."
argument-hint: "feature=NNN-feature-name"
agent: "enterprise-architect"
tools: ["read", "search", "edit"]
---
# /create-constitution

## Objetivo

Produzir `.specify/memory/constitution.md`: um conjunto curto (≤ 80 linhas) e numerado de regras testáveis e inegociáveis, agrupadas por categoria. Cada regra inclui a consequência de uma violação e uma marcação de mutável ou imutável. ADRs registram decisões. A constituição define os limites que essas decisões não podem ultrapassar.

## Quando usar

No início de uma funcionalidade (ou do projeto), antes que ADRs e especificações dependam de restrições compartilhadas. Execute novamente esta instrução para alterar a constituição por meio do processo documentado.

## Pré-condições

- `specs/<NNN>-<feature>/` existe, ou o escopo do projeto foi acordado
- As restrições organizacionais são conhecidas (linha de base de segurança, uso exclusivo do Azure, OWASP Top 10 e LGPD)
- Qualquer constituição superior que deva ser herdada está identificada

## Entradas que a equipe deve fornecer

- `feature=<NNN>-<feature>` (ou `project`)
- As restrições organizacionais existentes que devem ser codificadas
- Qualquer constituição superior que deva ser herdada
- As pessoas responsáveis pela aprovação, identificadas nominalmente (Arquiteto Corporativo, Líder Técnico e equipe de segurança da informação, ou InfoSec)
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Herdarei a constituição superior e a adaptarei com uma justificativa explícita
- Agruparei as regras em Pilha, Segurança, Dados, Operações, Processo e Conformidade
- Tornarei cada regra testável e atribuirei um ID (`C1`, `C2`, …)
- Declararei a consequência da violação de cada regra
- Marcarei cada regra como mutável (pode ser flexibilizada por ADR com aprovação da InfoSec) ou imutável
- Registrarei a data, aplicarei versionamento semântico (semver) e identificarei as pessoas responsáveis pela aprovação
- Manterei o arquivo com no máximo 80 linhas

## O que não farei

- Escrever princípios ("valorizamos a qualidade") em vez de regras ("somente Java 21")
- Emitir uma regra sem ID ou consequência de violação
- Ultrapassar 80 linhas. Uma constituição que ninguém consegue lembrar não funciona
- Inventar uma restrição organizacional ou uma pessoa responsável pela aprovação. Perguntarei à equipe
- Decidir uma escolha específica de projeto. Essa decisão deve ser registrada em um ADR por meio de `/create-adr`

## Formato da saída

A entrega é `.specify/memory/constitution.md`:

```markdown
# CONSTITUIÇÃO: 001-pagamento-beneficio

- **Versão**: 1.0.0
- **Data**: 2026-04-29
- **Responsáveis pela aprovação**: @paula (Arquiteto Corporativo), @morgan (Líder Técnico), @infosec-lead
- **Escopo**: regras aplicáveis a esta funcionalidade

## 1. Pilha
| ID | Regra | Consequência |
|---|---|---|
| C1 | A camada de serviços é executada somente em Java 21 (Temurin) e Spring Boot 3.3. | A compilação falha. |
| C2 | A interface acessada pelo navegador é executada em Next.js 15 com TypeScript `strict: true`. `any` é proibido. | A análise estática impede a integração. |
| C3 | PostgreSQL 16 é o único sistema de registro dos dados do SIFAP. | Exige uma exceção da InfoSec. |

## 2. Segurança
| ID | Regra | Consequência |
|---|---|---|
| C4 | A autenticação entre serviços usa Azure Managed Identity (identidade gerenciada do Azure). Segredos de cliente são proibidos no código e na configuração. | A solicitação de integração (PR) é bloqueada. |
| C5 | Os segredos são lidos do Azure Key Vault (cofre de chaves do Azure) no ambiente de execução. É proibido versionar `.env`. | O Gitleaks impede a integração. |
| C6 | Linha de base OWASP Top 10: validação de entradas, SQL parametrizado e proibição de consultas construídas por concatenação de strings. | A solicitação de integração (PR) é rejeitada. |

## 3. Dados
| ID | Regra | Consequência |
|---|---|---|
| C7 | As colunas com informações de identificação pessoal (PII) contêm um `COMMENT` que as identifica como PII. | A revisão da administração de banco de dados (DBA) impede o avanço. |
| C8 | PII de produção são proibidas em `dev` ou `stage`. Use somente dados sintéticos. | A InfoSec registra uma constatação e exige reversão imediata. |

## 4. Operações
| ID | Regra | Consequência |
|---|---|---|
| C9 | Cada ponto de extremidade público emite um registro estruturado com `requestId`, `userId` e `latencyMs`. | A revisão de código impede o avanço. |
| C10 | Cada ponto de extremidade voltado à pessoa usuária tem um objetivo de nível de serviço (SLO) registrado em um `REQ-OPS-*`. | A revisão da especificação impede o avanço. |

## 5. Processo
| ID | Regra | Consequência |
|---|---|---|
| C11 | Use uma ramificação por item de trabalho, criada a partir de `develop` com o prefixo do papel definido em `00-GIT-WORKFLOW.md` (`spec/`, `impl/`, `infra/`, `docs/`, `agent/`). Confirmações diretas em `develop` ou `main` são proibidas. | A solicitação de integração (PR) é rejeitada. |
| C12 | Cada requisito usa a notação EARS e cada teste cita um `REQ-ID`. | A revisão da especificação impede o avanço. |

## 6. Conformidade
| ID | Regra | Consequência |
|---|---|---|
| C13 | Os pontos de extremidade de direitos do titular previstos na LGPD (leitura, exclusão e exportação) têm cobertura de `REQ-COMP-*`. | A revisão de conformidade impede a liberação. |

## 7. Mutáveis e imutáveis
- Mutáveis (podem ser flexibilizadas por ADR com aprovação da InfoSec): C9–C12.
- Imutáveis (exigem mudança constitucional): C1, C3, C4, C5, C6, C7, C8, C13.

## 8. Processo de alteração
Abra uma solicitação de integração (PR) para este arquivo. O fórum de arquitetura faz a revisão e incrementa a versão (`1.0.0` -> `1.1.0` secundária, `-> 2.0.0` principal). As novas pessoas responsáveis registram a aprovação.
```

## Definição de pronto

- [ ] O arquivo tem ≤ 80 linhas, sem contar as assinaturas
- [ ] Cada regra tem um ID e uma consequência de violação
- [ ] Existe pelo menos uma regra por categoria (Pilha, Segurança, Dados, Operações, Processo e Conformidade)
- [ ] A distinção entre mutável e imutável está declarada
- [ ] O processo de alteração está documentado
- [ ] A constituição herda de uma constituição superior quando ela existe
- [ ] As pessoas responsáveis pela aprovação, a data e uma versão conforme o versionamento semântico estão registradas

## Corpo do prompt

Você atua como Arquiteto Corporativo (`@enterprise-architect`). A equipe precisa fixar os limites antes que as decisões e o código dependam deles.

**Etapa 1: herde e adapte.**
Comece pela constituição no nível do projeto. Torne-a mais ou menos restritiva somente para esta funcionalidade, com uma justificativa explícita.

**Etapa 2: agrupe as regras por categoria.**
Use Pilha, Segurança, Dados, Operações, Processo e Conformidade.

**Etapa 3: torne cada regra testável.**
"Use Java 21" é testável (`mvnw --version`); "use Java moderna" não é.

**Etapa 4: numere as regras.**
Use `C1`, `C2`, … para que as pessoas responsáveis pela revisão possam citá-las.

**Etapa 5: declare a consequência.**
Use "A compilação falha", "A solicitação de integração é rejeitada" ou "Exige uma exceção da InfoSec". Nunca omita a consequência.

**Etapa 6: marque como mutável ou imutável.**
Algumas regras podem ser flexibilizadas por meio de um ADR com aprovação da InfoSec. Outras exigem uma nova constituição.

**Etapa 7: registre data, versão e aprovações.**
Registre a data do fórum, as pessoas responsáveis pela aprovação e a versão `1.0.0`. Incremente a versão somente quando a própria constituição mudar.

Mantenha somente regras, não princípios, e limite o arquivo a 80 linhas. Uma escolha específica de projeto pertence a um ADR criado por meio de `/create-adr`, não a uma regra constitucional.

## Exemplo de chamada

```
/create-constitution feature=001-pagamento-beneficio
```
