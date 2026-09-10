---
name: "tdd-workflow"
description: "Use ao praticar desenvolvimento orientado a testes, escrever primeiro um teste com falha ou orientar o ciclo vermelho-verde-refatorar. Os gatilhos incluem \"TDD\", \"ciclo vermelho-verde-refatorar\", \"teste primeiro\", \"teste com falha\" e \"escrever um teste\"."
---
# Fluxo de TDD

## Quando invocar

- Ao iniciar um novo comportamento ou uma correção de erro.
- Ao trabalhar em programação em par ou em grupo em código desconhecido e precisar de uma rede de segurança.
- Quando as alterações continuam causando falhas inesperadas.

## O ciclo

```text
VERMELHO → escreva o menor teste com falha que expresse o próximo comportamento
VERDE → escreva a menor quantidade de código que faça o teste passar
REFATORAR → melhore o projeto enquanto os testes permanecem verdes
```

Faça um commit em cada etapa verde. Cubra um comportamento por ciclo.

## Regras

1. **Não escreva código de produção sem um teste com falha.** Sem teste, sem alteração.
2. **Mantenha apenas um teste com falha por vez.** Nunca tenha dois testes vermelhos.
3. **Dê o menor passo que produza falha.** Se o primeiro teste for difícil de escrever, o projeto está indicando um problema.
4. **Os nomes dos testes descrevem o comportamento**, não a implementação: `calculates_tax_for_tax_exempt_customer`, não `test_method1`.
5. Use a estrutura **Dado-Quando-Então / Preparar-Agir-Verificar** no corpo do teste.
6. **A fase de refatoração não é opcional**. Nela está a maior parte do valor.

## Como escolher o próximo teste

Ordene os testes para orientar o projeto:

- Comece pelo caso não trivial mais simples (o caso "0→1" ou o fluxo de sucesso com uma entrada).
- Em seguida, adicione uma única variação (um limite, uma ramificação ou um erro).
- Evite escrever um teste enorme que cubra tudo.

## Objetos falsos e respostas programadas

- Use um substituto de teste apenas quando o colaborador real for lento, não determinístico ou ainda não existir.
- Não crie objetos simulados de tipos que você não controla. Primeiro, envolva-os em uma abstração fina.
- Um teste que simula tudo não testa nada.

## Quando o TDD é difícil, o problema costuma estar no projeto

- Dificuldade para construir o objeto testado → colaboradores demais, violação do princípio de responsabilidade única (SRP).
- Impossibilidade de criar uma asserção sem ler três outros objetos → problema na Lei de Demeter ou no encapsulamento.
- Necessidade de simular o mundo inteiro → acoplamento oculto; introduza uma abstração.

## Antipadrões

- Escrever o código e depois o teste (isso é verificação, não TDD).
- Ignorar a fase de refatoração.
- Testes que duplicam a implementação (detectores de mudança).
- Conjuntos de dados de teste enormes compartilhados entre arquivos, pois são frágeis.
- Verificar detalhes de implementação (métodos privados ou strings SQL exatas).

## Modelo de saída

```java
// REQ-NNN: <comportamento testado>
@Test
void calculatesTaxForTaxExemptCustomer() {
    // Preparar
    var customer = new Customer(TAX_EXEMPT);
    // Agir
    var tax = calculator.taxFor(customer);
    // Verificar
    assertThat(tax).isEqualTo(Money.ZERO);
}
```

Sequência de registros por comportamento: `red: adicionar teste com falha` -> `green: fazer passar` -> `refactor: <melhoria>`.

## Critérios de qualidade

- [ ] Nenhum código de produção foi escrito sem um teste com falha primeiro.
- [ ] Apenas um teste fica vermelho por vez, e cada ciclo cobre um comportamento.
- [ ] A etapa de refatoração foi executada enquanto os testes estavam verdes.
- [ ] Os nomes dos testes descrevem o comportamento e referenciam o REQ-ID em um comentário.

## Referências

- [Kent Beck - Test Driven Development: By Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
- [GOOS - Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)
- [Martin Fowler - Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
