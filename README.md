# Concerns About Violence Within Social Networks — accessible edition

A faithful, accessible (WCAG 2.1 AA) digital edition of a two-page research
infographic published by the **California Firearm Violence Research Center at
UC Davis Health**:

> **Concerns About Violence Within Social Networks — Results from the 2020
> California Safety and Wellbeing Survey (CSaWS).** January 2023.

The brief summarizes peer-reviewed findings on *anticipatory concerns about
violence* — situations where people perceive that someone in their social
network is at risk of harming others or themselves — and what, if anything,
they did about it.

This repository re-creates that infographic as three accessible deliverables
generated from a single source of truth, so the formats never drift apart.

## Deliverables

| Format | File | Notes |
|---|---|---|
| Markdown | [`document/CSaWS_SocialNetwork.md`](document/CSaWS_SocialNetwork.md) | Plain, faithful transcription with a data table for every chart |
| HTML | [`document/CSaWS_SocialNetwork.html`](document/CSaWS_SocialNetwork.html) | Self-contained, single-file accessible **infographic**; zero external requests. Pie charts are interactive (Highcharts, inlined) with a static-SVG + data-table fallback; CSP allows inline script for the inlined library (no `unsafe-eval`) |
| PDF | [`document/CSaWS_SocialNetwork_accessible.pdf`](document/CSaWS_SocialNetwork_accessible.pdf) | Tagged **PDF/UA-1** |

The original infographic is kept for reference at
[`CSaWSBrief_SocialNetwork.pdf`](CSaWSBrief_SocialNetwork.pdf).

## Accessibility

Conformance target: **WCAG 2.1 Level A and AA**. See
[`docs/ACCESSIBILITY.md`](docs/ACCESSIBILITY.md) for the full audit.

- A designed two-column **infographic** (brand colours, callout panels, a
  "What we learned" accent panel, highlight chips) that stays fully accessible.
- Semantic landmarks, single `h1`, logical heading order, skip link, `lang`.
- A decorative "1 in 5" pictogram (`aria-hidden`) accompanies the headline stat,
  which is also stated in text — so the graphic carries no information the text
  does not.
- The **pie charts** are interactive accessible **Highcharts** (keyboard
  navigation + screen-reader point announcements via the accessibility module),
  layered as progressive enhancement over a static decorative SVG and a real data
  `<table>`. If JavaScript is off or Highcharts fails, the static SVG stays and
  the table is always present. The interactive pie deliberately draws **no SVG
  text labels** (Highcharts SVG `<text>` confuses axe-core's contrast check); an
  HTML swatch legend provides the colour key in real, measurable text.
- The **donut and bar** charts remain decorative (`aria-hidden`) SVG/CSS paired
  with a real data `<table>`. Bar charts are CSS bars (no SVG text), so contrast
  is measured on real HTML and renders identically in the PDF.
- Data tables sit in collapsible `<details>` on screen; in the PDF they are
  expanded so the accessible representation always prints. The tagged PDF uses
  the static SVG charts (WeasyPrint runs no JavaScript).
- All text meets ≥ 4.5:1 contrast (≥ 3:1 for large text / UI).
- The PDF is tagged PDF/UA-1 (`MarkInfo/Marked`, `StructTreeRoot`, `/Lang`,
  `DisplayDocTitle`, XMP `pdfuaid` marker).

Verified with `pa11y` (axe-core + HTML CodeSniffer, WCAG2AA → *no issues*), a
token contrast script, a structural lint, and `pikepdf` inspection of the PDF
structure tree.

## Fidelity notes

This is a **faithful** transcription. Survey percentages are reproduced exactly
as printed and may not sum to 100% due to rounding and non-responses (as the
source itself notes).

The two reasons-related bar charts on page 2 of the original carry **no printed
data labels** — only a quantitative 0–50% axis with 10% gridlines. Their per-bar
values are given here as **approximate** percentages read off that axis (rounded
and clearly marked with `~`), with an explicit note and a link to the
peer-reviewed source study so readers can verify the exact figures. The values
are read from the chart's own axis, not invented, and are never presented as
exact.

## Build

All three deliverables are generated from `scripts/content.py`.

```bash
make export   # build md + html + pdf
make verify   # build + check PDF/UA scaffolding with pikepdf
make md | make html | make pdf   # individual targets
```

Requirements: Python 3, [WeasyPrint](https://weasyprint.org/) (system
Pango/cairo/gdk-pixbuf), and `pikepdf` for verification.

```
scripts/
  content.py     # single source of truth (all text + data)
  charts.py      # dependency-free SVG pie/donut generation
  build_md.py    # -> document/CSaWS_SocialNetwork.md
  build_html.py  # -> document/CSaWS_SocialNetwork.html
  build_pdf.py   # HTML -> PDF/UA-1 via WeasyPrint
  verify_pdf.py  # PDF/UA structure-tree checks
  lib/           # Highcharts core + accessibility module (inlined for the
                 # interactive pie charts; keeps the HTML self-contained)
```

## Citation

According to PubMed, the underlying peer-reviewed study is:

> Aubel AJ, Wintemute GJ, Kravitz-Wirtz N. Anticipatory concerns about violence
> within social networks: prevalence and implications for prevention.
> *Prev. Med.* 2023;167:107421.
> [DOI:10.1016/j.ypmed.2023.107421](https://doi.org/10.1016/j.ypmed.2023.107421)
> · PMID: 36641127

## Crisis resource

If you or someone you know is in crisis, call or text **988** (the U.S. Suicide
and Crisis Lifeline), available 24/7. In an emergency, call **911**. *This
crisis resource is added by this accessible edition and was not part of the
original infographic.*

## Attribution & disclaimer

Content and survey data are the work of the original authors and the California
Firearm Violence Research Center at UC Davis Health
(<https://health.ucdavis.edu/vprp/ucfc>). **This accessible edition is an
independent re-creation and is not affiliated with or endorsed by UC Davis.**
All survey figures are transcribed faithfully from the published infographic.

See [`NOTICE.md`](NOTICE.md) for the rights basis of this accessible edition
(Chafee Amendment, 17 U.S.C. § 121) and the terms for the bundled Highcharts
library (proprietary; free for non-commercial use).
