import { isUtf8 } from "node:buffer";
import { posix } from "node:path";

export const languages = [
  { code: "en", label: "English", branch: "main" },
  { code: "es", label: "Español", branch: "espanol" },
  { code: "pt-br", label: "Português (BR)", branch: "portugues-br" },
];

export function validatePath(path) {
  if (typeof path !== "string" || !path || path.startsWith("/") ||
      /[\u0000-\u001f\\]/u.test(path) ||
      path.split("/").some((part) => !part || part === "." || part === "..")) {
    throw new Error(`Invalid repository path: ${JSON.stringify(path)}`);
  }
  return path;
}

export function parseTree(text) {
  return text.split("\0").filter(Boolean).map((row) => {
    const separator = row.indexOf("\t");
    if (separator < 0) throw new Error("Invalid Git tree record.");
    const [mode, type, blob, size] = row.slice(0, separator).trim().split(/\s+/);
    const path = validatePath(row.slice(separator + 1));
    if (type !== "blob" || !["100644", "100755", "120000"].includes(mode)) {
      throw new Error(`Unsupported Git entry: ${path} (${type}/${mode}).`);
    }
    const bytes = Number(size);
    if (!/^[a-f0-9]{40,64}$/.test(blob ?? "") || !Number.isSafeInteger(bytes) || bytes < 0) {
      throw new Error(`Invalid Git blob metadata for ${path}.`);
    }
    return { mode, type, blob, bytes, path };
  });
}

export function parseBatch(buffer) {
  const blobs = new Map();
  let offset = 0;
  while (offset < buffer.length) {
    const end = buffer.indexOf(10, offset);
    if (end < 0) throw new Error("Truncated Git batch header.");
    const [blob, type, size] = buffer.subarray(offset, end).toString("utf8").split(" ");
    const length = Number(size);
    if (type !== "blob" || !/^[a-f0-9]{40,64}$/.test(blob ?? "") ||
        !Number.isSafeInteger(length) || length < 0) {
      throw new Error("Invalid Git batch blob header.");
    }
    const start = end + 1;
    const next = start + length;
    if (next >= buffer.length) throw new Error("Truncated Git batch content.");
    if (buffer[next] !== 10) throw new Error("Invalid Git batch delimiter.");
    blobs.set(blob, buffer.subarray(start, next));
    offset = next + 1;
  }
  return blobs;
}

export function decodeText(buffer) {
  return !buffer.includes(0) && isUtf8(buffer) ? buffer.toString("utf8") : undefined;
}

export function fileKind(path, buffer) {
  if (/\.md$/i.test(path)) {
    if (decodeText(buffer) === undefined) throw new Error(`Markdown must be UTF-8: ${path}`);
    return "document";
  }
  if (/\.(?:svg|png|jpe?g|webp|gif|avif)$/i.test(path)) return "image";
  return decodeText(buffer) === undefined ? "binary" : "source";
}

export function routeFor(path, kind) {
  validatePath(path);
  const transformed = (kind === "document" ? path.replace(/\.md$/i, "") : path)
    .split("/")
    .map((part) => encodeURIComponent(part.startsWith(".") ? `dot-${part.slice(1)}` : part))
    .join("/");
  return `${kind === "document" ? "docs" : "files"}/${transformed}`;
}

export function categoryFor(path) {
  if (path === "README.md" || /^00-/.test(path)) return "start";
  const prefix = path.split("/")[0];
  return ({
    "01-archaeology": "archaeology",
    "02-modern-spec": "specification",
    "03-implementation": "implementation",
    "04-evolution": "evolution",
    "05-personas": "personas",
    "06-stage-agents": "agents",
    "07-concepts": "concepts",
    "09-cheat-sheets": "cheat-sheets",
    docs: "documentation",
    ".github": "copilot",
    infra: "infrastructure",
    site: "portal",
    specs: "specification",
  })[prefix] ?? "repository";
}

export function siteBase(value) {
  const url = new URL(value);
  if (!["http:", "https:"].includes(url.protocol)) {
    throw new Error("The site base must be an HTTP or HTTPS URL.");
  }
  if (url.username || url.password || url.search || url.hash) {
    throw new Error("The site base cannot contain credentials, a query or a fragment.");
  }
  const basePath = `${url.pathname.replace(/\/+$/, "")}/`;
  return { siteUrl: `${url.origin}${basePath}`, basePath };
}

export function resolveRepositoryTarget(sourcePath, href) {
  if (/^(?:https?:|mailto:|tel:|\/\/)/i.test(href)) return { kind: "external", href };
  if (/^[a-z][a-z0-9+.-]*:/i.test(href)) return { kind: "blocked", href };
  if (/[<>{}*$]/.test(href) || /(?:^|\/)(?:NNN|XXX|YOUR[_-])/.test(href)) {
    return { kind: "placeholder", href };
  }
  const hashAt = href.indexOf("#");
  const fragment = hashAt < 0 ? "" : decodeURIComponent(href.slice(hashAt + 1));
  const beforeHash = hashAt < 0 ? href : href.slice(0, hashAt);
  const queryAt = beforeHash.indexOf("?");
  const query = queryAt < 0 ? "" : beforeHash.slice(queryAt + 1);
  const raw = decodeURIComponent(queryAt < 0 ? beforeHash : beforeHash.slice(0, queryAt));
  let path = raw
    ? posix.normalize(raw.startsWith("/") ? raw.slice(1) : posix.join(posix.dirname(sourcePath), raw))
    : sourcePath;
  if (path === ".." || path.startsWith("../")) {
    throw new Error(`Link escapes outside the repository: ${sourcePath}.`);
  }
  if (path === ".") path = "";
  return { kind: "file", path, fragment, query };
}

export function assertCoverage(editions, preserved = new Set()) {
  const codes = new Set(editions.map((edition) => edition.code));
  if (editions.length !== 3 || codes.size !== 3 ||
      languages.some((language) => !codes.has(language.code))) {
    throw new Error("All three language editions are required.");
  }
  const english = editions.find((edition) => edition.code === "en");
  const allPaths = new Set(editions.flatMap((edition) => edition.entries.map((entry) => entry.path)));
  for (const edition of editions) {
    const byPath = new Map(edition.entries.map((entry) => [entry.path, entry]));
    if (byPath.size !== edition.entries.length) throw new Error(`Duplicate source path in ${edition.code}.`);
    const routes = new Set();
    for (const entry of edition.entries) {
      if (entry.route && routes.has(entry.route)) {
        throw new Error(`Route collision in ${edition.code}: ${entry.route}`);
      }
      if (entry.route) routes.add(entry.route);
    }
    for (const path of allPaths) {
      if (!byPath.has(path)) throw new Error(`Missing ${edition.code} counterpart: ${path}`);
    }
    if (edition.code !== "en") {
      for (const source of english.entries) {
        if (source.path.startsWith("site/") && source.kind !== "document" &&
            byPath.get(source.path)?.blob !== source.blob) {
          throw new Error(`Portal engine differs in ${edition.code}: ${source.path}`);
        }
        if (source.kind === "document" && !preserved.has(source.path)) {
          const translated = byPath.get(source.path);
          if (translated?.blob === source.blob) {
            throw new Error(`Untranslated ${edition.code} document: ${source.path}`);
          }
          if (typeof source.text === "string") {
            if (typeof translated?.text !== "string") throw new Error(`Missing document text: ${source.path}`);
            const unchanged = unchangedProseLines(source.text, translated.text);
            if (unchanged.length) {
              throw new Error(`Untranslated prose in ${edition.code}:${source.path} at lines ${unchanged.join(", ")}.`);
            }
          }
        }
      }
    }
  }
}

export function unchangedProseLines(original, translated) {
  function candidates(text) {
    let fence;
    let fenceLength = 0;
    let frontmatter = text.startsWith("---\n");
    const lines = [];
    for (const [index, raw] of text.split("\n").entries()) {
      const line = raw.trim();
      if (index === 0 && frontmatter) continue;
      if (frontmatter) { if (line === "---") frontmatter = false; continue; }
      const marker = line.match(/^(`{3,}|~{3,})/);
      if (marker) {
        if (!fence) { fence = marker[1][0]; fenceLength = marker[1].length; }
        else if (marker[1][0] === fence && marker[1].length >= fenceLength) fence = undefined;
        continue;
      }
      if (fence || /^[>#<]/.test(line)) continue;
      const prose = line.replace(/`[^`]*`/g, "").replace(/\[([^\]]*)\]\([^)]*\)/g, "$1");
      if (prose.length >= 140 && (prose.match(/\p{L}+/gu) ?? []).length >= 20) {
        lines.push({ line: index + 1, text: line.replace(/\s+/g, " ") });
      }
    }
    return lines;
  }
  const source = new Set(candidates(original).map((line) => line.text));
  return candidates(translated).filter((line) => source.has(line.text)).map((line) => line.line);
}

export function assertPagesAccess(repository, pages) {
  if (typeof repository?.private !== "boolean" || typeof pages?.public !== "boolean") {
    throw new Error("Repository or Pages visibility is unknown; publication is blocked.");
  }
  if (repository.private && pages.public) {
    throw new Error("A private repository must never publish to public Pages.");
  }
  if (pages.build_type !== "workflow") {
    throw new Error("Pages must use a verified workflow deployment.");
  }
  const url = siteBase(pages.html_url).siteUrl;
  if (!url.startsWith("https://")) throw new Error("Published Pages must use HTTPS.");
  return url;
}

export function escapeHtml(text) {
  return text.replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}

export function renderSourceLines(text) {
  return text.split("\n").map((line, index) => {
    const number = index + 1;
    return `<span id="L${number}" class="source-line"><a class="line-number" href="#L${number}" aria-label="${number}">${number}</a>${escapeHtml(line)}</span>`;
  }).join("");
}
