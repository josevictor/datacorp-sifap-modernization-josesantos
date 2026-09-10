# Pontos de verificação da investigação

Perguntas de investigação por modelo para a Fase 2 do fluxo de trabalho de aquisição de conhecimento da base de código. Em cada área do modelo, procure primeiro as respostas na saída da varredura. Depois, leia os arquivos-fonte para preencher as lacunas.

---

## 1. STACK.md: conjunto de tecnologias

- Qual é a linguagem principal e sua versão exata? (verifique `.nvmrc`, `go.mod`, `pyproject.toml` e a linha `FROM` do Docker)
- Qual gerenciador de pacotes é usado? (`npm`, `yarn`, `pnpm`, `go mod`, `pip`, `uv`)
- Quais são as principais estruturas de software do ambiente de execução? (servidor web, ORM e contêiner de DI)
- O que `dependencies` (produção) e `devDependencies` (ferramentas de desenvolvimento) contêm?
- Existe uma imagem Docker? Qual imagem base ela usa?
- Quais são os principais scripts em `package.json`, `Makefile` ou `pyproject.toml`?

## 2. STRUCTURE.md: estrutura de diretórios

- Onde fica o código-fonte? (geralmente em `src/`, `lib/` ou na raiz do projeto para Go)
- Quais são os pontos de entrada? (verifique `main` em `package.json`, `scripts.start`, `cmd/main.go` e `app.py`)
- Qual é a finalidade declarada de cada diretório de nível superior?
- Existem diretórios menos evidentes (por exemplo, `eng/`, `platform/` ou `infra/`)?
- Existem diretórios ocultos de configuração (`.github/`, `.vscode/`, `.husky/`)?
- Quais convenções de nomenclatura os diretórios seguem? (camelCase, kebab-case, organização por domínio versus por camada)

## 3. ARCHITECTURE.md: padrões

- O código é organizado por camada (controladores → serviços → repositórios) ou por funcionalidade?
- Qual é o fluxo de dados principal? Rastreie uma solicitação ou comando da entrada ao armazenamento de dados.
- Existem instâncias únicas (singletons), padrões de injeção de dependência ou requisitos explícitos de ordem de inicialização?
- Existem processos em segundo plano, filas ou componentes orientados a eventos?
- Quais padrões de projeto aparecem repetidamente? (Fábrica, Repositório, Decorador e Estratégia)

## 4. CONVENTIONS.md: padrões de código

- Qual é a convenção de nomes dos arquivos? (verifique dez ou mais arquivos: camelCase, kebab-case ou PascalCase)
- Qual é a convenção de nomes de funções e variáveis?
- Métodos e campos privados têm prefixos (por exemplo, `_methodName` ou `#field`)?
- Quais ferramentas de análise estática e formatação estão configuradas? (verifique `.eslintrc`, `.prettierrc` e `golangci.yml`)
- Quais são as configurações de rigor do TypeScript? (`strict`, `noImplicitAny` etc.)
- Como os erros são tratados em cada camada? (lançar exceção versus retornar erro estruturado)
- Qual biblioteca de registros é usada e qual é o formato das mensagens?
- Como as importações são organizadas? (exportações agrupadas, nomes alternativos de caminho e regras de agrupamento)

## 5. INTEGRATIONS.md: serviços externos

- Quais APIs externas são chamadas? (procure `axios.`, `fetch(`, `http.Get(` e URLs base em constantes)
- Como as credenciais são armazenadas e acessadas? (`.env`, gerenciador de segredos e variáveis de ambiente)
- Quais bancos de dados estão conectados? (verifique no manifesto `pg`, `mongoose`, `prisma`, `typeorm` e `sqlalchemy`)
- Existe um API gateway, service mesh ou proxy entre a aplicação e os serviços externos?
- Quais ferramentas de monitoramento ou observabilidade são usadas? (APM, Prometheus e fluxo de registros)
- Existem filas de mensagens ou barramentos de eventos? (Kafka, RabbitMQ, SQS e Pub/Sub)

## 6. TESTING.md: configuração de testes

- Qual executor de testes está configurado? (verifique `scripts.test` em `package.json`, `pytest.ini` e `go test`)
- Onde estão os arquivos de teste? (junto ao código-fonte, em `tests/` ou em `__tests__/`)
- Qual biblioteca de asserções é usada? (Jest expect, Chai ou pytest assert)
- Como as dependências externas são simuladas? (`jest.mock`, injeção de dependência ou dados de preparação, conhecidos como `fixtures`)
- Existem testes de integração que acessam serviços reais e testes unitários com simulações?
- Existe um limite de cobertura obrigatório? (verifique `jest.config.js`, `.nycrc` e `pyproject.toml`)

## 7. CONCERNS.md: problemas conhecidos

- Quantos TODOs, FIXMEs e HACKs existem no código de produção? (consulte a saída da varredura)
- Quais arquivos tiveram mais alterações no git nos últimos 90 dias? (consulte a saída da varredura)
- Existem arquivos com mais de 500 linhas que misturam várias responsabilidades?
- Algum serviço faz chamadas sequenciais que poderiam ser paralelizadas?
- Existem valores fixos (URLs, IDs ou números mágicos) que deveriam estar na configuração?
- Quais riscos de segurança existem? (falta de validação de entrada, mensagens de erro brutas expostas a clientes ou verificações de autenticação ausentes)
- Existem padrões de desempenho que não escalam? (consultas N+1 ou caches em memória em configurações com várias instâncias)
