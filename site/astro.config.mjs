import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import { readFileSync } from "node:fs";
import { siteBase } from "./scripts/lib/content.mjs";

if (process.env.GITHUB_ACTIONS === "true" && !process.env.SITE_URL) {
  throw new Error("SITE_URL must come from the verified GitHub Pages configuration.");
}

const settings = JSON.parse(readFileSync(new URL("./repository.json", import.meta.url), "utf8"));
if (typeof settings.pagesUrl !== "string") {
  throw new Error("repository.json must declare the Pages URL.");
}
const { siteUrl, basePath } = siteBase(process.env.SITE_URL ?? settings.pagesUrl);
const url = new URL(siteUrl);

export default defineConfig({
  integrations: [react()],
  site: url.origin,
  base: basePath,
  output: "static",
  trailingSlash: "always",
  build: { format: "directory" },
  vite: {
    server: { strictPort: true },
    preview: { strictPort: true },
  },
});
