"""Deterministic, dependency-free SVG chart generation.

The SVGs produced here are DECORATIVE: every chart is paired with a real data
table that carries the same numbers, and the SVG is marked aria-hidden so
assistive technology reads the table, not the graphic. Because the graphics are
purely visual we can draw them with plain arc math -- no charting library, no
fonts to embed, no network access.

Palettes loosely echo the original infographic (blues for other-directed
violence, greens for self-directed) while meeting >=3:1 non-text contrast
against the white page for adjacent slices.
"""

import math

# Qualitative palettes (color-blind-considerate ordering, distinct lightness
# steps so adjacent slices remain distinguishable without relying on hue alone).
BLUE_PALETTE = ["#0b3d66", "#1f6fb2", "#3a9bd9", "#7fc3e8", "#173a5e", "#5aa9d6"]
GREEN_PALETTE = ["#2f5d1e", "#4f8a32", "#6faa3f", "#9ac45f", "#3f6f24", "#86b94f"]

BLUE = "#1f6fb2"
GREEN = "#4f8a32"


def _polar(cx, cy, r, angle_deg):
    a = math.radians(angle_deg - 90)  # start at 12 o'clock
    return cx + r * math.cos(a), cy + r * math.sin(a)


def pie_svg(data, palette, size=240, inner_ratio=0.0):
    """Return an SVG string for a pie (inner_ratio=0) or donut chart.

    data: list of (label, percent) tuples. Percent values are used for slice
    sizing as-printed; they need not sum to 100 (the chart normalizes by total
    so the visual is proportional, while the table shows the printed numbers).
    """
    total = sum(p for _, p in data) or 1
    cx = cy = size / 2
    r = size / 2 - 2
    inner = r * inner_ratio
    parts = []
    angle = 0.0
    for i, (_label, pct) in enumerate(data):
        frac = pct / total
        sweep = frac * 360
        color = palette[i % len(palette)]
        if frac >= 0.9999:  # single full-circle slice
            parts.append(
                f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" '
                f'fill="{color}"/>'
            )
            angle += sweep
            continue
        large = 1 if sweep > 180 else 0
        x1, y1 = _polar(cx, cy, r, angle)
        x2, y2 = _polar(cx, cy, r, angle + sweep)
        if inner > 0:
            xi1, yi1 = _polar(cx, cy, inner, angle + sweep)
            xi2, yi2 = _polar(cx, cy, inner, angle)
            d = (
                f"M{x1:.2f},{y1:.2f} A{r:.2f},{r:.2f} 0 {large} 1 {x2:.2f},{y2:.2f} "
                f"L{xi1:.2f},{yi1:.2f} A{inner:.2f},{inner:.2f} 0 {large} 0 "
                f"{xi2:.2f},{yi2:.2f} Z"
            )
        else:
            d = (
                f"M{cx:.2f},{cy:.2f} L{x1:.2f},{y1:.2f} "
                f"A{r:.2f},{r:.2f} 0 {large} 1 {x2:.2f},{y2:.2f} Z"
            )
        parts.append(f'<path d="{d}" fill="{color}"/>')
        angle += sweep
    body = "".join(parts)
    return (
        f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" '
        f'role="presentation" aria-hidden="true" focusable="false" '
        f'class="pie">{body}</svg>'
    )


def stat_donut_svg(percent_int, color, size=160, track="#d7d7e0", label=True):
    """Big single-value donut used for the 67% / 85% action stats.

    The percentage is drawn as SVG <text> in the donut's empty center (dark ink
    on the light page) so there is no separately positioned HTML element
    overlapping the ring -- that overlap makes axe-core unable to resolve the
    text background. The whole graphic is aria-hidden; the readable value is
    provided by the adjacent paragraph.
    """
    cx = cy = size / 2
    r = size / 2 - 12
    stroke = 14
    circumference = 2 * math.pi * r
    filled = circumference * (percent_int / 100)
    hole_r = r - stroke / 2 - 1  # solid disc that fills the ring's interior
    text = ""
    if label:
        text = (
            f'<text x="{cx}" y="{cy}" text-anchor="middle" '
            f'dominant-baseline="central" font-size="34" font-weight="800" '
            f'font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" '
            f'fill="#1a1f29">{percent_int}%</text>'
        )
    return (
        f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" '
        f'role="presentation" aria-hidden="true" focusable="false" '
        f'class="donut">'
        f'<circle cx="{cx}" cy="{cy}" r="{r:.2f}" fill="none" '
        f'stroke="{track}" stroke-width="{stroke}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r:.2f}" fill="none" '
        f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
        f'stroke-dasharray="{filled:.2f} {circumference:.2f}" '
        f'transform="rotate(-90 {cx} {cy})"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{hole_r:.2f}" fill="#ffffff"/>'
        f'{text}</svg>'
    )


def legend_swatches(data, palette):
    """Return small inline swatch markup so the decorative pie's colors are
    explained for sighted users (the table remains the accessible source)."""
    items = []
    for i, (label, _pct) in enumerate(data):
        color = palette[i % len(palette)]
        items.append(
            f'<li><span class="swatch" style="background:{color}" '
            f'aria-hidden="true"></span>{label}</li>'
        )
    return '<ul class="legend">' + "".join(items) + "</ul>"
