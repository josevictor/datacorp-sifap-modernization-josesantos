import type { Category, Locale } from "./model";

interface Messages {
  kit: string; privateKit: string; privateNotice: string; skip: string;
  home: string; journey: string; library: string; personas: string; repository: string;
  language: string; menu: string; search: string; searchHint: string; close: string;
  loading: string; noResults: string; searchError: string; searchPrompt: string;
  dark: string; light: string; preferencesError: string; all: string;
  category: string; kind: string; document: string; source: string; image: string; binary: string;
  filter: string; clear: string; results: string; showMore: string; files: string;
  heroEyebrow: string; heroTitle: string; heroLead: string; start: string; explore: string;
  stages: string; languages: string; years: string;
  terminalLabel: string; terminalCaption: string; terminalTitle: string;
  terminalSearchType: string; terminalReady: string; terminalSubmit: string;
  terminalExit: string; terminalSimulation: string; terminalEmpty: string; terminalNotice: string;
  journeyLabel: string; journeyTitle: string; journeyLead: string;
  libraryLabel: string; libraryTitle: string; libraryLead: string;
  personasLabel: string; personasTitle: string; personasLead: string;
  sourceLabel: string; sourceTitle: string; sourceLead: string; sourceCommit: string;
  footerTitle: string; footerLead: string; top: string; generated: string;
  contents: string; navigation: string; original: string; download: string; copy: string;
  copied: string; copyError: string; markRead: string; markedRead: string;
  reading: string; minutes: string; diagramError: string; viewSource: string;
  technicalNote: string; bytes: string; allFiles: string; builtWith: string;
  markdownSource: string;
  filterPlaceholder: string;
  licenses: string;
}

const messages: Record<Locale, Messages> = {
  en: {
    kit: "Team kit", privateKit: "Instructor kit", privateNotice: "Private · authorized instructors only",
    skip: "Skip to content", home: "Home", journey: "Learning path", library: "Library",
    personas: "Personas", repository: "Repository", language: "Language", menu: "Menu",
    search: "Search", searchHint: "Search the complete kit", close: "Close",
    loading: "Searching…", noResults: "No matching content. Try another term or clear the filters.",
    searchError: "Search could not be loaded. You can still browse the complete library.",
    searchPrompt: "Search instructions, concepts, source files and guides.",
    dark: "Dark theme", light: "Light theme", preferencesError: "This browser could not save your preference.",
    all: "All", category: "Category", kind: "File type", document: "Document", source: "Source",
    image: "Image", binary: "Download", filter: "Filter by title or path", clear: "Clear filters",
    results: "results", showMore: "Show more", files: "Files", heroEyebrow: "SIFAP / Legacy modernization",
    heroTitle: "Understand the past.\nBuild what comes next.",
    heroLead: "A complete field guide to modernizing Natural and Adabas with Java, Next.js and GitHub Copilot. Read, discover and follow the same instructions here or in the repository.",
    start: "Start the journey", explore: "Explore the library", stages: "Connected stages",
    languages: "Complete languages", years: "Years of legacy",
    terminalLabel: "SIFAP 3270 terminal simulation", terminalCaption: "Before modernization: the original SIFAP.",
    terminalTitle: "Beneficiary query", terminalSearchType: "Search type", terminalReady: "Awaiting query",
    terminalSubmit: "Query", terminalExit: "Exit", terminalSimulation: "Visual simulation",
    terminalEmpty: "Empty field", terminalNotice: "Demonstration only. No connection to real data.",
    journeyLabel: "01 / The learning path", journeyTitle: "Four stages.\nOne traceable journey.",
    journeyLead: "Move from understanding the original system to a working modernization. Explore each stage and follow its guide.",
    libraryLabel: "02 / The complete collection", libraryTitle: "Everything you need.\nNothing hidden in folders.",
    libraryLead: "Every versioned file is available here: guides, personas, instructions, prompts, skills, source and assets. Filter the collection or search inside the documentation.",
    personasLabel: "03 / Your role", personasTitle: "Different perspectives.\nA shared delivery.",
    personasLead: "Discover your persona, its responsibilities and the tools that support your part of the journey.",
    sourceLabel: "04 / Open the source", sourceTitle: "The same knowledge.\nTwo ways to follow it.",
    sourceLead: "Prefer working in GitHub or VS Code? Every page links to its original file and immutable source commit. The website never replaces the repository.",
    sourceCommit: "Source commit", footerTitle: "Build with context.", footerLead: "The SIFAP modernization knowledge hub.",
    top: "Back to top", generated: "Built from versioned sources", contents: "On this page",
    navigation: "Browse the kit", original: "Open on GitHub", download: "Download original",
    copy: "Copy source", copied: "Copied", copyError: "Copy failed. Use the original download instead.",
    markRead: "Mark as read", markedRead: "Read", reading: "Reading progress", minutes: "min read",
    diagramError: "This diagram could not be rendered. Its original source remains available below.",
    viewSource: "Diagram source", technicalNote: "Technical source is shown in its original form to preserve behavior and provenance.",
    bytes: "bytes", allFiles: "All repository files", builtWith: "Astro + React · Hub Editorial", markdownSource: "Full Markdown source", filterPlaceholder: "SIFAP, requirements, Copilot…", licenses: "Licenses",
  },
  es: {
    kit: "Kit del equipo", privateKit: "Kit del instructor", privateNotice: "Privado · solo instructores autorizados",
    skip: "Saltar al contenido", home: "Inicio", journey: "Ruta de aprendizaje", library: "Biblioteca",
    personas: "Personas", repository: "Repositorio", language: "Idioma", menu: "Menú",
    search: "Buscar", searchHint: "Buscar en todo el kit", close: "Cerrar",
    loading: "Buscando…", noResults: "No hay contenido coincidente. Prueba otro término o borra los filtros.",
    searchError: "No se pudo cargar la búsqueda. Puedes seguir explorando la biblioteca completa.",
    searchPrompt: "Busca instrucciones, conceptos, archivos fuente y guías.",
    dark: "Tema oscuro", light: "Tema claro", preferencesError: "Este navegador no pudo guardar tu preferencia.",
    all: "Todos", category: "Categoría", kind: "Tipo de archivo", document: "Documento", source: "Código fuente",
    image: "Imagen", binary: "Descarga", filter: "Filtrar por título o ruta", clear: "Borrar filtros",
    results: "resultados", showMore: "Mostrar más", files: "Archivos", heroEyebrow: "SIFAP / Modernización de sistemas legados",
    heroTitle: "Comprende el pasado.\nConstruye lo que viene.",
    heroLead: "Una guía completa para modernizar Natural y Adabas con Java, Next.js y GitHub Copilot. Lee, descubre y sigue las mismas instrucciones aquí o en el repositorio.",
    start: "Comenzar el recorrido", explore: "Explorar la biblioteca", stages: "Etapas conectadas",
    languages: "Idiomas completos", years: "Años de legado",
    terminalLabel: "Simulación del terminal 3270 de SIFAP", terminalCaption: "Antes de modernizar: el SIFAP original.",
    terminalTitle: "Consulta de beneficiarios", terminalSearchType: "Tipo de búsqueda", terminalReady: "Esperando consulta",
    terminalSubmit: "Consultar", terminalExit: "Salir", terminalSimulation: "Simulación visual",
    terminalEmpty: "Campo vacío", terminalNotice: "Solo demostración. Sin conexión a datos reales.",
    journeyLabel: "01 / La ruta de aprendizaje", journeyTitle: "Cuatro etapas.\nUn recorrido trazable.",
    journeyLead: "Avanza desde la comprensión del sistema original hasta una modernización funcional. Explora cada etapa y sigue su guía.",
    libraryLabel: "02 / La colección completa", libraryTitle: "Todo lo que necesitas.\nNada oculto en carpetas.",
    libraryLead: "Todos los archivos versionados están aquí: guías, personas, instrucciones, prompts, skills, código y recursos. Filtra la colección o busca dentro de la documentación.",
    personasLabel: "03 / Tu rol", personasTitle: "Perspectivas diferentes.\nUna entrega compartida.",
    personasLead: "Descubre tu persona, sus responsabilidades y las herramientas que apoyan tu parte del recorrido.",
    sourceLabel: "04 / Consulta la fuente", sourceTitle: "El mismo conocimiento.\nDos maneras de seguirlo.",
    sourceLead: "¿Prefieres trabajar en GitHub o VS Code? Cada página enlaza con su archivo original y su commit inmutable. El sitio nunca sustituye al repositorio.",
    sourceCommit: "Commit de origen", footerTitle: "Construye con contexto.", footerLead: "El centro de conocimiento de modernización SIFAP.",
    top: "Volver arriba", generated: "Generado desde fuentes versionadas", contents: "En esta página",
    navigation: "Explorar el kit", original: "Abrir en GitHub", download: "Descargar original",
    copy: "Copiar código", copied: "Copiado", copyError: "No se pudo copiar. Descarga el archivo original.",
    markRead: "Marcar como leído", markedRead: "Leído", reading: "Progreso de lectura", minutes: "min de lectura",
    diagramError: "No se pudo representar este diagrama. Su fuente original sigue disponible debajo.",
    viewSource: "Fuente del diagrama", technicalNote: "El código técnico se muestra en su forma original para preservar el comportamiento y la procedencia.",
    bytes: "bytes", allFiles: "Todos los archivos del repositorio", builtWith: "Astro + React · Hub Editorial", markdownSource: "Fuente Markdown completa", filterPlaceholder: "SIFAP, requisitos, Copilot…", licenses: "Licencias",
  },
  "pt-br": {
    kit: "Kit do time", privateKit: "Kit do instrutor", privateNotice: "Privado · somente instrutores autorizados",
    skip: "Pular para o conteúdo", home: "Início", journey: "Trilha de aprendizagem", library: "Biblioteca",
    personas: "Personas", repository: "Repositório", language: "Idioma", menu: "Menu",
    search: "Buscar", searchHint: "Buscar em todo o kit", close: "Fechar",
    loading: "Buscando…", noResults: "Nenhum conteúdo encontrado. Tente outro termo ou limpe os filtros.",
    searchError: "Não foi possível carregar a busca. Você ainda pode navegar pela biblioteca completa.",
    searchPrompt: "Busque instruções, conceitos, arquivos-fonte e guias.",
    dark: "Tema escuro", light: "Tema claro", preferencesError: "Este navegador não conseguiu salvar sua preferência.",
    all: "Todos", category: "Categoria", kind: "Tipo de arquivo", document: "Documento", source: "Código-fonte",
    image: "Imagem", binary: "Download", filter: "Filtrar por título ou caminho", clear: "Limpar filtros",
    results: "resultados", showMore: "Mostrar mais", files: "Arquivos", heroEyebrow: "SIFAP / Modernização de legado",
    heroTitle: "Entenda o passado.\nConstrua o que vem depois.",
    heroLead: "Um guia completo para modernizar Natural e Adabas com Java, Next.js e GitHub Copilot. Leia, descubra e siga as mesmas instruções aqui ou no repositório.",
    start: "Começar a jornada", explore: "Explorar a biblioteca", stages: "Estágios conectados",
    languages: "Idiomas completos", years: "Anos de legado",
    terminalLabel: "Simulação do terminal 3270 do SIFAP", terminalCaption: "Antes da modernização: o SIFAP original.",
    terminalTitle: "Consulta de beneficiários", terminalSearchType: "Tipo de pesquisa", terminalReady: "Aguardando consulta",
    terminalSubmit: "Consultar", terminalExit: "Sair", terminalSimulation: "Simulação visual",
    terminalEmpty: "Campo vazio", terminalNotice: "Apenas demonstração. Sem conexão com dados reais.",
    journeyLabel: "01 / A trilha de aprendizagem", journeyTitle: "Quatro estágios.\nUma jornada rastreável.",
    journeyLead: "Avance do entendimento do sistema original até uma modernização funcionando. Explore cada estágio e siga seu guia.",
    libraryLabel: "02 / A coleção completa", libraryTitle: "Tudo o que você precisa.\nNada escondido em pastas.",
    libraryLead: "Todos os arquivos versionados estão aqui: guias, personas, instruções, prompts, skills, código e recursos. Filtre a coleção ou busque dentro da documentação.",
    personasLabel: "03 / Seu papel", personasTitle: "Perspectivas diferentes.\nUma entrega compartilhada.",
    personasLead: "Descubra sua persona, suas responsabilidades e as ferramentas que apoiam sua parte da jornada.",
    sourceLabel: "04 / Consulte a fonte", sourceTitle: "O mesmo conhecimento.\nDuas formas de seguir.",
    sourceLead: "Prefere trabalhar no GitHub ou no VS Code? Cada página aponta para seu arquivo original e commit imutável. O site nunca substitui o repositório.",
    sourceCommit: "Commit de origem", footerTitle: "Construa com contexto.", footerLead: "O hub de conhecimento da modernização SIFAP.",
    top: "Voltar ao topo", generated: "Gerado a partir de fontes versionadas", contents: "Nesta página",
    navigation: "Navegar pelo kit", original: "Abrir no GitHub", download: "Baixar original",
    copy: "Copiar código", copied: "Copiado", copyError: "Não foi possível copiar. Baixe o arquivo original.",
    markRead: "Marcar como lido", markedRead: "Lido", reading: "Progresso de leitura", minutes: "min de leitura",
    diagramError: "Não foi possível renderizar este diagrama. A fonte original continua disponível abaixo.",
    viewSource: "Fonte do diagrama", technicalNote: "O código técnico é exibido em sua forma original para preservar o comportamento e a proveniência.",
    bytes: "bytes", allFiles: "Todos os arquivos do repositório", builtWith: "Astro + React · Hub Editorial", markdownSource: "Fonte Markdown completa", filterPlaceholder: "SIFAP, requisitos, Copilot…", licenses: "Licenças",
  },
};

export const categories: Record<Locale, Record<Category, string>> = {
  en: { start: "Start here", archaeology: "Archaeology", specification: "Specification", implementation: "Implementation", evolution: "Evolution", personas: "Personas", agents: "Stage agents", concepts: "Concepts", "cheat-sheets": "Quick reference", documentation: "Documentation", copilot: "Copilot toolkit", infrastructure: "Infrastructure", portal: "Portal source", repository: "Repository resources" },
  es: { start: "Comienza aquí", archaeology: "Arqueología", specification: "Especificación", implementation: "Implementación", evolution: "Evolución", personas: "Personas", agents: "Agentes de etapa", concepts: "Conceptos", "cheat-sheets": "Referencia rápida", documentation: "Documentación", copilot: "Herramientas de Copilot", infrastructure: "Infraestructura", portal: "Código del portal", repository: "Recursos del repositorio" },
  "pt-br": { start: "Comece aqui", archaeology: "Arqueologia", specification: "Especificação", implementation: "Implementação", evolution: "Evolução", personas: "Personas", agents: "Agentes de estágio", concepts: "Conceitos", "cheat-sheets": "Referência rápida", documentation: "Documentação", copilot: "Ferramentas do Copilot", infrastructure: "Infraestrutura", portal: "Código do portal", repository: "Recursos do repositório" },
};

export function t(locale: Locale): Messages {
  return messages[locale];
}
