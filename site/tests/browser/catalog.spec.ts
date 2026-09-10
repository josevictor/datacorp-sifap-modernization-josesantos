import { expect, test } from "@playwright/test";
import { fileURLToPath } from "node:url";
import { getCatalog, getEdition } from "../../src/lib/catalog";
import { localeCodes } from "../../src/lib/model";
import { readSnapshot, repositorySlug } from "../../scripts/lib/git.mjs";

const repositoryRoot = fileURLToPath(new URL("../../../", import.meta.url));
const repository = repositorySlug(repositoryRoot);
interface SourceSnapshot {
  files: Array<{ path: string; blob: string }>;
  blobs: Map<string, Buffer>;
}

function verifiedCatalog() {
  const catalog = getCatalog();
  expect(catalog.repository).toBe(repository);
  for (const edition of catalog.editions) {
    expect(edition.commit).toMatch(/^[a-f0-9]{40,64}$/);
    expect(edition.commit).not.toMatch(/^0+$/);
    const snapshot: SourceSnapshot = readSnapshot(repositoryRoot, edition.commit);
    expect(edition.entries.map(({ path }) => path).sort())
      .toEqual(snapshot.files.map(({ path }) => path).sort());
    const blobs = new Map(snapshot.files.map(({ path, blob }) => [path, blob]));
    for (const entry of edition.entries) expect(entry.blob).toBe(blobs.get(entry.path));
  }
  return catalog;
}

test("rejects a demo or different repository before accepting source coverage", async ({ page }) => {
  // REQ-PORTAL-001, REQ-PORTAL-002, REQ-PORTAL-004, REQ-PORTAL-010
  await page.goto("en/");
  await expect(page.locator('.portal-nav a[href^="https://github.com/"]'),
    "The served repository must match the source repository; demo content cannot validate this portal.")
    .toHaveAttribute("href", `https://github.com/${repository}`);
  const catalog = verifiedCatalog();
  for (const edition of catalog.editions) {
    await page.goto(`${edition.code}/library/`);
    await expect(page.locator(".collection-count [role=status]"))
      .toContainText(`${edition.entries.length} / ${edition.entries.length}`);
  }
});

test("serves full Copilot instructions and original legacy bytes in each real edition", async ({ page, request }) => {
  // REQ-PORTAL-001, REQ-PORTAL-002, REQ-PORTAL-003, REQ-PORTAL-004, REQ-PORTAL-008
  const catalog = verifiedCatalog();
  const english = getEdition("en");
  const technical = english.entries.find(({ kind, extension }) => kind === "source" && extension === "nsp");
  if (!technical) throw new Error("The complete repository must include the original Natural sources.");
  for (const path of [".github/copilot-instructions.md", technical.path]) {
    const initial = english.entries.find((entry) => entry.path === path);
    if (!initial) throw new Error(`Missing required source document: ${path}`);
    await page.goto(initial.href);
    for (const locale of localeCodes) {
      const edition = getEdition(locale);
      const entry = edition.entries.find((candidate) => candidate.path === path);
      if (!entry) throw new Error(`Missing ${locale} counterpart: ${path}`);
      await page.locator(`.language-picker a[hreflang="${locale}"]`).click();
      expect(new URL(page.url()).pathname).toBe(entry.href);
      await expect(page.locator("html")).toHaveAttribute("lang", locale === "pt-br" ? "pt-BR" : locale);
      await expect(page.locator(".doc-actions a").first()).toHaveAttribute("href", entry.sourceHref);
      expect(entry.sourceHref).toContain(`/${catalog.repository}/blob/${edition.commit}/`);
      const snapshot: SourceSnapshot = readSnapshot(repositoryRoot, edition.commit);
      const original = snapshot.blobs.get(entry.blob);
      if (!original) throw new Error(`Missing original Git blob: ${path}`);
      const response = await request.get(new URL(entry.downloadHref, page.url()).href);
      expect(response.status()).toBe(200);
      expect(await response.body()).toEqual(original);
      if (entry.kind === "document") {
        expect(await page.locator("[data-original-markdown] code").textContent()).toBe(original.toString("utf8"));
      }
    }
  }
});
