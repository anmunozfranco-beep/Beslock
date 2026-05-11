# OCR manual ingestion workflow

Reusable OCR pipeline for scanned/image-based product manuals.

## Folder layout

```text
tools/manual_ocr/
  extract_manual.py
  requirements.txt
  README.md
generated_manuals/
  e-orbit/
    manual_raw.txt
    manual.md
    manual.json
    extraction_report.md
    extraction.log
    extracted_images/
```

## Install (Linux / GitHub Codespaces)

```bash
# system dependencies
sudo apt-get install -y tesseract-ocr tesseract-ocr-spa tesseract-ocr-eng poppler-utils

# Python packages
pip install -r tools/manual_ocr/requirements.txt
```

## Install (macOS)

```bash
brew install poppler tesseract ocrmypdf
brew install tesseract-lang  # optional: Spanish language data

cd tools/manual_ocr
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (preferred batch command from repository root)

```bash
python process_manuals.py
```

This command processes all PDFs under `User manuals/` and writes one slugged folder per manual under `generated_manuals/`.

## Run (single PDF → custom output folder)

```bash
python tools/manual_ocr/extract_manual.py \
  --input "User manuals/e-Orbit user manual.pdf" \
  --output "generated_manuals/e-orbit"
```

Generated output:

```text
generated_manuals/e-orbit/
  manual_raw.txt        # raw OCR text
  manual.md             # AI-ready markdown with headings and warnings
  manual.json           # structured JSON for downstream integrations
  extraction_report.md  # quality report summarizing the extraction
  extraction.log        # per-stage debug log
  extracted_images/     # preprocessed page images used for OCR
```

## Run (batch directory via OCR tool)

```bash
python tools/manual_ocr/extract_manual.py \
  --input "User manuals" \
  --output "generated_manuals"
```

Batch mode writes each PDF to its own slugged sub-folder inside `generated_manuals/` (e.g. `generated_manuals/e-orbit/`).

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

1. **PDF type detection** — uses PyMuPDF (text density + image-heavy pages) to decide OCR strategy.
2. **OCR stage 1 — OCRmyPDF** — first attempt; if successful, text is read from the searchable PDF.
3. **OCR stage 2 — pdf2image + pytesseract** — fallback when OCRmyPDF/native extraction fails; converts pages to images, applies preprocessing (grayscale, autocontrast, denoise, threshold), then runs Tesseract page-by-page with confidence scoring.
4. **OCR stage 3 — PyMuPDF native fallback** — used when image-based methods are unavailable.
5. Continues processing even if one stage fails; each failure is logged.
6. Produces all output artifacts plus an extraction quality report.

## Structured extraction helpers

The script includes helper functions for:

- OCR noise cleanup and spacing normalization
- Section detection with semantic categorization (Installation, Configuration, Operation, Specifications, App Instructions, Warnings, Troubleshooting, Maintenance, Features)
- Specification table detection
- Ordered step preservation
- App-instruction candidate detection
- Warning and note detection
- Feature list detection
- OCR confidence estimation via `image_to_data`

## Extraction report

Every run automatically generates `extraction_report.md` summarizing:

- PDF type (scanned vs. text-based)
- Pages processed
- OCR methods attempted and their success/failure
- Average confidence score and quality rating
- Detected semantic section categories
- Downstream readiness notes

## Integration hooks

`manual.json` is intentionally normalized to ease later mapping to:

- WooCommerce product/manual pipelines
- AI-assisted manual authoring and enrichment workflows
- FAQ and installation guide generation
