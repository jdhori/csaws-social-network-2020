#!/usr/bin/env python3
"""Generate the Markdown deliverable from content.py (the single source of truth)."""

from pathlib import Path

import content as C

OUT = Path(__file__).resolve().parent.parent / "document" / "CSaWS_SocialNetwork.md"


def pct_table(title, rows, footnote_marker=None):
    lines = [f"| {title} | Percent |", "| --- | ---: |"]
    for label, pct in rows:
        mark = " \\*" if (footnote_marker and label == "Nonbinary") else ""
        lines.append(f"| {label}{mark} | {pct}% |")
    return "\n".join(lines)


def reasons_table(block):
    lines = [
        "| Reason | Other-directed violence | Self-directed violence |",
        "| --- | --- | --- |",
    ]
    for cat, other, selfd in block["rows"]:
        lines.append(f"| {cat} | {other} bar | {selfd} bar |")
    return "\n".join(lines)


def build():
    m = C.META
    out = []
    w = out.append

    w(f"# {m['title']}")
    w("")
    w(f"**{m['subtitle']}**")
    w("")
    w(f"_{m['publisher']} - {m['date']}_")
    w("")

    w("## The question we asked")
    w("")
    w(C.QUESTION)
    w("")

    w("## Key finding")
    w("")
    w(f"**{C.HEADLINE['stat']}** {C.HEADLINE['detail']}")
    w("")

    # Other-directed
    w("## Persons at perceived risk of other-directed violence")
    w("")
    w("They were described as follows. Highlights: "
      + "; ".join(C.OTHER_CALLOUTS) + ".")
    w("")
    w("### Relationship to the respondent")
    w("")
    w(pct_table("Relationship", C.OTHER_RELATIONSHIP))
    w("")
    w("### Sex or gender")
    w("")
    w(pct_table("Sex or gender", C.OTHER_GENDER, footnote_marker=True))
    w("")
    w("### Age")
    w("")
    w(pct_table("Age group", C.OTHER_AGE))
    w("")

    # Self-directed
    w("## Persons at perceived risk of self-directed violence")
    w("")
    w("They were described as follows. Highlights: "
      + "; ".join(C.SELF_CALLOUTS) + ".")
    w("")
    w("### Relationship to the respondent")
    w("")
    w(pct_table("Relationship", C.SELF_RELATIONSHIP))
    w("")
    w("### Sex or gender")
    w("")
    w(pct_table("Sex or gender", C.SELF_GENDER, footnote_marker=True))
    w("")
    w("### Age")
    w("")
    w(pct_table("Age group", C.SELF_AGE))
    w("")

    w("> \\* " + C.FOOTNOTES[0])
    w(">")
    w("> Note: " + C.FOOTNOTES[1])
    w("")

    # Likelihood
    w("## Likelihood of harm in the next year")
    w("")
    for item in C.LIKELIHOOD:
        w(f"- **{item['percent']}** {item['text']}")
    w("")

    # Reasons for concern
    w("## Why respondents were concerned")
    w("")
    w(C.REASONS_CONCERN["title"])
    w("")
    w(reasons_table(C.REASONS_CONCERN))
    w("")
    w(f"_Note: {C.REASONS_CONCERN['axis_note']} Bar values below are described "
      "by relative length (for example, \"highest\" or \"low\") because the "
      "original chart shows no exact percentages._")
    w("")

    # Actions taken
    w("## Actions taken to reduce risk")
    w("")
    for item in C.ACTION_TAKEN:
        w(f"- **{item['percent']}** {item['text']}")
    w("")

    # Reasons for inaction
    w("## Why some respondents did not take action")
    w("")
    w(C.REASONS_INACTION["title"])
    w("")
    w(reasons_table(C.REASONS_INACTION))
    w("")
    w(f"_Note: {C.REASONS_INACTION['axis_note']} Bar values are described by "
      "relative length because the original chart shows no exact percentages._")
    w("")

    # Firearms
    w("## Access to firearms")
    w("")
    w(C.FIREARMS)
    w("")

    # Takeaways
    w("## What we learned")
    w("")
    for t in C.TAKEAWAYS:
        w(f"- {t}")
    w("")

    # Methodology
    w("## About the survey")
    w("")
    w(C.METHODOLOGY)
    w("")

    # Citation
    w("## Recommended citation")
    w("")
    w(C.META["citation"])
    w("")
    w(f"DOI: [{m['doi']}]({m['doi_url']}) - PMID: {m['pmid']}")
    w("")

    # Disclaimer
    w("## Disclaimer")
    w("")
    w(C.DISCLAIMER)
    w("")

    # Editorial note
    w(f"## {C.EDITOR_NOTE['heading']}")
    w("")
    w(C.EDITOR_NOTE["body"])
    w("")
    w(f"**{C.EDITOR_NOTE['crisis']}**")
    w("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
