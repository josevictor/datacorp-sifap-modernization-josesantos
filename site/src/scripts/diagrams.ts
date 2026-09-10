import { isLocale } from "../lib/model";
import { t } from "../lib/i18n";

export async function renderDiagrams(): Promise<void> {
  const content = document.querySelector<HTMLElement>(".doc-content[data-locale]");
  const locale = content?.dataset.locale;
  if (!content || !isLocale(locale)) return;
  const blocks = Array.from(content.querySelectorAll<HTMLElement>("pre > code.language-mermaid"));
  if (!blocks.length) return;
  const words = t(locale);
  const { default: mermaid } = await import("mermaid");
  mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "neutral", fontFamily: "Inter, sans-serif", suppressErrorRendering: true });
  for (const [index, block] of blocks.entries()) {
    const pre = block.parentElement;
    if (!pre) continue;
    const details = document.createElement("details");
    const summary = document.createElement("summary");
    summary.textContent = words.viewSource;
    details.append(summary);
    pre.before(details);
    details.append(pre);
    const output = document.createElement("div");
    output.className = "diagram-output";
    details.before(output);
    try {
      const result = await mermaid.render(`sifap-diagram-${index}`, block.textContent ?? "");
      output.innerHTML = result.svg;
    } catch (error) {
      console.error("Repository diagram could not be rendered.", error);
      output.textContent = words.diagramError;
      output.setAttribute("role", "status");
      details.open = true;
    }
  }
}
