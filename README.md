# Spanish-OCR-Translator
A Python pipeline for OCR, linguistic analysis, English translation, and PDF generation from Spanish text.

# Spanish OCR Translator

An end-to-end Python pipeline that converts Spanish text images into structured bilingual PDF reports using OCR, NLP, translation, and document generation.

The project extracts Spanish text from images, performs linguistic analysis, translates sentences and lemmas into English, and creates a formatted PDF suitable for language learning and text analysis.

---

## Features

- Spanish OCR using **Tesseract**
- OCR text cleaning and normalization
- Sentence segmentation using **spaCy/Stanza**
- Tokenization and linguistic annotation:
  - Word forms
  - Lemmas
  - Universal POS tags
  - Morphological features
- Automatic Spanish → English translation
- Persistent lemma translation cache
- Professional PDF report generation using **ReportLab**
- Complete automated pipeline using a shell script

---

## Pipeline
