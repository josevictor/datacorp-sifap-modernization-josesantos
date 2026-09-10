---
name: "create-spring-boot-java-project"
description: "Crie a estrutura inicial do backend Spring Boot do SIFAP 2.0 (Java 21 + PostgreSQL 16), delegando a mecânica à skill create-spring-boot-java-project."
argument-hint: "projectName=<artifactId>"
agent: "implementer"
tools: ["read", "edit", "search", "execute"]
---
# /create-spring-boot-java-project

## Objetivo

Criar uma nova estrutura de backend Spring Boot para o SIFAP 2.0 e configurar sua base, fixada na stack do kit: Java 21 + Spring Boot 3.3 + PostgreSQL 16. A mecânica detalhada está na skill [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md). Este prompt a aplica sem repeti-la e substitui os padrões genéricos da skill.

> [!IMPORTANT]
> `backend/` ainda não existe. Este comando o cria do zero na Etapa 3. Não pressuponha um protótipo herdado.

## Quando usar

No início da Etapa 3, quando a equipe criar o módulo `backend/` pela primeira vez.

## Pré-condições

- Java 21, Docker e Docker Compose estão instalados
- A equipe concordou com o nome do artefato e o pacote-base
- Ainda não existe um módulo `backend/`

## Entradas que a equipe deve fornecer

- `projectName`: o `artifactId` Maven do novo módulo
- O pacote-base, por exemplo, `com.sifap.<context>`
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Seguirei as etapas de criação da skill [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md)
- Substituirei os padrões para este kit: Spring Boot 3.3.x, PostgreSQL 16, sem Redis e sem MongoDB
- Gerarei o projeto em `backend/` com os starters `web, data-jpa, postgresql, validation, testcontainers` e `springdoc-openapi-starter-webmvc-ui`
- Executarei `./mvnw clean test` para confirmar que a estrutura compila

## O que não farei

- Adicionar `data-redis`, `data-mongodb` ou seus blocos de configuração
- Criar a estrutura na raiz do repositório ou usar Spring Boot 3.4.x
- Criar serviços do Docker Compose diferentes do PostgreSQL 16
- Versionar segredos; as credenciais ficam em variáveis de ambiente ou no Azure Key Vault

## Formato da saída

```markdown
### Criado
- Estrutura Spring Boot 3.3 em `backend/` (Java 21, PostgreSQL 16)
- Dependências: web, data-jpa, postgresql, validation, testcontainers, springdoc
- `docker-compose.yaml` (somente PostgreSQL 16) — opcional

### Build
`./mvnw clean test` → BUILD SUCCESS
```

## Definição de pronto

- [ ] `backend/` contém uma estrutura Spring Boot 3.3 em Java 21
- [ ] As dependências são as definidas pelo kit; Redis e MongoDB não estão presentes
- [ ] Qualquer Docker Compose contém somente PostgreSQL 16
- [ ] `./mvnw clean test` passa e nenhum segredo foi versionado

## Corpo do prompt

A skill [`create-spring-boot-java-project`](../skills/create-spring-boot-java-project/SKILL.md) define as etapas de download no start.spring.io e de configuração. Leia-a e aplique-a com as substituições do kit abaixo.

**Etapa 1 — Confirmar entradas.**
Defina o `artifactId` e o pacote-base com a equipe. Verifique se o Java 21 está disponível.

**Etapa 2 — Aplicar a skill.**
Gere o projeto conforme a skill, restrinja as dependências à stack do kit e remova Redis e MongoDB.

**Etapa 3 — Respeitar as regras do kit.**
Use Spring Boot 3.3.x e PostgreSQL 16, crie a estrutura em `backend/` e limite o Docker Compose, se houver, ao PostgreSQL 16.

**Etapa 4 — Verificar.**
Execute `./mvnw clean test` e confirme um build bem-sucedido antes da entrega.

## Exemplo de chamada

```
/create-spring-boot-java-project projectName=sifap-backend
```
