# @DataJpaTest

Teste de repositórios JPA com uma fatia isolada da camada de dados.

## Estrutura básica

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @Autowired
  private OrderRepository orderRepository;

  @Autowired
  private TestEntityManager entityManager;
}
```

## O que é carregado

- Beans de repositório
- EntityManager / TestEntityManager
- DataSource
- Gerenciador de transações
- Nenhuma camada web, nenhum serviço e nenhum controlador

## Teste de consultas personalizadas

```java
@Test
void shouldFindOrdersByStatus() {
  // Dado: uso de var para deixar o código mais limpo
  var pending = new Order("PENDING");
  var completed = new Order("COMPLETED");
  entityManager.persist(pending);
  entityManager.persist(completed);
  entityManager.flush();

  // Quando
  var pendingOrders = orderRepository.findByStatus("PENDING");

  // Então: uso dos métodos de coleções sequenciadas
  assertThat(pendingOrders).hasSize(1);
  assertThat(pendingOrders.getFirst().getStatus()).isEqualTo("PENDING");
}
```

## Teste de consultas nativas

```java
@Test
void shouldExecuteNativeQuery() {
  entityManager.persist(new Order("PENDING", BigDecimal.valueOf(100)));
  entityManager.persist(new Order("PENDING", BigDecimal.valueOf(200)));
  entityManager.flush();

  var total = orderRepository.calculatePendingTotal();

  assertThat(total).isEqualTo(new BigDecimal("300.00"));
}
```

## Teste de paginação

```java
@Test
void shouldReturnPagedResults() {
  // Insere 20 pedidos usando IntStream
  IntStream.range(0, 20).forEach(i -> {
    entityManager.persist(new Order("PENDING"));
  });
  entityManager.flush();

  var page = orderRepository.findByStatus("PENDING", PageRequest.of(0, 10));

  assertThat(page.getContent()).hasSize(10);
  assertThat(page.getTotalElements()).isEqualTo(20);
  assertThat(page.getContent().getFirst().getStatus()).isEqualTo("PENDING");
}
```

## Teste de carregamento tardio

```java
@Test
void shouldLazyLoadOrderItems() {
  var order = new Order("PENDING");
  order.addItem(new OrderItem("Product", 2));
  entityManager.persist(order);
  entityManager.flush();
  entityManager.clear(); // Desanexa do contexto de persistência

  var found = orderRepository.findById(order.getId());

  assertThat(found).isPresent();
  // Isto acionará o carregamento tardio
  assertThat(found.get().getItems()).hasSize(1);
  assertThat(found.get().getItems().getFirst().getProduct()).isEqualTo("Product");
}
```

## Teste de operações em cascata

```java
@Test
void shouldCascadeDelete() {
  var order = new Order("PENDING");
  order.addItem(new OrderItem("Product", 2));
  entityManager.persist(order);
  entityManager.flush();

  orderRepository.delete(order);
  entityManager.flush();

  assertThat(entityManager.find(OrderItem.class, order.getItems().getFirst().getId()))
    .isNull();
}
```

## Teste de métodos @Query

```java
@Query("SELECT o FROM Order o WHERE o.createdAt > :date AND o.status = :status")
List<Order> findRecentByStatus(@Param("date") LocalDateTime date,
                               @Param("status") String status);

@Test
void shouldFindRecentOrders() {
  var old = new Order("PENDING");
  old.setCreatedAt(LocalDateTime.now().minusDays(10));
  var recent = new Order("PENDING");
  recent.setCreatedAt(LocalDateTime.now().minusHours(1));

  entityManager.persist(old);
  entityManager.persist(recent);
  entityManager.flush();

  var recentOrders = orderRepository.findRecentByStatus(
    LocalDateTime.now().minusDays(1), "PENDING");

  assertThat(recentOrders).hasSize(1);
  assertThat(recentOrders.getFirst().getId()).isEqualTo(recent.getId());
}
```

## Uso de H2 versus banco de dados real

### H2 (padrão, não recomendado para paridade com produção)

```java
@DataJpaTest // Usa H2 integrado por padrão
class OrderRepositoryH2Test {
  // Rápido, mas pode não detectar problemas específicos do banco
}
```

### Testcontainers (recomendado)

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryPostgresTest {
  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");
}
```

## Comportamento das transações

Os testes são @Transactional por padrão e executam reversão após cada teste.

```java
@Test
@Rollback(false) // Não executa reversão (raramente necessário)
void shouldPersistData() {
  orderRepository.save(new Order("PENDING"));
  // Os dados permanecerão no banco após o teste
}
```

## Pontos principais

1. Use TestEntityManager para preparar os dados
2. Sempre execute flush() após persist() para acionar o SQL
3. Execute clear() no gerenciador de entidades para testar o carregamento tardio
4. Use um banco real (Testcontainers) para obter resultados precisos
5. Teste casos de sucesso e falha
6. Aproveite a palavra-chave var do Java 21 para declarações mais limpas
7. Use métodos de coleções sequenciadas (getFirst(), getLast(), reversed())
