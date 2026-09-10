# @MockitoBean

Simulação de dependências em testes do Spring Boot (substitui o @MockBean obsoleto no Spring Boot 4+).

## Visão geral

`@MockitoBean` substitui a anotação obsoleta `@MockBean` no Spring Boot 4.0+. Ela cria um objeto simulado do Mockito e o registra no contexto Spring, substituindo qualquer bean existente do mesmo tipo.

## Uso básico

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

  @MockitoBean
  private OrderService orderService;

  @MockitoBean
  private UserService userService;
}
```

## Fatias de teste compatíveis

- `@WebMvcTest`: simula dependências de serviço ou repositório
- `@WebFluxTest`: simula dependências de serviços reativos
- `@SpringBootTest`: substitui beans reais por objetos simulados

## Programação de respostas para métodos

### Resposta programada básica

```java
@Test
void shouldReturnOrder() {
  Order order = new Order(1L, "PENDING");
  given(orderService.findById(1L)).willReturn(order);

  // Código do teste
}
```

### Vários retornos

```java
given(orderService.findById(anyLong()))
  .willReturn(new Order(1L, "PENDING"))
  .willReturn(new Order(2L, "COMPLETED"));
```

### Lançamento de exceções

```java
given(orderService.findById(999L))
  .willThrow(new OrderNotFoundException(999L));
```

### Correspondência de argumentos

```java
given(orderService.create(argThat(req -> req.getQuantity() > 0)))
  .willReturn(1L);

given(orderService.findByStatus(eq("PENDING")))
  .willReturn(List.of(new Order()));
```

## Verificação de interações

### Verificar se o método foi chamado

```java
verify(orderService).findById(1L);
```

### Verificar se nunca foi chamado

```java
verify(orderService, never()).delete(any());
```

### Verificar a quantidade

```java
verify(orderService, times(2)).findById(anyLong());
verify(orderService, atLeastOnce()).findByStatus(anyString());
```

### Verificar a ordem

```java
InOrder inOrder = inOrder(orderService, userService);
inOrder.verify(orderService).findById(1L);
inOrder.verify(userService).getUser(any());
```

## Reinicialização dos objetos simulados

Os objetos simulados são reinicializados automaticamente entre os testes. Para reinicializar durante um teste:

```java
Mockito.reset(orderService);
```

## @MockitoSpyBean para simulação parcial

Use `@MockitoSpyBean` para envolver um bean real com Mockito.

```java
@SpringBootTest
class OrderServiceIntegrationTest {

  @MockitoSpyBean
  private PaymentGatewayClient paymentClient;

  @Test
  void shouldProcessOrder() {
    doReturn(true).when(paymentClient).processPayment(any());

    // Testa com serviço real, mas cliente de pagamento simulado
  }
}
```

## @TestBean para beans de teste personalizados

Registre uma instância de bean personalizada no contexto de teste:

```java
@SpringBootTest
class OrderServiceTest {

  @TestBean
  private PaymentGatewayClient paymentClient() {
    return new FakePaymentClient();
  }
}
```

## Escopo: instância única versus protótipo

O Spring Framework 7+ (Spring Boot 4+) permite simular beans que não sejam de instância única:

```java
@Component
@Scope("prototype")
public class OrderProcessor {
  public String process() { return "real"; }
}

@SpringBootTest
class OrderServiceTest {
  @MockitoBean
  private OrderProcessor orderProcessor;

  @Test
  void shouldWorkWithPrototype() {
    given(orderProcessor.process()).willReturn("mocked");
    // Código do teste
  }
}
```

## Padrões comuns

### Simulação de repositório em teste de serviço

```java
@SpringBootTest
class OrderServiceTest {
  @MockitoBean
  private OrderRepository orderRepository;

  @Autowired
  private OrderService orderService;

  @Test
  void shouldCreateOrder() {
    given(orderRepository.save(any())).willReturn(new Order(1L));

    Long id = orderService.createOrder(new OrderRequest());

    assertThat(id).isEqualTo(1L);
    verify(orderRepository).save(any(Order.class));
  }
}
```

### Vários objetos simulados do mesmo tipo

Use os nomes dos beans:

```java
@MockitoBean(name = "primaryDataSource")
private DataSource primaryDataSource;

@MockitoBean(name = "secondaryDataSource")
private DataSource secondaryDataSource;
```

## Migração do @MockBean

### Antes (obsoleto)

```java
@MockBean
private OrderService orderService;
```

### Depois (Spring Boot 4+)

```java
@MockitoBean
private OrderService orderService;
```

## Principais diferenças em relação ao @Mock do Mockito

| Recurso | @MockitoBean | @Mock |
| ------- | ------------ | ----- |
| Integração com o contexto | Sim | Não |
| Ciclo de vida do Spring | Participa | Nenhum |
| Funciona com @Autowired | Sim | Não |
| Compatibilidade com fatias de teste | Sim | Limitada |

## Práticas recomendadas

1. Use `@MockitoBean` somente quando houver contexto Spring
2. Em testes unitários puros, use `@Mock` ou `Mockito.mock()` do Mockito
3. Sempre verifique interações com efeitos colaterais
4. Não verifique consultas simples (a resposta programada é suficiente)
5. Reinicialize os objetos simulados se o teste alterar o estado compartilhado
