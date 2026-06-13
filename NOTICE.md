# NOTICE — rights basis and third-party components

*This file documents the legal basis and third-party components for this
accessible edition. It is informational, not legal advice.*

## The accessible edition (the work)

This repository is a **faithful accessible re-creation** of a two-page research
infographic, *"Concerns About Violence Within Social Networks — Results from the
2020 California Safety and Wellbeing Survey (CSaWS)"* (January 2023), by the
**California Firearm Violence Research Center at UC Davis Health**
(<https://health.ucdavis.edu/vprp/ucfc>). The underlying peer-reviewed study is
Aubel AJ, Wintemute GJ, Kravitz-Wirtz N, *Prev. Med.* 2023;167:107421
(DOI 10.1016/j.ypmed.2023.107421, PMID 36641127).

All survey content and data are the work of the original authors. This edition
is an **independent re-creation and is not affiliated with or endorsed by
UC Davis.** Survey figures are transcribed faithfully from the published
infographic.

### Purpose and rights basis

This edition exists to **make the source material accessible** to people with
disabilities (WCAG 2.1 AA conforming HTML and a tagged PDF/UA-1), and to
demonstrate accessible-format conversion with the permission of the copyright
holders.

Reproduction and distribution of accessible-format copies for people who are
blind or have other disabilities is contemplated by the **Chafee Amendment,
17 U.S.C. § 121**, which permits authorized entities to reproduce and distribute
copies of a previously published literary work in **accessible formats**
exclusively for use by eligible persons with disabilities. The accessibility
work in this repository (semantic structure, data tables for every chart,
tagged PDF, contrast and keyboard conformance) is the accessible-format
production that provision describes.

Note: this rights basis applies to **the underlying copyrighted content** being
made accessible. It does **not** extend to third-party tooling, which is covered
by its own license terms (below).

## Third-party components

### Highcharts (interactive pie charts)

The HTML edition inlines **Highcharts core and the Highcharts Accessibility
module** (`scripts/lib/highcharts.js`, `scripts/lib/accessibility.js`,
Highcharts JS v13.0.0, © Highsoft AS) to render the pie charts as interactive,
keyboard- and screen-reader-accessible charts. They are layered as progressive
enhancement: if scripting is unavailable the figures fall back to a static SVG
chart and a data table, so no information depends on Highcharts.

Highcharts is **proprietary software, free for personal and non-commercial
use** under the Highcharts Non-Commercial License
(<https://www.highcharts.com/license>). This repository's use is
**non-commercial** (an accessibility demonstration). Any **commercial** use of
Highcharts requires a commercial license from Highsoft AS. The Highcharts source
retains its original copyright header.

Anyone reusing this repository commercially must either obtain a Highcharts
license or remove the interactive layer and rely on the static-SVG + data-table
charts, which carry no third-party dependency.

## Crisis resource

If you or someone you know is in crisis, call or text **988** (U.S. Suicide and
Crisis Lifeline), available 24/7. In an emergency, call **911**. *This crisis
resource was added by this accessible edition and was not part of the original
infographic.*
