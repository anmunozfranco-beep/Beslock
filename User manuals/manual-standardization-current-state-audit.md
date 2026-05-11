# Manual standardization current-state audit

## 1. PROJECT PURPOSE & DESIGN PHILOSOPHY

### 1.1 Observed purpose
- The repository treats manual work as a reusable OCR-to-structured-content pipeline plus product-facing documentation assets, not as one-off files. This is explicit in the OCR tooling docs and root README (`tools/manual_ocr/README.md:1-4`, `README.md:144-160`).
- The e-Orbit project pack frames documentation as an implementation system spanning editorial closure, technical validation, CMS loading, and visual production (`User manuals/e-Orbit project/00-paquete-maestro.md:5-13`, `User manuals/e-Orbit project/00-paquete-maestro.md:17-29`).

### 1.2 Core philosophy inferred from implementation
- **Standardize first, then adapt per product:** repeated per-product image prompt/matrix/starter-pack files exist for e-Flex, e-Nova, e-Orbit, e-Prime, e-Shield, and e-Touch with shared structure and product-specific tokens (`User manuals/e-Flex - image generation matrix.md:1-33`, `User manuals/e-Nova - image generation matrix.md:1-33`, `User manuals/e-Prime - image generation matrix.md:1-33`, `User manuals/e-Shield - image generation matrix.md:1-33`, `User manuals/e-Touch - image generation matrix.md:1-33`).
- **Practical editorial quality over theoretical completeness:** e-Orbit editorial guidance emphasizes clarity, actionability, and explicit uncertainty marking (`User manuals/e-Orbit project/01-guia-estilo-editorial.md:9-15`, `User manuals/e-Orbit project/01-guia-estilo-editorial.md:35-42`).
- **Parallel content+visual production:** starter packs explicitly recommend beginning implementation with structured content and stable filenames while visuals are produced in parallel (`User manuals/e-Orbit - implementation starter pack.md:160-167`, `User manuals/e-Flex - implementation starter pack.md:15-16`).

## 2. CURRENT REPOSITORY STRUCTURE

### 2.1 Subtree organization (`User manuals/`)
- Source manuals are OEM-style PDFs (referenced by exact filename in product mappings and batch outputs): `e-Flex`, `e-Nova`, `e-Orbit`, `e-Prime`, `e-Shield`, `e-Touch` (`wp-content/themes/beslock-custom/data/product-manual-features.php:5`, `:30`, `:59`, `:84`, `:117`, `:154`; `generated_manuals/batch_summary.json:3-10`).
- The subtree includes:
  - Per-product AI prompt docs.
  - Per-product image-generation matrices.
  - Per-product implementation starter packs.
  - A deep e-Orbit project pack (editorial/visual/CMS/backlog/plan docs).
  - Product asset placeholder folders under `User manuals/assets/<slug>/` with README conventions (`User manuals/assets/e-orbit/README.md:3-11`).

### 2.2 Adjacent pipeline structure outside subtree (directly connected)
- Batch entrypoint: `process_manuals.py` (`process_manuals.py:14-22`, `:64-96`).
- OCR engine and normalization logic: `tools/manual_ocr/extract_manual.py` (`tools/manual_ocr/extract_manual.py:1-10`, `:947-1099`).
- Generated artifacts in `generated_manuals/<slug>/` and tracked via selective `.gitignore` rules (`.gitignore:3-13`).
- Legacy/sandbox run output also exists under `output/e-orbit/` (including extraction log), indicating iterative pipeline evolution (`output/e-orbit/extraction.log:1-16`).

## 3. CONTENT PIPELINE

### 3.1 Ingestion and orchestration
1. PDFs are discovered from `User manuals/` (or any input path) via recursive discovery (`process_manuals.py:16-17`, `:67-70`; `tools/manual_ocr/extract_manual.py:282-287`).
2. Product slug output folders are generated from filename normalization (e.g., remove “user manual”, kebab-case) (`tools/manual_ocr/extract_manual.py:290-295`).
3. Batch mode writes summaries (`batch_summary.json`, `batch_report.md`) with pass/fail status (`process_manuals.py:25-37`, `:39-62`, `:94-96`; `generated_manuals/batch_report.md:1-18`).

### 3.2 OCR extraction stack (current)
- PDF type detection uses text-density and image-heavy heuristics (`tools/manual_ocr/extract_manual.py:303-320`).
- Multi-stage OCR strategy is explicit and resilient:
  1. OCRmyPDF (`:328-349`, `:989-1004`)
  2. pdf2image+pytesseract fallback with per-page preprocessing and confidence (`:375-429`, `:1014-1029`)
  3. PyMuPDF native fallback (`:431-440`, `:1031-1045`)
- This same staged behavior is documented for operators in README (`tools/manual_ocr/README.md:93-101`).

### 3.3 Cleanup, semantic normalization, and restructuring
- Noise cleanup and spacing normalization are first-class functions (`tools/manual_ocr/extract_manual.py:461-470`, `:473-479`).
- Heuristic filters remove page numbers/symbol noise and preserve valid short tokens like “app/paso” (`tools/manual_ocr/extract_manual.py:482-531`, `:134-135`).
- Semantic section categorization spans Installation/Configuration/Operation/Specifications/App/Troubleshooting/etc. (`tools/manual_ocr/extract_manual.py:159-169`, `:551-556`).
- Structured detectors extract specs, ordered steps, app instructions, warnings, features, troubleshooting candidates (`tools/manual_ocr/extract_manual.py:602-674`).

### 3.4 Markdown/JSON artifact generation
- Markdown output is generated with OCR metadata, section rendering, warning blocks, and synthesized sections (Features, Technical Specifications, Setup Steps, App Setup, Troubleshooting) (`tools/manual_ocr/extract_manual.py:681-755`).
- JSON output is normalized (`ManualStructure`) with metadata and downstream use hints (`tools/manual_ocr/extract_manual.py:193-207`, `:757-796`).
- Quality report generation includes method history, quality notes, missing expected section checks, and downstream readiness (`tools/manual_ocr/extract_manual.py:808-920`).

### 3.5 Current-state evidence from generated outputs
- All six manuals processed successfully in the latest tracked batch (`generated_manuals/batch_summary.json:3-13`).
- Method/quality vary by manual: e-Orbit reached `ocrmypdf` + Good quality (`generated_manuals/e-orbit/extraction_report.md:12-19`, `:23-25`), while e-Nova/e-Shield fell back to pytesseract with acceptable quality and OCRmyPDF invalid-PDF warnings (`generated_manuals/e-nova/extraction_report.md:12-15`, `:23-48`; `generated_manuals/e-shield/extraction_report.md:12-15`, `:23-60`).

### 3.6 Reusable content blocks and website integration
- Reports explicitly position artifacts for WooCommerce pages, FAQs, and installation guides (`generated_manuals/e-orbit/extraction_report.md:121-126`; same template in tool code `tools/manual_ocr/extract_manual.py:913-917`).
- Current live integration appears manual-curated: product feature rows are stored in a PHP catalog keyed by product slug and source PDF filename (`wp-content/themes/beslock-custom/data/product-manual-features.php:3-6`, `:58-60`, `:153-155`).
- Theme logic loads this catalog and prioritizes it over post meta (`wp-content/themes/beslock-custom/inc/woocommerce/product-features.php:13-33`, `:55-63`, `:158-169`).

## 4. IMAGE PIPELINE

### 4.1 Source, extracted, and regenerated image layers
- **Source layer:** OEM PDFs under `User manuals/` (referenced by filename in catalog and batch summary) (`wp-content/themes/beslock-custom/data/product-manual-features.php:5`, `:30`, `:59`; `generated_manuals/batch_summary.json:3-10`).
- **OCR-extracted layer:** `generated_manuals/<slug>/extracted_images/page_###.png` produced during pytesseract fallback (`tools/manual_ocr/extract_manual.py:410-412`).
- **AI-regenerated layer:** prompt and matrix docs define synthetic assets by deterministic names (`User manuals/e-Orbit - AI image prompts.md:6-7`, `:249-259`; `User manuals/e-Nova - AI image prompts.md:5`, `:14`, `:20`).

### 4.2 Current extracted-image behavior (evidence)
- Extracted page images are present for at least e-Nova and e-Shield in tracked artifacts (`generated_manuals/e-nova/extracted_images/page_001.png`, `generated_manuals/e-shield/extracted_images/page_001.png`).
- Other manuals show empty/placeholder extracted-image folders in tracked outputs, which aligns with method differences reported across manuals (`generated_manuals/e-nova/extraction_report.md:12-13`, `generated_manuals/e-orbit/extraction_report.md:12-13`).

### 4.3 Prompt systems and matrix controls
- e-Orbit has a full production-grade image system with per-image prompts, negative prompts, format guidance, variant strategy, and generation order (`User manuals/e-Orbit - AI image prompts.md:4-17`, `:227-246`, `:249-259`).
- Other products currently use a lighter template (short prompt set + prioritized categories), suggesting staged maturity (`User manuals/e-Shield - AI image prompts.md:4-24`, `User manuals/e-Prime - AI image prompts.md:4-24`).

### 4.4 Visual asset reuse and naming conventions
- Asset README files define strict filename conventions: lowercase, hyphenated, no accents/spaces, descriptive names (`User manuals/assets/e-orbit/README.md:14-21`).
- They also define page-to-image mapping and IA-to-real replacement strategy (`User manuals/assets/e-orbit/README.md:62-74`, `:87-88`).
- Folder strategy is intentionally minimal now, with optional future split (`ai-generated`, `real-captures`, `web-ready`, `thumbnails`) when volume grows (`User manuals/assets/e-orbit/README.md:46-59`).

## 5. MANUAL STANDARDIZATION SYSTEM

### 5.1 System components currently in place
- **Extraction engine:** robust OCR and normalization implementation (`tools/manual_ocr/extract_manual.py:245-275`, `:986-1099`).
- **Batch operational wrapper:** one-command processing of all manuals (`process_manuals.py:64-96`; `README.md:148-152`).
- **Structured outputs:** raw text, md draft, json schema, quality report, extracted images (`README.md:154-160`; `.gitignore:8-13`).
- **Editorial controls:** e-Orbit validation checklist and style guides (`User manuals/e-Orbit - manual validation checklist.md:9-19`, `:22-33`; `User manuals/e-Orbit project/01-guia-estilo-editorial.md:35-42`).
- **Visual controls:** image matrix/prompt/starter-pack triad per product (`User manuals/e-Flex - image generation matrix.md:1-33`, `User manuals/e-Flex - AI image prompts.md:1-24`, `User manuals/e-Flex - implementation starter pack.md:1-16`).

### 5.2 Standardization vs flexibility balance
- Standardized skeleton repeats across products (same document families, same asset naming pattern) (`User manuals/e-Flex - implementation starter pack.md:1-16`, `User manuals/e-Touch - implementation starter pack.md:1-16`).
- Flexibility is preserved via product-specific names, slugs, and path mappings (`User manuals/e-Nova - AI image prompts.md:5`, `:14`, `:20`; `User manuals/e-Orbit - implementation starter pack.md:19-30`).
- e-Orbit serves as a “reference implementation” with deeper editorial and operational detail than other products (`User manuals/e-Orbit - image generation matrix.md:62-76`, `:79-256`; `User manuals/e-Orbit project/README.md:20-26`).

## 6. EXISTING CONVENTIONS

### 6.1 Naming and path conventions
- Product slugs are kebab-case (`e-orbit`, `e-nova`, etc.) and reused across OCR outputs and asset naming (`tools/manual_ocr/extract_manual.py:290-295`; `User manuals/assets/e-orbit/README.md:23-33`).
- Suggested CMS URL taxonomy is stable and hierarchical (`/productos/<slug>/...`) (`User manuals/e-Orbit - implementation starter pack.md:19-30`, `:55-94`).

### 6.2 Editorial conventions
- Action-first step writing, consistent product/app names, and prudent handling of uncertain technical points (`User manuals/e-Orbit project/01-guia-estilo-editorial.md:35-42`; `User manuals/e-Orbit user manual.md:154-156`).
- Validation checklists include editorial, technical, visual, and structure gates (`User manuals/e-Orbit - manual validation checklist.md:9-63`).

### 6.3 Output-tracking conventions
- Only core generated artifacts are committed; other runtime artifacts remain ignored (`.gitignore:3-13`).
- OCR tooling itself also keeps local virtualenv/output untracked (`tools/manual_ocr/.gitignore:1-4`).

## 7. CURRENT MATURITY ASSESSMENT

### 7.1 What is mature now
- OCR ingestion architecture is mature and fault-tolerant (multi-engine with staged fallback and quality reporting) (`tools/manual_ocr/extract_manual.py:986-1045`, `:808-920`).
- Batch operations and artifact contract are clear and documented (`process_manuals.py:14-22`, `:94-96`; `tools/manual_ocr/README.md:44-51`, `:60-70`).
- Product feature consumption in WordPress is production-usable through curated PHP catalog + normalization (`wp-content/themes/beslock-custom/inc/woocommerce/product-features.php:13-33`, `:92-145`, `:158-173`).

### 7.2 What is partially mature
- Manual standardization artifacts are uneven: e-Orbit is deep and operationally detailed, while other product packs are currently lightweight templates (`User manuals/e-Orbit - image generation matrix.md:79-256` vs `User manuals/e-Nova - image generation matrix.md:16-33`).
- Image production pipeline controls are defined, but `User manuals/assets/*` currently hold only README guidance (no committed final visual files yet) (`User manuals/assets/e-orbit/README.md:3-11`; `User manuals/assets/e-shield/README.md:3-11`).

## 8. CURRENT BOTTLENECKS

1. **OCR reliability variance by source PDF quality/tool behavior**
   - OCRmyPDF succeeds for some manuals but fails/produces invalid searchable output for others, triggering fallback and “Acceptable” quality outcomes (`generated_manuals/e-orbit/extraction_report.md:12-15`, `:23-25`; `generated_manuals/e-nova/extraction_report.md:23-48`; `generated_manuals/e-shield/extraction_report.md:23-60`).
2. **Semantic extraction noise still present in difficult manuals**
   - Section indexes contain OCR-garbled headings in some outputs, increasing editorial cleanup load (`generated_manuals/e-nova/extraction_report.md:62-70`; `generated_manuals/e-shield/extraction_report.md:74-103`).
3. **Editorial system depth concentrated in a single product (e-Orbit)**
   - e-Orbit has full project governance docs, while other products mostly have concise prompt/matrix/starter templates (`User manuals/e-Orbit project/00-paquete-maestro.md:17-29`; `User manuals/e-Flex - implementation starter pack.md:1-16`).
4. **No evident automated bridge from `generated_manuals/*.json` into theme catalog**
   - OCR reports claim downstream readiness, but current theme integration reads `product-manual-features.php` directly (`tools/manual_ocr/extract_manual.py:913-917`; `wp-content/themes/beslock-custom/inc/woocommerce/product-features.php:22-29`, `:158-169`).

## 9. HIGH-VALUE UPGRADE OPPORTUNITIES

> Framed as compatible next steps within current architecture (not redesign).

1. **Add a lightweight “artifact promotion” convention from OCR outputs to curated product catalog**
   - Compatible because current system already separates generated artifacts from curated feature rows (`.gitignore:3-13`; `wp-content/themes/beslock-custom/data/product-manual-features.php:3-6`).
   - Opportunity: codify a review step that maps approved `manual.json` fields into the existing PHP catalog structure.

2. **Standardize the e-Orbit governance pack pattern across remaining products incrementally**
   - Compatible with existing template family and naming conventions (`User manuals/e-Orbit project/README.md:9-17`; `User manuals/e-Nova - implementation starter pack.md:1-16`).
   - Opportunity: replicate checklist/editorial/visual/seed/backlog layers where product complexity justifies it.

3. **Introduce extraction-quality triage thresholds for editorial workload planning**
   - Compatible with existing confidence + quality report outputs (`tools/manual_ocr/extract_manual.py:798-806`, `:824-905`).
   - Opportunity: use current `Good/Acceptable/Poor/Failed` and section-missing flags to drive whether a manual goes straight to editorial or needs deeper OCR rework.

4. **Operationalize asset-folder lifecycle already documented**
   - Compatible with current assets README recommendations (`User manuals/assets/e-orbit/README.md:46-59`, `:87-88`).
   - Opportunity: start populating `ai-generated` and `real-captures` subfolders only when production volume requires it, preserving current lightweight state.

5. **Keep iterative pipeline comparisons explicit (as shown by `output/e-orbit` vs `generated_manuals/e-orbit`)**
   - Compatible with current evidence of iterative improvement (`output/e-orbit/extraction_report.md:12-19` vs `generated_manuals/e-orbit/extraction_report.md:12-19`).
   - Opportunity: preserve this compare-and-promote practice as a QA pattern when OCR logic is tuned.

## 10. OUTPUT FORMAT

### 10.1 Current canonical outputs (per manual)
- `manual_raw.txt` (raw/cleaned OCR text) (`tools/manual_ocr/extract_manual.py:932`).
- `manual.md` (structured markdown draft) (`tools/manual_ocr/extract_manual.py:933`).
- `manual.json` (normalized schema for downstream integrations) (`tools/manual_ocr/extract_manual.py:936-939`).
- `extraction_report.md` (quality and method trace) (`tools/manual_ocr/extract_manual.py:934`, `:808-920`).
- `extracted_images/` (OCR preprocessing page images when applicable) (`tools/manual_ocr/extract_manual.py:978-980`, `:410-412`).

### 10.2 Batch-level outputs
- `generated_manuals/batch_summary.json` and `generated_manuals/batch_report.md` summarize run success/failure (`process_manuals.py:35-37`, `:61`, `:94`; `generated_manuals/batch_summary.json:1-14`).

### 10.3 Current editorial-delivery formats in `User manuals/`
- Product-facing manuals: OEM PDFs and e-Orbit markdown manuals (`User manuals/e-Orbit user manual.md:1-5`, `User manuals/e-Orbit user manual - image-ready.md:1-8`).
- Visual-production formats: matrix docs, AI prompt packs, starter packs, per-product asset README contracts (`User manuals/e-Orbit - image generation matrix.md:1-5`, `User manuals/e-Orbit - AI image prompts.md:1-3`, `User manuals/assets/e-orbit/README.md:14-21`).
