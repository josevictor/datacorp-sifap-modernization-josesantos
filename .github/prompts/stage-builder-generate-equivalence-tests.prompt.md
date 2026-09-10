---
name: "generate-equivalence-tests"
description: "Gera testes JUnit que validam se a implementação Java moderna produz as mesmas saídas do programa Natural original para as mesmas entradas."
argument-hint: "class=<java.package>.<Service> method=<method>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /generate-equivalence-tests

## Objetivo

Gerar testes parametrizados JUnit 5 que comprovem que um método Java traduzido produz resultados de negócio equivalentes aos do programa Natural para as mesmas entradas.

## Quando usar

Depois de `/translate-natural-to-java`, para verificar equivalência.

## Pré-condições

- A tradução Java existe e compila
- A origem Natural está em `01-archaeology/legacy-sifap/`
- O Javadoc referencia arquivo e linhas Natural

## Entradas que a equipe deve fornecer

- Classe e método Java
- Caminho do arquivo Natural
- Dados e casos-limite conhecidos na Etapa 1

## O que farei

- Identificarei entradas, saídas e todos os ramos `IF/ELSE`, `DECIDE` e `AT BREAK`
- Gerarei testes para fluxo esperado, ramos, limites, nulos e vazios
- Executarei os testes, informarei resultados e listarei ramos sem cobertura

## O que não farei

- Declarar equivalência sem um teste por ramo
- Omitir limites numéricos ou caminhos de erro
- Inventar valores esperados; todos serão derivados da lógica Natural

## Formato da saída

`src/test/java/.../[ClassName]EquivalenceTest.java`

## Definição de pronto

- [ ] Há um teste por ramo
- [ ] Testes parametrizados cobrem fluxo esperado, ramos, limites, nulos e vazios
- [ ] Os testes compilam e executam
- [ ] Resultados e cobertura de ramos são informados
- [ ] Falhas identificam o ramo divergente

## Corpo do prompt

Você é `@builder`. Gere testes de equivalência para uma tradução Natural–Java.

**Etapa 1 — Localizar a origem.** Leia no Javadoc o arquivo e as linhas Natural e abra-os.

**Etapa 2 — Identificar ramos.** Liste condição, ação ou saída esperada e entradas que acionam cada caminho. Cada `IF...THEN...ELSE` cria dois ou mais caminhos; `DECIDE ON`, N caminhos; `AT BREAK`, um caminho de quebra de controle.

**Etapa 3 — Derivar casos.** Crie pelo menos um caso por ramo:

```java
@ParameterizedTest
@CsvSource({
    "input1, input2, expectedOutput",  // Branch 1: [description]
    "input3, input4, expectedOutput",  // Branch 2: [description]
})
void should_produce_equivalent_output(Type param1, Type param2, Type expected) {
    var service = new ServiceUnderTest(/* dependencies */);
    var result = service.methodUnderTest(param1, param2);
    assertThat(result).isEqualTo(expected);
}
```

Inclua mínimos e máximos, strings vazias ou de um caractere, nulos e precisão `BigDecimal` equivalente ao decimal compactado Natural.

**Etapa 4 — Tratar estado de dados.** Para ramos dependentes de registro, simule respostas para registro existente e ausente.

**Etapa 5 — Executar.** Informe total, aprovados, falhas detalhadas e ramos cobertos sobre o total.

**Etapa 6 — Documentar ramos obscuros.**

```java
@Test
@Disabled("MYSTERY: Branch at [nat-file:L73] — unclear condition; cannot derive expected output")
void should_handle_mystery_branch() {
    fail("Needs team investigation — see MYS-NNN");
}
```

## Exemplo de chamada

```
/generate-equivalence-tests class=<java.package>.<Service> method=<method>
```
