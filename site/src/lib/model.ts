export const localeCodes = ["en", "es", "pt-br"] as const;
export type Locale = (typeof localeCodes)[number];
export type EntryKind = "document" | "source" | "image" | "binary";
export const categoryCodes = [
  "start", "archaeology", "specification", "implementation", "evolution",
  "personas", "agents", "concepts", "cheat-sheets", "documentation",
  "copilot", "infrastructure", "portal", "repository",
] as const;
export type Category = (typeof categoryCodes)[number];

export interface Heading {
  depth: number;
  slug: string;
  text: string;
}

export interface Entry {
  id: string;
  path: string;
  title: string;
  description: string;
  kind: EntryKind;
  category: Category;
  extension: string;
  bytes: number;
  lines: number;
  blob: string;
  route: string;
  href: string;
  sourceHref: string;
  downloadHref: string;
  mediaHref?: string;
  html?: string;
  text?: string;
  headings: Heading[];
}

export interface Edition {
  code: Locale;
  label: string;
  branch: string;
  commit: string;
  entries: Entry[];
}

export interface Catalog {
  schemaVersion: 1;
  repository: string;
  audience: "team" | "instructor";
  siteUrl: string;
  basePath: string;
  generatedAt: string;
  editions: Edition[];
}

export function isLocale(value: string | undefined): value is Locale {
  return value === "en" || value === "es" || value === "pt-br";
}
