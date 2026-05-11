# Beslock — AI Project Context Export

> **Purpose of this document**
> Transfer the **current state** of the Beslock manual standardization project to another AI system so it can continue evolving the project intelligently, preserving its architecture, editorial philosophy, and conventions.
>
> **This is not a redesign proposal.** It explains what already exists and how it works today.
>
> **Repository:** `anmunozfranco-beep/Beslock`
> **Working branch for this stream:** `technical_info_dev`
> **Scope analyzed:** `User manuals/` plus directly related OCR / processing code (`process_manuals.py`, `tools/manual_ocr/extract_manual.py`), the `generated_manuals/` outputs, and the `assets/` governance docs.

---

## 1. System overview

### 1.1 What the project does

Beslock is an **AI-assisted technical-manual standardization system** for a family of consumer smart-lock products (`e-Flex`, `e-Nova`, `e-Orbit`, `e-Prime`, `e-Shield`, `e-Touch`).

It transforms inconsistent OEM PDF manuals — which arrive in varied layouts, languages, and quality levels — into a consistent set of editorial assets:

- standardized **web manuals** (Spanish-first help-center pages, mapped to deterministic CMS routes),
- downloadable **PDF manuals** (post-editorial, after technical/visual validation),
- improved **UX documentation** (task-oriented, step-by-step, with route boxes, recommendations and troubleshooting),
- **reusable technical documentation assets** (image matrices, prompts, asset naming conventions, validation checklists).

### 1.2 What problems it solves

- OEM PDFs are heterogeneous in structure, language and quality (some are scanned-only, some are noisy).
- Products differ significantly in features, app integration, installation flow, and operational logic, but the brand needs **a single editorial voice and structural skeleton** across them.
- Image production is manual, slow, and inconsistent unless prompts and slots are pre-defined.
- Validation is a recurring blocker: technical codes (e.g. `888#`, `3009#` in e-Orbit) and menu flows must be confirmed on real devices before publication.

### 1.3 What the architecture is optimizing for

In priority order, observable in the artifacts:

1. **Editorial consistency** across heterogeneous products.
2. **Pragmatism**: file-based, lightweight, no premature platform/tooling investment.
3. **Repeatability**: each product gets the same module set (manual + image matrix + prompts + starter pack + checklist + asset README).
4. **Adaptability**: per-product namespaces and product-specific notes are first-class.
5. **AI-assistability**: prompts, matrices, slots, JSON outputs and naming conventions are all designed to be consumed by AI tools (text and image).

### 1.4 How the system appears to have evolved

The repository shows a clearly layered evolution:

- **Layer 1 — Ingest automation**: a Python OCR pipeline (`process_manuals.py` + `tools/manual_ocr/extract_manual.py`) that processes all PDFs in `User manuals/` into per-product `generated_manuals/<slug>/` artifacts. Multiple OCR fallbacks already exist (OCRmyPDF → pdf2image+pytesseract → PyMuPDF), which signals real production friction encountered with scanned PDFs.
- **Layer 2 — Editorial scaffolding**: per-product markdown documents added inside `User manuals/` (image matrix, AI prompts, implementation starter pack), forming a “triplet” pattern around each product.
- **Layer 3 — Editorial maturity (e-Orbit reference)**: a deeper, near-complete pack only for e-Orbit, including a project folder with master package, editorial style guide, visual style guide, CMS seed content, MVP backlog, weekly schedule, implementation starter pack, plus an image-ready manual variant and a validation checklist. **e-Orbit is the reference implementation; other products are still at Layer 2.**
- **Layer 4 — Audit & context**: a recent `manual-standardization-current-state-audit.md` and this `ai-project-context-export.md` codify the system itself so it can be carried forward.

### 1.5 Existing project philosophy

Reading across the editorial and visual style docs, asset READMEs and validation checklists, the project consistently expresses these explicit principles:

- **Write to help people do**, not to impress (`e-Orbit project/01-guia-estilo-editorial.md` — “escribir para ayudar a hacer”, “priorizar claridad sobre formalismo”).
- **Clarity over decoration**, **scannability first**, **strong hierarchy**, **reusable blocks** (`02-guia-estilo-visual.md`).
- **Action-first steps** that begin with a verb; consistent menu route formatting; restraint when information is not yet validated.
- **AI now, real captures later**: AI-generated images are explicitly accepted as initial support, to be replaced by real captures when available (`assets/e-orbit/README.md §7`).
- **Validate before publishing**: a checklist gate is mandatory for editorial, technical, visual and structural readiness (`e-Orbit - manual validation checklist.md`).
- **Prudence with uncertainty**: items pending technical confirmation must be explicitly marked, never asserted.

---

## 2. Repository structure

### 2.1 Top-level relevant tree

```text
/
├── User manuals/                       ← editorial source-of-truth (manuals + planning + assets)
│   ├── e-Flex user manual.pdf
│   ├── e-Flex - AI image prompts.md
│   ├── e-Flex - image generation matrix.md
│   ├── e-Flex - implementation starter pack.md
│   ├── e-Nova user manual.pdf
│   ├── e-Nova - ... (same triplet)
│   ├── e-Orbit user manual.pdf
│   ├── e-Orbit user manual.md                       ← polished editorial manual
│   ├── e-Orbit user manual - image-ready.md         ← variant with image slot placeholders
│   ├── e-Orbit - AI image prompts.md
│   ├── e-Orbit - image generation matrix.md
│   ├── e-Orbit - implementation starter pack.md
│   ├── e-Orbit - manual validation checklist.md
│   ├── e-Orbit project/                             ← deep editorial pack (reference impl.)
│   │   ├── 00-paquete-maestro.md
│   │   ├── 01-guia-estilo-editorial.md
│   │   ├── 02-guia-estilo-visual.md
│   │   ├── 03-seed-content-cms.md
│   │   ├── 04-backlog-mvp-fase-1.md
│   │   ├── 05-cronograma-semanal.md
│   │   ├── 06-starter-pack-implementacion.md
│   │   └── README.md
│   ├── e-Prime / e-Shield / e-Touch ... (same triplet pattern)
│   ├── assets/
│   │   ├── e-flex/README.md
│   │   ├── e-nova/README.md
│   │   ├── e-orbit/README.md
│   │   ├── e-prime/README.md
│   │   ├── e-shield/README.md
│   │   └── e-touch/README.md
│   ├── manual-standardization-current-state-audit.md
│   └── ai-project-context-export.md   ← this document
│
├── process_manuals.py                  ← batch OCR entry point (run from repo root)
├── tools/manual_ocr/                   ← OCR engine + helpers
│   ├── extract_manual.py
│   └── README.md
├── generated_manuals/                  ← machine outputs (tracked subset)
│   ├── batch_report.md
│   ├── batch_summary.json
│   └── <slug>/
│       ├── manual_raw.txt
│       ├── manual.md
│       ├── manual.json
│       ├── extraction_report.md
│       └── extracted_images/
├── output/                             ← additional run output (e.g. e-orbit/)
└── README.md, Makefile, docker-compose.yml, wp-content/, data/products.json, ...
                                       ← WordPress / Docker stack used downstream as the publishing target
```

### 2.2 Module relationships and responsibilities

| Layer                  | Location                                                | Responsibility                                                                 |
|------------------------|---------------------------------------------------------|--------------------------------------------------------------------------------|
| Ingest                 | `User manuals/*.pdf`                                    | OEM source PDFs (one per product).                                             |
| OCR / extraction       | `process_manuals.py`, `tools/manual_ocr/extract_manual.py` | Convert PDFs → text + structured JSON + images, per product slug.            |
| Machine artifacts      | `generated_manuals/<slug>/`                             | `manual_raw.txt`, `manual.md`, `manual.json`, `extraction_report.md`, `extracted_images/`. Feeds editorial work. |
| Editorial planning     | `User manuals/<Product> - image generation matrix.md`, `... - AI image prompts.md`, `... - implementation starter pack.md` | Per-product image slots, prompts, route mapping, asset names, priorities.    |
| Editorial production   | `User manuals/e-Orbit user manual.md`, `... - image-ready.md`, `... - manual validation checklist.md` | Finished editorial manual + image-slotted variant + QA gates.                |
| Editorial system       | `User manuals/e-Orbit project/`                         | Style guides (editorial + visual), CMS seed content, backlog, schedule, master package. |
| Asset governance       | `User manuals/assets/<slug>/README.md`                  | Per-product naming, organization, asset-to-page mapping, before-publish checklist. |
| Publishing target      | `wp-content/`, `docker-compose.yml`, `data/products.json`, `wp-content/plugins/beslock-product-sync/` | WordPress site that consumes products and (eventually) manual content.       |
| Self-documentation     | `User manuals/manual-standardization-current-state-audit.md`, this file | Architecture/editorial reference for humans and AI agents.                   |

### 2.3 Shared vs product-specific structures

- **Shared (architectural / convention layer):**
  - The “triplet” pattern (`matrix` + `prompts` + `starter pack`) per product.
  - Per-product `assets/<slug>/README.md` with the same template (objective, naming, types, organization, asset-to-page mapping, pre-add checklist, operational recommendation).
  - Generated artifact set (`raw/md/json/report/images`) per slug.
  - Editorial and visual style guides (currently scoped to e-Orbit but written as reusable principles).
- **Product-specific:**
  - The OEM PDFs themselves.
  - Per-product menu flows, codes, and app-coupling notes (e.g. Smart Life integration, `888#` / `3009#` codes for e-Orbit).
  - The full editorial pack (manual.md, image-ready.md, validation checklist, project folder) currently exists only for **e-Orbit** as the reference implementation.

### 2.4 Workflow entry points

- **Batch OCR:** `python process_manuals.py` from repo root (CLI flags: `--input`, `--output`, `--dpi`, `--language`, `--force-ocr`, `--skip-json`). Writes per-product folders under `generated_manuals/` plus `batch_report.md` and `batch_summary.json`.
- **Per-product editorial work:** open the product’s triplet (`matrix`, `prompts`, `starter pack`) under `User manuals/`. For e-Orbit, also open `e-Orbit project/` and the manual + image-ready variants.
- **Asset placement:** per-product folder under `User manuals/assets/<slug>/`, governed by the local `README.md`.
- **Publishing stack:** the Dockerized WordPress stack (`make up` / `make down` / `make fresh` / `make logs` / `make restart`); product data flows in via `data/products.json` consumed by `wp-content/plugins/beslock-product-sync/`. Manual content publication into the CMS is **not yet automated** — it is currently planned through `e-Orbit project/03-seed-content-cms.md`.

### 2.5 Architectural patterns already in use

- **Slug-based per-product namespace** (`e-orbit`, `e-flex`, ...) used uniformly across `assets/`, `generated_manuals/`, and CMS routes.
- **Triplet module pattern** (matrix / prompts / starter pack) per product.
- **Reference implementation pattern**: e-Orbit defines the depth of maturity; other products are scaffolded to follow.
- **Two-track manual**: an editorial manual (`*.md`) and an image-ready variant (`* - image-ready.md`) with explicit slots.
- **Checklist-as-gate**: explicit checklists for asset addition, manual validation, and editorial QA — the only enforcement mechanism today.
- **File-based truth**: there is no database or service layer for the editorial pipeline; everything is markdown + JSON in git.

---

## 3. Editorial system

### 3.1 How manuals are standardized

Standardization happens in three layered passes:

1. **Machine normalization** — OCR pipeline produces `manual_raw.txt` (verbatim OCR), `manual.md` (cleaned + section-grouped), `manual.json` (structured: sections, specs, steps, warnings, troubleshooting, app), `extraction_report.md` (quality summary), `extracted_images/` (page-level image extraction).
2. **Editorial normalization** — a human/AI-assisted pass rewrites the manual into the brand voice with consistent section ordering, route boxes, recommendations and validation notes (visible end-to-end for e-Orbit).
3. **Implementation normalization** — the editorial output is mapped to deterministic CMS routes and to deterministic asset filenames (image matrix + starter pack).

### 3.2 Audience handling

The current target audience is **end users of consumer smart locks** (Spanish-speaking). The editorial guide explicitly chooses:

- “Help to do” over “explain in depth”.
- Clear and close (cercano) tone, never overly promotional, never ambiguous.
- Use product names exactly: **e-Orbit**, **Smart Life** — never variations.
- Begin every step with a verb.

There is currently **no separate installer/technician track**; the manual mixes installation prerequisites and use, but always from a user perspective.

### 3.3 How technical differences between products are handled

- Each product gets its own image matrix and prompt pack, so product-specific shapes, panels and apps are encoded once per product.
- Product-specific menu codes and app coupling are captured in the per-product manual (e-Orbit currently the only one fully written).
- Standardization is in **structure** (page archetypes, ordering, blocks), not in **content** — content is allowed to diverge as much as the product requires.

### 3.4 Reusable vs product-specific sections

- **Reusable sections** (page archetypes appearing in every product’s plan):
  - product hub (`/productos/<slug>`)
  - first steps (`/primeros-pasos`)
  - users (`/usuarios/agregar-administrador`, `/usuarios/agregar-usuario`)
  - usage (`/uso/pin`, `/uso/huella`, ...)
  - configuration (`/configuracion/idioma`, ...)
  - app (`/app/agregar-dispositivo`, `/app/vincular-por-qr`)
  - troubleshooting (`/solucion-de-problemas/...`)
  - downloads
- **Product-specific sections** are placed inside the same archetypes but with product-specific menu paths, codes, app flows, and visual assets.

### 3.5 Readability and usability

The editorial style guide enforces the following per-page structure (`01-guia-estilo-editorial.md §5`):

1. what you are going to do
2. what you need first
3. steps
4. recommendation or warning
5. what to validate after
6. frequent problems
7. recommended next step

The visual style guide (`02-guia-estilo-visual.md`) defines reusable visual blocks: page header, checklist, menu-route box, numbered steps, recommendation box, warning box, frequent-problems block, next-steps block.

### 3.6 Web vs PDF requirements

- The **web** target is the primary editorial form: a help-center site with deterministic routes, scannable blocks, and per-page hero/support imagery (slots defined in the image matrix + starter pack).
- The **PDF** target is treated as an export of the same content — currently the OEM PDFs are the input artifact; the project does not yet produce its own polished PDFs, but the editorial content is structured (route boxes, block components) so a PDF generation step can be added without reauthoring.

### 3.7 Content hierarchy logic

Hierarchy is enforced through:

- Section ordering inside each manual (style guide §5).
- URL hierarchy in seed content (`03-seed-content-cms.md`): `/productos/<slug>/<category>/<task>`.
- Image hierarchy in matrix / starter pack: hero → contextual → action-per-task → troubleshooting → downloads, with explicit priority lists.

### 3.8 Consistency mechanisms

- Style guides (editorial + visual) at `User manuals/e-Orbit project/`.
- Validation checklist (`e-Orbit - manual validation checklist.md`) covering editorial, technical, visual and structural QA.
- Per-product asset README with a “before adding an asset” checklist.
- Naming conventions enforced by convention (slug, hyphenated, lowercase, no accents).
- Audit document (`manual-standardization-current-state-audit.md`) and this export, which freeze the conventions.

---

## 4. Content pipeline

### 4.1 OEM PDF ingestion

- Source PDFs live in `User manuals/<Product> user manual.pdf`.
- The batch runner discovers them recursively (`tools/manual_ocr/extract_manual.list_input_pdfs`).
- One slugged output folder is created per PDF under `generated_manuals/<slug>/`.

### 4.2 OCR extraction

`process_manuals.py` calls `tools.manual_ocr.extract_manual.process_manual` for each PDF. The OCR strategy uses **three fallback stages** to handle the heterogeneous PDF quality:

1. PDF type detection (text vs scanned/image-based).
2. Stage 1 — **OCRmyPDF** (preferred when usable).
3. Stage 2 — **pdf2image + pytesseract** fallback.
4. Stage 3 — **PyMuPDF** native text fallback.

CLI flags (see `process_manuals.py:14-22`): `--input` (default `User manuals`), `--output` (default `generated_manuals`), `--dpi` (default 300), `--language` (default `spa+eng`), `--force-ocr`, `--skip-json`.

### 4.3 Cleanup, semantic restructuring, markdown generation

Performed inside `extract_manual.py`:

- OCR cleanup and noise filtering.
- Section detection and semantic categorization (general / specifications / operation / app / warnings / troubleshooting / setup steps).
- Generation of the artifact set per product:
  - `manual_raw.txt` (verbatim OCR),
  - `manual.md` (cleaned, section-grouped markdown),
  - `manual.json` (structured fields),
  - `extraction_report.md` (per-stage status, OCR confidence, counts),
  - `extracted_images/` (page-level image extraction).

The most recent run (visible in `generated_manuals/batch_report.md`) processed **6 manuals successfully, 0 failed**, with quality varying from “Good” (e-Orbit, ocrmypdf, ~92% confidence) to “Acceptable” (e-Nova, pytesseract fallback, ~84% confidence) — the variance is expected and documented in the per-product `extraction_report.md`.

### 4.4 Reusable blocks

Reuse happens at three levels:

- **Pipeline level**: same artifact set per product, same OCR fallback chain.
- **Editorial level**: the “triplet” (matrix / prompts / starter pack) is the reusable per-product editorial unit; the page-archetype set is the reusable cross-product structure.
- **Visual level**: the reusable visual blocks defined in `02-guia-estilo-visual.md`.

### 4.5 Markdown generation, PDF generation, website publishing

- **Markdown generation**: automated for the machine layer (`generated_manuals/<slug>/manual.md`); manual/AI-assisted for the editorial layer (`User manuals/e-Orbit user manual.md`, `... - image-ready.md`).
- **PDF generation**: not currently automated. The project consumes OEM PDFs as input; downstream PDFs of the editorial output are a future step the structure is ready for.
- **Website publishing**: the WordPress stack under `wp-content/` + `docker-compose.yml` is the publishing target. Product catalog data already syncs deterministically (plugin `beslock-product-sync`, fed by `data/products.json`). Manual/help-center content publishing is currently planned via the seed content (`03-seed-content-cms.md`) but is **not yet wired automatically** from the editorial markdown to the CMS.

### 4.6 Review stages

- **Machine review**: `extraction_report.md` per product, plus the batch-level `batch_report.md` / `batch_summary.json`.
- **Editorial review**: editorial QA against the style guide.
- **Technical review**: `manual validation checklist §3` enforces real-device confirmation of flows and codes.
- **Visual review**: `manual validation checklist §4` enforces existence and quality of every required image slot.
- **Structural review**: `manual validation checklist §5–6` enforces presence of required sections and overall publish-readiness.

### 4.7 Where automation, manual work, and rules live

| Stage                                | Automated                                          | Manual / AI-assisted                          | Rules / standardization                        |
|--------------------------------------|----------------------------------------------------|-----------------------------------------------|------------------------------------------------|
| Ingest / OCR / structured extraction | `process_manuals.py` + `extract_manual.py`         | —                                             | OCR fallback chain; semantic section detection |
| Cleanup of OCR output                | Partially (filters in `extract_manual.py`)         | Final cleanup during editorial rewrite        | Section taxonomy in code                       |
| Editorial rewrite                    | —                                                  | Human/AI in markdown                          | `01-guia-estilo-editorial.md`                  |
| Visual planning (matrix + prompts)   | —                                                  | Human in markdown                             | `02-guia-estilo-visual.md`, matrix template    |
| Image generation                     | —                                                  | External AI tools (DALL·E, etc.)              | Prompt + negative prompt + format per slot     |
| Asset placement                      | —                                                  | Human                                         | `assets/<slug>/README.md` checklist            |
| QA before publication                | —                                                  | Human checklist                               | `e-Orbit - manual validation checklist.md`     |
| CMS publication                      | Product data sync only                             | Manual content publication still manual       | `03-seed-content-cms.md` route plan            |

---

## 5. Image system

### 5.1 Source / extracted / regenerated images

- **Source images** from OEM PDFs are emitted to `generated_manuals/<slug>/extracted_images/` by the OCR pipeline.
- **Regenerated/AI images** for the editorial output are planned via the per-product image matrix and prompt pack, and are intended to live under `User manuals/assets/<slug>/` (currently each `assets/<slug>/` folder contains only its `README.md` — image files have not yet been committed).
- The official policy is **AI-generated first, real captures later** (`assets/e-orbit/README.md §7`).

### 5.2 How prompts are organized

For each product, two paired files exist:

- `<Product> - image generation matrix.md` — defines for each image: `id`, `pagina`, `tipo_de_imagen`, `objetivo`, `descripcion_visual`, `prompt_base`, `negative_prompt`, `formato`, `prioridad`, `estado`, `notas` (`e-Orbit - image generation matrix.md §3`).
- `<Product> - AI image prompts.md` — finalized copy/paste-ready prompt + negative prompt + format + optional variants per image slot.

The matrix is the planning view; the prompts file is the production view. e-Orbit currently has both filled in; other products have the templates in place with varying depth.

### 5.3 How image matrices are organized

Each matrix entry corresponds to a CMS route + a deterministic asset name. The matrix doubles as a **prioritized backlog** (status: pending / in progress / approved). The MVP-Phase-1 backlog is then condensed into a short asset-priority list in the **implementation starter pack** (`<Product> - implementation starter pack.md §3`), which lists “produce first” vs “produce after” for each product.

### 5.4 Technical illustrations

There is currently no separate vector/diagram authoring system. Technical illustrations are treated as image slots in the matrix, generated by the same AI image flow, and reviewed against the visual style guide (no fake interfaces, no embedded text inside images, one action per image, neutral backgrounds, realistic materials).

### 5.5 How consistency is maintained

- The visual style guide (`02-guia-estilo-visual.md`) sets cross-product visual rules.
- The matrix/prompt template is the same across products.
- The per-product `assets/<slug>/README.md` enforces naming, organization, asset-to-page mapping, and a pre-add checklist.
- The validation checklist enforces existence and quality of each image slot before publishing.

### 5.6 Where manual work is still heavy

- Generation, selection and refinement of every image (the loop “generate variants → select by clarity/realism/utility → refine” is documented but performed by hand).
- Review for hand/finger artifacts, fake UIs, embedded text, and brand consistency.
- Replacement of AI images with real captures over time.
- Producing the per-product depth that e-Orbit already has.

### 5.7 Naming conventions, reusable systems, prompts, assets

- **Asset filenames**: `lowercase + hyphens + no spaces + no accents + descriptive` (`assets/<slug>/README.md §2`). Pattern: `<slug>-<context>-<action-or-subject>.<ext>`. Examples (e-Orbit): `e-orbit-hero-main.jpg`, `e-orbit-add-admin-action.jpg`, `e-orbit-troubleshoot-fingerprint.jpg`.
- **Reusable visual systems**: visual blocks defined in the visual style guide; image archetypes (hero / contextual / action / troubleshoot / downloads).
- **Prompt conventions**: structured fields (final prompt, negative prompt, suggested format, optional variants) and a recurring stylistic envelope (clean, technical, realistic, contemporary, useful for documentation, not promotional).
- **Asset conventions**: optional subdivision when volume grows (`ai-generated/`, `real-captures/`, `web-ready/`, `thumbnails/`); single flat folder while volume is small.

---

## 6. Current conventions

The following conventions are **stable, observable, and worth preserving**:

### 6.1 Folder conventions
- `User manuals/` is the editorial source of truth.
- `generated_manuals/<slug>/` is the machine-output convention; only a tracked subset is committed (`manual_raw.txt`, `manual.md`, `manual.json`, `extraction_report.md`, `extracted_images/`, plus `batch_report.md` / `batch_summary.json` at the root).
- `User manuals/assets/<slug>/` is the per-product visual asset namespace.
- `User manuals/<Product> project/` is the deep editorial pack for a product (e-Orbit only today).

### 6.2 Slug conventions
- Each product has a single slug used everywhere: `e-flex`, `e-nova`, `e-orbit`, `e-prime`, `e-shield`, `e-touch`.
- Slugs are lowercase, hyphenated, no accents, and used identically in folders, asset filenames and CMS routes.

### 6.3 Markdown conventions
- One H1 per file, title is `# <Product>` followed by `## <Document name>`.
- Numbered top-level sections (`## 1. ...`, `## 2. ...`).
- `---` horizontal rules between sections.
- Inline code for menu paths, codes, routes and filenames (e.g. `888#`, `/productos/e-orbit`, `e-orbit-hero-main.jpg`).
- Bold for product names: **e-Orbit**, **Smart Life**.
- Step lists begin with a verb.

### 6.4 Naming conventions
- Per-product editorial files: `<Product> - <document>.md` (note the hyphen-with-spaces between Product and document, e.g. `e-Orbit - AI image prompts.md`).
- Per-product asset files: `<slug>-<context>-<action>.jpg`.

### 6.5 Prompt conventions
- A finalized prompt is one paragraph (sensory + compositional + stylistic envelope), Spanish.
- A negative prompt enumerates banned elements (text-in-image, deformed hands, fake UIs, neon lights, busy backgrounds, low resolution, ...).
- Format is declared explicitly (e.g. `16:9 horizontal`, `4:3 horizontal`).
- Optional variants are listed for selection.

### 6.6 Page-archetype conventions
- The set `{producto, primeros-pasos, usuarios, uso, configuracion, app, solucion-de-problemas, descargas}` is the canonical CMS skeleton.
- Each page follows the editorial 7-block structure (do / prerequisites / steps / recommendation-or-warning / validate-after / frequent-problems / next-step).

### 6.7 Generation conventions
- Loop: **generate variants → select by clarity, realism, utility → refine**.
- Status field on each image slot (pendiente / en proceso / aprobado).
- Priority labelling (Fase 1 first lot, then secondary lot) in the starter pack.

### 6.8 Mature / valuable conventions

The most mature and re-export-worthy conventions today are:
- the slug convention,
- the triplet pattern (matrix + prompts + starter pack),
- the per-product asset README template,
- the editorial 7-block per-page structure,
- the validation checklist as the publish gate,
- the OCR artifact set + tracked-subset policy.

---

## 7. Current maturity state

### 7.1 Already robust
- The OCR pipeline with three fallbacks; six products processed end-to-end with a per-product extraction report and a batch summary.
- The per-product artifact contract (`raw / md / json / report / images`).
- The slug-based namespace shared across folders, assets and CMS routes.
- The e-Orbit editorial pack (style + visual + CMS seed + backlog + schedule + manual + image-ready + checklist + asset README).

### 7.2 Already scales adequately
- Adding a new product is mechanical: drop the PDF in `User manuals/`, run `process_manuals.py`, scaffold the triplet markdown files, scaffold an `assets/<new-slug>/README.md`. The system absorbs new products without architectural change.
- Per-product editorial work scales because each product is independent (no shared monolith file).

### 7.3 Fragile / debt-prone
- **OCR quality variance**: products falling back to pytesseract (e-Nova, e-Shield) yield noisier section detection than the OCRmyPDF path. Visible in their `extraction_report.md`.
- **Editorial completeness is uneven**: e-Orbit is mature; the other five products have only the planning triplet.
- **Duplication risk**: per-product asset READMEs and per-product matrices share large amounts of identical prose; updates to conventions require N edits.
- **No automatic bridge** from `generated_manuals/<slug>/manual.json` to the editorial markdown or to the CMS — the structured output is currently underused.

### 7.4 Duplicated
- Asset README structure across `assets/e-flex|e-nova|e-orbit|e-prime|e-shield|e-touch/`.
- Matrix template prose across products.
- Prompt stylistic envelope across prompt files.

### 7.5 Overcomplicated
- Nothing materially overengineered. The system is intentionally lightweight (markdown + a single Python pipeline + Docker WordPress). The OCR fallback chain is justified by the heterogeneity of OEM PDFs.

### 7.6 Missing
- A canonical, root-level cross-product editorial standard (style guides currently sit inside `e-Orbit project/`, formally scoped to one product).
- A canonical image registry (one place to see, per product: route ↔ asset ↔ status).
- Automation from `manual.json` to CMS ingest.
- Automated PDF export of the editorial manuals.
- A per-product maturity scoreboard (editorial / visual / validation / publish readiness).

### 7.7 Where technical debt may emerge
- Convention drift across the six per-product asset READMEs and matrices as products mature independently.
- Stale `extraction_report.md` if OEM PDFs are revised but `process_manuals.py` is not re-run consistently.
- `e-Orbit project/` may keep accumulating reference-only material if the same depth is not lifted up to a shared layer once a second product reaches that maturity.

---

## 8. Current bottlenecks (prioritized by practical production impact)

1. **Editorial throughput** — only e-Orbit has a complete editorial pack; replicating that depth for the five other products is the largest blocker to launching the help center.
2. **Technical validation** — flows and codes (e.g. `888#`, `3009#`, Smart Life device-add flow) require real-device confirmation; this is a hard human gate enforced by the validation checklist.
3. **Image production** — planning is mature (matrix + prompts + naming + slot priorities), but generation, selection, refinement and replacement-with-real-captures remain manual and slow.
4. **Consistency drift** — convention changes must be propagated across six asset READMEs / matrices / prompt packs by hand.
5. **OCR variance handling** — products that hit the pytesseract fallback need extra editorial cleanup; there is no standard “re-run with adjusted DPI / `--force-ocr`” policy yet.
6. **CMS publication gap** — `manual.json` and the editorial markdown are not wired to the WordPress stack; product catalog data is synced, but manual content is not.
7. **Onboarding friction** — until the recent audit + this export, there was no single place to read the system end-to-end.

---

## 9. High-value upgrade opportunities (compatible with the current architecture)

These are improvements that reinforce — not replace — the current system. They are pragmatic, file-based, and low-risk.

1. **Promote the e-Orbit style guides to repo-root scope.** Move (or symlink) the editorial and visual style guides out of `e-Orbit project/` into a root-level location inside `User manuals/` and reference them from each product. Removes the implicit “e-Orbit only” signal and makes them the official cross-product standard.
2. **Add a single per-product maturity scoreboard.** One markdown table at `User manuals/` listing each slug × {ocr quality, editorial pack, image matrix filled, prompts filled, assets present, validation checklist passed, CMS published}. Drives prioritization at a glance.
3. **Add a canonical image registry per product.** One markdown table per product mapping route ↔ asset filename ↔ status ↔ matrix-id. Eliminates ambiguity between matrix, prompts, starter pack and asset README.
4. **Document an OCR-fallback handling policy.** When to accept pytesseract output vs re-run with `--force-ocr` and adjusted `--dpi`; codify per-product overrides if needed. Reduces editorial cleanup load.
5. **Define a lightweight `manual.json` → CMS ingest checklist.** Without building automation yet, document exactly which JSON fields map to which CMS sections; this makes future automation a small step.
6. **Template-extract the per-product asset README.** Keep one template + per-product overrides only; reduces duplication and drift.
7. **Add a “new product onboarding” one-pager.** Steps to add a product end-to-end (drop PDF, run `process_manuals.py`, scaffold triplet, scaffold asset README, fill matrix, run validation checklist). Compresses onboarding time.
8. **Optional: lock conventions with a tiny linter.** A short script that validates slug usage, asset filename pattern, presence of required per-product files, and presence of every checklist item. Runs locally; no CI required.

Each of these preserves the existing philosophy: pragmatic, editorial-first, file-based, AI-assisted, product-adaptive.

---

## 10. AI context transfer objective

This document is intentionally written so that another AI system can:

- **Quickly understand the project**: sections 1–4 give the system, structure, editorial system and pipeline.
- **Preserve architectural consistency**: section 2 fixes the folder/module map, section 6 enumerates the conventions, section 4 enumerates pipeline boundaries (what is automated vs manual vs ruled).
- **Preserve editorial philosophy**: section 1.5 captures the explicit principles, sections 3 and 5 describe how those principles materialize in editorial and visual decisions, with direct references to the style guides and validation checklist.
- **Continue evolving the project intelligently**: sections 7 and 8 mark where the system is robust, fragile, and bottlenecked; section 9 lists upgrades that are compatible with — not destructive of — the current architecture.

### 10.1 What another AI system must not do

- Do not introduce a new editorial voice or new page-archetype set; the current ones are stable and intentional.
- Do not rename slugs, asset filenames, or CMS routes.
- Do not change the per-product triplet pattern (matrix / prompts / starter pack) or the artifact set under `generated_manuals/<slug>/`.
- Do not delete or bypass the validation checklist; it is the publish gate.
- Do not assert technical claims (codes, menu paths, app flows) without preserving the “validate before publishing” caveat.
- Do not centralize what is intentionally per-product (product-specific menus, codes, app flows).
- Do not over-engineer. The system is pragmatic by design.

### 10.2 What another AI system should do

- Treat **e-Orbit** as the reference implementation when bringing other products to the same maturity.
- Reuse the existing conventions enumerated in section 6 verbatim.
- Use `manual.json` as the structured handoff between OCR and editorial / CMS work.
- When proposing improvements, frame them as additions compatible with the current architecture (see section 9), not as redesigns.
- Update this document and `manual-standardization-current-state-audit.md` whenever conventions change, so the project remains self-describing.

---

## Evidence index

- OCR batch entry point: `process_manuals.py:11`, `:14-22`, `:64-96`
- OCR core: `tools/manual_ocr/extract_manual.py` (PDF detection, OCR fallback chain, cleanup, semantic section detection, artifact emission)
- Tracked artifacts policy: `.gitignore:3-13`
- Batch outputs: `generated_manuals/batch_report.md`, `generated_manuals/batch_summary.json`
- OCR variance examples: `generated_manuals/e-orbit/extraction_report.md` (Good, ocrmypdf), `generated_manuals/e-nova/extraction_report.md` (Acceptable, pytesseract fallback), `generated_manuals/e-shield/extraction_report.md`
- Editorial style: `User manuals/e-Orbit project/01-guia-estilo-editorial.md`
- Visual style: `User manuals/e-Orbit project/02-guia-estilo-visual.md`
- CMS seed (page topology): `User manuals/e-Orbit project/03-seed-content-cms.md`
- Master package index: `User manuals/e-Orbit project/00-paquete-maestro.md`
- e-Orbit polished manual: `User manuals/e-Orbit user manual.md`
- e-Orbit image-ready manual: `User manuals/e-Orbit user manual - image-ready.md`
- e-Orbit validation checklist: `User manuals/e-Orbit - manual validation checklist.md`
- e-Orbit image matrix: `User manuals/e-Orbit - image generation matrix.md`
- e-Orbit AI image prompts: `User manuals/e-Orbit - AI image prompts.md`
- e-Orbit implementation starter pack: `User manuals/e-Orbit - implementation starter pack.md`
- Per-product triplets (other products): `User manuals/e-Flex - ...`, `User manuals/e-Nova - ...`, `User manuals/e-Prime - ...`, `User manuals/e-Shield - ...`, `User manuals/e-Touch - ...`
- Per-product asset governance: `User manuals/assets/e-flex|e-nova|e-orbit|e-prime|e-shield|e-touch/README.md`
- Companion architectural audit: `User manuals/manual-standardization-current-state-audit.md`
- Publishing target / Docker stack: `Makefile`, `docker-compose.yml`, `wp-content/`, `data/products.json`, `wp-content/plugins/beslock-product-sync/beslock-product-sync.php`
