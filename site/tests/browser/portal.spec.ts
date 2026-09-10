import { expect, test } from "@playwright/test";
import { t } from "../../src/lib/i18n";

test("lets readers choose a language at the root without a forced redirect", async ({ page }) => {
  // REQ-PORTAL-002, REQ-PORTAL-006
  await page.goto("./");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Choose your language.");
  await expect(page.locator('meta[http-equiv="refresh"]')).toHaveCount(0);
  await expect(page.getByRole("navigation", { name: "Choose a complete edition" }).getByRole("link")).toHaveCount(3);
});

test("keeps all languages visible and every viewport within its width", async ({ page }) => {
  // REQ-PORTAL-002, REQ-PORTAL-006
  for (const locale of ["en", "es", "pt-br"] as const) {
    await page.goto(`${locale}/`);
    await expect(page.locator("html")).toHaveAttribute("lang", locale === "pt-br" ? "pt-BR" : locale);
    const choices = page.locator(".language-picker a");
    await expect(choices).toHaveCount(3);
    for (const choice of await choices.all()) await expect(choice).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);
  }
});

test("uses readable hero text and persists the selected theme", async ({ page }) => {
  // REQ-PORTAL-006, REQ-PORTAL-007
  await page.goto("en/");
  const contrast = await page.evaluate(() => {
    const luminance = (value: string) => {
      const channels = value.match(/[\d.]+/g)?.slice(0, 3).map(Number);
      if (!channels || channels.length !== 3) throw new Error("Expected RGB color.");
      const linear = channels.map((channel) => {
        const value = channel / 255;
        return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
      });
      return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
    };
    const hero = document.querySelector(".portal-hero");
    if (!hero) throw new Error("Missing hero.");
    const background = luminance(getComputedStyle(hero).backgroundColor);
    return [".he-hero__lead", ".hero-caption", ".portal-hero .he-index__item strong", ".portal-hero .he-index__item span"]
      .map((selector) => {
        const element = document.querySelector(selector);
        if (!element) throw new Error(`Missing contrast target: ${selector}`);
        const foreground = luminance(getComputedStyle(element).color);
        return (Math.max(foreground, background) + 0.05) / (Math.min(foreground, background) + 0.05);
      });
  });
  for (const value of contrast) expect(value).toBeGreaterThanOrEqual(4.5);
  await page.getByRole("button", { name: t("en").dark, exact: true }).click();
  await expect(page.locator("html")).toHaveAttribute("data-he-theme", "dark");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-he-theme", "dark");
});

test("searches the active edition using the keyboard-accessible dialog", async ({ page }) => {
  // REQ-PORTAL-005
  await page.goto("es/");
  await page.getByRole("button", { name: t("es").searchHint, exact: true }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  await dialog.getByRole("searchbox").fill("SIFAP");
  await expect(dialog.locator(".search-results a").first()).toBeVisible();
  const href = await dialog.locator(".search-results a").first().getAttribute("href");
  expect(href).toContain("/es/");
  await page.keyboard.press("Escape");
  await expect(dialog).not.toBeVisible();
  await expect(page.getByRole("button", { name: t("es").searchHint, exact: true })).toBeFocused();
});

test("keeps the complete Markdown and the same source path when switching languages", async ({ page, request }) => {
  // REQ-PORTAL-001, REQ-PORTAL-003, REQ-PORTAL-004, REQ-PORTAL-008
  await page.goto("en/library/");
  await expect(page.locator(".collection-card").first().locator("code")).toHaveText("00-START-HERE.md");
  await expect(page.getByRole("searchbox")).toHaveAttribute("placeholder", t("en").filterPlaceholder);
  await page.getByRole("searchbox").fill("00-START-HERE");
  const entry = page.locator(".collection-card").filter({
    has: page.locator("code").filter({ hasText: /^00-START-HERE\.md$/ }),
  });
  await expect(entry).toHaveCount(1);
  await entry.click();
  for (const locale of ["es", "pt-br", "en"] as const) {
    await page.locator(`.language-picker a[hreflang="${locale}"]`).click();
    expect(page.url()).toContain(`/${locale}/docs/00-START-HERE/`);
    const original = page.getByRole("link", { name: t(locale).download, exact: false }).first();
    const href = await original.getAttribute("href");
    if (!href) throw new Error("The original download is required.");
    const response = await request.get(new URL(href, page.url()).href);
    expect(response.ok()).toBeTruthy();
    const markdown = await response.text();
    const source = page.locator(".he-details .source-code code");
    expect(await source.textContent()).toBe(markdown);
    await page.getByRole("button", { name: t(locale).markRead, exact: true }).click();
    await expect(page.getByRole("button", { name: t(locale).markedRead, exact: true })).toHaveAttribute("aria-pressed", "true");
    await page.getByRole("button", { name: t(locale).markedRead, exact: true }).click();
  }
});

test("supports stage keyboard navigation and reduced-motion preference", async ({ page }) => {
  // REQ-PORTAL-006, REQ-PORTAL-007
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("en/");
  const first = page.getByRole("tab").first();
  await first.scrollIntoViewIfNeeded();
  await expect(first).toBeEnabled();
  await first.focus();
  await page.keyboard.press("ArrowRight");
  await expect(page.getByRole("tab").nth(1)).toHaveAttribute("aria-selected", "true");
  await expect(page.getByRole("tabpanel")).toHaveAttribute("id", "stage-panel-1");
  const duration = await page.locator(".stage-panel").evaluate((element) => getComputedStyle(element).animationDuration);
  expect(duration).toBe("0s");
});
