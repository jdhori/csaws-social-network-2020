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
| HTML | [`document/CSaWS_SocialNetwork.html`](document/CSaWS_SocialNetwork.html) | Self-contained, single file, zero external requests, strict CSP |
| PDF | [`document/CSaWS_SocialNetwork_accessible.pdf`](document/CSaWS_SocialNetwork_accessible.pdf) | Tagged **PDF/UA-1** |

The original infographic is kept for reference at
[`CSaWSBrief_SocialNetwork.pdf`](CSaWSBrief_SocialNetwork.pdf).

## Accessibility

Conformance target: **WCAG 2.1 Level A and AA**. See
[`docs/ACCESSIBILITY.md`](docs/ACCESSIBILITY.md) for the full audit.

- Semantic landmarks, single `h1`, logical heading order, skip link, `lang`.
- Every pie/donut chart is decorative (`aria-hidden`) and paired with a real
  data `<table>` (caption + scoped headers) that carries the same numbers.
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

The two reasons-related bar charts on page 2 of the original carry **no numeric
labels** — only a 0–50% axis. To avoid inventing data, they are presented here
as ordered categories with a relative-magnitude description (for example
"highest" / "low"), with an explicit note that exact percentages are not given
in the source.

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
