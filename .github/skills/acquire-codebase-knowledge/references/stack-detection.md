# Referência para detecção do conjunto de tecnologias

Carregue este arquivo quando o conjunto de tecnologias for ambíguo, por exemplo, quando houver vários arquivos de manifesto, extensões de arquivo desconhecidas ou nenhum `package.json` ou `go.mod` evidente.

---

## Arquivo de manifesto → ecossistema

| Arquivo | Ecossistema | Principais campos para leitura |
|------|-----------|--------------------|
| `package.json` | Node.js / JavaScript / TypeScript | `dependencies`, `devDependencies`, `scripts`, `main`, `type`, `engines` |
| `go.mod` | Go | Caminho do módulo, versão do Go e bloco `require` |
| `requirements.txt` | Python (pip) | Lista de pacotes com versões fixadas |
| `Pipfile` | Python (pipenv) | `[packages]`, `[dev-packages]` e versão do Python em `[requires]` |
| `pyproject.toml` | Python (poetry / uv / hatch) | `[tool.poetry.dependencies]`, `[project]`, `[build-system]` |
| `setup.py` / `setup.cfg` | Python (setuptools, legado) | `install_requires`, `python_requires` |
| `Cargo.toml` | Rust | `[dependencies]`, `[[bin]]`, `[lib]` |
| `pom.xml` | Java / Kotlin (Maven) | `<dependencies>`, `<artifactId>`, `<groupId>`, `<java.version>` |
| `build.gradle` / `build.gradle.kts` | Java / Kotlin (Gradle) | `dependencies {}`, `sourceCompatibility` |
| `composer.json` | PHP | `require`, `require-dev` |
| `Gemfile` | Ruby | Declarações `gem` e restrição de versão de `ruby` |
| `mix.exs` | Elixir | `deps/0`, `elixir: "~> X.Y"` |
| `pubspec.yaml` | Dart / Flutter | `dependencies`, `dev_dependencies`, `environment.sdk` |
| `*.csproj` | .NET / C# | `<PackageReference>`, `<TargetFramework>` |
| `*.sln` | Solução .NET | Referencia vários projetos `.csproj` |
| `deno.json` / `deno.jsonc` | Deno (ambiente de execução TypeScript) | `imports`, `tasks` |
| `bun.lockb` | Bun (ambiente de execução JavaScript) | Arquivo de bloqueio binário; verifique as dependências em `package.json` |

---

## Detecção da versão do ambiente de execução da linguagem

| Linguagem | Onde encontrar a versão |
|----------|--------------------------|
| Node.js | `.nvmrc`, `.node-version`, `engines.node` em `package.json` e Docker `FROM node:X` |
| Python | `.python-version`, `pyproject.toml [requires-python]`, Docker `FROM python:X` |
| Go | Primeira linha de `go.mod` (`go 1.21`) |
| Java | `<java.version>` em `pom.xml`, `sourceCompatibility` em `build.gradle` e Docker `FROM eclipse-temurin:X` |
| Ruby | `.ruby-version`, `Gemfile` `ruby 'X.Y.Z'` |
| Rust | Arquivo `rust-toolchain.toml` ou `rust-toolchain` |
| .NET | `<TargetFramework>` em `.csproj` (por exemplo, `net8.0`) |

---

## Detecção de estrutura de software (Node.js/TypeScript)

| Dependência em `package.json` | Estrutura de software |
|-----------------------------|-----------|
| `express` | Express.js (servidor HTTP mínimo) |
| `fastify` | Fastify (servidor HTTP de alto desempenho) |
| `next` | Next.js (SSR/SSG React; verifique os diretórios `pages/` ou `app/`) |
| `nuxt` | Nuxt.js (SSR/SSG Vue) |
| `@nestjs/core` | NestJS (estrutura de software Node.js opinativa com DI) |
| `koa` | Koa (focado em componentes intermediários, sem roteador integrado) |
| `@hapi/hapi` | Hapi |
| `@trpc/server` | tRPC (API com segurança de tipos sem esquemas REST/GraphQL) |
| `routing-controllers` | routing-controllers (camada adaptadora do Express baseada em decoradores) |
| `typeorm` | TypeORM (ORM SQL com decoradores) |
| `prisma` | Prisma (ORM com segurança de tipos; verifique `prisma/schema.prisma`) |
| `mongoose` | Mongoose (MongoDB ODM) |
| `sequelize` | Sequelize (SQL ORM) |
| `drizzle-orm` | Drizzle (ORM SQL leve) |
| `react` sem `next` | SPA React pura (verifique `react-router-dom`) |
| `vue` sem `nuxt` | SPA Vue pura |

---

## Detecção de estrutura de software (Python)

| Pacote | Estrutura de software |
|---------|-----------|
| `fastapi` | FastAPI (REST assíncrono e documentação OpenAPI automática) |
| `flask` | Flask (estrutura de software web WSGI mínima) |
| `django` | Django (com recursos integrados; verifique `settings.py`) |
| `starlette` | Starlette (ASGI, usado frequentemente como base do FastAPI) |
| `aiohttp` | aiohttp (cliente e servidor HTTP assíncronos) |
| `sqlalchemy` | SQLAlchemy (ORM SQL; verifique migrações `alembic`) |
| `alembic` | Alembic (ferramenta de migração do SQLAlchemy) |
| `pydantic` | Pydantic (validação de dados; componente central do FastAPI) |
| `celery` | Celery (fila de tarefas distribuída) |

---

## Detecção de monorepositório

Verifique estes sinais em ordem. Um monorepositório reúne vários projetos no mesmo repositório:

1. `pnpm-workspace.yaml`: espaços de trabalho do pnpm
2. `lerna.json`: monorepositório Lerna
3. `nx.json`: monorepositório Nx (verifique também `workspace.json`)
4. `turbo.json`: Turborepo
5. `rush.json`: Rush (gerenciador de monorepositórios da Microsoft)
6. `moon.yml`: Moon
7. `package.json` com `"workspaces": [...]`: espaços de trabalho do npm/yarn
8. Presença dos diretórios `packages/`, `apps/`, `libs/` ou `services/` com seus próprios arquivos `package.json`

Se um monorepositório for detectado, cada espaço de trabalho poderá ter dependências e convenções **independentes**. Mapeie cada subpacote separadamente em `STACK.md` e registre a estrutura do monorepositório em `STRUCTURE.md`.

---

## Detecção de nomes alternativos de caminho do TypeScript

Se `tsconfig.json` tiver uma chave `paths`, as importações com prefixos não relativos serão nomes alternativos. Mapeie-os antes de documentar a estrutura.

```json
// Exemplo de tsconfig.json
"paths": {
  "@/*": ["./src/*"],
  "@components/*": ["./src/components/*"],
  "@utils/*": ["./src/utils/*"]
}
```

Importações como `import { foo } from '@/utils/bar'` são resolvidas como `src/utils/bar`. Documente como `src/utils/bar`, não como `@/utils/bar`.

---

## Imagem base do Docker → ambiente de execução

Se nenhum arquivo de manifesto estiver presente, mas existir um `Dockerfile`, a linha `FROM` revelará o ambiente de execução:

| Padrão da linha FROM | Ambiente de execução |
|------------------|---------|
| `FROM node:X` | Node.js X |
| `FROM python:X` | Python X |
| `FROM golang:X` | Go X |
| `FROM eclipse-temurin:X` | Java X (JDK Eclipse Temurin) |
| `FROM mcr.microsoft.com/dotnet/aspnet:X` | .NET X |
| `FROM ruby:X` | Ruby X |
| `FROM rust:X` | Rust X |
| `FROM alpine` (isolado) | Verifique o que foi instalado por meio de `RUN apk add` |
