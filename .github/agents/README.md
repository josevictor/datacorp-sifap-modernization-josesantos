# Índice de agentes

Este diretório contém os agentes personalizados do GitHub Copilot para a imersão: **17** no total, cada um em seu próprio `<name>.agent.md`.

> [!NOTE]
> O Copilot descobre arquivos `*.agent.md` em `.github/agents/`. Invoque um agente por seu `name` com `@<name>` (por exemplo, `@archaeologist`). O `name` também vincula prompts: um arquivo `*.prompt.md` seleciona seu agente pela chave `agent:` do frontmatter. Portanto, o ID do agente é um contrato, não um rótulo.

O kit usa **duas camadas de agentes**. Este é o modelo mental central, por isso os agentes são agrupados por camada em vez de aparecerem em uma lista plana:

- **Agentes de estágio (4)**: um por estágio da imersão, usados sequencialmente durante o dia.
- **Agentes de persona (10)**: um por papel da equipe, usados pela dupla responsável por esse papel.

Outros três **agentes especialistas** ficam fora dessas duas camadas. Eles aprofundam trabalhos específicos e aparecem ao fim.

## Agentes de estágio

Quatro agentes sequenciais, um por estágio da imersão. Eles se encadeiam pela chave `handoffs:` do frontmatter: `archaeologist -> architect -> builder` passam o trabalho ao próximo; o agente terminal do Estágio 4 (`evolution`) não possui handoff.

| Estágio | Agente | Invocação | Prompts vinculados | Descrição |
| --- | --- | --- | --- | --- |
| Estágio 1 | [`archaeologist`](archaeologist.agent.md) | `@archaeologist` | 5 | Agente do Estágio 1: lê código Natural/Adabas legado, extrai regras de negócio, mapeia dependências e registra perguntas em aberto |
| Estágio 2 | [`architect`](architect.agent.md) | `@architect` | 4 | Agente do Estágio 2: define contextos delimitados, escreve especificações EARS, gera ADRs e projeta uma arquitetura de Monólito Modular |
| Estágio 3 | [`builder`](builder.agent.md) | `@builder` | 5 | Agente do Estágio 3: traduz Natural para Java, gera JPA a partir de FDTs, escreve testes de equivalência e cria REST + Next.js |
| Estágio 4 | [`evolution`](evolution.agent.md) | `@evolution` | 4 | Agente do Estágio 4: escreve GitHub Issues para o Copilot Agent, revisa PRs geradas por IA e configura CI/CD e IaC |

## Agentes de persona

Dez agentes, um por papel da equipe. O agente [`implementer`](implementer.agent.md) atende à persona Pessoa Desenvolvedora. Por isso, seus prompts se chamam `persona-developer-*`, mas se vinculam a `agent: "implementer"`.

| Agente | Invocação | Prompts vinculados | Descrição |
| --- | --- | --- | --- |
| [`product-owner`](product-owner.agent.md) | `@product-owner` | 3 | Assistente do Responsável pelo Produto para escrever especificações, refinar a lista priorizada e validar a aceitação com notação EARS e o fluxo SDD |
| [`requirements-engineer`](requirements-engineer.agent.md) | `@requirements-engineer` | 4 | Assistente do Especialista em Requisitos para notação EARS, validação de especificações e requisitos rastreáveis ao legado no fluxo SDD |
| [`enterprise-architect`](enterprise-architect.agent.md) | `@enterprise-architect` | 3 | Assistente de arquitetura corporativa para a constituição do Spec-Kit, ADRs, mapeamento de integrações externas e projeto transversal |
| [`software-architect`](software-architect.agent.md) | `@software-architect` | 3 | Assistente de arquitetura de software para CODEMAP, contextos delimitados, topologia de módulos e contratos de API |
| [`tech-lead`](tech-lead.agent.md) | `@tech-lead` | 3 | Assistente de liderança técnica para curadoria de CODEMAP e contexto, orientação de uso do Copilot e padrões de revisão de código |
| [`implementer`](implementer.agent.md) | `@implementer` | 6 | Assistente da Pessoa Desenvolvedora para Java 21 e Next.js 15: TDD, correção de bugs e refatoração com rastreabilidade de REQ-ID |
| [`dba`](dba.agent.md) | `@dba` | 4 | Assistente de banco de dados para migrações PostgreSQL, otimização de consultas, estratégia de indexação e auditoria de injeção de SQL |
| [`qa-engineer`](qa-engineer.agent.md) | `@qa-engineer` | 5 | Assistente de garantia de qualidade para geração de testes a partir de especificações, análise de lacunas de cobertura e portões de qualidade de CI |
| [`devops-engineer`](devops-engineer.agent.md) | `@devops-engineer` | 5 | Assistente do Engenheiro DevOps para esteiras do GitHub Actions, IaC Terraform, compilações de contêiner, observabilidade e análise de incidentes |
| [`tech-writer`](tech-writer.agent.md) | `@tech-writer` | 5 | Assistente do Redator Técnico para documentação de API, guias operacionais, ADRs, CODEMAP e conteúdo no estilo Diátaxis com detecção de desvios |

## Agentes especialistas

Três especialistas que não pertencem à camada de estágio nem à de persona. Nenhum possui prompts; invoque-os diretamente com `@<name>`.

| Agente | Invocação | Prompts vinculados | Descrição |
| --- | --- | --- | --- |
| [`se-ux-ui-designer`](se-ux-ui-designer.agent.md) | `@se-ux-ui-designer` | 0 | Especialista em pesquisa de UX/UI para a IU moderna do SIFAP: Jobs-to-be-Done (necessidades a atender), jornadas de usuário e especificações de acessibilidade que orientam a criação do frontend. Use para pesquisa e intenção de projeto; use @expert-react-frontend-engineer ou @implementer para escrever o código Next.js. |
| [`expert-react-frontend-engineer`](expert-react-frontend-engineer.agent.md) | `@expert-react-frontend-engineer` | 0 | Especialista aprofundado de frontend para a IU do SIFAP: React 19 + Next.js 15 App Router, limites entre servidor e cliente, Server Actions, IU otimista, acessibilidade e desempenho. Use para trabalho concentrado no frontend; use @implementer para um único item rastreável de tasks.md ou qualquer alteração de backend. |
| [`java-mcp-expert`](java-mcp-expert.agent.md) | `@java-mcp-expert` | 0 | Especialista em nova implementação de servidores Model Context Protocol (MCP) em Java com o MCP Java SDK oficial, Project Reactor e Spring Boot 3.3. Use quando a equipe ampliar a cadeia de ferramentas com um servidor MCP personalizado; a modernização do SIFAP de legado para Java pertence a @archaeologist, @architect e @builder. |

## Responsabilidade pelos prompts

Os 59 prompts em [`../prompts/`](../prompts/) vinculam-se a um agente por sua chave `agent:`:

- Todos os **59** se vinculam a um dos **14** agentes nomeados acima (estágio + persona); nenhum prompt permanece no agente genérico integrado `agent: "agent"`. As contagens por agente estão nas colunas **Prompts vinculados** das tabelas.
- Os três agentes especialistas (`se-ux-ui-designer`, `expert-react-frontend-engineer`, `java-mcp-expert`) possuem **0** prompts e são invocados diretamente.

Recalcule as contagens com `grep -h '^agent:' ../prompts/*.prompt.md | sort | uniq -c`.

## Regra de manutenção

- Renomear um agente quebra silenciosamente **todos** os prompts vinculados a ele por `agent:`. Renomeie o agente e todos os vínculos de prompts em conjunto e execute novamente o validador.
- `description` é a única chave de frontmatter estritamente exigida pelo portão; `handoffs` destina-se somente a agentes de estágio e apenas quando existe um próximo estágio.
- As seções obrigatórias do corpo (`Missão`, `Personas líderes`, `Princípios operacionais`, `O que este agente sabe`, `O que este agente NÃO sabe`, `Prompts disponíveis`, um título de `Definição de pronto`, `Antipadrões que este agente rejeita`, `Integração com o Spec-Kit`) e o schema completo estão definidos em [`../PRIMITIVE-STANDARD.md`](../PRIMITIVE-STANDARD.md) e são impostos por [`../scripts/validate-copilot-primitives.py`](../scripts/validate-copilot-primitives.py).
- Ao adicionar um agente, inclua sua linha na camada correta acima. Se um prompt precisar invocá-lo, defina o `agent:` desse prompt com este `name`.
