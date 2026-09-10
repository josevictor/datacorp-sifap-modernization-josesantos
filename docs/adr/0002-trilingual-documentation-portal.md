# ADR-0002: Publicar um portal de documentação trilíngue e interativo com Astro

> **Trilha:** [Kit do time](../../README.md) > [Documentação](../README.md) > [ADRs](README.md)

| Campo | Valor |
|---|---|
| Status | accepted |
| Data | 2026-09-07 |
| Escopo | Distribuição da documentação, não o frontend da aplicação SIFAP |
| Origem da decisão | Solicitação de edições completas EN, ES e PT-BR do repositório e GitHub Pages |

## Contexto

As pessoas precisam seguir o mesmo material pelo GitHub ou por um site acessível.
O portal deve expor cada arquivo versionado, não um subconjunto selecionado manualmente.
As edições em inglês, espanhol e português do Brasil usam `main`, `espanol` e `portugues-br`.
O desenvolvimento da aplicação continua seguindo a arquitetura existente Java 21 e Next.js 15.

A referência visual é o [Agentic DevOps Hub](https://agenticdevopsplatform.ai/en/).
Seu design medido usa superfícies em branco quente, uma área de destaque escura, tipografia Inter, rótulos monoespaçados, linhas finas e quatro cores de destaque.
A implementação usa layout e ilustrações próprios do SIFAP, não a marca, fotografia ou texto do site de referência.

## Decisão

Criar uma aplicação Astro separada em `site/`, com geração estática e ilhas React 19 focadas nas interações do navegador, conforme solicitado explicitamente.
O GitHub Pages serve arquivos estáticos; busca, filtros, seleção de tema, progresso de leitura e animações continuam interativos no navegador.
O seletor de idiomas permanece visível no desktop e no celular e leva ao mesmo documento lógico.

Na compilação, resolver as três branches Git para commits imutáveis e inventariar seus arquivos versionados.
Renderizar Markdown como documentação sanitizada, oferecer visualização de código e downloads originais para outros arquivos e preservar os bytes das fontes técnicas.
Registrar caminhos de origem, IDs dos commits e cobertura no catálogo gerado.
Compilações de produção rejeitam edições de idioma ausentes, documentos ausentes e rotas internas quebradas, em vez de substituir silenciosamente por inglês.

Usar implantações separadas para repositórios públicos e privados.
Um repositório privado só pode implantar após a API do GitHub Pages confirmar `public: false`.
Verificar isso antes de publicar artefatos no Pages e novamente imediatamente antes da implantação.
Uma configuração de privacidade indisponível ou ambígua interrompe a publicação; nunca habilita acesso público como alternativa.

## Justificativa das dependências

| Dependência | Finalidade |
|---|---|
| Astro | Rotas estáticas e templates de componentes tipados sem exigir um framework cliente |
| `@astrojs/react`, React 19, React DOM e seus tipos | Busca, filtros, tema e controles de leitura hidratados, mantendo a documentação renderizada no servidor |
| `@storybook/icons` | Ícones de contorno fornecidos com a referência Hub Editorial, sem adotar a marca Storybook |
| `@astrojs/markdown-remark` | Renderização Markdown compatível com Astro, blocos de código e metadados de títulos |
| `rehype-raw`, `rehype-sanitize` | Preservar HTML suportado pelo Markdown, removendo marcação executável ou insegura |
| Mermaid | Renderizar os diagramas já presentes no repositório, com configurações estritas de segurança |
| Pagefind | Busca local por idioma sem serviço externo de indexação |
| `@fontsource-variable/inter`, `@fontsource-variable/jetbrains-mono` | Fontes auto-hospedadas com licença aberta que correspondem à tipografia de referência |
| `@astrojs/check`, TypeScript 5 e tipos do Node.js | Validação estrita de templates e TypeScript |
| Runner de testes integrado do Node.js | Testar ingestão Git, caminhos, cobertura de idiomas e proteções de implantação sem outro framework de testes |
| Playwright | Verificar no navegador o site responsivo e interativo, a navegação de idioma, a busca e o contraste |
| `parse5` | Auditar nós HTML reais sem confundir exemplos escapados de Markdown/código com links ou IDs ativos |

Fixar as versões resolvidas no lockfile.
Usar Node.js 24 para o portal; não alterar os requisitos de runtime da aplicação.
Os dicionários de localização da interface são recursos da aplicação, não documentação traduzida duplicada na `main`.

## Alternativas consideradas

| Alternativa | Motivo para não selecionar |
|---|---|
| Markdown renderizado somente pelo GitHub | Não oferece o design solicitado, o catálogo completo, a busca ou a leitura interativa |
| Exportação estática do Next.js | É viável, mas se sobrepõe ao frontend separado da aplicação SIFAP; Astro limita a hidratação às ilhas interativas |
| Cópia incorporada do site de referência | Copiaria marca e conteúdo não relacionados e não resolveria a cobertura baseada em Git |
| Serviços externos de tradução ou busca | Adicionariam serviços recorrentes e poderiam expor material privado do instrutor |

## Consequências

- Cada documento-fonte permanece versionado na branch de idioma e utilizável sem o site.
- O mesmo mecanismo atende aos dois públicos sem misturar conteúdo.
- O GitHub Pages exige workflow explícito e URL-base correta, incluindo o hostname separado do Pages privado.
- Traduções e compatibilidade de âncoras são critérios de publicação, não alternativas silenciosas.
- As interações respeitam teclado, telas pequenas e preferência por movimento reduzido.

## Requisitos relacionados

Consulte os [requisitos do portal](../../specs/trilingual-portal.md).

## Referências

- [Documentação do Astro](https://docs.astro.build/en/getting-started/)
- [Controle de acesso do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site)
- [Workflows personalizados do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Referência visual](https://agenticdevopsplatform.ai/en/)
