import { assertCoverage, languages } from "./content.mjs";

export function assessContentReadiness(sources) {
  const byLocale = new Map(sources.map((source) => [source.code, source]));
  if (sources.length !== languages.length || byLocale.size !== languages.length ||
      languages.some(({ code }) => !byLocale.has(code))) {
    throw new Error("Select exactly the three required language editions.");
  }
  const allPaths = [...new Set(sources.flatMap((source) =>
    (source.entries ?? []).map(({ path }) => path)))].sort();
  const entriesByLocale = new Map(sources.map((source) => [
    source.code, new Map((source.entries ?? []).map((entry) => [entry.path, entry])),
  ]));
  const english = byLocale.get("en");
  const issues = [];
  const editions = languages.map(({ code, branch }) => {
    const source = byLocale.get(code);
    const entries = source.entries ?? [];
    const byPath = entriesByLocale.get(code);
    const addIssue = (kind, details = {}) => issues.push({ language: code, kind, ...details });
    if (source.commit === undefined) {
      addIssue("missing-ref", { ref: source.ref });
    } else {
      if (!/^[a-f0-9]{40,64}$/.test(source.commit) || /^0+$/.test(source.commit)) {
        addIssue("invalid-commit", { ref: source.ref });
      }
      if (source.metadata === undefined) {
        addIssue("missing-metadata", { path: ".github/language.json" });
      } else {
        let metadata;
        try {
          metadata = JSON.parse(source.metadata);
        } catch (error) {
          if (!(error instanceof SyntaxError)) throw error;
        }
        if (!metadata || metadata.language !== code || metadata.branch !== branch) {
          addIssue("invalid-metadata", { path: ".github/language.json" });
        }
      }
    }
    if (byPath.size !== entries.length) addIssue("duplicate-path");
    const missingFiles = allPaths.filter((path) => !byPath.has(path));
    for (const path of missingFiles) addIssue("missing-file", { path });
    const untranslatedDocuments = code === "en" ? [] : (english.entries ?? [])
      .filter((entry) => entry.kind === "document" && byPath.get(entry.path)?.blob === entry.blob)
      .map(({ path }) => path).sort();
    for (const path of untranslatedDocuments) addIssue("untranslated-document", { path });
    const documents = entries.filter(({ kind }) => kind === "document").length;
    return {
      language: code,
      branch,
      ref: source.ref,
      commit: source.commit ?? null,
      files: entries.length,
      documents,
      otherFiles: entries.length - documents,
      missingFiles,
      untranslatedDocuments,
    };
  });
  if (issues.length === 0) {
    try {
      assertCoverage(sources);
    } catch (error) {
      if (!(error instanceof Error) || error.name !== "Error") throw error;
      issues.push({ kind: "coverage-validation", message: error.message });
    }
  }
  return {
    schemaVersion: 1,
    status: issues.length ? "blocked" : "ready-for-build",
    buildValidation: "not-run",
    totalPaths: allPaths.length,
    editions,
    files: allPaths.map((path) => ({
      path,
      editions: Object.fromEntries(editions.map((edition) => {
        const entry = entriesByLocale.get(edition.language).get(path);
        const status = !edition.commit ? "unavailable-ref" : !entry ? "missing" :
          edition.untranslatedDocuments.includes(path) ? "untranslated" : "available";
        return [edition.language, { status, ...(entry ? { kind: entry.kind, blob: entry.blob } : {}) }];
      })),
    })),
    issues,
  };
}
