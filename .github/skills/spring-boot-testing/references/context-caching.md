# Cache de contexto

Otimize o desempenho da suíte de testes do Spring Boot com cache de contexto.

## Como funciona o cache de contexto

O TestContext Framework do Spring armazena contextos de aplicação em cache com base na "chave" de configuração. Testes com configurações idênticas reutilizam o mesmo contexto.

### O que afeta a chave do cache

- @ContextConfiguration
- @TestPropertySource
- @ActiveProfiles
- @WebAppConfiguration
- definições de @MockitoBean
- importações de @TestConfiguration

## Exemplos de chaves de cache

### Mesma chave (contexto reutilizado)

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest1 {
  @MockitoBean private OrderService orderService;
}

@WebMvcTest(OrderController.class)
class OrderControllerTest2 {
  @MockitoBean private OrderService orderService;
}
// O mesmo contexto é reutilizado
```

### Chave diferente (novo contexto)

```java
@WebMvcTest(OrderController.class)
@ActiveProfiles("test")
class OrderControllerTest1 { }

@WebMvcTest(OrderController.class)
@ActiveProfiles("integration")
class OrderControllerTest2 { }
// Contextos diferentes são carregados
```

## Visualização das estatísticas do cache

### Spring Boot Actuator

```yaml
management:
  endpoints:
    web:
      exposure:
        include: metrics
```

Acesso: `GET /actuator/metrics/spring.test.context.cache`

### Registros de depuração

```properties
logging.level.org.springframework.test.context.cache=DEBUG
```

## Otimização da taxa de acerto do cache

### Agrupe os testes por configuração

```text
 tests/
   unit/           # Sem contexto
   web/            # @WebMvcTest
   repository/     # @DataJpaTest
   integration/    # @SpringBootTest
```

### Minimize variações de @TestPropertySource

**Ruim (vários contextos):**

```java
@TestPropertySource(properties = "app.feature-x=true")
class FeatureXTest { }

@TestPropertySource(properties = "app.feature-y=true")
class FeatureYTest { }
```

**Melhor (agrupado):**

```java
@TestPropertySource(properties = {"app.feature-x=true", "app.feature-y=true"})
class FeaturesTest { }
```

### Use @DirtiesContext com moderação

Somente quando o estado do contexto realmente mudar:

```java
@Test
@DirtiesContext // Força a reconstrução do contexto após o teste
void testThatModifiesBeanDefinitions() { }
```

## Práticas recomendadas

1. **Agrupe por configuração**: mantenha juntos os testes com a mesma configuração
2. **Limite as variações de propriedades**: prefira perfis a propriedades individuais
3. **Evite @DirtiesContext**: prefira limpar os dados de teste
4. **Use fatias restritas**: @WebMvcTest em vez de @SpringBootTest
5. **Monitore os acertos do cache**: habilite os registros de depuração ocasionalmente
