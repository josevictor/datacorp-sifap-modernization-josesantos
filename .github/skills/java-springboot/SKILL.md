---
name: "java-springboot"
description: "Práticas recomendadas para aplicações Spring Boot: estrutura de pacotes por funcionalidade, injeção por construtor, DTOs e validação, transações na camada de serviço, Spring Data JPA e tratamento de configurações e segredos. Use ao criar ou revisar código da camada de servidor Spring Boot para aplicar estruturas e convenções idiomáticas. Complementa o conjunto tecnológico Java 21 + Spring Boot 3.3 do kit."
---
# Práticas recomendadas do Spring Boot

Crie e revise fatias idiomáticas do Spring Boot 3.3 para a camada de servidor do SIFAP 2.0 (Java 21, PostgreSQL 16): estrutura de pacotes por funcionalidade, injeção por construtor, DTOs record, transações na camada de serviço e Spring Data JPA. Esta habilidade é uma lista rápida de práticas recomendadas. As convenções autoritativas, impostas pela CI, estão nos arquivos de instruções. Siga-as quando houver sobreposição:

- [`backend.instructions.md`](../../instructions/backend.instructions.md): controladores, DTOs, validação e tratamento de erros.
- [`modular-monolith.instructions.md`](../../instructions/modular-monolith.instructions.md): limites dos módulos e mapeamento de FDT do Adabas para JPA.

## Quando invocar

- "Crie a estrutura de uma nova fatia de funcionalidade (controlador, serviço e repositório) para este módulo."
- "Revise a estrutura e as convenções deste código Spring Boot."
- "Configure as propriedades e os segredos deste serviço."
- "Transforme esta entidade JPA em um endpoint adequado baseado em DTO."

## Configuração e estrutura do projeto

- **Ferramenta de compilação:** use Maven (`pom.xml`) ou Gradle (`build.gradle`) para gerenciar dependências.
- **Inicializadores:** use os inicializadores (starters) do Spring Boot, como `spring-boot-starter-web` e `spring-boot-starter-data-jpa`, para simplificar o gerenciamento de dependências.
- **Estrutura de pacotes:** organize o código por funcionalidade ou domínio, como `com.example.app.order` e `com.example.app.user`, não por camada, como `com.example.app.controller` e `com.example.app.service`.

## Injeção de dependências e componentes

- **Injeção por construtor:** sempre use injeção por construtor para as dependências obrigatórias. Isso explicita as dependências e facilita o teste dos componentes.
- **Imutabilidade:** declare os campos de dependência como `private final`.
- **Estereótipos de componentes:** use adequadamente as anotações `@Component`, `@Service`, `@Repository` e `@Controller`/`@RestController` para definir beans.

## Configuração

- **Configuração externalizada:** use `application.yml` (ou `application.properties`) para a configuração. YAML costuma ser preferível por sua legibilidade e estrutura hierárquica.
- **Propriedades com tipagem segura:** use `@ConfigurationProperties` para vincular a configuração a objetos Java fortemente tipados.
- **Perfis:** use os perfis do Spring (`application-dev.yml`, `application-prod.yml`) para gerenciar configurações específicas do ambiente.
- **Gerenciamento de segredos:** nunca fixe segredos no código. Use variáveis de ambiente localmente e Azure Key Vault por meio de Managed Identity no Azure. Nunca use `application.yml`, `locals` ou o código-fonte. Consulte [`security.instructions.md`](../../instructions/security.instructions.md).

## Camada web (controladores)

- **APIs RESTful:** use caminhos `/api/v1/{resource}`, verbos e códigos de status corretos (`201`/`204`/`409`) e anotações OpenAPI em cada ponto de acesso.
- **DTOs record:** exponha DTOs `record` do Java 21 nos limites; nunca retorne entidades JPA ao cliente.
- **Validação:** aplique Bean Validation (`@Valid`, `@NotBlank`, `@Positive`, `@Size`) ao record da solicitação no limite do controlador.
- **Tratamento de erros:** centralize os erros em um `@RestControllerAdvice` que retorne `ProblemDetail` conforme a RFC 7807. Consulte [`backend.instructions.md`](../../instructions/backend.instructions.md) para ver o formato completo do controlador e dos erros.

## Camada de serviço

- **Lógica de negócio:** encapsule toda a lógica de negócio em classes `@Service`.
- **Ausência de estado:** os serviços não devem manter estado.
- **Gerenciamento de transações:** use `@Transactional` somente na camada de serviço, nunca em controladores ou repositórios. Nas leituras, use `@Transactional(readOnly = true)`.
- **Sem retornos null:** represente a ausência com `Optional`; nunca retorne `null` de um método público.
- **Uniões de tipos:** use uma `sealed interface` com records para estados discriminados do domínio (Java 21).

## Camada de dados (repositórios)

- **Spring Data JPA:** use repositórios Spring Data JPA que estendam `JpaRepository` ou `CrudRepository` para operações padrão do banco de dados.
- **Consultas personalizadas:** use `@Query` ou a JPA Criteria API para consultas complexas.
- **Projeções:** use projeções de DTO para buscar apenas os dados necessários do banco.

## Registros de eventos

- **SLF4J:** use a API SLF4J para registrar eventos.
- **Declaração do registrador:** `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`
- **Registros parametrizados:** use mensagens parametrizadas (`logger.info("Processando usuário {}...", userId);`) em vez de concatenar textos, para melhorar o desempenho.

## Testes

- **Testes unitários:** teste serviços e componentes com JUnit 5 + Mockito. Consulte [`java-junit`](../java-junit/SKILL.md).
- **Testes de fatia e integração:** use `@WebMvcTest`, `@DataJpaTest` e `@SpringBootTest` com Testcontainers e um PostgreSQL 16 real. Consulte [`spring-boot-testing`](../spring-boot-testing/SKILL.md).

## Segurança

- **Spring Security:** use Spring Security para autenticação e autorização (OAuth2/JWT).
- **Codificação de senhas:** sempre aplique hash às senhas com um algoritmo forte, como BCrypt.
- **Tratamento de entradas:** use Spring Data JPA / JPQL (nunca SQL concatenado em strings) e codifique a saída para evitar XSS. Consulte [`security.instructions.md`](../../instructions/security.instructions.md).

## Modelo de saída

```java
// com.sifap.payment: um contexto delimitado por pacote
@RestController
@RequestMapping("/api/v1/payments")
@RequiredArgsConstructor
class PaymentController {
    private final PaymentService service;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Registrar um pagamento")
    PaymentResponse create(@Valid @RequestBody CreatePaymentRequest request) {
        return service.create(request);
    }
}

public record CreatePaymentRequest(@NotBlank String reference, @NotNull @Positive BigDecimal amount) {}

@Service
@RequiredArgsConstructor
class PaymentService {
    private final PaymentRepository repository;

    @Transactional
    PaymentResponse create(CreatePaymentRequest request) {
        return PaymentResponse.from(repository.save(Payment.from(request)));
    }
}

interface PaymentRepository extends JpaRepository<Payment, UUID> {}
```

## Critérios de qualidade

- [ ] O código está organizado por funcionalidade ou contexto delimitado; nenhum módulo importa partes internas de outro.
- [ ] As dependências usam injeção por construtor (`private final`); nenhum campo usa `@Autowired`.
- [ ] Os pontos de acesso usam `/api/v1/{resource}`, códigos de status corretos, anotações OpenAPI e DTOs `record`.
- [ ] `@Transactional` aparece somente em serviços; nenhum método público retorna `null`.
- [ ] Os erros passam por um único `@RestControllerAdvice` como `ProblemDetail`; nenhum segredo ou dado sensível é registrado em log.
- [ ] Os testes unitários (Mockito) e os testes de fatia relevantes passam. Consulte `java-junit` e `spring-boot-testing`.
