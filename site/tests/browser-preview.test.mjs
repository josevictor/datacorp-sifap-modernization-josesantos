import assert from "node:assert/strict";
import test from "node:test";
import { browserPreviewConfig } from "../scripts/lib/browser-preview.mjs";

test("should use the repository Pages base path and an isolated browser server by default", () => {
  // REQ-PORTAL-004, REQ-PORTAL-010
  const preview = browserPreviewConfig({}, "https://private.pages.github.io/");
  assert.equal(preview.baseURL, "http://127.0.0.1:4321/");
  assert.equal(preview.reuseExistingServer, false);
  assert.equal(preview.siteUrl, "https://private.pages.github.io/");
});

test("should support a separate port without changing a project-site prefix", () => {
  // REQ-PORTAL-004, REQ-PORTAL-010
  const preview = browserPreviewConfig({
    PLAYWRIGHT_PORT: "4333",
    SITE_URL: "https://example.github.io/team-kit/",
  }, "https://private.pages.github.io/");
  assert.equal(preview.baseURL, "http://127.0.0.1:4333/team-kit/");
  assert.equal(preview.command, "npm run preview -- --port 4333");
});

test("should require explicit local opt-in before reusing any running preview", () => {
  // REQ-PORTAL-010
  const preview = browserPreviewConfig({ PLAYWRIGHT_REUSE_SERVER: "1" }, "https://example.com/");
  assert.equal(preview.reuseExistingServer, true);
  assert.throws(() => browserPreviewConfig({
    CI: "true", PLAYWRIGHT_REUSE_SERVER: "1",
  }, "https://example.com/"), /CI.*reuse|reuse.*CI/i);
  assert.throws(() => browserPreviewConfig({
    PLAYWRIGHT_REUSE_SERVER: "false",
  }, "https://example.com/"), /0 or 1/);
});

test("should reject invalid ports and unsafe site URLs before starting a server", () => {
  // REQ-PORTAL-004, REQ-PORTAL-010
  for (const port of ["", "0", "65536", "-1", "4.5", "1e3", "4321;echo", " 4321"]) {
    assert.throws(() => browserPreviewConfig({ PLAYWRIGHT_PORT: port }, "https://example.com/"), /port/i);
  }
  assert.throws(() => browserPreviewConfig({ SITE_URL: "file:///tmp/" }, "https://example.com/"), /HTTP/i);
  assert.throws(() => browserPreviewConfig({ SITE_URL: "https://user:pass@example.com/" }, "https://example.com/"),
    /credentials/i);
});
