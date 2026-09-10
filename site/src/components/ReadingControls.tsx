import { useEffect, useState } from "react";
import { CheckIcon, CopyIcon } from "@storybook/icons";
import { t } from "../lib/i18n";
import type { Locale } from "../lib/model";

export default function ReadingControls({ locale, repository, path, downloadHref }: { locale: Locale; repository: string; path: string; downloadHref: string }) {
  const words = t(locale);
  const key = `sifap-read:${repository}:${path}`;
  const [read, setRead] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  useEffect(() => {
    try { setRead(localStorage.getItem(key) === "true"); }
    catch (error) { if (!(error instanceof DOMException)) throw error; setStatus(words.preferencesError); }
    const update = () => {
      const range = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(range > 0 ? Math.min(100, Math.max(0, (window.scrollY / range) * 100)) : 100);
    };
    update();
    window.addEventListener("scroll", update, { passive: true });
    return () => window.removeEventListener("scroll", update);
  }, [key, words.preferencesError]);

  function toggleRead() {
    const next = !read;
    setRead(next);
    try { localStorage.setItem(key, String(next)); setStatus(""); }
    catch (error) { if (!(error instanceof DOMException)) throw error; setStatus(words.preferencesError); }
  }
  async function copy() {
    try {
      const response = await fetch(downloadHref);
      if (!response.ok) throw new Error(`Source download failed: ${response.status}`);
      await navigator.clipboard.writeText(await response.text());
      setStatus(words.copied);
    } catch (error) {
      console.error("Source copy failed.", error);
      setStatus(words.copyError);
    }
  }
  return <div className="reading-controls">
    <div className="reading-progress" style={{ width: `${progress}%` }} role="progressbar" aria-label={words.reading} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(progress)} />
    <button className="he-button" type="button" aria-pressed={read} onClick={toggleRead}><CheckIcon size={14} aria-hidden="true" />{read ? words.markedRead : words.markRead}</button>
    <button className="he-button" type="button" onClick={copy}><CopyIcon size={14} aria-hidden="true" />{words.copy}</button>
    <span className="local-status" role="status">{status}</span>
  </div>;
}
