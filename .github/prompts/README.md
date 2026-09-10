# Índice de prompts

Este diretório contém os arquivos de prompt do GitHub Copilot para a imersão.

> Importante: mantenha os arquivos `*.prompt.md` diretamente em `.github/prompts/`. O local do espaço de trabalho documentado pelo Copilot é plano (`.github/prompts/*.prompt.md`). A organização por etapa e persona é representada pelo prefixo do nome do arquivo e por este índice.

## Convenção de nomenclatura

| Prefixo | Uso |
| --- | --- |
| `stage-<agent>-<task>.prompt.md` | Prompts para agentes de etapa (`archaeologist`, `architect`, `builder`, `evolution`). |
| `persona-<persona>-<task>.prompt.md` | Prompts para kits de personas (`product-owner`, `developer`, `qa-engineer` etc.). |

## Prompts de etapa

| Agente | Arquivos |
| --- | --- |
| `archaeologist` | `stage-archaeologist-*.prompt.md` |
| `architect` | `stage-architect-*.prompt.md` |
| `builder` | `stage-builder-*.prompt.md` |
| `evolution` | `stage-evolution-*.prompt.md` |

## Prompts de persona

| Persona | Arquivos |
| --- | --- |
| Responsável pelo Produto | `persona-product-owner-*.prompt.md` |
| Engenheiro de Requisitos | `persona-requirements-engineer-*.prompt.md` |
| Arquiteto Corporativo | `persona-enterprise-architect-*.prompt.md` |
| Arquiteto de Software | `persona-software-architect-*.prompt.md` |
| Líder Técnico | `persona-technical-lead-*.prompt.md` |
| Desenvolvedor | `persona-developer-*.prompt.md` |
| DBA | `persona-dba-*.prompt.md` |
| Engenheiro de QA | `persona-qa-engineer-*.prompt.md` |
| Engenheiro de DevOps | `persona-devops-engineer-*.prompt.md` |
| Redator Técnico | `persona-tech-writer-*.prompt.md` |

## Regras de manutenção

- Todo prompt deve ter um frontmatter YAML válido.
- Prefira declarar explicitamente os campos `description`, `name`, `argument-hint` (quando houver entradas), `agent` e `tools`.
- Evite ferramentas em excesso. Use o menor conjunto necessário para a tarefa.
- As ferramentas definidas no prompt substituem, em vez de ampliar, as ferramentas do agente personalizado. Declare no próprio prompt todas as permissões necessárias.
- Prefira aliases portáveis do VS Code (`read`, `search`, `edit`, `execute`, `agent`, `web`, `todo`) a IDs específicos da implementação.
- Não especifique capacidade nem provedor no prompt. A pessoa usuária decide como executar a tarefa.
- Ao usar um agente personalizado, referencie o respectivo `name` em `.github/agents/` (por exemplo, `archaeologist`, e não o nome de exibição no corpo do arquivo).
- Ao adicionar um prompt, use um dos prefixos acima para preservar a capacidade de descoberta e a organização.
