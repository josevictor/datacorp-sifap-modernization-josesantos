---
name: "java-docs"
description: "Aplica práticas recomendadas de Javadoc para documentar corretamente tipos e membros Java: frases de resumo, @param/@return/@throws, blocos {@code}, @since e documentação herdada. Use quando a pessoa solicitar a criação, revisão ou melhoria de Javadoc ou da documentação de API para código Java."
---
# Documentação Java (Javadoc)

Escreva e revise o Javadoc da camada de servidor do SIFAP 2.0 (Java 21 + Spring Boot 3.3) para que cada membro público e protegido tenha um contrato correto e consistente. Esta habilidade define as convenções de Javadoc: ela ensina a documentar o comportamento, não decide o projeto do código e nunca inclui valores regulados reais, como CPF ou valores de benefícios, nos exemplos.

## Quando invocar

- "Escreva o Javadoc desta classe de serviço."
- "Revise o Javadoc deste pacote e corrija o que estiver faltando."
- "Documente a API pública deste módulo antes da publicação."
- "Adicione `@param`/`@return`/`@throws` a estes métodos."

## O que documentar

| Visibilidade | Regra |
|---|---|
| `public`, `protected` | O Javadoc é obrigatório, pois esses membros formam o contrato da API |
| package-private (acesso restrito ao pacote) | Documente quando a intenção não estiver evidente no nome |
| `private` | Documente apenas lógicas realmente complexas; prefira código claro a comentários |

> [!NOTE]
> Documente o contrato, ou seja, aquilo em que a parte chamadora pode confiar, e não a implementação. Nunca inclua CPF, valor de benefício, token ou outro dado sensível real em um exemplo de Javadoc. Use marcadores claramente fictícios.

## Frase de resumo

- A primeira frase é o resumo. Ela termina com ponto e deve ser uma frase verbal curta ("Retorna...", "Registra...").
- Inicie resumos de métodos com um verbo na terceira pessoa ("Calcula o imposto..."), não com "Este método...".
- Concentre o resumo no contrato e mova os detalhes para os parágrafos seguintes.

## Tags de bloco

| Tag | Quando usar | Regra de formato |
|---|---|---|
| `@param name` | Cada parâmetro de método ou construtor | A descrição começa com letra minúscula e não termina com ponto |
| `@param <T>` | Cada parâmetro de tipo de um tipo ou método genérico | A mesma regra de letra minúscula e ausência de ponto |
| `@return` | Cada método que retorna um valor (omita em `void`) | Descreva o valor, inclusive a semântica de `Optional` |
| `@throws` / `@exception` | Cada exceção verificada e cada exceção não verificada documentada | Informe a condição que a dispara |
| `@see` | Referências cruzadas a tipos ou membros relacionados | Crie um link, sem repetir o conteúdo |
| `@since` | Quando o membro foi introduzido | Use a versão do projeto ou módulo |
| `@deprecated` | Um membro programado para remoção | Indique o substituto e adicione `@Deprecated` ao código |

Opcional: inclua `@author` e `@version` somente se a convenção da equipe exigir. Muitos guias de estilo omitem `@author` e preferem o histórico do controle de versão.

> [!WARNING]
> Ordene as tags: `@param` (na ordem de declaração), seguida de `@return` e `@throws`. Um `@param` ausente ou fora de ordem é o defeito mais comum em revisões de Javadoc.

## Tags no corpo do texto e código

- Use `{@code ...}` para identificadores, palavras-chave e literais no corpo do texto (`{@code null}`, `{@code Optional.empty()}`).
- Use `{@link Type#member}` para criar um link para outro elemento e `{@linkplain ...}` quando quiser texto de link simples.
- Use `<pre>{@code ... }</pre>` para exemplos com várias linhas, de modo que genéricos e sinais de maior e menor sejam renderizados literalmente.
- Use `{@inheritDoc}` para herdar o contrato de um supertipo, mas documente novamente qualquer comportamento realmente diferente.

## Como documentar records do Java 21

O Javadoc de um record fica no tipo. Documente cada componente com `@param`. Não adicione métodos de acesso apenas para anexar Javadoc a eles.

## Modelo de saída

```java
/**
 * Registra um recurso de pagamento e retorna sua representação armazenada.
 *
 * <p>O rótulo deve ser único; uma duplicata é rejeitada, não mesclada.
 *
 * @param request a solicitação de criação validada; não pode ser {@code null}
 * @return o recurso persistido como DTO de resposta
 * @throws ResourceConflictException se já existir um recurso com o mesmo rótulo
 * @since 1.0.0
 * @see ResourceService#getById(java.util.UUID)
 */
ResourceResponse create(CreateResourceRequest request);

/**
 * Solicitação de criação imutável para um recurso de pagamento.
 *
 * @param label  um rótulo único e legível (máximo de 120 caracteres)
 * @param amount o valor monetário positivo a registrar
 */
public record CreateResourceRequest(String label, BigDecimal amount) {}
```

## Critérios de qualidade

- [ ] Cada membro público e protegido tem uma frase de resumo no Javadoc terminada por ponto.
- [ ] Cada parâmetro, inclusive parâmetros de tipo `<T>`, tem um `@param`; cada método que não seja `void` tem um `@return`.
- [ ] Cada exceção documentada tem um `@throws` que descreve a condição que a dispara.
- [ ] `{@code}` e `{@link}` envolvem identificadores em vez de texto simples, e as tags de bloco estão na ordem correta.
- [ ] Nenhum exemplo contém CPF, valor de benefício ou outro dado sensível real.
- [ ] `mvn javadoc:javadoc` (ou a tarefa `javadoc` do Gradle) é gerado sem avisos.
