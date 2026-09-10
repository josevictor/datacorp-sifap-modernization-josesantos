---
name: "comment-code-generate-a-tutorial"
description: "Refatore um script Python conforme a PEP 8, adicione comentários didáticos para iniciantes e gere um tutorial README.md completo (visão geral, configuração, funcionamento e exemplo de uso). Use quando a pessoa quiser transformar um script Python em um projeto aprimorado e didático ou produzir um guia passo a passo."
---
# Comentar o código e gerar um tutorial

Use esta habilidade para transformar um script funcional em um artefato didático. Refatore o código para melhorar a clareza, adicione comentários instrutivos que expliquem o raciocínio por trás de cada decisão e escreva um tutorial `README.md` que permita a iniciantes executar o script e entender seu funcionamento. O exemplo usa Python, mas o mesmo procedimento de três etapas se aplica a qualquer linguagem.

> [!NOTE]
> Nesta imersão, o prompt (instrução) [`/comment-code-generate-a-tutorial`](../../prompts/comment-code-generate-a-tutorial.prompt.md) aplica este procedimento ao conjunto de tecnologias Java 21 e TypeScript do kit. Mantenha esta habilidade como a fonte procedural oficial à qual o prompt recorre.

## Quando usar

- "Refatore este script Python e escreva um tutorial README para ele."
- "Adicione comentários para iniciantes a este script e explique como ele funciona."
- "Transforme este utilitário em um projeto didático com documentação de configuração e uso."
- "Gere um guia passo a passo para este script."

## Fluxo de trabalho

### 1. Refatorar para melhorar a clareza

- Aplique o guia de estilo da linguagem (PEP 8 para Python).
- Renomeie variáveis e funções pouco claras para que os nomes revelem a intenção.
- Extraia blocos longos em funções pequenas e nomeadas.
- Mantenha a interface pública e a saída observável idênticas. Esta etapa melhora a legibilidade, não reescreve o programa.

### 2. Adicionar comentários instrutivos

Explique o raciocínio, não a sintaxe. Um comentário útil responde "por quê"; um comentário ruim repete "o quê".

| Escreva comentários que | Evite comentários que |
|---|---|
| Expliquem por que uma decisão de design foi tomada | Repitam uma linha, como `i += 1  # soma um` |
| Apresentem um idioma da linguagem na primeira ocorrência | Repitam o nome da função em prosa |
| Alertem sobre um caso extremo ou uma invariante | Narrem um fluxo de controle óbvio |
| Nomeiem o conceito que uma pessoa iniciante deve pesquisar | Adicionem ruído que se torna obsoleto |

### 3. Gerar o tutorial

Escreva um `README.md` ao lado do script com estas seções: visão geral do projeto, instruções de configuração, funcionamento, exemplo de uso e, opcionalmente, uma saída de exemplo.

## Regras

- Preserve o comportamento, a codificação do arquivo e o estilo de fim de linha. Uma revisão didática nunca deve quebrar a compilação.
- Use apenas caracteres padrão do teclado em código e comentários. Não use emojis.
- Escreva todos os comentários e todas as seções do tutorial em português do Brasil.
- Nunca inclua dados sensíveis (por exemplo, números de CPF ou valores de benefícios) em exemplos ou saídas de exemplo.
- Execute o comando de configuração e o exemplo antes de publicar o tutorial.

## Modelo de saída

O `README.md` gerado começa com um H1 que nomeia o projeto, seguido destas seções:

```markdown
## Visão geral do projeto
`wordcount.py` conta quantas vezes cada palavra aparece em um arquivo de texto e
exibe as entradas mais frequentes. Ele demonstra leitura de arquivo, agregação
com dicionários e ordenação em Python.

## Configuração
- Requer Python 3.8 ou mais recente
- Não tem dependências de terceiros

Execute a partir da raiz do projeto:

    python3 wordcount.py sample.txt --top 10

## Como funciona
1. Leia o arquivo e converta cada linha em minúsculas para ignorar diferenças entre maiúsculas e minúsculas.
2. Divida cada linha nos espaços em branco e conte as palavras em um dicionário.
3. Ordene o dicionário pela contagem e exiba as N primeiras entradas.

## Exemplo de uso
    python3 wordcount.py article.txt --top 5

## Saída de exemplo
    the      42
    and      31
    data     27
```

## Critérios de qualidade

- [ ] O script ainda funciona e produz uma saída idêntica após a refatoração.
- [ ] Os nomes revelam a intenção e nenhum comportamento mudou durante a melhoria de legibilidade.
- [ ] Os comentários explicam raciocínios e idiomas da linguagem, não sintaxe óbvia.
- [ ] O `README.md` inclui visão geral, configuração, funcionamento e exemplo de uso.
- [ ] O comando de configuração e o exemplo foram testados e estão corretos.
- [ ] Tudo está escrito em português do Brasil, sem emojis nem dados sensíveis.
