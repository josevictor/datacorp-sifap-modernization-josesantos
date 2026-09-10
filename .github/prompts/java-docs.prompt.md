---
name: "java-docs"
description: "Aplique boas práticas de Javadoc a tipos e membros Java, delegando a lista de verificação completa à skill java-docs."
argument-hint: "target=<file-or-package>"
agent: "tech-writer"
tools: ["read", "edit", "search"]
---
# /java-docs

## Objetivo

Adequar o Javadoc de um arquivo ou pacote Java ao padrão do projeto: frases de resumo, `@param`, `@return`, `@throws`, genéricos e blocos `{@code}`. Assim, membros públicos e protegidos ficam documentados de modo correto e consistente. A lista detalhada está na skill [`java-docs`](../skills/java-docs/SKILL.md). Este prompt a aplica ao backend do SIFAP 2.0 sem repeti-la.

> [!NOTE]
> Documente o motivo, não o conteúdo: a frase de resumo declara a intenção e não repete a assinatura do método.

## Quando usar

Durante as Etapas 3 ou 4, ao implementar ou revisar Java no backend, depois que a classe ou o pacote compilar e sua interface pública estiver estável o suficiente para documentação.

## Pré-condições

- O arquivo ou pacote `.java` de destino existe e compila
- A interface pública e protegida a documentar foi identificada
- O código segue as convenções de Java 21 em [`backend.instructions.md`](../instructions/backend.instructions.md)

## Entradas que a equipe deve fornecer

- `target`: o arquivo ou pacote a documentar, por exemplo, `backend/src/main/java/com/sifap/payment`
- Termos de domínio que esclareçam a intenção da frase de resumo
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Aplicarei as convenções de Javadoc da skill [`java-docs`](../skills/java-docs/SKILL.md) a todos os membros públicos e protegidos do destino
- Escreverei uma frase de resumo concisa para cada membro e documentarei parâmetros, retornos, exceções lançadas e parâmetros de tipo
- Usarei `{@inheritDoc}` quando o comportamento não mudar e documentarei a diferença quando houver mudança
- Manterei o comportamento compilado inalterado; modificarei somente a documentação

## O que não farei

- Adicionar comentários desnecessários que repitam a assinatura ou o óbvio
- Alterar corpos, assinaturas ou visibilidade de métodos para facilitar a documentação
- Incluir dados sensíveis, como CPF e valores de benefícios, em exemplos `{@code}`; farei o mascaramento
- Escrever Javadoc em outro idioma que não seja inglês

## Formato da saída

Os arquivos de destino com Javadoc adicionado no próprio local, além de um breve resumo:

```markdown
### Documentado
| Membro | Javadoc adicionado |
|---|---|
| `PaymentService#approve(PaymentId)` | resumo, `@param`, `@return`, `@throws` |

### Ignorado
- `PaymentService#toString()` — autoexplicativo; não precisa de Javadoc.
```

## Definição de pronto

- [ ] Cada membro público e protegido tem uma frase de resumo terminada em ponto
- [ ] `@param`, `@return`, `@throws` e `@param <T>` estão presentes quando aplicáveis
- [ ] Nenhum exemplo contém dados sensíveis
- [ ] Todo o Javadoc está em inglês e o arquivo continua compilando

## Corpo do prompt

A skill [`java-docs`](../skills/java-docs/SKILL.md) define todas as convenções de Javadoc. Leia-a e aplique-a ao destino.

**Etapa 1 — Localizar a interface.**
Abra `target` e liste todos os tipos e membros públicos e protegidos sem Javadoc correto.

**Etapa 2 — Aplicar a skill.**
Documente cada membro conforme a skill: primeiro uma frase de resumo; depois `@param` em minúsculas e sem ponto final, `@return`, `@throws`, `@param <T>` e `{@code}` ou `<pre>{@code ...}</pre>` quando forem úteis.

**Etapa 3 — Respeitar as regras do kit.**
Mantenha o comportamento inalterado, escreva em inglês e mascare CPF e valores de benefícios nos exemplos.

**Etapa 4 — Relatar.**
Resuma o que foi documentado e o que foi deliberadamente ignorado.

## Exemplo de chamada

```
/java-docs target=backend/src/main/java/com/sifap/payment
```
