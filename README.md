# Spanish-OCR-Translator
A Python pipeline for OCR, linguistic analysis, English translation, and PDF generation from Spanish text.

# Spanish OCR Translator

An end-to-end Python pipeline that converts Spanish text images into structured bilingual PDF reports using OCR, natural language processing (NLP), machine translation, and PDF generation.

The project is designed for language learning and document analysis. It extracts Spanish text from images, analyzes it linguistically, translates it into English, and generates a structured PDF report containing sentence translations and vocabulary information.

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

Generates structured bilingual PDF documents containing:

- Spanish sentence
- English translation
- Word-level vocabulary table
- Lemma
- English meaning
- Part-of-speech (POS) tags

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
PDF Report
```

---

## Example Output

### Sentence

**Spanish**

```text
La casa es grande.
```

**English**

```text
The house is big.
```

### Vocabulary

| Word | Lemma | English | POS |
|------|--------|----------|------|
| La | el | the | DET |
| casa | casa | house | NOUN |
| es | ser | be | VERB |
| grande | grande | big | ADJ |

---

## Project Structure

```text
Spanish-OCR-Translator/
│
├── run.sh
├── README.md
├── requirements.txt
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
│   └── generate_pdf.py
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

## Install Language Models

### spaCy Spanish model

```bash
python -m spacy download es_core_news_sm
```

### Stanza Spanish model

```python
import stanza

stanza.download("es")
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
2. Spanish sentence segmentation
3. NLP analysis
4. Translation
5. PDF generation

The generated report will be saved as:

```text
report_<name>.pdf
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
temp/tex_json.json
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

Output:

```text
report_<name>.pdf
```

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Tesseract OCR | Image text extraction |
| spaCy | Spanish NLP |
| Stanza | Linguistic annotation |
| deep-translator | Spanish-to-English translation |
| ReportLab | PDF generation |

---

## Future Improvements

Potential future enhancements include:

- Support multiple images or PDF documents
- OCR confidence scoring
- Vocabulary difficulty levels
- Verb conjugation tables
- Improved PDF styling using HTML templates
- Support for additional languages

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

This project is licensed under the MIT License.
