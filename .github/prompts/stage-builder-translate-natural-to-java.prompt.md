---
name: "translate-natural-to-java"
description: "Traduz um programa Natural para Java 21 + Spring Boot 3.3 idiomático, preservando a semântica de negócio."
argument-hint: "file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN context=<context> package=<java.package>"
agent: "builder"
tools: ["read", "search", "edit", "execute"]
---
# /translate-natural-to-java

## Objetivo

Traduzir Natural para Java 21 + Spring Boot 3.3 idiomático, preservando semântica, com compilação e Javadoc rastreável.

## Quando usar

No início da Etapa 3, ao implementar contextos da Etapa 2.

## Pré-condições

- `plan.md` e `spec.md` existem
- Contexto, pacote, origem Natural e REQ-IDs são conhecidos

## Entradas que a equipe deve fornecer

- Caminho Natural, contexto, pacote e REQ-IDs

## O que farei

- Lerei por blocos, identificarei finalidade, traduzirei com recursos do Java 21, gerarei Javadoc e stubs de teste
- Sinalizarei lógica órfã sem REQ-ID

## O que não farei

- Fazer port linha a linha (“JOBOL”), combinar conceitos silenciosamente, inventar significado ou ignorar EARS

## Formato da saída

Arquivos em `src/main/java/` e stubs em `src/test/java/`, com Javadoc da origem.

## Definição de pronto

- [ ] Compila
- [ ] Métodos públicos citam arquivo e linhas Natural
- [ ] Cada regra EARS tem método
- [ ] Órfãos usam `// ORPHAN: [file:line] - Team decision required`
- [ ] Há stub por método e uso idiomático de Java 21

## Corpo do prompt

Você é `@builder`. Traduza o programa selecionado.

**Etapa 1 — Ler EARS.** Leia `spec.md` e liste requisitos pertinentes.

**Etapa 2 — Ler Natural.** Analise `DEFINE DATA`, decisões `IF`, acessos `READ`/`FIND`, dependências `CALLNAT` e subrotinas `PERFORM`.

**Etapa 3 — Relacionar blocos.** Associe cada bloco a um REQ-ID. Para órfãos:

```java
// ORPHAN: [natural-file.NSN:L42-58] - No matching REQ. Team decision required: keep, modify, or remove?
```

Consulte a equipe antes de prosseguir.

**Etapa 4 — Traduzir.** Mapeie variáveis para tipos Java; condições para `if/else` ou `switch`; `READ LOGICAL BY` para `findBy*`; `FIND WITH` para `@Query` nomeada; `CALLNAT` para serviço injetado; decimais para `BigDecimal` com escala e arredondamento; strings com atenção ao charset. Use records, sealed interfaces, `Optional`, injeção por construtor, `@Valid` e `@Transactional` somente em serviços.

**Etapa 5 — Gerar Javadoc.**

```java
/**
 * [Business description].
 *
 * <p>Translated from: {@code [natural-file.NSN#L42-L58]}</p>
 * <p>Implements: REQ-NNN</p>
 */
```

**Etapa 6 — Criar stubs.**

```java
@Test
void should_[expected]_when_[condition]() {
    // Arrange: [describe the setup based on the Natural input parameters]
    // Act: [call the translated method]
    // Assert: [verify against the EARS acceptance criteria]
    fail("TODO: implement — see REQ-NNN acceptance criteria");
}
```

**Etapa 7 — Compilar.** Corrija erros. Se não houver equivalente limpo, apresente duas alternativas e deixe a equipe escolher.

## Exemplo de chamada

```
/translate-natural-to-java file=01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSN context=<context> package=<java.package>
```
