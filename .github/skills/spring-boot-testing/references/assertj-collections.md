# Coleções no AssertJ

Asserções AssertJ para coleções: `List`, `Set`, `Map`, arrays (vetores) e fluxos.

## Quando usar esta referência

- O valor testado é `List`, `Set`, `Map`, array ou `Stream`
- Você precisa verificar vários elementos, sua ordem ou campos específicos
- Você usa `extracting()`, `filteredOn()`, `containsExactly()` ou métodos semelhantes de coleção
- Para verificar um único escalar ou objeto, use [assertj-basics.md](assertj-basics.md)

## Verificações básicas de coleções

```java
List<Order> orders = orderService.findAll();

assertThat(orders).isNotEmpty();
assertThat(orders).isEmpty();
assertThat(orders).hasSize(3);
assertThat(orders).hasSizeGreaterThan(0);
assertThat(orders).hasSizeLessThanOrEqualTo(10);
```

## Asserções de contenção

```java
// Contém (qualquer ordem, permite itens adicionais)
assertThat(orders).contains(order1, order2);

// Contém exatamente estes elementos nesta ordem (sem itens adicionais)
assertThat(statuses).containsExactly("NEW", "PENDING", "COMPLETED");

// Contém exatamente estes elementos em qualquer ordem (sem itens adicionais)
assertThat(statuses).containsExactlyInAnyOrder("COMPLETED", "NEW", "PENDING");

// Contém qualquer um destes elementos (pelo menos uma correspondência)
assertThat(statuses).containsAnyOf("NEW", "CANCELLED");

// Não contém
assertThat(statuses).doesNotContain("DELETED");
```

## Extração de campos

Extraia um campo de cada elemento antes da asserção:

```java
assertThat(orders)
  .extracting(Order::getStatus)
  .containsExactly("NEW", "PENDING", "COMPLETED");
```

Extraia vários campos como tuplas:

```java
assertThat(orders)
  .extracting(Order::getId, Order::getStatus)
  .containsExactly(
    tuple(1L, "NEW"),
    tuple(2L, "PENDING"),
    tuple(3L, "COMPLETED")
  );
```

## Filtragem antes da asserção

```java
assertThat(orders)
  .filteredOn(order -> order.getStatus().equals("PENDING"))
  .hasSize(2)
  .extracting(Order::getId)
  .containsExactlyInAnyOrder(1L, 3L);

// Filtra pelo valor do campo
assertThat(orders)
  .filteredOn("status", "PENDING")
  .hasSize(2);
```

## Verificações com predicados

```java
assertThat(orders).allMatch(o -> o.getTotal().compareTo(BigDecimal.ZERO) > 0);
assertThat(orders).anyMatch(o -> o.getStatus().equals("COMPLETED"));
assertThat(orders).noneMatch(o -> o.getStatus().equals("DELETED"));

// Com descrição para mensagens de falha
assertThat(orders)
  .allSatisfy(o -> assertThat(o.getId()).isPositive());
```

## Asserções ordenadas por elemento

Verifique cada elemento em ordem com condições individuais:

```java
assertThat(orders).satisfiesExactly(
  first  -> assertThat(first.getStatus()).isEqualTo("NEW"),
  second -> assertThat(second.getStatus()).isEqualTo("PENDING"),
  third  -> {
    assertThat(third.getStatus()).isEqualTo("COMPLETED");
    assertThat(third.getTotal()).isGreaterThan(BigDecimal.ZERO);
  }
);
```

## Coleções aninhadas e planas

```java
// flatExtracting: achata um nível de coleções aninhadas
assertThat(orders)
  .flatExtracting(Order::getItems)
  .extracting(OrderItem::getProduct)
  .contains("Laptop", "Mouse");
```

## Comparação recursiva de campos

Compare elementos por campos, não pela identidade do objeto:

```java
assertThat(orders)
  .usingRecursiveFieldByFieldElementComparator()
  .containsExactlyInAnyOrder(expectedOrder1, expectedOrder2);

// Ignora campos específicos (por exemplo, IDs gerados ou timestamps)
assertThat(orders)
  .usingRecursiveFieldByFieldElementComparatorIgnoringFields("id", "createdAt")
  .containsExactly(expectedOrder1, expectedOrder2);
```

## Asserções de mapas

```java
Map<String, Integer> stockByProduct = inventoryService.getStock();

assertThat(stockByProduct)
  .isNotEmpty()
  .hasSize(3)
  .containsKey("Laptop")
  .doesNotContainKey("Fax Machine")
  .containsEntry("Laptop", 10)
  .containsEntries(entry("Laptop", 10), entry("Mouse", 50));

assertThat(stockByProduct)
  .hasEntrySatisfying("Laptop", qty -> assertThat(qty).isGreaterThan(0));
```

## Asserções de arrays

```java
String[] roles = user.getRoles();

assertThat(roles).hasSize(2);
assertThat(roles).contains("ADMIN");
assertThat(roles).containsExactlyInAnyOrder("USER", "ADMIN");
```

## Asserções de conjuntos

```java
Set<String> tags = product.getTags();

assertThat(tags).contains("electronics", "sale");
assertThat(tags).doesNotContain("expired");
assertThat(tags).hasSizeGreaterThanOrEqualTo(1);
```

## Import estático

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.tuple;
import static org.assertj.core.api.Assertions.entry;
```

## Pontos principais

1. **`containsExactly` versus `containsExactlyInAnyOrder`**: use o primeiro quando a ordem for importante
2. **`extracting()` antes das verificações de contenção**: evita implementar `equals()` nos objetos do domínio
3. **`filteredOn()` + `extracting()`**: combine-os para verificar precisamente um subconjunto da coleção
4. **`satisfiesExactly()`**: use quando cada elemento exigir asserções diferentes
5. **`usingRecursiveFieldByFieldElementComparator()`**: prefira-o a `equals()` para DTOs e records
