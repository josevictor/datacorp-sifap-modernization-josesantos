# Portal de documentação SIFAP

Esta aplicação Astro + React publica o repositório completo em inglês, espanhol e português do Brasil. Ela é separada do frontend Next.js da aplicação SIFAP.

## Leia no site ou no GitHub

As edições de idioma são `main` (EN), `espanol` (ES) e `portugues-br` (PT-BR).
O seletor de idiomas persistente do site abre o mesmo documento-fonte em outra edição.
Cada documento Markdown é renderizado na íntegra, incluindo instruções do Copilot, prompts, skills, personas e guias dos estágios.
Cada documento também oferece seu Markdown original completo, download com os bytes preservados e link para o commit imutável de origem.
Os demais arquivos versionados têm visualização de código, prévia de imagem ou download original.

## Execute localmente

Requisitos: Node.js 24, npm, Git e referências remotas locais das três edições.

```bash
git fetch origin
cd site
npm ci
npm run content:status
npm test
npm run build
npm run preview
```

A URL padrão vem de [`repository.json`](repository.json). Para compilar e visualizar na raiz de um endereço local, defina `SITE_URL=http://127.0.0.1:4321/` nos dois comandos.
Nunca copie dados fictícios de prévia para uma publicação de produção.

## Valide

```bash
npm run check
npm test
npm run build
npx playwright install chromium
npm run test:browser
```

A compilação de produção resolve todas as branches de idioma para commits imutáveis. Ela falha se houver edição ou arquivo ausente, Markdown ou prosa sem tradução, código do portal desatualizado, link não resolvido, âncora inválida ou download original alterado.
Mantenha os arquivos que não são Markdown em `site/` idênticos nas três branches ao atualizar o motor compartilhado do portal.
Os relatórios são gerados em `.generated/coverage.json` e `.generated/site-audit.json`.
`npm run content:status` informa cada arquivo ausente ou não traduzido sem gerar um catálogo substituto. O relatório distingue prontidão de uma compilação ou implantação concluída.
Os testes de navegador verificam troca de idioma, acesso ao Markdown integral, busca, layout responsivo, contraste, estado de leitura e movimento reduzido.
Os testes de navegador usam um servidor local novo por padrão. Defina `PLAYWRIGHT_PORT` para outra porta livre quando necessário; `PLAYWRIGHT_REUSE_SERVER=1` exige consentimento explícito e somente local. Use `PORTAL_TEST_URL` para validar um site já publicado.

## Conteúdo e design

- Os documentos-fonte ficam nas branches de idioma; o portal não mantém resumos separados.
- [`src/lib/i18n.ts`](src/lib/i18n.ts) contém traduções da interface, não a documentação do repositório.
- [`src/styles/hub-editorial.css`](src/styles/hub-editorial.css) reutiliza a folha de componentes Hub Editorial fornecida.
- [`src/styles/tokens.css`](src/styles/tokens.css) define tipografia, cores e espaçamento; os estilos do portal preservam o contraste legível nos dois temas.
- Ilhas React fornecem busca, filtros, navegação de estágios e preferências de leitura. O texto dos documentos continua disponível sem JavaScript.
- Fontes e busca são hospedadas localmente. As fontes técnicas originais e as licenças permanecem inalteradas.
- Os avisos originais de distribuição estão em [`public/licenses/`](public/licenses/) e no catálogo de licenças do site.

## GitHub Pages e privacidade

O [workflow do Pages](../.github/workflows/pages.yml) compila as três edições e valida o site antes da implantação.
[`scripts/pages-guard.mjs`](scripts/pages-guard.mjs) consulta a visibilidade real do repositório e do Pages pela API do GitHub.
Um repositório privado é impedido de publicar em Pages público ou com visibilidade não verificada.
A proteção executa antes da compilação, antes da publicação do artefato e imediatamente antes da implantação.
O kit público do time e o kit privado do instrutor nunca devem compartilhar conteúdo gerado.

## Arquitetura e requisitos

- [ADR-0002](../docs/adr/0002-trilingual-documentation-portal.md)
- [REQ-PORTAL-001 a REQ-PORTAL-010](../specs/trilingual-portal.md)
