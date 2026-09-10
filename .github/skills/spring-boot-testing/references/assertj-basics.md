# Fundamentos do AssertJ

Asserções fluentes para testes legíveis e fáceis de manter.

## Asserções básicas

### Igualdade de objetos

```java
assertThat(order.getStatus()).isEqualTo("PENDING");
assertThat(order.getId()).isNotEqualTo(0);
assertThat(order).isEqualTo(expectedOrder);
assertThat(order).isNotNull();
assertThat(nullOrder).isNull();
```

### Asserções de texto

```java
assertThat(order.getDescription())
  .isEqualTo("Test Order")
  .startsWith("Test")
  .endsWith("Order")
  .contains("Test")
  .hasSize(10)
  .matches("[A-Za-z ]+");
```

### Asserções de números

```java
assertThat(order.getAmount())
  .isEqualTo(99.99)
  .isGreaterThan(50)
  .isLessThan(100)
  .isBetween(50, 100)
  .isPositive()
  .isNotZero();
```

### Asserções booleanas

```java
assertThat(order.isActive()).isTrue();
assertThat(order.isDeleted()).isFalse();
```

## Asserções de data e hora

```java
assertThat(order.getCreatedAt())
  .isEqualTo(LocalDateTime.of(2024, 1, 15, 10, 30))
  .isBefore(LocalDateTime.now())
  .isAfter(LocalDateTime.of(2024, 1, 1))
  .isCloseTo(LocalDateTime.now(), within(5, ChronoUnit.SECONDS));
```

## Asserções de Optional

```java
Optional<Order> maybeOrder = orderService.findById(1L);

assertThat(maybeOrder)
  .isPresent()
  .hasValueSatisfying(order -> {
    assertThat(order.getId()).isEqualTo(1L);
  });

assertThat(orderService.findById(999L)).isEmpty();
```

## Asserções de exceções

### Tratamento de exceções do JUnit 5

```java
@Test
void shouldThrowException() {
  OrderService service = new OrderService();

  assertThatThrownBy(() -> service.findById(999L))
    .isInstanceOf(OrderNotFoundException.class)
    .hasMessage("Pedido 999 não encontrado")
    .hasMessageContaining("999");
}
```

### Tratamento de exceções do AssertJ

```java
@Test
void shouldThrowExceptionWithCause() {
  assertThatExceptionOfType(OrderProcessingException.class)
    .isThrownBy(() -> service.processOrder(invalidOrder))
    .withCauseInstanceOf(ValidationException.class);
}
```

## Asserções personalizadas

Crie asserções específicas do domínio para reutilizar o código de teste:

```java
public class OrderAssert extends AbstractAssert<OrderAssert, Order> {

  public static OrderAssert assertThat(Order actual) {
    return new OrderAssert(actual);
  }

  private OrderAssert(Order actual) {
    super(actual, OrderAssert.class);
  }

  public OrderAssert isPending() {
    isNotNull();
    if (!"PENDING".equals(actual.getStatus())) {
      failWithMessage("Esperava status PENDING para o pedido, mas era %s", actual.getStatus());
    }
    return this;
  }

  public OrderAssert hasTotal(BigDecimal expected) {
    isNotNull();
    if (!expected.equals(actual.getTotal())) {
      failWithMessage("Esperava total %s, mas era %s", expected, actual.getTotal());
    }
    return this;
  }
}
```

Uso:

```java
OrderAssert.assertThat(order)
  .isPending()
  .hasTotal(new BigDecimal("99.99"));
```

## Asserções agrupadas

Colete várias falhas antes de interromper o teste:

```java
@Test
void shouldValidateOrder() {
  Order order = orderService.findById(1L);

  SoftAssertions.assertSoftly(softly -> {
    softly.assertThat(order.getId()).isEqualTo(1L);
    softly.assertThat(order.getStatus()).isEqualTo("PENDING");
    softly.assertThat(order.getItems()).isNotEmpty();
  });
}
```

## Padrão `satisfies`

```java
assertThat(order)
  .satisfies(o -> {
    assertThat(o.getId()).isPositive();
    assertThat(o.getStatus()).isNotBlank();
    assertThat(o.getCreatedAt()).isNotNull();
  });
```

## Uso com Spring

```java
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class OrderServiceTest {

  @Autowired
  private OrderService orderService;

  @Test
  void shouldCreateOrder() {
    Order order = orderService.create(new OrderRequest("Product", 2));

    assertThat(order)
      .isNotNull()
      .extracting(Order::getId, Order::getStatus)
      .containsExactly(1L, "PENDING");
  }
}
```

## Import estático

Sempre use import estático para manter as asserções limpas:

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.assertj.core.api.Assertions.catchThrowable;
```

## Principais benefícios

1. **Legível**: estrutura semelhante a frases
2. **Tipagem segura**: o preenchimento automático da IDE funciona
3. **API abrangente**: muitas asserções integradas
4. **Extensível**: asserções personalizadas para seu domínio
5. **Erros melhores**: mensagens de falha claras
