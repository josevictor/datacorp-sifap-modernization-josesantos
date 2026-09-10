# DevOps Engineer — Kit do Copilot

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › **DevOps Engineer**

**Kit de referência para a persona DevOps Engineer na imersão de modernização do SIFAP.**

![Persona](https://img.shields.io/badge/Persona-DevOps%20Engineer-171717?style=flat-square) ![Dupla 5](https://img.shields.io/badge/Dupla-5%20%C2%B7%20Opera%C3%A7%C3%B5es-404040?style=flat-square) ![Estágio 4](https://img.shields.io/badge/Est%C3%A1gio-4%20%C2%B7%20Evolu%C3%A7%C3%A3o-737373?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que assume a persona DevOps Engineer na imersão |
| **Foco** | CI/CD com GitHub Actions, infraestrutura como código com Terraform para Azure, observabilidade e resposta a incidentes |
| **Fase do SDLC** | Transversal aos Estágios 1 a 4; rascunha a CI no Estágio 3 e colabora no Estágio 4 |
| **Resultado esperado** | Pipeline verde, build reproduzível, execução local documentada e CI/IaC validada quando relevante |

Leia primeiro: [PERSONA.md](PERSONA.md).

---

## Conceito

A pessoa DevOps Engineer é responsável pelo caminho entre um commit de código e algo que funciona de forma confiável. Na imersão de modernização do SIFAP (Sistema de Fiscalização e Administração de Pagamentos), essa persona garante que qualquer máquina do time consiga iniciar o ambiente local, que o GitHub Actions valide cada PR e que o Terraform descreva a topologia-alvo no Azure, mesmo quando ela não é aplicada durante a imersão.

Por que isso importa: sem um pipeline confiável, a pessoa Developer não recebe feedback rápido, a pessoa QA Engineer não dispõe de um ambiente de testes estável e a demonstração final corre o risco de falhar por causa do ambiente, não do código.

## Kit de persona

Todos os artefatos ativos ficam no diretório `.github/` da raiz do repositório. Esta pasta serve como referência; quando precisar fazer manutenção, edite os arquivos em `.github/`.

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, estágios, prompts e rubricas de DevOps Engineer |
| `.github/agents/devops-engineer.agent.md` | Agente | CI/CD, infraestrutura como código, monitoramento e incidentes |
| `.github/prompts/persona-devops-engineer-pipeline.prompt.md` | Prompt | `/pipeline` |
| `.github/prompts/persona-devops-engineer-iac-module.prompt.md` | Prompt | `/iac-module` |
| `.github/prompts/persona-devops-engineer-incident-rca.prompt.md` | Prompt | `/incident-rca` |
| `.github/instructions/cicd.instructions.md` | Instruções | Convenções de CI/CD |
| `.github/instructions/infrastructure.instructions.md` | Instruções | Convenções de infraestrutura |

> [!TIP]
> Se a pessoa facilitadora solicitar uma configuração local de MCP e este kit tiver `mcp.json`, copie somente esse arquivo para `.vscode/mcp.json`.

## Onde ficam os artefatos ativos

- Agentes: `.github/agents/`
- Prompts: `.github/prompts/persona-*.prompt.md`
- Skills: `.github/skills/`
- Instruções: `.github/instructions/`

## Boas práticas

- [ ] **Trate tudo como código.** Infraestrutura, configuração, políticas e runbooks devem ser versionados.
- [ ] **Mantenha os pipelines abaixo de 10 minutos.** Pipelines mais longos viram gargalos; paralelize ou remova etapas redundantes.
- [ ] **Armazene segredos exclusivamente em um cofre.** Nunca use um `.env` versionado, variáveis avulsas de CI ou código-fonte.
- [ ] **Escolha a estratégia de implantação com base no custo de rollback.** Blue/green e canary resolvem problemas diferentes.

## Exemplo do SIFAP

No Estágio 3, a pessoa DevOps Engineer rascunha a estrutura do pipeline de CI para lint, testes e build conforme o protótipo criado pelo time. No Estágio 4, ajusta o workflow e valida IaC somente quando esse trabalho for relevante para a Issue delegada.

## Referências

- [Boas práticas do Terraform](https://developer.hashicorp.com/terraform/language/style)
- [Proteção do GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [Módulos verificados do Azure](https://azure.github.io/Azure-Verified-Modules/)
- [The DevOps Handbook — Gene Kim et al.](https://itrevolution.com/product/the-devops-handbook-second-edition/)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Visão geral das personas](../OVERVIEW.md)<br/><sub>Tabela das 10 personas e suas duplas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil completo da persona DevOps Engineer.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
