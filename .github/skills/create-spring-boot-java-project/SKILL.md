---
name: "create-spring-boot-java-project"
description: "Cria a estrutura inicial de um projeto Spring Boot (Java 21) por meio do start.spring.io com Maven, springdoc-openapi e ArchUnit, pronta para execução com Docker Compose. Use quando a pessoa quiser iniciar uma nova aplicação de servidor Spring Boot ou gerar um projeto inicial. Alinha-se ao conjunto de tecnologias Java 21 + Spring Boot 3.3 do kit."
---
# Criar projeto Java com Spring Boot

Crie uma nova estrutura de aplicação de servidor Spring Boot 3.3 em Java 21, fixada no conjunto de tecnologias do kit (PostgreSQL 16, Maven, springdoc-openapi, ArchUnit e Testcontainers). Execute todos os comandos no terminal integrado do VS Code, o único editor aprovado pelo kit. O comando orientado [`/create-spring-boot-java-project`](../../prompts/create-spring-boot-java-project.prompt.md) aplica as substituições específicas do kit (módulo de destino e conjunto de dependências).

> [!IMPORTANT]
> O kit usa **somente PostgreSQL 16**, sem Redis nem MongoDB. Crie a estrutura em um novo módulo `backend/`; ele ainda não existe (a equipe o cria na Etapa 3). Nunca registre credenciais no histórico do Git. Forneça-as por meio de variáveis de ambiente.

## Quando usar

- "Inicie uma nova aplicação de servidor Spring Boot para nós."
- "Crie a estrutura inicial do módulo `backend/`."
- "Gere um projeto inicial Spring Boot 3.3 em Java 21 com PostgreSQL."
- "Configure a estrutura do projeto para iniciarmos a Etapa 3."

## Pré-requisitos

Confirme se as ferramentas necessárias estão instaladas:

| Ferramenta | Finalidade |
|---|---|
| Java 21 (JDK) | Compilar e executar a aplicação |
| Docker + Docker Compose | Executar o PostgreSQL 16 localmente |
| VS Code | Editor aprovado pelo kit |

Para personalizar o nome do artefato ou o pacote-base, altere `artifactId` e `packageName` em [Baixar o modelo de projeto Spring Boot](#baixar-o-modelo-de-projeto-spring-boot). Para mudar a versão do Spring Boot, altere `bootVersion` na mesma etapa. Mantenha a versão na linha 3.3.x do kit.

## Verificar a versão do Java

```shell
java -version
```

Confirme se a saída informa Java 21.

## Baixar o modelo de projeto Spring Boot

Baixe do start.spring.io uma estrutura Maven + Java 21 com o conjunto de dependências do kit (sem Redis nem MongoDB):

```shell
curl https://start.spring.io/starter.zip \
  -d artifactId=${input:projectName:demo-java} \
  -d bootVersion=3.3.5 \
  -d dependencies=lombok,configuration-processor,web,data-jpa,postgresql,validation,testcontainers \
  -d javaVersion=21 \
  -d packageName=com.example \
  -d packaging=jar \
  -d type=maven-project \
  -o starter.zip
```

## Descompactar e limpar

```shell
unzip starter.zip -d ./${input:projectName:demo-java}
rm -f starter.zip
cd ${input:projectName:demo-java}
```

## Adicionar springdoc-openapi e ArchUnit

Insira as dependências `springdoc-openapi-starter-webmvc-ui` e `archunit-junit5` no `pom.xml`:

```xml
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
  <version>2.8.6</version>
</dependency>
<dependency>
  <groupId>com.tngtech.archunit</groupId>
  <artifactId>archunit-junit5</artifactId>
  <version>1.2.1</version>
  <scope>test</scope>
</dependency>
```

## Configurar SpringDoc e JPA

Adicione as configurações da interface do SpringDoc ao `application.properties`:

```properties
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha
```

Adicione as configurações da fonte de dados PostgreSQL e do JPA. Leia a senha de uma variável de ambiente. Nunca a fixe no código:

```properties
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost:5432/postgres
spring.datasource.username=postgres
spring.datasource.password=${POSTGRES_PASSWORD}
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

> [!NOTE]
> Use `ddl-auto=validate` (não `update`) para que as migrações versionadas do Flyway controlem o esquema, conforme [`database.instructions.md`](../../instructions/database.instructions.md). Defina `POSTGRES_PASSWORD` no terminal de comandos ou em um arquivo `.env` local ignorado pelo Git, nunca no `application.properties`.

## Adicionar Docker Compose (somente PostgreSQL 16)

Crie `compose.yaml` na raiz do projeto com um único serviço PostgreSQL 16:

```yaml
services:
  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
```

Adicione o diretório de dados ao `.gitignore`:

```gitignore
postgres_data
```

## Verificar a compilação

O Testcontainers fornece um PostgreSQL 16 real para os testes. Assim, a compilação é executada sem iniciar um banco de dados manualmente:

```shell
./mvnw clean test
```

Para executar a aplicação com um banco de dados local, inicie primeiro o serviço do Compose:

```shell
docker compose up -d
./mvnw spring-boot:run
docker compose down
```

## Modelo de saída

```markdown
### Criado
- `backend/`: estrutura Spring Boot 3.3 (Java 21, Maven)
- Dependências: web, data-jpa, postgresql, validation, testcontainers, lombok, springdoc, archunit
- `compose.yaml`: somente o serviço PostgreSQL 16

### Compilação
`./mvnw clean test` -> BUILD SUCCESS
```

## Critérios de qualidade

- [ ] A estrutura usa Spring Boot 3.3.x em Java 21 e foi gerada em um novo módulo `backend/`.
- [ ] O conjunto de dependências é o do kit; não há Redis, MongoDB nem componente inicial de armazenamento temporário (`cache`).
- [ ] Todo arquivo Docker Compose define somente um serviço PostgreSQL 16.
- [ ] Nenhuma credencial está fixada no código; a senha da fonte de dados vem de `POSTGRES_PASSWORD`.
- [ ] `./mvnw clean test` passa (BUILD SUCCESS) antes da entrega da estrutura.
