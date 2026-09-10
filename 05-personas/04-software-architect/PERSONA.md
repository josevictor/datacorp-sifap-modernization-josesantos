# Persona: Software Architect

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › [Software Architect](README.md) › **PERSONA**

**Perfil completo da persona Software Architect.** Define a missão, as responsabilidades por estágio, as ferramentas, o handoff e as rubricas de avaliação.

| Campo | Valor |
|---|---|
| **Papel** | Software Architect |
| **Dupla** | 2 · Arquitetura (com o Enterprise Architect) |
| **Estágios ativos** | Lidera a conversa com `@architect` no Estágio 2 e apoia a revisão estrutural no Estágio 3 |
| **Artefatos produzidos** | `plan.md`, `CODEMAP.md`, estrutura de pacotes Spring, ADRs de design interno |
| **Artefatos consumidos** | Evidências de dependências (EA), REQ-IDs (RE) |
| **Handoff para** | Dupla 3 (Implementação) no Estágio 2: `plan.md` claro e primeira tarefa |

![Estágio 2: Especificação](https://img.shields.io/badge/Est%C3%A1gio-2%20%C2%B7%20Especifica%C3%A7%C3%A3o-171717?style=flat-square) ![Estágio 3: Implementação](https://img.shields.io/badge/Est%C3%A1gio-3%20%C2%B7%20Implementa%C3%A7%C3%A3o-404040?style=flat-square)

---

## Conceito

O Software Architect define a estrutura interna do sistema: como os módulos são organizados, onde começam e terminam os bounded contexts (uma técnica de Domain-Driven Design para separar responsabilidades) e quais contratos são expostos entre as partes do sistema.

No mercado, esse papel é responsável por manter o sistema verdadeiramente modular. Isso significa que mudanças em um módulo não quebram outros de forma inesperada. Em um Monólito Modular (um único processo implantado com o código organizado em módulos independentes), o SA garante que a modularidade do código seja mantida mesmo sob pressão de prazo.

No SIFAP (Sistema de Fiscalização e Administração de Pagamentos), o SA define os bounded contexts do sistema moderno (por exemplo, `pagamento`, `beneficiario`, `fiscalizacao`) e como cada um é mapeado para os programas Natural legados. Essa decisão orienta todo o Estágio 3.

**Exemplo concreto do SIFAP:** o SA compara conceitos, dependências e regras confirmadas nos programas atribuídos antes de propor limites de contexto. A estrutura de módulos só é registrada quando as evidências do legado e os requisitos sustentam a decisão.

---

## Onde você atua no SDLC

```mermaid
%%{init: {'theme':'neutral','themeVariables':{'fontFamily':'ui-sans-serif, system-ui, sans-serif','primaryColor':'#F5F5F5','primaryTextColor':'#171717','primaryBorderColor':'#171717','lineColor':'#525252','secondaryColor':'#FFFFFF','tertiaryColor':'#FAFAFA','background':'#FFFFFF'}}}%%
flowchart LR
    classDef active fill:#F5F5F5,stroke:#171717,color:#171717
    classDef support fill:#FAFAFA,stroke:#A3A3A3,color:#404040
    classDef inactive fill:#FFFFFF,stroke:#E5E5E5,color:#A3A3A3

    E1["Estágio 1<br/>Arqueologia"]:::support --> E2["Estágio 2<br/>Especificação"]:::active
    E2 --> E3["Estágio 3<br/>Implementação"]:::active
    E3 --> E4["Estágio 4<br/>Evolução"]:::inactive
```

- **Recebe de:** Enterprise Architect (evidências de dependências) e Requirements Engineer (REQ-IDs)
- **Faz handoff para:** Dupla 3 (Implementação) no Estágio 2: `plan.md` claro e primeira tarefa

---

## Responsabilidades por estágio

| **Estágio** | O que você faz | Entregável que depende de você |
|---|---|---|
| **1 · Arqueologia** | Identificar conceitos recorrentes e dependências relevantes para a fatia. | Evidências para discutir os limites dos contextos |
| **2 · Especificação** | Escrever o plano técnico da feature e registrar uma decisão somente quando ela bloquear a tarefa. | `plan.md` e ADR de apoio, se necessário |
| **3 · Implementação** | Estabelecer a estrutura inicial do projeto Spring (pacotes, camadas). Revisar PRs que cruzam limites de contextos. | `pom.xml` + organização dos módulos + revisão de PRs estruturais |
| **4 · Evolução** | Validar se o PR do Agent respeita os limites. Rejeitar merges que quebrem a modularidade. | Modularidade preservada |

---

## Kit da persona

| **Artefato** | Finalidade |
|---|---|
| `.github/agents/software-architect.agent.md` | Agente do Copilot configurado para arquitetura de software |
| `/codemap` — `persona-software-architect-codemap.prompt.md` | Gera ou atualiza o `CODEMAP.md` do projeto |
| `/impl-plan` — `persona-software-architect-impl-plan.prompt.md` | Cria o plano técnico de implementação |
| `/api-validate` — `persona-software-architect-api-validate.prompt.md` | Valida os contratos de API em relação à especificação |
| `.github/instructions/backend.instructions.md` | Convenções do backend Java |
| `.github/instructions/frontend.instructions.md` | Convenções do frontend Next.js |

---

## Ferramentas e primitivas

- **Copilot Plan** para projetar esqueletos de módulos antes da implementação.
- **GitHub Spec-Kit**: `/speckit.plan` e `/speckit.analyze` para planos, contratos e consistência.
- **Mermaid / C4** para diagramas de contexto e componentes.
- Skills do kit: prompts para escolher entre padrões (pacotes hexagonais ou em camadas).

**Cartões de referência relevantes:**

- [`../../09-cheat-sheets/spec-kit-workflow.md`](../../09-cheat-sheets/spec-kit-workflow.md): `/speckit.plan`, `/speckit.tasks` e `/speckit.analyze`.
- [`../../09-cheat-sheets/model-routing.md`](../../09-cheat-sheets/model-routing.md): Claude Opus 4.6 para decisões; Sonnet 4.6 para edições em lote.

---

## Checklist de integração

- [ ] **Leia este perfil.** Conheça a missão, as responsabilidades e o handoff.
- [ ] **Abra o `README.md` do kit.** Confirme se os agentes e prompts aparecem no GitHub Copilot.
- [ ] **Identifique sua dupla.** Consulte [00-TEAM-FLOW.md](../../00-TEAM-FLOW.md).
- [ ] **Alinhe-se com o EA.** Defina onde começa e termina o escopo de cada pessoa.
- [ ] **Registre o handoff.** Saiba quem recebe `plan.md` e o que o arquivo deve conter.

---

## Como ter sucesso neste papel

- A organização dos pacotes reflete bounded contexts, não camadas técnicas.
- Seus ADRs são curtos, específicos e citam a feature correspondente em `specs/<NNN>-<feature>/` quando relevante.
- O Monólito Modular continua sendo um monólito na implantação, mas é modular no código.
- Você redesenha os limites quando há evidências, em vez de "pedir perdão depois".

---

## Erros comuns e como evitá-los

| **Sintoma** | Causa | Correção |
|---|---|---|
| Código organizado por camadas (controller/service/repository) | O SA não definiu explicitamente os bounded contexts | Crie pacotes por contexto de negócio, não por tipo técnico |
| ADR genérico e sem valor | "Usaremos Spring Boot" não é uma decisão arquitetural | Um ADR de SA responde "como organizamos X?" ou "qual padrão usamos aqui?" |
| Dois contextos importam as classes um do outro | O limite do contexto não foi respeitado | Exponha somente interfaces públicas; nunca use importações diretas entre contextos |
| Arquitetura hexagonal rígida onde ela não agrega valor | Padrão aplicado por hábito | Escolha o padrão que melhor atende ao contexto e registre a escolha |

---

## 3 exemplos de prompts

1. **(Ask)** "Com base nestes requisitos EARS, proponha hipóteses de limites de contexto. Para cada hipótese, liste evidências, entidades e dependências."
2. **(Plan)** "No projeto Spring Boot, planeje a estrutura de pacotes para um novo bounded context `notification` seguindo o padrão existente (domain/application/infrastructure)."
3. **(Ask)** "Revise este PR e identifique importações que cruzam limites de bounded contexts. Para cada violação, sugira como isolá-la."

---

## Se você ficar bloqueado

| **Situação** | O que fazer |
|---|---|
| Os bounded contexts não estão claros | Comece com evidências de coesão, acoplamento e frequência de mudança; não presuma os limites |
| A decisão sobre os limites está bloqueada | Retorne às evidências do legado e registre a questão; não crie um diagrama para substituir a confirmação |
| A equipe organizou o código por camadas em vez de contextos | Não refatore agora. Documente no ADR e corrija se houver tempo |
| Não sabe se algo pertence a domain ou application | "Se for uma regra de negócio pura, pertence a domain. Se orquestrar ações, pertence a application." |

---

## Dependências

| **Persona** | Relação | Artefato |
|---|---|---|
| Enterprise Architect | Você depende dessa persona | Evidências de dependências para o plano técnico |
| Developer | Depende de você | Estrutura de pacotes a implementar |
| Technical Lead | Depende de você | Padrões de módulos a aplicar |
| DBA | Depende de você | Limites de contextos para o modelo de dados |

---

## Como você é avaliado

- **Rubrica A2 (Especificação):** plano técnico coerente com os requisitos e as evidências.
- **Rubrica A3 (Integridade Técnica):** bounded contexts respeitados no código.
- Critério: "Nenhuma importação cruza o limite de um contexto sem justificativa."

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Enterprise Architect](../03-enterprise-architect/PERSONA.md)<br/><sub>Dupla 2 · Arquitetura · C4 + ADRs estruturais.</sub> | [Technical Lead](../05-technical-lead/PERSONA.md)<br/><sub>Dupla 3 · Implementação · padrões e revisão.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
