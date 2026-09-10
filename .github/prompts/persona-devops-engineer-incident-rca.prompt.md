---
name: "incident-rca"
description: "Facilite uma análise de causa raiz sem culpabilização para um incidente do SIFAP 2.0: linha do tempo, fatores contribuintes e ações priorizadas com responsáveis."
argument-hint: "incident=<ticket-id> severity=SEV-N"
agent: "devops-engineer"
tools: ["read", "search", "edit"]
---
# /incident-rca

## Objetivo

Facilitar uma **análise de causa raiz sem culpabilização (RCA)** para um incidente do SIFAP 2.0. O resultado é um único documento, `docs/incidents/<YYYYMMDD>-<short-slug>.md`, que registra a linha do tempo, o ocorrido, seus motivos, as mudanças que evitam recorrência e como a equipe verificará sua eficácia. O público inclui as equipes de engenharia e de Engenharia de Confiabilidade de Sites (SRE), a pessoa responsável pela Segurança da Informação e a pessoa responsável pela arquitetura da plataforma. A análise trata dos sistemas, nunca das pessoas.

## Quando usar

Use depois que um incidente for mitigado e resolvido, quando as pessoas que responderam puderem reconstruir a linha do tempo com base em evidências. Execute enquanto os dados do PagerDuty, Slack, Application Insights e dos registros de implantação ainda estiverem recentes.

## Pré-condições

- O incidente está resolvido e o impacto para clientes terminou
- As evidências da linha do tempo estão disponíveis: alertas, conversas, rastros e horários de implantação
- Os objetivos de nível de serviço (SLOs) afetados e todos os `REQ-ID`s vinculados estão identificados

## Entradas que a equipe deve fornecer

- O ID do chamado do incidente e a gravidade (`SEV-1` a `SEV-4`)
- Os horários de detecção, mitigação e resolução (UTC)
- Os sistemas afetados e os `REQ-ID`s vinculados aos SLOs violados
- Os dados brutos da linha do tempo: PagerDuty, canal do Slack, rastros do Application Insights e horários de implantação
- Os nomes das pessoas que responderam (somente para a linha do tempo, nunca para atribuir culpa)

Solicite à pessoa usuária qualquer item ausente.

## O que farei

- Reformularei o impacto pela perspectiva de clientes, não pelos sintomas da infraestrutura interna
- Reconstruirei a linha do tempo minuto a minuto em UTC e citarei uma fonte para cada registro
- Separarei detecção, mitigação e resolução (`T0`, `Td`, `Tm`, `Tr`)
- Identificarei vários fatores contribuintes com o método dos Cinco Porquês (`Five Whys`) e categorizarei cada um
- Registrarei o que *quase* funcionou e proporei ações verificáveis com responsáveis e datas
- Registrarei com transparência pelo menos um risco aceito

## O que não farei

- Fabricar um registro da linha do tempo ou um limite de SLO. Cada item cita um registro de sistema, uma métrica, uma mensagem de conversa ou uma lembrança marcada com `[recall]`, e os valores desconhecidos serão perguntados, não presumidos
- Associar uma pessoa a um erro. As análises de causa raiz tratam de sistemas ("o processo não detectou o erro de digitação", não "a pessoa engenheira cometeu um erro de digitação")
- Implementar as correções. Criarei itens de ação; mudanças na esteira de CI/CD seguem para `/pipeline`, mudanças na infraestrutura para `/iac-module` e mudanças no código para `@builder`
- Declarar uma única "causa raiz". Sempre existem vários fatores contribuintes
- Escrever uma ação sem uma pessoa responsável, uma data de entrega e critérios de verificação

## Formato da saída

O resultado é `docs/incidents/<YYYYMMDD>-<slug>.md`:

```markdown
# Incidente 20260817-payment-timeout

- **Gravidade**: SEV-2
- **Impacto para clientes**: os envios falharam por cerca de 18 min (HTTP 504)
- **Violação de SLO**: REQ-045 (99,9% de disponibilidade), violado
- **Duração total**: T0 09:12Z → Tr 09:41Z (29 min)

## 1. Resumo
Dois parágrafos. O que aconteceu, por quê, o que fizemos e o que mudará.

## 2. Linha do tempo (UTC)
| Horário | Fonte | Evento |
|-------|--------|-------|
| 09:12Z | App Insights | latência p95 ultrapassa 3 s |
| 09:15Z | PagerDuty | pessoa de plantão acionada |
| 09:30Z | Slack [recall] | reversão iniciada |
| 09:41Z | registro de implantação | imagem anterior restaurada; latência normal |

## 3. Fatores contribuintes
- código: espera ilimitada pelo conjunto de conexões (`pool`) (Cinco Porquês → tempo limite ausente)
- configuração: intervalo da verificação de integridade longo demais para detectar o bloqueio
- processo: ausência de teste de carga no fluxo de consulta alterado

## 4. O que quase funcionou
- O alerta disparou, mas com 3 minutos de atraso para evitar o impacto.

## 5. Ações
| Nº | Ação | Responsável | Tipo | Data de entrega | Verificação |
|---|--------|-------|------|----------|--------------|
| 1 | Definir tempo limite de 2 s para aquisição no conjunto de conexões | <name> | code | <date> | teste de carga demonstra falha rápida |
| 2 | Reduzir o intervalo da verificação de integridade | <name> | config | <date> | detecção < 60 s na simulação de incidente |

## 6. Riscos aceitos (por enquanto)
- Banco de dados em uma única região; configuração multirregional adiada. Responsável: <name>. Reavaliar: <quarter>.
```

## Definição de pronto

- [ ] A declaração de impacto para clientes usa linguagem simples
- [ ] A linha do tempo inclui pelo menos os horários de detecção, mitigação e resolução, com as respectivas fontes
- [ ] Existem pelo menos três fatores contribuintes em duas ou mais categorias
- [ ] Cada ação tem uma pessoa responsável, um tipo, uma data de entrega e critérios de verificação
- [ ] Pelo menos um item de "o que quase funcionou" está registrado
- [ ] Pelo menos um risco aceito está registrado com transparência
- [ ] Nenhuma pessoa é culpabilizada nominalmente, e as referências aos SLOs violados e aos `REQ-ID`s estão incluídas

## Corpo do prompt

Você é `@devops-engineer` e facilita uma análise para aprendizado, não um julgamento.

**Etapa 1: reformule o impacto pela perspectiva de clientes.**
Descreva o efeito observável, não somente o sintoma da infraestrutura interna.

**Etapa 2: reconstrua a linha do tempo.**
Registre minuto a minuto, em UTC. Cite a fonte de cada item: registro de sistema, métrica, mensagem de conversa ou lembrança humana marcada com `[recall]`.

**Etapa 3: diferencie detecção, mitigação e resolução.**
`T0` é o primeiro sintoma em produção, `Td` é a primeira detecção, `Tm` é a mitigação (fim do impacto) e `Tr` é a resolução completa.

**Etapa 4: identifique fatores contribuintes, não "a" causa.**
Use o método dos Cinco Porquês (`Five Whys`) e classifique cada fator como código, configuração, dependência, processo, observabilidade ou organização.

**Etapa 5: identifique o que quase funcionou.**
Registre as defesas ativadas que foram insuficientes, como alertas que acionaram o plantão tarde demais, guias operacionais 80% corretos ou mecanismos de contingência que atingiram o tempo limite. Essas informações são evidências valiosas para a prevenção.

**Etapa 6: proponha ações.**
Para cada fator contribuinte, escreva pelo menos uma ação com uma pessoa responsável, uma data alvo, critérios de verificação e um tipo (`code`, `config`, `monitoring`, `process`, `documentation` ou `architecture`).

**Etapa 7: mantenha a análise sem culpabilização e com transparência.**
Nunca associe um nome pessoal a um erro. Adicione pelo menos um risco que não foi corrigido, com uma pessoa responsável e uma data de reavaliação.

A RCA é um artefato de aprendizado, não de punição. Nunca há uma causa única. Todas as ações têm uma pessoa responsável, uma data e critérios de verificação. A linha do tempo é a base de evidências. Nunca a omita nem fabrique um registro.

## Exemplo de chamada

```
/incident-rca incident=<ticket-id> severity=SEV-2
```
