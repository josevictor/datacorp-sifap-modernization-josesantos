import { escapeHtml } from "./content.mjs";

function addAlias(entry, from, to) {
  if (from === to || entry.anchors.includes(from)) return;
  const marker = `id="${escapeHtml(to)}"`;
  const position = entry.html.indexOf(marker);
  if (position < 0) throw new Error(`Cannot place heading alias in ${entry.path}: ${to}`);
  const opening = entry.html.lastIndexOf("<", position);
  entry.html = `${entry.html.slice(0, opening)}<span id="${escapeHtml(from)}" class="heading-alias"></span>${entry.html.slice(opening)}`;
  entry.anchors.push(from);
}

export function addEquivalentHeadingAliases(editions) {
  const english = editions.find((edition) => edition.code === "en");
  if (!english) throw new Error("English edition is required for heading alignment.");
  let aliases = 0;
  for (const source of english.entries.filter((entry) => entry.kind === "document")) {
    const peers = editions.map((edition) => edition.entries.find((entry) => entry.path === source.path))
      .filter((entry) => entry?.kind === "document");
    const compatible = peers.filter((entry) => entry.headings.length === source.headings.length &&
      entry.headings.every((heading, index) => heading.depth === source.headings[index].depth));
    for (const target of compatible) {
      const before = target.anchors.length;
      for (const peer of compatible) {
        if (peer.anchors[0] && target.anchors[0]) addAlias(target, peer.anchors[0], target.anchors[0]);
        for (const [index, heading] of peer.headings.entries()) {
          addAlias(target, heading.slug, target.headings[index].slug);
        }
      }
      aliases += target.anchors.length - before;
    }
  }
  return aliases;
}

export function unresolvedFragments(editions, references) {
  const entries = new Map(editions.map((edition) =>
    [edition.code, new Map(edition.entries.map((entry) => [entry.path, entry]))]));
  const missing = [];
  for (const link of references) {
    if (!link.fragment) continue;
    const target = entries.get(link.locale)?.get(link.target);
    if (!target) {
      missing.push({ ...link, reason: "missing-file" });
      continue;
    }
    if (target.kind === "document" && !target.anchors.includes(`doc-${link.fragment}`)) {
      missing.push({ ...link, reason: "missing-heading" });
    } else if (target.kind === "source" &&
      (!/^L\d+$/.test(link.fragment) || Number(link.fragment.slice(1)) < 1 || Number(link.fragment.slice(1)) > target.lines)) {
      missing.push({ ...link, reason: "missing-source-line" });
    }
  }
  return missing;
}
