---
name: "java-mcp-server-generator"
description: "Gera um projeto completo de servidor do Protocolo de Contexto de Modelo (Model Context Protocol, MCP) em Java usando o MCP Java SDK oficial, com Maven ou Gradle e integração opcional com Spring Boot. Use quando a pessoa quiser criar, estruturar ou iniciar um servidor MCP baseado em Java que exponha ferramentas, recursos ou prompts."
---
# Gerador de servidor MCP em Java

Gere um servidor do Protocolo de Contexto de Modelo (Model Context Protocol, MCP) completo e pronto para produção em **Java 21**, usando o MCP Java SDK oficial com Maven ou Gradle. Os manipuladores são reativos (Project Reactor `Mono`) e registram eventos por SLF4J. Gere e execute tudo no VS Code, o editor aprovado pelo kit.

## Quando invocar

- "Crie um servidor MCP em Java que exponha estas ferramentas."
- "Crie a estrutura de um projeto de servidor MCP com Maven e o Java SDK oficial."
- "Inicie um servidor MCP com ferramentas, recursos e prompts."
- "Gere o esqueleto de um servidor MCP em Java baseado em Gradle."

## O que esta skill gera

| Área | Arquivos produzidos |
|---|---|
| Compilação | `pom.xml` ou `build.gradle.kts` |
| Ponto de entrada | `McpServerApplication.java` |
| Ferramentas | `tools/ToolDefinitions.java`, `tools/ToolHandlers.java` |
| Recursos | `resources/ResourceDefinitions.java`, `resources/ResourceHandlers.java` |
| Prompts | `prompts/PromptDefinitions.java`, `prompts/PromptHandlers.java` |
| Testes | `McpServerTest.java` |
| Documentação | `README.md` |

## Geração do projeto

Quando for solicitado um servidor MCP em Java, gere um projeto completo com esta estrutura:

```text
my-mcp-server/
├── pom.xml (ou build.gradle.kts)
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/mcp/
│   │   │       ├── McpServerApplication.java
│   │   │       ├── config/
│   │   │       │   └── ServerConfiguration.java
│   │   │       ├── tools/
│   │   │       │   ├── ToolDefinitions.java
│   │   │       │   └── ToolHandlers.java
│   │   │       ├── resources/
│   │   │       │   ├── ResourceDefinitions.java
│   │   │       │   └── ResourceHandlers.java
│   │   │       └── prompts/
│   │   │           ├── PromptDefinitions.java
│   │   │           └── PromptHandlers.java
│   │   └── resources/
│   │       └── application.properties (se usar Spring)
│   └── test/
│       └── java/
│           └── com/example/mcp/
│               └── McpServerTest.java
└── README.md
```

## Modelo de pom.xml do Maven

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>my-mcp-server</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <name>Meu servidor MCP</name>
    <description>Implementação de servidor Model Context Protocol</description>

    <properties>
        <java.version>21</java.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <mcp.version>0.14.1</mcp.version>
        <slf4j.version>2.0.9</slf4j.version>
        <logback.version>1.4.11</logback.version>
        <junit.version>5.10.0</junit.version>
    </properties>

    <dependencies>
        <!-- MCP Java SDK -->
        <dependency>
            <groupId>io.modelcontextprotocol.sdk</groupId>
            <artifactId>mcp</artifactId>
            <version>${mcp.version}</version>
        </dependency>

        <!-- Registros de eventos -->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>${slf4j.version}</version>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>${logback.version}</version>
        </dependency>

        <!-- Testes -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.projectreactor</groupId>
            <artifactId>reactor-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.5.0</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <transformers>
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <mainClass>com.example.mcp.McpServerApplication</mainClass>
                                </transformer>
                            </transformers>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

## Modelo de build.gradle.kts do Gradle

```kotlin
plugins {
    id("java")
    id("application")
}

group = "com.example"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
}

dependencies {
    // MCP Java SDK
    implementation("io.modelcontextprotocol.sdk:mcp:0.14.1")

    // Registros de eventos
    implementation("org.slf4j:slf4j-api:2.0.9")
    implementation("ch.qos.logback:logback-classic:1.4.11")

    // Testes
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
    testImplementation("io.projectreactor:reactor-test:3.5.0")
}

application {
    mainClass.set("com.example.mcp.McpServerApplication")
}

tasks.test {
    useJUnitPlatform()
}
```

## Modelo de McpServerApplication.java

```java
package com.example.mcp;

import com.example.mcp.tools.ToolHandlers;
import com.example.mcp.resources.ResourceHandlers;
import com.example.mcp.prompts.PromptHandlers;
import io.mcp.server.McpServer;
import io.mcp.server.McpServerBuilder;
import io.mcp.server.transport.StdioServerTransport;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.Disposable;

public class McpServerApplication {

    private static final Logger log = LoggerFactory.getLogger(McpServerApplication.class);

    public static void main(String[] args) {
        log.info("Iniciando servidor MCP...");

        try {
            McpServer server = createServer();
            StdioServerTransport transport = new StdioServerTransport();

            // Inicia o servidor
            Disposable serverDisposable = server.start(transport).subscribe();

            // Encerramento normal
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                log.info("Encerrando servidor MCP");
                serverDisposable.dispose();
                server.stop().block();
            }));

            log.info("Servidor MCP iniciado com sucesso");

            // Mantém a execução
            Thread.currentThread().join();

        } catch (Exception e) {
            log.error("Falha ao iniciar o servidor MCP", e);
            System.exit(1);
        }
    }

    private static McpServer createServer() {
        McpServer server = McpServerBuilder.builder()
            .serverInfo("my-mcp-server", "1.0.0")
            .capabilities(capabilities -> capabilities
                .tools(true)
                .resources(true)
                .prompts(true))
            .build();

        // Registra os manipuladores
        ToolHandlers.register(server);
        ResourceHandlers.register(server);
        PromptHandlers.register(server);

        return server;
    }
}
```

## Modelo de ToolDefinitions.java

```java
package com.example.mcp.tools;

import io.mcp.json.JsonSchema;
import io.mcp.server.tool.Tool;

import java.util.List;

public class ToolDefinitions {

    public static List<Tool> getTools() {
        return List.of(
            createGreetTool(),
            createCalculateTool()
        );
    }

    private static Tool createGreetTool() {
        return Tool.builder()
            .name("greet")
            .description("Gera uma mensagem de saudação")
            .inputSchema(JsonSchema.object()
                .property("name", JsonSchema.string()
                    .description("Nome da pessoa a cumprimentar")
                    .required(true)))
            .build();
    }

    private static Tool createCalculateTool() {
        return Tool.builder()
            .name("calculate")
            .description("Executa cálculos matemáticos")
            .inputSchema(JsonSchema.object()
                .property("operation", JsonSchema.string()
                    .description("Operação a executar")
                    .enumValues(List.of("add", "subtract", "multiply", "divide"))
                    .required(true))
                .property("a", JsonSchema.number()
                    .description("Primeiro operando")
                    .required(true))
                .property("b", JsonSchema.number()
                    .description("Segundo operando")
                    .required(true)))
            .build();
    }
}
```

## Modelo de ToolHandlers.java

```java
package com.example.mcp.tools;

import com.fasterxml.jackson.databind.JsonNode;
import io.mcp.server.McpServer;
import io.mcp.server.tool.ToolResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.Mono;

public class ToolHandlers {

    private static final Logger log = LoggerFactory.getLogger(ToolHandlers.class);

    public static void register(McpServer server) {
        // Registra o manipulador da lista de ferramentas
        server.addToolListHandler(() -> {
            log.debug("Listando ferramentas disponíveis");
            return Mono.just(ToolDefinitions.getTools());
        });

        // Registra o manipulador de saudação
        server.addToolHandler("greet", ToolHandlers::handleGreet);

        // Registra o manipulador de cálculo
        server.addToolHandler("calculate", ToolHandlers::handleCalculate);
    }

    private static Mono<ToolResponse> handleGreet(JsonNode arguments) {
        log.info("Ferramenta de saudação chamada");

        if (!arguments.has("name")) {
            return Mono.just(ToolResponse.error()
                .message("Parâmetro 'name' ausente")
                .build());
        }

        String name = arguments.get("name").asText();
        String greeting = "Olá, " + name + "! Boas-vindas ao MCP.";

        log.debug("Saudação gerada para: {}", name);

        return Mono.just(ToolResponse.success()
            .addTextContent(greeting)
            .build());
    }

    private static Mono<ToolResponse> handleCalculate(JsonNode arguments) {
        log.info("Ferramenta de cálculo chamada");

        if (!arguments.has("operation") || !arguments.has("a") || !arguments.has("b")) {
            return Mono.just(ToolResponse.error()
                .message("Parâmetros obrigatórios ausentes")
                .build());
        }

        String operation = arguments.get("operation").asText();
        double a = arguments.get("a").asDouble();
        double b = arguments.get("b").asDouble();

        double result;
        switch (operation) {
            case "add":
                result = a + b;
                break;
            case "subtract":
                result = a - b;
                break;
            case "multiply":
                result = a * b;
                break;
            case "divide":
                if (b == 0) {
                    return Mono.just(ToolResponse.error()
                        .message("Divisão por zero")
                        .build());
                }
                result = a / b;
                break;
            default:
                return Mono.just(ToolResponse.error()
                    .message("Operação desconhecida: " + operation)
                    .build());
        }

        log.debug("Cálculo: {} {} {} = {}", a, operation, b, result);

        return Mono.just(ToolResponse.success()
            .addTextContent("Resultado: " + result)
            .build());
    }
}
```

## Modelo de ResourceDefinitions.java

```java
package com.example.mcp.resources;

import io.mcp.server.resource.Resource;

import java.util.List;

public class ResourceDefinitions {

    public static List<Resource> getResources() {
        return List.of(
            Resource.builder()
                .name("Dados de exemplo")
                .uri("resource://data/example")
                .description("Dados do recurso de exemplo")
                .mimeType("application/json")
                .build(),
            Resource.builder()
                .name("Configuração")
                .uri("resource://config")
                .description("Configuração do servidor")
                .mimeType("application/json")
                .build()
        );
    }
}
```

## Modelo de ResourceHandlers.java

```java
package com.example.mcp.resources;

import io.mcp.server.McpServer;
import io.mcp.server.resource.ResourceContent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.Mono;

import java.time.Instant;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class ResourceHandlers {

    private static final Logger log = LoggerFactory.getLogger(ResourceHandlers.class);
    private static final Map<String, Boolean> subscriptions = new ConcurrentHashMap<>();

    public static void register(McpServer server) {
        // Registra o manipulador da lista de recursos
        server.addResourceListHandler(() -> {
            log.debug("Listando recursos disponíveis");
            return Mono.just(ResourceDefinitions.getResources());
        });

        // Registra o manipulador de leitura de recurso
        server.addResourceReadHandler(ResourceHandlers::handleRead);

        // Registra o manipulador de assinatura de recurso
        server.addResourceSubscribeHandler(ResourceHandlers::handleSubscribe);

        // Registra o manipulador de cancelamento da assinatura do recurso
        server.addResourceUnsubscribeHandler(ResourceHandlers::handleUnsubscribe);
    }

    private static Mono<ResourceContent> handleRead(String uri) {
        log.info("Lendo recurso: {}", uri);

        switch (uri) {
            case "resource://data/example":
                String jsonData = String.format(
                    "{\"message\":\"Dados do recurso de exemplo\",\"timestamp\":\"%s\"}",
                    Instant.now()
                );
                return Mono.just(ResourceContent.text(jsonData, uri, "application/json"));

            case "resource://config":
                String config = "{\"serverName\":\"my-mcp-server\",\"version\":\"1.0.0\"}";
                return Mono.just(ResourceContent.text(config, uri, "application/json"));

            default:
                log.warn("Recurso desconhecido solicitado: {}", uri);
                return Mono.error(new IllegalArgumentException("URI de recurso desconhecido: " + uri));
        }
    }

    private static Mono<Void> handleSubscribe(String uri) {
        log.info("Cliente assinou o recurso: {}", uri);
        subscriptions.put(uri, true);
        return Mono.empty();
    }

    private static Mono<Void> handleUnsubscribe(String uri) {
        log.info("Cliente cancelou a assinatura do recurso: {}", uri);
        subscriptions.remove(uri);
        return Mono.empty();
    }
}
```

## Modelo de PromptDefinitions.java

```java
package com.example.mcp.prompts;

import io.mcp.server.prompt.Prompt;
import io.mcp.server.prompt.PromptArgument;

import java.util.List;

public class PromptDefinitions {

    public static List<Prompt> getPrompts() {
        return List.of(
            Prompt.builder()
                .name("code-review")
                .description("Gera um prompt de revisão de código")
                .argument(PromptArgument.builder()
                    .name("language")
                    .description("Linguagem de programação")
                    .required(true)
                    .build())
                .argument(PromptArgument.builder()
                    .name("focus")
                    .description("Área de foco da revisão")
                    .required(false)
                    .build())
                .build()
        );
    }
}
```

## Modelo de PromptHandlers.java

```java
package com.example.mcp.prompts;

import io.mcp.server.McpServer;
import io.mcp.server.prompt.PromptMessage;
import io.mcp.server.prompt.PromptResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

public class PromptHandlers {

    private static final Logger log = LoggerFactory.getLogger(PromptHandlers.class);

    public static void register(McpServer server) {
        // Registra o manipulador da lista de prompts
        server.addPromptListHandler(() -> {
            log.debug("Listando prompts disponíveis");
            return Mono.just(PromptDefinitions.getPrompts());
        });

        // Registra o manipulador de obtenção de prompt
        server.addPromptGetHandler(PromptHandlers::handleCodeReview);
    }

    private static Mono<PromptResult> handleCodeReview(String name, Map<String, String> arguments) {
        log.info("Obtendo prompt: {}", name);

        if (!name.equals("code-review")) {
            return Mono.error(new IllegalArgumentException("Prompt desconhecido: " + name));
        }

        String language = arguments.getOrDefault("language", "Java");
        String focus = arguments.getOrDefault("focus", "qualidade geral");

        String description = "Revisão de código " + language + " com foco em " + focus;

        List<PromptMessage> messages = List.of(
            PromptMessage.user("Revise este código " + language + " com foco em " + focus + "."),
            PromptMessage.assistant("Revisarei o código com foco em " + focus + ". Compartilhe o código."),
            PromptMessage.user("Este é o código para revisão: [cole o código aqui]")
        );

        log.debug("Prompt de revisão de código gerado para {} ({})", language, focus);

        return Mono.just(PromptResult.builder()
            .description(description)
            .messages(messages)
            .build());
    }
}
```

## Modelo de McpServerTest.java

```java
package com.example.mcp;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import io.mcp.server.McpServer;
import io.mcp.server.McpSyncServer;
import io.mcp.server.tool.ToolResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class McpServerTest {

    private McpSyncServer syncServer;
    private ObjectMapper objectMapper;

    @BeforeEach
    void setUp() {
        McpServer server = createTestServer();
        syncServer = server.toSyncServer();
        objectMapper = new ObjectMapper();
    }

    private McpServer createTestServer() {
        // Mesma configuração da aplicação principal
        McpServer server = McpServerBuilder.builder()
            .serverInfo("test-server", "1.0.0")
            .capabilities(cap -> cap.tools(true))
            .build();

        // Registra os manipuladores
        ToolHandlers.register(server);

        return server;
    }

    @Test
    void testGreetTool() {
        ObjectNode args = objectMapper.createObjectNode();
        args.put("name", "Java");

        ToolResponse response = syncServer.callTool("greet", args);

        assertFalse(response.isError());
        assertEquals(1, response.getContent().size());
        assertTrue(response.getContent().get(0).getText().contains("Java"));
    }

    @Test
    void testCalculateTool() {
        ObjectNode args = objectMapper.createObjectNode();
        args.put("operation", "add");
        args.put("a", 5);
        args.put("b", 3);

        ToolResponse response = syncServer.callTool("calculate", args);

        assertFalse(response.isError());
        assertTrue(response.getContent().get(0).getText().contains("8"));
    }

    @Test
    void testDivideByZero() {
        ObjectNode args = objectMapper.createObjectNode();
        args.put("operation", "divide");
        args.put("a", 10);
        args.put("b", 0);

        ToolResponse response = syncServer.callTool("calculate", args);

        assertTrue(response.isError());
    }
}
```

## Modelo de README.md

````markdown
Meu servidor MCP
================

Servidor Model Context Protocol criado em Java com o MCP Java SDK oficial.

## Funcionalidades

- Ferramentas: greet, calculate
- Recursos: dados de exemplo, configuração
- Prompts: code-review
- Fluxos reativos (Reactive Streams) com Project Reactor
- Registros de eventos estruturados com SLF4J
- Cobertura completa de testes

## Requisitos

- Java 21 ou posterior
- Maven 3.6+ ou Gradle 7+

## Compilação

### Maven
```bash
mvn clean package
```

### Gradle
```bash
./gradlew build
```

## Execução

### Maven
```bash
java -jar target/my-mcp-server-1.0.0.jar
```

### Gradle
```bash
./gradlew run
```

## Testes

### Maven
```bash
mvn test
```

### Gradle
```bash
./gradlew test
```

## Integração com o VS Code

Adicione o servidor ao `.vscode/mcp.json` do VS Code:

```json
{
  "servers": {
    "my-mcp-server": {
      "command": "java",
      "args": ["-jar", "/path/to/my-mcp-server-1.0.0.jar"]
    }
  }
}
```

## Licença

MIT
````

## Instruções de geração

1. **Solicite o nome e o pacote do projeto**
2. **Escolha a ferramenta de build** (Maven ou Gradle)
3. **Gere todos os arquivos** com a estrutura correta de pacotes
4. **Use fluxos reativos (Reactive Streams)** nos manipuladores assíncronos
5. **Inclua registros de eventos completos** com SLF4J
6. **Adicione testes** para todos os handlers
7. **Siga as convenções Java** (camelCase, PascalCase)
8. **Inclua tratamento de erros** com respostas adequadas
9. **Documente as APIs públicas** com Javadoc
10. **Forneça exemplos síncronos e assíncronos**

## Modelo de saída

```text
my-mcp-server/  (Java 21, Maven ou Gradle)
├── pom.xml | build.gradle.kts
├── src/main/java/com/example/mcp/
│   ├── McpServerApplication.java
│   ├── tools/       ToolDefinitions.java, ToolHandlers.java
│   ├── resources/   ResourceDefinitions.java, ResourceHandlers.java
│   └── prompts/     PromptDefinitions.java, PromptHandlers.java
├── src/test/java/com/example/mcp/McpServerTest.java
└── README.md

capacidades: tools=greet,calculate | resources=example,config | prompts=code-review
compilação: mvn clean package   (ou ./gradlew build)
execução: java -jar target/my-mcp-server-1.0.0.jar
```

## Critérios de qualidade

- [ ] O projeto compila no Java 21 com Maven (`mvn clean package`) ou Gradle (`./gradlew build`).
- [ ] Cada ferramenta, recurso e prompt tem uma definição e um manipulador registrado.
- [ ] Os manipuladores validam os argumentos e retornam uma resposta de erro, em vez de lançar exceção para entradas inválidas.
- [ ] Os manipuladores assíncronos usam Project Reactor (`Mono`); os registros de eventos usam SLF4J (sem `System.out`).
- [ ] `McpServerTest` cobre cada ferramenta, inclusive um fluxo de erro como divisão por zero.
- [ ] O README documenta compilação, execução e integração do cliente MCP pelo `.vscode/mcp.json` do VS Code.
