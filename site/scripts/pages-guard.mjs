import { execFileSync } from "node:child_process";
import { appendFileSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { assertPagesAccess } from "./lib/content.mjs";

const siteRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const settings = JSON.parse(readFileSync(resolve(siteRoot, "repository.json"), "utf8"));
const name = process.env.GITHUB_REPOSITORY ?? settings.repository;
if (!/^[\w.-]+\/[\w.-]+$/.test(name) || name !== settings.repository) {
  throw new Error("The deployment repository does not match the portal configuration.");
}
const api = (path) => JSON.parse(execFileSync("gh", ["api", path], { encoding: "utf8" }));
const repository = api(`repos/${name}`);
const pages = api(`repos/${name}/pages`);
const siteUrl = assertPagesAccess(repository, pages);
if (process.env.EXPECTED_SITE_URL && process.env.EXPECTED_SITE_URL !== siteUrl) {
  throw new Error("Pages URL changed after the build; rebuild before publishing.");
}
if (process.env.GITHUB_OUTPUT) appendFileSync(process.env.GITHUB_OUTPUT, `site_url=${siteUrl}\n`);
console.log(JSON.stringify({ repository: name, privateRepository: repository.private, publicPages: pages.public, siteUrl }));
