import { useEffect, useRef, useState, type CSSProperties } from "react";
import { ArrowRightIcon } from "@storybook/icons";
import type { Locale } from "../lib/model";
import { t } from "../lib/i18n";

export interface Stage { title: string; description: string; href: string; agent: string }
const accents = ["#39B8FF", "#FFDE59", "#7ED956", "#FF3133"];
type AccentStyle = CSSProperties & { "--stage-accent": string };

export default function StageExplorer({ locale, stages }: { locale: Locale; stages: Stage[] }) {
  const [selected, setSelected] = useState(0);
  const [ready, setReady] = useState(false);
  useEffect(() => setReady(true), []);
  const buttons = useRef<Array<HTMLButtonElement | null>>([]);
  const current = stages[selected];
  if (!current) throw new Error("The learning path requires its stage guides.");
  const style: AccentStyle = { "--stage-accent": accents[selected] ?? accents[0] };
  function move(next: number) {
    const index = (next + stages.length) % stages.length;
    setSelected(index);
    buttons.current[index]?.focus();
  }
  return <div>
    <div role="tablist" aria-label={t(locale).journey} className="stage-tabs">
      {stages.map((stage, index) => {
        const accent: AccentStyle = { "--stage-accent": accents[index] ?? accents[0] };
        return <button key={stage.href} ref={(element) => { buttons.current[index] = element; }}
          id={`stage-tab-${index}`} aria-controls={`stage-panel-${index}`} role="tab"
          aria-selected={selected === index} tabIndex={selected === index ? 0 : -1}
          disabled={!ready}
          className="stage-tab" style={accent} onClick={() => setSelected(index)}
          onKeyDown={(event) => {
            if (event.key === "ArrowRight") { event.preventDefault(); move(selected + 1); }
            if (event.key === "ArrowLeft") { event.preventDefault(); move(selected - 1); }
            if (event.key === "Home") { event.preventDefault(); move(0); }
            if (event.key === "End") { event.preventDefault(); move(stages.length - 1); }
          }}>
          <span>0{index + 1} / {stage.agent}</span><strong>{stage.title}</strong>
        </button>;
      })}
    </div>
    <div role="tabpanel" id={`stage-panel-${selected}`} aria-labelledby={`stage-tab-${selected}`} className="stage-panel" style={style} key={selected} tabIndex={0}>
      <div className="stage-number" aria-hidden="true">0{selected + 1}</div>
      <div><h3>{current.title}</h3><p>{current.description}</p><a className="he-button" href={current.href}>{t(locale).start}<ArrowRightIcon size={16} aria-hidden="true" /></a></div>
    </div>
  </div>;
}
