# Matriz persona-agente

![Tipo: referência](https://img.shields.io/badge/Tipo-Refer%C3%AAncia-171717?style=flat-square)
![Uso: quem faz o quê](https://img.shields.io/badge/Uso-Quem%20faz%20o%20qu%C3%AA-737373?style=flat-square)

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Matriz persona-agente**

**Relaciona cada persona a todos os agentes de estágio** — mostra quem lidera, apoia ou observa em cada momento do dia.

| Campo | Valor |
|---|---|
| **Público-alvo** | O time inteiro |
| **Quando consultar** | No início de cada estágio e ao formar as duplas |
| **Resultado esperado** | Clareza sobre o nível de participação esperado de cada persona |

---

## Como ler esta matriz

1. Encontre a linha da sua persona.
2. Leia as colunas para ver seu nível de participação em cada estágio.
3. Nos estágios em que você for **Líder** ou **Apoio**, leia as orientações detalhadas abaixo.
4. Abra o README do kit de agente do estágio atual para ver o fluxo completo.

---

## A matriz

| # | Persona | @archaeologist | @architect | @builder | @evolution |
|---|---|---|---|---|---|
| 01 | Product Owner | Observador | Apoio | Observador | Apoio |
| 02 | Requirements Engineer | **Líder** | Apoio | Observador | Observador |
| 03 | Enterprise Architect | Apoio | Apoio | Observador | Observador |
| 04 | Software Architect | Observador | **Líder** | Apoio | Observador |
| 05 | Technical Lead | Observador | Apoio | Apoio | **Líder** |
| 06 | Developer | Observador | Observador | **Líder** | Apoio |
| 07 | DBA | Apoio | Observador | Apoio | Observador |
| 08 | QA Engineer | Observador | Observador | Apoio | Apoio |
| 09 | DevOps Engineer | Observador | Observador | Apoio | Apoio |
| 10 | Tech Writer | Apoio | Observador | Observador | Apoio |

**Líder** — orienta o uso do agente e responde pelos entregáveis do estágio.
**Apoio** — contribui ativamente e trabalha com a liderança.
**Observador** — acompanha o GitHub Copilot e está pronto para ajudar quando sua especialidade for necessária.

---

## Orientações por célula

### Estágio 1 — @archaeologist

| Persona | O que você faz |
|---|---|
| **Requirements Engineer (Líder)** | Lidera a exploração. Abre cada programa Natural, pede ajuda ao agente para decodificá-lo e captura regras de negócio como rascunhos de requisitos. Responde pelos rascunhos das regras. |
| Tech Writer (Apoio) | Constrói o glossário do domínio em tempo real. Cada novo termo, nome de variável, rótulo de campo ou finalidade de sub-rotina entra no glossário com uma definição. |
| Enterprise Architect (Apoio) | Concentra-se na visão geral: quais sistemas externos o código legado chama? De onde vêm as entradas batch? Começa a rascunhar o contexto do sistema. |
| DBA (Apoio) | Concentra-se nos DDMs (Data Definition Modules) do Adabas. Documenta tipos de campo, descritores, estruturas MU/PE e relações entre arquivos para o mapa de dados. |
| Product Owner (Observador) | Escuta e valida. Quando o time propõe uma interpretação de uma regra de negócio, confirma ou questiona com base no conhecimento do domínio. |
| Outras personas (Observadores) | Acompanham o GitHub Copilot. Contribuem quando alguém pergunta sobre um padrão de sua área, como um Developer que reconhece um cálculo. |

### Estágio 2 — @architect

| Persona | O que você faz |
|---|---|
| **Software Architect (Líder)** | Lidera a definição dos contextos delimitados. Usa o mapa de dados e o grafo de chamadas do Estágio 1 para identificar fronteiras naturais. Desenha diagramas C4. Escreve os primeiros ADRs. |
| Requirements Engineer (Apoio) | Converte as regras de negócio do Estágio 1 em requisitos EARS formais com IDs `REQ-NNN`. Todo requisito precisa de critérios de aceitação. Trabalha com o Software Architect para mapear requisitos para contextos delimitados. |
| Enterprise Architect (Apoio) | Valida o diagrama de contexto do sistema. Garante que pontos de integração, feeds batch, APIs externas e autenticação sejam capturados. Revisa a consistência arquitetural dos ADRs. |
| Product Owner (Apoio) | Prioriza requisitos. Com tempo limitado, ajuda a decidir o que é obrigatório e o que é desejável. |
| Technical Lead (Observador) | Começa a considerar a ordem de implementação. Qual contexto delimitado deve ser construído primeiro? Quais são as dependências? |
| Outras personas (Observadores) | Revisam a especificação em formação e sinalizam inconsistências de suas especialidades. |

### Estágio 3 — @builder

| Persona | O que você faz |
|---|---|
| **Developer (Líder)** | Escreve código. Usa o agente builder para gerar entidades JPA, serviços Spring, controllers REST e páginas Next.js. Cada segmento de código é rastreável a um `REQ-NNN`. |
| DBA (Apoio) | Responde pela camada de banco de dados. Revisa mapeamentos de entidades, escreve migrações Flyway e valida se o schema PostgreSQL representa corretamente o modelo de dados do Estágio 2. |
| QA Engineer (Apoio) | Escreve testes com o Developer. Para cada serviço, produz pelo menos um teste do caminho feliz e um do caminho de erro. Monitora a cobertura e sinaliza lacunas. |
| Technical Lead (Apoio) | Revisa o código à medida que é produzido. Verifica violações dos padrões: sem `@Autowired` em campo, sem retornos `null` e sem `any` em TypeScript. Integra pull requests. |
| Software Architect (Apoio) | Valida se a implementação corresponde ao design. Sinaliza cedo os desvios das fronteiras dos contextos delimitados. |
| Outras personas (Observadores) | Permanecem disponíveis para perguntas. O Developer pode precisar de um esclarecimento do domínio que somente o Product Owner ou o Requirements Engineer pode fornecer. |

### Estágio 4 — @evolution

| Persona | O que você faz |
|---|---|
| **Technical Lead (Líder)** | Escreve GitHub Issues para o Copilot Agent. Revisa pull requests gerados por IA. Decide o que integrar e rejeitar. Responde pela integração e pela preparação da demonstração. |
| DevOps Engineer (Apoio) | Escreve o workflow do GitHub Actions e os módulos Terraform. Garante tags corretas, gestão de segredos e configuração de recursos. |
| QA Engineer (Apoio) | Valida se a CI inclui todos os gates de qualidade: lint, build e teste. Revisa os resultados dos testes dos pull requests gerados por IA. |
| Developer (Apoio) | Revisa a correção do código gerado por IA. Conhece a base de código e detecta erros lógicos que as verificações automatizadas podem não encontrar. |
| Tech Writer (Apoio) | Refina o README, documenta o roteiro da demonstração e garante que as notas da retrospectiva capturem o aprendizado do time. |
| Product Owner (Apoio) | Ajuda a priorizar o que deve funcionar na demonstração e o que pode ser adiado. Prepara a narrativa da apresentação. |
| Outras personas (Observadores) | Contribuem com observações para a retrospectiva: o que surpreendeu e o que fariam de outra forma. |

---

## Ordem de leitura sugerida

- [ ] Leia o `PERSONA.md` do seu papel em [`05-personas/`](../05-personas/) — entenda suas responsabilidades.
- [ ] Leia sua linha nesta matriz — entenda sua intensidade em cada estágio.
- [ ] No início de cada estágio, abra o README do kit de agente em [`06-stage-agents/`](../06-stage-agents/).
- [ ] Ative o agente do estágio atual no GitHub Copilot e comece a trabalhar.

## Referências

- [Kits de agentes](../06-stage-agents/README.md)
- [Arquitetura dos agentes](4-agents-explained.md)
- [Kits de persona consolidados](../05-personas/)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Quatro agentes explicados](4-agents-explained.md)<br/><sub>Por que há quatro agentes.</sub> | [Fluxo do SDLC](sdlc-flow-guide.md)<br/><sub>Contratos entre duplas.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
