# Migração para Spring Boot 4.0

Principais alterações de teste ao migrar do Spring Boot 3.x para o 4.0.

## Alterações de dependências

### Inicializadores de teste modulares

O Spring Boot 4.0 introduz inicializadores de teste modulares:

**Antes (3.x):**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
```

**Depois (4.0), testes WebMvc:**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-webmvc-test</artifactId>
  <scope>test</scope>
</dependency>
```

**Depois (4.0), testes de cliente REST:**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-restclient-test</artifactId>
  <scope>test</scope>
</dependency>
```

## Migração de anotações

### @MockBean → @MockitoBean

**Obsoleto (3.x):**

```java
@MockBean
private OrderService orderService;
```

**Novo (4.0):**

```java
@MockitoBean
private OrderService orderService;
```

### @SpyBean → @MockitoSpyBean

**Obsoleto (3.x):**

```java
@SpyBean
private PaymentGatewayClient paymentClient;
```

**Novo (4.0):**

```java
@MockitoSpyBean
private PaymentGatewayClient paymentClient;
```

## Novos recursos de teste

### RestTestClient

Substitui TestRestTemplate (obsoleto):

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class OrderIntegrationTest {

  @Autowired
  private RestTestClient restClient;

  @Test
  void shouldCreateOrder() {
    restClient
      .post()
      .uri("/orders")
      .body(new OrderRequest("Product", 2))
      .exchange()
      .expectStatus()
      .isCreated()
      .expectHeader()
      .location("/orders/1");
  }
}
```

## Compatibilidade com JUnit 6

O Spring Boot 4.0 usa JUnit 6 por padrão:

- JUnit 4 está obsoleto (use JUnit Vintage temporariamente)
- Todos os recursos do JUnit 5 continuam funcionando
- Remova as dependências do JUnit 4 para uma migração limpa

## Testcontainers 2.0

Os nomes dos módulos mudaram:

**Antes (1.x):**

```xml
<artifactId>postgresql</artifactId>
```

**Depois (2.0):**

```xml
<artifactId>testcontainers-postgresql</artifactId>
```

## Simulação de beans não singleton

O Spring Framework 7 permite simular beans com escopo de protótipo:

```java
@Component
@Scope("prototype")
public class OrderProcessor { }

@SpringBootTest
class OrderServiceTest {
  @MockitoBean
  private OrderProcessor orderProcessor; // Agora funciona!
}
```

## Alterações no contexto do SpringExtension

Agora, o contexto da extensão tem escopo de método de teste por padrão.

Se os testes falharem com classes @Nested:

```java
@SpringExtensionConfig(useTestClassScopedExtensionContext = true)
@SpringBootTest
class OrderTest {
  // Usa o comportamento antigo
}
```

## Lista de verificação da migração

- [ ] Substituir @MockBean por @MockitoBean
- [ ] Substituir @SpyBean por @MockitoSpyBean
- [ ] Atualizar os nomes das dependências do Testcontainers para 2.0
- [ ] Adicionar inicializadores de teste modulares conforme necessário
- [ ] Migrar TestRestTemplate para RestTestClient
- [ ] Remover dependências do JUnit 4
- [ ] Atualizar implementações personalizadas de TestExecutionListener
- [ ] Testar o comportamento de classes @Nested

## Compatibilidade retroativa

Use inicializadores "clássicos" para uma migração gradual:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test-classic</artifactId>
  <scope>test</scope>
</dependency>
```

Isso mantém o comportamento antigo durante a migração incremental.
