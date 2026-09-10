# RestTestClient

Teste moderno de clientes REST com Spring Boot 4+ (substitui TestRestTemplate).

## Visão geral

RestTestClient é a alternativa moderna ao TestRestTemplate no Spring Boot 4.0+. Ele fornece uma API fluente e reativa para testar endpoints REST.

## Configuração

### Dependência (Spring Boot 4+)

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-restclient-test</artifactId>
  <scope>test</scope>
</dependency>
```

### Configuração básica

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class OrderIntegrationTest {

  @Autowired
  private RestTestClient restClient;
}
```

## Métodos HTTP

### Solicitação GET

```java
@Test
void shouldGetOrder() {
  restClient
    .get()
    .uri("/orders/1")
    .exchange()
    .expectStatus()
    .isOk()
    .expectBody(Order.class)
    .value(order -> {
      assertThat(order.getId()).isEqualTo(1L);
      assertThat(order.getStatus()).isEqualTo("PENDING");
    });
}
```

### Solicitação POST

```java
@Test
void shouldCreateOrder() {
  OrderRequest request = new OrderRequest("Laptop", 2);

  restClient
    .post()
    .uri("/orders")
    .contentType(MediaType.APPLICATION_JSON)
    .body(request)
    .exchange()
    .expectStatus()
    .isCreated()
    .expectHeader()
    .location("/orders/1")
    .expectBody(Long.class)
    .isEqualTo(1L);
}
```

### Solicitação PUT

```java
@Test
void shouldUpdateOrder() {
  restClient
    .put()
    .uri("/orders/1")
    .body(new OrderUpdate("COMPLETED"))
    .exchange()
    .expectStatus()
    .isOk();
}
```

### Solicitação DELETE

```java
@Test
void shouldDeleteOrder() {
  restClient
    .delete()
    .uri("/orders/1")
    .exchange()
    .expectStatus()
    .isNoContent();
}
```

## Asserções de resposta

### Códigos de status

```java
restClient
  .get()
  .uri("/orders/1")
  .exchange()
  .expectStatus()
  .isOk()           // 200
  .isCreated()      // 201
  .isNoContent()    // 204
  .isBadRequest()   // 400
  .isNotFound()     // 404
  .is5xxServerError() // 5xx
  .isEqualTo(200);  // Código específico
```

### Cabeçalhos da resposta

```java
restClient
  .post()
  .uri("/orders")
  .exchange()
  .expectHeader()
  .location("/orders/1")
  .contentType(MediaType.APPLICATION_JSON)
  .exists("X-Request-Id")
  .valueEquals("X-Api-Version", "v1");
```

### Asserções do corpo

```java
restClient
  .get()
  .uri("/orders/1")
  .exchange()
  .expectBody(Order.class)
  .value(order -> assertThat(order.getId()).isEqualTo(1L))
  .returnResult();
```

### JSON Path

```java
restClient
  .get()
  .uri("/orders")
  .exchange()
  .expectBody()
  .jsonPath("$.content[0].id").isEqualTo(1)
  .jsonPath("$.content[0].status").isEqualTo("PENDING")
  .jsonPath("$.totalElements").isNumber();
```

## Configuração da solicitação

### Cabeçalhos da solicitação

```java
restClient
  .get()
  .uri("/orders/1")
  .header("Authorization", "Bearer token")
  .header("X-Api-Key", "secret")
  .exchange();
```

### Parâmetros de consulta

```java
restClient
  .get()
  .uri(uriBuilder -> uriBuilder
    .path("/orders")
    .queryParam("status", "PENDING")
    .queryParam("page", 0)
    .queryParam("size", 10)
    .build())
  .exchange();
```

### Variáveis de path

```java
restClient
  .get()
  .uri("/orders/{id}", 1L)
  .exchange();
```

## Com MockMvc

RestTestClient também funciona com MockMvc (sem iniciar o servidor):

```java
@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureRestTestClient
class OrderMockMvcTest {

  @Autowired
  private RestTestClient restClient;

  @Test
  void shouldWorkWithMockMvc() {
    // Usa MockMvc internamente, sem iniciar o servidor
    restClient
      .get()
      .uri("/orders/1")
      .exchange()
      .expectStatus()
      .isOk();
  }
}
```

## Comparação: RestTestClient versus TestRestTemplate

| Recurso | RestTestClient | TestRestTemplate |
| ------- | -------------- | ---------------- |
| Estilo | Fluente/reativo | Imperativo |
| Spring Boot | 4.0+ | Todas as versões (obsoleto na 4) |
| Asserções | Integradas | Manuais |
| Suporte a MockMvc | Sim | Não |
| Assíncrono | Nativo | Exige tratamento adicional |

## Migração do TestRestTemplate

### Antes (obsoleto)

```java
@Autowired
private TestRestTemplate restTemplate;

@Test
void shouldGetOrder() {
  ResponseEntity<Order> response = restTemplate
    .getForEntity("/orders/1", Order.class);

  assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
  assertThat(response.getBody().getId()).isEqualTo(1L);
}
```

### Depois (RestTestClient)

```java
@Autowired
private RestTestClient restClient;

@Test
void shouldGetOrder() {
  restClient
    .get()
    .uri("/orders/1")
    .exchange()
    .expectStatus()
    .isOk()
    .expectBody(Order.class)
    .value(order -> assertThat(order.getId()).isEqualTo(1L));
}
```

## Práticas recomendadas

1. Use com @SpringBootTest(WebEnvironment.RANDOM_PORT) para HTTP real
2. Use com @AutoConfigureMockMvc para testes mais rápidos sem servidor
3. Aproveite as asserções fluentes para melhorar a legibilidade
4. Teste cenários de sucesso e de erro
5. Verifique cabeçalhos de segurança e versionamento da API
