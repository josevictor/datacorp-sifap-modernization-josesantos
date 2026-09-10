---
name: "code-modernization"
description: "Use ao modernizar um sistema legado com um fluxo de trabalho disciplinado que preserve o comportamento. Os gatilhos incluem \"modernizar\", \"código legado\", \"COBOL\", \"extração de regras de negócio\" e \"reescrita com preservação de comportamento\"."
---
# Modernização de código

Use esta habilidade para orientar a modernização de sistemas legados com preservação de comportamento. O fluxo de trabalho é dividido em etapas para que a equipe entenda o sistema antes de transformá-lo.

## Quando usar

- "Planeje a modernização deste módulo legado."
- "Avalie esta base de código antes de reescrevermos qualquer coisa."
- "Extraia as regras de negócio ocultas neste programa."
- "Transforme este módulo preservando seu comportamento."

## Fluxo de trabalho

1. **Resumo**: defina o que será modernizado, por que agora, restrições, itens fora do escopo e critérios de sucesso.
2. **Avaliação**: inventarie linguagens, módulos, integrações, compilação, cobertura de testes, complexidade e riscos.
3. **Extração de regras**: transforme a lógica procedural oculta em cartões de regras de negócio com evidências do código-fonte.
4. **Mapeamento**: relacione módulos legados a domínios, pacotes e serviços de destino e à sequência de migração.
5. **Reformulação**: projete a API, o modelo de dados, o ambiente de execução e o modelo operacional de destino.
6. **Transformação**: reescreva módulo por módulo em `backend/` e `frontend/`, com testes que fixem o comportamento legado.
7. **Fortalecimento**: revise segurança, testes, tratamento de erros, observabilidade e prontidão para implantação.

## Primitivas do GitHub Copilot

| Necessidade | Primitiva |
| --- | --- |
| Descoberta aprofundada do legado | agente [`@archaeologist`](../../agents/archaeologist.agent.md) (Etapa 1) |
| Extração de regras de negócio | instrução [`/extract-business-rules`](../../prompts/stage-archaeologist-extract-business-rules.prompt.md) |
| Projeto de destino e ADRs | agente [`@architect`](../../agents/architect.agent.md) (Etapa 2) |
| Tradução de módulos e testes | agente [`@builder`](../../agents/builder.agent.md) (Etapa 3) |
| Fortalecimento de segurança e entrega | agente [`@evolution`](../../agents/evolution.agent.md) (Etapa 4) |
| Leitura segura de código legado | instruções [`natural-adabas`](../../instructions/natural-adabas.instructions.md) |

## Contrato de pastas

- `01-archaeology/legacy-sifap/**`: evidências do código-fonte e comportamento legados. Somente leitura.
- `01-archaeology/**` e `specs/<NNN>-<feature>/`: resumos, avaliações, mapas, catálogos de regras, especificações EARS e relatórios.
- `backend/**` e `frontend/**`: implementação transformada ou substituta e testes.

## Regras

- Não transforme o código antes da avaliação e da extração das regras de negócio.
- Cite arquivos-fonte nas constatações. Se os números de linha não estiverem disponíveis, cite o arquivo e explique o motivo.
- Diferencie o comportamento observado da intenção inferida.
- Prefira vários artefatos focados a um relatório excessivamente grande.
- Use testes de caracterização para preservar o comportamento legado antes de alterações intencionais.
- Não invente métricas de complexidade, custo, ambiente de execução ou risco. Use valores medidos ou declare as premissas.

## Validação

- Execute ferramentas de inventário disponíveis, como `scc`, `cloc` ou analisadores específicos da linguagem.
- Execute as suítes de testes disponíveis antes e depois da transformação.
- Para módulos transformados, forneça evidências de que os testes comparam ou fixam o comportamento legado.
- No fortalecimento, relate as constatações por gravidade com correções concretas.

## Modelo de saída

Registre cada módulo modernizado como uma nota de avaliação em `01-archaeology/`, vinculada ao destino em `backend/` ou `frontend/`:

```markdown
## Registro de modernização - <legacy module>

| Campo | Valor |
|---|---|
| Código-fonte legado | 01-archaeology/legacy-sifap/natural-programs/<FILE>.NSN |
| Módulo de destino | backend/src/main/java/<package>/ |
| Etapa alcançada | Brief / Assess / Extract / Map / Reimagine / Transform / Harden |
| Evidência de comportamento | <characterization test path> |
| Rastreia | REQ-NNN |

### Comportamento observado
- <fact drawn from the legacy code, with path:line evidence>

### Questões em aberto
- <mystery that needs human validation>
```

## Critérios de qualidade

- [ ] A avaliação e a extração das regras de negócio foram concluídas antes de qualquer transformação.
- [ ] Cada constatação cita um arquivo-fonte legado, com números de linha quando disponíveis.
- [ ] O comportamento observado está separado da intenção inferida.
- [ ] Os testes de caracterização fixam o comportamento legado antes de alterações intencionais.
- [ ] Não há métricas inventadas de complexidade, custo, ambiente de execução ou risco. Os valores são medidos ou identificados como premissas.
