#!/usr/bin/env python3
"""
translate_spanish.py

Reads a structured Spanish JSON file (from Stanza or spaCy),
adds English translations for sentences and lemmas,
and writes the translated JSON.

Input:
    ../temp/tex_json.json

Output:
    ../temp/spanish_json.json

First install:
    pip install deep-translator
"""

import json
import os
import time
from deep_translator import GoogleTranslator
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

INPUT_FILE = PROJECT_DIR / "temp" / "tex_json.json"
OUTPUT_FILE = PROJECT_DIR / "temp" / "spanish_json.json"

CACHE_FILE = SCRIPT_DIR / "spanish_lemma_cache.json"


# ----------------------------
# Load / Save Lemma Cache
# ----------------------------

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


# ----------------------------
# Clean lemma
# ----------------------------

def normalize_lemma(lemma):
    if not lemma:
        return lemma
    return lemma.replace("#", "")


# ----------------------------
# Translate lemma with cache
# ----------------------------

def translate_lemma(lemma, translator, cache):
    lemma = normalize_lemma(lemma)

    if lemma in cache:
        return cache[lemma]

    try:
        translation = translator.translate(lemma)
        cache[lemma] = translation
        time.sleep(0.1)  # avoid rate limiting
        return translation
    except Exception:
        return lemma


# ----------------------------
# Main
# ----------------------------

def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    translator = GoogleTranslator(source="es", target="en")

    lemma_cache = load_cache()

    output_data = []

    for sentence in data:

        sentence_text = sentence["text"]

        # Translate full sentence
        try:
            sentence_translation = translator.translate(sentence_text)
            time.sleep(0.2)
        except Exception:
            sentence_translation = sentence_text

        tokens_out = []

        for token in sentence["tokens"]:

            if token["upos"] == "PUNCT":
                lemma_en = token["text"]
            else:
                lemma_en = translate_lemma(
                    token["lemma"],
                    translator,
                    lemma_cache
                )

            token_out = {
                "id": token["id"],
                "form": token["text"],
                "lemma": token["lemma"],
                "lemma_en": lemma_en,
                "upos": token["upos"],
                "feats": token["feats"]
            }

            tokens_out.append(token_out)

        sentence_out = {
            "sent_id": sentence["sent_id"],
            "sentence_es": sentence_text,
            "sentence_en": sentence_translation,
            "tokens": tokens_out
        }

        output_data.append(sentence_out)

    save_cache(lemma_cache)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("Translation complete.")
    print(f"Output written to: {OUTPUT_FILE}")
    print(f"Lemma cache size: {len(lemma_cache)} entries")


if __name__ == "__main__":
    main()
