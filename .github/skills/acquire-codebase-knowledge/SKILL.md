---
name: "acquire-codebase-knowledge"
description: "Use esta habilidade quando a pessoa pedir explicitamente para mapear ou documentar uma base de código existente, ou para orientar a integração a ela. Acione para solicitações como \"mapeie esta base de código\", \"documente esta arquitetura\", \"ajude-me a começar neste repositório\" ou \"crie a documentação da base de código\". Não acione para implementação rotineira de funcionalidades, correções de bugs ou edições pontuais, a menos que seja solicitada uma descoberta no nível do repositório."
---
# Adquirir conhecimento da base de código

Produz sete documentos preenchidos em `docs/codebase/` com tudo o que é necessário para trabalhar de modo eficaz no projeto. Documente somente o que puder ser verificado em arquivos ou na saída do terminal. Nunca deduza nem presuma.

## Quando usar

- "Mapeie esta base de código e documente sua arquitetura."
- "Ajude-me a começar neste repositório. Por onde começo?"
- "Crie a documentação da base de código para que uma pessoa nova na engenharia seja produtiva na primeira semana."
- "Documente o conjunto de tecnologias, a estrutura e as integrações deste projeto."

> [!NOTE]
> Nesta imersão, a aplicação moderna só passa a existir na Etapa 3. Portanto, direcione esta habilidade a um projeto existente ou ao próprio kit. Trate tudo em `01-archaeology/legacy-sifap/` como evidência somente leitura e nunca afirme o conteúdo de um programa ou campo legado. Registre como descobrir essas informações e siga o critério de leitura em [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md) e [`01-archaeology/legacy-sifap/HOW-TO-READ-NATURAL.md`](../../../01-archaeology/legacy-sifap/HOW-TO-READ-NATURAL.md).

## Fluxo de trabalho

Copie e acompanhe esta lista de verificação:

```text
- [ ] Fase 1: executar a varredura e ler os documentos de intenção
- [ ] Fase 2: investigar cada área da documentação
- [ ] Fase 3: preencher os sete documentos em docs/codebase/
- [ ] Fase 4: validar os documentos, apresentar as descobertas e resolver todos os itens [ASK USER]
```

## Modo de área de foco

Se a pessoa fornecer uma área de foco (por exemplo, "somente arquitetura" ou "testes e pontos de atenção"):

1. Sempre execute toda a Fase 1.
2. Primeiro, conclua integralmente os documentos da área de foco.
3. Nos documentos fora do foco que ainda não foram analisados, mantenha as seções obrigatórias e marque as informações desconhecidas como `[TODO]`.
4. Antes da saída final, ainda execute o ciclo de validação da Fase 4 nos sete documentos.

### Fase 1: fazer a varredura e ler a intenção

1. Execute o script de varredura na raiz do projeto de destino:

   ```bash
   python3 "$SKILL_ROOT/scripts/scan.py" --output docs/codebase/.codebase-scan.txt
   ```

   Em que `$SKILL_ROOT` é o caminho absoluto da pasta da habilidade. Funciona no Windows, macOS e Linux.

   **Início rápido:** se você tiver o caminho em linha:

   ```bash
   python3 /absolute/path/to/skills/acquire-codebase-knowledge/scripts/scan.py --output docs/codebase/.codebase-scan.txt
   ```

2. Procure arquivos `PRD`, `TRD`, `README`, `ROADMAP`, `SPEC` e `DESIGN` e leia-os.
3. Resuma a intenção declarada do projeto antes de ler qualquer código-fonte.

### Fase 2: investigar

Use a saída da varredura para responder às perguntas de cada um dos sete modelos. Carregue [`references/inquiry-checkpoints.md`](references/inquiry-checkpoints.md) para obter a lista completa de perguntas de cada modelo.

Se o conjunto de tecnologias for ambíguo (vários arquivos de manifesto, tipos de arquivo desconhecidos ou ausência de `package.json`), carregue [`references/stack-detection.md`](references/stack-detection.md).

### Fase 3: preencher os modelos

Copie cada modelo de `assets/templates/` para `docs/codebase/`. Preencha-os nesta ordem:

1. [STACK.md](assets/templates/STACK.md): linguagem, ambiente de execução, estruturas de software e todas as dependências
2. [STRUCTURE.md](assets/templates/STRUCTURE.md): estrutura de diretórios, pontos de entrada e arquivos principais
3. [ARCHITECTURE.md](assets/templates/ARCHITECTURE.md): camadas, padrões e fluxo de dados
4. [CONVENTIONS.md](assets/templates/CONVENTIONS.md): nomenclatura, formatação, tratamento de erros e importações
5. [INTEGRATIONS.md](assets/templates/INTEGRATIONS.md): APIs externas, bancos de dados, autenticação e monitoramento
6. [TESTING.md](assets/templates/TESTING.md): estruturas de software, organização dos arquivos e estratégia de simulações
7. [CONCERNS.md](assets/templates/CONCERNS.md): dívida técnica, bugs, riscos de segurança e gargalos de desempenho

Use `[TODO]` para tudo o que não puder ser determinado pelo código. Use `[ASK USER]` quando a resposta correta depender da intenção da equipe.

### Fase 4: validar, corrigir e verificar

Execute este ciclo obrigatório de validação antes de finalizar:

1. Valide cada documento em relação a `references/inquiry-checkpoints.md`.
2. Para cada afirmação não trivial, confirme a existência de pelo menos uma referência de evidência.
3. Se alguma seção obrigatória estiver ausente ou sem suporte:

- Corrija o documento.
- Execute a validação novamente.

4. Repita até que os sete documentos sejam aprovados.

Em seguida, apresente um resumo dos sete documentos, liste cada item `[ASK USER]` como pergunta numerada e destaque qualquer divergência entre intenção e realidade identificada na Fase 1.

Critérios de aprovação da validação:

- Nenhuma afirmação sem suporte.
- Nenhuma seção obrigatória vazia.
- Informações desconhecidas usam `[TODO]` em vez de suposições.
- Lacunas sobre a intenção da equipe estão marcadas explicitamente como `[ASK USER]`.

---

## Armadilhas

**Monorepositórios:** o `package.json` da raiz pode não conter código-fonte. Verifique `workspaces` e os diretórios `packages/` ou `apps/`. Cada espaço de trabalho pode ter dependências e convenções próprias. Mapeie cada subpacote separadamente.

**README desatualizado:** o README muitas vezes descreve a arquitetura pretendida, não a atual. Compare-o com a estrutura real de arquivos antes de tratar qualquer afirmação do README como fato.

**Nomes alternativos de caminho do TypeScript:** a configuração `paths` do `tsconfig.json` significa que importações como `@/foo` não correspondem diretamente ao sistema de arquivos. Mapeie os nomes alternativos para caminhos reais antes de documentar a estrutura.

**Saída gerada ou compilada:** nunca documente padrões de `dist/`, `build/`, `generated/`, `.next/`, `out/` ou `__pycache__/`. Esses diretórios contêm artefatos. Documente somente as convenções do código-fonte.

**O `.env.example` revela a configuração obrigatória:** segredos nunca são versionados. Leia `.env.example`, `.env.template` ou `.env.sample` para descobrir as variáveis de ambiente obrigatórias.

**`devDependencies` ≠ conjunto de tecnologias de produção:** somente `dependencies` (ou equivalente, por exemplo, `[tool.poetry.dependencies]`) é executado em produção. Documente ferramentas de análise estática, formatadores e estruturas de teste separadamente como ferramentas de desenvolvimento.

**TODOs de testes ≠ dívida de produção:** TODOs em `test/`, `tests/`, `__tests__/` ou `spec/` são lacunas de cobertura, não dívida técnica de produção. Separe-os em `CONCERNS.md`.

**Arquivos com muitas alterações = áreas frágeis:** os arquivos que mais aparecem no histórico recente do git têm maior taxa de modificação e provavelmente escondem complexidade. Sempre registre-os em `CONCERNS.md`.

---

## Antipadrões

| Antipadrão | Em vez disso |
|---------|--------------|
| "Usa Arquitetura Limpa (Clean Architecture) com camadas de Domínio/Dados." (quando esses diretórios não existem) | Declare somente o que a estrutura de diretórios realmente mostra. |
| "Este é um projeto Next.js." (sem verificar `package.json`) | Primeiro, verifique `dependencies`. Declare o que realmente existe. |
| Deduzir o banco de dados por um nome de variável como `dbUrl` | Verifique no manifesto a presença de `pg`, `mysql2`, `mongoose`, `prisma` etc. |
| Documentar padrões de nomenclatura de `dist/` ou `build/` como convenções | Use somente arquivos-fonte. |

---

## Seções ampliadas da saída da varredura

O script `scan.py` agora produz as seguintes seções além da saída original:

- **MÉTRICAS DE CÓDIGO**: total de arquivos, linhas de código por linguagem e maiores arquivos (sinais de complexidade)
- **FLUXOS AUTOMATIZADOS DE CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI etc. detectados
- **CONTÊINERES E ORQUESTRAÇÃO**: configurações de Docker, Docker Compose, Kubernetes e Vagrant
- **SEGURANÇA E CONFORMIDADE**: Snyk, Dependabot, SECURITY.md, SBOM e políticas de segurança
- **DESEMPENHO E TESTES**: configurações de medição de desempenho, marcadores de análise de desempenho e ferramentas de teste de carga

Use essas seções durante a Fase 2 para orientar as perguntas da investigação e identificar padrões específicos das ferramentas.

---

## Recursos incluídos

| Recurso | Quando carregar |
|-------|-------------|
| [`scripts/scan.py`](scripts/scan.py) | Fase 1: execute primeiro, antes de ler qualquer código (requer Python 3.8+) |
| [`references/inquiry-checkpoints.md`](references/inquiry-checkpoints.md) | Fase 2: carregue para obter as perguntas de investigação de cada modelo |
| [`references/stack-detection.md`](references/stack-detection.md) | Fase 2: somente se o conjunto de tecnologias for ambíguo |
| [`assets/templates/STACK.md`](assets/templates/STACK.md) | Fase 3, etapa 1 |
| [`assets/templates/STRUCTURE.md`](assets/templates/STRUCTURE.md) | Fase 3, etapa 2 |
| [`assets/templates/ARCHITECTURE.md`](assets/templates/ARCHITECTURE.md) | Fase 3, etapa 3 |
| [`assets/templates/CONVENTIONS.md`](assets/templates/CONVENTIONS.md) | Fase 3, etapa 4 |
| [`assets/templates/INTEGRATIONS.md`](assets/templates/INTEGRATIONS.md) | Fase 3, etapa 5 |
| [`assets/templates/TESTING.md`](assets/templates/TESTING.md) | Fase 3, etapa 6 |
| [`assets/templates/CONCERNS.md`](assets/templates/CONCERNS.md) | Fase 3, etapa 7 |

Modo de uso dos modelos:

- Modo padrão: preencha somente as "Seções principais (obrigatórias)" de cada modelo.
- Modo ampliado: adicione seções opcionais somente quando a complexidade do repositório as justificar.

## Modelo de saída

Cada um dos sete arquivos em `docs/codebase/` apresenta primeiro as afirmações e depois as evidências que as sustentam. Por exemplo, `STACK.md`:

```markdown
## Conjunto de tecnologias

| Camada | Tecnologia | Versão | Evidência |
|---|---|---|---|
| Linguagem | Java | 21 | backend/pom.xml |
| Framework | Spring Boot | 3.3.x | backend/pom.xml |
| Banco de dados | PostgreSQL | 16 | compose.yml, application.yml |

### Informações desconhecidas
- [TODO] Nenhuma camada de cache foi encontrada nos manifestos
- [ASK USER] O Redis está planejado ou a intenção é usar cache em memória?

### Evidências
- backend/pom.xml
- compose.yml
```

## Critérios de qualidade

- [ ] Existem exatamente sete arquivos em `docs/codebase/`, cada um com suas seções obrigatórias.
- [ ] Toda afirmação não trivial pode ser rastreada até um arquivo, configuração ou saída do terminal.
- [ ] Informações desconhecidas usam `[TODO]`; decisões que dependem da intenção usam `[ASK USER]`.
- [ ] Cada documento contém uma lista concreta de evidências com caminhos reais.
- [ ] Saídas geradas (`dist/`, `build/`, `.next/`) estão excluídas das afirmações sobre convenções.
- [ ] A resposta final apresenta perguntas `[ASK USER]` numeradas e cada divergência entre intenção e realidade.
