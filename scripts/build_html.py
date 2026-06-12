#!/usr/bin/env python3
"""Generate the self-contained, accessible (WCAG 2.1 AA) HTML deliverable.

Design goals:
- One file, zero external requests (self-contained; strict CSP).
- Semantic landmarks, single h1, logical heading order, skip link.
- Every chart paired with a real data <table> (caption + scoped headers);
  decorative SVGs are aria-hidden so AT reads the table, not the graphic.
- Print CSS makes the same markup render as a clean tagged PDF via WeasyPrint.
"""

import html
from pathlib import Path

import content as C
import charts

OUT = Path(__file__).resolve().parent.parent / "document" / "CSaWS_SocialNetwork.html"


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


def pie_figure(fig_caption, table_caption, rows, palette, footnote=False):
    svg = charts.pie_svg(rows, palette, size=220)
    legend = charts.legend_swatches(rows, palette)
    return (
        f'<figure class="chart">'
        f'<figcaption>{esc(fig_caption)}</figcaption>'
        f'<div class="chart-row">'
        f'<div class="chart-vis">{svg}{legend}</div>'
        f'<div class="chart-data">{pct_table(table_caption, rows, footnote)}</div>'
        f'</div></figure>'
    )


def stat_block(items, donut=False, color=charts.BLUE):
    cards = []
    for it in items:
        pct = it["percent"]
        vis = ""
        if donut:
            n = int(pct.rstrip("%"))
            vis = (
                f'<div class="donut-wrap">'
                f'{charts.stat_donut_svg(n, color, label=False)}'
                f'<span class="donut-num" aria-hidden="true">{esc(pct)}</span>'
                f'</div>'
            )
        cards.append(
            f'<div class="stat">{vis}'
            f'<p><span class="stat-num">{esc(pct)}</span> {esc(it["text"])}</p>'
            f'</div>'
        )
    return f'<div class="stat-grid">{"".join(cards)}</div>'


def reasons_block(block):
    rows = []
    for cat, other, selfd in block["rows"]:
        rows.append(
            f'<tr><th scope="row">{esc(cat)}</th>'
            f'<td>{esc(other)}</td><td>{esc(selfd)}</td></tr>'
        )
    note = (
        f'{esc(block["axis_note"])} Values describe relative bar length '
        f'(for example "highest" or "low"); the original chart shows no exact '
        f'percentages, so none are given here.'
    )
    return (
        f'<table class="data reasons"><caption>{esc(block["title"])}</caption>'
        f'<thead><tr><th scope="col">Reason</th>'
        f'<th scope="col">Other-directed violence (relative)</th>'
        f'<th scope="col">Self-directed violence (relative)</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
        f'<p class="note">Note: {note}</p>'
    )


# --- CSS --------------------------------------------------------------------

CSS = """
:root{
  color-scheme: light;
  --ink:#1a1f29; --muted:#3d4554; --line:#c9ced9;
  --bg:#ffffff; --panel:#f4f6fb; --brand:#0b2f55; --accent:#1f6fb2;
  --green:#3f6f24; --focus:#b8002e;
  --space:1.25rem; --maxw:60rem;
}
*{box-sizing:border-box}
html{font-size:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.55;}
.skip{position:absolute;left:-999px;top:0;background:var(--brand);color:#fff;
  padding:.6rem 1rem;z-index:10;border-radius:0 0 .4rem 0}
.skip:focus{left:0}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--space)}
a{color:#0a4f8a}
a:focus-visible, summary:focus-visible, th a:focus-visible{
  outline:3px solid var(--focus);outline-offset:2px}
header.brief{background:var(--brand);color:#fff;padding:1.6rem 0}
header.brief h1{margin:0 0 .25rem;font-size:clamp(1.5rem,1rem+2.4vw,2.3rem);line-height:1.15}
header.brief p{margin:.15rem 0;color:#d7e3f1}
main{padding:1.5rem 0 2.5rem}
h2{font-size:clamp(1.25rem,1rem+1.2vw,1.6rem);color:var(--brand);
  border-bottom:3px solid var(--accent);padding-bottom:.25rem;margin:2rem 0 .75rem}
h3{font-size:1.1rem;color:var(--muted);margin:1.25rem 0 .4rem}
.lead{font-size:1.15rem;background:var(--panel);border-left:5px solid var(--accent);
  padding:1rem 1.2rem;border-radius:.3rem}
.headline{font-size:1.3rem}
.headline .big{font-size:2.4rem;font-weight:800;color:var(--accent);
  display:inline-block;margin-right:.4rem}
table.data{border-collapse:collapse;width:100%;margin:.5rem 0 0;font-size:.97rem}
table.data caption{text-align:left;font-weight:700;color:var(--brand);
  padding:.35rem 0;font-size:1.02rem}
table.data th,table.data td{border:1px solid var(--line);padding:.45rem .6rem;text-align:left}
table.data thead th{background:var(--brand);color:#fff;border-color:var(--brand)}
table.data tbody th{background:var(--panel);font-weight:600}
table.data td{text-align:left}
.reasons td{text-transform:capitalize}
figure.chart{margin:1rem 0;background:#fff;border:1px solid var(--line);
  border-radius:.5rem;padding:1rem 1.1rem}
figure.chart figcaption{font-weight:700;color:var(--brand);margin-bottom:.6rem}
.chart-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);
  gap:1.2rem;align-items:start}
.chart-vis{text-align:center}
.pie{max-width:100%;height:auto}
ul.legend{list-style:none;margin:.6rem 0 0;padding:0;text-align:left;
  display:grid;gap:.2rem;font-size:.9rem}
ul.legend .swatch{display:inline-block;width:.85rem;height:.85rem;border-radius:2px;
  margin-right:.45rem;vertical-align:middle;border:1px solid rgba(0,0,0,.25)}
.stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));
  gap:1rem;margin:.75rem 0}
.stat{background:var(--panel);border-radius:.5rem;padding:1.1rem;text-align:center}
.stat .stat-num{font-weight:800;color:var(--accent);font-size:1.2rem}
.donut-wrap{position:relative;width:160px;height:160px;margin:0 auto .5rem}
/* Own solid background so axe-core computes contrast directly (no SVG-overlap
   heuristic). Sits inside the ring's hole; ink-on-white = ~16:1. */
.donut-num{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:7rem;height:7rem;border-radius:50%;background:#fff;display:grid;
  place-items:center;font-size:1.7rem;font-weight:800;color:var(--ink)}
.note{font-size:.88rem;color:var(--muted);margin:.5rem 0 0}
blockquote.fnbox{margin:1rem 0;background:var(--panel);border-left:4px solid var(--line);
  padding:.6rem 1rem;font-size:.9rem;color:var(--muted);border-radius:.3rem}
ul.takeaways, ul.likely{padding-left:1.2rem}
ul.takeaways li, ul.likely li{margin:.4rem 0}
.methodology{background:var(--panel);border-radius:.5rem;padding:1rem 1.2rem}
.editor{border:2px solid var(--accent);border-radius:.5rem;padding:1rem 1.2rem;
  background:#eef4fb;margin-top:2rem}
.editor h2{border:0;margin-top:0}
.crisis{font-weight:700;background:#fff3f4;border:1px solid #e3b6bd;border-radius:.4rem;
  padding:.7rem .9rem;margin-top:.6rem}
footer.brief{border-top:1px solid var(--line);padding:1.5rem 0;color:var(--muted);
  font-size:.88rem}
@media (max-width:640px){
  .chart-row{grid-template-columns:1fr}
}
@media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}}

@media print{
  @page{size:letter;margin:18mm 16mm;
    @top-center{content:"Concerns About Violence Within Social Networks - CSaWS 2020";
      font-size:8pt;color:#555}
    @bottom-right{content:"Page " counter(page) " of " counter(pages);
      font-size:8pt;color:#555}}
  body{font-size:10.5pt}
  .skip{display:none}
  header.brief{background:#0b2f55!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  table.data thead th, table.data tbody th, .stat, .methodology, .lead,
  figure.chart, .editor, .crisis{-webkit-print-color-adjust:exact;print-color-adjust:exact}
  h2{string-set:section content();bookmark-level:1;bookmark-label:content()}
  h3{bookmark-level:2;bookmark-label:content()}
  /* Keep each data table whole and bound to its caption. A table that splits
     across a page break crashes WeasyPrint's PDF/UA tagger
     ("Table wrapper without a table"); the caption break-after is required. */
  table.data{break-inside:avoid}
  table.data caption{break-after:avoid}
  figure.chart, .stat{break-inside:avoid}
}
"""

# Strict CSP: self-contained, no external anything, no inline-event JS needed.
CSP = ("default-src 'none'; img-src data:; style-src 'unsafe-inline'; "
       "font-src data:; base-uri 'none'; form-action 'none'")


def build():
    m = C.META
    P = charts  # palettes
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
<header class="brief"><div class="wrap">
<h1>{esc(m['title'])}</h1>
<p>{esc(m['subtitle'])}</p>
<p>{esc(m['publisher'])} &middot; {esc(m['date'])}</p>
</div></header>
<main id="main"><div class="wrap">
"""

    s = [head]
    a = s.append

    a('<section aria-labelledby="q-h"><h2 id="q-h">The question we asked</h2>')
    a(f'<p class="lead">{esc(C.QUESTION)}</p></section>')

    a('<section aria-labelledby="key-h"><h2 id="key-h">Key finding</h2>')
    a(f'<p class="headline"><span class="big">{esc(C.HEADLINE["stat"])}</span>'
      f'{esc(C.HEADLINE["detail"])}</p></section>')

    # Other-directed
    a('<section aria-labelledby="other-h"><h2 id="other-h">'
      'Persons at perceived risk of other-directed violence</h2>')
    a(f'<p>They were described as follows. Highlights: {esc("; ".join(C.OTHER_CALLOUTS))}.</p>')
    a('<h3>Relationship to the respondent</h3>')
    a(pie_figure("Relationship of the person at perceived risk to the respondent",
                 "Relationship (other-directed violence)", C.OTHER_RELATIONSHIP, P.BLUE_PALETTE))
    a('<h3>Sex or gender</h3>')
    a(pie_figure("Sex or gender of the person at perceived risk",
                 "Sex or gender (other-directed violence)", C.OTHER_GENDER, P.BLUE_PALETTE, footnote=True))
    a('<h3>Age</h3>')
    a(pie_figure("Age of the person at perceived risk",
                 "Age (other-directed violence)", C.OTHER_AGE, P.BLUE_PALETTE))
    a('</section>')

    # Self-directed
    a('<section aria-labelledby="self-h"><h2 id="self-h">'
      'Persons at perceived risk of self-directed violence</h2>')
    a(f'<p>They were described as follows. Highlights: {esc("; ".join(C.SELF_CALLOUTS))}.</p>')
    a('<h3>Relationship to the respondent</h3>')
    a(pie_figure("Relationship of the person at perceived risk to the respondent",
                 "Relationship (self-directed violence)", C.SELF_RELATIONSHIP, P.GREEN_PALETTE))
    a('<h3>Sex or gender</h3>')
    a(pie_figure("Sex or gender of the person at perceived risk",
                 "Sex or gender (self-directed violence)", C.SELF_GENDER, P.GREEN_PALETTE, footnote=True))
    a('<h3>Age</h3>')
    a(pie_figure("Age of the person at perceived risk",
                 "Age (self-directed violence)", C.SELF_AGE, P.GREEN_PALETTE))
    a('</section>')

    # Footnotes
    a(f'<blockquote class="fnbox" id="fn-nb"><p>* {esc(C.FOOTNOTES[0])}</p>'
      f'<p>Note: {esc(C.FOOTNOTES[1])}</p></blockquote>')

    # Likelihood
    a('<section aria-labelledby="like-h"><h2 id="like-h">'
      'Likelihood of harm in the next year</h2><ul class="likely">')
    for it in C.LIKELIHOOD:
        a(f'<li><strong>{esc(it["percent"])}</strong> {esc(it["text"])}</li>')
    a('</ul></section>')

    # Reasons for concern
    a('<section aria-labelledby="why-h"><h2 id="why-h">Why respondents were concerned</h2>')
    a(reasons_block(C.REASONS_CONCERN))
    a('</section>')

    # Actions taken (donuts)
    a('<section aria-labelledby="act-h"><h2 id="act-h">Actions taken to reduce risk</h2>')
    a(stat_block(C.ACTION_TAKEN, donut=True, color=P.BLUE))
    a('</section>')

    # Reasons for inaction
    a('<section aria-labelledby="noact-h"><h2 id="noact-h">'
      'Why some respondents did not take action</h2>')
    a(reasons_block(C.REASONS_INACTION))
    a('</section>')

    # Firearms
    a('<section aria-labelledby="fire-h"><h2 id="fire-h">Access to firearms</h2>')
    a(f'<p class="lead">{esc(C.FIREARMS)}</p></section>')

    # Takeaways
    a('<section aria-labelledby="learn-h"><h2 id="learn-h">What we learned</h2>'
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
    a('</body></html>')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(s), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
