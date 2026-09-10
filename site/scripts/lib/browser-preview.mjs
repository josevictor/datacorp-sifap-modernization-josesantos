import { siteBase } from "./content.mjs";

/**
 * @param {Record<string, string | undefined>} environment
 * @param {string} defaultSiteUrl
 */
export function browserPreviewConfig(environment, defaultSiteUrl) {
  const port = environment.PLAYWRIGHT_PORT ?? "4321";
  if (!/^[1-9]\d{0,4}$/.test(port) || Number(port) > 65535) {
    throw new Error("PLAYWRIGHT_PORT must be a port number from 1 to 65535.");
  }
  const reuse = environment.PLAYWRIGHT_REUSE_SERVER ?? "0";
  if (!["0", "1"].includes(reuse)) {
    throw new Error("PLAYWRIGHT_REUSE_SERVER must be 0 or 1.");
  }
  if (environment.CI && reuse === "1") {
    throw new Error("CI must not reuse an existing preview server.");
  }
  const { siteUrl, basePath } = siteBase(environment.SITE_URL ?? defaultSiteUrl);
  return {
    baseURL: `http://127.0.0.1:${port}${basePath}`,
    siteUrl,
    command: `npm run preview -- --port ${port}`,
    reuseExistingServer: reuse === "1",
  };
}
