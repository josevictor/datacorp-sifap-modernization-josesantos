---
name: "comment-code-generate-a-tutorial"
description: "Refatore um arquivo-fonte, adicione comentários didáticos para iniciantes e gere um tutorial README, delegando o fluxo de trabalho à skill comment-code-generate-a-tutorial."
argument-hint: "file=<path-to-source>"
agent: "tech-writer"
tools: ["read", "edit", "search"]
---
# /comment-code-generate-a-tutorial

## Objetivo

Transformar um único arquivo-fonte em material didático: refatorá-lo para dar clareza, adicionar comentários instrutivos que expliquem o raciocínio e gerar um tutorial `README.md`. O fluxo completo está na skill [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md). Este prompt o aplica à stack do SIFAP 2.0 sem repeti-lo.

> [!NOTE]
> O exemplo da skill usa Python. Neste kit, aplique-a a Java 21 ou TypeScript e siga o guia de estilo correspondente.

## Quando usar

Durante as Etapas 3 ou 4, ao preparar uma apresentação guiada para a imersão, por exemplo, para explicar um módulo traduzido ao restante da equipe.

## Pré-condições

- O arquivo-fonte de destino existe e executa ou compila
- O público e o conceito a ensinar são conhecidos
- O arquivo não contém dados sensíveis sem mascaramento

## Entradas que a equipe deve fornecer

- `file`: o caminho do arquivo-fonte a documentar
- O público pretendido e o objetivo didático
- Solicite à pessoa usuária qualquer informação ausente.

## O que farei

- Seguirei o procedimento refatorar → comentar → criar tutorial da skill [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md)
- Aplicarei o procedimento às linguagens do kit: Java 21 no backend ou TypeScript com Next.js 15 no frontend
- Adicionarei comentários instrutivos que expliquem intenção e raciocínio, não a sintaxe
- Gerarei um `README.md` com visão geral, configuração, funcionamento e exemplo de uso

## O que não farei

- Aplicar convenções de Python ou PEP 8, a menos que o arquivo seja realmente Python
- Adicionar comentários superficiais que apenas repitam o código
- Incluir dados sensíveis, como CPF e valores de benefícios, em exemplos ou saídas
- Escrever o tutorial em outro idioma que não seja inglês

## Formato da saída

```markdown
### Refatorado
`backend/.../PaymentRules.java` — nomes mais claros e comentários instrutivos adicionados

### Tutorial (README.md)
- Visão geral do projeto
- Instruções de configuração
- Como funciona
- Exemplo de uso
- Exemplo de saída (opcional)
```

## Definição de pronto

- [ ] O código foi refatorado para clareza e segue o guia de estilo da linguagem
- [ ] Os comentários instrutivos explicam o raciocínio sem gerar ruído
- [ ] O `README.md` apresenta visão geral, configuração, funcionamento e exemplo de uso
- [ ] Não há dados sensíveis e todo o texto está em inglês

## Corpo do prompt

A skill [`comment-code-generate-a-tutorial`](../skills/comment-code-generate-a-tutorial/SKILL.md) define o procedimento de refatoração, comentários e tutorial. Leia-a e aplique-a ao arquivo.

**Etapa 1 — Ler e refatorar.**
Compreenda o arquivo e melhore nomes e estrutura conforme as boas práticas da linguagem, Java 21 ou TypeScript.

**Etapa 2 — Aplicar a skill.**
Adicione comentários instrutivos adequados a iniciantes e gere as seções de `README.md` prescritas pela skill.

**Etapa 3 — Respeitar as regras do kit.**
Use o guia de estilo correto para a linguagem, escreva em inglês e mascare dados sensíveis.

**Etapa 4 — Revisar.**
Confirme que os comentários ensinam a intenção e que o tutorial é compreensível de forma independente.

## Exemplo de chamada

```
/comment-code-generate-a-tutorial file=backend/src/main/java/com/sifap/payment/PaymentRules.java
```
