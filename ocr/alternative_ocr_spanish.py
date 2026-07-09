#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import re
import unicodedata
import spacy

# Load the Spanish spaCy model
nlp = spacy.load("es_core_news_sm")

DASH_CHARS = "\u2010\u2011\u2012\u2013\u2014\u2212"  # hyphen, nonbreak, figure, en, em, minus
PIPE_CHARS = "|\uFF5C\u01C0"  # ASCII pipe, fullwidth vertical bar, OCR-confused characters


def normalize_text(raw: str) -> str:
    """Clean common OCR artifacts."""

    # Normalize Unicode
    t = unicodedata.normalize("NFKC", raw)

    # Normalize dash characters
    t = t.translate({ord(c): "-" for c in DASH_CHARS})

    # Remove soft hyphens and zero-width characters
    t = t.replace("\u00AD", "")
    t = re.sub(r"[\u200B-\u200D\uFEFF]", "", t)

    # Replace OCR pipes with spaces
    t = t.translate({ord(c): " " for c in PIPE_CHARS})

    # Remove standalone page/line numbers
    t = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", t)
    t = re.sub(r"(?m)^\s*\d{1,3}\s+(?=\S)", "", t)

    # Join hyphenated words split across lines
    # Example:
    # elec-
    # ción -> elección
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)

    # Convert remaining newlines to spaces
    t = re.sub(r"\s*\n\s*", " ", t)

    # Normalize spacing around standalone hyphens
    t = re.sub(r"\s*-\s*", " - ", t)
    t = re.sub(r"(?:\s-\s){2,}", " - ", t)

    # Remove stray hyphens before punctuation
    t = re.sub(r"\s-\s(?=[,.;:!?])", " ", t)
    t = re.sub(r"(?<=\()\s-\s", " ", t)

    # Remove hyphen at beginning of text
    t = re.sub(r"^\s*-\s+", "", t)

    # Remove hyphen at beginning of sentences
    t = re.sub(r"([.!?…])\s*-\s+(?=\S)", r"\1 ", t)

    # Collapse repeated punctuation
    t = re.sub(r"\.{2,}", ".", t)
    t = re.sub(r";{2,}", ";", t)
    t = re.sub(r":{2,}", ":", t)
    t = re.sub(r"([.;:])(?:\s*[.;:])+", r"\1", t)

    # Normalize whitespace
    t = re.sub(r"[ \t]{2,}", " ", t).strip()

    return t


def run_tesseract(image_path: Path, lang: str) -> str:
    """Run Tesseract OCR."""

    cmd = [
        "tesseract",
        str(image_path),
        "stdout",
        "-l",
        lang,
        "--oem",
        "1",
        "--psm",
        "6",
    ]

    p = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if p.returncode != 0:
        raise RuntimeError(f"Tesseract failed:\n{p.stderr.strip()}")

    return p.stdout.strip()


def rebuild_sentences(text: str) -> str:
    """Split OCR output into sentences using spaCy."""

    doc = nlp(text)
    return "\n".join(sent.text.strip() for sent in doc.sents)


def main():
    parser = argparse.ArgumentParser(
        description="OCR an image into Spanish text."
    )

    parser.add_argument(
        "image",
        type=Path,
        help="Path to image (jpg/png/webp)"
    )

    parser.add_argument(
        "--lang",
        default="spa",
        help="Tesseract language (default: spa)"
    )

    args = parser.parse_args()

    if not args.image.exists():
        raise FileNotFoundError(args.image)

    # Run OCR and clean text
    text = run_tesseract(args.image, args.lang)
    text = normalize_text(text)
    text = rebuild_sentences(text)

    # Save output to ../temp/ocr_out.txt (relative to this script)
    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir.parent / "temp"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "ocr_out.txt"

    with output_file.open("w", encoding="utf-8") as f:
        f.write(text)

    print(text)
    print(f"\nOCR output saved to: {output_file}")


if __name__ == "__main__":
    main()
