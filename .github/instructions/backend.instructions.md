---
description: "Use ao implementar APIs de backend, serviços, controllers, validação de solicitações, tratamento de erros e limites de serviços de negócio."
applyTo: "backend/src/main/java/**,backend/src/test/java/**"
---

# Convenções de backend — Controllers, serviços e validação

Este arquivo é ativado quando você edita código-fonte ou testes Java em `backend/`. Ele ensina como estruturar controllers, DTOs, a camada de serviço, a validação de solicitações e as respostas de erro de uma aplicação Java 21 + Spring Boot 3.3. Ele **não** decide limites de módulos nem mapeamento JPA/FDT, que pertencem a [`modular-monolith.instructions.md`](modular-monolith.instructions.md), e não aborda autenticação, que pertence a [`security.instructions.md`](security.instructions.md).

> [!NOTE]
> `backend/` ainda não existe. A equipe o cria do zero no Estágio 3. Trate as regras abaixo como as convenções que o código deve seguir desde o momento em que for escrito.

## Camadas e limites

As solicitações fluem em uma direção: `Controller → Service → Repository`. Mantenha os controllers enxutos (somente mapeamento HTTP) e coloque todas as regras de negócio no serviço.

- `@Transactional` fica **somente** na camada de serviço, nunca em um controller ou repositório; as leituras usam `@Transactional(readOnly = true)`.
- Métodos públicos nunca retornam `null`; represente ausência com `Optional`.
- Mantenha controllers e serviços package-private em seus módulos para que nenhum outro módulo importe internos.

## Controllers e endpoints REST

Os paths seguem `/api/v1/{resource}` (plural e kebab-case para recursos com várias palavras). Todo endpoint possui anotações OpenAPI e retorna o status correto: `201` na criação, `204` na exclusão, `409` em conflito e `PATCH` para atualizações parciais.

```java
@RestController
@RequestMapping("/api/v1/resources")
@RequiredArgsConstructor
class ResourceController {

    private final ResourceService resourceService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED) // 201 na criação
    @Operation(summary = "Cadastrar um recurso")
    @ApiResponse(responseCode = "201", description = "Criado")
    @ApiResponse(responseCode = "409", description = "Recurso duplicado")
    ResourceResponse create(@Valid @RequestBody CreateResourceRequest request) {
        return resourceService.create(request);
    }
}
```

## DTOs e validação

Exponha DTOs `record` do Java 21, nunca entidades JPA. Valide no limite do controller com Bean Validation no record da solicitação.

```java
public record CreateResourceRequest(
    @NotBlank @Size(max = 120) String label,
    @NotNull @Positive BigDecimal amount) {}
```

## Camada de serviço

O serviço coordena a transação, impõe invariantes e transforma resultados de persistência em DTOs.

```java
@Service
@RequiredArgsConstructor
class ResourceService {

    private final ResourceRepository resourceRepository;

    @Transactional(readOnly = true)
    ResourceResponse getById(UUID id) {
        return resourceRepository.findById(id)
            .map(ResourceResponse::from)
            .orElseThrow(() -> new ResourceNotFoundException(id));
    }

    @Transactional
    ResourceResponse create(CreateResourceRequest request) {
        resourceRepository.findByLabel(request.label()).ifPresent(existing -> {
            throw new ResourceConflictException(request.label());
        });
        return ResourceResponse.from(resourceRepository.save(Resource.from(request)));
    }
}
```

## Tratamento de erros

Retorne `ProblemDetail` da RFC 7807 por um único `@RestControllerAdvice`, mapeie falhas de validação para `400` e anexe um ID de correlação para relacionar logs e respostas.

```java
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        return problem(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    private ProblemDetail problem(HttpStatus status, String detail) {
        ProblemDetail body = ProblemDetail.forStatusAndDetail(status, detail);
        body.setProperty("correlationId", MDC.get("correlationId"));
        return body;
    }
}
```

## Logs e dados sensíveis

> [!WARNING]
> Nunca registre CPF, valores de benefícios, tokens ou outros dados sensíveis. Registre identificadores e o ID de correlação e mascare todo campo regulamentado antes que chegue a um log ou mensagem de erro.

```java
// Errado: log.info("pagamento para CPF {} no valor {}", cpf, amount);
log.info("pagamento processado correlationId={} resourceId={}", correlationId, id);
```

## Convenções

| Regra | Justificativa |
|---|---|
| Controllers em `PascalCase`; rotas `/api/v1/{resource}` em kebab-case | Superfície HTTP previsível e versionada |
| `@Transactional` somente em serviços | Repositórios e controllers representam efeitos colaterais com honestidade |
| Records para DTOs de solicitação/resposta | Contratos imutáveis e com limites explícitos |
| `@Valid` + Bean Validation em controllers | Rejeita entradas inválidas antes da lógica de negócio |
| `Optional` para resultados ausentes | Elimina `NullPointerException` em APIs públicas |
| `ProblemDetail` (RFC 7807) para todo erro | Um único formato de erro legível por máquina |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Retorne `201`/`204`/`409` quando aplicável | Retorne `200` para todo resultado |
| Lance exceções de domínio mapeadas no advice | Retorne stack traces brutos ou erros `Map<String,Object>` |
| Injete dependências pelo construtor | Use `@Autowired` em campo |
| Mascare CPF e valores nos logs | Registre entidades, corpos de solicitações ou tokens |

## Lista de verificação antes de abrir uma PR

- [ ] Todo endpoint usa `/api/v1/{resource}`, o verbo correto e o status correto
- [ ] Todo endpoint possui anotações OpenAPI e um corpo de solicitação `record` validado
- [ ] `@Transactional` aparece somente em serviços; nenhum método público retorna `null`
- [ ] Os erros passam pelo `@RestControllerAdvice` como `ProblemDetail` com um ID de correlação
- [ ] Nenhum dado sensível (CPF, valores, tokens) chega aos logs ou payloads de erro
- [ ] Os testes cobrem o fluxo de sucesso, uma falha de validação e uma falha de autenticação (consulte [`tests.instructions.md`](tests.instructions.md))
