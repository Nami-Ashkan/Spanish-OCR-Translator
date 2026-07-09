#!/usr/bin/env python3
"""
json_to_pdf.py

Reads:
    temp/spanish_json.json

Prompts the user for a report name.

Writes:
    report_<name>.pdf

Works correctly whether run directly or from run.sh.
"""

import json
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

INPUT_JSON = PROJECT_DIR / "temp" / "spanish_json.json"


def safe_filename(name):
    """Remove characters that are not suitable for filenames."""
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", "_", name)
    return name


def main():

    report_name = input("Enter report name: ").strip()

    if not report_name:
        report_name = "report"

    output_pdf = PROJECT_DIR / f"report_{safe_filename(report_name)}.pdf"

    with INPUT_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    styles = getSampleStyleSheet()

    title_style = styles["Heading2"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading3"]

    normal = styles["BodyText"]

    doc = SimpleDocTemplate(
        str(output_pdf),
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    elements = []

    for sentence in data:

        # ----------------------------------------------------
        # Sentence title
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                f"Sentence {sentence['sent_id']}",
                title_style,
            )
        )

        elements.append(Spacer(1, 0.4 * cm))

        # Spanish

        elements.append(
            Paragraph("<b>Spanish</b>", heading_style)
        )

        elements.append(
            Paragraph(sentence["sentence_es"], normal)
        )

        elements.append(Spacer(1, 0.3 * cm))

        # English

        elements.append(
            Paragraph("<b>English</b>", heading_style)
        )

        elements.append(
            Paragraph(sentence["sentence_en"], normal)
        )

        elements.append(Spacer(1, 0.5 * cm))

        # ----------------------------------------------------
        # Vocabulary table
        # ----------------------------------------------------

        table_data = [["Word", "Lemma", "English", "POS"]]

        for token in sentence["tokens"]:
            table_data.append(
                [
                    token["form"],
                    token["lemma"],
                    token["lemma_en"],
                    token["upos"],
                ]
            )

        table = Table(
            table_data,
            colWidths=[5 * cm, 5 * cm, 5 * cm, 2.5 * cm],
            repeatRows=1,
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        elements.append(table)
        elements.append(Spacer(1, 0.8 * cm))

    doc.build(elements)

    print()
    print("PDF created successfully.")
    print(f"Saved to: {output_pdf}")


if __name__ == "__main__":
    main()
