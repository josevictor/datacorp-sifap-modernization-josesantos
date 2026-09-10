import { execFileSync } from "node:child_process";
import { parseBatch, parseTree } from "./content.mjs";

export function git(cwd, args, options = {}) {
  return execFileSync("git", args, {
    cwd,
    maxBuffer: 256 * 1024 * 1024,
    ...options,
  });
}

export function resolveCommit(cwd, ref) {
  if (typeof ref !== "string" || !ref || ref.startsWith("-") || /[\0\r\n]/.test(ref)) {
    throw new Error("Invalid content reference.");
  }
  const commit = git(cwd, ["rev-parse", "--verify", "--end-of-options", `${ref}^{commit}`], {
    encoding: "utf8",
  }).trim();
  if (!/^[a-f0-9]{40,64}$/.test(commit)) throw new Error(`Could not resolve ${ref} to a commit.`);
  return commit;
}

export function readSnapshot(cwd, ref) {
  const commit = resolveCommit(cwd, ref);
  const files = parseTree(git(cwd, ["ls-tree", "-r", "-l", "-z", commit], { encoding: "utf8" }));
  const ids = [...new Set(files.map((file) => file.blob))];
  const blobs = parseBatch(git(cwd, ["cat-file", "--batch"], { input: `${ids.join("\n")}\n` }));
  for (const file of files) {
    const bytes = blobs.get(file.blob);
    if (!bytes || bytes.length !== file.bytes) throw new Error(`Blob size mismatch: ${file.path}`);
  }
  return { commit, files, blobs };
}

export function repositorySlug(cwd) {
  if (process.env.GITHUB_REPOSITORY) {
    if (!/^[\w.-]+\/[\w.-]+$/.test(process.env.GITHUB_REPOSITORY)) {
      throw new Error("Invalid GITHUB_REPOSITORY.");
    }
    return process.env.GITHUB_REPOSITORY;
  }
  const origin = git(cwd, ["remote", "get-url", "origin"], { encoding: "utf8" }).trim();
  const match = origin.match(/^(?:https:\/\/github\.com\/|git@github\.com:)([\w.-]+\/[\w.-]+?)(?:\.git)?$/);
  if (!match) throw new Error("The portal requires an identifiable GitHub origin.");
  return match[1];
}
