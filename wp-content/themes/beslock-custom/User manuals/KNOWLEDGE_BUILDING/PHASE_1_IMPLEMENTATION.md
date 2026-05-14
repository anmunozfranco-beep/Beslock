# PHASE 1 IMPLEMENTATION

Status: Active governance.
Phase: Phase 1 — OEM Knowledge Ingestion and Product Truth Consolidation.
Scope: Defines the execution scope for Phase 1 of the BESLOCK Product Knowledge Factory.

---

## 1. Phase 1 definition

Phase 1 ingests OEM material and the single canonical product PNG, extracts raw knowledge, normalizes terminology, preserves provenance, and establishes **product truth** before any manual, support page, structured-knowledge object, or generated visual is produced.

Phase 1 does not deliver. Phase 1 establishes the truth that every later phase reads from.

Inputs:
- OEM PDFs, technical sheets, installation guides, configuration guides, multilingual references, supplemental OEM artifacts.
- One canonical product PNG per product, stored at `ext-images/<slug>/source-of-truth/product-images/<Product>.png`.

Outputs land inside the product nucleus only.

---

## 2. Ingestion pipeline

Authoritative tooling:
- `process_manuals.py` — batch entry point for OEM ingestion.
- `tools/manual_ocr/extract_manual.py` — OCR engine and structural extraction (3-stage: OCRmyPDF, pdf2image + pytesseract, PyMuPDF).
- `tools/manual_ocr/README.md` — documented OCR/manual extraction workflow.
- `tools/generate_reset_review_assets.py` — PNG segmentation and deterministic anchor extraction bridge.
- `generated_manuals/<slug>/` — staging area for OCR outputs (`manual_raw.txt`, `manual.md`, `manual.json`, `extraction_report.md`, `extracted_images/`).

Pipeline steps (per product):
1. Discover valid OEM inputs and classify by document type (user, installation, app, supplemental, datasheet).
2. Extract raw text and page-level evidence with OCR plus fallback strategies.
3. Detect sections, specifications, steps, app instructions, warnings, features, troubleshooting cues.
4. Extract OEM visual evidence candidates: diagram pages, UI panels, icon regions, installation figures, layout references.
5. Ingest the canonical PNG and derive product-local geometry anchors, component boundaries, sensor positions, credential zones, control zones, exterior/interior distinction, visible UI constraints.
6. Merge OEM text evidence and PNG evidence into one product-truth review surface.
7. Record uncertainty as validation flags. Do not silently normalize unknowns into truth.
8. Promote only normalized source-of-truth artifacts and lineage manifests into the product nucleus.

Staging vs nucleus:
- `generated_manuals/<slug>/` is a staging surface. It is not canonical.
- Promotion into `ext-images/<slug>/source-of-truth/` requires explicit lineage and validation entries.
- After promotion, the staging surface may be retained for traceability but must not be treated as truth.

---

## 3. OEM extraction goals

Per OEM document, Phase 1 must extract:
- Raw text in source language.
- Multilingual variants when present.
- Tables and specification rows.
- Section structure and headings.
- Step lists for procedures, installation, configuration.
- App-side instructions where present.
- Warnings, cautions, and safety notes.
- Troubleshooting cues.
- Source metadata (file name, page count, OCR engine used, extraction confidence).
- Per-document extraction quality report.

Rules:
- One OEM document, one extraction report.
- OCR confidence and fallbacks must be recorded.
- OEM originals are preserved. Normalized derivatives are stored alongside, never overwriting the source.

---

## 4. Text normalization strategy

Normalization is its own pipeline, applied after extraction and before structured-knowledge assembly.

Normalization stages:
1. Terminology normalization to BESLOCK-approved terms.
2. Colombian-Spanish adaptation for delivery surfaces (see §5).
3. Duplicate-statement collapse across OEM documents.
4. Cross-document contradiction detection.
5. Technical consistency review.
6. Validation-state tagging.
7. Procedural wording standardization.

Normalization statuses (must be assigned to every normalized claim):
- `verified`
- `normalized`
- `inferred-but-unverified`
- `blocked-pending-validation`
- `deprecated-historical`

Normalization rule:
- Colombian-Spanish output is canonical for delivery surfaces.
- OEM wording is preserved verbatim in `source-of-truth/manuals/` and in provenance records.
- Normalization never deletes the OEM original.

---

## 5. Colombian-Spanish normalization goals

Goals:
- Deliver consistent Colombian-Spanish phrasing across web, PDF, support, onboarding, chatbot, and RAG outputs.
- Preserve OEM original wording for traceability and validation.
- Resolve OEM regional variants (Iberian Spanish, Mexican Spanish, English source) to a single Colombian-Spanish canonical form.
- Maintain a shared terminology registry of approved BESLOCK terms and forbidden OEM phrasings.
- Maintain a per-product `structured-knowledge/glossary.json` with the canonical Colombian-Spanish term, OEM source variants, and definition.

Rules:
- Editorial normalization decisions must be recorded in the validation ledger when they resolve ambiguity.
- Terminology drift between products is forbidden; the shared registry is the single source.
- A normalized term may not be promoted to delivery without an entry in the shared registry or product-local glossary.

---

## 6. Semantic structuring goals

Phase 1 does not produce final semantic objects (that is Phase 2), but it must produce the inputs Phase 2 consumes:
- Section-level normalized text with stable IDs.
- Step-level normalized procedures with stable IDs.
- Specification rows in structured form.
- Warning and troubleshooting candidates with severity hints.
- Glossary candidates.
- Visual evidence objects with anchor references.

Each candidate carries:
- product slug
- source document reference
- page or section reference
- extraction confidence
- normalization status
- proposed semantic object type

---

## 7. PNG source-of-truth governance

The canonical PNG is the **absolute** visual source of truth.

Rules:
- Exactly one canonical PNG per product.
- Stored at `ext-images/<slug>/source-of-truth/product-images/<Product>.png`.
- The PNG governs: silhouette, geometry, materials, exterior/interior identity, visible sensor layout, visible UI layout, visible control layout.
- Every visual derivative (cutouts, masks, anchor overlays, conditioning assets, generated support visuals) must trace back to this PNG.
- Replacement of the canonical PNG requires a new lineage entry and a re-derivation of all dependent visual derivatives. It is not a silent overwrite.
- Compatibility PNGs at the `ext-images/` root are not canonical and must be retired once the nucleus PNG exists.
- OEM diagrams, UI captures, and icon fragments are **secondary visual evidence**, not replacement anchors.

---

## 8. Extraction outputs

Required Phase 1 outputs per product nucleus:

```
ext-images/<slug>/
├── source-of-truth/
│   ├── manuals/                 # Normalized source documents + retained OEM originals
│   ├── specifications/          # Normalized + original technical evidence
│   ├── product-images/
│   │   └── <Product>.png        # Single canonical image
│   └── visual-evidence/         # OEM diagrams, UI snippets, icons, installation cues
├── visual-system/
│   └── references/
│       └── <slug>-visual-profile.md   # Or machine-readable equivalent
└── metadata/
    ├── lineage/
    │   └── source-lineage.json        # Source-to-derived mapping
    ├── manifests/
    │   └── product-domain-manifest.json   # Approved sources + canonical truth files
    └── validation/
        └── validation-ledger.json     # Unresolved claims, hardware-confirmation items, editorial cautions
```

---

## 9. Knowledge persistence strategy

Persistence rules:
- All Phase 1 outputs are persisted inside the product nucleus.
- OEM originals are retained alongside normalized derivatives.
- Lineage manifests are written before legacy files are deleted from any other location.
- The validation ledger is mandatory; it is not optional documentation.
- Provenance is machine-readable (JSON), not narrative-only.

Promotion gates (must all pass before Phase 2 begins for that product):
1. Every truth claim has `source_refs` or an explicit validation flag.
2. Every visual claim references the canonical PNG or named OEM visual evidence.
3. No manual-era delivery file acts as the primary truth source.
4. No generated image appears in `source-of-truth/`.
5. `metadata/lineage/source-lineage.json` and `metadata/manifests/product-domain-manifest.json` exist and validate.
6. The canonical PNG exists at the prescribed path.

Failure of any gate blocks Phase 2 for that product.

---

## 10. Phase 1 status (per product, current repository state)

- `e-orbit` — Phase 1 substantially complete; reference nucleus.
- `e-flex`, `e-nova`, `e-prime`, `e-shield`, `e-touch` — Phase 1 not complete; OEM material and OCR outputs exist in legacy locations and must be promoted into nuclei following this document.

Naming anomaly to track in the validation ledger: `e-Shied_2.pdf` (typo, missing 'l') exists in the legacy root. Provenance must record the OEM filename verbatim while normalized references use `e-shield`.
