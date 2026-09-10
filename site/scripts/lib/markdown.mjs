import { createMarkdownProcessor, rehypeHeadingIds } from "@astrojs/markdown-remark";
import rehypeRaw from "rehype-raw";
import rehypeSanitize, { defaultSchema } from "rehype-sanitize";
import { escapeHtml, resolveRepositoryTarget } from "./content.mjs";

const labels = {
  en: { metadata: "File metadata", future: "Created during the exercise", NOTE: "Note", TIP: "Tip", IMPORTANT: "Important", WARNING: "Warning", CAUTION: "Caution" },
  es: { metadata: "Metadatos del archivo", future: "Se crea durante el ejercicio", NOTE: "Nota", TIP: "Consejo", IMPORTANT: "Importante", WARNING: "Advertencia", CAUTION: "Precaución" },
  "pt-br": { metadata: "Metadados do arquivo", future: "Criado durante o exercício", NOTE: "Nota", TIP: "Dica", IMPORTANT: "Importante", WARNING: "Aviso", CAUTION: "Cuidado" },
};

function walk(node, visitor, parent) {
  visitor(node, parent);
  if (Array.isArray(node.children)) {
    for (const child of node.children) walk(child, visitor, node);
  }
}

function plain(node) {
  if (node.type === "text" || node.type === "inlineCode") return node.value ?? "";
  return Array.isArray(node.children) ? node.children.map(plain).join("") : "";
}

function entryFor(path, entries) {
  const stripped = path.replace(/\/+$/, "");
  return entries.get(stripped) ?? entries.get(`${stripped ? `${stripped}/` : ""}README.md`) ??
    entries.get(`${stripped ? `${stripped}/` : ""}readme.md`) ??
    entries.get(`${stripped ? `${stripped}/` : ""}00-README.md`) ??
    entries.get(`${stripped ? `${stripped}/` : ""}SKILL.md`);
}

function resolveHref(href, context, image = false) {
  const owned = `https://github.com/${context.repository}/blob/`;
  let targetContext = context;
  let targetHref = href;
  if (href.startsWith(owned)) {
    const rest = href.slice(owned.length);
    const separator = rest.indexOf("/");
    const branch = rest.slice(0, separator);
    const edition = context.editions.find((item) => item.branch === branch || item.commit === branch);
    if (separator >= 0 && edition) {
      targetContext = { ...context, locale: edition.code, byPath: new Map(edition.entries.map((entry) => [entry.path, entry])) };
      targetHref = `/${rest.slice(separator + 1)}`;
    }
  }
  const target = resolveRepositoryTarget(context.sourcePath, targetHref);
  if (target.kind !== "file") return target;
  const entry = entryFor(target.path, targetContext.byPath);
  if (!entry) {
    const directory = target.path.replace(/\/+$/, "");
    const child = [...targetContext.byPath.values()].find((item) => item.path.startsWith(`${directory}/`));
    if (child && !target.fragment && !image) {
      const localeRoot = child.href.split(`/${targetContext.locale}/`)[0];
      return { kind: "resolved", href: `${localeRoot}/${targetContext.locale}/library/?path=${encodeURIComponent(`${directory}/`)}` };
    }
    if (/^(?:backend|frontend)\//.test(target.path)) return { kind: "placeholder", href };
    context.unresolved.push({ source: context.sourcePath, target: target.path, href });
    return { kind: "missing", href };
  }
  const rawFragment = target.fragment.replace(/^(L\d+)-L\d+$/, "$1");
  const fragment = rawFragment
    ? `#${encodeURIComponent(entry.kind === "document" ? `doc-${rawFragment}` : rawFragment)}`
    : "";
  const url = image ? (entry.mediaHref ?? entry.downloadHref) :
    target.query === "raw=true" ? entry.downloadHref : `${entry.href}${fragment}`;
  context.references.push({
    source: context.sourcePath,
    target: entry.path,
    locale: targetContext.locale,
    fragment: rawFragment,
    href: url,
  });
  return { kind: "resolved", href: url };
}

function portalHtml(options) {
  const { context, state } = options;
  const text = labels[context.locale];
  if (!text) throw new Error(`Unknown document locale: ${context.locale}`);
  return (tree, file) => {
    walk(tree, (node, parent) => {
      if (node.type !== "element") return;
      node.properties ??= {};
      if (typeof node.properties.id === "string") node.properties.id = `doc-${node.properties.id}`;
      if (node.tagName === "h1" && !state.title) {
        state.title = plain(node);
        node.tagName = "span";
        node.children = [];
      }
      if (node.tagName === "p" && parent?.tagName !== "blockquote" && !state.description) {
        const value = plain(node).replace(/\s+/g, " ").trim();
        if (value.length > 40 && !value.startsWith("[!")) state.description = value.slice(0, 230);
      }
      if (node.tagName === "blockquote") {
        const paragraph = node.children?.find((child) => child.tagName === "p");
        const first = paragraph?.children?.find((child) => child.type === "text");
        const match = first?.value?.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*/);
        if (match) {
          first.value = first.value.slice(match[0].length);
          node.properties.className = ["admonition", `admonition-${match[1].toLowerCase()}`];
          node.children.unshift({
            type: "element", tagName: "strong", properties: { className: ["admonition-title"] },
            children: [{ type: "text", value: text[match[1]] }],
          });
        }
      }
      if (node.tagName === "img" && typeof node.properties.src === "string") {
        if (/^https:\/\/(?:img\.shields\.io|badgen\.net)\//.test(node.properties.src)) {
          node.tagName = "span";
          node.children = [{ type: "text", value: String(node.properties.alt ?? "") }];
          node.properties = { className: ["doc-badge"] };
          return;
        }
        const target = resolveHref(node.properties.src, context, true);
        if (target.kind === "external" || target.kind === "resolved") {
          node.properties.src = target.href;
          node.properties.loading = "lazy";
          node.properties.decoding = "async";
        } else {
          node.tagName = "span";
          node.children = [{ type: "text", value: String(node.properties.alt ?? node.properties.src) }];
          node.properties = { className: ["unresolved-reference"] };
        }
      }
      if (node.tagName === "a" && typeof node.properties.href === "string") {
        const original = node.properties.href;
        const target = resolveHref(original, context);
        if (target.kind === "external" || target.kind === "resolved") {
          node.properties.href = target.href;
          if (target.kind === "external") node.properties.rel = ["noopener", "noreferrer"];
        } else {
          if (target.kind === "blocked") {
            throw new Error(`Unsafe link protocol in ${context.sourcePath}.`);
          }
          if (target.kind === "placeholder") {
            context.placeholders.push({ source: context.sourcePath, href: original });
          }
          node.tagName = "span";
          node.properties = {
            className: [target.kind === "placeholder" ? "future-artifact" : "unresolved-reference"],
            title: target.kind === "placeholder" ? `${text.future}: ${original}` : original,
          };
        }
      }
    });
    const headings = [];
    const anchors = [];
    walk(tree, (node) => {
      if (node.type === "element" && typeof node.properties?.id === "string") {
        anchors.push(node.properties.id);
      }
      if (node.type === "element" && /^h[2-6]$/.test(node.tagName) &&
          typeof node.properties?.id === "string") {
        headings.push({ depth: Number(node.tagName[1]), slug: node.properties.id, text: plain(node) });
      }
    });
    file.data.astro ??= {};
    file.data.astro.headings = headings;
    state.anchors = anchors;
  };
}

function splitMetadata(text) {
  const normalized = text.replace(/^\uFEFF/, "").replace(/\r\n/g, "\n");
  if (!normalized.startsWith("---\n")) return { metadata: "", body: normalized };
  const end = normalized.indexOf("\n---", 4);
  if (end < 0) throw new Error("Unclosed Markdown frontmatter.");
  const metadata = normalized.slice(4, end);
  if (!/^[a-z][\w-]*:/im.test(metadata)) return { metadata: "", body: normalized };
  return { metadata, body: normalized.slice(end + 4).replace(/^\n/, "") };
}

export async function renderDocument(source, context) {
  const state = { title: "", description: "", anchors: [] };
  const { metadata, body } = splitMetadata(source);
  const schema = {
    ...defaultSchema,
    clobberPrefix: "",
    attributes: {
      ...defaultSchema.attributes,
      "*": [...(defaultSchema.attributes["*"] ?? []), "className"],
      code: [...(defaultSchema.attributes.code ?? []), ["className", /^language-/]],
      img: [...(defaultSchema.attributes.img ?? []), "loading", "decoding"],
    },
  };
  const processor = await createMarkdownProcessor({
    gfm: true,
    smartypants: false,
    syntaxHighlight: false,
    rehypePlugins: [
      rehypeRaw,
      rehypeHeadingIds,
      [portalHtml, { context, state }],
      [rehypeSanitize, schema],
    ],
  });
  const result = await processor.render(body);
  const metadataHtml = metadata
    ? `<details class="source-metadata"><summary>${labels[context.locale].metadata}</summary><pre><code class="language-yaml">${escapeHtml(metadata)}</code></pre></details>`
    : "";
  return {
    title: state.title || context.sourcePath.split("/").at(-1),
    description: state.description,
    html: `${metadataHtml}${result.code}`,
    headings: result.metadata.headings,
    anchors: state.anchors,
  };
}
