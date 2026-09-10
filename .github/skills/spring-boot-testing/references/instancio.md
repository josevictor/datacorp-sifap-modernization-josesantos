# Instancio

Gere automaticamente objetos de teste complexos. Use quando entidades ou DTOs tiverem três ou mais propriedades.

## Quando usar

- Objetos com **três ou mais propriedades**
- Preparação de dados de teste para repositórios
- Criação de DTOs para testes de controladores
- Redução de chamadas repetitivas a construtores ou métodos de definição

## Dependência

```xml
<dependency>
  <groupId>org.instancio</groupId>
  <artifactId>instancio-junit</artifactId>
  <version>5.5.1</version>
  <scope>test</scope>
</dependency>
```

## Uso básico

### Objeto simples

```java
final var order = Instancio.create(Order.class);
// Todos os campos são preenchidos com dados aleatórios
```

### Lista de objetos

```java
final var orders = Instancio.ofList(Order.class).size(5).create();
// Cinco pedidos com dados aleatórios
```

## Personalização de valores

### Definição de campos específicos

```java
final var order = Instancio.of(Order.class)
  .set(field(Order::getStatus), "PENDING")
  .set(field(Order::getTotal), new BigDecimal("99.99"))
  .create();
```

### Fornecimento de valores gerados

```java
final var order = Instancio.of(Order.class)
  .supply(field(Order::getEmail), () -> "user" + UUID.randomUUID() + "@test.com")
  .create();
```

### Campos ignorados

```java
final var order = Instancio.of(Order.class)
  .ignore(field(Order::getId)) // Deixa o banco gerar
  .create();
```

## Objetos complexos

### Objetos aninhados

```java
final var order = Instancio.of(Order.class)
  .set(field(Order::getCustomer), Instancio.create(Customer.class))
  .set(field(Order::getItems), Instancio.ofList(OrderItem.class).size(3).create())
  .create();
```

### Todos os campos aleatórios

```java
// Quando forem necessários dados totalmente aleatórios, mas válidos
final var randomOrder = Instancio.create(Order.class);
// Cliente, itens e endereços: todos preenchidos
```

## Integração com Spring Boot

### Configuração do teste de repositório

```java
@DataJpaTest
@AutoConfigureTestDatabase
@Testcontainers
class OrderRepositoryTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @Autowired
  private OrderRepository orderRepository;

  @Test
  void shouldFindOrdersByStatus() {
    // Dado: cria dez pedidos aleatórios com status PENDING
    final var orders = Instancio.ofList(Order.class)
      .size(10)
      .set(field(Order::getStatus), "PENDING")
      .create();

    orderRepository.saveAll(orders);

    // Quando
    final var found = orderRepository.findByStatus("PENDING");

    // Então
    assertThat(found).hasSize(10);
  }
}
```

### Configuração do teste de controlador

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

  @Autowired
  private MockMvcTester mvc;

  @MockitoBean
  private OrderService orderService;

  @Test
  void shouldReturnOrder() {
    // Dado: pedido aleatório com um ID específico
    Order order = Instancio.of(Order.class)
      .set(field(Order::getId), 1L)
      .create();

    given(orderService.findById(1L)).willReturn(order);

    // Quando/Então
    assertThat(mvc.get().uri("/orders/1"))
      .hasStatus(HttpStatus.OK)
      .bodyJson()
      .convertTo(OrderResponse.class)
      .satisfies(response -> {
        assertThat(response.getId()).isEqualTo(1L);
      });
  }
}
```

## Padrões

### Alternativa ao padrão Construtor (Builder)

```java
// Em vez de:
Order order = Order.builder()
  .id(1L)
  .status("PENDING")
  .customer(Customer.builder().name("John").build())
  .items(List.of(
    OrderItem.builder().product("A").price(10).build(),
    OrderItem.builder().product("B").price(20).build()
  ))
  .build();

// Use:
Order order = Instancio.of(Order.class)
  .set(field(Order::getId), 1L)
  .set(field(Order::getStatus), "PENDING")
  .create();
// Cliente e itens gerados automaticamente
```

### Dados com semente de geração

```java
// Dados "aleatórios" consistentes para testes reproduzíveis
Order order = Instancio.of(Order.class)
  .withSeed(12345L)
  .create();
// Os mesmos dados em cada execução com a semente 12345
```

## Padrões comuns

### Geração de e-mail

```java
String email = Instancio.gen().net().email();
```

### Geração de data

```java
LocalDateTime createdAt = Instancio.gen().temporal()
  .localDateTime()
  .past()
  .create();
```

### Padrões de texto

```java
String phone = Instancio.gen().text().pattern("+1-###-###-####");
```

## Comparação

| Abordagem | Linhas de código | Manutenibilidade |
| -------- | ------------- | --------------- |
| Métodos de definição manuais | 10-20 | Baixa |
| Padrão Construtor | 5-10 | Média |
| **Instancio** | 2-5 | **Alta** |

## Práticas recomendadas

1. **Use em objetos com três ou mais propriedades**: não compensa para objetos simples
2. **Defina apenas o que for relevante**: deixe o Instancio preencher o restante
3. **Use com Testcontainers**: adequado para semear o banco de dados
4. **Defina os IDs explicitamente**: ao testar cenários específicos
5. **Ignore campos gerados automaticamente**: como createdAt e updatedAt

## Referências

- [Documentação do Instancio](https://www.instancio.org/)
- [Extensão do JUnit 5](https://www.instancio.org/user-guide/#junit-integration)
