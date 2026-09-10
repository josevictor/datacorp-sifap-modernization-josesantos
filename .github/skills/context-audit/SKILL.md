---
name: "context-audit"
description: "Use quando uma nova pessoa da engenharia entrar na equipe, durante a integração a uma base de código desconhecida ou ao auditar se a equipe compartilha um entendimento comum. Os gatilhos incluem \"integração\", \"contexto\", \"lacuna de conhecimento\", \"fator ônibus\" e \"entendimento da equipe\"."
---
# Auditoria de contexto

## Quando usar

- "Uma nova pessoa desenvolvedora começa na segunda-feira. O que ela precisa saber na primeira semana?"
- "Audite se a equipe realmente entende por que escolhemos X."
- "Nosso fator ônibus é 1 para o módulo de faturamento. Corrija isso."

## Objetivo

Meça o entendimento compartilhado da equipe, revele o conhecimento concentrado em uma pessoa e crie um roteiro de adaptação para a primeira semana de novos integrantes.

## Perguntas da auditoria (faça-as em particular a cada integrante)

1. Você consegue desenhar a arquitetura do sistema em um quadro branco em 5 minutos?
2. Quais são as 3 invariantes mais importantes que este sistema deve preservar?
3. Onde está o código mais arriscado? Quem o entende melhor?
4. O que você nunca alteraria sem uma revisão sênior? Por quê?
5. Quais partes você evita alterar? Por quê?

Se as respostas diferirem significativamente, a equipe tem uma lacuna de contexto.

## Antipadrões

- "Nossa integração consiste apenas nos READMEs." (É insuficiente porque os READMEs omitem conhecimento tácito.)
- Um plano para a primeira semana sem programação nem operação do sistema.
- Nenhuma menção a invariantes ou modos de falha.
- Conhecimento mantido apenas por profissionais seniores de engenharia, sem registro na documentação.

## Modelo de saída

### 1. Mapa de arquitetura compartilhado (1 página)

- Diagrama Mermaid dos serviços e do fluxo de dados
- Lista de integrações externas e de seus responsáveis
- Lista de invariantes (regras de negócio que devem permanecer intactas)

### 2. Mapa de calor de riscos

```
| Módulo | Criticidade | Fator ônibus | Última refatoração | Responsável |
|----------|-------------|------------|----------------|-------|
| faturamento | alta | 1 (Alex) | há 2 anos | Alex |
| autenticação | alta | 3 | há 6 meses | equipe |
```

Qualquer linha com fator ônibus igual a 1 para um módulo de alta criticidade exige uma ação P0.

### 3. Guia operacional da primeira semana para novos integrantes

- Dia 1: leia estas 5 ADRs e execute o conjunto de serviços localmente.
- Dia 2: forme uma dupla com Alex no faturamento e envie uma melhoria de documentação.
- Dia 3: acompanhe a rotação de plantão.
- Dia 4: assuma uma tarefa inicial com revisão em dupla.
- Dia 5: faça uma retrospectiva com o Líder Técnico. O que ainda não está claro?

## Critérios de qualidade

- [ ] O mapa de arquitetura compartilhado, o mapa de calor de riscos e o guia operacional da primeira semana existem.
- [ ] Cada módulo de alta criticidade com fator ônibus igual a 1 tem uma ação de correção P0.
- [ ] O guia operacional inclui tarefas de programação e operação do sistema, não apenas leitura.
- [ ] Uma nova pessoa da engenharia consegue entregar uma alteração de baixo risco até o fim da primeira semana, com revisão em dupla.
