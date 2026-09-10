# MockMvc clássico

API `MockMvc` clássica para testes de controladores Spring MVC, abordagem usada pelo kit no **Spring Boot 3.3**.

## Quando usar esta referência

- O projeto usa Spring Boot 3.3 (conjunto tecnológico do kit) ou uma versão anterior à 3.4, na qual `MockMvcTester` não está disponível
- Os testes existentes usam `mvc.perform(...)`, e você os mantém ou amplia
- Você precisa migrar testes MockMvc clássicos para `MockMvcTester` (consulte a seção de migração)
- A pessoa pergunta explicitamente sobre `ResultActions`, `andExpect()` ou asserções web no estilo Hamcrest

`MockMvcTester` (estilo AssertJ) exige **Spring Boot 3.4+** e está fora do escopo do kit. Consulte [mockmvc-tester.md](mockmvc-tester.md) somente se o projeto for atualizado para uma versão posterior à 3.3.

## Configuração

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

  @Autowired
  private MockMvc mvc;

  @MockBean
  private OrderService orderService;
}
```

## Solicitação GET básica

```java
@Test
void shouldReturnOrder() throws Exception {
  given(orderService.findById(1L)).willReturn(new Order(1L, "PENDING", 99.99));

  mvc.perform(get("/orders/1"))
    .andExpect(status().isOk())
    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
    .andExpect(jsonPath("$.id").value(1))
    .andExpect(jsonPath("$.status").value("PENDING"))
    .andExpect(jsonPath("$.totalToPay").value(99.99));
}
```

## POST com corpo da solicitação

```java
@Test
void shouldCreateOrder() throws Exception {
  given(orderService.create(any(OrderRequest.class))).willReturn(1L);

  mvc.perform(post("/orders")
      .contentType(MediaType.APPLICATION_JSON)
      .content("{\"product\": \"Laptop\", \"quantity\": 2}"))
    .andExpect(status().isCreated())
    .andExpect(header().string("Location", "/orders/1"));
}
```

## Solicitação PUT

```java
@Test
void shouldUpdateOrder() throws Exception {
  mvc.perform(put("/orders/1")
      .contentType(MediaType.APPLICATION_JSON)
      .content("{\"status\": \"COMPLETED\"}"))
    .andExpect(status().isOk());
}
```

## Solicitação DELETE

```java
@Test
void shouldDeleteOrder() throws Exception {
  mvc.perform(delete("/orders/1"))
    .andExpect(status().isNoContent());
}
```

## Comparadores de status

```java
.andExpect(status().isOk())           // 200
.andExpect(status().isCreated())      // 201
.andExpect(status().isNoContent())    // 204
.andExpect(status().isBadRequest())   // 400
.andExpect(status().isUnauthorized()) // 401
.andExpect(status().isForbidden())    // 403
.andExpect(status().isNotFound())     // 404
.andExpect(status().is(422))          // código arbitrário
```

## Asserções JSON Path

```java
// Valor exato
.andExpect(jsonPath("$.status").value("PENDING"))

// Existência
.andExpect(jsonPath("$.id").exists())
.andExpect(jsonPath("$.deletedAt").doesNotExist())

// Tamanho do array
.andExpect(jsonPath("$.items").isArray())
.andExpect(jsonPath("$.items", hasSize(3)))

// Campo aninhado
.andExpect(jsonPath("$.customer.name").value("John Doe"))
.andExpect(jsonPath("$.customer.address.city").value("Berlin"))

// Com comparadores do Hamcrest
.andExpect(jsonPath("$.total", greaterThan(0.0)))
.andExpect(jsonPath("$.description", containsString("order")))
```

## Asserções de conteúdo

```java
.andExpect(content().contentType(MediaType.APPLICATION_JSON))
.andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
.andExpect(content().string(containsString("PENDING")))
.andExpect(content().json("{\"status\":\"PENDING\"}"))
```

## Asserções de cabeçalhos

```java
.andExpect(header().string("Location", "/orders/1"))
.andExpect(header().string("Content-Type", containsString("application/json")))
.andExpect(header().exists("X-Request-Id"))
.andExpect(header().doesNotExist("X-Deprecated"))
```

## Parâmetros e cabeçalhos da solicitação

```java
// Parâmetros de consulta
mvc.perform(get("/orders").param("status", "PENDING").param("page", "0"))
  .andExpect(status().isOk());

// Variáveis de caminho
mvc.perform(get("/orders/{id}", 1L))
  .andExpect(status().isOk());

// Cabeçalhos da solicitação
mvc.perform(get("/orders/1").header("X-Api-Key", "secret"))
  .andExpect(status().isOk());
```

## Captura da resposta

```java
@Test
void shouldReturnCreatedId() throws Exception {
  given(orderService.create(any())).willReturn(42L);

  MvcResult result = mvc.perform(post("/orders")
      .contentType(MediaType.APPLICATION_JSON)
      .content("{\"product\": \"Laptop\", \"quantity\": 1}"))
    .andExpect(status().isCreated())
    .andReturn();

  String location = result.getResponse().getHeader("Location");
  assertThat(location).isEqualTo("/orders/42");
}
```

## Encadeamento com andDo

```java
mvc.perform(get("/orders/1"))
  .andDo(print())              // exibe solicitação/resposta no console (depuração)
  .andExpect(status().isOk());
```

## Imports estáticos

```java
import org.springframework.boot.test.mock.mockito.MockBean;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.*;
import static org.hamcrest.Matchers.*;
```

## Migração para MockMvcTester

| MockMvc clássico | MockMvcTester (recomendado) |
| --- | --- |
| `@Autowired MockMvc mvc` | `@Autowired MockMvcTester mvc` |
| `mvc.perform(get("/orders/1"))` | `mvc.get().uri("/orders/1")` |
| `.andExpect(status().isOk())` | `.hasStatusOk()` |
| `.andExpect(jsonPath("$.status").value("X"))` | `.bodyJson().convertTo(T.class)` + AssertJ |
| `throws Exception` em cada método | Sem exceção verificada |
| Comparadores Hamcrest | Asserções fluentes AssertJ |

Consulte [mockmvc-tester.md](mockmvc-tester.md) para conhecer a API moderna completa.

## Pontos principais

1. **Cada método de teste deve declarar `throws Exception`**: `perform()` lança exceções verificadas
2. **Use `andDo(print())` durante a depuração**: remova antes do registro da alteração
3. **Prefira `jsonPath()` a `content().string()`**: asserções mais precisas no nível dos campos
4. **Imports estáticos são obrigatórios**: a IDE pode adicioná-los automaticamente
5. **Migre para MockMvcTester** ao atualizar para Spring Boot 3.4+ para melhorar a legibilidade
