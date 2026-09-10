import { useEffect, useMemo, useState } from "react";
import { ArrowRightIcon, SearchIcon } from "@storybook/icons";
import type { Category, Entry, Locale } from "../lib/model";
import { categories, t } from "../lib/i18n";

export type CatalogItem = Pick<Entry, "id" | "path" | "title" | "description" | "kind" | "category" | "href">;
const normalize = (value: string) => value.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase();

export default function Collection({ locale, items, initialLimit = 24 }: { locale: Locale; items: CatalogItem[]; initialLimit?: number }) {
  const words = t(locale);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [kind, setKind] = useState("");
  const [prefix, setPrefix] = useState("");
  const [limit, setLimit] = useState(initialLimit);
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setPrefix(params.get("path") ?? "");
    setQuery(params.get("q") ?? "");
  }, []);
  const available = useMemo(() => [...new Set(items.map((item) => item.category))], [items]);
  const filtered = useMemo(() => items.filter((item) =>
    (!category || item.category === category) && (!kind || item.kind === kind) &&
    (!prefix || item.path.startsWith(prefix)) &&
    normalize(`${item.title} ${item.path} ${item.description}`).includes(normalize(query))),
  [items, category, kind, prefix, query]);
  const labels = { document: words.document, source: words.source, image: words.image, binary: words.binary };
  function reset() { setQuery(""); setCategory(""); setKind(""); setPrefix(""); setLimit(initialLimit); }

  return <div className="collection">
    <div className="collection-toolbar">
      <label><span className="he-field-label"><SearchIcon size={14} aria-hidden="true" /> {words.filter}</span>
        <input className="he-field" type="search" value={query} placeholder={words.filterPlaceholder} onChange={(event) => { setQuery(event.target.value); setLimit(initialLimit); }} />
      </label>
      <label><span className="he-field-label">{words.category}</span>
        <select className="he-field" value={category} onChange={(event) => { setCategory(event.target.value); setLimit(initialLimit); }}>
          <option value="">{words.all}</option>
          {available.map((value: Category) => <option key={value} value={value}>{categories[locale][value]}</option>)}
        </select>
      </label>
      <label><span className="he-field-label">{words.kind}</span>
        <select className="he-field" value={kind} onChange={(event) => { setKind(event.target.value); setLimit(initialLimit); }}>
          <option value="">{words.all}</option>
          {Object.entries(labels).map(([value, label]) => <option value={value} key={value}>{label}</option>)}
        </select>
      </label>
    </div>
    <div className="collection-count">
      <p className="he-results" role="status">{filtered.length} / {items.length} {words.results}{prefix && <> · <code>{prefix}</code></>}</p>
      <button className="he-button he-button--quiet" onClick={reset} type="button">{words.clear}</button>
    </div>
    {filtered.length === 0 && <p className="he-empty">{words.noResults}</p>}
    <div className="collection-grid">
      {filtered.slice(0, limit).map((item) => <a className="collection-card" href={item.href} key={item.id}>
        <div className="card-type"><span>{categories[locale][item.category]}</span><ArrowRightIcon size={16} aria-hidden="true" /></div>
        <h3>{item.title}</h3><p>{item.description || labels[item.kind]}</p><code>{item.path}</code>
      </a>)}
    </div>
    {limit < filtered.length && <div className="load-more"><button type="button" className="he-button" onClick={() => setLimit((value) => value + 24)}>{words.showMore} · {Math.min(24, filtered.length - limit)}</button></div>}
  </div>;
}
