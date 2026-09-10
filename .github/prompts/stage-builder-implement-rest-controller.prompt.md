---
name: "implement-rest-controller"
description: "Implementa um controlador REST do Spring a partir da definição de um endpoint OpenAPI e o conecta aos serviços do contexto delimitado."
argument-hint: "endpoint=\"<METHOD /api/v1/resource>\" context=<context> service=<Service>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /implement-rest-controller

## Objetivo

Gerar um controlador REST Spring Boot a partir de OpenAPI. O controlador é um adaptador fino: valida, delega e retorna, sem lógica de negócio.

## Quando usar

Depois que a camada de serviço existir e a equipe quiser expô-la por REST.

## Pré-condições

- OpenAPI contém o endpoint
- Serviço ou interface existe
- DTOs existem ou serão records

## Entradas que a equipe deve fornecer

- Método e caminho OpenAPI
- Contexto e pacote
- Serviço de destino

## O que farei

- Lerei OpenAPI, gerarei `@RestController`, records com Bean Validation, injeção por construtor e `@ControllerAdvice` se necessário
- Compilarei o projeto

## O que não farei

- Colocar lógica no controlador, omitir `@Valid`, usar injeção de campo `@Autowired`, fixar mensagens ou inventar comportamento
- Erros usarão RFC 7807 `ProblemDetail`

## Formato da saída

1. `src/main/java/[package]/api/[Name]Controller.java`
2. DTOs em `src/main/java/[package]/api/dto/`
3. `src/main/java/[package]/shared/exception/GlobalExceptionHandler.java`, se ausente

## Definição de pronto

- [ ] Compila; Javadoc cita `operationId` e REQ-IDs
- [ ] DTO usa `@NotNull`, `@Size` etc.
- [ ] Status são 201 para POST, 200 para GET e 204 para DELETE
- [ ] Controlador só valida, delega e mapeia
- [ ] Erros usam `ProblemDetail`

## Corpo do prompt

Você é `@builder`. Implemente o endpoint OpenAPI indicado.

**Etapa 1 — Ler OpenAPI.** Extraia método, caminho, operation ID, resumo, schemas, parâmetros e REQ-IDs.

**Etapa 2 — Gerar records.**

```java
public record [RequestName](
    @NotNull [FieldType] [requiredField],
    @Size(max = [maxLength]) String [optionalTextField]
) {}
```

**Etapa 3 — Gerar o controlador.** Use `@RestController`, `@RequestMapping`, `@Tag`, campo `private final`, construtor, `@Operation`, `@Valid`, delegação ao serviço e `ResponseEntity`. Preserve os placeholders técnicos e dados de OpenAPI.

**Etapa 4 — Garantir tratamento de erros.** Se necessário, crie handlers: `MethodArgumentNotValidException` → 400; `EntityNotFoundException` → 404; `IllegalStateException` → 409; `Exception` → 500 seguro, sem stack trace.

**Etapa 5 — Compilar.** Execute `mvn compile` ou equivalente e corrija erros. Se faltar a interface, gere assinatura mínima com implementação TODO para a equipe.

## Exemplo de chamada

```
/implement-rest-controller endpoint="<METHOD /api/v1/resource>" context=<context> service=<Service>
```
