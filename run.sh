#!/bin/bash

set -e

# Change to the directory containing this script
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

echo "========================================"
echo "Step 1: OCR"
echo "========================================"
python3 ocr/ocr_spanish.py

echo
echo "========================================"
echo "Step 2: Sentence segmentation"
echo "========================================"
python3 json_maker/spanish_segment_stanza.py

echo
echo "========================================"
echo "Step 3: Translation"
echo "========================================"
python3 translator/translate_structured.py

echo
echo "========================================"
echo "Step 4: PDF generation"
echo "========================================"
python3 pdf_maker/generate_pdf.py

echo
echo "========================================"
echo "Done!"
echo "========================================"

