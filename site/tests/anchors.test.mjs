import assert from "node:assert/strict";
import test from "node:test";
import { addEquivalentHeadingAliases, unresolvedFragments } from "../scripts/lib/anchors.mjs";

function entry(title, section, depth = 2) {
  return { path: "README.md", kind: "document", html: `<span id="doc-${title}"></span><h${depth} id="doc-${section}">${section}</h${depth}>`,
    headings: [{ depth, slug: `doc-${section}`, text: section }], anchors: [`doc-${title}`, `doc-${section}`] };
}

test("should preserve corresponding heading links across translated editions", () => {
  // REQ-PORTAL-003, REQ-PORTAL-004
  const editions = [
    { code: "en", entries: [entry("guide", "start")] },
    { code: "es", entries: [entry("guia", "comenzar")] },
    { code: "pt-br", entries: [entry("guia", "comecar")] },
  ];
  assert.equal(addEquivalentHeadingAliases(editions), 9);
  for (const edition of editions) {
    assert.ok(edition.entries[0].anchors.includes("doc-start"));
    assert.ok(edition.entries[0].anchors.includes("doc-comenzar"));
    assert.ok(edition.entries[0].anchors.includes("doc-comecar"));
  }
  assert.deepEqual(unresolvedFragments(editions, [{ locale: "es", target: "README.md", fragment: "start" }]), []);
  assert.equal(unresolvedFragments(editions, [{ locale: "es", target: "README.md", fragment: "absent" }]).length, 1);
});

test("should not guess heading counterparts with incompatible document structure", () => {
  // REQ-PORTAL-004, REQ-PORTAL-010
  const editions = [
    { code: "en", entries: [entry("guide", "start")] },
    { code: "es", entries: [entry("guia", "comenzar", 3)] },
  ];
  assert.equal(addEquivalentHeadingAliases(editions), 0);
  assert.equal(unresolvedFragments(editions, [{ locale: "es", target: "README.md", fragment: "start" }]).length, 1);
});
