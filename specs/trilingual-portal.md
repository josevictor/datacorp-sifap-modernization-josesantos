# Portal de documentação trilíngue

Esta é uma nova superfície de distribuição do kit, não uma alteração no comportamento de negócio do SIFAP.

## Requisitos

### REQ-PORTAL-001: Cobertura completa do repositório

QUANDO uma compilação de produção resolver as branches de idioma, o portal DEVE inventariar cada arquivo versionado e fornecer um documento, visualização de código ou download original para cada arquivo.
source_legacy: "[GREENFIELD] O portal de distribuição do repositório não existe na aplicação Natural/Adabas."

### REQ-PORTAL-002: Três edições completas de idioma

O portal DEVE fornecer rotas em inglês, espanhol e português do Brasil baseadas em `main`, `espanol` e `portugues-br`, sem substituir silenciosamente documentação traduzida ausente por inglês.
source_legacy: "[GREENFIELD] A distribuição de documentação trilíngue é uma nova capacidade do kit."

### REQ-PORTAL-003: Navegação persistente entre idiomas

QUANDO uma pessoa alterar o idioma de um documento, o portal DEVE abrir o mesmo caminho lógico de origem na edição selecionada.
source_legacy: "[GREENFIELD] A navegação de idiomas do site não tem equivalente legado."

### REQ-PORTAL-004: Links corretos e proveniência da fonte

QUANDO o portal renderizar um link do repositório, ele DEVE resolver o documento ou recurso correspondente no site e manter um link explícito para a fonte Git original e seu commit.
source_legacy: "[GREENFIELD] O roteamento web e a proveniência da fonte pertencem ao novo portal."

### REQ-PORTAL-005: Descoberta interativa

QUANDO uma pessoa buscar ou filtrar o catálogo, o portal DEVE mostrar o conteúdo correspondente no idioma ativo e anunciar de forma acessível os estados de carregamento, vazio e erro.
source_legacy: "[GREENFIELD] A busca de documentação no navegador é uma nova capacidade."

### REQ-PORTAL-006: Interface responsiva e acessível

ENQUANTO a janela for estreita, o portal DEVE manter a navegação de idiomas visível e os controles acessíveis pelo teclado sem transbordamento horizontal da página.
source_legacy: "[GREENFIELD] A navegação web responsiva é independente do comportamento da aplicação legada."

### REQ-PORTAL-007: Movimento e preferências

QUANDO uma pessoa selecionar um tema, marcar progresso de leitura ou solicitar movimento reduzido, o portal DEVE aplicar a preferência sem ocultar conteúdo obrigatório nem alterar dados do repositório.
source_legacy: "[GREENFIELD] Preferências locais de leitura e controles de animação são novos comportamentos do portal."

### REQ-PORTAL-008: Preservar fontes técnicas

O portal DEVE preservar os bytes originais dos arquivos para download, renderizar código como texto não executável e evitar atravessar links simbólicos Git para fora do repositório.
source_legacy: "[GREENFIELD] A distribuição segura de arquivos-fonte é uma nova preocupação de publicação do repositório."

### REQ-PORTAL-009: Proteger o conteúdo privado do instrutor

SE o repositório de origem for privado e a visibilidade do Pages for pública ou desconhecida, ENTÃO a implantação DEVE parar antes de publicar seu conteúdo.
source_legacy: "[GREENFIELD] O controle de acesso do Pages privado protege material do instrutor fora do sistema legado."

### REQ-PORTAL-010: Validação reproduzível da publicação

QUANDO uma versão for compilada, o portal DEVE registrar IDs dos commits de origem, cobertura de idiomas e resultados de validação de links internos e DEVE falhar se alguma verificação obrigatória falhar.
source_legacy: "[GREENFIELD] A validação reproduzível de publicação da documentação é um novo requisito do kit."
