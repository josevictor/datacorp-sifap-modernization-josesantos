---
description: "Use ao escrever ou revisar asserções JUnit 5 (Jupiter) em testes Java de backend — ordem do valor esperado, mensagens Supplier lazy, agrupamento assertAll, assertThrows e assertThrowsExactly, timeouts e assertInstanceOf."
applyTo: "**/*Test.java,**/*IT.java,**/*Steps.java,**/*StepDefs.java"
---

# Asserções JUnit 5 — Convenções de asserções Jupiter

Este arquivo é ativado em testes Java de backend (`*Test.java`, `*IT.java`, `*Steps.java`, `*StepDefs.java`). Ele ensina a usar corretamente as `org.junit.jupiter.api.Assertions` integradas do JUnit Jupiter no Java 21: ordem do valor esperado, mensagens de falha lazy, asserções agrupadas, verificações de exceção e tipo e timeouts. Ele ensina como fazer asserções, mas não decide estratégia de testes, escolha de slice, política de mocks ou metas de cobertura. A estrutura e a pirâmide ficam na skill [`java-junit`](../skills/java-junit/SKILL.md), os testes de slice e integração Spring na skill [`spring-boot-testing`](../skills/spring-boot-testing/SKILL.md) e a rastreabilidade e cobertura em [`tests.instructions.md`](tests.instructions.md).

> [!NOTE]
> Estas são as `Assertions` integradas do Jupiter. Para cadeias fluentes e verificações avançadas de objetos ou coleções, o kit prefere AssertJ (`assertThat(...)`), como em [`tests.instructions.md`](tests.instructions.md) e na skill [`spring-boot-testing`](../skills/spring-boot-testing/SKILL.md). Use as asserções Jupiter abaixo para verificações agrupadas, de exceção, timeout, tipo exato e igualdade simples.

## Imports estáticos

Importe cada asserção estaticamente para que os métodos de teste expressem intenção, não código repetitivo. Prefira imports explícitos ao curinga, salvo quando o módulo já o padronizar.

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertAll;

assertEquals(expected, actual);
```

Sempre importe de `org.junit.jupiter.api.Assertions`. Nunca misture `org.junit.Assert` (JUnit 4): a ordem dos argumentos é diferente, e as APIs não são intercambiáveis.

## Valor esperado primeiro

`expected` é sempre o **primeiro** argumento, e `actual`, o **segundo**, para que o log de falha informe corretamente "esperado X, mas encontrado Y".

```java
// Evite — ordem invertida; a mensagem de falha engana
assertEquals(resourceService.count(), 2);

// Prefira
assertEquals(2, resourceService.count());

// Ponto flutuante inevitável (nunca dinheiro, que usa BigDecimal): informe um delta
assertEquals(0.3, 0.1 + 0.2, 1e-9);
```

> [!WARNING]
> `assertEquals` em `BigDecimal` usa `equals`, que é sensível à escala: `new BigDecimal("10.0")` **não** é igual a `new BigDecimal("10.00")`. Para valores monetários, compare o valor com `assertEquals(0, expected.compareTo(actual))` ou use `isEqualByComparingTo` do AssertJ.

## Mensagens de falha: Supplier e String

Passe a mensagem como `Supplier<String>` quando sua construção for cara, para criar a string somente na falha. Um literal constante pode continuar como `String`.

```java
// Evite — a mensagem formatada é criada mesmo quando a asserção passa
assertEquals(expected, actual, "expected %s but got %s".formatted(expected, actual));

// Prefira — avaliação lazy, somente na falha
assertEquals(expected, actual,
    () -> "expected %s but got %s".formatted(expected, actual));

// Adequado — um literal constante não gera custo adicional
assertTrue(account.isActive(), "account must be active");
```

## Agrupamento com assertAll

Use `assertAll` para verificar várias propriedades de um resultado; todas as asserções executam mesmo quando uma anterior falha, mostrando todas as divergências.

```java
record PaymentView(String beneficiary, BigDecimal amount, PaymentStatus status) {}

@Test
void should_map_all_fields_when_building_view() { // REQ-042
    PaymentView view = mapper.toView(payment);
    assertAll("payment view",
        () -> assertEquals("ACME LTDA", view.beneficiary()),
        () -> assertEquals(0, new BigDecimal("1500.00").compareTo(view.amount())),
        () -> assertEquals(PaymentStatus.APPROVED, view.status())
    );
}
```

Não crie manualmente uma sequência de asserções isoladas para verificar um objeto; a primeira falha oculta as demais.

## Exceções: assertThrows e assertThrowsExactly

`assertThrows` retorna a exceção lançada para permitir verificações e aceita subtipos da classe esperada. Use `assertThrowsExactly` (JUnit 5.8+) quando a classe exata fizer parte do contrato.

```java
@Test
void should_reject_duplicate_label_when_it_exists() { // REQ-021
    var request = new CreateResourceRequest("alpha", new BigDecimal("5.00"));
    ResourceConflictException ex = assertThrows(
        ResourceConflictException.class,
        () -> resourceService.create(request));
    assertEquals("alpha", ex.conflictingLabel());
}

// Tipo exato obrigatório — uma subclasse NÃO deve satisfazer esta asserção
assertThrowsExactly(IllegalArgumentException.class, () -> ResourceLabel.of(""));
```

## assertDoesNotThrow

Use `assertDoesNotThrow` somente quando a ausência de exceção for o contrato em teste; ele retorna o valor para outras asserções.

```java
BigDecimal total = assertDoesNotThrow(() -> invoiceService.total(batch));
assertEquals(0, new BigDecimal("2500.00").compareTo(total));
```

## Timeouts

Use `assertTimeout` para verificar uma duração sem interromper o trabalho. Use `assertTimeoutPreemptively` somente quando for necessário abortar rigidamente.

```java
assertTimeout(Duration.ofSeconds(1), () -> reportService.generate(batch));

assertTimeoutPreemptively(Duration.ofMillis(500), () -> validator.check(payload));
```

> [!WARNING]
> `assertTimeoutPreemptively` executa o código em uma **thread separada**, por isso o estado `ThreadLocal` não é propagado. O `EntityManager` vinculado de um teste `@Transactional` e qualquer contexto de segurança ficam ausentes. Nunca envolva nele uma chamada transacional de persistência.

## Verificações de tipo: assertInstanceOf

Prefira `assertInstanceOf` (JUnit 5.8+) a `assertTrue(x instanceof T)`; ele falha com mensagem útil e retorna o valor já convertido, adequado aos tipos de resultado sealed do kit.

```java
sealed interface PaymentResult permits Approved, Rejected {}

Approved approved = assertInstanceOf(Approved.class, paymentService.process(request));
assertEquals(42L, approved.paymentId());
```

## Coleções e arrays

Use as asserções específicas para que as falhas mostrem um diff por elemento em vez de um `false` opaco.

```java
assertIterableEquals(List.of("alpha", "beta"), resourceService.labels()); // diff profundo ordenado
assertArrayEquals(expectedBytes, actualBytes);
```

## Convenções

| Regra | Justificativa |
|---|---|
| `expected` primeiro e `actual` depois em `assertEquals` | O log de falha mostra corretamente o esperado e o encontrado |
| Compare `BigDecimal` por valor, não com `equals` | `equals` é sensível à escala e falha silenciosamente com dinheiro |
| Envolva mensagens caras em `Supplier<String>` | A mensagem só é criada quando a asserção falha |
| Agrupe verificações relacionadas com `assertAll` | Todas as propriedades são informadas |
| `assertThrows` para hierarquia, `assertThrowsExactly` para classe exata | Corresponde à rigidez do tipo no contrato |
| `assertInstanceOf` em vez de `assertTrue(... instanceof ...)` | Retorna o valor convertido e falha com mensagem útil |
| Importe somente de `org.junit.jupiter.api.Assertions` | `org.junit.Assert` do JUnit 4 usa outra ordem de argumentos |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Coloque `expected` antes de `actual` | Inverta-os e gere logs enganosos |
| Compare dinheiro com `compareTo` ou `isEqualByComparingTo` | Compare `BigDecimal` com `equals`, sensível à escala |
| Use `assertEquals(2, result)` para valores | Use `assertTrue(result == 2)` e perca os valores no log |
| Verifique o valor quando possível | Limite-se a `assertNotNull` quando houver verificação real |
| Use `Supplier` para mensagens caras | Crie mensagem formatada em toda execução |
| Não use `assertTimeoutPreemptively` em código transacional | Envolva persistência `@Transactional` e perca o `EntityManager` |
| Permita que as asserções falhem claramente | Capture `AssertionError` para ocultar falha |

## Lista de verificação antes de abrir uma PR

- [ ] Todo `assertEquals` lista `expected` primeiro e `actual` depois
- [ ] `BigDecimal` e outros valores monetários são comparados por valor, não com `equals` sensível à escala
- [ ] Verificações de várias propriedades usam `assertAll`; mensagens caras usam `Supplier<String>`
- [ ] Testes de exceção escolhem deliberadamente `assertThrows` ou `assertThrowsExactly` e verificam a exceção retornada
- [ ] `assertTimeoutPreemptively` não envolve código transacional nem vinculado a `ThreadLocal`
- [ ] Os imports são somente do Jupiter; não há mistura com `org.junit.Assert` (JUnit 4)
- [ ] Testes orientados por requisitos mantêm o comentário inline `// REQ-NNN` (consulte [`tests.instructions.md`](tests.instructions.md))
