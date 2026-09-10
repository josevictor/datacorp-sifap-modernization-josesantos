import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import type { Catalog, Edition, Entry, Locale } from "./model";
import { categoryCodes } from "./model";

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isEntry(value: unknown): value is Entry {
  if (!isObject(value)) return false;
  const strings = ["id", "path", "title", "description", "category", "extension", "blob", "route", "href", "sourceHref", "downloadHref"];
  return strings.every((key) => typeof value[key] === "string") &&
    categoryCodes.some((category) => category === value.category) &&
    ["document", "source", "image", "binary"].includes(String(value.kind)) &&
    typeof value.bytes === "number" && typeof value.lines === "number" &&
    Array.isArray(value.headings) &&
    value.headings.every((heading: unknown) => isObject(heading) &&
      typeof heading.depth === "number" && typeof heading.slug === "string" && typeof heading.text === "string") &&
    (value.kind === "document" ? typeof value.html === "string" : value.html === undefined || typeof value.html === "string") &&
    (value.text === undefined || typeof value.text === "string") &&
    (value.mediaHref === undefined || typeof value.mediaHref === "string");
}

function isEdition(value: unknown): value is Edition {
  return isObject(value) &&
    ["en", "es", "pt-br"].includes(String(value.code)) &&
    typeof value.label === "string" && typeof value.branch === "string" &&
    typeof value.commit === "string" && Array.isArray(value.entries) &&
    value.entries.every(isEntry);
}

function isCatalog(value: unknown): value is Catalog {
  return isObject(value) && value.schemaVersion === 1 &&
    typeof value.repository === "string" &&
    (value.audience === "team" || value.audience === "instructor") &&
    typeof value.siteUrl === "string" && typeof value.basePath === "string" &&
    typeof value.generatedAt === "string" &&
    Array.isArray(value.editions) && value.editions.every(isEdition);
}

let cached: Catalog | undefined;

export function getCatalog(): Catalog {
  if (cached) return cached;
  const value: unknown = JSON.parse(readFileSync(resolve(process.cwd(), ".generated/catalog.json"), "utf8"));
  if (!isCatalog(value) || value.editions.length !== 3 ||
      new Set(value.editions.map((edition) => edition.code)).size !== 3) {
    throw new Error("Invalid or incomplete portal catalog. Run npm run prepare:content.");
  }
  cached = value;
  return cached;
}

export function getEdition(locale: Locale): Edition {
  const edition = getCatalog().editions.find((item) => item.code === locale);
  if (!edition) throw new Error(`Missing required edition: ${locale}`);
  return edition;
}

export function getCatalogItems(locale: Locale): Array<Pick<Entry, "id" | "path" | "title" | "description" | "kind" | "category" | "href">> {
  const starts = ["00-START-HERE.md", "00-SETUP.md", "00-TEAM-FLOW.md", "00-GIT-WORKFLOW.md", "README.md"];
  const rank = (entry: Entry) => {
    const start = starts.indexOf(entry.path);
    if (start >= 0) return start;
    return entry.kind === "document" ? 10 : 20;
  };
  return getEdition(locale).entries.toSorted((left, right) =>
    rank(left) - rank(right) || left.path.localeCompare(right.path))
    .map(({ id, path, title, description, kind, category, href }) => ({ id, path, title, description, kind, category, href }));
}

export function siteHref(locale: Locale, route = ""): string {
  const base = getCatalog().basePath;
  return `${base}${locale}/${route.replace(/^\/+|\/+$/g, "")}${route ? "/" : ""}`;
}

export function counterpartHref(locale: Locale, path?: string): string {
  if (!path) return siteHref(locale);
  const entry = getEdition(locale).entries.find((item) => item.path === path);
  if (!entry) throw new Error(`Missing ${locale} counterpart for ${path}`);
  return entry.href;
}
