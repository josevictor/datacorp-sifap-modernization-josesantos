---
name: "java-junit"
description: "Escreva testes unitários e parametrizados eficazes com JUnit 5, delegando a lista de boas práticas à skill java-junit."
argument-hint: "class=<ClassUnderTest>"
agent: "qa-engineer"
tools: ["read", "search", "edit"]
---
# /java-junit

## Objetivo

Produzir testes JUnit 5 focados, comuns e parametrizados, para uma classe ou comportamento. Seguir Preparar-Agir-Verificar, nomenclatura descritiva, isolamento adequado e rastreabilidade por REQ-ID. A lista de boas práticas está na habilidade [`java-junit`](../skills/java-junit/SKILL.md). Este prompt a aplica ao backend do SIFAP 2.0 sem repeti-la.

> [!IMPORTANT]
> Escreva os testes junto com o código, nunca depois. O kit proíbe testes adaptados posteriormente.

## Quando usar

Durante as Etapas 3 ou 4, ao implementar lógica de negócio do backend, depois que o comportamento em teste estiver definido por um REQ-ID e por seus critérios de aceitação.

## Pré-condições

- A classe ou o comportamento em teste existe ou está sendo escrito na mesma alteração
- O módulo de backend tem `junit-jupiter` e `testcontainers` no classpath de teste
- Os REQ-IDs que os testes devem cobrir são conhecidos

## Entradas que a equipe deve fornecer

- `class`: a classe ou o comportamento em teste, por exemplo, `PaymentService`
- Os REQ-IDs e critérios de aceitação que os testes devem atender
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Seguirei as práticas de JUnit 5 da skill [`java-junit`](../skills/java-junit/SKILL.md) e as aplicarei à classe em teste
- Escreverei um teste por critério de aceitação, nomeado `should_<expected>_when_<condition>`, cada um com um comentário `// REQ-NNN` no código
- Usarei `@ParameterizedTest` com `@MethodSource` ou `@CsvSource` para casos orientados por dados e Mockito para colaboradores
- Usarei Testcontainers com PostgreSQL 16 real em tudo o que acessar o banco de dados

## O que não farei

- Escrever testes depois do código de produção ou omitir um caso de qualquer critério de aceitação
- Substituir o PostgreSQL do Testcontainers por um banco em memória no caminho de integração
- Testar vários comportamentos em um só método ou depender da ordem de execução
- Deixar um teste sem comentário de REQ-ID, pois isso rompe `spec-traceability`

## Formato da saída

Uma classe de teste JUnit 5 com cada caso rastreável a um REQ-ID:

```java
// REQ-042: reject inactive beneficiary
@Test
@DisplayName("rejects a payment line for an inactive beneficiary")
void should_reject_when_beneficiary_is_inactive() {
    // Arrange - Act - Assert
}
```

## Definição de pronto

- [ ] Existe um teste para cada critério de aceitação de todos os REQ-IDs relacionados
- [ ] Cada teste contém um comentário `// REQ-NNN`
- [ ] Casos orientados por dados usam `@ParameterizedTest`; colaboradores são simulados
- [ ] Testes de banco de dados usam Testcontainers e `./mvnw test` passa

## Corpo do prompt

A skill [`java-junit`](../skills/java-junit/SKILL.md) define as convenções para testes comuns e parametrizados. Leia-a e aplique-as à classe em teste.

**Etapa 1 — Mapear o comportamento.**
Liste cada critério de aceitação dos REQ-IDs relacionados. Cada critério se torna um teste.

**Etapa 2 — Aplicar a skill.**
Escreva os testes conforme a skill: AAA, `@DisplayName`, `assertAll`, `assertThrows` e `@ParameterizedTest`. Simule os colaboradores com Mockito.

**Etapa 3 — Respeitar as regras do kit.**
Use Testcontainers com PostgreSQL 16 nos caminhos de banco de dados, adicione um comentário `// REQ-NNN` a cada teste e execute `./mvnw test`.

**Etapa 4 — Verificar.**
Execute a suíte e confirme que cada caso passa pelo motivo correto.

## Exemplo de chamada

```
/java-junit class=PaymentService
```
