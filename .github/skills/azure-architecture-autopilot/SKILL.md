---
name: "azure-architecture-autopilot"
description: "Use quando a pessoa quiser projetar uma infraestrutura do Azure em linguagem natural ou analisar um ambiente existente do Azure em um diagrama interativo de arquitetura, iterar e, opcionalmente, implantar. Conduz um fluxo de projeto, diagrama, revisão e implantação com um mecanismo de diagramas integrado que funciona sem conexão (mais de 605 ícones do Azure). Os gatilhos incluem \"crie X no Azure\", \"projete uma arquitetura RAG\", \"analise meus recursos do Azure\" e \"desenhe um diagrama para rg-...\". Gera Bicep, que está fora do escopo deste kit; converta qualquer projeto adotado em Terraform."
---
# Piloto automático de arquitetura do Azure

Um pipeline que projeta infraestrutura do Azure com base em linguagem natural ou analisa recursos existentes. Ele apresenta a arquitetura em um diagrama interativo e permite iterar por modificações e implantação.

> [!WARNING]
> A infraestrutura como código (IaC) deste kit usa **Terraform (provedor do Azure `~> 3.x`)**. Esta habilidade gera **Bicep**, que está **fora do escopo** das entregas do kit. Use-a somente para exploração, diagramas e referência. Converta qualquer arquitetura adotada em Terraform em `infra/` (criado pela equipe no Estágio 3), com as etiquetas obrigatórias `project`, `environment` e `owner`.

> [!NOTE]
> Esta habilidade depende de um mecanismo de diagramas Python integrado (`scripts/`, sem necessidade de instalação). As fases de implantação também exigem a interface de linha de comando (CLI) `az` e as ferramentas do Bicep. A verificação de fatos no Microsoft Docs usa as ferramentas `web_fetch` e `web_search` diretamente no agente principal.

## Quando usar

- "Crie uma arquitetura RAG no Azure."
- "Analise minha infraestrutura atual do Azure e desenhe um diagrama para rg-sifap."
- "O Foundry está lento. Como devo alterar esta arquitetura?"
- "Quero reduzir o custo ou reforçar a segurança deste projeto."

## Mecanismo de diagramas integrado

O mecanismo de diagramas está integrado à habilidade em `scripts/`. Não é necessário executar `pip install`. Os scripts Python incluídos renderizam diagramas HTML interativos com mais de 605 ícones oficiais do Azure, totalmente sem conexão. O ponto de entrada é [scripts/cli.py](scripts/cli.py), que importa [scripts/generator.py](scripts/generator.py) para renderizar HTML/SVG e [scripts/icons.py](scripts/icons.py) para obter os dados dos ícones.

## Idioma do conteúdo apresentado à pessoa

Detecte o idioma da primeira mensagem e apresente todo o conteúdo destinado à pessoa nesse idioma, incluindo perguntas, atualizações de progresso, relatórios e comentários do Bicep. Adapte os exemplos; não os copie literalmente.

## Uso de ferramentas

| Necessidade | Ferramenta | Observações |
|---|---|---|
| Buscar conteúdo de URL | `web_fetch` | Consultas ao Microsoft Docs |
| Pesquisar na Web | `web_search` | Descoberta de URLs |
| Perguntar à pessoa | `ask_user` | `choices` deve ser um array de strings |
| Subagentes | `task` | explore / task / general-purpose |
| Executar no interpretador de comandos | ferramenta de interpretador de comandos | Primeiro descubra os caminhos de `az` / `python` / `bicep` |

> [!NOTE]
> Os subagentes não podem usar `web_fetch` nem `web_search`. Verifique fatos no Microsoft Docs diretamente pelo agente principal.

## Descoberta de caminhos

`az`, `python` e `bicep` muitas vezes não estão no `PATH`. Descubra cada caminho uma vez antes de uma fase e armazene o resultado temporariamente. Não repita a descoberta em cada chamada. Prefira a descoberta direta no sistema de arquivos a apelidos do interpretador de comandos. Consulte a seção de geração de diagramas em [references/phase1-advisor.md](references/phase1-advisor.md) para ver o caminho do Python e a integração com o mecanismo incluído.

## Atualizações de progresso

Relate o progresso com linhas curtas de status no idioma da pessoa, sem emojis. Use uma linha por ação:

```text
Ação: motivo
Concluído: resultado
Aviso: detalhe a observar
Falha: causa e próxima etapa
```

## Fluxo

Há dois caminhos, escolhidos automaticamente com base na solicitação. Em caso de ambiguidade, pergunte qual a pessoa quer seguir.

### Caminho A: novo projeto

Frases de gatilho: "criar", "configurar", "implantar", "construir".

```text
Fase 1 (references/phase1-advisor.md)    Projeto interativo + diagrama
  -> Fase 2 (references/bicep-generator.md)  Geração de Bicep (fora do escopo do kit)
  -> Fase 3 (references/bicep-reviewer.md)    Revisão + verificação de compilação
  -> Fase 4 (references/phase4-deployer.md)    validação -> análise de alterações (what-if) -> implantação
```

### Caminho B: analisar e modificar

Frases de gatilho: "analisar", "recursos atuais", "examinar", "desenhar um diagrama".

```text
Fase 0 (references/phase0-scanner.md)    Exame de recursos existentes + diagrama
  -> Conversa sobre modificações (solicitação de alteração em linguagem natural)
  -> Fase 1 (references/phase1-advisor.md)   Confirmação das alterações + atualização do diagrama
  -> Fases 2 a 4, como no Caminho A
```

## Regras de transição entre fases

- Cada fase segue as instruções do respectivo arquivo `references/*.md`.
- Em toda transição, sempre informe a próxima etapa.
- Não pule fases. Em especial, nunca pule a análise de alterações (`what-if`) entre as Fases 3 e 4.
- A transição da Fase 1 para a Fase 2 exige que `01_arch_diagram_draft.html` tenha sido gerado e apresentado à pessoa. Nunca gere Bicep sem um diagrama confirmado.
- Uma modificação após a implantação retorna à Fase 1, não à Fase 0.

## Cobertura de serviços

Serviços otimizados: Microsoft Foundry, Azure OpenAI, AI Search, ADLS Gen2, Key Vault, Microsoft Fabric, Azure Data Factory, VNet / Private Endpoint e AML / AI Hub. Todos os outros serviços do Azure têm o mesmo padrão de qualidade por meio de consultas ao Microsoft Docs.

| Categoria | Tratamento | Exemplos |
|---|---|---|
| Estável | Consulte primeiro os arquivos de referência | `isHnsEnabled`, trios de endpoint privado (Private Endpoint) |
| Dinâmico | Sempre consulte o Microsoft Docs | Versão da API, disponibilidade do modelo, SKU, região |

## Arquivos de referência

| Arquivo | Função |
|---|---|
| [references/phase0-scanner.md](references/phase0-scanner.md) | Exame de recursos existentes, inferência de relações e diagrama |
| [references/phase1-advisor.md](references/phase1-advisor.md) | Projeto interativo e verificação de fatos |
| [references/bicep-generator.md](references/bicep-generator.md) | Regras de geração de Bicep (fora do escopo do kit) |
| [references/bicep-reviewer.md](references/bicep-reviewer.md) | Lista de verificação da revisão de código |
| [references/phase4-deployer.md](references/phase4-deployer.md) | validação -> análise de alterações (`what-if`) -> implantação |
| [references/service-gotchas.md](references/service-gotchas.md) | Propriedades obrigatórias e mapeamentos de Private Endpoint |
| [references/azure-dynamic-sources.md](references/azure-dynamic-sources.md) | Registro de URLs do Microsoft Docs |
| [references/azure-common-patterns.md](references/azure-common-patterns.md) | Padrões de Private Endpoint, segurança e nomenclatura |
| [references/architecture-guidance-sources.md](references/architecture-guidance-sources.md) | Fontes de orientação de arquitetura |
| [references/ai-data.md](references/ai-data.md) | Guia de serviços de IA e dados |

Exemplos de saída: [diagrama de arquitetura](assets/06-architecture-diagram.png), [recursos no portal do Azure](assets/07-azure-portal-resources.png) e [implantação concluída](assets/08-deployment-succeeded.png).

## Modelo de saída

A habilidade produz um diagrama HTML interativo e um resumo do projeto. Registre o projeto adotado para que ele possa ser convertido em Terraform:

```text
Arquitetura: <nome>
Caminho: A (novo projeto) | B (analisar + modificar)
Diagrama: 01_arch_diagram_draft.html (gerado, apresentado e confirmado)
Serviços: Foundry, AI Search, ADLS Gen2, Key Vault (Private Endpoints)
Bicep: gerado somente para referência (fora do escopo do kit)
Acompanhamento no kit: converter em Terraform em infra/ com as tags project/environment/owner
```

## Critérios de qualidade

- [ ] O caminho (A, novo projeto; B, analisar e modificar) foi escolhido ou confirmado.
- [ ] Um diagrama (`01_arch_diagram_draft.html`) foi gerado com o mecanismo integrado e apresentado antes de qualquer Bicep.
- [ ] As fases foram executadas na ordem, sem pular a análise de alterações (`what-if`) entre a revisão e a implantação.
- [ ] Os fatos dinâmicos (versão da API, SKU, região e disponibilidade do modelo) foram confirmados no Microsoft Docs.
- [ ] O conteúdo apresentado usou o idioma da pessoa e o próprio primitivo não contém emojis.
- [ ] Qualquer arquitetura adotada foi marcada para conversão em Terraform em `infra/`, pois Bicep está fora do escopo do kit.
