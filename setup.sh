#!/bin/bash

set -e

# ------------------------------------------------------------
# Move to the project directory
# ------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "Spanish OCR Translator Setup"
echo "========================================"

# ------------------------------------------------------------
# Check Python
# ------------------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is not installed."
    exit 1
fi

# ------------------------------------------------------------
# Create virtual environment
# ------------------------------------------------------------

echo
echo "Creating virtual environment..."

python3 -m venv .venv

# ------------------------------------------------------------
# Activate virtual environment
# ------------------------------------------------------------

echo "Activating virtual environment..."

source .venv/bin/activate

# ------------------------------------------------------------
# Upgrade pip
# ------------------------------------------------------------

echo
echo "Upgrading pip..."

python -m pip install --upgrade pip

# ------------------------------------------------------------
# Install Python packages
# ------------------------------------------------------------

echo
echo "Installing Python dependencies..."

pip install -r requirements.txt

# ------------------------------------------------------------
# Download spaCy model
# ------------------------------------------------------------

echo
echo "Downloading spaCy Spanish model..."

python -m spacy download es_core_news_sm

# ------------------------------------------------------------
# Download Stanza model
# ------------------------------------------------------------

echo
echo "Downloading Stanza Spanish model..."

python -c "import stanza; stanza.download('es')"

# ------------------------------------------------------------
# Check for Tesseract
# ------------------------------------------------------------

echo

if command -v tesseract >/dev/null 2>&1; then
    echo "✓ Tesseract is installed."
else
    echo "⚠ Tesseract is not installed."
    echo
    echo "Ubuntu:"
    echo "  sudo apt update"
    echo "  sudo apt install tesseract-ocr tesseract-ocr-spa"
fi

echo
echo "========================================"
echo "Setup complete!"
echo
echo "Activate the environment with:"
echo "    source .venv/bin/activate"
echo
echo "Run the project with:"
echo "    ./run.sh"
echo "========================================"
