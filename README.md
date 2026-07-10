# Spanish-OCR-Translator

A Python pipeline for OCR, linguistic analysis, English translation, and PDF generation from Spanish text.

## Overview

Spanish-OCR-Translator is an end-to-end Python pipeline that converts Spanish text images into structured bilingual PDF reports using Optical Character Recognition (OCR), Natural Language Processing (NLP), machine translation, and PDF generation.

The project is designed for language learning and document analysis. It extracts Spanish text from images, analyzes it linguistically, translates it into English, and generates a color-coded PDF report with word-by-word translations and full sentence translations.

---

## Features

### OCR Text Extraction

- Uses Tesseract OCR
- Supports Spanish text images

### OCR Text Cleaning

- Removes common OCR artifacts
- Fixes broken words across lines
- Normalizes punctuation and spacing

### Natural Language Processing

- Sentence segmentation
- Tokenization
- Lemmatization
- Part-of-speech tagging

### Automatic Translation

- Spanish-to-English sentence translation
- Lemma-based word translation
- Persistent translation cache

### PDF Report Generation

Generates a structured bilingual PDF report containing:

- Sentence numbering
- Spanish words
- Word-by-word English translations
- Full English sentence translations
- Automatic word wrapping
- Color-coded formatting
- Custom TrueType font support
- Interactive report naming

---

## Pipeline

```text
Image
  │
  ▼
Tesseract OCR
  │
  ▼
Cleaned Spanish Text
  │
  ▼
Stanza NLP Analysis
  │
  ▼
Structured JSON
  │
  ▼
Spanish → English Translation
  │
  ▼
Interactive PDF Generator
  │
  ▼
Report_<name>.pdf
```

---

## Example Output

```
1.

La      casa      es      grande
the     house     is      big

The house is big.
```

Each generated PDF contains:

- Sentence number
- Spanish words
- Word-by-word English translations
- Full English sentence translation

---

## Project Structure

```text
Spanish-OCR-Translator/
│
├── run.sh
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── ocr/
│   ├── ocr_spanish.py
│   └── test.png
│
├── json_maker/
│   └── spanish_segment_stanza.py
│
├── translator/
│   └── translate_structured.py
│
├── pdf_maker/
│   ├── generate_pdf.py
│   └── AptosDisplay.ttf
│
└── temp/
    └── (generated files)
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Spanish-OCR-Translator.git
cd Spanish-OCR-Translator
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Required Software

### Install Tesseract OCR

Ubuntu:

```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-spa
```

---

## Install Stanza Language Model

```bash
python -c "import stanza; stanza.download('es')"
```

---

## Usage

Place the input image in:

```text
ocr/test.png
```

Run the complete pipeline:

```bash
./run.sh
```

The pipeline performs the following steps:

1. OCR extraction
2. OCR text cleaning
3. Sentence segmentation
4. NLP analysis
5. English translation
6. PDF generation

During PDF generation you will be prompted for a report name:

```text
Enter a name for the report:
```

For example,

```text
Lesson_5
```

produces

```text
Report_Lesson_5.pdf
```

---

## Running Individual Components

### OCR

```bash
python3 ocr/ocr_spanish.py
```

Output:

```text
temp/ocr_out.txt
```

---

### NLP Processing

```bash
python3 json_maker/spanish_segment_stanza.py
```

Output:

```text
temp/text_json.json
```

---

### Translation

```bash
python3 translator/translate_structured.py
```

Output:

```text
temp/spanish_json.json
```

---

### PDF Generation

```bash
python3 pdf_maker/generate_pdf.py
```

The script prompts for a report name and generates:

```text
Report_<name>.pdf
```

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Tesseract OCR | Optical Character Recognition |
| Pillow | Image processing |
| Stanza | Sentence segmentation, tokenization, lemmatization, POS tagging |
| deep-translator | Spanish-to-English translation |
| ReportLab | PDF generation |

---

## Future Improvements

Potential future enhancements include:

- Support for multi-page PDF documents
- OCR confidence visualization
- Automatic image preprocessing
- Clickable vocabulary index
- Verb conjugation and grammar notes
- Export to HTML or EPUB
- Additional language support
- Custom PDF themes and layouts

---

## Requirements

Generate the dependency file with:

```bash
pip freeze > requirements.txt
```

---

## Recommended `.gitignore`

```gitignore
.venv/
__pycache__/
temp/
*.pyc
translator/*cache*.json
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
