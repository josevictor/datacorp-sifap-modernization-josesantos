import { useEffect, useRef, useState } from "react";
import { CloseIcon, MoonIcon, SearchIcon, SunIcon } from "@storybook/icons";
import type { Locale } from "../lib/model";
import { t } from "../lib/i18n";

interface SearchData {
  url: string;
  excerpt: string;
  meta: { title?: string };
}
interface Pagefind {
  search: (query: string) => Promise<{ results: Array<{ id: string; data: () => Promise<SearchData> }> }>;
}
interface Result { id: string; url: string; title: string; excerpt: string }

export default function HeaderTools({ locale, basePath }: { locale: Locale; basePath: string }) {
  const words = t(locale);
  const [dark, setDark] = useState(false);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Result[]>([]);
  const [state, setState] = useState<"idle" | "loading" | "ready" | "error">("idle");
  const [notice, setNotice] = useState("");
  const dialog = useRef<HTMLDialogElement>(null);
  const trigger = useRef<HTMLButtonElement>(null);
  const index = useRef<Promise<Pagefind> | undefined>(undefined);

  useEffect(() => {
    let preferred = window.matchMedia("(prefers-color-scheme: dark)").matches;
    try {
      const saved = localStorage.getItem("sifap-theme");
      if (saved === "dark" || saved === "light") preferred = saved === "dark";
    } catch (error) {
      if (!(error instanceof DOMException)) throw error;
      setNotice(words.preferencesError);
    }
    document.documentElement.dataset.heTheme = preferred ? "dark" : "light";
    setDark(preferred);
    const shortcut = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setOpen(true);
      }
    };
    window.addEventListener("keydown", shortcut);
    return () => window.removeEventListener("keydown", shortcut);
  }, [words.preferencesError]);

  useEffect(() => {
    if (open && !dialog.current?.open) dialog.current?.showModal();
    if (!open && dialog.current?.open) dialog.current.close();
  }, [open]);

  useEffect(() => {
    if (!open || query.trim().length < 2) {
      setState("idle");
      setResults([]);
      return;
    }
    let active = true;
    setState("loading");
    const timer = setTimeout(async () => {
      try {
        index.current ??= import(/* @vite-ignore */ `${basePath}pagefind/pagefind.js`);
        const pagefind = await index.current;
        const response = await pagefind.search(query);
        const rows = await Promise.all(response.results.slice(0, 14).map(async (result) => {
          const data = await result.data();
          const url = new URL(data.url, window.location.origin);
          const excerpt = new DOMParser().parseFromString(data.excerpt, "text/html").body.textContent ?? "";
          return { id: result.id, url: url.pathname + url.hash, title: data.meta.title ?? url.pathname, excerpt };
        }));
        if (active) {
          setResults(rows.filter((row) => row.url.startsWith(`${basePath}${locale}/`)));
          setState("ready");
        }
      } catch (error) {
        console.error("Local documentation search failed.", error);
        if (active) setState("error");
      }
    }, 180);
    return () => { active = false; clearTimeout(timer); };
  }, [query, open, basePath, locale]);

  function toggleTheme() {
    const next = !dark;
    setDark(next);
    document.documentElement.dataset.heTheme = next ? "dark" : "light";
    try {
      localStorage.setItem("sifap-theme", next ? "dark" : "light");
      setNotice("");
    } catch (error) {
      if (!(error instanceof DOMException)) throw error;
      setNotice(words.preferencesError);
    }
  }

  return <div className="header-island">
    <button ref={trigger} className="icon-button search-trigger" type="button" aria-label={words.searchHint} aria-keyshortcuts="Control+k Meta+k" onClick={() => setOpen(true)}>
      <SearchIcon size={18} aria-hidden="true" /><span className="search-label">{words.search} <kbd>Ctrl / ⌘ K</kbd></span>
    </button>
    <button className="icon-button" type="button" onClick={toggleTheme} aria-label={dark ? words.light : words.dark} aria-pressed={dark}>
      {dark ? <SunIcon size={18} aria-hidden="true" /> : <MoonIcon size={18} aria-hidden="true" />}
    </button>
    <span className="sr-only" role="status">{notice}</span>
    <dialog ref={dialog} className="search-dialog" aria-label={words.searchHint}
      onKeyDown={(event) => {
        if (event.key === "Escape") {
          event.preventDefault();
          event.stopPropagation();
          setOpen(false);
        }
      }}
      onCancel={() => setOpen(false)}
      onClose={() => { setOpen(false); trigger.current?.focus(); }}
      onClick={(event) => { if (event.target === event.currentTarget) setOpen(false); }}>
      <header>
        <SearchIcon size={20} aria-hidden="true" />
        <input type="search" aria-label={words.searchHint} placeholder={words.searchHint} value={query} autoFocus onChange={(event) => setQuery(event.target.value)} />
        <button className="icon-button" type="button" onClick={() => setOpen(false)} aria-label={words.close}><CloseIcon size={18} /></button>
      </header>
      <div className="search-content">
        <p role="status">{state === "loading" ? words.loading : state === "error" ? words.searchError :
          state === "idle" ? words.searchPrompt : results.length ? `${results.length} ${words.results}` : words.noResults}</p>
        {state === "error" && <a href={`${basePath}${locale}/library/`}>{words.library}</a>}
        <ul className="search-results">
          {results.map((result) => <li key={result.id}><a href={result.url}><strong>{result.title}</strong><p>{result.excerpt}</p></a></li>)}
        </ul>
      </div>
    </dialog>
  </div>;
}
