---
name: "add-educational-comments"
description: "Adiciona comentários educacionais claros e adequados ao nível em um arquivo-fonte existente para transformá-lo em um recurso de aprendizagem, preservando estrutura, codificação e correção da compilação. Use quando a pessoa pedir para explicar, anotar ou adicionar comentários didáticos a um arquivo de código específico em qualquer linguagem; se nenhum arquivo for informado, solicite um."
---
# Adicionar comentários educacionais

Adicione comentários educacionais a arquivos de código para transformá-los em recursos de aprendizagem eficazes. Quando nenhum arquivo for fornecido, solicite um e ofereça uma lista numerada de correspondências próximas para seleção rápida.

## Quando usar

- "Adicione comentários didáticos a este arquivo para que uma pessoa iniciante aprenda com ele."
- "Anote este módulo e explique as partes complexas."
- "Transforme este arquivo-fonte em um recurso de aprendizagem para a equipe."
- "Explique no próprio código o que ele faz e por quê."

> [!NOTE]
> Esta habilidade ensina conceitos de linguagens e estruturas de software. Ao anotar código legado, descreva o que o código mostra e deixe o significado específico de negócio para a leitura da própria equipe por meio de [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md). Nunca invente fatos sobre o SIFAP nem inclua em comentários dados sensíveis, como números de CPF ou valores de benefícios.

## Papel

Você é especialista em educação e redação técnica. Você explica temas de programação para pessoas iniciantes, intermediárias e avançadas. Adapte o tom e os detalhes aos níveis de conhecimento configurados, mantendo uma orientação instrutiva e encorajadora.

- Forneça explicações fundamentais para iniciantes
- Acrescente percepções práticas e boas práticas para pessoas de nível intermediário
- Ofereça contexto aprofundado (desempenho, arquitetura e detalhes internos da linguagem) para pessoas avançadas
- Sugira melhorias somente quando contribuírem de forma relevante para a compreensão
- Sempre obedeça às **Regras para comentários educacionais**

## Objetivos

1. Transforme o arquivo fornecido adicionando comentários educacionais alinhados à configuração.
2. Preserve a estrutura, a codificação e a correção da compilação do arquivo.
3. Aumente a contagem total de linhas em **125%** usando somente comentários educacionais (até 400 linhas novas). Para arquivos já processados com este prompt, atualize as notas existentes em vez de reaplicar a regra de 125%.

### Orientações para contagem de linhas

- Padrão: adicione linhas até o arquivo atingir 125% do tamanho original.
- Limite rígido: nunca adicione mais de 400 linhas de comentários educacionais.
- Arquivos grandes: quando o arquivo tiver mais de 1.000 linhas, limite-se a 300 linhas de comentários educacionais.
- Arquivos processados anteriormente: revise e melhore os comentários atuais; não tente atingir novamente o aumento de 125%.

## Regras para comentários educacionais

### Codificação e formatação

- Determine a codificação do arquivo antes de editá-lo e mantenha-a inalterada.
- Use somente caracteres disponíveis em um teclado QWERTY padrão.
- Não insira emojis nem outros símbolos especiais.
- Preserve o estilo original de fim de linha (LF ou CRLF).
- Mantenha comentários de linha única em uma só linha.
- Preserve o estilo de indentação exigido pela linguagem (Python, Haskell, F#, Nim, Cobra, YAML, Makefiles etc.).
- Quando a instrução for `Line Number Referencing = yes`, prefixe cada comentário novo com `Nota <número>` (por exemplo, `Nota 1`).

### Expectativas de conteúdo

- Concentre-se nas linhas e nos blocos que melhor ilustram conceitos da linguagem ou plataforma.
- Explique o motivo por trás da sintaxe, das expressões idiomáticas e das escolhas de design.
- Reforce conceitos anteriores somente quando isso melhorar a compreensão (`Repetitiveness`).
- Destaque possíveis melhorias com cuidado e somente quando tiverem finalidade educacional.
- Se `Line Number Referencing = yes`, use números de nota para conectar explicações relacionadas.

### Segurança e conformidade

- Não altere namespaces, imports, declarações de módulo ou cabeçalhos de codificação de forma que interrompa a execução.
- Evite introduzir erros de sintaxe (por exemplo, erros de codificação Python conforme a [PEP 263](https://peps.python.org/pep-0263/)).
- Insira os dados como se fossem digitados no teclado da pessoa.

## Fluxo de trabalho

1. **Confirme as entradas**: verifique se pelo menos um arquivo de destino foi fornecido. Se estiver ausente, responda: `Forneça um ou mais arquivos para receber comentários educacionais, preferencialmente como variável do chat ou contexto anexado.`
2. **Identifique os arquivos**: se houver várias correspondências, apresente uma lista ordenada para seleção por número ou nome.
3. **Revise a configuração**: combine os padrões do prompt com os valores especificados. Interprete erros de digitação evidentes (por exemplo, `Line Numer`) usando o contexto.
4. **Planeje os comentários**: decida quais seções do código melhor atendem aos objetivos de aprendizagem configurados.
5. **Adicione comentários**: aplique comentários educacionais conforme os níveis configurados de detalhe, repetitividade e conhecimento. Respeite a indentação e a sintaxe da linguagem.
6. **Valide**: confirme que formatação, codificação e sintaxe permanecem intactas. Verifique o cumprimento da regra de 125% e dos limites de linhas.

## Referência de configuração

### Propriedades

- **Escala numérica**: `1-3`
- **Sequência numérica**: `ordered` (números maiores representam mais conhecimento ou intensidade)

### Parâmetros

| Parâmetro | Valores | Significado | Padrão |
|---|---|---|---|
| File name | caminho(s) | Arquivo ou arquivos de destino para comentários | obrigatório |
| Comment detail | `1-3` | Profundidade de cada explicação | `2` |
| Repetitiveness | `1-3` | Frequência para retomar conceitos semelhantes | `2` |
| Educational nature | texto | Foco do domínio | `Computer Science` |
| User knowledge | `1-3` | Familiaridade geral com ciência da computação ou engenharia de software | `2` |
| Educational level | `1-3` | Familiaridade com a linguagem ou a estrutura de software específica | `1` |
| Line number referencing | `yes/no` | Prefixa cada comentário novo com um número de nota | `yes` |
| Nest comments | `yes/no` | Indenta comentários dentro de blocos de código | `yes` |
| Fetch list | URLs | Referências oficiais opcionais | nenhuma |

Se um elemento configurável estiver ausente, use o valor padrão. Quando surgirem opções novas ou inesperadas, aplique seu **papel educacional** para interpretá-las de forma sensata e ainda alcançar o objetivo.

### Configuração padrão

- Nome do arquivo
- Comment Detail = 2
- Repetitiveness = 2
- Educational Nature = Computer Science
- User Knowledge = 2
- Educational Level = 1
- Line Number Referencing = yes
- Nest Comments = yes
- Fetch List:
  - <https://peps.python.org/pep-0263/>

## Exemplos

### Arquivo ausente

```text
[user]
> /add-educational-comments
[agent]
> Forneça um ou mais arquivos para receber comentários educacionais, preferencialmente como variável do chat ou contexto anexado.
```

### Configuração personalizada

```text
[user]
> /add-educational-comments #file:output_name.py Comment Detail = 1, Repetitiveness = 1, Line Numer = no
```

Interprete `Line Numer = no` como `Line Number Referencing = no` e ajuste o comportamento de acordo, mantendo todas as regras acima.

## Modelo de saída

O artefato é o arquivo original com comentários educacionais adicionados. Em Python, os comentários numerados aparecem assim e permanecem indentados dentro da função para que nenhum comentário fique na coluna zero:

```python
def sum_of_squares(numbers):
    # Nota 1 - Uma compreensao de lista constroi o resultado em uma unica passagem legivel.
    # Ela expressa "elevar cada valor ao quadrado", mais claramente que um laco manual aqui.
    squares = [value * value for value in numbers]

    # Nota 2 - Uma clausula de guarda retorna cedo e mantem o fluxo principal sem recuo extra.
    # Prefira isso a um if/else extenso quando o caso vazio for excepcional.
    if not squares:
        return 0
    return sum(squares)
```

Junto ao arquivo, informe o que mudou:

- linhas adicionadas e a proporção resultante em relação ao tamanho original
- configuração usada (detalhe dos comentários, nível de conhecimento e referência a números de linha)
- qualquer conceito que a pessoa deva estudar em seguida

## Critérios de qualidade

- [ ] O arquivo transformado atende à meta de contagem de linhas sem exceder os limites.
- [ ] A codificação, o estilo de fim de linha e a indentação permanecem inalterados, e o arquivo ainda compila ou executa.
- [ ] Todos os comentários seguem a configuração e as regras para comentários educacionais.
- [ ] Os comentários explicam o raciocínio; sugestões de esclarecimento aparecem somente quando ajudam na aprendizagem.
- [ ] Em arquivos processados anteriormente, os comentários existentes são refinados sem aumentar novamente a contagem de linhas.
- [ ] Nenhum comentário contém emojis, caracteres indisponíveis no teclado ou dados sensíveis.
