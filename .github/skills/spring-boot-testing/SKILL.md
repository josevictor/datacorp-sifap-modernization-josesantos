---
name: "spring-boot-testing"
description: "Seleciona a técnica de teste adequada do Spring Boot para um cenário: fatias (@WebMvcTest, @DataJpaTest, @RestClientTest, @JsonTest, @SpringBootTest), Testcontainers, Mockito e AssertJ. Use ao escrever ou revisar testes de integração ou de fatia do Spring Boot. Destina-se ao Spring Boot 3.3 + JUnit 5 do kit; APIs mais recentes das versões 3.4+/4.0 (MockMvcTester, @MockitoBean, RestTestClient) estão fora do escopo."
---
# Testes com Spring Boot

Esta habilidade ajuda a escolher a técnica de teste do Spring Boot adequada para um cenário. Destina-se ao conjunto tecnológico **Spring Boot 3.3 + JUnit 5 + Testcontainers** do kit. Algumas APIs mais recentes do Spring Boot 3.4+/4.0 aparecem apenas como referência e estão claramente marcadas como **fora do escopo do kit**. Para testes unitários simples de lógica de negócio, sem contexto Spring, use [`java-junit`](../java-junit/SKILL.md).

## Quando invocar

- "Qual fatia de teste devo usar para este controlador?"
- "Escreva um `@DataJpaTest` contra um PostgreSQL real com Testcontainers."
- "Revise a camada e o escopo destes testes do Spring Boot."
- "Configure o Testcontainers para nossos testes de integração."

## Princípios básicos

1. **Pirâmide de testes**: unitário (rápido) > fatia (focada) > integração (completo)
2. **Ferramenta adequada**: use a fatia mais restrita que ofereça confiança
3. **Estilo AssertJ**: prefira asserções fluentes e legíveis a comparadores verbosos
4. **Conjunto tecnológico do kit**: no Spring Boot 3.3, use MockMvc clássico e `@MockBean`; as APIs mais recentes MockMvcTester / `@MockitoBean` / RestTestClient (3.4+/4.0) estão fora do escopo

## Qual fatia de teste usar?

| Cenário | Anotação | Referência |
|----------|------------|-----------|
| Controlador + semântica HTTP | `@WebMvcTest` | [references/webmvctest.md](references/webmvctest.md) |
| Repositório + consultas JPA | `@DataJpaTest` | [references/datajpatest.md](references/datajpatest.md) |
| Cliente REST + APIs externas | `@RestClientTest` | [references/restclienttest.md](references/restclienttest.md) |
| (Des)serialização JSON | `@JsonTest` | [references/test-slices-overview.md](references/test-slices-overview.md) |
| Aplicação completa | `@SpringBootTest` | [references/test-slices-overview.md](references/test-slices-overview.md) |

## Referência de fatias de teste

- [references/test-slices-overview.md](references/test-slices-overview.md): matriz de decisão e comparação
- [references/webmvctest.md](references/webmvctest.md): camada web com MockMvc
- [references/datajpatest.md](references/datajpatest.md): camada de dados com Testcontainers
- [references/restclienttest.md](references/restclienttest.md): testes de cliente REST

## Referência de ferramentas de teste

- [references/mockmvc-classic.md](references/mockmvc-classic.md): MockMvc clássico, padrão do kit no Spring Boot 3.3
- [references/mockmvc-tester.md](references/mockmvc-tester.md): MockMvc no estilo AssertJ (Spring Boot 3.4+, fora do escopo)
- [references/mockitobean.md](references/mockitobean.md): objetos simulados com `@MockitoBean` (Spring Boot 3.4+, fora do escopo)
- [references/resttestclient.md](references/resttestclient.md): RestTestClient (Spring Boot 4.0, fora do escopo)

## Bibliotecas de asserção

- [references/assertj-basics.md](references/assertj-basics.md): escalares, strings, booleanos e datas
- [references/assertj-collections.md](references/assertj-collections.md): listas, conjuntos, mapas e arrays

## Testcontainers

- [references/testcontainers-jdbc.md](references/testcontainers-jdbc.md): PostgreSQL 16 e outros bancos de dados JDBC

## Geração de dados de teste

- [references/instancio.md](references/instancio.md): geração de objetos de teste complexos (3 ou mais propriedades)

## Desempenho e migração

- [references/context-caching.md](references/context-caching.md): aceleração das suítes de teste
- [references/sb4-migration.md](references/sb4-migration.md): alterações do Spring Boot 4.0

## Árvore de decisão rápida

```text
Testando um ponto de acesso de controlador?
  Sim → @WebMvcTest com MockMvc clássico (MockMvcTester exige Spring Boot 3.4+)

Testando consultas de repositório?
  Sim → @DataJpaTest com Testcontainers (banco de dados real)

Testando lógica de negócio no serviço?
  Sim → JUnit simples + Mockito (sem contexto Spring)

Testando cliente de API externa?
  Sim → @RestClientTest com MockRestServiceServer

Testando mapeamento JSON?
  Sim → @JsonTest

Precisa de um teste de integração completo?
  Sim → @SpringBootTest com configuração mínima de contexto
```

## APIs mais recentes fora do escopo do kit (Spring Boot 3.4+/4.0)

O kit está fixado em **Spring Boot 3.3 + JUnit 5**. As APIs mais recentes a seguir são listadas
apenas para conhecimento. Não as adote no código do kit:

- **MockMvcTester**: asserções MockMvc no estilo AssertJ (Spring Boot 3.4+). Na versão 3.3, use MockMvc clássico.
- **@MockitoBean**: substitui `@MockBean` (Spring Boot 3.4+). Na versão 3.3, use `@MockBean`.
- **RestTestClient**: alternativa ao `TestRestTemplate` (Spring Boot 4.0). Na versão 3.3, use `TestRestTemplate` ou `RestClient`.
- **Inicializadores de teste modulares** e **pausa de contexto** (Spring Boot 4.0 / Spring Framework 7).

Consulte [references/sb4-migration.md](references/sb4-migration.md) somente se o projeto realmente for atualizado para uma versão posterior à 3.3.

## Práticas recomendadas de teste

### Avaliação da complexidade do código

Quando um método ou uma classe for complexo demais para ser testado com eficácia:

1. **Analise a complexidade**: se forem necessários mais de cinco a sete casos de teste para cobrir um único método, ele provavelmente é complexo demais
2. **Recomende a refatoração**: sugira dividir o código em funções menores e focadas
3. **Respeite a decisão da pessoa**: se ela concordar com a refatoração, ajude a identificar pontos de extração
4. **Prossiga se necessário**: se ela decidir manter o código complexo, implemente os testes apesar da dificuldade

**Exemplo de recomendação de refatoração:**

```java
// Antes: método complexo e difícil de testar
public Order processOrder(OrderRequest request) {
  // Validação, cálculo de desconto, pagamento, estoque, notificação...
  // Mais de 50 linhas com responsabilidades misturadas
}

// Depois: refatorado em unidades testáveis
public Order processOrder(OrderRequest request) {
  validateOrder(request);
  var order = createOrder(request);
  applyDiscount(order);
  processPayment(order);
  updateInventory(order);
  sendNotification(order);
  return order;
}
```

### Evite repetição de código

Crie métodos auxiliares para objetos usados com frequência e para a configuração de objetos simulados, melhorando a legibilidade e a manutenibilidade.

### Organização de testes com @DisplayName

Use nomes de exibição descritivos para esclarecer a intenção do teste:

```java
@Test
@DisplayName("Deve calcular o desconto para cliente VIP")
void shouldCalculateDiscountForVip() { }

@Test
@DisplayName("Deve rejeitar o pedido quando o cliente não tiver crédito suficiente")
void shouldRejectOrderForInsufficientCredit() { }
```

### Ordem da cobertura de testes

Sempre estruture os testes nesta ordem:

1. **Cenário principal**: fluxo de sucesso, caso de uso mais comum
2. **Outros fluxos**: cenários válidos alternativos e casos-limite
3. **Exceções/erros**: entradas inválidas, condições de erro e modos de falha

### Teste cenários de produção

Escreva testes pensando em cenários reais de produção. Isso torna os testes mais compreensíveis e ajuda a entender o comportamento do código em casos reais.

### Metas de cobertura de testes

Busque 80% de cobertura de código como equilíbrio prático entre qualidade e esforço. Uma cobertura maior é benéfica, mas não é o único objetivo.

Use o plugin Maven JaCoCo para gerar relatórios e acompanhar a cobertura.

**Regras de cobertura:**

- Cobertura mínima de 80%
- Foco em asserções relevantes, não apenas na execução

**O que priorizar:**

1. Fluxos críticos de negócio (processamento de pagamentos, validação de pedidos)
2. Algoritmos complexos (precificação, cálculo de descontos)
3. Tratamento de erros (exceções, casos-limite)
4. Pontos de integração (APIs externas, bancos de dados)

## Dependências (Spring Boot 3.3)

`spring-boot-starter-test` já inclui JUnit 5, Mockito, AssertJ e MockMvc. Adicione o módulo de
suporte do Testcontainers para executar `@DataJpaTest` / `@SpringBootTest` contra um PostgreSQL 16 real.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>

<!-- Suporte do Testcontainers (PostgreSQL real para @DataJpaTest / @SpringBootTest) -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>postgresql</artifactId>
  <scope>test</scope>
</dependency>
```

## Modelo de saída

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class PaymentRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired
    PaymentRepository repository;

    @Test
    void findsByStatus() {
        repository.save(new Payment("PENDING"));
        assertThat(repository.findByStatus("PENDING")).hasSize(1);
    }
}
```

## Critérios de qualidade

- [ ] É usada a fatia mais restrita que ofereça confiança (unitário -> fatia -> `@SpringBootTest`).
- [ ] Os testes da camada de dados e de integração completa são executados contra um PostgreSQL 16 real via Testcontainers, não H2.
- [ ] No Spring Boot 3.3, são usados `MockMvc` clássico e `@MockBean`; nenhuma API 3.4+/4.0 (MockMvcTester, `@MockitoBean`, RestTestClient) é adotada.
- [ ] As asserções usam `assertThat` do AssertJ; cada teste se concentra em um comportamento.
- [ ] A suíte reutiliza o contexto Spring quando possível (consulte context-caching) para permanecer rápida.
- [ ] `./mvnw test` passa localmente antes da abertura do PR.
