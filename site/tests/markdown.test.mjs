import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { renderDocument } from "../scripts/lib/markdown.mjs";

function context() {
  const entries = [
    { path: "README.md", kind: "document", href: "/kit/en/docs/README/", downloadHref: "/kit/raw/readme.bin" },
    { path: "docs/guide.md", kind: "document", href: "/kit/en/docs/docs/guide/", downloadHref: "/kit/raw/guide.bin" },
    { path: "assets/figure.svg", kind: "image", href: "/kit/en/files/assets/figure.svg/", mediaHref: "/kit/content-media/figure.svg", downloadHref: "/kit/raw/figure.bin" },
  ];
  return {
    locale: "en",
    repository: "example/kit",
    sourcePath: "docs/guide.md",
    byPath: new Map(entries.map((entry) => [entry.path, entry])),
    editions: [],
    references: [],
    unresolved: [],
    placeholders: [],
  };
}

test("should render all Markdown with source metadata and safe link destinations", async () => {
  // REQ-PORTAL-001, REQ-PORTAL-004
  const ctx = context();
  const result = await renderDocument("---\nname: guide\n---\n# Guide\n\nSee [home](../README.md#start).\n\n## Detail\n\n![Diagram](../assets/figure.svg)\n\n```natural\nEND\n```\n", ctx);
  assert.equal(result.title, "Guide");
  assert.match(result.html, /name: guide/);
  assert.match(result.html, /\/kit\/en\/docs\/README\/#doc-start/);
  assert.match(result.html, /\/kit\/content-media\/figure\.svg/);
  assert.equal(result.headings.some((heading) => heading.slug === "doc-detail"), true);
  assert.equal(ctx.unresolved.length, 0);
});

test("should remove executable HTML while retaining readable content", async () => {
  // REQ-PORTAL-008
  const ctx = context();
  const result = await renderDocument('# Safe\n\n<script>alert(1)</script>\n\n<img src="x" onerror="alert(2)">\n\n<details><summary>More</summary>Text</details>', ctx);
  assert.doesNotMatch(result.html, /<script|onerror=/);
  assert.match(result.html, /<details>/);
  assert.match(result.html, /Text/);
});

test("should retain technical examples and render badges without remote tracking", async () => {
  // REQ-PORTAL-005, REQ-PORTAL-008
  const result = await renderDocument("# Guide\n\n![Stage: one](https://img.shields.io/badge/stage-one-blue)\n\n```mermaid\ngraph LR\nA-->B\n```", context());
  assert.match(result.html, /Stage: one/);
  assert.doesNotMatch(result.html, /<img[^>]+shields\.io/);
  assert.match(result.html, /language-mermaid/);
});

test("should keep all three repository editions inside the same navigation table", async () => {
  // REQ-PORTAL-002
  const readme = readFileSync(new URL("../../README.md", import.meta.url), "utf8");
  const section = readme.split(/\n---\n/).find((block) =>
    ["/tree/main", "/tree/espanol", "/tree/portugues-br"].every((target) => block.includes(target)));
  assert.ok(section, "The README must expose all three repository language editions.");
  const result = await renderDocument(section, context());
  const table = result.html.match(/<table>[\s\S]*?<\/table>/)?.[0];
  assert.ok(table);
  assert.equal((table.match(/<tr>/g) ?? []).length, 4);
  for (const label of ["English", "Español", "Português (BR)"]) assert.ok(table.includes(label));
});

test("should use the document introduction rather than navigation as its catalog description", async () => {
  // REQ-PORTAL-005
  const introduction = "This introduction explains how to follow the complete modernization guide.";
  const source = `# Guide\n\n> **Path:** Repository documentation and a long navigation breadcrumb.\n\n${introduction}\n`;
  const result = await renderDocument(source, context());
  assert.equal(result.description, introduction);
});
