#!/usr/bin/env python3
"""Verify the generated PDF carries the PDF/UA-1 accessibility scaffolding.

Catalog and structure tree live in compressed object streams, so raw byte
grepping is unreliable -- we inspect the parsed objects with pikepdf instead.
"""

from pathlib import Path

import pikepdf

PDF = Path(__file__).resolve().parent.parent / "document" / "CSaWS_SocialNetwork_accessible.pdf"


def main():
    pdf = pikepdf.open(str(PDF))
    root = pdf.Root
    checks = []

    checks.append(("MarkInfo/Marked true",
                   "/MarkInfo" in root and bool(root.MarkInfo.get("/Marked", False))))
    checks.append(("StructTreeRoot present", "/StructTreeRoot" in root))
    checks.append(("Document /Lang set", "/Lang" in root))
    vp = root.get("/ViewerPreferences", {})
    checks.append(("ViewerPreferences/DisplayDocTitle true",
                   bool(vp.get("/DisplayDocTitle", False))))

    # Count Figure structure elements and their /Alt text (we have decorative
    # SVGs marked aria-hidden, so we mainly care that any /Figure has /Alt).
    figures = 0
    figures_with_alt = 0

    def walk(node):
        nonlocal figures, figures_with_alt
        if not isinstance(node, pikepdf.Dictionary):
            return
        if node.get("/S") == "/Figure":
            figures += 1
            if "/Alt" in node:
                figures_with_alt += 1
        kids = node.get("/K")
        if isinstance(kids, pikepdf.Array):
            for k in kids:
                walk(k)
        elif isinstance(kids, pikepdf.Dictionary):
            walk(kids)

    if "/StructTreeRoot" in root:
        walk(root.StructTreeRoot)

    # XMP pdfuaid marker
    try:
        meta = pdf.open_metadata()
        xmp = str(meta)
        ua_part = "pdfuaid" in xmp
    except Exception:
        ua_part = False
    checks.append(("XMP pdfuaid marker present", ua_part))

    print(f"PDF: {PDF}")
    print(f"pages: {len(pdf.pages)}")
    print(f"/Figure elements: {figures} (with /Alt: {figures_with_alt})")
    print("-" * 48)
    ok = True
    for name, passed in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    if figures and figures_with_alt < figures:
        print(f"[WARN] {figures - figures_with_alt} Figure(s) missing /Alt")
    print("-" * 48)
    print("PDF/UA scaffolding:", "OK" if ok else "INCOMPLETE")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
