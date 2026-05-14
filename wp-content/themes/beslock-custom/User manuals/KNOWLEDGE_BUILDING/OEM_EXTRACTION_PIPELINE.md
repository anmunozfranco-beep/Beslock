# OEM EXTRACTION PIPELINE

Status: Active governance.
Scope: Deterministic OEM ingestion and extraction pipeline for the BESLOCK Product Knowledge Core.
Authoritative tooling: `process_manuals.py`, `tools/manual_ocr/extract_manual.py`, `tools/manual_ocr/README.md`, `tools/generate_reset_review_assets.py`.
Staging area: `generated_manuals/<slug>/`.
Promotion target: `ext-images/<slug>/source-of-truth/` and adjacent nucleus locations.

This pipeline assumes OEM manuals are imperfect. Extracted text requires normalization. Knowledge must become reusable and machine-readable.

---

## 1. Pipeline overview

```
OEM PDFs / sheets / images
        │
        ▼
[1] Discovery & classification
        │
        ▼
[2] PDF ingestion
        │
        ▼
[3] OCR (3-stage, with fallbacks)
        │
        ▼
[4] Multilingual extraction
        │
        ▼
[5] Image & diagram extraction
        │
        ▼
[6] Chunking & section detection
        │
        ▼
[7] Procedural / warning / troubleshooting extraction
        │
        ▼
[8] Semantic cleanup
        │
        ▼
[9] Colombian-Spanish normalization
        │
        ▼
[10] Duplication detection
        │
        ▼
[11] Confidence scoring
        │
        ▼
[12] Metadata extraction
        │
        ▼
[13] Provenance recording
        │
        ▼
[14] Promotion to nucleus
```

Stages 1–13 produce staging artifacts under `generated_manuals/<slug>/`. Stage 14 promotes vetted outputs into the nucleus.

---

## 2. Inputs

Per product:
- One or more OEM PDFs (user manual, installation manual, app manual, datasheets, supplementary references).
- Optional spreadsheets, configuration guides, multilingual references.
- The single canonical product PNG (handled by `tools/generate_reset_review_assets.py`; covered in `PRODUCT_VISUAL_TRUTH.md`, not here).

Naming anomaly tracked in the validation ledger: `e-Shied_2.pdf` (OEM typo, missing `l`). The OEM filename is preserved verbatim in provenance; normalized references use the slug `e-shield`.

---

## 3. Discovery & classification

Step 1 of the pipeline.

- Discover candidate files matching `<slug>*.pdf`, `<Slug>*.pdf`, and known anomalies (`e-Shied_2.pdf`).
- Classify by document type: `user`, `installation`, `app`, `datasheet`, `supplemental`.
- Reject files with zero text and zero rasterizable pages; record the rejection in the per-document extraction report.

Output:
- `generated_manuals/<slug>/discovery.json` — list of input files with declared document type, page count, and SHA-256 hash.

---

## 4. PDF ingestion

Step 2.

- Open each PDF with PyMuPDF.
- Capture: page count, page size, embedded text presence per page, embedded image inventory.
- Decide per-page extraction strategy based on embedded text density:
  - Dense embedded text → direct text extraction.
  - Sparse or no embedded text → rasterize for OCR.
- Write per-page strategy to the extraction report.

Risks:
- Encrypted PDFs (record and skip; flag for manual handling).
- Mixed-orientation pages (must be auto-rotated before OCR).
- Embedded vector text disguised as image (forces OCR fallback).

---

## 5. OCR strategy

Step 3. Three-stage cascade with explicit fallbacks (implemented in `tools/manual_ocr/extract_manual.py`).

1. **OCRmyPDF** (preferred) — produces a searchable PDF and a text layer.
2. **pdf2image + pytesseract** — fallback when OCRmyPDF fails or returns empty pages.
3. **PyMuPDF text extraction** — fallback for pages with embedded text where OCR is unreliable.

Per-page recording:
- Engine used.
- Tesseract language packs invoked (e.g. `spa`, `eng`).
- Confidence score (per-page mean and minimum word confidence when available).
- Fallback chain (e.g. `ocrmypdf -> pytesseract`).

Rules:
- No silent OCR. Every page records its engine and confidence.
- A page with confidence below a configured threshold is flagged in the extraction report and added to the validation ledger as `inferred-but-unverified`.
- OCR output is written to `generated_manuals/<slug>/manual_raw.txt` (concatenated) and `generated_manuals/<slug>/pages/<n>.txt` (per page).

---

## 6. Multilingual extraction

Step 4.

- OEM material may include English, Iberian Spanish, Mexican Spanish, and occasional Mandarin/Korean OEM blocks.
- Tesseract is invoked with the language packs declared in the document classification (default: `spa+eng`).
- Per-page detected language is recorded.
- Foreign-language blocks (e.g. Mandarin) are extracted, marked, and **not** silently translated. Translation is a normalization step (§10), not an extraction step.

Output:
- `generated_manuals/<slug>/multilingual.json` — page → detected language(s) → text block.

---

## 7. Image & diagram extraction

Step 5.

- For every page, extract embedded raster images via PyMuPDF.
- For pages with diagram-like content (vector strokes, schematic geometry), rasterize the page region and store as a candidate diagram.
- Classify candidates: `diagram`, `ui-panel`, `icon`, `installation-figure`, `topology`, `photograph`, `decorative`.
- Decorative candidates are dropped. The rest become OEM visual evidence candidates.

Output:
- `generated_manuals/<slug>/extracted_images/<page>-<index>.png` (or `.jpg` when source is JPEG).
- `generated_manuals/<slug>/visual-evidence-candidates.json` — candidate list with classification and source references.

Rules:
- Extracted images are **not** product truth. The canonical PNG is. Extracted images are secondary visual evidence.
- Extracted images are promoted into `ext-images/<slug>/source-of-truth/visual-evidence/` only after editorial review.

---

## 8. Chunking strategy

Step 6.

- Detect headings using a combination of font size, font weight, position, and known OEM heading patterns.
- Build a section tree per document with stable anchor IDs (`#<n>` numbered in document order).
- Emit chunks at three granularities:
  - Document chunk (whole document).
  - Section chunk (one chunk per detected section).
  - Paragraph chunk (one chunk per paragraph within a section).
- Each chunk records its section path, anchor ID, and source page range.

Output:
- `generated_manuals/<slug>/manual.md` — section-aware markdown rendering.
- `generated_manuals/<slug>/chunks.jsonl` — one JSON object per chunk, with `anchor_id`, `section_path`, `page_range`, `text`, `chunk_level`.

---

## 9. Procedural / warning / troubleshooting extraction

Step 7. Pattern-based candidate extraction (not yet semantic; that is Phase 2).

- **Procedural cues**: numbered lists, imperative verbs at sentence start, menu-path patterns (`Menu -> Submenu`).
- **Warning cues**: keywords (`Advertencia`, `Caution`, `Warning`, `Precaución`, `Important`, `Nota`), iconography in adjacent extracted images.
- **Troubleshooting cues**: section headings matching `Solución de problemas`, `Troubleshooting`, `Problemas comunes`; symptom-resolution table layouts.
- **Specification cues**: spec table layouts and unit-bearing rows (V, A, mm, kg, IP rating).

Output:
- `generated_manuals/<slug>/manual.json` — typed candidates with source anchors.
- `generated_manuals/<slug>/extraction_report.md` — per-document extraction quality summary.

Rules:
- Candidates are **proposals**, not knowledge. They become knowledge only after Phase 2 conversion into entities conforming to `KNOWLEDGE_SCHEMA.md`.
- Every candidate carries source anchor (`<file>#<anchor_id>`).

---

## 10. Semantic cleanup

Step 8.

- Strip OCR artifacts: stray punctuation, repeated whitespace, broken hyphenation across line breaks, page-header/footer pollution.
- Re-join paragraphs split by OCR pagination.
- Normalize bullet markers and numbered-list indentation.
- Detect and remove duplicate page headers/footers across pages.
- Preserve the unmodified raw extraction in `manual_raw.txt`.

Rule: cleanup is reversible (raw is preserved). No claim is deleted; only formatting noise is removed.

---

## 11. Colombian-Spanish normalization

Step 9. Editorial normalization. See `KNOWLEDGE_SCHEMA.md` §7 and `PHASE_1_IMPLEMENTATION.md` §5.

- Resolve regional variants to Colombian-Spanish canonical forms.
- Apply the shared terminology registry.
- Generate glossary candidates for terms not yet in the registry.
- Translate non-Spanish blocks (English, Mandarin, Korean) into Colombian-Spanish, recording the original verbatim in the glossary `oem_variants[]`.
- Emit a normalization diff report so editorial decisions are auditable.

Output:
- `generated_manuals/<slug>/normalized.md` — Colombian-Spanish normalized rendering.
- `generated_manuals/<slug>/normalization-diff.md` — change report (raw → normalized).
- `generated_manuals/<slug>/glossary-candidates.json` — proposed glossary terms.

Rule: normalization never overwrites `manual_raw.txt`. Originals are immutable.

---

## 12. Duplication detection

Step 10.

- Detect duplicate statements across documents of the same product (e.g. user manual and installation manual both stating the same warning).
- Detect near-duplicates using normalized-text similarity (token overlap; threshold configurable).
- Cluster duplicates and choose a canonical statement per cluster, recording rejected duplicates with their source anchors.
- Detect contradictions: same topic, different claims. Contradictions are added to the validation ledger as `blocked-pending-validation`.

Output:
- `generated_manuals/<slug>/duplication-report.json` — clusters with canonical and rejected members, plus contradictions.

---

## 13. Confidence scoring

Step 11.

Per chunk and per candidate:
- OCR confidence (from §5).
- Normalization confidence (heuristic: 1.0 if all terms resolved against registry; lower when glossary candidates were created).
- Source agreement (1.0 when only one document supports the claim; higher when multiple documents agree; lower when contradictions exist).
- Composite confidence = weighted combination, recorded in the candidate.

Mapping to `validation_status`:
- composite ≥ 0.9 and no contradictions → `verified` candidate (subject to editorial review).
- 0.6 ≤ composite < 0.9 → `normalized`.
- composite < 0.6 → `inferred-but-unverified`.
- contradiction present → `blocked-pending-validation`.

Editorial review may upgrade or downgrade status; the pipeline never auto-promotes to `verified` without review.

---

## 14. Metadata extraction

Step 12.

Per document:
- OEM filename (verbatim).
- File hash (SHA-256).
- Page count.
- Detected language(s).
- Document type classification.
- Extraction engine versions used.
- Extraction timestamp.
- Operator (user or CI run ID).

Output:
- `generated_manuals/<slug>/source-metadata.json` — one entry per OEM document.

---

## 15. Provenance preservation

Step 13.

- Every chunk, candidate, image, and glossary candidate carries `source_refs` pointing to the OEM source path and anchor.
- A staging-side lineage manifest is emitted: `generated_manuals/<slug>/staging-lineage.json` mapping raw → normalized → candidate.
- Promotion (Stage 14) merges `staging-lineage.json` into the nucleus `metadata/lineage/source-lineage.json`.
- OEM originals are copied unchanged into `ext-images/<slug>/source-of-truth/manuals/originals/` during promotion. They are never edited.

Rule: provenance is mandatory at every step. A claim with no traceable origin does not exist.

---

## 16. Promotion to nucleus (Step 14)

Promotion gates (must all pass; defined in `PHASE_1_IMPLEMENTATION.md` §9):
1. Every promoted chunk has `source_refs` or an explicit non-`verified` status.
2. Every promoted visual evidence references the canonical PNG or named OEM evidence.
3. No manual-era delivery file is promoted as primary truth.
4. No generated image is promoted into `source-of-truth/`.
5. `metadata/lineage/source-lineage.json` and `metadata/manifests/product-domain-manifest.json` are written or updated atomically.
6. The canonical PNG exists at the prescribed path.

Promotion writes:
- `ext-images/<slug>/source-of-truth/manuals/<file>.md` — normalized manual.
- `ext-images/<slug>/source-of-truth/manuals/originals/<file>.pdf` — OEM original.
- `ext-images/<slug>/source-of-truth/specifications/` — normalized spec rows.
- `ext-images/<slug>/source-of-truth/visual-evidence/` — approved OEM images.
- `ext-images/<slug>/structured-knowledge/glossary.json` — accepted glossary terms (created or updated).
- `ext-images/<slug>/metadata/lineage/source-lineage.json` — merged lineage.
- `ext-images/<slug>/metadata/manifests/product-domain-manifest.json` — updated source list.
- `ext-images/<slug>/metadata/validation/validation-ledger.json` — flagged items.

After promotion the staging directory `generated_manuals/<slug>/` is retained for traceability but is no longer canonical.

---

## 17. Outputs (summary)

Staging (`generated_manuals/<slug>/`):
- `discovery.json`, `multilingual.json`, `chunks.jsonl`, `manual_raw.txt`, `manual.md`, `manual.json`, `extraction_report.md`, `extracted_images/`, `visual-evidence-candidates.json`, `normalized.md`, `normalization-diff.md`, `glossary-candidates.json`, `duplication-report.json`, `source-metadata.json`, `staging-lineage.json`.

Nucleus (after promotion):
- See §16.

---

## 18. Recommended tools

Already in repository:
- `process_manuals.py` — batch entry point.
- `tools/manual_ocr/extract_manual.py` — OCR + structural extraction.
- `tools/manual_ocr/README.md` — pipeline notes.
- `tools/generate_reset_review_assets.py` — canonical PNG segmentation (visual side).
- PyMuPDF, pdf2image, pytesseract, OCRmyPDF (declared dependencies).

Recommended additions:
- A normalization runner that produces `normalized.md` and `normalization-diff.md` deterministically.
- A duplication-detection runner with a configurable similarity threshold.
- A confidence-scoring module shared by OCR and normalization.
- A promotion CLI that performs Stage 14 atomically and refuses to write on gate failure.
- A schema validator that checks promoted JSON against `KNOWLEDGE_SCHEMA.md`.

---

## 19. Extraction risks

- OCR errors propagate silently if confidence is not surfaced. Mitigation: §5 confidence recording.
- Translation drift across languages. Mitigation: §11 verbatim preservation in glossary.
- Heading detection misses unconventional OEM layouts. Mitigation: section-tree review in extraction report.
- Embedded vector text mistaken for diagrams. Mitigation: §4 strategy decision per page.
- Spec tables flattened by OCR into prose. Mitigation: dedicated table-detection pass before §7.
- Visual evidence misclassified as decorative. Mitigation: editorial review before promotion.
- Contradictions normalized away. Mitigation: §12 explicit `blocked-pending-validation`.

---

## 20. Ambiguity handling

Ambiguity is recorded, not resolved silently.

- Ambiguous OCR → flagged in extraction report; chunk gets `inferred-but-unverified`.
- Ambiguous terminology → glossary candidate created; awaits editorial decision.
- Ambiguous procedure step (e.g. unclear menu path) → candidate marked `blocked-pending-validation`; promotion to procedure entity is blocked until resolved.
- Ambiguous warning severity → defaults to `caution`; editorial may reclassify.
- Ambiguous component identity → flagged for canonical-PNG cross-check; resolution is a deliberate editorial step.

The validation ledger is the single record of unresolved ambiguity per product.

---

## 21. Future automation opportunities

- Layout-aware extraction with a vision model to improve table and diagram fidelity (advisory only; the canonical PNG remains truth).
- Cross-product duplication detection to seed shared terminology.
- Automated contradiction resolution proposals (still requiring editorial approval).
- CI gate that blocks merges introducing chunks without `source_refs`.
- Automated re-extraction when an OEM original is replaced (lineage-driven).
- Vector-store ingestion hook that emits RAG chunks directly from promoted entities (see `KNOWLEDGE_SCHEMA.md` §9).
