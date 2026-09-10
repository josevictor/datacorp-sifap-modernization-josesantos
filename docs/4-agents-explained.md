# Os quatro agentes do SDLC — explicados

![Tipo: conceito](https://img.shields.io/badge/Tipo-Conceito-171717?style=flat-square)
![Uso: entender os kits de agentes](https://img.shields.io/badge/Uso-Entender%20os%20kits%20de%20agentes-737373?style=flat-square)

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Quatro agentes explicados**

**Explica o raciocínio por trás dos quatro agentes de estágio** — leia quando alguém perguntar: "Por que temos agentes de estágio se cada persona já tem seu próprio kit?"

| Campo | Valor |
|---|---|
| **Público-alvo** | O time inteiro, especialmente quem usa o Copilot em equipe pela primeira vez |
| **Pré-requisitos** | Leia o `PERSONA.md` do seu papel |
| **Resultado esperado** | Entender a diferença entre um kit de persona e um kit de agente e saber qual usar em cada momento |

---

## Conceito

Um **kit de persona** responde: "Qual é o meu papel?"
Um **kit de agente** responde: "Como o time está trabalhando agora, neste estágio?"

Ambos são necessários e complementares. Uma pessoa pode assumir as personas Developer e Technical Lead, mas, no Estágio 1, ainda deve usar `@archaeologist`, pois o time inteiro está lendo o sistema legado naquele momento.

---

## Por que há quatro agentes

A imersão tem quatro modos de trabalho. Cada modo exige um comportamento diferente do Copilot.

| Estágio | Modo de trabalho | Agente | Regra principal |
|---|---|---|---|
| 1 — Arqueologia | Observar e catalogar | `@archaeologist` | Não escrever código |
| 2 — Especificação moderna | Estruturar e decidir | `@architect` | Não aceitar um requisito sem evidência do legado |
| 3 — Implementação | Construir e verificar | `@builder` | Não programar sem um REQ-ID e o teste correspondente |
| 4 — Evolução | Delegar e revisar | `@evolution` | Não aceitar um pull request gerado por IA sem revisão humana |

Um único agente teria instruções conflitantes: no Estágio 1, deve operar somente para leitura; no Estágio 3, deve editar arquivos e executar testes. Separar os agentes por estágio torna a experiência mais segura e fácil de entender.

---

## Anatomia de um agente

![Anatomia de um agente: cinco camadas (Agente + Instruções + Prompts + Skills + MCP)](../assets/agent-anatomy.svg)

| Camada | Finalidade | Exemplo |
|---|---|---|
| Agente | Define missão, ferramentas e comportamento | `@builder` sabe como implementar e testar |
| Instruções | Regras sensíveis ao tipo de arquivo | Natural/Adabas, Java, frontend |
| Prompts | Ações reutilizáveis | `/translate-natural-to-java`, `/write-ears-spec` |
| Skills | Orientações aprofundadas para uma técnica | TDD, ADR, extração de regras de negócio |
| MCP | Conecta o agente a sistemas externos | GitHub, bancos de dados e Azure, quando configurados |

---

## Como usar os agentes durante o dia

- [ ] **Comece pelo estágio, não pela preferência individual.** Consulte o cronograma em [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md).
- [ ] **Selecione o agente de estágio no GitHub Copilot.** Exemplo: `@architect` no Estágio 2.
- [ ] **Leia também seu `PERSONA.md`.** Ele descreve o que você deve observar durante esse estágio.
- [ ] **Use os prompts do estágio.** Eles transformam a conversa em um artefato verificável.
- [ ] **Pare no gate.** Avance somente quando a Definição de Pronto do estágio for atendida.

---

## Fluxo de interação

Durante o Estágio 2, o Requirements Engineer pode levar uma descoberta confirmada ao Software Architect, que coordena o estágio com `@architect`.

```text
@architect
Temos esta regra extraída do sistema legado:
"<regra confirmada>"
Ajude a estruturá-la em EARS com um REQ-ID, critérios de aceitação e source_legacy.
```

O artefato deve registrar somente as evidências do time:

```yaml
REQ-XXX:
  pattern: <EARS pattern>
  text: "<requirement>"
  source_legacy: <file:lines or [GREENFIELD] + justification>
  acceptance: "<verifiable scenario>"
```

---

## Regra: nenhuma resposta pronta sem evidência

Os agentes ensinam o caminho, mas não fornecem uma resposta pronta sem evidências. Isso protege o aprendizado e evita alucinações.

| Se você perguntar... | O agente responderá... |
|---|---|
| "Diga quais são os contextos delimitados" | "Mostre o catálogo de programas e o mapa de dados." |
| "Crie requisitos para tudo" | "Vamos começar com uma regra que tenha uma fonte no legado." |
| "Implemente esta funcionalidade sem uma especificação" | "Faltam o REQ-ID, o critério de aceitação e o `source_legacy`." |

---

## Como saber se você entendeu

Você entende o modelo quando consegue explicar estas três afirmações para outra pessoa:

1. Um kit de persona define um papel; um kit de agente define um estágio.
2. O agente de estágio muda ao longo do dia; suas duas personas permanecem as mesmas.
3. Todo artefato importante deve permanecer fora do chat, em um arquivo versionado.

---

## Referências

- [Kits de agentes](../06-stage-agents/README.md)
- [Matriz persona-agente](persona-agent-matrix.md)
- [Fluxo completo do SDLC](sdlc-flow-guide.md)
- [Kits de persona](../05-personas/README.md)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Matriz persona-agente](persona-agent-matrix.md)<br/><sub>Intensidade por persona e estágio.</sub> | [Fluxo do SDLC](sdlc-flow-guide.md)<br/><sub>Contratos entre duplas.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
