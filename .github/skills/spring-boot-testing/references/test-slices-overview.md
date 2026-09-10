# Visão geral das fatias de teste

Referência rápida para selecionar a fatia de teste adequada do Spring Boot.

## Matriz de decisão

| Anotação | Quando usar | Carrega | Velocidade |
| ---------- | -------- | ----- | ----- |
| **Nenhuma** (JUnit simples) | Lógica de negócio pura | Nada | Mais rápida |
| `@WebMvcTest` | Controlador + camada HTTP | Controladores, MVC, Jackson | Rápida |
| `@DataJpaTest` | Consultas de repositório | Repositórios, JPA, DataSource | Rápida |
| `@RestClientTest` | Código de cliente REST | RestTemplate/RestClient, Jackson | Rápida |
| `@JsonTest` | Serialização JSON | Somente ObjectMapper | Fatia mais rápida |
| `@WebFluxTest` | Controladores reativos | Controladores, WebFlux | Rápida |
| `@DataJdbcTest` | Repositórios JDBC | Repositórios, JDBC | Rápida |
| `@DataMongoTest` | Repositórios MongoDB | Repositórios, MongoDB | Rápida |
| `@DataRedisTest` | Repositórios Redis | Repositórios, Redis | Rápida |
| `@SpringBootTest` | Integração completa | Aplicação inteira | Lenta |

## Guia de seleção

### Sem anotação (teste unitário simples)

```java
class PriceCalculatorTest {
  private PriceCalculator calculator = new PriceCalculator();

  @Test
  void shouldApplyDiscount() {
    var result = calculator.applyDiscount(100, 0.1);
    assertThat(result).isEqualTo(new BigDecimal("90.00"));
  }
}
```

**Quando**: lógica de negócio pura, sem dependências ou com dependências simples que podem ser simuladas por injeção de construtor.

### Use @WebMvcTest

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {
  @Autowired private MockMvcTester mvc;
  @MockitoBean private OrderService orderService;
}
```

**Quando**: para testar o mapeamento de solicitações, validação, mapeamento JSON, segurança e filtros.

**O que você obtém**: MockMvc, ObjectMapper, Spring Security (se presente) e manipuladores de exceção.

### Use @DataJpaTest

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryTest {
  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");
}
```

**Quando**: para testar consultas JPA personalizadas, mapeamentos de entidades, comportamento transacional e operações em cascata.

**O que você obtém**: beans de repositório, EntityManager, TestEntityManager e suporte a transações.

### Use @RestClientTest

```java
@RestClientTest(WeatherService.class)
class WeatherServiceTest {
  @Autowired private WeatherService weatherService;
  @Autowired private MockRestServiceServer server;
}
```

**Quando**: para testar clientes REST que chamam APIs externas.

**O que você obtém**: MockRestServiceServer para programar respostas HTTP.

### Use @JsonTest

```java
@JsonTest
class OrderJsonTest {
  @Autowired private JacksonTester<Order> json;
}
```

**Quando**: para testar serializadores e desserializadores personalizados e mapeamento JSON complexo.

### Use @SpringBootTest

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class OrderIntegrationTest {
  @Autowired private RestTestClient restClient;
}
```

**Quando**: para testar o fluxo completo da solicitação, filtros de segurança e interações com o banco de dados em conjunto.

**O que você obtém**: contexto completo da aplicação, servidor integrado opcional e beans reais.

## Erros comuns

1. **Usar @SpringBootTest para tudo**: torna a suíte desnecessariamente lenta
2. **Usar @WebMvcTest sem simular serviços**: causa falhas no carregamento do contexto
3. **Usar @DataJpaTest com @MockBean**: anula o objetivo, pois são necessários repositórios reais
4. **Usar várias fatias em um teste**: cada fatia deve estar em uma classe de teste separada

## Recursos do Java 21 nos testes

### Records para dados de teste

```java
record OrderRequest(String product, int quantity) {}
record OrderResponse(Long id, String status, BigDecimal total) {}
```

### Correspondência de padrões nos testes

```java
@Test
void shouldHandleDifferentOrderTypes() {
  var order = orderService.create(new OrderRequest("Product", 2));

  switch (order) {
    case PhysicalOrder po -> assertThat(po.getShippingAddress()).isNotNull();
    case DigitalOrder do_ -> assertThat(do_.getDownloadLink()).isNotNull();
    default -> throw new IllegalStateException("Tipo de pedido desconhecido");
  }
}
```

### Blocos de texto para JSON

```java
@Test
void shouldParseComplexJson() {
  var json = """
    {
      "id": 1,
      "status": "PENDING",
      "items": [
        {"product": "Laptop", "price": 999.99},
        {"product": "Mouse", "price": 29.99}
      ]
    }
    """;

  assertThat(mvc.post().uri("/orders")
    .contentType(APPLICATION_JSON)
    .content(json))
    .hasStatus(CREATED);
}
```

### Coleções sequenciadas

```java
@Test
void shouldReturnOrdersInSequence() {
  var orders = orderRepository.findAll();

  assertThat(orders.getFirst().getStatus()).isEqualTo("NEW");
  assertThat(orders.getLast().getStatus()).isEqualTo("COMPLETED");
  assertThat(orders.reversed().getFirst().getStatus()).isEqualTo("COMPLETED");
}
```

## Dependências por fatia

```xml
<!-- WebMvcTest -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-webmvc-test</artifactId>
  <scope>test</scope>
</dependency>

<!-- DataJpaTest -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<!-- RestClientTest -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-restclient-test</artifactId>
  <scope>test</scope>
</dependency>

<!-- Testcontainers -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
```
