# @WebMvcTest

Teste de controladores Spring MVC com testes de fatia focados.

> [!IMPORTANT]
> Os exemplos abaixo usam `MockMvcTester` e `@MockitoBean`, que pertencem ao **Spring Boot 3.4+** e estão **fora do escopo do kit**. No Spring Boot 3.3 do kit, use `MockMvc` clássico com `mockMvc.perform(...).andExpect(...)` e `@MockBean`. Consulte [mockmvc-classic.md](mockmvc-classic.md).

## Estrutura básica

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

  @Autowired
  private MockMvcTester mvc;

  @MockitoBean
  private OrderService orderService;

  @MockitoBean
  private UserService userService;
}
```

## O que é carregado

- Os controladores especificados
- Infraestrutura Spring MVC (HandlerMapping, HandlerAdapter)
- ObjectMapper do Jackson (para JSON)
- Manipuladores de exceção (@ControllerAdvice)
- Filtros do Spring Security (se estiver no caminho de classes)
- Validação (se estiver no caminho de classes)

## Teste de pontos de acesso GET

```java
@Test
void shouldReturnOrder() {
  var order = new Order(1L, "PENDING", BigDecimal.valueOf(99.99));
  given(orderService.findById(1L)).willReturn(order);

  assertThat(mvc.get().uri("/orders/1"))
    .hasStatusOk()
    .hasContentType(MediaType.APPLICATION_JSON)
    .bodyJson()
    .extractingPath("$.status")
    .isEqualTo("PENDING");
}
```

## Teste de POST com corpo da solicitação

### Uso de blocos de texto (Java 21)

```java
@Test
void shouldCreateOrder() {
  given(orderService.create(any(OrderRequest.class))).willReturn(1L);

  var json = """
    {
      "product": "Product A",
      "quantity": 2
    }
    """;

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content(json))
    .hasStatus(HttpStatus.CREATED)
    .hasHeader("Location", "/orders/1");
}
```

### Uso de records

```java
record OrderRequest(String product, int quantity) {}

@Test
void shouldCreateOrderWithRecord() {
  var request = new OrderRequest("Product A", 2);
  given(orderService.create(any())).willReturn(1L);

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content(json.write(request).getJson()))
    .hasStatus(HttpStatus.CREATED);
}
```

## Teste de erros de validação

```java
@Test
void shouldRejectInvalidOrder() {
  var invalidJson = """
    {
      "product": "",
      "quantity": -1
    }
    """;

  assertThat(mvc.post().uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .content(invalidJson))
    .hasStatus(HttpStatus.BAD_REQUEST)
    .bodyJson()
    .hasPath("$.errors");
}
```

## Teste de parâmetros de consulta

```java
@Test
void shouldFilterOrdersByStatus() {
  assertThat(mvc.get().uri("/orders?status=PENDING"))
    .hasStatusOk();

  verify(orderService).findByStatus(OrderStatus.PENDING);
}
```

## Teste de variáveis de caminho

```java
@Test
void shouldCancelOrder() {
  assertThat(mvc.put().uri("/orders/123/cancel"))
    .hasStatusOk();

  verify(orderService).cancel(123L);
}
```

## Teste com segurança

```java
@Test
@WithMockUser(roles = "ADMIN")
void adminShouldDeleteOrder() {
  assertThat(mvc.delete().uri("/orders/1"))
    .hasStatus(HttpStatus.NO_CONTENT);
}

@Test
void anonymousUserShouldBeForbidden() {
  assertThat(mvc.delete().uri("/orders/1"))
    .hasStatus(HttpStatus.UNAUTHORIZED);
}
```

## Vários controladores

```java
@WebMvcTest({OrderController.class, ProductController.class})
class WebLayerTest {
  // Testa vários controladores em uma fatia
}
```

## Exclusão de configuração automática

```java
@WebMvcTest(OrderController.class)
@AutoConfigureMockMvc(addFilters = false) // Ignora os filtros de segurança
class OrderControllerWithoutSecurityTest {
  // Testa sem filtros de segurança
}
```

## Pontos principais

1. No Spring Boot 3.3, simule colaboradores com `@MockBean` (`@MockitoBean` é o substituto na versão 3.4+)
2. No Spring Boot 3.3, use `MockMvc` clássico (`perform(...).andExpect(...)`); `MockMvcTester` exige 3.4+
3. Teste a semântica HTTP (status, cabeçalhos e tipo de conteúdo)
4. Verifique chamadas a métodos de serviço quando os efeitos colaterais forem importantes
5. Não teste lógica de negócio aqui; isso cabe aos testes unitários
6. Aproveite os blocos de texto do Java 21 para conteúdos JSON
