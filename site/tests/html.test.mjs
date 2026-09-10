import assert from "node:assert/strict";
import test from "node:test";
import { inspectRenderedHtml } from "../scripts/lib/html.mjs";

test("should inspect real attributes without treating escaped source examples as links or IDs", () => {
  // REQ-PORTAL-004, REQ-PORTAL-008, REQ-PORTAL-010
  const page = inspectRenderedHtml(`<html lang="es"><body>
    <a id="real" href="/es/guide/">Guía</a>
    <pre><code>&lt;a id="real" href="/not-a-live-link/"&gt;Example&lt;/a&gt;</code></pre>
    <details data-original-markdown><summary>Fuente</summary><pre><code># Guía
&lt;a id="real" href="/not-a-live-link/"&gt;Example&lt;/a&gt;</code></pre></details>
  </body></html>`);
  assert.equal(page.language, "es");
  assert.deepEqual(page.links, [{ attribute: "href", value: "/es/guide/" }]);
  assert.deepEqual([...page.ids], ["real"]);
  assert.deepEqual(page.duplicateIds, []);
  assert.deepEqual(page.markdownSources, ['# Guía\n<a id="real" href="/not-a-live-link/">Example</a>']);
});

test("should still detect actual duplicate IDs and links in browser template content", () => {
  // REQ-PORTAL-010
  const page = inspectRenderedHtml('<div id="same"></div><div id="same"></div><template><a href="/real/">Link</a></template>');
  assert.deepEqual(page.duplicateIds, ["same"]);
  assert.deepEqual(page.links, [{ attribute: "href", value: "/real/" }]);
});
