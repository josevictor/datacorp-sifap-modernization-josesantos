---
description: "Use ao criar, revisar ou depurar uma GitHub Copilot Agent Skill em .github/skills/: frontmatter de SKILL.md, regra de correspondência entre nome e diretório, ajuste da descrição para carregamento automático, divulgação progressiva e recursos incluídos."
applyTo: ".github/skills/**/SKILL.md"
---

# Agent Skills — Guia de autoria

Este arquivo é ativado ao criar ou editar um `SKILL.md` em `.github/skills/`. Ele ensina a criar uma skill que carregue de forma confiável e tenha escopo claro: schema de frontmatter com duas chaves, igualdade entre `name` e diretório, uso de `description` no carregamento automático, divulgação progressiva e inclusão de scripts e referências. Ele ensina como estruturar e empacotar uma skill, mas não decide quais skills a imersão precisa nem qual procedimento de domínio deve conter. Isso pertence ao `SKILL.md` de cada skill e a [`.github/copilot-instructions.md`](../copilot-instructions.md).

## O que é uma skill

Uma skill é uma pasta autocontida com um `SKILL.md` e recursos opcionais (scripts, referências, modelos e assets) que ensina ao Copilot uma capacidade especializada e repetível.

| Primitiva | Finalidade | Carregamento |
|---|---|---|
| Arquivo de instruções (`*.instructions.md`) | Regras permanentes para arquivos que correspondem a `applyTo` | Sempre que um arquivo correspondente está no contexto |
| Skill (`SKILL.md`) | Fluxo de trabalho ou capacidade sob demanda | Somente quando a solicitação corresponde a `description` |

As skills são portáveis entre VS Code, Copilot CLI e Copilot coding agent. O corpo e os recursos permanecem fora do contexto até serem necessários.

## Onde ficam as skills

| Local | Escopo |
|---|---|
| `.github/skills/<skill-name>/` | Este repositório; local de todas as skills da imersão |
| `~/.copilot/skills/<skill-name>/` | Pessoal; todos os seus repositórios |

Cada skill possui seu próprio diretório e ao menos um `SKILL.md`. Este arquivo rege `.github/skills/**/SKILL.md`.

## Frontmatter — Somente duas chaves

O frontmatter de `SKILL.md` aceita exatamente `name` e `description`.

```yaml
---
name: "draw-io-diagram-generator"
description: "Use ao criar, editar ou gerar diagramas draw.io (.drawio, .drawio.svg, .drawio.png), fluxogramas, diagramas de sequência ou diagramas ER."
---
```

| Campo | Obrigatório | Restrição |
|---|---|---|
| `name` | Sim | Somente letras minúsculas, números e hifens; no máximo 64 caracteres; deve ser exatamente igual ao diretório pai |
| `description` | Sim | Informa quando usar a skill; concentra palavras-chave; no máximo 1.024 caracteres |

> [!IMPORTANT]
> `name` deve ser idêntico ao nome da pasta. `.github/skills/draw-io-diagram-generator/SKILL.md` deve declarar `name: "draw-io-diagram-generator"`. Qualquer diferença faz a skill deixar de carregar silenciosamente.

> [!WARNING]
> Somente `name` e `description` pertencem ao schema. `license`, `allowed-tools`, `compatibility` e `metadata` não são reconhecidas. Não as adicione nem presuma que `LICENSE.txt` seja conectado por `license:`.

## A descrição controla o carregamento automático

O Copilot lê somente `name` e `description` durante a descoberta. Inclua:

1. O que a skill faz.
2. Quando usá-la, com gatilhos, tipos de arquivo ou frases concretas.
3. Palavras-chave que a pessoa usuária provavelmente escreverá.

```yaml
# Bom: específico
description: "Use ao criar ou gerar arquivos draw.io, fluxogramas, diagramas de sequência ou diagramas ER."

# Ruim: vago
description: "Auxiliares de diagrama"
```

Coloque o valor entre aspas. Use aspas simples quando houver gatilhos entre aspas duplas.

## Formato obrigatório do corpo

Depois do frontmatter, use um título `#` em sentence case e estas seções, na ordem:

- `## Quando invocar`: três ou quatro solicitações realistas entre aspas.
- Uma ou mais seções de procedimento com tabelas, checklists ou etapas.
- `## Modelo de saída`: bloco cercado com o artefato exato.
- `## Portão de qualidade`: checklist `- [ ]`.

Seções como `## Armadilhas`, `## Solução de problemas` e `## Referências` são opcionais quando agregarem informação.

## Divulgação progressiva

| Nível | Conteúdo carregado | Momento |
|---|---|---|
| Descoberta | Somente `name` e `description` | Sempre |
| Instruções | Corpo completo de `SKILL.md` | Quando a solicitação corresponde à descrição |
| Recursos | Scripts, referências e modelos | Quando o corpo os vincula e o Copilot segue o link |

Mantenha o corpo focado. Após cerca de 200 linhas, mova detalhes para `references/` e vincule-os. Considere 500 linhas o limite rígido.

## Inclusão de recursos

| Pasta | Conteúdo | Lido no contexto? |
|---|---|---|
| `scripts/` | Automação executável (`.py`, `.sh`, `.ts`) | Somente ao executar |
| `references/` | Documentação usada pelo Copilot para decidir | Sim, quando vinculada |
| `templates/` | Estruturas que o Copilot modifica | Sim, quando vinculadas |
| `assets/` | Arquivos estáticos emitidos sem alteração | Não |

Use `templates/` quando o Copilot editar o arquivo e `assets/` quando o emitir sem mudanças. Referencie arquivos por paths relativos, como [o validador](../skills/draw-io-diagram-generator/scripts/validate-drawio.py).

Prefira scripts a código inline regenerado quando a lógica se repetir, exigir determinismo ou merecer testes. Scripts devem oferecer `--help`, falhar com mensagens claras, não armazenar segredos e usar paths relativos.

## Como escrever skills de alto impacto

- Ensine somente o que o Copilot provavelmente erraria: convenções internas, padrões não óbvios, particularidades de versão e fluxos de domínio.
- Mantenha descrições curtas e concentradas em palavras-chave, pois todas competem pela mesma janela de descoberta.
- Registre armadilhas no formato "nunca faça X porque Y" quando o Copilot produzir um resultado incorreto.
- Prefira orientação flexível em trabalhos abertos e reserve etapas numeradas para sequências obrigatórias, como build, implantação e setup.

## Convenções

| Regra | Justificativa |
|---|---|
| Frontmatter contém somente `name` e `description` | Outras chaves são ignoradas e ocultam suposições falsas |
| `name` é exatamente igual ao diretório da skill | Divergência impede o carregamento silenciosamente |
| `description` informa quando usar a skill em até 1.024 caracteres | É o único texto lido na descoberta |
| Corpo segue invocação, procedimento, modelo de saída e portão de qualidade | Corresponde ao padrão da imersão |
| Detalhes profundos vão para `references/` após cerca de 200 linhas | Reduz o custo de contexto |
| Scripts oferecem `--help`, tratam erros e não guardam segredos | Automação incluída deve ser segura e autoexplicativa |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Use o mesmo nome na pasta e em `name` | Renomeie somente um deles |
| Escreva `description` rica em gatilhos | Use descrição vaga como "auxiliares" |
| Mantenha somente duas chaves no frontmatter | Adicione chaves fora do schema |
| Vincule arquivos incluídos por paths relativos | Fixe paths absolutos ou específicos de máquina |
| Divida skills grandes em `references/` | Deixe um `SKILL.md` ultrapassar cerca de 500 linhas |
| Inclua as quatro seções obrigatórias | Omita invocação, modelo de saída ou portão de qualidade |

## Lista de verificação antes de abrir uma PR

- [ ] O frontmatter contém somente `name` e `description`, ambos entre aspas
- [ ] `name` usa minúsculas e hifens, possui até 64 caracteres e é idêntico ao diretório pai
- [ ] `description` informa o que a skill faz e quando usá-la, em até 1.024 caracteres
- [ ] O corpo possui invocação, ao menos um procedimento, modelo de saída e portão de qualidade
- [ ] O conteúdo ensina conhecimento não óbvio, não sintaxe básica
- [ ] Scripts, referências, modelos e assets usam paths relativos
- [ ] O corpo permanece focado, sem emojis nem pragma de lint inline
