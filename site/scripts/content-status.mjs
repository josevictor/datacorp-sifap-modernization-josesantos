import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { decodeText, fileKind, languages, routeFor } from "./lib/content.mjs";
import { assessContentReadiness } from "./lib/content-readiness.mjs";
import { git, readSnapshot, repositorySlug } from "./lib/git.mjs";

const siteRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(siteRoot, "..");
const args = process.argv.slice(2);
if (args.length && (args.length !== 2 || args[0] !== "--output" || !args[1].endsWith(".json"))) {
  throw new Error("Usage: npm run content:status -- [--output path/to/report.json]");
}
const output = args.length ? resolve(args[1]) : resolve(siteRoot, ".generated/content-readiness.json");
const settings = JSON.parse(readFileSync(resolve(siteRoot, "repository.json"), "utf8"));
const repository = repositorySlug(repositoryRoot);
if (settings.repository !== repository || !["team", "instructor"].includes(settings.audience)) {
  throw new Error("site/repository.json must identify the current GitHub repository and audience.");
}

function findCommit(ref) {
  if (!ref || ref.startsWith("-") || /[\0\r\n]/.test(ref)) {
    throw new Error("Invalid content reference.");
  }
  try {
    return git(repositoryRoot, ["rev-parse", "--verify", "--quiet", "--end-of-options", `${ref}^{commit}`], {
      encoding: "utf8",
      stdio: ["pipe", "pipe", "pipe"],
    }).trim();
  } catch (error) {
    if (!(error instanceof Error) || !("status" in error) || error.status !== 1) throw error;
    return undefined;
  }
}

const sources = languages.map(({ code, branch }) => {
  const variable = `CONTENT_REF_${code.toUpperCase().replaceAll("-", "_")}`;
  const ref = process.env[variable] ?? `origin/${branch}`;
  const commit = findCommit(ref);
  if (!commit) return { code, ref };
  const snapshot = readSnapshot(repositoryRoot, commit);
  const metadataFile = snapshot.files.find(({ path }) => path === ".github/language.json");
  return {
    code,
    ref,
    commit,
    metadata: metadataFile ? decodeText(snapshot.blobs.get(metadataFile.blob)) : undefined,
    entries: snapshot.files.map((file) => {
      const buffer = snapshot.blobs.get(file.blob);
      const kind = file.mode === "120000" ? "source" : fileKind(file.path, buffer);
      return {
        path: file.path,
        blob: file.blob,
        kind,
        route: routeFor(file.path, kind),
        ...(kind === "document" ? { text: decodeText(buffer) } : {}),
      };
    }),
  };
});
const report = {
  repository,
  audience: settings.audience,
  inspectedAt: new Date().toISOString(),
  ...assessContentReadiness(sources),
};
mkdirSync(dirname(output), { recursive: true });
writeFileSync(output, `${JSON.stringify(report, null, 2)}\n`);
console.table(report.editions.map((edition) => ({
  language: edition.language,
  ref: edition.ref,
  files: edition.files,
  markdown: edition.documents,
  missing: edition.missingFiles.length,
  untranslated: edition.untranslatedDocuments.length,
})));
console.log(`Content status: ${report.status}. ${report.totalPaths} distinct tracked paths.`);
console.log(`Complete report: ${output}`);
console.log("This check does not build or deploy the portal. The production build and Pages access checks remain mandatory.");
if (report.issues.length) {
  const counts = new Map();
  for (const { kind } of report.issues) counts.set(kind, (counts.get(kind) ?? 0) + 1);
  console.error(`Blockers: ${[...counts].map(([kind, count]) => `${kind}=${count}`).join(", ")}`);
  process.exitCode = 1;
}
