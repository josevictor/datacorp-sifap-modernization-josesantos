# Índice de instruções

Este diretório contém as instruções específicas por arquivo do GitHub Copilot para a imersão.

> Importante: o Copilot descobre arquivos `*.instructions.md` em `.github/instructions/` e em seus subdiretórios. Esta imersão os mantém diretamente neste diretório para facilitar a revisão do índice e dos escopos.

## Arquivos de instruções

| Arquivo | Descrição | Escopo `applyTo` |
| --- | --- | --- |
| `agent-skills.instructions.md` | Use ao criar, revisar ou depurar GitHub Copilot Agent Skills: frontmatter de SKILL.md, regra de igualdade entre nome e diretório, ajuste de descrição e divulgação progressiva. | `.github/skills/**/SKILL.md` |
| `backend.instructions.md` | Use ao implementar APIs de backend, serviços, controllers, validação de solicitações, tratamento de erros e limites de serviços de negócio. | `backend/src/main/java/**,backend/src/test/java/**` |
| `cicd.instructions.md` | Use ao criar ou revisar GitHub Actions, workflows de CI/CD, portões de pipeline YAML, verificações de build e automação de implantação. | `.github/workflows/**,.github/actions/**,**/action.yml,**/action.yaml` |
| `database.instructions.md` | Use ao escrever repositórios de banco de dados, migrações, mudanças de schema, consultas SQL, índices e alterações de dados seguras para rollback. | `backend/src/main/java/**/infrastructure/**,backend/src/main/resources/db/migration/**` |
| `draw-io.instructions.md` | Use ao criar, editar ou revisar diagramas draw.io e XML mxGraph em arquivos .drawio, .drawio.svg ou .drawio.png. | `**/*.drawio,**/*.drawio.svg,**/*.drawio.png` |
| `frontend-spec.instructions.md` | Use ao implementar ou revisar Next.js 15 App Router, TypeScript, Tailwind CSS, shadcn/ui e server components em frontend/. | `frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**,frontend/**/*.ts,frontend/**/*.tsx` |
| `frontend.instructions.md` | Use ao criar componentes de IU de frontend, páginas, interações no cliente, estado de componentes, acessibilidade e fluxos voltados às pessoas usuárias. | `frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**` |
| `infrastructure.instructions.md` | Use ao criar ou revisar infraestrutura como código, Terraform, Bicep, definições de recursos Azure e configuração de ambientes. | `infra/**,**/*.tf,**/*.bicep,compose*.yml,compose*.yaml,docker-compose*.yml,docker-compose*.yaml` |
| `java-junit5-assertions.instructions.md` | Use ao escrever ou revisar asserções JUnit 5 (Jupiter) em testes Java de backend: ordem do valor esperado, mensagens lazy, assertAll, assertThrows/assertThrowsExactly, timeouts e assertInstanceOf. | `**/*Test.java,**/*IT.java,**/*Steps.java,**/*StepDefs.java` |
| `modular-monolith.instructions.md` | Use ao projetar ou revisar arquitetura de Monólito Modular, limites de pacotes por funcionalidade, mapeamento JPA e migração Strangler Fig. | `backend/src/main/java/**,backend/pom.xml,backend/build.gradle*` |
| `natural-adabas.instructions.md` | Use ao ler código legado Natural/Adabas, padrões da linguagem, estrutura FDT, convenções de nomenclatura e fluxos batch. | `01-archaeology/legacy-sifap/**,**/*.NSP,**/*.nsp,**/*.NSN,**/*.nsn,**/*.NSS,**/*.nss,**/*.NSA,**/*.nsa,**/*.NSL,**/*.nsl,**/*.NSC,**/*.nsc,**/*.NSM,**/*.nsm,**/*.NSD,**/*.nsd,**/*.NAT,**/*.nat,**/*.CPY,**/*.cpy,**/*.DDM,**/*.ddm,**/*.jcl,**/*.JCL` |
| `requirements.instructions.md` | Use ao escrever ou revisar requisitos, especificações EARS, critérios de aceitação, rastreabilidade e requisitos fundamentados na documentação. | `docs/**/*.md,specs/**/*.md,02-modern-spec/**/*.md` |
| `security.instructions.md` | Use ao implementar ou revisar autenticação, autorização, criptografia, configuração segura, tratamento de segredos e código sensível à segurança. | `backend/src/main/java/**/auth/**,backend/src/main/java/**/security/**,backend/src/main/java/**/config/**,backend/src/main/resources/**,frontend/**/auth/**,frontend/**/middleware.ts` |
| `terraform.instructions.md` | Use para higiene geral de Terraform (layout de arquivos, variáveis, outputs, formatação, validação, testes e estado); as regras Azure do kit ficam em infrastructure.instructions.md. | `**/*.tf` |
| `tests.instructions.md` | Use ao criar ou revisar testes automatizados, estratégia de testes, specs, lacunas de cobertura, testes de regressão e portões de qualidade. | `**/*.test.*,**/*.spec.*,**/tests/**` |

## Regra de manutenção

- Todo arquivo DEVE manter um frontmatter YAML válido com exatamente os campos `description` e `applyTo` necessários.
- `applyTo` é uma única string entre aspas; vários globs são separados por vírgulas sem espaços.
- Evite `applyTo: "**"`; prefira globs específicos que correspondam aos arquivos realmente regidos pela instrução.
- Mantenha o padrão interno consistente: parágrafo introdutório -> seções temáticas -> `## Convenções` -> `## Faça / Não faça` -> `## Lista de verificação antes de abrir uma PR`.
- Ao criar uma nova área, adicione um arquivo plano `*.instructions.md` neste diretório e atualize este índice.
