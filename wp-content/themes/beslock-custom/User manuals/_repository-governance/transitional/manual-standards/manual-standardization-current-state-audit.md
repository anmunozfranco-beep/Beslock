# Beslock Manual Standardization — Current-State Architecture & Editorial Audit

> Repository: `anmunozfranco-beep/Beslock`  
> Commit analyzed: `b2f9a5ff4264928f0e80e98f494382366068ca31`  
> Scope: `User manuals/` plus directly related OCR/manual-processing code and docs

## 1. Project purpose & design philosophy

The implementation is optimizing for **practical manual standardization** from OEM PDFs into reusable, Spanish-first help-center content, while keeping tooling lightweight and file-based.

Evidence of intent:
- Batch OCR pipeline dedicated to manuals: `process_manuals.py:2`, `process_manuals.py:15-22`, `README.md:146-160`
- Reusable OCR workflow with fallback stages and downstream hooks: `tools/manual_ocr/README.md:93-133`
- Editorial style centered on clarity/action over marketing tone: `User manuals/ext-images/e-orbit/automation/project/01-guia-estilo-editorial.md:9-15`, `:35-42`
- Visual style centered on utility/scannability over decoration: `User manuals/ext-images/e-orbit/automation/project/02-guia-estilo-visual.md:9-15`, `:30-36`

In practice, the system balances:
- **Usability**: task-oriented pages and step-by-step flows
- **Standardization**: common structures, naming, and image slot patterns
- **Scalability**: repeatable per-product document packs
- **Flexibility**: explicit “validate before final publication” notes in content
- **Product adaptation**: product-specific docs and asset namespaces (`e-orbit`, `e-flex`, etc.)

---

## 2. Current repository structure (`User manuals/` deep audit)

Top-level structure under `User manuals/` currently includes:
- Source PDFs (6 products): e-Flex, e-Nova, e-Orbit, e-Prime, e-Shield, e-Touch
- Per-product image planning docs:
  - `*- image generation matrix.md`
  - `*- AI image prompts.md`
  - `*- implementation starter pack.md`
- e-Orbit product nucleus under `User manuals/ext-images/e-orbit/`:
  - `source-of-truth/manuals/e-Orbit user manual.md`
  - `publishing/web/manuals/e-Orbit user manual - image-ready.md`
  - `metadata/audit/manual-validation-checklist.md`
  - `automation/project/` (editorial + visual + CMS + backlog package)
- Shared asset roots by product:
  - `User manuals/assets/e-flex/README.md`
  - `User manuals/assets/e-nova/README.md`
  - `User manuals/assets/e-prime/README.md`
  - `User manuals/assets/e-shield/README.md`
  - `User manuals/assets/e-touch/README.md`
- e-Orbit publishing asset control now lives under:
  - `User manuals/ext-images/e-orbit/publishing/web/assets/README.md`

Key responsibility split inferred:
- `User manuals/*.pdf`: OEM inputs
- `generated_manuals/<slug>/...`: machine extraction artifacts
- `User manuals/*.md`: editorial standardization outputs/planning
- `User manuals/assets/*`: visual asset governance and future storage

Emerging pattern: **“product namespace + repeated module set”** (prompts/matrix/starter-pack/assets), with e-Orbit as the most mature reference implementation.

---

## 3. Content pipeline (current actual flow)

### 3.1 Ingestion and OCR
1. PDFs discovered recursively in `User manuals/`: `tools/manual_ocr/extract_manual.py:282-287`
2. Batch runner executes per PDF into slugged output dirs: `process_manuals.py:76-87`, `extract_manual.py:958`
3. OCR strategy:
   - PDF-type detection: `extract_manual.py:303-320`
   - Stage 1 OCRmyPDF: `extract_manual.py:328-349`
   - Stage 2 pdf2image + pytesseract fallback: `extract_manual.py:1014-1030`
   - Stage 3 PyMuPDF native fallback: `extract_manual.py:1031-1046`

### 3.2 Cleanup and semantic structuring
- OCR cleanup and noise filtering: `extract_manual.py:461-531`
- Section detection and semantic categorization: `extract_manual.py:551-599`, `:159-169`
- Specs/steps/app/warnings/troubleshooting extraction: `extract_manual.py:602-674`

### 3.3 Generated artifacts
Per product:
- `manual_raw.txt`
- `manual.md`
- `manual.json`
- `extraction_report.md`
- `extracted_images/`

Written in code: `extract_manual.py:931-939` and documented in `README.md:154-160`.

Batch status currently shows 6/6 successful at run level: `generated_manuals/batch_report.md:3-14`, `generated_manuals/batch_summary.json:3-13`.

### 3.4 Editorial restructuring
After OCR outputs, editorial standardization is manually/AI-assisted in markdown docs (fully visible for e-Orbit):
- polished manual: `User manuals/ext-images/e-orbit/source-of-truth/manuals/e-Orbit user manual.md`
- image-ready variant with placeholders: `User manuals/ext-images/e-orbit/publishing/web/manuals/e-Orbit user manual - image-ready.md:7`, `:26`, `:44`, etc.

### 3.5 CMS/web integration readiness
- URL/page topology is already defined in seed docs: `User manuals/ext-images/e-orbit/automation/project/03-seed-content-cms.md:20-32`
- Starter packs map assets to routes: `User manuals/ext-images/e-orbit/source-of-truth/manuals/e-Orbit - implementation starter pack.md:53-94`

### 3.6 Manual intervention points (still required)
- Technical validation of uncertain codes/flows before publication:
  - `User manuals/ext-images/e-orbit/source-of-truth/manuals/e-Orbit user manual.md:14`, `:155-156`
  - checklist enforces validation: `User manuals/ext-images/e-orbit/metadata/audit/manual-validation-checklist.md:23-33`
- Final editorial QA and visual QA are checklist-driven, not automated.

---

## 4. Image pipeline audit

Current architecture is planning-heavy and generation-ready but still mostly manual in execution.

### 4.1 Existing system
- Image matrix templates per product define IDs, purpose, prompt base, negative prompt, format, priority, status (fully detailed in e-Orbit):
  - `User manuals/ext-images/e-orbit/visual-system/generation-matrices/image-generation-matrix.md:62-76`, `:79-317`
- Prompt libraries exist per product (depth varies):
  - Full detailed prompt pack for e-Orbit: `User manuals/ext-images/e-orbit/visual-system/prompts/ai-image-prompts.md`
- Starter packs map asset filenames to CMS page routes:
  - `User manuals/ext-images/e-orbit/source-of-truth/manuals/e-Orbit - implementation starter pack.md:53-94`

### 4.2 Asset governance
Asset README convention is consistent across products:
- lowercase + hyphens + no spaces/accents: e.g. `User manuals/ext-images/e-orbit/publishing/web/assets/README.md:15-21`
- recommended canonical names: `User manuals/ext-images/e-orbit/publishing/web/assets/README.md:23-33`
- “AI now, real captures later” policy: `User manuals/ext-images/e-orbit/publishing/web/assets/README.md:87-88`

### 4.3 Strengths
- Strong naming consistency and page-to-asset mapping
- Reusable matrix/prompt framework
- Clear quality checklist before integration

### 4.4 Bottlenecks
- Pipeline is still manual-heavy for generation/selection/refinement
- Product maturity is uneven (e-Orbit is far ahead)
- No committed shared central image registry file beyond per-product docs
- Potential duplication in nearly identical asset README structures across products

---

## 5. Manual standardization system (how normalization works)

Normalization currently happens through layered artifacts:

1. **Machine normalization** (OCR + structure extraction)
   - Produces raw + structured machine-readable outputs
2. **Editorial normalization** (human/AI-guided)
   - Applies tone, structure, and action-first language style
3. **Implementation normalization**
   - Maps editorial modules to URL routes and asset names

### Audience handling
The e-Orbit docs are written as practical end-user support content (clear tasks, minimal jargon), with explicit QA gates for technical confirmation before publication.

### Reusable vs product-specific
- Reusable:
  - docs triplet pattern (matrix/prompts/starter-pack)
  - asset naming schema
  - page archetypes (hub, primeros pasos, tareas, troubleshooting)
- Product-specific:
  - menu flows
  - app coupling details (e.g., Smart Life for e-Orbit)
  - technical codes to validate (e.g., `888#`, `3009#`)

### UX/readability strategy
- action-first steps
- route boxes/menu paths
- recommendations + post-validation checks
- troubleshooting slices for common failures

(Ref: `01-guia-estilo-editorial.md:45-53`, `02-guia-estilo-visual.md:18-27`)

---

## 6. Existing conventions (stable and valuable)

### Naming
- Product slug naming in assets and generated outputs (`e-orbit`, `e-flex`, etc.)
- Deterministic file naming for images and generated OCR pages

### Markdown/document conventions
- Modular docs by purpose (manual, prompts, matrix, starter, checklist)
- Checklist-driven QA gates
- Consistent route mapping format

### Generation conventions
- “Generate variants → select by clarity/realism/utility → refine”
  - `User manuals/ext-images/e-orbit/source-of-truth/manuals/e-Orbit - implementation starter pack.md:135-157`
  - `User manuals/ext-images/e-orbit/visual-system/prompts/ai-image-prompts.md:227-246`

### OCR artifacts tracked in git
Repo tracks core artifacts while ignoring other generated noise:
- `.gitignore:3-13`

These conventions appear stable and scalable for adding more products incrementally.

---

## 7. Current maturity assessment

### Robust today
- OCR engine architecture and fallback resilience
- Artifact model (`raw/md/json/report/images`) per product
- e-Orbit editorial package depth (style + visual + CMS seed + backlog + schedule)

### Scales reasonably well
- Slug-based foldering
- Repeatable per-product documentation modules
- Batch processing from repository root

### Fragile / debt-prone
- OCR quality variability by manual (some products rely on fallback OCR and show noisier section detection)
  - e-Nova fallback and invalid OCRmyPDF output: `generated_manuals/e-nova/extraction_report.md:23-48`
  - e-Shield similar pattern: `generated_manuals/e-shield/extraction_report.md:23-60`
- Editorial completion is uneven across products
- Significant duplicated prose across per-product docs may drift over time

### Missing pieces
- Fully unified cross-product master editorial standard file at `User manuals/` root
- More explicit automation bridge from structured OCR JSON to CMS ingest
- Executed image production inventory in repo (most is still planning structure)

---

## 8. Prioritized bottlenecks (practical impact)

1. **Editorial throughput bottleneck**: only e-Orbit has full, mature manual pack
2. **Validation bottleneck**: technical flows/codes require real-device confirmation before publication
3. **Image production bottleneck**: robust planning exists, but generation/refinement is still manually intensive
4. **Consistency drift risk**: duplicated product docs can diverge as updates accumulate
5. **Maintainability bottleneck**: no single top-level “manual standardization system” source-of-truth doc until now

---

## 9. High-value upgrade opportunities (compatible with current approach)

Without redesigning architecture:

1. **Consolidate shared conventions** into root-level reusable templates to reduce duplicated edits
2. **Add a root “standardization playbook”** (workflow + gates + naming + QA) for onboarding speed
3. **Define lightweight JSON-to-CMS mapping checklist** using existing `manual.json` fields
4. **Add per-product maturity scoreboard** (editorial ready, visual ready, validation ready) in one md table
5. **Create a canonical image registry table** per product/route/asset/status to reduce ambiguity
6. **Document fallback OCR handling policy** (when to accept vs re-run with force/dpi adjustments)

These changes preserve current philosophy: pragmatic, editorial-first, and product-adaptive.

---

## Evidence index (selected references)

- OCR batch runner: `/home/runner/work/Beslock/Beslock/process_manuals.py`
- OCR core: `/home/runner/work/Beslock/Beslock/tools/manual_ocr/extract_manual.py`
- OCR docs: `/home/runner/work/Beslock/Beslock/tools/manual_ocr/README.md`
- Root OCR usage docs: `/home/runner/work/Beslock/Beslock/README.md:146-160`
- Tracked generated artifacts policy: `/home/runner/work/Beslock/Beslock/.gitignore:3-13`
- e-Orbit manual (editorial baseline): `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/source-of-truth/manuals/e-Orbit user manual.md`
- e-Orbit image-ready manual: `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/publishing/web/manuals/e-Orbit user manual - image-ready.md`
- e-Orbit validation checklist: `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/metadata/audit/manual-validation-checklist.md`
- e-Orbit project package:
  - `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/automation/project/00-paquete-maestro.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/automation/project/01-guia-estilo-editorial.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/automation/project/02-guia-estilo-visual.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/automation/project/03-seed-content-cms.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/automation/project/04-backlog-mvp-fase-1.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/automation/project/05-cronograma-semanal.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/automation/project/06-starter-pack-implementacion.md`
- Product asset conventions:
  - `/home/runner/work/Beslock/Beslock/User manuals/ext-images/e-orbit/publishing/web/assets/README.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/assets/e-flex/README.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/assets/e-nova/README.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/assets/e-prime/README.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/assets/e-shield/README.md`
  - `/home/runner/work/Beslock/Beslock/User manuals/assets/e-touch/README.md`
- Batch outputs:
  - `/home/runner/work/Beslock/Beslock/generated_manuals/batch_report.md`
  - `/home/runner/work/Beslock/Beslock/generated_manuals/batch_summary.json`
  - `/home/runner/work/Beslock/Beslock/generated_manuals/e-nova/extraction_report.md`
  - `/home/runner/work/Beslock/Beslock/generated_manuals/e-shield/extraction_report.md`

