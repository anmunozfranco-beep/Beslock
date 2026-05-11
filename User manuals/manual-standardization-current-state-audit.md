# Manual Standardization — Current-State Architecture & Editorial Audit

> Scope: `User manuals/` at commit `b2f9a5ff4264928f0e80e98f494382366068ca31`.
> Purpose: serve as a current-state architecture document, editorial system audit, and foundation for future evolution by another AI system.
> Approach: inspect, do not redesign. The system is partially mature; this report assumes existing decisions are deliberate.

---

## 1. Project purpose & design philosophy

### What the system is optimizing for
The `User manuals/` subsystem is not a generic AI-image project — it is an **editorial normalization platform** for OEM smart-lock manuals (`e-Orbit`, `e-Flex`, `e-Nova`, `e-Prime`, `e-Shield`, `e-Touch`). Its primary optimizations are:

- **Task-oriented usability** for end users (one page per real action).
- **Editorial consistency** across products that share family traits but not identical capabilities.
- **Dual-target output** (web help center + downloadable PDF) from a single normalized markdown source.
- **Decoupling content production from visual production**, so editorial work can ship before final imagery exists.
- **Honesty about uncertainty**: OCR-derived flows that are not yet visually validated are explicitly flagged in-line rather than silently dropped or fabricated.

### How the architecture appears to have evolved
Two distinct maturity tiers coexist in the same folder, and that tiered layout is itself the architecture:

1. **Reference / pilot product (`e-Orbit`)** — fully developed:
   - Source PDF
   - Two markdown manuals (`e-Orbit user manual.md` for content, `e-Orbit user manual - image-ready.md` for layout-with-imagery)
   - Image generation matrix, AI prompts, implementation starter pack
   - Validation checklist
   - A dedicated `e-Orbit project/` sub-folder with editorial guide, visual guide, CMS seed content, MVP backlog, weekly schedule, and master package
2. **Sibling products (`e-Flex`, `e-Nova`, `e-Prime`, `e-Shield`, `e-Touch`)** — skeletal:
   - PDF
   - Trimmed clones of the three "satellite" docs (image prompts, image generation matrix, implementation starter pack), each ~16–32 lines.
   - Empty `assets/<slug>/` folder with a uniform README.

The pattern is a **template-by-fork model**: e-Orbit is the canonical reference; other products are stubs waiting to be expanded against the same shape.

### Editorial philosophy (inferred)
- **"Escribir para ayudar a hacer"** — the explicit principle from `01-guia-estilo-editorial.md`. Procedural, action-first writing.
- **One action per page, one image per action.** Reflected in both the manual structure and the image matrix.
- **Verb-initial steps, consistent menu-route formatting** (`**Agregar usuario → Agregar administrador**`).
- **Prudent flagging of OCR-derived data** ("Conviene validar estos códigos visualmente con la versión real…").
- **Reusability over per-product reinvention**: shared structural skeleton, shared naming convention, shared image categories.
- **Spanish-first** content and slugs.

### Assumptions baked into the structure
- All products in scope are smart locks → can share a base information architecture (admin, user, PIN, fingerprint, language, app, QR, troubleshooting).
- The Smart Life app is a shared dependency across the family.
- Web is the primary delivery surface; PDF is a derived artifact.
- AI imagery is acceptable as a temporary stand-in, designed to be replaced later by real captures.
- The CMS/frontend will be built on a deterministic URL scheme (`/productos/<slug>/...`).

### How the project balances competing concerns
| Concern | How it is handled |
|---|---|
| Usability | Task-oriented page model with "qué necesitas antes / pasos / qué validar después / problemas frecuentes". |
| Standardization | Identical 7-point page template (`01-guia-estilo-editorial.md` §5) applied across products. |
| Flexibility | Per-product satellite docs (prompts/matrix/starter pack) can diverge in depth without breaking the shared shape. |
| Maintainability | Per-product asset folders, slug-prefixed file names, shared validation checklist pattern. |
| Product-specific adaptation | `image-ready` variant separates content from layout-with-images; per-product matrices allow product-specific imagery. |

---

## 2. Current repository structure

```text
User manuals/
├── <Product> user manual.pdf                    ← OEM source (one per product)
├── <Product> - AI image prompts.md              ← copy/paste prompts for image AI
├── <Product> - image generation matrix.md       ← imagery plan, IDs, page mapping
├── <Product> - implementation starter pack.md   ← page list + asset list + folder layout
│
├── e-Orbit user manual.md                       ← normalized editorial manual (reference product)
├── e-Orbit user manual - image-ready.md         ← layout-with-image-slots variant
├── e-Orbit - manual validation checklist.md     ← editorial/technical/visual QA gate
│
├── e-Orbit project/                             ← deeper documentation set (only for the pilot)
│   ├── 00-paquete-maestro.md
│   ├── 01-guia-estilo-editorial.md
│   ├── 02-guia-estilo-visual.md
│   ├── 03-seed-content-cms.md
│   ├── 04-backlog-mvp-fase-1.md
│   ├── 05-cronograma-semanal.md
│   ├── 06-starter-pack-implementacion.md
│   └── README.md
│
└── assets/
    └── <slug>/
        └── README.md                            ← naming/organization convention per product
```

### Module / responsibility map (inferred)
| Artifact type | Responsibility |
|---|---|
| `<Product> user manual.pdf` | Immutable OEM source of truth (input). |
| `<slug>/manual_raw.txt` (upstream, in `generated_manuals/`) | OCR baseline produced by `process_manuals.py`. |
| `<Product> user manual.md` | Normalized, editorially clean manual. Source of truth for downstream renderers. |
| `<Product> user manual - image-ready.md` | Layout target with `[IMAGEN SUGERIDA: ...]` slots. Bridges editorial → visual production. |
| `<Product> - image generation matrix.md` | Production plan: image IDs, page URLs, prompts, negative prompts, formats, priorities, status. |
| `<Product> - AI image prompts.md` | Operational copy/paste sheet for the image AI tool. |
| `<Product> - implementation starter pack.md` | Cross-cuts content + assets + URLs into one MVP integration brief. |
| `<Product> - manual validation checklist.md` | Pre-publication QA gate (editorial / technical / visual / structural). |
| `assets/<slug>/README.md` | Per-product asset conventions and image↔page mapping. |
| `e-Orbit project/` | Reference editorial+governance bundle for the pilot product. |

### Important entry points for an evolving AI agent
- **Pilot, end-to-end**: `e-Orbit user manual.md` → `e-Orbit user manual - image-ready.md` → `e-Orbit - image generation matrix.md` → `e-Orbit - AI image prompts.md` → `assets/e-orbit/README.md` → `e-Orbit - manual validation checklist.md`.
- **Editorial law**: `e-Orbit project/01-guia-estilo-editorial.md` (tone, rules, page template).
- **Visual law**: `e-Orbit project/02-guia-estilo-visual.md` (visual principles, components, image criteria).
- **CMS contract**: `e-Orbit project/03-seed-content-cms.md` (URL scheme).
- **Schedule/scope contract**: `04-backlog-mvp-fase-1.md`, `05-cronograma-semanal.md`, `06-starter-pack-implementacion.md`, `00-paquete-maestro.md`.

### Architectural patterns already emerging
- **Reference + clones** (e-Orbit is the master template; other products are reduced clones).
- **Three-document satellite around each PDF** (prompts / matrix / starter pack) — a stable reusable triad.
- **Two-state markdown** (`user manual.md` = pure content; `user manual - image-ready.md` = content + image hooks). Currently realized only for e-Orbit.
- **Per-product asset namespacing** with slug-prefixed file names.
- **Convention-as-code via README files** in each `assets/<slug>/` folder, not via a central config.

---

## 3. Content pipeline

The full content pipeline crosses outside `User manuals/` (OCR happens upstream in `tools/manual_ocr/` writing to `generated_manuals/<slug>/`) but `User manuals/` is the editorial layer that consumes that output.

```
OEM PDF (User manuals/*.pdf)
   │
   ▼  [upstream] python process_manuals.py
generated_manuals/<slug>/manual_raw.txt
generated_manuals/<slug>/manual.md          ← machine-OCR baseline
generated_manuals/<slug>/manual.json
generated_manuals/<slug>/extraction_report.md
generated_manuals/<slug>/extracted_images/
   │
   ▼  [editorial normalization — currently human/AI assisted]
User manuals/<Product> user manual.md       ← canonical editorial manual
   │
   ├── ▼ [layout adaptation]
   │   User manuals/<Product> user manual - image-ready.md
   │
   ├── ▼ [imagery planning]
   │   <Product> - image generation matrix.md
   │   <Product> - AI image prompts.md
   │
   ├── ▼ [integration planning]
   │   <Product> - implementation starter pack.md
   │   e-Orbit project/03-seed-content-cms.md   (CMS URL contract)
   │
   ├── ▼ [QA gate]
   │   <Product> - manual validation checklist.md (only e-Orbit today)
   │
   ▼
Web help center  (CMS-rendered from .md, paths under /productos/<slug>/...)
Downloadable PDF (re-derived from the standardized manual)
```

### Where transformations occur
- **OCR → raw text → AI-ready md → JSON**: outside this folder (`tools/manual_ocr/extract_manual.py`, invoked via `process_manuals.py`).
- **Raw OCR → editorial manual**: inside `User manuals/`, currently a manual/AI-assisted transformation. Evidence: in `e-Orbit user manual.md` §7 the language-change codes (`888#`, `3009#`) are introduced with an explicit "extracción disponible muestra…" note — i.e. the editorial layer is consciously rephrasing OCR findings rather than copying them.
- **Editorial manual → image-ready manual**: by interleaving `[IMAGEN SUGERIDA: ...]` markers (see `e-Orbit user manual - image-ready.md`).
- **Image-ready manual → matrix → prompts**: each image marker becomes an `IMG-NNN` row, then a copy/paste prompt with negative prompt and format.
- **All of the above → starter pack**: collapses content+assets+URLs into a single MVP brief.

### Where automation already exists
- **OCR ingestion** is fully scripted (`process_manuals.py`).
- **Filename + slug conventions** are deterministic and consistent enough to be templated.
- **Image ID scheme** (`IMG-001`…`IMG-011`) and asset naming (`<slug>-<purpose>.jpg`) are mechanical.
- **Page→asset→URL mapping** is enumerated in implementation starter packs and asset READMEs (could be machine-consumed).

### Where manual intervention still exists
- Translating `manual.md` (OCR baseline) into `User manuals/<Product> user manual.md` (editorial manual).
- Producing the `image-ready` variant.
- Writing the matrix and prompts (only e-Orbit's are detailed; others are placeholder).
- Validating OCR-extracted codes against the real device.
- Filling each `assets/<slug>/` folder with actual imagery.
- Running the validation checklist.

### Where standardization rules already exist
- **Page template** (`01-guia-estilo-editorial.md` §5): qué vas a hacer → qué necesitas antes → pasos → recomendación → qué validar después → problemas frecuentes → siguiente paso.
- **Tone rules** (§3) and **terminology rules** (§4: always "e-Orbit", always "Smart Life", verb-first steps, consistent menu routes).
- **Visual rules** (`02-guia-estilo-visual.md`): claridad sobre decoración, una acción por imagen, etc.
- **URL scheme** (`03-seed-content-cms.md`): `/productos/<slug>/<seccion>/<accion>`.

---

## 4. Image pipeline

### Source / handling layers
| Layer | Where | Notes |
|---|---|---|
| Source images | `generated_manuals/<slug>/extracted_images/` (upstream) | Raw page rasterizations from OCR; not editorial. |
| AI-generated images | `User manuals/assets/<slug>/` | Conventionally `<slug>-<purpose>.jpg`; not yet checked in. |
| Real captures | Same folder, intended to **replace** AI placeholders later (asset README §7). |
| Web-ready / thumbnails | Optional sub-folders described in asset README §4 (`ai-generated/`, `real-captures/`, `web-ready/`, `thumbnails/`) — present as documented convention, not yet active. |

### Prompt system
Two-document pattern per product:
- **Image generation matrix** — structured rows with the schema documented in `e-Orbit - image generation matrix.md` §3:
  `id, pagina, tipo_de_imagen, objetivo, descripcion_visual, prompt_base, negative_prompt, formato, prioridad, estado, notas`.
- **AI image prompts** — clean copy/paste version of those prompts plus reusable "master prompts by category" (Producto hero, Acción de uso, App + producto, Troubleshooting) and a "negative prompt maestro".

The pilot defines **categorical master prompts** (`§5 A–D` of the matrix), so each new product only needs to swap the product noun while inheriting the visual style guarantees.

### Image matrix categories (stable taxonomy)
1. Hero principal del producto
2. Producto instalado en contexto real
3. Interacción con panel (admin/usuario)
4. Uso del teclado (PIN)
5. Uso del lector de huella
6. Configuración / cambio de idioma
7. Uso de app para agregar dispositivo
8. Vincular por QR
9. Troubleshooting de huella
10. Troubleshooting de app
11. Documentación / descargas

These map 1:1 to the page list in `06-starter-pack-implementacion.md` and `03-seed-content-cms.md`. This is a **shared visual ontology** for the smart-lock family.

### Naming / consistency systems
- Slug-prefixed, lower-case, hyphenated, no accents (`assets/<slug>/README.md` §2).
- One canonical filename per (product, purpose).
- Page → asset mapping explicit in two places (matrix and asset README §5) — currently duplicated, see §6/§7.

### Strengths
- Categorical master prompts give visual coherence across the product family with low marginal cost.
- Negative-prompt-maestro centralizes "what we never want" (text in image, deformed hands, futurism, etc.) — concrete editorial control over the AI.
- Format guidance per use (hero 16:9, article 4:3 or 4:5, card 1:1 or 4:5, download thumbnail 16:9) is consistent across the matrix.
- Status/priority columns make the matrix actionable as a production board.

### Bottlenecks & duplicated logic
- The page↔asset mapping appears in **three** places (image generation matrix, implementation starter pack, asset README). Drifts likely.
- Sibling products (e-Flex, e-Nova, e-Prime, e-Shield, e-Touch) lack the per-image rows — only category-level master prompts. Production for those products is not yet operational.
- Image `estado` column in the matrix is informally maintained in markdown rather than a tracked source.
- No mechanism (script or convention) to promote AI-generated assets into "real captures" cleanly when they arrive.

### Manual-heavy areas
- Writing per-image rows for each new product.
- Generating, choosing, refining variants (described in three rounds in `e-Orbit - AI image prompts.md` §12 — entirely manual).
- Replacing AI assets with real captures (no link from manual to specific asset filename in the markdown sources except indirectly via the matrix).

---

## 5. Manual standardization system

### How manuals are normalized
The OCR baseline (`generated_manuals/<slug>/manual.md`) is rewritten into a 7-step page template defined in `01-guia-estilo-editorial.md`:
1. qué vas a hacer
2. qué necesitas antes
3. pasos (verb-first, numbered)
4. recomendación o advertencia
5. qué validar después
6. problemas frecuentes
7. siguiente paso recomendado

The pilot manual (`e-Orbit user manual.md`) realizes a slightly looser variant of the same skeleton across 11 sections (Introducción, Primeros pasos, then per-action, then Problemas frecuentes, then Recomendación final).

### How different audiences are handled
- A single base manual targets the **end user**. There is no separate installer/admin/dev manual.
- Within the manual, audience nuance is handled by **role-aware sections** ("Agregar administrador" vs. "Agregar un usuario") and by **recomendación** boxes that distinguish admin-specific best practice (e.g., admin should leave a backup method).
- The "image-ready" variant targets the **layout/CMS audience** — same content, image hooks added, recommendations trimmed.

### How product technical differences are accommodated
- **Same skeleton, optional sections.** Products without QR/app simply omit those pages; the URL/asset scheme already namespaces them per product.
- **Per-product image matrices** decouple visual production from the shared editorial template.
- **Explicit "validar visualmente"** disclaimers wrap any code or flow that came from OCR but has not been confirmed against the real device — this is the system's "uncertainty type", and it is product-specific.
- **Per-product satellite docs** allow each product to grow more elaborate over time without mutating the others.

### Reusable vs product-specific
| Reusable across products | Product-specific |
|---|---|
| Editorial style guide (`01-guia-estilo-editorial.md`) | Manual contents (PDF, .md) |
| Visual style guide (`02-guia-estilo-visual.md`) | Image matrix rows |
| Image categories taxonomy | Image filenames (slug-prefixed) |
| Master prompts (per category) | Concrete prompts (per IMG-NNN row) |
| Negative-prompt maestro | Validation checklist (currently only e-Orbit) |
| URL scheme `/productos/<slug>/...` | The slug itself |
| Asset README template (currently 6 identical copies) | The product name in that README |
| Validation checklist structure | OCR'd menu codes (`888#`, `3009#`) |

### UX / readability strategy
- Short paragraphs, bulleted prerequisites, numbered steps, bolded menu routes, "qué validar después" closing each task — built for **scan-then-do** reading.
- Tone: claro, útil, cercano, ordenado, confiable, práctico (`01-guia-estilo-editorial.md` §3).
- Every section begins with the user goal, not with the device feature.

### Consistency strategy
- Naming: always **e-Orbit**, always **Smart Life** (rule §4).
- Step formatting: verb-first, lower-case starter (matches Spanish convention).
- Menu route formatting: bold, with arrow `→`.
- Visual: master prompts + negative-prompt maestro guarantee aesthetic consistency across imagery.

### Information hierarchy strategy
The hierarchy is: **product → section → task → step**, mirrored in the URL scheme: `/productos/<slug>/<seccion>/<accion>`. The manual headings (`## 3. Agregar un administrador`, `### Ruta de menú`, `### Paso a paso`) align with this hierarchy.

### Web vs PDF adaptation strategy
- The `.md` is the canonical artifact; the PDF is a downstream rendering of it (the PDF currently in the folder is the OEM original — the project intends to *replace* it later with a regenerated PDF from the standardized manual, see `00-paquete-maestro.md` §3 "Pendiente: maquetación o integración final").
- The `image-ready` variant is the bridge: it's structurally identical to the canonical manual but inserts image hooks for the layout pipeline. This means the editorial source is **single-source** but rendered twice.

---

## 6. Existing conventions

### Naming conventions
- **Product slug**: lower-case, hyphenated → `e-orbit`, `e-flex`, `e-nova`, `e-prime`, `e-shield`, `e-touch`.
- **Asset filenames**: `<slug>-<purpose>.jpg`, lower-case, no spaces, no accents (`assets/<slug>/README.md` §2).
- **Image IDs**: zero-padded sequence per product, `IMG-001`…`IMG-NNN`.
- **Top-level docs**: `<Product> - <kind>.md` where `<kind>` ∈ {AI image prompts, image generation matrix, implementation starter pack, manual validation checklist}.
- **Manual files**: `<Product> user manual.pdf`, `<Product> user manual.md`, `<Product> user manual - image-ready.md`.
- **CMS URLs**: `/productos/<slug>/<seccion>/<accion>` (Spanish, lower-case, hyphenated).

### Markdown conventions
- One H1 per file (the product name). H2 for the document subtitle. H2-numbered sections (`## 1.`, `## 2.`, …) inside.
- `---` rules between major sections.
- Bold for menu route segments and app/feature names (`**Smart Life**`, `**Agregar usuario → Agregar administrador**`).
- Backticked codes for OEM key sequences (`` `888#` ``, `` `3009#` ``).
- Verb-first step text, lower-case start.
- `[IMAGEN SUGERIDA: <descripción>]` as the image placeholder marker in the image-ready variant.

### Prompt conventions
Each image entry has, at minimum: prompt base / negative prompt / formato / variantes opcionales. Master prompts are grouped by category (A producto hero, B acción de uso, C app + producto, D troubleshooting). A single negative-prompt maestro is the catch-all baseline.

### Folder conventions
- PDFs and editorial markdown live at the top level of `User manuals/`.
- Per-product visual assets live under `User manuals/assets/<slug>/`.
- Deeper governance docs for a fully developed product live in `User manuals/<Product> project/` (only `e-Orbit project/` exists today).
- Optional asset sub-folders (`ai-generated/`, `real-captures/`, `web-ready/`, `thumbnails/`) are documented but unused.

### Asset conventions
- One canonical filename per (product, purpose).
- AI imagery is treated as a **placeholder** to be replaced by real captures.
- The asset README in each `assets/<slug>/` folder enumerates the canonical filename↔page mapping.

### Formatting conventions
- Spanish throughout.
- Sentence-case section titles.
- Numbered task pages mirror the hub navigation.

### Generation conventions (for IA imagery)
- 3 variants → choose 1 → refine in second round → optional third round for crops (hero, article header, card thumbnail). See `e-Orbit - AI image prompts.md` §12.
- Order of generation explicit (`§13` of the same file).
- Master prompts per category to enforce visual coherence; negative prompt to enforce visual hygiene.

### Reusable template conventions
- The 7-step page template from `01-guia-estilo-editorial.md` §5.
- The 11-row image matrix shape (e-Orbit reference).
- The asset README skeleton (6 instances are byte-equivalent except for the product name).
- The implementation starter pack structure (objetivo / páginas prioritarias / assets prioritarios / mapeo / carpetas / checklist / flujo / recomendaciones).

**Conventions that already feel stable and valuable**
- Slug + asset naming.
- The 7-step editorial page template.
- The image category taxonomy + master prompts.
- The URL scheme.
- The two-tier manual (`user manual.md` + `user manual - image-ready.md`).

---

## 7. Current maturity assessment

### Already robust
- The **OCR ingestion** layer is scripted, deterministic, and produces a clean per-slug folder structure (validated by `process_manuals.py` + `tools/manual_ocr/`).
- The **editorial style** (tone, page template, terminology rules) is coherent and explicitly documented.
- The **image taxonomy + master prompts** scale across the product family with very low cost.
- The **slug + asset naming** convention is uniform across all six products.
- The **CMS URL contract** is concrete enough to start frontend work.

### Already scales well
- Adding a new product to the satellite document model is mechanical: PDF + 3 stub markdown files + `assets/<slug>/README.md` (the existing 6 README copies prove it).
- The image matrix's master-prompt model means new products inherit visual style by construction.

### Fragile
- The **mapping table page↔asset↔URL** is duplicated in three locations (matrix, starter pack, asset README) without a single source of truth.
- The **status of each image** lives only in markdown rows (`Estado: pendiente`) — no machine-readable state, easy to drift.
- The **OCR codes embedded in the manual** (`888#`, `3009#`) carry an explicit "validar visualmente" warning but no formal review state. If the warning is removed prematurely, accuracy claims become silent.
- The **`image-ready` variant is currently re-typed**, not derived. If the canonical manual is edited, the image-ready twin must be edited by hand.

### Duplicated
- Six byte-identical `assets/<slug>/README.md` files (only the product name differs).
- Page lists appear in `03-seed-content-cms.md`, `06-starter-pack-implementacion.md`, the image matrix, and the implementation starter pack.
- Asset filename lists appear in the matrix, the starter pack, and the asset README.

### Overcomplicated
- The pilot has both `06-starter-pack-implementacion.md` (inside `e-Orbit project/`) **and** `e-Orbit - implementation starter pack.md` (at the root of `User manuals/`). Their content overlaps significantly. Some consolidation would simplify navigation without losing fidelity.

### Missing
- A **content-coverage map** showing which products have which artifacts. Today it is implicit and inferred from file presence.
- **Validation checklists for non-pilot products** — only e-Orbit has one.
- **`<Product> user manual.md`** for everything except e-Orbit. The other five products have only the OEM PDF, with no normalized editorial manual yet.
- **`<Product> user manual - image-ready.md`** for everything except e-Orbit.
- **A schema definition** for the image matrix (the field list is described in prose rather than as a JSON/YAML schema).
- **An index** at `User manuals/README.md` that explains how the documents fit together.

### Where technical debt could emerge
- Drift between the multiple page↔asset↔URL listings.
- Drift between `User manuals/<Product> user manual.md` and `… - image-ready.md` once the non-pilot products fill in.
- Conventions encoded only in prose READMEs (no linter, no template generator) — easy to violate accidentally as more products are onboarded.
- Spanish-only content with no translation strategy yet, even though `process_manuals.py` defaults to `spa+eng` OCR (`tools/manual_ocr/README.md`).

---

## 8. Current bottlenecks

Prioritized by practical impact on shipping the help center.

### 1. Editorial bottlenecks (highest practical impact)
- Only **1 of 6** products has a normalized editorial manual (`e-Orbit`). The other five sit at PDF + skeleton metadata.
- Only the pilot has a validation checklist; the rest cannot be QA-gated consistently.

### 2. Workflow bottlenecks
- Two manuals (`user manual.md` and `user manual - image-ready.md`) for the pilot — kept in sync **manually**.
- Three places to update when image↔page↔asset mapping changes.

### 3. Image bottlenecks
- Per-image rows exist only for e-Orbit; sibling products have only category-level master prompts, so production cannot start for them without first writing matrices.
- Image variant selection / refinement is a fully manual three-round process with no record of which variant was chosen and why.
- `Estado: pendiente` is the default everywhere — no tracking of progress beyond that.

### 4. Maintainability bottlenecks
- Six near-identical asset READMEs (no shared template referenced from a single source).
- No `User manuals/README.md` to orient a newcomer.
- The `e-Orbit project/` folder partly overlaps with the per-product satellite docs, so it is unclear which document "wins" if they ever diverge.

### 5. Scalability bottlenecks (relative to project size — modest)
- New product onboarding still requires hand-writing six near-identical files; tolerable at 6 products, painful at 20.
- Page list maintained as prose bullets in several files (no structured product manifest).

### 6. Consistency bottlenecks
- Terminology rules ("always **e-Orbit**", "always **Smart Life**") are not mechanically enforced.
- Image filename rules are documented but not validated against actual files.
- The image matrix schema is described in prose; nothing prevents a row from missing `negative_prompt` or `formato`.

---

## 9. High-value upgrade opportunities

These are compatible with the current philosophy: **template-by-fork, single editorial source per product, AI imagery as placeholder, web/PDF dual delivery**. They do **not** redesign the architecture.

### Editorial consistency (highest leverage, low cost)
1. Add a `User manuals/README.md` index that lists each product's artifacts and their status (PDF / OCR / editorial md / image-ready md / matrix / prompts / starter pack / validation). This is the missing "front door" of the folder.
2. Promote `e-Orbit project/01-guia-estilo-editorial.md` and `02-guia-estilo-visual.md` to **family-wide** documents by moving them up to `User manuals/` (or symlinking) and removing the implicit "pilot only" framing. They already read as universal rules.
3. Generalize the validation checklist (`e-Orbit - manual validation checklist.md`) into a **family template** by extracting the product-specific lines (`888#`, `3009#`, `Smart Life`) into a small per-product appendix.

### Production speed
4. For each non-pilot product, expand the satellite trio (`AI image prompts`, `image generation matrix`, `implementation starter pack`) to the same row-level depth as e-Orbit. The pilot's matrix already provides the per-row schema and the master prompts to start from.
5. Produce the missing `<Product> user manual.md` and `… - image-ready.md` for the five sibling products, applying the e-Orbit shape. Use the OCR output (`generated_manuals/<slug>/manual.md`) as the starting draft for each.

### Reduction of repetitive work
6. Replace the six near-identical `assets/<slug>/README.md` files with a shared `assets/README.md` documenting the convention once, plus a one-line per-product `assets/<slug>/README.md` that just states the product name. Today the repetition is harmless; tomorrow it diverges.
7. Define the **image matrix row schema** once (e.g., a YAML/JSON schema or a dedicated section in `02-guia-estilo-visual.md`) so each product's matrix can reference it instead of redocumenting the field list.

### Image consistency
8. Add a small **"chosen-variant log"** convention — one line per generated image inside the matrix's `notas` column or in a sibling `assets/<slug>/CHOSEN.md` — recording which variant prompt+seed was selected. Closes the audit loop on AI imagery without imposing tooling.
9. Treat the negative-prompt maestro as **append-only**: every time an unwanted artifact appears, add the term and never remove it. Keep that list at the top of `02-guia-estilo-visual.md`.

### Onboarding clarity
10. Inside the missing `User manuals/README.md`, add a "How a new product is added" recipe that lists, in order, the files to create and the conventions to follow (slug, asset names, page list, image categories). The pilot already shows the answer; codifying it removes guesswork.
11. Consolidate `e-Orbit project/06-starter-pack-implementacion.md` and `e-Orbit - implementation starter pack.md` into a single canonical document (or explicitly mark one as the summary). They overlap today.

### Future extensibility
12. Treat the **page list** as a small per-product manifest (e.g., a fenced YAML block inside the implementation starter pack) so it can later be consumed by a CMS-seed script without restructuring anything.
13. When a product genuinely diverges from the smart-lock template (different feature set, different audience), allow the `<Product> project/` folder to opt in (mirroring `e-Orbit project/`) rather than forcing the divergence into the satellite trio.
14. Keep AI imagery and real captures **co-located** with a single naming rule and a clear "real captures replace AI placeholders one-for-one when available" policy. The asset README §7 already states this; reinforce it in the family-wide visual guide.

### What to deliberately avoid
- A heavy CMS / pipeline framework that would replace the current markdown-first workflow.
- Auto-generating manuals from OCR without an editorial pass — the system's value is precisely that humans (or AI under editorial rules) rewrite the OCR baseline; bypassing it would erase the project.
- Splitting the manual into many small files per task. The current one-file-per-product manual is intentionally browsable end-to-end and renderable to PDF as a single artifact.
- Introducing a separate "translations" subsystem before the Spanish baseline is complete across all six products.

---

## 10. Output format / how to use this document

This file is intended to be:
- **A current-state architecture document.** Section 2 maps the folder; sections 3–5 describe the pipelines.
- **An editorial system audit.** Sections 1, 5, 6 capture the philosophy, the rules, and the conventions that already exist.
- **A foundation for future evolution.** Sections 7–9 isolate fragility, bottlenecks, and the smallest valuable upgrades — explicitly without prescribing a redesign.

Any AI system continuing this project should:
1. Treat e-Orbit as the **reference implementation** of every pattern in the family.
2. Treat `01-guia-estilo-editorial.md` and `02-guia-estilo-visual.md` as the **editorial laws** of the system.
3. Treat the **OCR output** as a *baseline*, not as content; always pass it through the editorial template before publication.
4. Keep AI imagery as **temporary stand-ins**, replaceable one-for-one by real captures using the existing slug+purpose filename rule.
5. Prefer **expanding the existing template-by-fork model** (more rows, more checklists, more sibling manuals) over inventing parallel structures.
