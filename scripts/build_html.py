#!/usr/bin/env python3
"""Generate the self-contained, accessible (WCAG 2.1 AA) HTML infographic.

This is a faithful *visual* re-creation of the original two-page infographic --
brand colours, callout panels, a "What we learned" sidebar, real pie/donut/bar
graphics -- rebuilt so it is fully accessible:

- One file, zero external requests (self-contained; strict CSP).
- Semantic landmarks, single h1, logical heading order, skip link, lang.
- Every chart is DECORATIVE (aria-hidden) and paired with a real data <table>
  (caption + scoped headers). Tables live in <details> so the infographic stays
  visually clean while assistive tech can still reach every number.
- Bar charts are CSS bars (no SVG text), so contrast is real HTML text -- robust
  under axe-core and renders identically in WeasyPrint's PDF.
- Print CSS makes the same markup render as a clean tagged PDF/UA-1.
"""

import html
import json
from pathlib import Path

import content as C
import charts

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "document" / "CSaWS_SocialNetwork.html"
LIB = HERE / "lib"

# Bars are plotted on the source chart's 0%-50% axis.
AXIS_MAX = 50

# Accessible interactive Highcharts are layered on top of the static graphic +
# data table as progressive enhancement. Each chart's config is collected here
# and emitted in a single init script; the static SVG/CSS graphic and the data
# table remain the default/fallback (and the only thing the tagged PDF uses,
# since WeasyPrint runs no JavaScript). PIE_SPECS holds the pies; BAR_SPECS the
# grouped bar charts.
PIE_SPECS = {}
BAR_SPECS = {}


def read_lib(name):
    return (LIB / name).read_text(encoding="utf-8")


def pie_config(title, rows, palette, desc):
    """Highcharts pie config (JSON-serializable; no functions). Uses point.y so
    the printed survey percentages are shown verbatim, not re-normalized."""
    data = [{"name": lbl, "y": pct} for lbl, pct in rows]
    colors = [palette[i % len(palette)] for i in range(len(rows))]
    return {
        "chart": {"type": "pie", "height": 240, "backgroundColor": "transparent",
                  "style": {"fontFamily": "inherit"}},
        "title": {"text": None},
        "credits": {"enabled": False},
        "colors": colors,
        "accessibility": {"enabled": True, "description": desc,
                          "point": {"valueSuffix": "%"}},
        # No persistent SVG <text>: Highcharts data labels / legend render as SVG
        # text, which axe-core cannot resolve a background for and reports as
        # false-positive contrast failures. We disable both and keep an HTML
        # swatch legend (real, measurable text) for the colour->category mapping;
        # values are announced by the accessibility module on keyboard focus and
        # listed in the data table.
        "legend": {"enabled": False},
        "tooltip": {"pointFormat": "<b>{point.y}%</b>"},
        "plotOptions": {"pie": {
            "borderWidth": 1, "borderColor": "#ffffff",
            "dataLabels": {"enabled": False}}},
        "series": [{"name": title, "colorByPoint": True, "data": data}],
    }


def bar_config(rows, desc):
    """Highcharts grouped horizontal-bar config (JSON-serializable; no functions).

    Two series (other-/self-directed) plotted on the source's 0%-50% axis. Like
    the pies, the Highcharts legend and data labels are OFF: those render as SVG
    <text> that axe-core cannot resolve a background for (false-positive contrast
    failures). The colour->series key is the real HTML legend (`.bc-legend`);
    values are announced on keyboard focus by the accessibility module and listed
    in the data table. Axis text uses high-contrast ink (#1a1f29) on the white
    figure background so the remaining SVG text is genuinely legible."""
    cats = [r[0] for r in rows]
    return {
        # Solid WHITE chart background (not transparent): the bar chart must keep
        # its axis labels (SVG <text>), and axe-core only flags those as contrast
        # failures when it cannot resolve a background. An explicit opaque white
        # lets axe compute the real ratio (dark ink on white ~= 15:1 -> passes).
        "chart": {"type": "bar", "height": 96 + len(rows) * 84,
                  "backgroundColor": "#ffffff", "style": {"fontFamily": "inherit"},
                  "spacingBottom": 16},
        "title": {"text": None},
        "credits": {"enabled": False},
        "colors": ["#1f6fb2", "#4f8a32"],
        "accessibility": {"enabled": True, "description": desc,
                          "point": {"valueSuffix": "%"}},
        "legend": {"enabled": False},
        # useHTML renders axis labels/titles as real HTML (foreignObject) instead
        # of SVG <text>. axe-core cannot evaluate contrast on SVG text and reports
        # false-positive failures; HTML text on the white chart background is
        # measured correctly (dark ink ~= 15:1 -> passes).
        "xAxis": {"categories": cats, "lineColor": "#c9ced9", "tickColor": "#c9ced9",
                  "labels": {"useHTML": True,
                             "style": {"color": "#1a1f29", "fontSize": "12px",
                                       "backgroundColor": "#ffffff"}}},
        "yAxis": {"min": 0, "max": AXIS_MAX, "tickInterval": 10,
                  "gridLineColor": "#dbe0ea",
                  "title": {"text": "Percent (approximate)", "useHTML": True,
                            "style": {"color": "#3d4554", "backgroundColor": "#ffffff"}},
                  "labels": {"format": "{value}%", "useHTML": True,
                             "style": {"color": "#1a1f29", "fontSize": "12px",
                                       "backgroundColor": "#ffffff"}}},
        "tooltip": {"shared": True, "valueSuffix": "%"},
        "plotOptions": {"bar": {"borderWidth": 0, "groupPadding": 0.12,
                                "dataLabels": {"enabled": False}}},
        "series": [
            {"name": "Other-directed violence", "data": [r[1] for r in rows]},
            {"name": "Self-directed violence", "data": [r[2] for r in rows]},
        ],
    }


def esc(s):
    return html.escape(str(s), quote=True)


# --- component builders -----------------------------------------------------

def pct_table(caption, rows, footnote=False):
    body = []
    for label, pct in rows:
        mark = ' <a href="#fn-nb" class="fn">*</a>' if (footnote and label == "Nonbinary") else ""
        body.append(
            f'<tr><th scope="row">{esc(label)}{mark}</th>'
            f'<td>{pct}%</td></tr>'
        )
    return (
        f'<table class="data"><caption>{esc(caption)}</caption>'
        f'<thead><tr><th scope="col">Category</th>'
        f'<th scope="col">Percent of persons at perceived risk</th></tr></thead>'
        f'<tbody>{"".join(body)}</tbody></table>'
    )


def details_table(summary, table_html):
    """Tuck a data table into a collapsible <details> so the visual leads while
    the accessible representation stays in the DOM."""
    return (
        f'<details class="data-details"><summary>{esc(summary)}</summary>'
        f'<div class="dd-body">{table_html}</div></details>'
    )


def pie_card(chart_id, title, table_caption, rows, palette, footnote=False, desc=None):
    """One pie figure with the full progressive-enhancement fallback chain:

      1. interactive accessible Highcharts pie  (screen, only once chart-ready)
      2. static decorative SVG pie               (default; print; JS-off)
      3. collapsible data <table>                (always in the DOM)

    JS adds `.chart-ready` to this figure only if Highcharts initializes, which
    flips CSS from the static SVG to the interactive chart. If JS is disabled or
    Highcharts fails, the static SVG stays -- and the data table is always there.
    """
    PIE_SPECS[chart_id] = pie_config(title, rows, palette, desc or table_caption)
    svg = charts.pie_svg(rows, palette, size=200)
    legend = charts.legend_swatches(rows, palette)
    table = pct_table(table_caption, rows, footnote)
    return (
        f'<figure class="pie-card chart-figure">'
        f'<figcaption>{esc(title)}</figcaption>'
        f'<div class="pie-interactive" id="{esc(chart_id)}"></div>'
        f'<div class="pie-vis pie-static">{svg}</div>'
        f'{legend}'
        f'{details_table("Show the data table: " + table_caption, table)}'
        f'</figure>'
    )


def pictogram(total=5, filled=1):
    """Decorative '1 in N' pictogram (aria-hidden): N person glyphs, `filled`
    highlighted. Purely visual -- the same ratio is stated in text in the hero
    stat ("1 in 5"), so marking the graphic aria-hidden is correct (it carries
    no information the text does not)."""
    glyph = ('<path d="M14 8 a6 6 0 1 1 -0.01 0 z" />'
             '<path d="M14 16 c-6 0 -9 4 -9 10 v8 h18 v-8 c0 -6 -3 -10 -9 -10 z" />')
    figs = []
    for i in range(total):
        cls = "on" if i < filled else "off"
        figs.append(f'<g class="pg {cls}" transform="translate({i*30},2)">{glyph}</g>')
    return (
        f'<svg class="pictogram" aria-hidden="true" focusable="false" '
        f'viewBox="0 0 {total*30-2} 40" width="{total*30-2}" height="40" '
        f'role="presentation">{"".join(figs)}</svg>'
    )


def callout_chips(items):
    chips = "".join(f'<li>{esc(c)}</li>' for c in items)
    return f'<ul class="chips" aria-label="Highlights">{chips}</ul>'


def bar_table(block):
    rows = []
    for cat, other, selfd in block["rows"]:
        rows.append(
            f'<tr><th scope="row">{esc(cat)}</th>'
            f'<td>~{other}%</td><td>~{selfd}%</td></tr>'
        )
    return (
        f'<table class="data reasons"><caption>{esc(block["title"])}</caption>'
        f'<thead><tr><th scope="col">Reason</th>'
        f'<th scope="col">Other-directed violence (approximate)</th>'
        f'<th scope="col">Self-directed violence (approximate)</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )


def _bar(series_class, label, value):
    w = max(2.0, value / AXIS_MAX * 100)  # min width so a tiny bar stays visible
    return (
        f'<div class="bc-line">'
        f'<span class="bc-key">{esc(label)}</span>'
        f'<span class="bc-track"><span class="bc-fill {series_class}" '
        f'style="width:{w:.1f}%"></span></span>'
        f'<span class="bc-num">~{value}%</span>'
        f'</div>'
    )


def bar_chart(block, chart_id, desc=None):
    """One grouped bar figure with the full progressive-enhancement fallback:

      1. interactive accessible Highcharts bar  (screen, only once chart-ready)
      2. static CSS grouped bars                (default; print; JS-off)
      3. collapsible data <table>               (always in the DOM)

    The static CSS graphic is aria-hidden; every number is repeated as real HTML
    text so axe-core measures contrast on HTML (not SVG), and it renders the same
    way in the tagged PDF. The data table is the accessible source of truth. JS
    adds `.chart-ready` to this figure only if Highcharts initializes, flipping
    CSS from the static bars to the interactive chart.
    """
    BAR_SPECS[chart_id] = bar_config(block["rows"], desc or block["title"])
    legend = (
        '<div class="bc-legend" aria-hidden="true">'
        '<span class="bc-tag"><span class="sw other"></span>Other-directed</span>'
        '<span class="bc-tag"><span class="sw self"></span>Self-directed</span>'
        '</div>'
    )
    rows = []
    for cat, other, selfd in block["rows"]:
        rows.append(
            f'<div class="bc-row">'
            f'<div class="bc-cat">{esc(cat)}</div>'
            f'<div class="bc-bars">{_bar("other", "Other-directed", other)}'
            f'{_bar("self", "Self-directed", selfd)}</div>'
            f'</div>'
        )
    axis = (
        '<div class="bc-axis" aria-hidden="true">'
        + "".join(f"<span>{t}%</span>" for t in range(0, AXIS_MAX + 1, 10))
        + "</div>"
    )
    note = (
        f'<p class="note">Note: {esc(block["axis_note"])} For the exact data, '
        f'see <a href="{esc(C.META["doi_url"])}">the peer-reviewed source study '
        f'(DOI {esc(C.META["doi"])})</a>.</p>'
    )
    return (
        f'<figure class="bar-card chart-figure">'
        f'<figcaption>{esc(block["title"])}</figcaption>'
        f'{legend}'
        f'<div class="bar-interactive" id="{esc(chart_id)}"></div>'
        f'<div class="barchart bar-static" aria-hidden="true">{"".join(rows)}{axis}</div>'
        f'{details_table("Show the data table for this chart", bar_table(block))}'
        f'{note}'
        f'</figure>'
    )


def donut_pair(items, color):
    cards = []
    for it in items:
        n = int(it["percent"].rstrip("%"))
        cards.append(
            f'<div class="donut-card">'
            f'<div class="donut-wrap">'
            f'{charts.stat_donut_svg(n, color, label=False)}'
            f'<span class="donut-num" aria-hidden="true">{esc(it["percent"])}</span>'
            f'</div>'
            f'<p><span class="sr-only">{esc(it["percent"])}: </span>{esc(it["text"])}</p>'
            f'</div>'
        )
    return f'<div class="donut-grid">{"".join(cards)}</div>'


# --- CSS --------------------------------------------------------------------

CSS = """
:root{
  color-scheme: light;
  --ink:#1a1f29; --muted:#3d4554; --line:#c9ced9;
  --bg:#ffffff; --panel:#f4f6fb;
  --brand:#0b2f55; --blue:#1f6fb2; --blue-dark:#0b3d66;
  --bar-other:#1f6fb2; --bar-self:#4f8a32; --green-ink:#2f5d1e;
  --lavender:#e9e5f5; --lightblue:#e7f0fb; --focus:#b8002e;
  --space:1.25rem; --maxw:64rem;
}
*{box-sizing:border-box}
html{font-size:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.55}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0,0,0,0);white-space:nowrap;border:0}
.skip{position:absolute;left:-999px;top:0;background:var(--brand);color:#fff;
  padding:.6rem 1rem;z-index:10;border-radius:0 0 .4rem 0}
.skip:focus{left:0}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--space)}
a{color:#0a4f8a}
a:focus-visible, summary:focus-visible, th a:focus-visible{
  outline:3px solid var(--focus);outline-offset:2px}

/* Hero */
/* Solid background (no gradient image): axe-core cannot evaluate contrast for
   text over a background-image, so a solid colour keeps the white hero text
   measurable and passing. A thin accent rule adds depth without an image. */
header.hero{background:#0b2f55;color:#fff;padding:2rem 0 2.2rem;
  border-bottom:4px solid #1f6fb2}
header.hero .eyebrow{margin:0;font-size:.85rem;letter-spacing:.12em;text-transform:uppercase;
  color:#bcd3ec;font-weight:700}
header.hero h1{margin:.35rem 0 .4rem;font-size:clamp(1.6rem,1rem+3vw,2.8rem);line-height:1.12;
  max-width:24ch}
header.hero p.sub{margin:.15rem 0;color:#d7e3f1;font-size:1.05rem}
.hero-stat{display:flex;align-items:baseline;gap:.6rem;margin-top:1.1rem;
  background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.25);
  border-radius:.6rem;padding:.7rem 1rem;max-width:34rem}
.hero-stat .big{font-size:2.4rem;font-weight:800;color:#fff;line-height:1;white-space:nowrap}
.hero-stat .txt{color:#eaf1f9;font-size:1rem}
/* Decorative '1 in 5' pictogram: 1 highlighted figure of 5. aria-hidden, so it
   adds no accessibility burden -- the ratio is also stated as text. */
.pictogram{flex:0 0 auto;align-self:center;height:40px;width:auto}
.pictogram .pg.on path{fill:#ffffff}
.pictogram .pg.off path{fill:rgba(255,255,255,.34)}

main{padding:1.5rem 0 2.5rem}
section{margin:0 0 1.5rem}
/* Left accent bar via border (no flex / no ::before): a flex heading with a
   generated-content box makes WeasyPrint's tagger emit a duplicate /H2. */
h2{font-size:clamp(1.3rem,1rem+1.3vw,1.7rem);color:var(--brand);margin:2rem 0 .4rem;
  border-left:.45rem solid var(--blue);padding-left:.6rem;line-height:1.25}
.section-sub{color:var(--muted);margin:.1rem 0 1rem}
h3{font-size:1.02rem;color:var(--brand);margin:0 0 .5rem}

.lead{font-size:1.18rem;background:var(--panel);border-left:5px solid var(--blue);
  padding:1rem 1.2rem;border-radius:.4rem}

/* Highlight chips */
ul.chips{list-style:none;display:flex;flex-wrap:wrap;gap:.5rem;margin:.2rem 0 1rem;padding:0}
ul.chips li{background:var(--lightblue);color:var(--blue-dark);font-weight:700;
  border:1px solid #c4ddf4;border-radius:999px;padding:.3rem .8rem;font-size:.92rem}

/* Pie cards */
.pie-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1rem}
figure.pie-card{margin:0;background:#fff;border:1px solid var(--line);border-radius:.6rem;
  padding:1rem;text-align:center;box-shadow:0 1px 2px rgba(11,47,85,.06)}
figure.pie-card figcaption{font-weight:700;color:var(--brand);margin-bottom:.5rem}
.pie-vis{display:flex;justify-content:center}
.pie{max-width:100%;height:auto}
/* Progressive enhancement: static SVG is the DEFAULT; the interactive Highcharts
   pie is hidden until JS adds .chart-ready to the figure. Then we swap to the
   interactive chart and hide the now-redundant static SVG + swatch legend
   (Highcharts draws its own data labels). */
.pie-interactive{display:none;min-height:240px}
.chart-figure.chart-ready .pie-interactive{display:block}
.chart-figure.chart-ready .pie-static{display:none}
/* The HTML swatch legend stays visible in the interactive view too: the
   interactive pie intentionally draws no SVG text labels, so the legend is the
   sighted-user colour key. */
.highcharts-credits{display:none}
ul.legend{list-style:none;margin:.6rem 0 0;padding:0;text-align:left;display:grid;gap:.2rem;
  font-size:.88rem}
ul.legend .swatch{display:inline-block;width:.85rem;height:.85rem;border-radius:2px;
  margin-right:.45rem;vertical-align:middle;border:1px solid rgba(0,0,0,.25)}

/* Tables (collapsed under charts) */
details.data-details{margin-top:.7rem;text-align:left;border:1px solid var(--line);
  border-radius:.4rem;background:var(--panel)}
details.data-details>summary{cursor:pointer;padding:.5rem .7rem;font-weight:600;
  color:var(--blue-dark);font-size:.9rem;list-style-position:inside}
details.data-details[open]>summary{border-bottom:1px solid var(--line)}
.dd-body{padding:.6rem .7rem}
table.data{border-collapse:collapse;width:100%;font-size:.95rem}
table.data caption{text-align:left;font-weight:700;color:var(--brand);padding:.2rem 0 .4rem;
  font-size:.98rem}
table.data th,table.data td{border:1px solid var(--line);padding:.4rem .6rem;text-align:left}
table.data thead th{background:var(--brand);color:#fff;border-color:var(--brand)}
table.data tbody th{background:#fff;font-weight:600}
.reasons td{text-align:right;font-variant-numeric:tabular-nums}

/* Bento for the page-2 concern row */
.bento{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:1rem;align-items:start}

/* Bar charts */
figure.bar-card{margin:0;background:#fff;border:1px solid var(--line);border-radius:.6rem;
  padding:1.1rem 1.2rem;box-shadow:0 1px 2px rgba(11,47,85,.06)}
figure.bar-card figcaption{font-weight:700;color:var(--brand);margin-bottom:.5rem}
.bc-legend{display:flex;gap:1rem;margin-bottom:.7rem;font-size:.9rem;font-weight:600;color:var(--muted)}
.bc-tag{display:inline-flex;align-items:center;gap:.4rem}
.bc-tag .sw{width:.9rem;height:.9rem;border-radius:2px;display:inline-block}
.sw.other{background:var(--bar-other)} .sw.self{background:var(--bar-self)}
.barchart{display:grid;gap:.55rem}
.bc-row{display:grid;grid-template-columns:11rem 1fr;gap:.6rem;align-items:center}
.bc-cat{font-size:.92rem;color:var(--ink);font-weight:600}
.bc-bars{display:grid;gap:.3rem}
.bc-line{display:grid;grid-template-columns:1fr auto;gap:.5rem;align-items:center}
.bc-track{position:relative;background:#eef1f6;border-radius:3px;height:1rem;overflow:hidden;
  background-image:repeating-linear-gradient(90deg,transparent 0,transparent calc(20% - 1px),#dbe0ea calc(20% - 1px),#dbe0ea 20%)}
.bc-fill{display:block;height:100%;border-radius:3px 0 0 3px;min-width:.2rem}
.bc-fill.other{background:var(--bar-other)} .bc-fill.self{background:var(--bar-self)}
.bc-num{font-size:.85rem;font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums;
  min-width:3.2rem;text-align:right}
.bc-key{display:none}
.bc-axis{display:flex;justify-content:space-between;margin:.45rem 0 0 11.6rem;
  font-size:.75rem;color:var(--muted)}
/* Progressive enhancement: the static CSS bars are the DEFAULT; the interactive
   Highcharts bar is hidden until JS adds .chart-ready to the figure, then we
   swap to the interactive chart and hide the now-redundant CSS bars. The HTML
   colour key (.bc-legend) stays in both views. */
.bar-interactive{display:none;background:#fff;border-radius:.4rem;overflow:hidden}
.chart-figure.chart-ready .bar-interactive{display:block}
.chart-figure.chart-ready .bar-static{display:none}

/* Firearms callout */
.callout{background:var(--lightblue);border:1px solid #c4ddf4;border-radius:.6rem;
  padding:1.1rem 1.2rem;color:var(--blue-dark)}
.callout .big{display:block;font-size:1.35rem;font-weight:800;color:var(--brand);
  margin-bottom:.3rem;line-height:1.2}

/* Donuts */
.donut-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1rem}
.donut-card{background:var(--panel);border-radius:.6rem;padding:1.2rem;text-align:center}
.donut-wrap{position:relative;width:160px;height:160px;margin:0 auto .6rem}
/* Own solid white background so axe-core computes contrast directly; kept small
   (5rem chip) so its square bounding box stays inside the SVG's white hole. */
.donut-num{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:5rem;height:5rem;border-radius:50%;background:#fff;display:grid;place-items:center;
  font-size:1.7rem;font-weight:800;color:var(--ink)}

/* Likelihood list */
ul.likely,ul.takeaways{padding-left:1.2rem;margin:.4rem 0}
ul.likely li,ul.takeaways li{margin:.45rem 0}

/* "What we learned" accent panel */
.learned{background:var(--lavender);border-radius:.7rem;padding:1.2rem 1.4rem;border:1px solid #d3cbe9}
.learned h2{margin-top:0}
.learned ul{margin:.3rem 0 0}

.methodology{background:var(--lightblue);border-radius:.6rem;padding:1.1rem 1.3rem;
  border:1px solid #c4ddf4}
.note{font-size:.86rem;color:var(--muted);margin:.6rem 0 0}
blockquote.fnbox{margin:1rem 0;background:var(--panel);border-left:4px solid var(--line);
  padding:.6rem 1rem;font-size:.9rem;color:var(--muted);border-radius:.3rem}
.editor{border:2px solid var(--blue);border-radius:.6rem;padding:1.1rem 1.3rem;
  background:#eef4fb;margin-top:2rem}
.editor h2{margin-top:0}
.crisis{font-weight:700;background:#fff3f4;border:1px solid #e3b6bd;border-radius:.4rem;
  padding:.7rem .9rem;margin-top:.6rem;color:#7a1020}
footer.brief{border-top:1px solid var(--line);padding:1.5rem 0;color:var(--muted);font-size:.88rem}

@media (max-width:760px){
  .bento{grid-template-columns:1fr}
  .bc-row{grid-template-columns:1fr}
  .bc-axis{margin-left:0}
}
@media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}}

@media print{
  @page{size:letter;margin:16mm 14mm;
    @top-center{content:"Concerns About Violence Within Social Networks - CSaWS 2020";
      font-size:8pt;color:#555}
    @bottom-right{content:"Page " counter(page) " of " counter(pages);font-size:8pt;color:#555}}
  body{font-size:10pt}
  .skip{display:none}
  header.hero, .callout, .learned, .methodology, .donut-card, .editor, .crisis,
  table.data thead th, ul.chips li, .lead, .bc-fill, .bc-track, .sw,
  figure.pie-card, figure.bar-card{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  h2{string-set:section content();bookmark-level:1;bookmark-label:content()}
  /* Expand every data table in the PDF so the accessible representation prints. */
  details.data-details>summary{display:none!important}
  details.data-details>.dd-body{display:block!important}
  details.data-details{background:none;border:0}
  /* A data table that splits across a page break crashes WeasyPrint's PDF/UA
     tagger ("Table wrapper without a table"); the caption break-after is required. */
  table.data{break-inside:avoid}
  table.data caption{break-after:avoid}
  /* Keep small blocks whole, but let the tall bar-card flow across pages
     (otherwise it strands its heading with a full blank page). Its inner table
     and rows still stay intact via the rules above. */
  figure.pie-card, .donut-card, .bc-row, .callout{break-inside:avoid}
  figure.bar-card figcaption, .bc-legend{break-after:avoid}
  .bento, .pie-grid, .donut-grid{display:block}
  figure.pie-card, .donut-card{margin-bottom:.6rem}
  /* WeasyPrint runs no JS (chart-ready never set), so the static SVG already
     prints; this also forces it if a browser prints after enhancement. */
  .pie-interactive{display:none!important}
  .chart-figure .pie-static{display:flex!important}
  .chart-figure ul.legend{display:grid!important}
  /* Same for bar charts: print the static CSS bars, never the interactive layer. */
  .bar-interactive{display:none!important}
  .chart-figure .bar-static{display:grid!important}
}
"""

# CSP: still self-contained (no external requests of any kind). Interactive pie
# charts add inlined Highcharts, so script-src must allow 'unsafe-inline'. The
# libs use no eval / new Function, so 'unsafe-eval' is deliberately NOT granted.
CSP = ("default-src 'none'; img-src data:; style-src 'unsafe-inline'; "
       "script-src 'unsafe-inline'; font-src data:; base-uri 'none'; "
       "form-action 'none'")


def build():
    m = C.META
    P = charts
    PIE_SPECS.clear()
    head = f"""<!doctype html>
<html lang="{esc(m['lang'])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{esc(CSP)}">
<meta name="author" content="{esc(m['publisher'])}">
<meta name="description" content="{esc(m['description'])}">
<meta name="keywords" content="{esc(m['keywords'])}">
<title>{esc(m['title'])} - CSaWS 2020 (accessible edition)</title>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header class="hero"><div class="wrap">
<p class="eyebrow">{esc(m['publisher'])} &middot; {esc(m['date'])}</p>
<h1>{esc(m['title'])}</h1>
<p class="sub">{esc(m['subtitle'])}</p>
<div class="hero-stat">{pictogram(5, 1)}<span class="big">{esc(C.HEADLINE['stat'])}</span>
<span class="txt">{esc(C.HEADLINE['detail'])}</span></div>
</div></header>
<main id="main"><div class="wrap">
"""

    s = [head]
    a = s.append

    # The question
    a('<section aria-labelledby="q-h"><h2 id="q-h">The question we asked</h2>')
    a(f'<p class="lead">{esc(C.QUESTION)}</p></section>')

    # Other-directed
    a('<section aria-labelledby="other-h">'
      '<h2 id="other-h">Persons at perceived risk of other-directed violence</h2>')
    a('<p class="section-sub">How respondents described the person they were worried about.</p>')
    a(callout_chips(C.OTHER_CALLOUTS))
    a('<div class="pie-grid">')
    a(pie_card("pie-or-rel", "Relationship to the respondent",
               "Relationship (other-directed violence)",
               C.OTHER_RELATIONSHIP, P.BLUE_PALETTE,
               desc="Relationship of the person at perceived risk of other-directed "
                    "violence to the respondent."))
    a(pie_card("pie-or-gen", "Sex or gender", "Sex or gender (other-directed violence)",
               C.OTHER_GENDER, P.BLUE_PALETTE, footnote=True,
               desc="Sex or gender of persons at perceived risk of other-directed violence."))
    a(pie_card("pie-or-age", "Age", "Age (other-directed violence)",
               C.OTHER_AGE, P.BLUE_PALETTE,
               desc="Age groups of persons at perceived risk of other-directed violence."))
    a('</div></section>')

    # Self-directed
    a('<section aria-labelledby="self-h">'
      '<h2 id="self-h">Persons at perceived risk of self-directed violence</h2>')
    a('<p class="section-sub">How respondents described the person they were worried about.</p>')
    a(callout_chips(C.SELF_CALLOUTS))
    a('<div class="pie-grid">')
    a(pie_card("pie-sf-rel", "Relationship to the respondent",
               "Relationship (self-directed violence)",
               C.SELF_RELATIONSHIP, P.GREEN_PALETTE,
               desc="Relationship of the person at perceived risk of self-directed "
                    "violence to the respondent."))
    a(pie_card("pie-sf-gen", "Sex or gender", "Sex or gender (self-directed violence)",
               C.SELF_GENDER, P.GREEN_PALETTE, footnote=True,
               desc="Sex or gender of persons at perceived risk of self-directed violence."))
    a(pie_card("pie-sf-age", "Age", "Age (self-directed violence)",
               C.SELF_AGE, P.GREEN_PALETTE,
               desc="Age groups of persons at perceived risk of self-directed violence."))
    a('</div></section>')

    # Footnotes for the pies
    a(f'<blockquote class="fnbox" id="fn-nb"><p>* {esc(C.FOOTNOTES[0])}</p>'
      f'<p>Note: {esc(C.FOOTNOTES[1])}</p></blockquote>')

    # Likelihood
    a('<section aria-labelledby="like-h">'
      '<h2 id="like-h">Likelihood of harm in the next year</h2><ul class="likely">')
    for it in C.LIKELIHOOD:
        a(f'<li><strong>{esc(it["percent"])}</strong> {esc(it["text"])}</li>')
    a('</ul></section>')

    # Reasons for concern + firearms callout (bento)
    a('<section aria-labelledby="why-h"><h2 id="why-h">Why respondents were concerned</h2>')
    a('<div class="bento">')
    a(bar_chart(C.REASONS_CONCERN, "bar-concern",
                desc="Approximate share of respondents citing each reason for "
                     "concern, split by other-directed and self-directed violence."))
    a(f'<aside class="callout" aria-label="Access to firearms">'
      f'<span class="big">Access to firearms</span>{esc(C.FIREARMS)}</aside>')
    a('</div></section>')

    # Actions taken (donuts)
    a('<section aria-labelledby="act-h"><h2 id="act-h">Actions taken to reduce risk</h2>')
    a(donut_pair(C.ACTION_TAKEN, P.BLUE))
    a('</section>')

    # Reasons for inaction
    a('<section aria-labelledby="noact-h">'
      '<h2 id="noact-h">Why some respondents did not take action</h2>')
    a(bar_chart(C.REASONS_INACTION, "bar-inaction",
                desc="Approximate share of respondents giving each reason for not "
                     "acting, split by other-directed and self-directed violence."))
    a('</section>')

    # What we learned (accent panel)
    a('<section class="learned" aria-labelledby="learn-h"><h2 id="learn-h">What we learned</h2>'
      '<ul class="takeaways">')
    for t in C.TAKEAWAYS:
        a(f'<li>{esc(t)}</li>')
    a('</ul></section>')

    # Methodology
    a('<section aria-labelledby="meth-h"><h2 id="meth-h">About the survey</h2>')
    a(f'<div class="methodology"><p>{esc(C.METHODOLOGY)}</p></div></section>')

    # Citation
    a('<section aria-labelledby="cite-h"><h2 id="cite-h">Recommended citation</h2>')
    a(f'<p>{esc(C.META["citation"])}</p>')
    a(f'<p>DOI: <a href="{esc(m["doi_url"])}">{esc(m["doi"])}</a> '
      f'&middot; PMID: {esc(m["pmid"])} &middot; '
      f'<a href="{esc(m["study_url"])}">Read the full study</a></p></section>')

    # Disclaimer
    a('<section aria-labelledby="disc-h"><h2 id="disc-h">Disclaimer</h2>')
    a(f'<p>{esc(C.DISCLAIMER)}</p></section>')

    # Editorial note
    a(f'<aside class="editor" aria-labelledby="ed-h">'
      f'<h2 id="ed-h">{esc(C.EDITOR_NOTE["heading"])}</h2>'
      f'<p>{esc(C.EDITOR_NOTE["body"])}</p>'
      f'<p class="crisis">{esc(C.EDITOR_NOTE["crisis"])}</p></aside>')

    a('</div></main>')
    a(f'<footer class="brief"><div class="wrap"><p>{esc(C.DISCLAIMER)}</p>'
      f'<p>Accessible edition generated from a single source of truth; all '
      f'survey figures transcribed faithfully from the original infographic.</p>'
      f'</div></footer>')
    # Interactive accessible pie charts (progressive enhancement). Inlined so the
    # file stays self-contained (zero external requests). If JS is off or this
    # fails, every figure already shows its static SVG + data table.
    a(f'<script>{read_lib("highcharts.js")}</script>')
    a(f'<script>{read_lib("accessibility.js")}</script>')
    a("<script>\n"
      "(function(){\n"
      "  if(!window.Highcharts){return;}\n"
      f"  var specs={json.dumps({**PIE_SPECS, **BAR_SPECS})};\n"
      "  Object.keys(specs).forEach(function(id){\n"
      "    var el=document.getElementById(id);\n"
      "    if(!el){return;}\n"
      "    try{\n"
      "      Highcharts.chart(id,specs[id]);\n"
      "      var fig=el.closest('.chart-figure');\n"
      "      if(fig){fig.classList.add('chart-ready');}\n"
      "    }catch(e){/* keep the static SVG + data table fallback */}\n"
      "  });\n"
      "})();\n"
      "</script>")
    a('</body></html>')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(s), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
