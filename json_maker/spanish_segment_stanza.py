#!/usr/bin/env python3

import json
from pathlib import Path

import stanza

# --------------------------------------------------
# Configuration
# --------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

INPUT_FILE = PROJECT_DIR / "temp" / "ocr_out.txt"
OUTPUT_FILE = PROJECT_DIR / "temp" / "tex_json.json"

# --------------------------------------------------

def build_pipeline():
    return stanza.Pipeline(
        lang="es",
        processors="tokenize,pos,lemma,depparse",
        use_gpu=False,
    )


def doc_to_json(doc):
    sentences_out = []

    for i, sent in enumerate(doc.sentences, start=1):
        sent_data = {
            "sent_id": i,
            "text": sent.text,
            "tokens": [],
        }

        for w in sent.words:
            sent_data["tokens"].append({
                "id": w.id,
                "text": w.text,
                "lemma": w.lemma,
                "upos": w.upos,
                "xpos": w.xpos,
                "feats": w.feats,
                "head": w.head,
                "deprel": w.deprel,
                "start_char": w.start_char,
                "end_char": w.end_char,
            })

        sentences_out.append(sent_data)

    return sentences_out


def main():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    text = INPUT_FILE.read_text(encoding="utf-8")

    if not text.strip():
        raise ValueError("Input file is empty.")

    nlp = build_pipeline()

    doc = nlp(text)

    data = doc_to_json(doc)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Saved output to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
