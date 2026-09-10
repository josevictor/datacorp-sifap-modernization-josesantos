import { parse } from "parse5";

export function inspectRenderedHtml(html) {
  const result = { language: undefined, ids: new Set(), duplicateIds: [], links: [], markdownSources: [] };
  function text(node) {
    if (node.nodeName === "#text") return node.value;
    return (node.childNodes ?? []).map(text).join("");
  }
  function firstCode(node) {
    if (node.tagName === "code") return node;
    for (const child of node.childNodes ?? []) {
      const match = firstCode(child);
      if (match) return match;
    }
  }
  function visit(node) {
    const attributes = new Map((node.attrs ?? []).map((attribute) => [attribute.name, attribute.value]));
    if (node.tagName === "html") result.language = attributes.get("lang");
    const id = attributes.get("id");
    if (id !== undefined) {
      if (result.ids.has(id)) result.duplicateIds.push(id);
      result.ids.add(id);
    }
    for (const name of ["href", "src"]) {
      if (attributes.has(name)) result.links.push({ attribute: name, value: attributes.get(name) });
    }
    if (attributes.has("data-original-markdown")) {
      const code = firstCode(node);
      if (code) result.markdownSources.push(text(code));
    }
    for (const child of node.childNodes ?? []) visit(child);
    if (node.content) visit(node.content);
  }
  visit(parse(html));
  return result;
}
