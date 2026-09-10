---
name: "java-junit"
description: "Práticas recomendadas para testes unitários com JUnit 5: estrutura Preparar-Agir-Verificar, ciclo de vida, testes parametrizados e orientados a dados, asserções, isolamento com Mockito e organização. Use ao escrever ou revisar testes unitários simples com JUnit 5 para lógica de negócio Java. Para testes de fatia ou integração do Spring Boot (@WebMvcTest, @DataJpaTest, Testcontainers), use spring-boot-testing."
---
# Práticas recomendadas do JUnit 5

Escreva testes unitários focados com JUnit 5 para a lógica de negócio da camada de servidor do SIFAP 2.0 (Java 21 + Spring Boot 3.3). Cubra abordagens padrão e orientadas a dados com isolamento por Mockito e asserções AssertJ. Para testes de fatia ou integração do Spring Boot (`@WebMvcTest`, `@DataJpaTest`, Testcontainers), use a habilidade [`spring-boot-testing`](../spring-boot-testing/SKILL.md). Para o ciclo vermelho-verde-refatorar, consulte [`tdd-workflow`](../tdd-workflow/SKILL.md).

## Quando invocar

- "Escreva testes JUnit 5 para este serviço."
- "Adicione um teste parametrizado que cubra estes valores-limite."
- "Revise o isolamento e os nomes destes testes unitários."
- "Cubra os fluxos de erro deste método de negócio."

## Configuração do projeto

- Use o layout padrão do Maven ou Gradle e coloque os testes em `src/test/java`.
- `spring-boot-starter-test` já inclui JUnit 5 (inclusive `junit-jupiter-params`), Mockito e AssertJ no conjunto tecnológico do kit. Nenhuma dependência de teste adicional é necessária.
- Execute os testes com `./mvnw test` (ou `./gradlew test`).

## Estrutura dos testes

- As classes de teste devem ter o sufixo `Test`, por exemplo, `CalculatorTest` para uma classe `Calculator`.
- Use `@Test` nos métodos de teste.
- Siga o padrão Preparar-Agir-Verificar.
- Nomeie os testes com uma convenção descritiva, como `methodName_should_expectedBehavior_when_scenario`.
- Use `@BeforeEach` e `@AfterEach` para preparação e limpeza por teste.
- Use `@BeforeAll` e `@AfterAll` para preparação e limpeza por classe. Esses métodos devem ser estáticos.
- Use `@DisplayName` para fornecer um nome legível às classes e aos métodos de teste.
- Referencie o requisito testado com um comentário `// REQ-NNN`. O kit rastreia testes até REQ-IDs.

## Testes padrão

- Mantenha cada teste focado em um único comportamento.
- Evite testar várias condições no mesmo método de teste.
- Crie testes independentes e idempotentes, que possam ser executados em qualquer ordem.
- Evite interdependências entre testes.

## Testes orientados a dados (parametrizados)

Marque o método com `@ParameterizedTest` em vez de `@Test` e forneça os argumentos com uma anotação de origem:

| Origem | Uso |
|---|---|
| `@ValueSource` | Um parâmetro de literais simples (textos e números inteiros) |
| `@CsvSource` | Linhas inline de valores separados por vírgulas (vários parâmetros) |
| `@CsvFileSource` | Linhas carregadas de um arquivo CSV no caminho de classes |
| `@MethodSource` | Argumentos criados por um método fábrica que retorna `Stream` ou `Collection` |
| `@EnumSource` | Todas as constantes, ou um subconjunto nomeado, de um enum |

## Asserções

- Prefira o `assertThat(...)` fluente do AssertJ para produzir falhas legíveis. Ele já está no caminho de classes do kit.
- Os métodos `org.junit.jupiter.api.Assertions` do JUnit (`assertEquals`, `assertTrue`, `assertNotNull`) continuam disponíveis.
- Use `assertThrows` (ou `assertThatThrownBy` do AssertJ) para verificar exceções.
- Agrupe asserções relacionadas com `assertAll` para verificar todas antes de o teste falhar.
- Use mensagens descritivas nas asserções para esclarecer a falha.

## Objetos simulados e isolamento

- Use uma estrutura de simulação como o Mockito para criar objetos simulados para as dependências.
- Use as anotações `@Mock` e `@InjectMocks` do Mockito para simplificar a criação e a injeção de objetos simulados.
- Use interfaces para facilitar a criação de objetos simulados.

## Organização dos testes

- Agrupe os testes por funcionalidade ou componente usando pacotes.
- Use `@Tag` para categorizar testes, por exemplo, `@Tag("fast")` e `@Tag("integration")`.
- Use `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` e `@Order` para controlar a ordem de execução somente quando for estritamente necessário.
- Use `@Disabled` para ignorar temporariamente um método ou uma classe de teste e sempre informe o motivo.
- Use `@Nested` para agrupar testes relacionados em uma classe interna aninhada.

## Modelo de saída

```java
// REQ-042: o imposto é zero para cliente isento
@ExtendWith(MockitoExtension.class)
class TaxCalculatorTest {

    @Mock TaxRateProvider rateProvider;
    @InjectMocks TaxCalculator calculator;

    @Test
    @DisplayName("retorna imposto zero para cliente isento")
    void returnsZeroForTaxExemptCustomer() {
        // Preparar
        var customer = new Customer(Status.TAX_EXEMPT);
        // Agir
        var tax = calculator.taxFor(customer);
        // Verificar
        assertThat(tax).isEqualTo(Money.ZERO);
    }

    @ParameterizedTest(name = "renda {0} -> imposto {1}")
    @CsvSource({ "1000, 100", "2000, 200" })
    void appliesFlatRate(BigDecimal income, BigDecimal expected) {
        when(rateProvider.ratePercent()).thenReturn(new BigDecimal("10"));
        assertThat(calculator.taxFor(income)).isEqualByComparingTo(expected);
    }
}
```

## Critérios de qualidade

- [ ] Cada teste verifica um comportamento e é executado independentemente dos demais, em qualquer ordem.
- [ ] Os nomes dos testes descrevem o comportamento, e a classe contém um comentário de rastreabilidade `// REQ-NNN`.
- [ ] Os casos-limite e os fluxos de erro estão cobertos, não apenas o fluxo de sucesso.
- [ ] Os colaboradores estão isolados com Mockito; nenhum teste unitário usa banco de dados, relógio ou rede reais.
- [ ] As asserções são relevantes (`assertThat` do AssertJ), não apenas "não lança exceção".
- [ ] `./mvnw test` passa localmente antes da abertura do PR.
