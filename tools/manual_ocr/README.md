# OCR manual ingestion workflow

Reusable OCR pipeline for scanned/image-based product manuals.

## Folder layout

```text
tools/manual_ocr/
  extract_manual.py
  requirements.txt
  README.md
```

## Install (macOS)

```bash
# poppler + tesseract
brew install poppler tesseract ocrmypdf

# optional Spanish language data if not present
brew install tesseract-lang

cd /home/runner/work/Beslock/Beslock/tools/manual_ocr
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (single PDF)

```bash
cd /home/runner/work/Beslock/Beslock/tools/manual_ocr
python extract_manual.py \
  --input "/home/runner/work/Beslock/Beslock/User manuals/e-Nova user manual.pdf" \
  --output "/home/runner/work/Beslock/Beslock/tools/manual_ocr/output"
```

Generated output:

```text
output/
  manual_raw.txt
  manual.md
  manual.json
  extracted_images/
```

## Run (batch directory)

```bash
python extract_manual.py \
  --input "/home/runner/work/Beslock/Beslock/User manuals" \
  --output "/home/runner/work/Beslock/Beslock/tools/manual_ocr/output"
```

Batch mode writes each PDF to its own folder inside `output/`.

## CLI options

```text
--input       PDF file or folder with PDFs (required)
--output      Output directory (default: output)
--dpi         OCR render DPI (default: 300)
--language    Tesseract language(s), default spa+eng
--force-ocr   Force OCR even if text is detected
--skip-json   Do not generate manual.json
```

## Workflow behavior

1. Detects scanned/image PDFs using PyMuPDF (text density + image-heavy pages).
2. Uses OCRmyPDF when available to improve OCR source quality.
3. Converts pages to images and applies preprocessing (grayscale, contrast, denoise, threshold) for scanned/manual OCR paths.
4. Runs Tesseract OCR page-by-page for scanned/manual OCR paths.
5. Produces:
   - `manual_raw.txt` (raw extracted text)
   - `manual.md` (clean markdown with section/spec/steps heuristics)
   - `manual.json` (structured representation for downstream integrations)
6. Stores preprocessed page images under `extracted_images/`.

## Structured extraction helpers

The script includes helper functions for:

- OCR noise cleanup
- spacing normalization
- section detection
- specification table detection
- ordered step preservation
- app-instruction candidate detection

## Future integration hooks

`manual.json` is intentionally normalized to ease later mapping to:

- WooCommerce product/manual pipelines
- AI-assisted manual authoring and enrichment workflows
