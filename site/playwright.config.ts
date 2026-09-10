import { defineConfig } from "@playwright/test";
import { readFileSync } from "node:fs";
import { browserPreviewConfig } from "./scripts/lib/browser-preview.mjs";
import { siteBase } from "./scripts/lib/content.mjs";

const settings: unknown = JSON.parse(readFileSync(new URL("./repository.json", import.meta.url), "utf8"));
if (!settings || typeof settings !== "object" || !("pagesUrl" in settings) || typeof settings.pagesUrl !== "string") {
  throw new Error("repository.json must declare the verified Pages URL.");
}
const preview = browserPreviewConfig(process.env, settings.pagesUrl);
const liveURL = process.env.PORTAL_TEST_URL;
const baseURL = liveURL ? siteBase(liveURL).siteUrl : preview.baseURL;

export default defineConfig({
  testDir: "./tests/browser",
  timeout: 30000,
  fullyParallel: true,
  workers: 2,
  forbidOnly: Boolean(process.env.CI),
  retries: 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: { baseURL, trace: "retain-on-failure", screenshot: "only-on-failure" },
  projects: [
    { name: "desktop", use: { viewport: { width: 1440, height: 960 } } },
    { name: "mobile", use: { viewport: { width: 360, height: 800 }, isMobile: true, hasTouch: true } },
  ],
  webServer: liveURL ? undefined : {
    command: preview.command,
    url: `${baseURL}en/`,
    reuseExistingServer: preview.reuseExistingServer,
    timeout: 30000,
    env: { SITE_URL: preview.siteUrl, ASTRO_TELEMETRY_DISABLED: "1" },
  },
});
