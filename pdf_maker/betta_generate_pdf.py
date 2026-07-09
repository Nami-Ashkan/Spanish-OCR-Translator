#!/usr/bin/env python3
"""
json_to_pdf.py

Reads:
    ../temp/spanish_json.json

Prompts the user for a report name and writes:
    ../report_<name>.pdf

Requires:
    pip install reportlab
"""

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# ------------------------------------------------------------
# Files
# ------------------------------------------------------------

INPUT_FILE = Path("../temp/spanish_json.json")


# ------------------------------------------------------------
# Ask report name
# ------------------------------------------------------------

report_name = input("Enter report name: ").strip()

if not report_name:
    report_name = "output"

OUTPUT_FILE = Path(f"../report_{report_name}.pdf")


# ------------------------------------------------------------
# Read JSON
# ------------------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


# ------------------------------------------------------------
# Styles
# ------------------------------------------------------------

styles = getSampleStyleSheet()

title_style = styles["Heading2"]

lang_style = styles["Heading4"]

text_style = styles["BodyText"]

text_style.spaceAfter = 6

separator_style = styles["Heading5"]

center_style = styles["BodyText"]
center_style.alignment = TA_CENTER


# ------------------------------------------------------------
# PDF
# ------------------------------------------------------------

doc = SimpleDocTemplate(
    str(OUTPUT_FILE),
    pagesize=(21 * cm, 29.7 * cm),  # A4
    leftMargin=1.5 * cm,
    rightMargin=1.5 * cm,
    topMargin=1.5 * cm,
    bottomMargin=1.5 * cm,
)

story = []

usable_width = doc.width

LABEL_WIDTH = 2.8 * cm


# ------------------------------------------------------------
# Process each sentence
# ------------------------------------------------------------

for sentence in data:

    story.append(
        Paragraph(
            f"Sentence {sentence['sent_id']}",
            title_style,
        )
    )

    story.append(Spacer(1, 0.15 * cm))

    story.append(Paragraph("<b>Spanish</b>", lang_style))
    story.append(Paragraph(sentence["sentence_es"], text_style))

    story.append(Spacer(1, 0.1 * cm))

    story.append(Paragraph("<b>English</b>", lang_style))
    story.append(Paragraph(sentence["sentence_en"], text_style))

    story.append(Spacer(1, 0.25 * cm))

    # --------------------------------------------------------
    # Build rows
    # --------------------------------------------------------

    tokens = sentence["tokens"]

    rows = []

    current_word = ["<b>Word</b>"]
    current_eng = ["<b>English</b>"]
    current_pos = ["<b>POS</b>"]

    widths = [LABEL_WIDTH]

    current_width = LABEL_WIDTH

    # estimate available width
    available = usable_width

    for token in tokens:

        word = token["form"]
        eng = token["lemma_en"]
        pos = token["upos"]

        # Estimate column width from longest string
        longest = max(len(word), len(eng), len(pos))

        col_width = max(1.3 * cm, longest * 0.22 * cm)

        # wrap to new table row if needed
        if current_width + col_width > available:

            rows.append(current_word)
            rows.append(current_eng)
            rows.append(current_pos)

            current_word = ["<b>Word</b>"]
            current_eng = ["<b>English</b>"]
            current_pos = ["<b>POS</b>"]

            widths = [LABEL_WIDTH]
            current_width = LABEL_WIDTH

        current_word.append(word)
        current_eng.append(eng)
        current_pos.append(pos)

        widths.append(col_width)
        current_width += col_width

    rows.append(current_word)
    rows.append(current_eng)
    rows.append(current_pos)

    # --------------------------------------------------------
    # Recompute widths for final rows
    # --------------------------------------------------------

    max_cols = max(len(r) for r in rows)

    col_widths = [LABEL_WIDTH]

    for c in range(1, max_cols):

        longest = 4

        for r in rows:
            if c < len(r):
                txt = str(r[c]).replace("<b>", "").replace("</b>", "")
                longest = max(longest, len(txt))

        col_widths.append(max(1.3 * cm, longest * 0.22 * cm))

    table = Table(
        rows,
        colWidths=col_widths,
        repeatRows=0,
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("BACKGROUND", (0, 3), (-1, 3), colors.whitesmoke),
                ("BACKGROUND", (0, 6), (-1, 6), colors.whitesmoke),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 0.25 * cm))

    story.append(
        Paragraph(
            "-" * 90,
            separator_style,
        )
    )

    story.append(Spacer(1, 0.6 * cm))


# ------------------------------------------------------------
# Build PDF
# ------------------------------------------------------------

doc.build(story)

print(f"PDF written to:\n{OUTPUT_FILE}")
