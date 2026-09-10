# Technical Lead — Kit do Copilot

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › **Technical Lead**

**Inventário do kit do Copilot para a persona Technical Lead.** Lista os artefatos ativos, onde ficam em `.github/` e as boas práticas específicas desse papel.

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que assume a persona Technical Lead na imersão |
| **Dupla** | 3 · Implementação (com Developer) |
| **Fase do SDLC** | Todas as fases (coordenação técnica) |
| **Pré-requisitos** | Leitura de [PERSONA.md](PERSONA.md) |
| **Resultado esperado** | Kit validado e prompts acessíveis no GitHub Copilot |

> [!IMPORTANT]
> Leia [PERSONA.md](PERSONA.md) antes de continuar. O perfil explica a missão, o handoff e as rubricas de avaliação.

---

## Conceito

O Technical Lead conecta a arquitetura ao código cotidiano. Esse papel define padrões de implementação, desbloqueia o time quando alguém encontra uma dificuldade técnica e garante que a aplicação criada pelo time realmente funcione de ponta a ponta ao final do Estágio 3. No SIFAP (Sistema de Fiscalização e Administração de Pagamentos), o TL mantém a velocidade de execução sem comprometer a qualidade ao escolher quais discussões técnicas merecem atenção.

---

## Kit da persona

| **Artefato** | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, handoff, prompts e rubrica |
| `.github/agents/tech-lead.agent.md` | Agente | Governança técnica |
| `.github/prompts/persona-technical-lead-setup-project.prompt.md` | Prompt | `/setup-project` |
| `.github/prompts/persona-technical-lead-routing-table.prompt.md` | Prompt | `/routing-table` |
| `.github/prompts/persona-technical-lead-audit-context.prompt.md` | Prompt | `/audit-context` |
| `hooks.json` | Hooks | Escopo, lint e testes |

---

## Onde ficam os artefatos

Os artefatos ativos estão consolidados no diretório `.github/` da raiz:

| **Tipo** | Caminho |
|---|---|
| Agentes | `.github/agents/` |
| Prompts | `.github/prompts/persona-*.prompt.md` |
| Skills | `.github/skills/` |
| Instruções | `.github/instructions/` |

Use esse diretório como referência. Os arquivos ativos ficam somente no diretório `.github/` da raiz. Edite-os nesse local quando houver necessidade de manutenção.

Se o kit incluir `mcp.json` e a pessoa facilitadora solicitar MCP local, copie somente esse arquivo para `.vscode/mcp.json`.

---

## Boas práticas

- Bloqueie mudanças inadequadas, não pessoas. Revise o PR e preserve o tempo de quem faz a revisão.
- `CODEMAP.md` é a memória de trabalho do time. Se estiver desatualizado, o time trabalha sem visibilidade.
- O roteamento de modelos importa: Opus para descoberta, Sonnet para implementação e Haiku para transformações mecânicas.
- O custo por feature é uma métrica de engenharia. Acompanhe-o junto com a cobertura.

---

## Referências

- [Staff Engineer — Will Larson](https://staffeng.com/)
- [The Manager's Path — Camille Fournier](https://www.oreilly.com/library/view/the-managers-path/9781491973882/)
- [Accelerate — Forsgren, Humble, Kim](https://itrevolution.com/product/accelerate/)
- [GitHub Copilot Best Practices](https://docs.github.com/en/copilot)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [OVERVIEW](../OVERVIEW.md)<br/><sub>Tabela das 10 personas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil desta persona.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
