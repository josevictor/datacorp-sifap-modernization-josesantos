import assert from "node:assert/strict";
import test from "node:test";
import { assessContentReadiness } from "../scripts/lib/content-readiness.mjs";

function editions() {
  return [
    { code: "en", branch: "main", hash: "a", title: "Guide" },
    { code: "es", branch: "espanol", hash: "b", title: "Guía" },
    { code: "pt-br", branch: "portugues-br", hash: "c", title: "Guia" },
  ].map(({ code, branch, hash, title }) => ({
    code,
    ref: `origin/${branch}`,
    commit: hash.repeat(40),
    metadata: JSON.stringify({ language: code, branch }),
    entries: [
      { path: "README.md", kind: "document", blob: hash.repeat(40), text: `# ${title}` },
      { path: ".github/agents/builder.agent.md", kind: "document", blob: hash.repeat(40), text: `# ${title}` },
      { path: "legacy/program.NSP", kind: "source", blob: "d".repeat(40) },
    ],
  }));
}

test("should report complete inventories without claiming a deployment or a completed build", () => {
  // REQ-PORTAL-001, REQ-PORTAL-002, REQ-PORTAL-010
  const report = assessContentReadiness(editions());
  assert.equal(report.status, "ready-for-build");
  assert.equal(report.totalPaths, 3);
  assert.equal(report.buildValidation, "not-run");
  assert.deepEqual(report.issues, []);
  assert.deepEqual(report.files.map(({ path }) => path),
    [".github/agents/builder.agent.md", "README.md", "legacy/program.NSP"]);
  assert.deepEqual(report.files[2].editions.es,
    { status: "available", kind: "source", blob: "d".repeat(40) });
  assert.deepEqual(report.editions.map(({ files, documents, otherFiles }) => ({ files, documents, otherFiles })),
    Array(3).fill({ files: 3, documents: 2, otherFiles: 1 }));
});

test("should list every missing counterpart rather than stop at the first gap", () => {
  // REQ-PORTAL-001, REQ-PORTAL-002
  const sources = editions();
  sources[1].entries = sources[1].entries.slice(2);
  sources[2].entries = sources[2].entries.slice(0, 1);
  const report = assessContentReadiness(sources);
  assert.equal(report.status, "blocked");
  assert.deepEqual(report.editions[1].missingFiles, [".github/agents/builder.agent.md", "README.md"]);
  assert.deepEqual(report.editions[2].missingFiles, [".github/agents/builder.agent.md", "legacy/program.NSP"]);
  assert.equal(report.issues.filter(({ kind }) => kind === "missing-file").length, 4);
});

test("should show absent published refs alongside metadata and untranslated-document blockers", () => {
  // REQ-PORTAL-002, REQ-PORTAL-010
  const sources = editions();
  delete sources[0].metadata;
  sources[1] = { code: "es", ref: "origin/espanol" };
  sources[2].entries[0] = { ...sources[0].entries[0] };
  const report = assessContentReadiness(sources);
  assert.equal(report.status, "blocked");
  assert.equal(report.editions[1].commit, null);
  assert.equal(report.editions[1].files, 0);
  assert.equal(report.editions[1].missingFiles.length, 3);
  assert.equal(report.files[0].editions.es.status, "unavailable-ref");
  assert.deepEqual(report.editions[2].untranslatedDocuments, ["README.md"]);
  assert.ok(report.issues.some(({ kind, language }) => kind === "missing-ref" && language === "es"));
  assert.ok(report.issues.some(({ kind, language }) => kind === "missing-metadata" && language === "en"));
  assert.ok(report.issues.some(({ kind, language }) => kind === "untranslated-document" && language === "pt-br"));
  assert.equal(report.issues.some(({ kind, path }) =>
    kind === "untranslated-document" && path === "legacy/program.NSP"), false);
});

test("should reject malformed metadata, wrong language identity and fixture commits", () => {
  // REQ-PORTAL-002, REQ-PORTAL-010
  const sources = editions();
  sources[0].metadata = "{invalid";
  sources[1].metadata = JSON.stringify({ language: "en", branch: "main" });
  sources[2].commit = "0".repeat(40);
  const report = assessContentReadiness(sources);
  assert.equal(report.status, "blocked");
  assert.equal(report.issues.filter(({ kind }) => kind === "invalid-metadata").length, 2);
  assert.ok(report.issues.some(({ kind, language }) => kind === "invalid-commit" && language === "pt-br"));
});

test("should keep original document text out of the readiness report", () => {
  // REQ-PORTAL-008
  const sources = editions();
  sources[0].entries[0].text = "# Private content that belongs only in the authenticated portal";
  const json = JSON.stringify(assessContentReadiness(sources));
  assert.doesNotMatch(json, /Private content that belongs/);
  assert.match(json, /README\.md/);
});

test("should retain production coverage failures after all paths and language metadata match", () => {
  // REQ-PORTAL-010
  const sources = editions();
  for (const source of sources) {
    source.entries[0].route = "docs/collision";
    source.entries[1].route = "docs/collision";
  }
  const report = assessContentReadiness(sources);
  assert.equal(report.status, "blocked");
  assert.equal(report.issues[0].kind, "coverage-validation");
  assert.match(report.issues[0].message, /collision/i);
});

test("should reject ambiguous or incomplete source selections", () => {
  // REQ-PORTAL-002
  assert.throws(() => assessContentReadiness(editions().slice(0, 2)), /three|edition/i);
  assert.throws(() => assessContentReadiness([editions()[0], editions()[0], editions()[2]]), /three|edition/i);
});
