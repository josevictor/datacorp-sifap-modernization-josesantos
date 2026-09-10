# @RestClientTest

Teste isolado de clientes REST com MockRestServiceServer.

## Visão geral

`@RestClientTest` configura automaticamente:

- RestTemplate/RestClient com suporte a servidor simulado
- Jackson ObjectMapper
- MockRestServiceServer

## Configuração básica

```java
@RestClientTest(WeatherService.class)
class WeatherServiceTest {

  @Autowired
  private WeatherService weatherService;

  @Autowired
  private MockRestServiceServer server;
}
```

## Teste de RestTemplate

```java
@RestClientTest(WeatherService.class)
class WeatherServiceTest {

  @Autowired
  private WeatherService weatherService;

  @Autowired
  private MockRestServiceServer server;

  @Test
  void shouldFetchWeather() {
    // Dado
    server.expect(requestTo("https://api.weather.com/v1/current"))
      .andExpect(method(HttpMethod.GET))
      .andExpect(queryParam("city", "Berlin"))
      .andRespond(withSuccess()
        .contentType(MediaType.APPLICATION_JSON)
        .body("{\"temperature\": 22, \"condition\": \"Sunny\"}"));

    // Quando
    Weather weather = weatherService.getCurrentWeather("Berlin");

    // Então
    assertThat(weather.getTemperature()).isEqualTo(22);
    assertThat(weather.getCondition()).isEqualTo("Sunny");
  }
}
```

## Teste de RestClient (Spring 6.1+)

```java
@RestClientTest(WeatherService.class)
class WeatherServiceTest {

  @Autowired
  private WeatherService weatherService;

  @Autowired
  private MockRestServiceServer server;

  @Test
  void shouldFetchWeatherWithRestClient() {
    server.expect(requestTo("https://api.weather.com/v1/current"))
      .andRespond(withSuccess()
        .body("{\"temperature\": 22}"));

    Weather weather = weatherService.getCurrentWeather("Berlin");

    assertThat(weather.getTemperature()).isEqualTo(22);
  }
}
```

## Correspondência de solicitações

### URL exata

```java
server.expect(requestTo("https://api.example.com/users/1"))
  .andRespond(withSuccess());
```

### Padrão de URL

```java
server.expect(requestTo(matchesPattern("https://api.example.com/users/\\d+")))
  .andRespond(withSuccess());
```

### Método HTTP

```java
server.expect(ExpectedCount.once(),
  requestTo("https://api.example.com/users"))
  .andExpect(method(HttpMethod.POST))
  .andRespond(withCreatedEntity(URI.create("/users/1")));
```

### Corpo da solicitação

```java
server.expect(requestTo("https://api.example.com/users"))
  .andExpect(content().contentType(MediaType.APPLICATION_JSON))
  .andExpect(content().json("{\"name\": \"John\"}"))
  .andRespond(withSuccess());
```

### Cabeçalhos

```java
server.expect(requestTo("https://api.example.com/users"))
  .andExpect(header("Authorization", "Bearer token123"))
  .andExpect(header("X-Api-Key", "secret"))
  .andRespond(withSuccess());
```

## Tipos de resposta

### Sucesso com corpo

```java
server.expect(requestTo("/users/1"))
  .andRespond(withSuccess()
    .contentType(MediaType.APPLICATION_JSON)
    .body("{\"id\": 1, \"name\": \"John\"}"));
```

### Sucesso com recurso

```java
server.expect(requestTo("/users/1"))
  .andRespond(withSuccess()
    .body(new ClassPathResource("user-response.json")));
```

### Criado

```java
server.expect(requestTo("/users"))
  .andExpect(method(HttpMethod.POST))
  .andRespond(withCreatedEntity(URI.create("/users/1")));
```

### Resposta de erro

```java
server.expect(requestTo("/users/999"))
  .andRespond(withResourceNotFound());

server.expect(requestTo("/users"))
  .andRespond(withServerError()
    .body("Erro interno do servidor"));

server.expect(requestTo("/users"))
  .andRespond(withStatus(HttpStatus.BAD_REQUEST)
    .body("{\"error\": \"Entrada inválida\"}"));
```

## Verificação de solicitações

```java
@Test
void shouldCallApi() {
  server.expect(ExpectedCount.once(),
    requestTo("https://api.example.com/data"))
    .andRespond(withSuccess());

  service.fetchData();

  server.verify(); // Verifica se todas as expectativas foram atendidas
}
```

## Como ignorar solicitações adicionais

```java
@Test
void shouldHandleMultipleCalls() {
  server.expect(ExpectedCount.manyTimes(),
    requestTo(matchesPattern("/api/.*")))
    .andRespond(withSuccess());

  // Várias chamadas permitidas
  service.callApi();
  service.callApi();
  service.callApi();
}
```

## Reinicialização entre testes

```java
@BeforeEach
void setUp() {
  server.reset();
}
```

## Teste de limites de tempo

```java
server.expect(requestTo("/slow-endpoint"))
  .andRespond(withSuccess()
    .body("{\"data\": \"test\"}")
    .delay(100, TimeUnit.MILLISECONDS));

// Testa o tratamento do limite de tempo
```

## Práticas recomendadas

1. Sempre execute `server.verify()` ao final do teste
2. Use arquivos de recursos para respostas JSON grandes
3. Compare o conjunto mínimo de atributos da solicitação
4. Reinicialize o servidor em @BeforeEach
5. Teste respostas de erro, não apenas sucesso
6. Verifique o corpo da solicitação em chamadas POST/PUT
