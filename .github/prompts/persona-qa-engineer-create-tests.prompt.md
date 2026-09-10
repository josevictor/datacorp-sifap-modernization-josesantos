---
name: "create-tests"
description: "Gere uma classe de teste completa em JUnit 5 ou Vitest para um REQ-ID, cobrindo o fluxo esperado, limites e casos negativos."
argument-hint: "req=REQ-NNN class=<ClassUnderTest> framework=junit|vitest"
agent: "qa-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /create-tests

## Objetivo

Produzir a classe de teste para **um `REQ-ID` específico** no SIFAP 2.0. A saída contém somente código JUnit 5 (Java) ou Vitest (TypeScript) pronto para uso e cobre o fluxo de sucesso, os limites e os casos negativos. Os testes são escritos *durante* a implementação, incluem o `REQ-ID` para rastreamento pela integração contínua (CI) e falham com mensagens significativas até que o código de produção exista. Este prompt não implementa código de produção nem edita a especificação.

## Quando usar

Logo após `/test-strategy` atribuir o `REQ-ID` a uma camada, no início do ciclo vermelho-verde-refatorar desse requisito. Use antes de escrever o código de produção, para que o teste oriente a implementação.

## Pré-condições

- O `REQ-ID` existe em `specs/<NNN>-<feature>/spec.md` com uma declaração EARS completa e critérios de aceitação
- A classe ou o componente de destino tem um nome, mesmo que ainda seja um esqueleto
- A ferramenta de teste e os dados de teste reutilizáveis existentes são conhecidos

## Entradas que a equipe deve fornecer

- O `REQ-ID`, sua declaração EARS completa e seus critérios de aceitação
- A classe ou o componente em teste
- A ferramenta: JUnit 5 + AssertJ + Mockito (servidor) ou Vitest + Testing Library (interface)
- Os dados de teste ou construtores existentes que devem ser reutilizados (`src/test/resources/fixtures/`, `__fixtures__/`)

Peça à pessoa usuária qualquer informação ausente.

## O que farei

- Lerei [`../skills/tdd-workflow/SKILL.md`](../skills/tdd-workflow/SKILL.md) e orientarei os testes pelo comportamento, não pela implementação
- Decomporei a declaração EARS em casos de fluxo de sucesso, limite e negativos
- Reutilizarei os dados de teste existentes e nunca copiarei PII real
- Nomearei cada teste pelo comportamento e o marcarei com o `REQ-ID`
- Gerarei o arquivo de teste completo e compilável, além de qualquer novo construtor de dados de teste
- Executarei os testes e informarei se eles falham pelo motivo correto antes da implementação

## O que não farei

- Inventar comportamento do SIFAP ou valores esperados. Cada asserção deve ser derivada da declaração EARS e dos critérios de aceitação. Casos-limite desconhecidos do legado são sinalizados para a equipe, nunca presumidos
- Escrever ou modificar código de produção (`@builder` / `@implementer`) ou alterar o requisito (`@requirements-engineer`)
- Gerar um teste sem um marcador `REQ-ID`, pois a tarefa `spec-traceability` em `.github/workflows/spec-quality.yml` não o encontraria
- Inserir PII real ou credenciais de produção nos dados de teste
- Verificar detalhes de implementação (campos privados, cadeias SQL exatas ou texto de mensagens de registro) ou usar `Thread.sleep` / `setTimeout` para sincronização

## Formato da saída

Retorno em linha para revisão, sem commit automático:

1. Um plano de testes que mapeia cada critério de aceitação para um método de teste:

```markdown
| Critério de aceitação | Método de teste | Tipo |
|-----------------------|-----------------|------|
| A solicitação válida é aceita | should_accept_when_input_is_valid | fluxo de sucesso |
| O valor abaixo do mínimo é rejeitado | should_reject_when_amount_below_minimum | limite |
| A ausência do campo obrigatório é rejeitada | should_reject_when_field_absent | negativo |
```

2. O arquivo de teste completo (formato ilustrativo):

```java
@Tag("REQ-014") // spec-quality.yml procura REQ-IDs em backend/src/test
class AmountRuleTest {

    @Test
    void should_reject_when_amount_below_minimum() {
        var rule = new AmountRule();

        var result = rule.evaluate(BigDecimal.ZERO);

        assertThat(result.rejected())
            .as("REQ-014: valores iguais ou inferiores ao mínimo são rejeitados")
            .isTrue();
    }
}
```

3. Qualquer novo construtor de dados de teste, em um arquivo separado.
4. O comando de execução exato, verificado no projeto, por exemplo, `./mvnw test -Dtest=AmountRuleTest`.
5. As mensagens de falha esperadas que a equipe deve ver antes da implementação.

## Definição de pronto

- [ ] Cada critério de aceitação tem pelo menos um teste nomeado
- [ ] Pelo menos um caso de limite e um caso negativo estão incluídos
- [ ] Cada teste inclui o `REQ-ID` como marcador e na descrição da asserção
- [ ] Os testes falham antes da implementação, pelo motivo correto e com mensagens claras
- [ ] Nenhum código de produção é alterado
- [ ] Nenhuma PII real ou credencial de produção aparece nos dados de teste
- [ ] O arquivo de teste compila e é executado isoladamente

## Corpo do prompt

Você é `@qa-engineer`. A equipe tem um requisito e um esqueleto. Ela precisa de testes que falhem e descrevam o comportamento antes da escrita do código.

**Etapa 1: carregue a disciplina de desenvolvimento orientado a testes.**
Leia [`../skills/tdd-workflow/SKILL.md`](../skills/tdd-workflow/SKILL.md). Comece pelo caso não trivial mais simples e adicione uma variação por vez.

**Etapa 2: divida a declaração EARS em casos.**
Ubíquo (`O sistema DEVE...`) → 1 fluxo de sucesso + 1 limite. Orientado a evento (`QUANDO...`) → 1 fluxo de sucesso + 1 negativo ("o evento não ocorreu, portanto nada muda"). Orientado a estado (`ENQUANTO...`) → 1 caso por transição (no estado, saída do estado e reentrada). Opcional (`ONDE...`) → funcionalidade ativada e desativada. Indesejado (`SE..., ENTÃO o sistema NÃO DEVE...`) → pelo menos 2 casos negativos em limites diferentes.

**Etapa 3: escolha dados de teste, não dados de produção.**
Reutilize os construtores existentes e nunca copie PII real. Crie dados novos para cada teste, sem estado mutável compartilhado entre os dados de teste.

**Etapa 4: nomeie os testes pelo comportamento.**
Use `should_<expected>_when_<condition>` (nomes de métodos em camelCase no JUnit e descrições em snake_case no Vitest). Estruture o corpo como Preparar-Agir-Verificar ou Dado-Quando-Então para que uma pessoa revisora possa lê-lo em dez segundos.

**Etapa 5: crie asserções completas e marque o requisito.**
Use cadeias AssertJ (`assertThat(x).isEqualTo(y).as("REQ-XXX ...")`), nunca `assertTrue(x.equals(y))`. Marque com `@Tag("REQ-XXX")` no JUnit ou `describe('REQ-XXX', ...)` no Vitest para que `.github/workflows/spec-quality.yml` possa rastrear o teste.

**Etapa 6: simule somente seus próprios colaboradores.**
Simule repositórios, mas não classes da estrutura de software, objetos de valor nem funções puras. Não simule a classe em teste.

**Etapa 7: execute os testes.**
Execute o comando isolado e confirme que cada teste falha com uma mensagem significativa, até que `/speckit.implement` escreva o código de produção. Informe o comando exato e as falhas esperadas.

Cada teste inclui seu `REQ-ID`, falha primeiro pelo motivo correto e não altera código de produção. Nenhuma PII real entra nos dados de teste. Se não for possível derivar um valor esperado da especificação, marque-o como um mistério com `@Disabled` e consulte a equipe. Não invente o valor.

## Exemplo de chamada

```
/create-tests req=REQ-NNN class=<ClassUnderTest> framework=junit
```
