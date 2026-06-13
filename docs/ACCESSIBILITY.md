# Accessibility Audit: Concerns About Violence Within Social Networks (accessible edition)

**Standard:** WCAG 2.1 AA · **Date:** 2026-06-12 · **Scope:** generated HTML
(`document/CSaWS_SocialNetwork.html`) and tagged PDF
(`document/CSaWS_SocialNetwork_accessible.pdf`).

## Summary

**Issues found:** 0 unresolved · **Critical:** 0 · **Major:** 0 · **Minor:** 0

Automated scan (`pa11y` with the axe-core and HTML CodeSniffer runners,
`--standard WCAG2AA`) reports **no issues**. A token contrast script, a
structural lint, and `pikepdf` inspection of the PDF structure tree all pass.

## How this was tested

1. `pa11y --runner axe --runner htmlcs --standard WCAG2AA` (headless Chromium) → no issues.
2. Token contrast script over every foreground/background color pair (WCAG ratio math).
3. Structural lint: `lang`, `<title>`, single `h1`, heading order, skip link,
   landmarks, `<img>` alt, table `<caption>` + `scope`, decorative SVG `aria-hidden`.
4. `pikepdf` structure-tree inspection of the PDF.
5. Manual review of rendered PDF pages (rasterized) for layout and reading order.

## Findings

### Perceivable

| # | Issue | WCAG Criterion | Severity | Resolution |
|---|-------|----------------|----------|------------|
| 1 | Decorative charts could be read as data noise | 1.1.1 Non-text Content | — | The donut SVGs and CSS bar charts are `aria-hidden`, each paired with a data `<table>` carrying the same numbers (collapsed in `<details>` on screen, expanded in the PDF). The pie charts are interactive accessible Highcharts (keyboard + screen-reader point announcements) layered over the same static SVG + table fallback. |
| 5 | Highcharts data labels flagged for contrast | 1.4.3 Contrast | Resolved | Highcharts renders data labels and its legend as SVG `<text>`, which axe-core cannot resolve a background for and reports as false-positive contrast failures. The interactive pies disable both; an HTML swatch legend (real, measurable text) supplies the colour key, and values are announced on keyboard focus and listed in the data table. |
| 6 | Decorative "1 in 5" pictogram | 1.1.1 Non-text Content | — | The five-figure pictogram is `aria-hidden`; the same ratio ("1 in 5") is stated in adjacent text, so the graphic conveys nothing the text does not. |
| 2 | Big donut percentage initially unresolved by axe | 1.4.3 Contrast | Resolved | Number rendered as an HTML element with its own solid white background; ink-on-white ≈ 16:1. |
| 3 | Information conveyed by chart color | 1.4.1 Use of Color | — | Color is never the only channel: every value appears as text in a table; legends pair swatches with text labels; bar charts label each series in text. |
| 4 | Hero text over a background-image | 1.4.3 Contrast | Resolved | axe-core cannot evaluate contrast over a `linear-gradient`; the hero uses a solid `#0b2f55` so white text is measurable (≈ 12:1). |

### Operable

| # | Issue | WCAG Criterion | Severity | Resolution |
|---|-------|----------------|----------|------------|
| 1 | Bypass repeated header | 2.4.1 Bypass Blocks | — | Skip link to `#main`. |
| 2 | Focus visibility | 2.4.7 Focus Visible | — | 3px high-contrast `:focus-visible` outline on all links/summary. |
| 3 | Page title | 2.4.2 Page Titled | — | Unique descriptive `<title>`; PDF `DisplayDocTitle` true. |

### Understandable

| # | Issue | WCAG Criterion | Severity | Resolution |
|---|-------|----------------|----------|------------|
| 1 | Language of page | 3.1.1 Language of Page | — | `<html lang="en">`; PDF `/Lang` set. |
| 2 | Ambiguous bar-chart data | 3.3.2 / fidelity | — | Source bars have a 0%–50% axis but no printed data labels; per-bar values given as approximate readings off that axis (marked with `~`), with a note and a link to the peer-reviewed source study for exact figures. |

### Robust

| # | Issue | WCAG Criterion | Severity | Resolution |
|---|-------|----------------|----------|------------|
| 1 | Name/role/value | 4.1.2 | — | Native semantic HTML throughout (headings, tables, lists, links). The only scripted widgets are the interactive Highcharts pies, whose accessibility module supplies roles, names, and keyboard navigation; each also has a static SVG + data-table fallback if scripting is unavailable. |
| 2 | PDF programmatic structure | 4.1.2 / PDF/UA-1 | — | Tagged structure tree: 1 H1, 14 H2, 6 H3, 8 tables (THead/TBody/TH/TD/Caption), lists, links. |

## Color contrast check (representative)

| Element | Foreground | Background | Ratio | Required | Pass? |
|---|---|---|---|---|---|
| Body text | `#1a1f29` | `#ffffff` | 16.5:1 | 4.5:1 | ✅ |
| H2 headings | `#0b2f55` | `#ffffff` | 13.5:1 | 4.5:1 | ✅ |
| H3 subheads | `#3d4554` | `#ffffff` | 9.6:1 | 4.5:1 | ✅ |
| Links | `#0a4f8a` | `#ffffff` | 8.4:1 | 4.5:1 | ✅ |
| Header subtitle | `#d7e3f1` | `#0b2f55` | 10.4:1 | 4.5:1 | ✅ |
| Table header | `#ffffff` | `#0b2f55` | 13.5:1 | 4.5:1 | ✅ |
| Row header | `#1a1f29` | `#f4f6fb` | 15.3:1 | 4.5:1 | ✅ |
| Emphasis number (large) | `#1f6fb2` | `#f4f6fb` | 4.9:1 | 3:1 | ✅ |
| Green stat text | `#3f6f24` | `#ffffff` | 6.0:1 | 4.5:1 | ✅ |
| Focus ring (UI) | `#b8002e` | `#ffffff` | 6.8:1 | 3:1 | ✅ |

## Keyboard navigation

| Element | Behavior |
|---|---|
| Skip link | First in tab order; moves focus to `#main`. |
| Links (DOI, study, footnote) | Reachable, visible focus ring, activate on Enter (pointer-up). |
| Interactive pie charts (Highcharts) | Focusable; arrow keys move between data points, each announced by the accessibility module. Falls back to a static SVG + data table when scripting is off. |
| Data-table `<details>` | Native `<summary>`, keyboard-toggle with Enter/Space. |

## Manual checks still recommended before each release

- Screen reader smoke test (NVDA / VoiceOver) of table reading order.
- 200% / 400% zoom reflow (single-column collapse verified in CSS at ≤640px).
- `prefers-reduced-motion` (no motion is used; rule present as a safeguard).
