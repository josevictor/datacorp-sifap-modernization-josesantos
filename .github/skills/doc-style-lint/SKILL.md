---
name: "doc-style-lint"
description: "Use ao revisar documentação quanto a estilo, clareza, linguagem inclusiva ou conformidade com os guias de estilo da Microsoft ou do Google. Os gatilhos incluem \"revisão de documentação\", \"guia de estilo\", \"linguagem simples\", \"linguagem inclusiva\" e \"legibilidade\"."
---
# Verificação de estilo da documentação

## Quando usar

- "Verifique este README conforme nosso guia de estilo."
- "Reescreva esta documentação de API em linguagem simples."
- "Procure termos excludentes e jargões."

## Regras

### Voz e tom

- **Voz ativa**. Use "O sistema armazena o arquivo", não "O arquivo é armazenado pelo sistema".
- **Tempo presente**. Use "Retorna uma resposta JSON", não "Retornará uma resposta JSON".
- **Segunda pessoa** ("você") em guias práticos; **terceira pessoa** em documentação de referência.
- **Títulos com apenas a primeira palavra em maiúscula**, não todas as palavras principais.

### Clareza

- Uma ideia por frase.
- Use 25 palavras por frase como máximo prático.
- Use no máximo cinco frases por parágrafo.
- Evite palavras que minimizam a dificuldade ("apenas", "simplesmente", "facilmente"). Elas induzem quem lê ao erro.
- Não use travessões. Use vírgulas, parênteses ou dois-pontos.

### Linguagem inclusiva

Substitua:

- `master/slave` -> "primário/réplica" ou "líder/seguidor"
- `whitelist/blacklist` -> "lista de permissões/lista de bloqueios"
- `guys` -> "pessoal", "todas as pessoas", "equipe"
- `crazy/insane` (como intensificadores) -> "significativo", "incomum"
- `dummy` (em nomes de variáveis) -> `example`, `sample`
- `sanity check` -> "verificação rápida", "verificação"

### Estrutura

- **Comece pelo resultado**, não pelo contexto. Quem lê deve saber por que continuar.
- **Informe no início o que será aprendido**.
- **Resuma no final** de documentos longos.
- **Use títulos descritivos** para facilitar a leitura rápida.

### Hiperlinks

- O texto do hiperlink descreve o destino. Nunca use "clique aqui" nem "este hiperlink".
- Use URLs absolutas para fontes externas e URLs relativas para conteúdo interno.
- Verifique os hiperlinks na integração contínua (CI).

### Exemplos de código

- Teste todos os trechos executáveis.
- Use exemplos realistas, não `foo/bar/baz`.
- Identifique claramente os marcadores de posição: `<YOUR-API-KEY>`.

### Números e unidades

- Use algarismos para 10 ou mais e palavras de zero a nove (estilo Microsoft).
- Use unidades métricas e inclua conversões para públicos mistos.
- Sempre especifique a unidade: "100 MB", não "100".

## Etapas da revisão

1. **Leia uma vez como o público-alvo**. O tamanho e o nível de detalhe estão adequados?
2. **Execute as verificações automatizadas configuradas no repositório**, como Vale, Alex.js ou markdownlint. Informe ferramentas ausentes sem instalá-las.
3. **Aplique as regras de estilo** seção por seção.
4. **Teste todos os exemplos de código**.
5. **Pergunte**: uma pessoa recém-contratada entenderia isto no primeiro dia?

## Antipadrões

- Revisar sem executar primeiro os verificadores automatizados.
- Priorizar o estilo em detrimento do conteúdo.
- Reescrever a voz de quem escreveu em vez de refiná-la.
- Ignorar a acessibilidade (texto alternativo, níveis de títulos e texto de hiperlinks).

## Modelo de saída

```markdown
## Revisão de estilo: <Documento>

### Resumo
- Legibilidade (nível Flesch-Kincaid): 11 (meta: <=12)
- Voz passiva: 8% (meta: <10%)
- Problemas de linguagem inclusiva: 2
- Hiperlinks quebrados: 0
- Exemplos de código não testados: 3

### Recomendações (10 principais)
| ID | Local | Problema | Correção |
|----|----------|-------|-----|
| 01 | Seção de instalação | Voz passiva | Reescrever na voz ativa |
| 02 | Solução de problemas | "os caras" | Substituir por "a equipe" |
| 03 | Referência da API | "basta chamar" | Remover "basta" |
```

## Critérios de qualidade

- [ ] O documento passa nos verificadores configurados no repositório (por exemplo, Vale, Alex.js e markdownlint) antes da revisão humana.
- [ ] O texto usa voz ativa e tempo presente, com apenas a primeira palavra dos títulos em maiúscula.
- [ ] Nenhum termo excludente permanece; os termos sinalizados foram substituídos por alternativas inclusivas.
- [ ] Todos os exemplos de código foram testados e todos os hiperlinks funcionam.
