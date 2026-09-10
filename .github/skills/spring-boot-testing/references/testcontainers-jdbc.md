# Testcontainers JDBC

Teste de repositórios JPA com bancos de dados reais usando Testcontainers.

## Visão geral

O Testcontainers fornece instâncias reais de bancos de dados em contêineres Docker para testes de integração. É mais confiável que o H2 para manter a paridade com produção.

## Configuração do PostgreSQL

### Dependências

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>testcontainers-postgresql</artifactId>
  <scope>test</scope>
</dependency>
```

### Teste básico

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryPostgresTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @Autowired
  private OrderRepository orderRepository;

  @Autowired
  private TestEntityManager entityManager;
}
```

## Configuração do MySQL

```xml
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>testcontainers-mysql</artifactId>
  <scope>test</scope>
</dependency>
```

```java
@Container
@ServiceConnection
static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.4");
```

## Vários bancos de dados

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class MultiDatabaseTest {

  @Container
  @ServiceConnection(name = "primary")
  static PostgreSQLContainer<?> primaryDb = new PostgreSQLContainer<>("postgres:16");

  @Container
  @ServiceConnection(name = "analytics")
  static PostgreSQLContainer<?> analyticsDb = new PostgreSQLContainer<>("postgres:16");
}
```

## Reutilização de contêineres (otimização de velocidade)

Adicione a `~/.testcontainers.properties`:

```properties
testcontainers.reuse.enable=true
```

Em seguida, habilite a reutilização no código:

```java
@Container
@ServiceConnection
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
  .withReuse(true);
```

## Inicialização do banco de dados

### Com scripts SQL

```java
@Container
@ServiceConnection
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
  .withInitScript("schema.sql");
```

### Com Flyway

```java
@SpringBootTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class MigrationTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @Autowired
  private Flyway flyway;

  @Test
  void shouldApplyMigrations() {
    flyway.migrate();
    // Código do teste
  }
}
```

## Configuração avançada

### Banco de dados ou esquema personalizado

```java
@Container
@ServiceConnection
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
  .withDatabaseName("testdb")
  .withUsername("testuser")
  .withPassword("testpass")
  .withInitScript("init-schema.sql");
```

### Estratégias de espera

```java
@Container
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
  .waitingFor(Wait.forLogMessage(".*database system is ready.*", 1));
```

## Exemplo de teste

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

  @Test
  void shouldFindOrdersByStatus() {
    // Dado
    entityManager.persist(new Order("PENDING"));
    entityManager.persist(new Order("COMPLETED"));
    entityManager.flush();

    // Quando
    List<Order> pending = orderRepository.findByStatus("PENDING");

    // Então
    assertThat(pending).hasSize(1);
    assertThat(pending.get(0).getStatus()).isEqualTo("PENDING");
  }

  @Test
  void shouldSupportPostgresSpecificFeatures() {
    // Pode usar recursos específicos do Postgres, como:
    // - colunas JSONB
    // - tipos array
    // - busca textual
  }
}
```

## Alternativa com @DynamicPropertySource

Se não usar @ServiceConnection:

```java
@SpringBootTest
@Testcontainers
class OrderServiceTest {

  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @DynamicPropertySource
  static void configureProperties(DynamicPropertyRegistry registry) {
    registry.add("spring.datasource.url", postgres::getJdbcUrl);
    registry.add("spring.datasource.username", postgres::getUsername);
    registry.add("spring.datasource.password", postgres::getPassword);
  }
}
```

## Bancos de dados compatíveis

| Banco de dados | Classe do contêiner | Artefato Maven |
| -------- | --------------- | -------------- |
| PostgreSQL | PostgreSQLContainer | testcontainers-postgresql |
| MySQL | MySQLContainer | testcontainers-mysql |
| MariaDB | MariaDBContainer | testcontainers-mariadb |
| SQL Server | MSSQLServerContainer | testcontainers-mssqlserver |
| Oracle | OracleContainer | testcontainers-oracle-free |
| MongoDB | MongoDBContainer | testcontainers-mongodb |

## Práticas recomendadas

1. Use @ServiceConnection quando possível (Spring Boot 3.1+)
2. Habilite a reutilização de contêineres para acelerar compilações locais
3. Use versões específicas (postgres:16), não a versão mais recente
4. Mantenha a configuração do contêiner em um campo estático
5. Use @DataJpaTest com AutoConfigureTestDatabase.Replace.NONE
