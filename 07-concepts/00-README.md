# 07 — Conceitos centrais da imersão

> **Trilha:** [Kit do Time](../README.md) › **Conceitos centrais**

**Este índice apresenta os conceitos essenciais da imersão de modernização do SIFAP — o que você vai aprender, em que ordem, quanto tempo leva e como cada conceito se conecta aos quatro estágios de trabalho.**

![Seção de conceitos](https://img.shields.io/badge/Se%C3%A7%C3%A3o-07%20Conceitos-171717?style=flat-square) ![Público todos](https://img.shields.io/badge/P%C3%BAblico-Todos-737373?style=flat-square) ![Leia antes do Estágio 1](https://img.shields.io/badge/Leitura-Antes%20do%20Est%C3%A1gio%201-A3A3A3?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Qualquer pessoa do time, inclusive quem não é desenvolvedor |
| **Pré-requisitos** | Nenhum — este é o ponto de partida |
| **Tempo estimado** | 60–90 min para ler todos os documentos |
| **Resultado esperado** | Vocabulário compartilhado antes do Estágio 1 |

---

## O que você vai aprender

Cada arquivo desta pasta explica um conceito técnico de forma direta, usando exemplos reais do domínio do SIFAP (Sistema de Fiscalização e Administração de Pagamentos): pagamentos, benefícios e fiscalização. Depois de lê-los, você será capaz de:

- Explicar o ciclo do Spec-Kit sem recorrer à documentação
- Distinguir um kit de persona de um agente de estágio e saber combiná-los no GitHub Copilot
- Escolher o modo certo do Copilot (Ask, Plan ou Agent) para cada situação
- Escrever ou revisar um requisito EARS com `source_legacy:`
- Escrever ou avaliar um Architecture Decision Record (ADR)

---

## Trilha de aprendizado

```mermaid
%%{init: {'theme':'neutral','themeVariables':{'fontFamily':'ui-sans-serif, system-ui, sans-serif','primaryColor':'#F5F5F5','primaryTextColor':'#171717','primaryBorderColor':'#171717','lineColor':'#525252','secondaryColor':'#FFFFFF','tertiaryColor':'#FAFAFA','background':'#FFFFFF'}}}%%
flowchart TD
    classDef step fill:#F5F5F5,stroke:#171717,color:#171717
    classDef tool fill:#FFFFFF,stroke:#525252,color:#171717
    classDef result fill:#FFFFFF,stroke:#171717,color:#171717,stroke-width:2px

    A["01 — Spec-Driven Development<br/><sub>O que é o Spec-Kit e por que especificar antes de codificar</sub>"]:::step
    B["02 — Agentes e personas<br/><sub>Duas camadas de contexto no GitHub Copilot</sub>"]:::step
    C["04 — Os 3 modos do Copilot<br/><sub>Ask · Plan · Agent e critérios de escolha</sub>"]:::step
    D["03 — Glossário visual<br/><sub>Referência com mais de 30 termos — consulte quando precisar</sub>"]:::tool
    E["05 — Notação EARS<br/><sub>Como escrever requisitos sem ambiguidade</sub>"]:::step
    F["06 — Architecture Decision Records<br/><sub>Como registrar decisões para o time do futuro</sub>"]:::step
    G["Estágio 1 — Arqueologia"]:::result

    A --> B --> C --> E --> F --> G
    D -. "consulte a qualquer momento" .-> G
```

---

## Documentos desta pasta

| # | Documento | Conceito central | Estágio principal |
|---|---|---|---|
| 01 | [Spec-Driven Development](01-spec-driven-development.md) | Ciclo do Spec-Kit: specify → plan → tasks → implement | Estágio 2 |
| 02 | [Agentes e personas](02-agents-and-personas.md) | Kit de persona individual × agente de estágio compartilhado | Todos |
| 03 | [Glossário visual](03-visual-glossary.md) | Mais de 30 termos com definição, exemplo do SIFAP e referência | Todos |
| 04 | [Os 3 modos do Copilot](04-3-copilot-modes.md) | Ask · Plan · Agent — critérios e antipadrões | Todos |
| 05 | [Notação EARS](05-ears-notation.md) | 6 padrões EARS (5 básicos + Complex), REQ-ID e `source_legacy:` | Estágio 2 |
| 06 | [Architecture Decision Records](06-architecture-decision-records.md) | Anatomia, quando escrever e o ciclo de vida do ADR | Estágio 2 |

---

## Conexão com os quatro estágios

| Estágio | Documentos de referência nesta pasta |
|---|---|
| Estágio 1 — Arqueologia | Glossário (termos do legado: Natural, DDM, MU, PE, BR-NNN) |
| Estágio 2 — Especificação | Spec-Kit, agentes, EARS, ADR, glossário (EARS, REQ-ID, source_legacy) |
| Estágio 3 — Implementação | Os 3 modos do Copilot, glossário (JPA, Flyway, Testcontainers, Controller) |
| Estágio 4 — Evolução | Os 3 modos do Copilot (modo Agent), glossário (IaC, Terraform, CI/CD) |

---

## Verifique antes de continuar

Antes de começar o Estágio 1, confirme que você consegue responder a estas perguntas sem recorrer à documentação:

- [ ] O que é o Spec-Kit e para que serve o comando `/speckit.specify`?
- [ ] Qual é a diferença entre um kit de persona (em `05-personas/`) e um agente de estágio (em `06-stage-agents/`)?
- [ ] Quando usar Ask em vez de Agent no Copilot?
- [ ] O que é EARS e por que o campo `source_legacy:` é obrigatório?
- [ ] O que é um ADR e em que situação você escreveria um?

Se você respondeu quatro das cinco, siga para [`../05-personas/`](../05-personas/) e leia os seus dois arquivos `PERSONA.md`.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Kit do Time](../README.md)<br/><sub>Hub principal da imersão.</sub> | [Spec-Driven Development](01-spec-driven-development.md)<br/><sub>Por que especificar antes de codificar e como o Spec-Kit estrutura o processo.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
