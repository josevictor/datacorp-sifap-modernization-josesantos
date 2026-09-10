# Agentes e personas — as duas camadas de contexto

> **Trilha:** [Kit do Time](../README.md) › [Conceitos](00-README.md) › **Agentes e personas**

**O GitHub Copilot opera com duas camadas de contexto ao mesmo tempo: a persona, que define o papel individual de cada participante, e o agente de estágio, que define o enquadramento compartilhado pelo time. Saber combiná-las é essencial para obter respostas relevantes durante a imersão.**

![Conceito 02](https://img.shields.io/badge/Conceito-02-171717?style=flat-square) ![Usado em todos os estágios](https://img.shields.io/badge/Uso-Todos%20os%20est%C3%A1gios-737373?style=flat-square) ![Duração 20 min](https://img.shields.io/badge/Dura%C3%A7%C3%A3o-20%20min-A3A3A3?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Todas as personas |
| **Pré-requisitos** | Nenhum — leia antes do Estágio 1 |
| **Tempo estimado** | 20 minutos |
| **Estágio** | Todos os estágios |
| **Resultado esperado** | Saber selecionar agente e persona e usá-los juntos no GitHub Copilot |

---

## Conceito

A imersão usa **dois tipos de agente** no Copilot:

- **Kit de persona** — contexto individual carregado por cada participante a partir de `05-personas/`. Define o papel, as habilidades e os comandos disponíveis daquela pessoa ao longo do dia.
- **Agente de estágio** — contexto compartilhado, selecionado por todo o time no início de cada estágio. Define o enquadramento temático das conversas do time com o Copilot naquele bloco de trabalho.

As duas camadas coexistem. Você nunca substitui a sua persona pelo agente de estágio — usa as duas ao mesmo tempo.

---

## Por que isso importa

Sem uma persona selecionada, o Copilot responde como um assistente genérico, sem considerar as habilidades nem as restrições do seu papel. Sem um agente de estágio, cada pessoa do time recebe respostas com enquadramentos diferentes, o que torna a consistência impossível.

Com as duas camadas ativas, o Copilot sabe ao mesmo tempo:

- **Quem está perguntando** (papel, habilidades e slash commands disponíveis)
- **Em que contexto o time está** (Estágio 1: arqueologia; Estágio 2: especificação; e assim por diante)

---

## Como elas se combinam

```mermaid
%%{init: {'theme':'neutral','themeVariables':{'fontFamily':'ui-sans-serif, system-ui, sans-serif','primaryColor':'#F5F5F5','primaryTextColor':'#171717','primaryBorderColor':'#171717','lineColor':'#525252','secondaryColor':'#FFFFFF','tertiaryColor':'#FAFAFA','background':'#FFFFFF'}}}%%
flowchart LR
    classDef step fill:#F5F5F5,stroke:#171717,color:#171717
    classDef result fill:#FFFFFF,stroke:#171717,color:#171717,stroke-width:2px
    classDef muted fill:#FAFAFA,stroke:#A3A3A3,color:#404040

    P["Kit de persona<br/><sub>05-personas/0X-name/<br/>PERSONA.md + prompts + skills</sub>"]:::step
    A["Agente de estágio<br/><sub>@archaeologist | @architect<br/>@builder | @evolution</sub>"]:::step
   C["GitHub Copilot<br/><sub>Resposta enquadrada pelo papel<br/>E pelo estágio atual</sub>"]:::result

    P --> C
    A --> C
```

---

## Camada 1 — Personas (kit individual)

Cada participante escolhe **dois papéis** (duas personas) e mantém os dois ao longo da imersão. Os arquivos de cada persona estão em [`05-personas/`](../05-personas/) e já foram consolidados em `.github/` na raiz do repositório.

| Persona | Papel na imersão | Estágio de maior atuação |
|---|---|---|
| **Product Owner** | Define o escopo e valida requisitos com o negócio | Estágios 1 e 2 |
| **Requirements Engineer** | Lê o legado e converte regras em EARS | Estágios 1 e 2 |
| **Enterprise Architect** | Fornece a visão de sistema (C4 L1 e L2) | Estágio 2 |
| **Software Architect** | Define bounded contexts e contratos de API | Estágio 2 |
| **Technical Lead** | Conduz revisões de PR e decisões de implementação | Estágios 3 e 4 |
| **Developer** | Implementa código Java e Next.js | Estágio 3 |
| **DBA** | Modela dados, escreve migrações e otimiza consultas | Estágio 3 |
| **QA Engineer** | Escreve e valida testes de equivalência | Estágio 3 |
| **DevOps Engineer** | Configura CI/CD, Terraform e Actions | Estágio 4 |
| **Tech Writer** | Documenta APIs, ADRs e runbooks | Estágios 2 e 4 |

### O que cada persona inclui

O kit de persona contém os seguintes artefatos em `05-personas/0X-name/` e em `.github/`:

| Artefato | Localização | Finalidade |
|---|---|---|
| `PERSONA.md` | `05-personas/0X-name/` | Perfil do papel: responsabilidades, entregáveis e slash commands |
| `*.prompt.md` | `.github/prompts/` | Prompts específicos do papel |
| `SKILL.md` | `.github/skills/*/` | Conhecimento de domínio ativado automaticamente |
| `*.instructions.md` | `.github/instructions/` | Regras aplicadas automaticamente a arquivos específicos |
| `mcp.json` | Raiz do repositório | Servidores MCP disponíveis para o papel |

> [!IMPORTANT]
> Leia os seus dois arquivos `PERSONA.md` antes de começar qualquer estágio. Os slash commands só funcionam quando o contexto do repositório está carregado no GitHub Copilot.

---

## Camada 2 — Agentes de estágio (kit compartilhado)

No início de cada bloco de trabalho, todo o time seleciona o mesmo agente de estágio no GitHub Copilot. Isso garante que todas as pessoas recebam respostas com o mesmo enquadramento.

| Estágio | Agente | Enquadramento temático | Papéis que lideram |
|---|---|---|---|
| Estágio 1 — Arqueologia | [`@archaeologist`](../06-stage-agents/01-archaeologist/) | Leitura e interpretação do código legado Natural/Adabas | Requirements Engineer, Tech Writer |
| Estágio 2 — Especificação | [`@architect`](../06-stage-agents/02-architect/) | Especificações EARS, ADRs e o modelo C4 | Enterprise Architect, Software Architect |
| Estágio 3 — Implementação | [`@builder`](../06-stage-agents/03-builder/) | Código Java 21, JPA, Testcontainers e Next.js 15 | Developer, DBA, QA Engineer |
| Estágio 4 — Evolução | [`@evolution`](../06-stage-agents/04-evolution/) | Delegação para o modo Agent, IaC e CI/CD | DevOps Engineer, Tech Writer |

### Diferença na prática

| Sem agente de estágio selecionado | Com agente de estágio selecionado |
|---|---|
| O Copilot responde no contexto geral do repositório | O Copilot adota o enquadramento do estágio atual |
| Cada pessoa recebe respostas com ênfases diferentes | O time recebe respostas consistentes entre si |
| Pode sugerir ações inadequadas ao momento (por exemplo, código no Estágio 1) | Ele se mantém dentro do escopo do estágio atual |

---

## Como selecioná-los

### Persona

1. Abra o GitHub Copilot no VS Code.
2. Selecione o painel de agentes (o ícone no canto do campo de mensagem).
3. Escolha na lista a persona que corresponde ao seu papel.
4. Confirme rodando um slash command do seu `PERSONA.md`. Se funcionar, a persona está ativa.

### Agente de estágio

1. No início de cada estágio, o facilitador anuncia qual agente o time vai usar.
2. Cada participante seleciona o agente no GitHub Copilot da mesma forma que a persona.
3. A persona individual continua ativa — o agente de estágio é somado ao contexto, não substituído por ele.

---

## Exemplo no SIFAP

**Cenário:** você é a Requirements Engineer no Estágio 2. O time acabou de concluir o Estágio 1.

```
1. O facilitador anuncia: "Selecionem @architect no chat."

2. Você seleciona @architect.
   Resultado: o GitHub Copilot passa a enquadrar as respostas
   no contexto de especificação e arquitetura.

3. Você usa o modo Ask para se orientar:
   "@architect, qual é a ordem recomendada para especificar
   as regras de business-rules-catalog.md?"

4. Com base na resposta, você roda o slash command do seu papel:
   /ears-convert BR-042: <regra de cálculo do benefício>
   Use CALCDSCT.NSP#L120-L198 como source_legacy.

5. O requisito EARS inclui um REQ-ID e source_legacy.
   O CI valida a rastreabilidade no PR.
```

---

## Erros comuns e como evitá-los

| Sintoma | Causa | Correção |
|---|---|---|
| O Copilot sugere código durante o Estágio 1 | Agente de estágio errado ou ausente | Selecione `@archaeologist` e confirme com o time |
| O slash command não é reconhecido | Janela do Copilot aberta fora da raiz do repositório | Reabra o VS Code na raiz do repositório |
| Respostas inconsistentes entre as pessoas do time | Cada pessoa selecionou um agente diferente | Confirme o agente ativo no início de cada estágio |
| O agente de estágio substituiu a persona | Confusão na seleção | Persona e agente de estágio são seleções independentes no painel |

---

## Checklist de ativação

- [ ] **Leia os dois arquivos `PERSONA.md` atribuídos a você.** Eles estão em `05-personas/`.
- [ ] **Teste um slash command da persona** no GitHub Copilot para confirmar que ela está ativa.
- [ ] **No início de cada estágio, selecione o agente correto** junto com o restante do time.
- [ ] **Confirme o agente ativo antes de fazer perguntas técnicas críticas.**

---

## Referências

- [Lista completa de personas](../05-personas/OVERVIEW.md)
- [Agentes de estágio](../06-stage-agents/)
- [Cartão dos 3 modos do Copilot](../09-cheat-sheets/copilot-3-modes.md)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Spec-Driven Development](01-spec-driven-development.md)<br/><sub>Por que especificar antes de codificar e o ciclo do Spec-Kit.</sub> | [Glossário visual](03-visual-glossary.md)<br/><sub>Mais de 30 termos com definição, exemplo do SIFAP e referência.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
