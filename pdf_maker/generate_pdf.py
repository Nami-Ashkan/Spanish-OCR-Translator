import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import signal
from datetime import datetime

# ==========================================================
# PATH CONFIGURATION
# ==========================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
INPUT_JSON = PROJECT_DIR / "temp" / "spanish_json.json"
OUTPUT_DIR = PROJECT_DIR
FONT_PATH = SCRIPT_DIR / "AptosDisplay.ttf"

# ==========================================================
# USER SETTINGS — COLOR CONFIGURATION (RGB FORMAT)
# ==========================================================

def RGB(r, g, b, alpha=1.0):
    """Helper to convert 0–255 RGB into ReportLab Color."""
    return colors.Color(r / 255, g / 255, b / 255, alpha=alpha)

# Color palette
COLOR_ROW2 = RGB(193, 6, 6)          # Spanish words (Row 2)
COLOR_ROW3 = RGB(51, 68, 219)        # Word-by-word translations (Row 3)
COLOR_ROW4 = RGB(45, 102, 21)        # Full sentence translation (Row 4)
LINE_NUMBER_COLOR = RGB(0, 0, 0)     # Line number color
PAGE_NUMBER_COLOR = RGB(0, 0, 0)     # Page number text
BOX_COLOR = RGB(255, 229, 61, alpha=0.1)  # Box background (translucent)
BOX_BORDER_COLOR = RGB(255, 229, 61)      # Optional border color

FONT_SIZE = 12
BOX_MARGIN = 8
# ==========================================================

class InputTimeout(Exception):
    pass


def timeout_handler(signum, frame):
    raise InputTimeout


def get_report_name(timeout=10):
    """
    Ask the user for a report name.

    If the user presses Enter or does not respond within
    `timeout` seconds, a timestamped name is generated:

        Report_2026_July_10_Friday_14_35
    """

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        name = input(
            f"Enter report name (auto in {timeout} seconds): "
        ).strip()

        signal.alarm(0)

        if name:
            return name

    except InputTimeout:
        print("\nNo input received.")

    finally:
        signal.alarm(0)

    now = datetime.now()

    return (
        f"file_"
        f"{now.year}_"
        f"{now.strftime('%B')}_"
        f"{now.day:02d}_"
        f"{now.strftime('%A')}_"
        f"{now.hour:02d}_"
        f"{now.minute:02d}"
    )

def draw_aligned_words_wrapped(
    c,
    es_words,
    en_words,
    x_start,
    y_start,
    font_name,
    width_limit,
    line_gap,
    draw=True,
):
    """
    Draw (or measure) aligned Spanish and English words.

    Parameters
    ----------
    draw : bool
        True  -> draw on the PDF canvas.
        False -> only calculate layout and return the final y position.

    Returns
    -------
    float
        Lowest y-coordinate reached after layout.
    """

    # Handle missing inputs
    es_words = es_words or []
    en_words = en_words or []

    # Make both lists the same length
    max_len = max(len(es_words), len(en_words))
    es_words = list(es_words) + [""] * (max_len - len(es_words))
    en_words = list(en_words) + [""] * (max_len - len(en_words))

    space_padding = 8

    if draw:
        c.setFont(font_name, FONT_SIZE)

    current_x = x_start
    current_y = y_start
    lowest_y = y_start

    for es_word, en_word in zip(es_words, en_words):

        # Convert everything to strings safely
        es_word = "" if es_word is None else str(es_word)
        en_word = "" if en_word is None else str(en_word)

        es_width = c.stringWidth(es_word, font_name, FONT_SIZE)
        en_width = c.stringWidth(en_word, font_name, FONT_SIZE)

        col_width = max(es_width, en_width) + space_padding

        # Wrap to next line if needed
        if current_x + col_width > width_limit:
            current_x = x_start
            current_y -= line_gap * 2

        if draw:
            # Spanish row
            c.setFont(font_name, FONT_SIZE)
            c.setFillColor(COLOR_ROW2)
            c.drawString(current_x, current_y, es_word)

            if es_width > 0:
                c.setStrokeColor(COLOR_ROW2)
                c.setLineWidth(0.6)
                c.line(
                    current_x,
                    current_y - 1,
                    current_x + es_width,
                    current_y - 1,
                )

            # English row
            c.setFillColor(COLOR_ROW3)
            c.drawString(
                current_x,
                current_y - line_gap,
                en_word,
            )

        current_x += col_width
        lowest_y = min(lowest_y, current_y - line_gap * 2)

    return lowest_y


def draw_wrapped_sentence(
    c,
    sentence,
    x_start,
    y_start,
    font_name,
    width_limit,
    line_gap,
    draw=True,
):
    """
    Draw (or measure) a wrapped sentence.

    Parameters
    ----------
    draw : bool
        True  -> draw the sentence.
        False -> only calculate layout and return the final y position.

    Returns
    -------
    float
        Lowest y-coordinate reached after layout.
    """

    # Handle missing values
    if sentence is None:
        return y_start

    # Convert to string safely
    sentence = str(sentence).strip()

    # Nothing to draw
    if not sentence:
        return y_start

    if draw:
        c.setFont(font_name, FONT_SIZE)
        c.setFillColor(COLOR_ROW4)

    words = sentence.split()

    current_x = x_start
    current_y = y_start
    lowest_y = y_start

    space_width = c.stringWidth(" ", font_name, FONT_SIZE)

    for word in words:

        # Ignore empty words (extra safety)
        if not word:
            continue

        word_width = c.stringWidth(word, font_name, FONT_SIZE)

        # Extremely long single words:
        # place them on a new line if necessary
        if current_x != x_start and current_x + word_width > width_limit:
            current_x = x_start
            current_y -= line_gap

        if draw:
            c.drawString(current_x, current_y, word)

        current_x += word_width + space_width
        lowest_y = min(lowest_y, current_y - line_gap)

    return lowest_y


def draw_box_background(c, x_left, x_right, y_top, y_bottom):
    """Draw translucent box behind each section with padding and vertical correction."""
    vertical_adjust1 = -10
    c.saveState()
    c.setFillColor(BOX_COLOR)
    c.setStrokeColor(colors.transparent)
    c.roundRect(
        x_left - BOX_MARGIN + 5,
        y_bottom - BOX_MARGIN - vertical_adjust1,
        (x_right - x_left) + 2 * BOX_MARGIN,
        (y_top - y_bottom) + 2 * BOX_MARGIN + 0,
        8,
        fill=1,
        stroke=0,
    )
    c.restoreState()


def estimate_pages(
    json_path,
    font_name="AptosDisplay",
    canvas_obj=None,
    margin=50,
    num_col_width=25,
    line_gap=20,
    section_gap=40,
):
    """
    Estimate the number of pages required.

    Compatible with the old version:
        estimate_pages(json_path)
        estimate_pages(json_path, "AptosDisplay")

    or the new version:
        estimate_pages(json_path, canvas_obj=my_canvas)
    """

    # Create a temporary canvas if none is provided
    if canvas_obj is None:
        from reportlab.pdfgen.canvas import Canvas
        import io

        canvas_obj = Canvas(io.BytesIO(), pagesize=A4)

    width, height = A4
    usable_left = margin + num_col_width
    usable_width = width - margin

    y = height - margin
    pages = 1

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        return pages

    canvas_obj.setFont(font_name, FONT_SIZE)

    for entry in data:

        tokens = entry.get("tokens", [])

        es_words = [str(t.get("form", "")) for t in tokens]
        en_words = [str(t.get("lemma_en", "")) for t in tokens]

        sentence = entry.get("sentence_en") or ""

        # Estimate height of word rows
        current_x = usable_left
        word_rows = 1

        for es, en in zip(es_words, en_words):
            col_width = (
                max(
                    canvas_obj.stringWidth(es, font_name, FONT_SIZE),
                    canvas_obj.stringWidth(en, font_name, FONT_SIZE),
                )
                + 8
            )

            if current_x + col_width > usable_width:
                word_rows += 1
                current_x = usable_left

            current_x += col_width

        words_height = word_rows * line_gap * 2

        # Estimate English sentence height
        sentence_rows = 1
        current_x = usable_left

        for word in str(sentence).split():
            word_width = (
                canvas_obj.stringWidth(word, font_name, FONT_SIZE)
                + canvas_obj.stringWidth(" ", font_name, FONT_SIZE)
            )

            if current_x + word_width > usable_width:
                sentence_rows += 1
                current_x = usable_left

            current_x += word_width

        sentence_height = sentence_rows * line_gap

        block_height = words_height + sentence_height + section_gap

        if y - block_height < margin:
            pages += 1
            y = height - margin

        y -= block_height

    return pages


def make_pdf(json_path, font_path, output_path):
    """Generate PDF from Spanish JSON data."""

    if not font_path.exists():
        raise FileNotFoundError(f"Font file not found: {font_path}")

    pdfmetrics.registerFont(TTFont("AptosDisplay", str(font_path)))

    width, height = A4

    margin = 50
    bottom_reserved = 300      # <-- Reserved space for page number and safety margin
    num_col_width = 25

    usable_left = margin + num_col_width
    usable_width = width - margin

    line_gap = 20
    section_gap = 40

    # Load JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_pages = estimate_pages(json_path, "AptosDisplay")

    current_page = 1
    sentence_number = 1

    c = canvas.Canvas(str(output_path), pagesize=A4)

    y = height - margin

    for entry in data:

        sentence_en = entry.get("sentence_en") or ""
        tokens = entry.get("tokens", [])

        es_words = [str(token.get("form", "")) for token in tokens]
        en_words = [str(token.get("lemma_en", "")) for token in tokens]

        # -------------------------------------------------
        # NEW PAGE CHECK
        # Reserve extra space at bottom of page
        # -------------------------------------------------

        if y < bottom_reserved:

            c.setFont("AptosDisplay", 9)
            c.setFillColor(PAGE_NUMBER_COLOR)
            c.drawCentredString(
                width * 0.9,
                margin / 2,
                f"Page {current_page}/{total_pages}",
            )

            c.showPage()

            current_page += 1
            y = height - margin

        # -------------------------------------------------

        y_top = y

        # First pass (measure)
        y_bottom = draw_aligned_words_wrapped(
            c,
            es_words,
            en_words,
            x_start=usable_left,
            y_start=y,
            font_name="AptosDisplay",
            width_limit=usable_width,
            line_gap=line_gap,
        )

        y_bottom = draw_wrapped_sentence(
            c,
            sentence_en,
            x_start=usable_left,
            y_start=y_bottom,
            font_name="AptosDisplay",
            width_limit=usable_width,
            line_gap=line_gap,
        )

        draw_box_background(
            c,
            usable_left,
            usable_width,
            y_top,
            y_bottom,
        )

        # Draw sentence number
        c.setFont("AptosDisplay", FONT_SIZE)
        c.setFillColor(LINE_NUMBER_COLOR)
        c.drawRightString(
            usable_left - 5,
            y_top,
            f"{sentence_number}.",
        )

        # Second pass (actual drawing)
        y_temp = draw_aligned_words_wrapped(
            c,
            es_words,
            en_words,
            x_start=usable_left,
            y_start=y_top,
            font_name="AptosDisplay",
            width_limit=usable_width,
            line_gap=line_gap,
        )

        y_temp = draw_wrapped_sentence(
            c,
            sentence_en,
            x_start=usable_left,
            y_start=y_temp,
            font_name="AptosDisplay",
            width_limit=usable_width,
            line_gap=line_gap,
        )

        y = y_bottom - section_gap
        sentence_number += 1

    # Final page number

    c.setFont("AptosDisplay", 9)
    c.setFillColor(PAGE_NUMBER_COLOR)
    c.drawCentredString(
        width / 2,
        margin / 2,
        f"Page {current_page}/{total_pages}",
    )

    c.save()

    print(f"[OK] PDF saved to: {output_path}")


def main():
    """Main entry point."""
    print(f"[INFO] Script directory: {SCRIPT_DIR}")
    print(f"[INFO] Project directory: {PROJECT_DIR}")
    print(f"[INFO] Input JSON: {INPUT_JSON}")

    if not INPUT_JSON.exists():
        raise FileNotFoundError(f"JSON file not found: {INPUT_JSON}")

    if not FONT_PATH.exists():
        print(f"[WARNING] Font file not found: {FONT_PATH}")
        print("[WARNING] Using system font as fallback.")

    # Ask user for report name
    report_name = get_report_name(timeout=10)

    # Replace invalid filename characters
    invalid_chars = '<>:"/\\|?*'
    for ch in invalid_chars:
        report_name = report_name.replace(ch, "_")

    # Optional: replace spaces with underscores
    report_name = report_name.replace(" ", "_")

    # Create output path
    output_pdf = OUTPUT_DIR / f"Report_{report_name}.pdf"

    print(f"[INFO] Output PDF: {output_pdf}")
    print(f"[INFO] Creating PDF from: {INPUT_JSON}")

    make_pdf(INPUT_JSON, FONT_PATH, output_pdf)


if __name__ == "__main__":
    main()
