---
name: "pipeline"
description: "Crie uma esteira de CI/CD robusta no GitHub Actions para o SIFAP 2.0, com controles de compilação, testes, segurança e promoção entre ambientes."
argument-hint: "target=backend|frontend|infra component=<name>"
agent: "devops-engineer"
tools: ["read", "search", "edit"]
---
# /pipeline

## Objetivo

Criar ou refatorar um fluxo de trabalho do **GitHub Actions** para o SIFAP 2.0 que compile, teste, verifique e promova artefatos de `develop` para `main` (produção) com controles explícitos de integração e entrega contínuas (CI/CD). O fluxo segue o padrão existente em `.github/workflows/ci.yml`: ações fixadas pelo SHA completo do registro de alteração, com um comentário `# vN` ao final, um bloco `permissions:` de privilégio mínimo, um grupo `concurrency` e `timeout-minutes` em cada tarefa (`job`). O artefato é entregue em `.github/workflows/`.

## Quando usar

Use quando um contexto delimitado chegar às Etapas 3 ou 4 e precisar de compilação, testes e implantação automatizados, ou quando um fluxo de trabalho existente precisar de reforço (OIDC, fixação por SHA ou assinatura).

## Pré-condições

- O componente alvo existe (`backend/`, `frontend/` ou `infra/`) ou está sendo criado nesta solicitação de integração
- Os ambientes do GitHub (`dev`, `prod`) estão configurados com as pessoas revisoras obrigatórias
- As credenciais federadas do Azure (OIDC) e o registro de contêineres estão disponíveis para o repositório

## Entradas que a equipe deve fornecer

- O alvo da esteira: serviço Java no servidor, aplicação de interface Next.js, módulo de IaC ou orquestração de ponta a ponta
- O modelo de ramificações (ramificações de funcionalidade criadas a partir de `develop`, com promoção de `develop` para `main`; consulte `00-GIT-WORKFLOW.md`)
- Os ambientes do GitHub e suas pessoas revisoras obrigatórias
- O registro de contêineres, por exemplo, Azure Container Registry, e todas as necessidades de conformidade (SBOM ou imagens assinadas)

Solicite à pessoa usuária qualquer item ausente.

## O que farei

- Lerei a habilidade [`pipeline-hardening`](../skills/pipeline-hardening/SKILL.md) e aplicarei seus controles dos níveis 1 a 3
- Escolherei os gatilhos e organizarei as tarefas por etapa (compilação, qualidade, segurança, empacotamento e implantação)
- Autenticarei no Azure com OIDC, sem segredo de principal de serviço de longa duração
- Fixarei cada ação por SHA com um comentário `# vN` e definirei um bloco `permissions:` de privilégio mínimo, um grupo `concurrency` e `timeout-minutes`, conforme `.github/workflows/ci.yml`
- Emitirei a rastreabilidade da implantação (SHA da mesclagem e `REQ-ID`s relacionados)

## O que não farei

- Inventar SHAs de ações, nomes de segredos ou endereços de registros. Os SHAs desconhecidos serão obtidos na versão publicada da ação, e os segredos serão referenciados pelo nome, nunca inseridos diretamente
- Escrever código de aplicação (`@builder`), criar módulos Terraform (`/iac-module`) ou alterar requisitos (`@requirements-engineer`)
- Armazenar um segredo do Azure no GitHub quando OIDC funcionar ou conceder `permissions: write-all`
- Fixar uma ação em uma etiqueta flutuante (`@v3`, `@main`) em vez de um SHA
- Implantar em produção sem um controle de aprovação ou inserir um segredo diretamente no YAML

## Formato da saída

O artefato principal é o YAML do fluxo de trabalho. Exemplo para um serviço no servidor:

```yaml
name: backend-ci
on:
  pull_request:
    paths: ["backend/**"]
  push:
    branches: [develop, main]
    paths: ["backend/**"]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    name: Compilar, testar e verificar
    runs-on: ubuntu-latest
    timeout-minutes: 20
    defaults:
      run:
        shell: bash
        working-directory: backend
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: "21"
          cache: maven
      - name: Compilar e testar
        run: ./mvnw -B verify
      - name: Verificar sistema de arquivos (falhar em gravidade crítica/alta)
        uses: aquasecurity/trivy-action@ed142fd0673e97e23eac54620cfb913e5ce36c25 # v0.36.0
        with:
          scan-type: fs
          severity: CRITICAL,HIGH
          exit-code: "1"

  deploy-prod:
    name: Implantar em produção
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: prod # pessoas revisoras obrigatórias exigem duas aprovações
    permissions:
      contents: read
      id-token: write # autenticação federada por OIDC; nenhum segredo do Azure armazenado
    steps:
      - name: Entrar no Azure (OIDC)
        uses: azure/login@7184910d9eb2b1c5e48f7073824a90609bb9b6d6 # v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - name: Instalar cosign e assinar a imagem pelo resumo criptográfico
        uses: sigstore/cosign-installer@398d4b0eeef1380460a10c8013a76f728fb906ac # v3
```

Acompanhe o YAML com todos os segredos e todas as variáveis obrigatórias (por nome e finalidade), as configurações de proteção de ramificação (verificações obrigatórias `build`, `quality` e `security`) e um fluxo de promoção em uma linha: solicitação de integração → `build+scan` (compilar e verificar) → `develop` → `deploy-dev` (implantar em desenvolvimento) → `main` → duas aprovações → `deploy-prod` (implantar em produção).

## Definição de pronto

- [ ] A autenticação usa OIDC e nenhum segredo do Azure é armazenado no GitHub
- [ ] Cada ação está fixada em um SHA de registro de alteração com um comentário `# vN`
- [ ] `build`, `quality` e `security` são verificações obrigatórias da solicitação de integração
- [ ] O `permissions:` de nível superior é `contents: read` e só é elevado quando uma tarefa precisa
- [ ] Um grupo `concurrency` impede duas implantações simultâneas no mesmo ambiente
- [ ] `timeout-minutes` está definido em todas as tarefas
- [ ] As implantações em produção exigem aprovações e registram o SHA da mesclagem e os `REQ-ID`s relacionados

## Corpo do prompt

Você é `@devops-engineer`. A equipe precisa de um fluxo de trabalho que corresponda exatamente às convenções de CI existentes no repositório.

**Etapa 1: carregue os controles de reforço.**
Leia a habilidade [`pipeline-hardening`](../skills/pipeline-hardening/SKILL.md) e abra `.github/workflows/ci.yml` para copiar o padrão do repositório (fixação por SHA com `# vN`, `permissions:`, `concurrency` e `timeout-minutes`).

**Etapa 2: escolha os gatilhos.**
Use `pull_request` para compilação e testes, `push` em ramificações protegidas para implantação e `workflow_dispatch` para reversão manual. Evite `pull_request_target`, exceto quando as bifurcações realmente precisarem de segredos.

**Etapa 3: organize as tarefas por etapa.**
Use `build` (compilação e testes unitários: `./mvnw -B verify` ou `pnpm install --frozen-lockfile && pnpm build && pnpm test`), `quality` (análise estática, verificação de tipos e envio da cobertura), `security` (Trivy, verificação de dependências e busca de segredos nas diferenças), `package` (criação da imagem, envio pelo resumo criptográfico, geração de um SBOM com syft e assinatura com cosign), `deploy-dev` (automático em `develop`) e `deploy-prod` (em `main`, com aprovações obrigatórias).

**Etapa 4: autentique com OIDC.**
Use `azure/login` com credenciais federadas e limite `id-token: write` somente à tarefa de implantação. Nunca armazene um segredo de principal de serviço.

**Etapa 5: fixe, armazene temporariamente e limite cada tarefa.**
Fixe cada ação por SHA com um comentário `# vN`. Armazene o Maven temporariamente (em cache) pelo resumo (`hash`) de `pom.xml` e use o armazenamento temporário (cache) do pnpm. Defina `timeout-minutes` por tarefa e um grupo `concurrency` no nível do fluxo de trabalho.

**Etapa 6: aplique os controles e a rastreabilidade.**
Torne `build`, `quality` e `security` verificações obrigatórias por meio da proteção de ramificação. Marque a imagem implantada com o SHA do registro de mesclagem e os `REQ-ID`s relacionados presentes na descrição da solicitação de integração. Exponha essas informações na descrição da implantação.

O `permissions:` de nível superior usa `contents: read` por padrão e só é elevado onde necessário. Use somente OIDC, sem segredos do Azure de longa duração e sem segredos inseridos diretamente no YAML. Todas as ações são fixadas por SHA com um comentário `# vN`, e as implantações em produção ficam protegidas por um controle de aprovação.

## Exemplo de chamada

```
/pipeline target=backend component=<service>
```
