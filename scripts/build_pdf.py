#!/usr/bin/env python3
"""Render the accessible HTML to a tagged PDF/UA-1 file via WeasyPrint.

PDF accessibility tracks the source HTML's structure, so all the semantic work
lives upstream in build_html.py. WeasyPrint runs no JavaScript; the document is
static HTML + CSS, so what prints is exactly what the markup describes.
"""

from pathlib import Path

from weasyprint import HTML

DOC = Path(__file__).resolve().parent.parent / "document"
SRC = DOC / "CSaWS_SocialNetwork.html"
OUT = DOC / "CSaWS_SocialNetwork_accessible.pdf"


def build():
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}; run build_html.py first")
    HTML(filename=str(SRC)).write_pdf(
        str(OUT),
        pdf_variant="pdf/ua-1",
    )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
