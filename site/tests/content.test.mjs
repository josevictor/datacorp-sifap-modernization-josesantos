import assert from "node:assert/strict";
import test from "node:test";
import {
  assertCoverage,
  assertPagesAccess,
  categoryFor,
  decodeText,
  fileKind,
  parseBatch,
  parseTree,
  resolveRepositoryTarget,
  renderSourceLines,
  routeFor,
  siteBase,
  unchangedProseLines,
} from "../scripts/lib/content.mjs";

const hash = "a".repeat(40);
const otherHash = "b".repeat(40);

test("should preserve Git paths, modes and bytes in the complete inventory", () => {
  // REQ-PORTAL-001
  const rows = parseTree(`100644 blob ${hash} 12\tdocs/a file.md\0` +
    `120000 blob ${otherHash} 15\tlink\0`);
  assert.equal(rows.length, 2);
  assert.deepEqual(rows[0], { mode: "100644", type: "blob", blob: hash, bytes: 12, path: "docs/a file.md" });
  assert.equal(rows[1].mode, "120000");
});

test("should reject invalid Git paths and unsupported entries", () => {
  // REQ-PORTAL-008
  assert.throws(() => parseTree(`100644 blob ${hash} 1\t../outside\0`), /path/i);
  assert.throws(() => parseTree(`100644 blob ${hash} 1\t/absolute\0`), /path/i);
  assert.throws(() => parseTree(`160000 commit ${hash} -\tmodule\0`), /unsupported/i);
});

test("should decode batched Git blobs without changing their original bytes", () => {
  // REQ-PORTAL-008
  const first = Buffer.from("á\nx", "utf8");
  const second = Buffer.from([0, 255, 10]);
  const response = Buffer.concat([
    Buffer.from(`${hash} blob ${first.length}\n`), first, Buffer.from("\n"),
    Buffer.from(`${otherHash} blob ${second.length}\n`), second, Buffer.from("\n"),
  ]);
  const blobs = parseBatch(response);
  assert.deepEqual(blobs.get(hash), first);
  assert.deepEqual(blobs.get(otherHash), second);
  assert.throws(() => parseBatch(response.subarray(0, response.length - 2)), /truncated|delimiter/i);
});

test("should keep binary data distinct from readable original sources", () => {
  // REQ-PORTAL-008
  assert.equal(decodeText(Buffer.from("ámbito")), "ámbito");
  assert.equal(decodeText(Buffer.from([0, 1, 2])), undefined);
  assert.equal(decodeText(Buffer.from([255])), undefined);
  assert.equal(fileKind("README.md", Buffer.from("# Read")), "document");
  assert.equal(fileKind("picture.svg", Buffer.from("<svg/>")), "image");
  assert.equal(fileKind("source.NSP", Buffer.from("END")), "source");
  assert.equal(fileKind("archive.bin", Buffer.from([0, 255])), "binary");
});

test("should render source line links without executing markup", () => {
  // REQ-PORTAL-008
  const html = renderSourceLines("<script>alert(1)</script>\nEND");
  assert.match(html, /id="L1"/);
  assert.match(html, /id="L2"/);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.doesNotMatch(html, /<script>/);
});

test("should build stable locale-independent routes without hidden directories", () => {
  // REQ-PORTAL-003
  assert.equal(routeFor("00-START-HERE.md", "document"), "docs/00-START-HERE");
  assert.equal(routeFor(".github/copilot-instructions.md", "document"), "docs/dot-github/copilot-instructions");
  assert.equal(routeFor("docs/a file.md", "document"), "docs/docs/a%20file");
  assert.equal(routeFor(".gitignore", "source"), "files/dot-gitignore");
  assert.equal(categoryFor("01-archaeology/legacy-sifap/program.NSP"), "archaeology");
  assert.equal(categoryFor(".github/agents/builder.agent.md"), "copilot");
});

test("should preserve project-site prefixes and private Pages root paths", () => {
  // REQ-PORTAL-004
  assert.deepEqual(siteBase("https://example.github.io/project/"), {
    siteUrl: "https://example.github.io/project/", basePath: "/project/",
  });
  assert.equal(siteBase("https://private.pages.github.io/").basePath, "/");
  assert.throws(() => siteBase("javascript:alert(1)"), /HTTP/i);
});

test("should resolve relative repository links without escaping the source tree", () => {
  // REQ-PORTAL-004
  assert.deepEqual(resolveRepositoryTarget("docs/guide.md", "../README.md#start"), {
    kind: "file", path: "README.md", fragment: "start", query: "",
  });
  assert.deepEqual(resolveRepositoryTarget("docs/guide.md", "#section"), {
    kind: "file", path: "docs/guide.md", fragment: "section", query: "",
  });
  assert.equal(resolveRepositoryTarget("README.md", "https://example.com/").kind, "external");
  assert.equal(resolveRepositoryTarget("README.md", "javascript:alert(1)").kind, "blocked");
  assert.equal(resolveRepositoryTarget("README.md", "specs/<NNN>/spec.md").kind, "placeholder");
  assert.throws(() => resolveRepositoryTarget("README.md", "../../private.txt"), /outside/i);
});

test("should require all three editions and every logical file", () => {
  // REQ-PORTAL-002
  const make = (code, blob) => ({ code, entries: [{ path: "README.md", kind: "document", blob }] });
  const editions = [make("en", hash), make("es", otherHash), make("pt-br", "c".repeat(40))];
  assert.doesNotThrow(() => assertCoverage(editions));
  assert.throws(() => assertCoverage(editions.slice(0, 2)), /three|edition/i);
  assert.throws(() => assertCoverage([editions[0], editions[1], { code: "pt-br", entries: [] }]), /README/);
  assert.throws(() => assertCoverage([editions[0], make("es", hash), editions[2]]), /untranslated/i);
});

test("should reject a translated heading with an unchanged English document body", () => {
  // REQ-PORTAL-002
  const paragraph = "This document explains how every member of the team must read the complete instructions before implementing changes, and why preserving traceability between source files and requirements is essential.";
  assert.deepEqual(unchangedProseLines(`# Guide\n\n${paragraph}`, `# Guía\n\n${paragraph}`), [3]);
  const translated = "Este documento explica cómo cada integrante debe leer las instrucciones completas antes de implementar cambios y por qué es esencial conservar la trazabilidad entre las fuentes y los requisitos.";
  assert.deepEqual(unchangedProseLines(`# Guide\n\n${paragraph}`, `# Guía\n\n${translated}`), []);
  assert.deepEqual(unchangedProseLines(`\`\`\`text\n${paragraph}\n\`\`\``, `\`\`\`text\n${paragraph}\n\`\`\``), []);
});

test("should reject a stale portal engine in a translated branch", () => {
  // REQ-PORTAL-008, REQ-PORTAL-010
  const make = (code, blob) => ({ code, entries: [{ path: "site/src/lib/i18n.ts", kind: "source", blob }] });
  assert.doesNotThrow(() => assertCoverage([make("en", hash), make("es", hash), make("pt-br", hash)]));
  assert.throws(() => assertCoverage([make("en", hash), make("es", otherHash), make("pt-br", hash)]), /engine differs/);
});

test("should reject route collisions before publishing", () => {
  // REQ-PORTAL-010
  const make = (code, blob) => ({ code, entries: [
    { path: ".github/test.md", kind: "document", blob, route: "docs/dot-github/test" },
    { path: "dot-github/test.md", kind: "document", blob: `${blob}2`, route: "docs/dot-github/test" },
  ] });
  assert.throws(() => assertCoverage([make("en", "a"), make("es", "b"), make("pt-br", "c")]), /collision/i);
});

test("should allow only verified safe Pages visibility", () => {
  // REQ-PORTAL-009
  const pages = { public: false, build_type: "workflow", html_url: "https://private.pages.github.io/" };
  assert.equal(assertPagesAccess({ private: true }, pages), pages.html_url);
  assert.doesNotThrow(() => assertPagesAccess({ private: false }, { ...pages, public: true }));
  assert.throws(() => assertPagesAccess({ private: true }, { ...pages, public: true }), /private/i);
  assert.throws(() => assertPagesAccess({ private: true }, { ...pages, public: undefined }), /unknown|visibility/i);
  assert.throws(() => assertPagesAccess({}, pages), /unknown|visibility/i);
  assert.throws(() => assertPagesAccess({ private: true }, { ...pages, build_type: "legacy" }), /workflow/i);
});
