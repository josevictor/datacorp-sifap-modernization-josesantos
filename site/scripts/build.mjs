import { execFileSync } from "node:child_process";

const env = { ...process.env, ASTRO_TELEMETRY_DISABLED: "1" };
function run(command, args) {
  execFileSync(command, args, { stdio: "inherit", env });
}
run(process.execPath, ["scripts/build-content.mjs"]);
run("npm", ["exec", "--no", "--", "astro", "check"]);
run("npm", ["exec", "--no", "--", "astro", "build"]);
run("npm", ["exec", "--no", "--", "pagefind", "--site", "dist"]);
run(process.execPath, ["scripts/audit-built-site.mjs"]);
