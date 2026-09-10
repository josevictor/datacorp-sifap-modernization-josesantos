import { createHash } from "node:crypto";
import { existsSync, lstatSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { assertCoverage, categoryFor, decodeText, fileKind, languages, renderSourceLines, routeFor, siteBase } from "./lib/content.mjs";
import { readSnapshot, repositorySlug } from "./lib/git.mjs";
import { renderDocument } from "./lib/markdown.mjs";
import { addEquivalentHeadingAliases, unresolvedFragments } from "./lib/anchors.mjs";

const siteRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(siteRoot, "..");
const settings = JSON.parse(readFileSync(resolve(siteRoot, "repository.json"), "utf8"));
const repository = repositorySlug(repositoryRoot);
if (settings.repository !== repository || !["team", "instructor"].includes(settings.audience)) {
  throw new Error("site/repository.json must identify the current GitHub repository and audience.");
}
if (process.env.GITHUB_ACTIONS === "true" && !process.env.SITE_URL) {
  throw new Error("CI must supply the verified Pages SITE_URL.");
}
const { siteUrl, basePath } = siteBase(process.env.SITE_URL ?? settings.pagesUrl);
const inspectLocale = process.argv.includes("--inspect")
  ? process.argv[process.argv.indexOf("--inspect") + 1]
  : undefined;
if (inspectLocale && !languages.some((language) => language.code === inspectLocale)) {
  throw new Error("Inspection requires a known locale.");
}

function resetOutput(relative) {
  if (![".generated", "public/content-raw", "public/content-media"].includes(relative)) {
    throw new Error("Refusing to remove an unowned output directory.");
  }
  const path = resolve(siteRoot, relative);
  if (existsSync(path)) {
    if (lstatSync(path).isSymbolicLink() || !lstatSync(path).isDirectory()) {
      throw new Error(`Generated output must be a real directory: ${relative}`);
    }
    rmSync(path, { recursive: true });
  }
  mkdirSync(path, { recursive: true });
}

function canDisplayImage(path, buffer) {
  if (!/\.svg$/i.test(path)) return true;
  const text = decodeText(buffer);
  return text !== undefined && !/<(?:script|foreignObject)\b|<!ENTITY|\bon\w+\s*=|javascript:/i.test(text);
}

function assertPublishable(file, buffer) {
  if (/^(?:site\/(?:dist|\.generated)|site\/public\/content-(?:raw|media))\//.test(file.path)) {
    throw new Error(`Generated portal output must not be tracked: ${file.path}`);
  }
  if (/(?:^|\/)\.env(?:$|\.(?:local|production|development)$)|\.tfstate(?:\.|$)/.test(file.path)) {
    throw new Error(`Sensitive runtime state cannot be published: ${file.path}`);
  }
  const text = decodeText(buffer);
  if (text && /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/.test(text)) {
    throw new Error(`Private key material cannot be published: ${file.path}`);
  }
}

const snapshots = languages.filter((language) => !inspectLocale || language.code === inspectLocale).map((language) => {
  const variable = `CONTENT_REF_${language.code.toUpperCase().replaceAll("-", "_")}`;
  const ref = process.env[variable] ?? `origin/${language.branch}`;
  const snapshot = readSnapshot(repositoryRoot, ref);
  const metadataFile = snapshot.files.find((file) => file.path === ".github/language.json");
  if (!inspectLocale) {
    if (!metadataFile) throw new Error(`Missing language metadata in ${language.branch}.`);
    const metadata = JSON.parse(snapshot.blobs.get(metadataFile.blob).toString("utf8"));
    if (metadata.language !== language.code || metadata.branch !== language.branch) {
      throw new Error(`Language metadata does not match ${language.code}/${language.branch}.`);
    }
  }
  return { ...language, ...snapshot };
});

const blobFiles = new Map();
const editions = snapshots.map((snapshot) => ({
  code: snapshot.code,
  label: snapshot.label,
  branch: snapshot.branch,
  commit: snapshot.commit,
  entries: snapshot.files.map((file) => {
    const buffer = snapshot.blobs.get(file.blob);
    assertPublishable(file, buffer);
    const kind = file.mode === "120000" ? "source" : fileKind(file.path, buffer);
    const text = decodeText(buffer);
    const route = routeFor(file.path, kind);
    const extension = extname(file.path).slice(1).toLowerCase();
    const media = kind === "image" && canDisplayImage(file.path, buffer)
      ? `${file.blob}.${extension}`
      : undefined;
    blobFiles.set(file.blob, { buffer, media });
    return {
      id: createHash("sha256").update(file.path).digest("hex").slice(0, 24),
      path: file.path,
      title: file.path.split("/").at(-1),
      description: "",
      kind,
      category: categoryFor(file.path),
      extension,
      bytes: file.bytes,
      lines: text === undefined ? 0 : text.split(/\r?\n/).length,
      blob: file.blob,
      route,
      href: `${basePath}${snapshot.code}/${route}/`,
      sourceHref: `https://github.com/${repository}/blob/${snapshot.commit}/${file.path.split("/").map(encodeURIComponent).join("/")}`,
      downloadHref: `${basePath}content-raw/${file.blob}.bin`,
      ...(media ? { mediaHref: `${basePath}content-media/${media}` } : {}),
      ...(text === undefined ? {} : { text }),
      ...(text !== undefined && kind !== "document" ? { html: renderSourceLines(text) } : {}),
      headings: [],
      anchors: [],
    };
  }),
}));

if (!inspectLocale) assertCoverage(editions);

const references = [];
const unresolved = [];
const placeholders = [];
for (const edition of editions) {
  const byPath = new Map(edition.entries.map((entry) => [entry.path, entry]));
  for (const entry of edition.entries) {
    if (entry.kind !== "document") continue;
    const rendered = await renderDocument(entry.text, {
      locale: edition.code,
      repository,
      sourcePath: entry.path,
      byPath,
      editions,
      references,
      unresolved,
      placeholders,
    });
    Object.assign(entry, rendered);
  }
}

const headingAliases = inspectLocale ? 0 : addEquivalentHeadingAliases(editions);
const missingFragments = unresolvedFragments(editions, references);
const report = {
  repository,
  generatedAt: new Date().toISOString(),
  sources: editions.map((edition) => ({
    language: edition.code,
    branch: edition.branch,
    commit: edition.commit,
    files: edition.entries.length,
    documents: edition.entries.filter((entry) => entry.kind === "document").length,
  })),
  uniqueBlobs: blobFiles.size,
  references: references.length,
  headingAliases,
  missingFragments,
  unresolved,
  placeholders,
};
if (inspectLocale) {
  mkdirSync(resolve(siteRoot, ".generated"), { recursive: true });
  writeFileSync(resolve(siteRoot, `.generated/inspection-${inspectLocale}.json`), `${JSON.stringify(report, null, 2)}\n`);
  console.log(JSON.stringify({ ...report, placeholders: placeholders.length, unresolved: unresolved.length }, null, 2));
  process.exitCode = unresolved.length || missingFragments.length ? 1 : 0;
} else {
  if (unresolved.length || missingFragments.length) {
    mkdirSync(resolve(siteRoot, ".generated"), { recursive: true });
    writeFileSync(resolve(siteRoot, ".generated/content-errors.json"), `${JSON.stringify(report, null, 2)}\n`);
    throw new Error(`${unresolved.length} unresolved repository links and ${missingFragments.length} missing fragments. See .generated/content-errors.json.`);
  }
  for (const directory of [".generated", "public/content-raw", "public/content-media"]) resetOutput(directory);
  for (const [blob, file] of blobFiles) {
    writeFileSync(resolve(siteRoot, `public/content-raw/${blob}.bin`), file.buffer);
    if (file.media) writeFileSync(resolve(siteRoot, `public/content-media/${file.media}`), file.buffer);
  }
  const catalog = {
    schemaVersion: 1,
    repository,
    audience: settings.audience,
    siteUrl,
    basePath,
    generatedAt: report.generatedAt,
    editions,
  };
  if (catalog.editions.some((edition) => /^0+$/.test(edition.commit))) {
    throw new Error("Preview fixtures cannot be used as production source snapshots.");
  }
  writeFileSync(resolve(siteRoot, ".generated/catalog.json"), `${JSON.stringify(catalog)}\n`);
  writeFileSync(resolve(siteRoot, ".generated/coverage.json"), `${JSON.stringify(report, null, 2)}\n`);
  console.log(`Prepared ${editions.length} editions, ${editions.reduce((sum, edition) => sum + edition.entries.length, 0)} file views and ${blobFiles.size} original blobs.`);
}
