# Visual System Current State Audit
## Beslock Product Manuals — AI-Assisted Documentation Asset System

**Date:** 2026-05-11  
**Scope:** `User manuals/` — full visual-production infrastructure review  
**Purpose:** Inventory, architecture audit, and foundation for scalable AI-assisted image production  
**System type:** Visual reconstruction pipeline / technical illustration system / AI-assisted documentation asset system — NOT a generic image-generation workflow

---

## TABLE OF CONTENTS

1. [Current Visual System Overview](#1-current-visual-system-overview)
2. [Image Inventory](#2-image-inventory)
3. [Image Classification System](#3-image-classification-system)
4. [Prompt System Audit](#4-prompt-system-audit)
5. [Visual Consistency Analysis](#5-visual-consistency-analysis)
6. [Product Geometry & Visual Truth](#6-product-geometry--visual-truth)
7. [Image Production Workflow](#7-image-production-workflow)
8. [Realism vs Schematic Analysis](#8-realism-vs-schematic-analysis)
9. [High-Value Visual System Upgrades](#9-high-value-visual-system-upgrades)
10. [Conclusion](#10-conclusion)

---

## 1. CURRENT VISUAL SYSTEM OVERVIEW

### 1.1 System Description

The visual system currently operates as an **AI-assisted documentation asset pipeline** for a set of six smart-lock products (e-Flex, e-Nova, e-Orbit, e-Prime, e-Shield, e-Touch). Its function is to supply images for reconstructed user manuals and help-center pages where:

- Original OEM images are not available or not reusable in the new editorial context.
- Manuals are being rebuilt from OCR-extracted text.
- Most required images do not yet exist as actual files.
- Product visual source material is limited (typically one or very few reference views per product).

The system is therefore not a stock-photography curation workflow or a brand visual identity system. It is a **technical visual reconstruction pipeline**: it must produce realistic, documentary, technically accurate images that can serve as functional substitutes for real product photography and screen captures until those become available.

### 1.2 Current Architecture

The visual system is structured as a three-layer documentation stack:

**Layer 1 — Planning and prioritization documents**
- `<product> - image generation matrix.md` — image-by-image breakdown tied to specific manual pages
- `<product> - implementation starter pack.md` — asset list, file-naming conventions, integration checklist, folder structure

**Layer 2 — Prompt-ready generation guides**
- `<product> - AI image prompts.md` — copy-paste prompts for AI image generators (DALL·E or equivalent), with negative prompts and format recommendations

**Layer 3 — Asset storage infrastructure**
- `User manuals/assets/<product>/README.md` — naming conventions, asset type expectations, page-to-image mapping, integration checklist

All six products have this three-layer structure in place. However, the depth and completeness of each layer varies significantly across products (see Section 2).

### 1.3 Visual Production Philosophy

Based on all existing documentation, the emerging editorial philosophy is:

- **Clarity over decoration:** images must be useful, not atmospheric. Each image serves a specific instructional purpose.
- **Realistic but not commercial:** the style target is documentary/technical photography — clean, controlled, legible — not advertising.
- **One action per image:** each image should show one interaction, one product state, or one action. Compound scenarios are avoided.
- **AI visuals as placeholders, not finals:** AI-generated images are explicitly intended as support assets that can be replaced by real product captures or real app screenshots when available.
- **App screens = real captures preferred:** the preferred source for app/UI images is real device captures, not mockups or AI-generated screens. If real captures are unavailable, sober, clearly-identifiable support mockups are acceptable.
- **Avoid generated text inside images:** a consistent and well-founded constraint — AI-generated text within images is unreliable and potentially misleading in a technical manual.
- **Domestic, clean, ordered environments:** interaction and context images favor a residential, neutral, well-lit environment that matches the product's end-use context.

### 1.4 Intended Editorial Role of Images

Images in this system serve three editorial functions:

| Role | Description | Examples |
|---|---|---|
| **Hero / orientation** | Establishes product identity and context | `hero-main`, `installed-context` |
| **Instructional support** | Illustrates a specific step or action | `fingerprint-use`, `add-admin-action`, `link-qr` |
| **Troubleshooting support** | Illustrates a problem scenario without dramatizing | `troubleshoot-fingerprint`, `troubleshoot-app-connection` |

A fourth role — **editorial/downloads support** — appears in the documentation image (`downloads-docs`) but is lower priority.

### 1.5 Workflow Assumptions

The current architecture assumes:
- A 3-round generation cycle per image (3 variants → select 1 → refine if needed)
- Content and images can be produced in parallel (not sequentially blocked)
- AI-generated images will be progressively replaced by real captures as the project matures
- File naming follows a deterministic `<product-slug>-<function>.jpg` convention
- CMS or frontend integration will happen after image production, using the pre-defined file names as stable references

---

## 2. IMAGE INVENTORY

### 2.1 Summary Table — Per-Product Artifact Count

| Product | AI Prompt File | Matrix File | Starter Pack | Asset README | User Manual | Image-Ready Manual | Validation Checklist | Project Subfolder |
|---|---|---|---|---|---|---|---|---|
| e-Flex | ✓ | ✓ | ✓ | ✓ | PDF only | — | — | — |
| e-Nova | ✓ | ✓ | ✓ | ✓ | PDF only | — | — | — |
| e-Orbit | ✓ (full) | ✓ (full) | ✓ (full) | ✓ | PDF + MD | ✓ | ✓ | ✓ (7 docs) |
| e-Prime | ✓ | ✓ | ✓ | ✓ | PDF only | — | — | — |
| e-Shield | ✓ | ✓ | ✓ | ✓ | PDF only | — | — | — |
| e-Touch | ✓ | ✓ | ✓ | ✓ | PDF only | — | — | — |

### 2.2 Planned Image Slots Per Product

All six asset READMEs define the same 11 image slots:

| Slot # | Asset Name Pattern | Editorial Role | Page / Use |
|---|---|---|---|
| 1 | `<product>-hero-main` | Hero | Hub / product page |
| 2 | `<product>-installed-context` | Hero / context | First steps / installation |
| 3 | `<product>-add-admin-action` | Instructional | Add administrator |
| 4 | `<product>-pin-use` | Instructional | Register PIN |
| 5 | `<product>-fingerprint-use` | Instructional | Register fingerprint |
| 6 | `<product>-language-settings` | Instructional | Change language |
| 7 | `<product>-app-add-device` | Instructional (app) | Add device in Smart Life |
| 8 | `<product>-link-qr` | Instructional (app) | QR pairing |
| 9 | `<product>-troubleshoot-fingerprint` | Troubleshooting | Fingerprint not recognized |
| 10 | `<product>-troubleshoot-app-connection` | Troubleshooting | Cannot connect to app |
| 11 | `<product>-downloads-docs` | Editorial support | Downloads / documentation section |

**Total planned image slots across all products:** 6 × 11 = **66 image slots**

### 2.3 Existing Images (Actual Files)

**All asset folders currently contain only README documentation. No image files exist in any `assets/<product>/` directory.**

| Product | Planned | Existing | Production Rate |
|---|---|---|---|
| e-Flex | 11 | 0 | 0% |
| e-Nova | 11 | 0 | 0% |
| e-Orbit | 11 | 0 | 0% |
| e-Prime | 11 | 0 | 0% |
| e-Shield | 11 | 0 | 0% |
| e-Touch | 11 | 0 | 0% |
| **Total** | **66** | **0** | **0%** |

### 2.4 Prompt Coverage Per Product

| Product | Detailed prompts (with format + negative prompt + variants) | Light prompts (name + brief description only) |
|---|---|---|
| e-Orbit | 10 (slots 1–10; slot 11 implied by matrix) | 0 |
| e-Flex | 3 (slots 1–3) | 0 |
| e-Nova | 3 (slots 1–3) | 0 |
| e-Prime | 3 (slots 1–3) | 0 |
| e-Shield | 3 (slots 1–3) | 0 |
| e-Touch | 3 (slots 1–3) | 0 |

**Prompt gap:** 5 products × 8 missing slots = **40 un-prompted image slots** across the non-Orbit products. An additional slot 11 (downloads-docs) is implicitly planned but has only a brief mention in e-Orbit's matrix.

### 2.5 Matrix Coverage Per Product

| Product | Image matrix depth | Entries with page URL | Entries with priority | Entries with status |
|---|---|---|---|---|
| e-Orbit | 11 entries, full structured fields | ✓ (all) | ✓ (all) | ✓ (all = "pending") |
| e-Flex | 7 category names only | — | Partial (first/later tiers) | — |
| e-Nova | (same light format as e-Flex) | — | — | — |
| e-Prime | (same light format as e-Flex) | — | — | — |
| e-Shield | (same light format as e-Flex) | — | — | — |
| e-Touch | (same light format as e-Flex) | — | — | — |

### 2.6 Image Slots with No Prompt in Any Product

Across all products, the following image categories lack prompts:

- `<product>-pin-use` (slot 4) — only e-Orbit has a matrix entry; no product has a standalone copy-paste prompt
- `<product>-language-settings` (slot 6) — only e-Orbit has a prompt; others have no prompt
- `<product>-troubleshoot-fingerprint` (slot 9) — only e-Orbit has a prompt
- `<product>-troubleshoot-app-connection` (slot 10) — only e-Orbit has a prompt
- `<product>-downloads-docs` (slot 11) — only e-Orbit has a prompt

### 2.7 Additional Image Requirements Not Yet Catalogued

The current image inventory covers the MVP Fase 1 scope. The following image categories appear in the `e-Orbit user manual - image-ready.md` as `[IMAGEN SUGERIDA: ...]` markers but do not have corresponding prompt entries:

- "interacción general con panel de usuario" (add user — distinct from add admin)
- Installation/mounting visuals (implied but not catalogued)
- Factory reset visuals (not catalogued in any document)
- Battery replacement visuals (not catalogued)
- Door alignment or mechanical troubleshooting (not catalogued)

---

## 3. IMAGE CLASSIFICATION SYSTEM

### 3.1 Image Type Taxonomy

Based on existing documentation, the following image types are present or implied:

#### Type A — Hero / Product Identification
- **Examples:** `hero-main`, `installed-context`
- **Editorial purpose:** Establish product identity; orient the user; serve as visual anchor for hub pages and first-steps sections
- **Visual register:** Product-in-context realistic photography
- **Count planned:** 2 per product × 6 = 12 images

#### Type B — Interaction / Instructional
- **Examples:** `add-admin-action`, `pin-use`, `fingerprint-use`, `language-settings`
- **Editorial purpose:** Support step-by-step instructions; show what the user's hand and the product look like during a specific action
- **Visual register:** Realistic documentary — tight crop, one action, clean background
- **Count planned:** 4 per product × 6 = 24 images

#### Type C — App / Digital Interface
- **Examples:** `app-add-device`, `link-qr`
- **Editorial purpose:** Support app-pairing flows; orient user to what they see on-screen
- **Visual register:** Contextual (person + phone + lock) for context shots; ideally real screen captures for UI detail
- **Count planned:** 2 per product × 6 = 12 images

#### Type D — Troubleshooting
- **Examples:** `troubleshoot-fingerprint`, `troubleshoot-app-connection`
- **Editorial purpose:** Illustrate a problem scenario in a calm, non-alarmist way; support diagnostic articles
- **Visual register:** Same documentary realism as Type B, with a subtle neutral-frustration or "checking" gesture
- **Count planned:** 2 per product × 6 = 12 images

#### Type E — Editorial Support
- **Examples:** `downloads-docs`
- **Editorial purpose:** Accompany download/documentation sections; evoke the concept of product documentation
- **Visual register:** Still-life / editorial composition — product + documents or tablet
- **Count planned:** 1 per product × 6 = 6 images

### 3.2 Image Types Not Yet Present in the System

| Missing Type | Description | Likely need |
|---|---|---|
| **Installation diagrams** | Steps for physical mounting; screw positions, door prep | Medium (not yet in any product's matrix) |
| **Wiring / terminal diagrams** | Electrical connection for products with wired components | Low-to-medium (schematic, not photographic) |
| **Product anatomy / callout** | Labeled view of product components | High (for orientation and troubleshooting) |
| **Reset procedure** | Factory reset sequence, button positions | Medium |
| **Battery access / replacement** | How to open and replace batteries | Medium |
| **App UI screens** | Actual Smart Life app navigation captures | High (explicitly preferred over AI generation) |
| **Error indicator states** | LED or beep patterns indicating errors | Low (possibly more text/icon than photo) |

### 3.3 Reusability Assessment

Several image slots have near-identical visual requirements across products:

- `app-add-device` — all 6 products use the same app (Smart Life); the app UI is identical. **This is a strong candidate for a single shared contextual image** (person with phone in front of door) with a product-specific variant only if needed.
- `link-qr` — same app, same QR flow. Similar reuse opportunity.
- `downloads-docs` — product-agnostic composition; could potentially use one image shared across products or very minor variants.

---

## 4. PROMPT SYSTEM AUDIT

### 4.1 e-Orbit Prompt System (Reference Level)

The e-Orbit AI image prompts file represents the **current reference level** for prompt quality in the system. Key characteristics:

**Structural completeness:**
- Each image slot has: named identifier, use context, full prompt text, negative prompt, recommended format, and optional variants.
- Master prompts by category (hero, action, app, troubleshooting) provide a modular base.
- A master negative prompt captures cross-category constraints.

**Prompt philosophy:**
- Prompts are structured for **realistic documentary photography simulation**, not AI artistic generation.
- Prompts describe scene composition, lighting, subject behavior, and exclusion constraints explicitly.
- Negative prompts systematically exclude the most common AI failure modes: deformed hands, in-image text, futuristic aesthetics, chaotic backgrounds, and low resolution.

**Modularity:**
- e-Orbit has 4 master prompt templates by category (hero, action, app+product, troubleshooting). These function as a modular base that can generate specific prompts by adding subject/context details.
- The structure supports prompt reuse across similar image types within the product.

### 4.2 Non-Orbit Prompt Coverage (e-Flex, e-Nova, e-Prime, e-Shield, e-Touch)

The five non-Orbit products each have exactly **3 prompt entries** in their AI image prompts files (hero, installed-context, interaction-with-panel). These prompts:

- Follow the same structural pattern as e-Orbit prompts (same language, same negative prompt where present)
- Are functionally **identical to e-Orbit prompts except for the product name substitution**
- Do not include format recommendations, variant suggestions, or per-image negative prompts
- Cover only slots 1–3 of the 11-slot inventory

This is a significant **prompt coverage gap**: 8 of 11 planned image slots per non-Orbit product have no prompt at all.

### 4.3 Prompt Consistency Analysis

| Criterion | e-Orbit | Non-Orbit products |
|---|---|---|
| Full prompt text | ✓ (all 10 active slots) | ✓ (3 slots only) |
| Negative prompt | ✓ (per-image + master) | Partial (slot 1 only) |
| Format recommendation | ✓ (all slots) | — |
| Variant options | ✓ (all slots) | — |
| Page/use context | ✓ | — |
| Master prompt templates | ✓ (4 categories) | — |
| Master negative prompt | ✓ | — |

### 4.4 Prompt Modularity Assessment

The e-Orbit system shows emerging prompt modularity through:
1. **Master prompts per category** — reusable base phrases for each image type
2. **Master negative prompt** — a single exclusion list that covers all categories
3. **Per-slot specificity layer** — subject-specific additions on top of the master base

This modular architecture is **partially applied** in the current system. The same structure has not been formalized for cross-product use, even though the logic already supports it.

### 4.5 Identified Prompt Gaps and Inconsistencies

1. **Product-specificity gap:** Prompts for all products name the product (e.g., "cerradura inteligente moderna e-Orbit") but contain no product-specific physical description. An AI model generating from these prompts would produce a generic smart lock, not a recognizable e-Orbit, e-Flex, etc. The prompts do not include any physical differentiators (form factor, panel shape, sensor position).

2. **Missing interaction-type prompts for 5 products:** PIN use, fingerprint use, language settings, app device-add, QR linking, troubleshooting (fingerprint), troubleshooting (app), downloads — no prompts exist for any of these for e-Flex, e-Nova, e-Prime, e-Shield, or e-Touch.

3. **Format not defined for non-Orbit products:** Without format guidance, image crops and aspect ratios will be inconsistent across the system.

4. **No cross-product negative prompt master:** Each product would benefit from a shared master negative prompt to ensure consistent exclusion rules. Currently only e-Orbit has this.

5. **App prompts assume physical co-presence of phone and lock:** This works for contextual app images but does not address UI-only screens, which require real captures.

---

## 5. VISUAL CONSISTENCY ANALYSIS

### 5.1 Currently Defined Standards

| Standard | Status | Source |
|---|---|---|
| Clean, domestic backgrounds | ✓ Defined | All prompt files, `02-guia-estilo-visual.md` |
| Soft/natural lighting | ✓ Defined | All prompt files |
| Realistic documentary style (not commercial) | ✓ Defined | Matrix docs, visual style guide |
| One action per image | ✓ Defined | `02-guia-estilo-visual.md` |
| No generated text inside images | ✓ Defined | All negative prompts |
| No deformed hands | ✓ Defined | All negative prompts |
| No futuristic/sci-fi aesthetics | ✓ Defined | All negative prompts |
| Avoid over-dramatic lighting | ✓ Defined | Negative prompts and style guide |
| Avoid advertising aesthetics | ✓ Defined | Multiple docs |
| File naming convention | ✓ Defined | All asset READMEs |
| Aspect ratio guidance per use | ✓ (e-Orbit) | Matrix doc section 7 |

### 5.2 Missing Standards

| Missing Standard | Risk Level | Impact |
|---|---|---|
| **Product-specific color/material reference** | High | AI will generate different finishes across images of the same product |
| **Camera distance / framing rules** | Medium | Close-up and wide shots may be inconsistent across generations |
| **Human subject parameters** | Medium | Gender, age, skin tone will vary randomly across image batches |
| **Background neutrality definition** | Medium | "Clean background" is interpreted differently; some iterations may use warm domestic tones, others cool/office environments |
| **Lighting temperature consistency** | Medium | Natural vs. warm artificial can vary |
| **Cross-product consistency rules** | Medium | No rule prevents e-Flex using a warmer color treatment than e-Shield |
| **Image status tracking** | High | No current mechanism to distinguish "planned" from "generated" from "approved" from "published" |
| **Aspect ratio guidance for non-Orbit products** | Medium | Cropping may differ across products |

### 5.3 Hidden Conventions Already Emerging

The following conventions appear implicitly across multiple documents without being explicitly stated as rules:

- **JPEG as default format** — all named assets use `.jpg` extension
- **Lowercase + hyphenated file names** — consistently applied across all asset READMEs
- **Slug-based product identifiers** — e-orbit, e-flex, e-nova, e-prime, e-shield, e-touch (lowercase, hyphenated)
- **Functional suffix naming** — `hero-main`, `installed-context`, `fingerprint-use`, etc. — function as a shared vocabulary that implicitly defines image types
- **Spanish-language prompts** — all prompt text is in Spanish, consistent with the manual language and intended audience

---

## 6. PRODUCT GEOMETRY & VISUAL TRUTH

### 6.1 Current State

The repository currently contains **no product-specific physical description documents** for any of the six products. There are:

- No canonical product renders or reference views stored in the repository
- No physical dimension or form-factor documentation for any product
- No labeled anatomy illustrations
- No canonical view definitions (front, 3/4, detail, panel-only, etc.)
- No sensor placement maps
- No keypad layout documentation
- No UI state documentation (panel idle state, panel active state, error indicator)

The only product-specific visual references are the OEM PDFs (`e-Orbit user manual.pdf`, etc.), which are present as source files but whose content has not been extracted into visual reference documents.

### 6.2 Risks of Visual Distortion in AI Generation

Without product geometry protection, the following risks are active for every image generation:

| Risk | Mechanism | Consequence |
|---|---|---|
| **Generic lock substitution** | AI generates a "modern smart lock" shape that does not match any Beslock product | Images cannot be validated as representing the correct product |
| **Inconsistent panel geometry** | Different generations produce different keypad shapes, button layouts, or sensor positions | Users may be confused by conflicting visual representations |
| **Inconsistent fingerprint sensor position** | Sensor appears on different zones of the panel in different images | Instructional images contradict each other |
| **Inconsistent form factor across batches** | Without a reference, the lock shape may vary significantly between the hero image and the fingerprint-use image | Visual system loses coherence even within a single product |
| **Cross-product visual contamination** | With prompts that are near-identical except for the product name, AI-generated images for different products may look identical or similar | Products cannot be visually differentiated |

### 6.3 What Is Currently Needed

To protect visual truth at a level consistent with a lightweight, AI-assisted documentation system, the following additions would provide significant protection without enterprise overengineering:

| Artifact | Purpose | Complexity |
|---|---|---|
| **Per-product physical descriptor paragraph** | Short text block describing the product's distinctive visible features (form factor, panel shape, color, sensor location) — to be inserted into prompts | Low |
| **Canonical view reference image** | One approved image per product (sourced from OEM PDF or product catalogue) stored in the assets folder as `<product>-reference.jpg` | Low |
| **Sensor/interaction zone notes** | Simple text noting where the fingerprint sensor and keypad are located on the panel | Low |

### 6.4 Current Validation Mechanism

The `ext-images/e-orbit/metadata/audit/manual-validation-checklist.md` file includes a visual validation section, but its checks are purely presence-based:

- "Existe imagen general del producto" ✓/✗
- "Existe imagen contextual de uso" ✓/✗
- etc.

There are **no quality or accuracy validation rules** — the checklist does not verify whether the generated image accurately represents the product, only whether an image exists. This is the sole current visual validation mechanism, and it is present only for e-Orbit.

---

## 7. IMAGE PRODUCTION WORKFLOW

### 7.1 Inferred Current Workflow

Based on existing documentation, the intended production workflow is:

```
[Matrix doc] → [Prompt file] → [AI generation (3 variants)] → [Manual selection] → [Optional refinement round] → [File naming] → [Asset folder placement] → [CMS/frontend integration]
```

**Step-by-step:**

1. **Plan:** Identify required images from matrix doc, prioritized by page importance
2. **Prompt:** Use copy-paste prompts from AI image prompts file (or derive from master templates)
3. **Generate:** Produce 3 variants per image in DALL·E or equivalent
4. **Select:** Choose one variant based on clarity, realism, documentary utility, product consistency
5. **Refine (if needed):** Adjust angle, lighting, background, hand position, or framing
6. **Name and export:** Use the predetermined file name from the asset README or starter pack
7. **Store:** Place in `assets/<product>/`
8. **Integrate:** Connect to CMS or frontend using the stable file name

### 7.2 Where Manual Work Is Currently Heavy

| Stage | Manual Load | Comment |
|---|---|---|
| Prompt creation for non-Orbit products | **High** — must be written from scratch for 8 slots × 5 products | No templates have been applied yet |
| Image selection from variants | **High** — requires human editorial judgment | Cannot be automated |
| Visual accuracy review | **High** — verifying the image represents the correct product | No automated check possible |
| App/UI screen capture | **High** — requires real device access | AI substitution is explicitly a fallback |
| Cross-product consistency review | **High** — no automated comparison tool | Not addressed in current docs |

### 7.3 Where Automation Could Realistically Help

| Stage | Automation Opportunity |
|---|---|
| Prompt expansion | Master prompt templates + product-specific descriptor paragraphs could automatically generate all 11 prompts per product |
| File renaming | Deterministic naming convention supports scripted renaming after download |
| Asset inventory tracking | A simple status CSV or YAML file per product could track planned/generated/approved/published states |

### 7.4 Where Human Review Is Essential

- Verifying that the lock in the image is visually consistent with the specific product
- Confirming hands/fingers are realistic and not deformed
- Approving that the "action" shown is readable and correct
- Deciding whether a generated image is usable as-is or needs a refinement round
- Approving replacement of AI-generated images with real captures

### 7.5 Integration Bottleneck

The current workflow has a structural bottleneck: **content and CMS integration are ready (starter packs, file names, page URLs are defined), but zero images exist**. This means the visual production stage is the sole blocker to a fully implemented product. The documentation infrastructure is ahead of actual production by several phases.

---

## 8. REALISM VS SCHEMATIC ANALYSIS

### 8.1 Framework

For each image category, the key question is: does **adding realism increase clarity**, or does it **introduce ambiguity, distraction, or dependency on accurate AI generation of hard-to-control details**?

### 8.2 Per-Category Analysis

#### Hero images (`hero-main`, `installed-context`)
- **Recommended style:** Highly realistic
- **Rationale:** Hero images establish product identity and trust. A clean, realistic product photo on a door communicates product quality and context immediately. Schematic treatment would reduce emotional engagement and contextual legibility.
- **AI suitability:** High — scene composition is well-defined and does not require product-specific geometric accuracy.

#### Keypad/PIN interaction (`pin-use`)
- **Recommended style:** Semi-realistic with strong compositional focus
- **Rationale:** The value of this image is showing "where to touch" and "what it looks like to enter a PIN." Extreme realism risks AI inventing incorrect numeric labels on keys. Schematic treatment (e.g., a diagram of the keypad with labeled zones) might actually convey more accurate information.
- **Caveat:** Do not rely on visible key numbers in AI-generated images. The image should show the gesture and approximate panel area, not readable key values.
- **Alternative option:** A simple labeled panel diagram (schematic) for PIN and language-code entry might outperform a realistic photo.

#### Fingerprint sensor use (`fingerprint-use`, `troubleshoot-fingerprint`)
- **Recommended style:** Semi-realistic — tight composition
- **Rationale:** The critical visual information (where to place finger, how to apply pressure) is well-served by a close-up photo-style image. Realism helps convey the tactile quality of the interaction. Schematic adds little value here unless sensor position is ambiguous.
- **AI suitability:** High — finger-on-sensor is a clear and reproducible scene. Negative prompts already protect against the main failure modes (deformed fingers, unclear sensor).

#### App pairing (`app-add-device`, `link-qr`)
- **Recommended style:** Hybrid — contextual photo (person + phone + door) AI-generated; app UI screen = real capture only
- **Rationale:** The contextual image (person with phone near door) is well-suited to AI generation. The actual app screen content (menus, buttons, flows) **must come from real device captures** because AI-generated app screens will contain incorrect labels, phantom menus, and misleading UI elements that could actively harm user comprehension. If no real captures exist, use a clearly labeled placeholder or cropped screenshot — not an AI-generated screen.
- **Risk:** The current prompt for `app-add-device` shows "smartphone with visible content" in the scene. Care must be taken that the screen content is either invisible/blurred or a known real capture.

#### Troubleshooting (`troubleshoot-fingerprint`, `troubleshoot-app-connection`)
- **Recommended style:** Semi-realistic, with deliberately restrained emotional register
- **Rationale:** Troubleshooting images must not alarm the user or exaggerate the problem. A slight "reviewing" or "pausing" gesture is sufficient. Excessive realism in facial expression or dramatic framing would be counterproductive.
- **Schematic alternative:** In some cases, a labeled diagram indicating "check this zone" might be clearer than a staged photo.

#### Installation / mounting (not yet catalogued)
- **Recommended style:** Diagrammatic / schematic preferred
- **Rationale:** Physical installation requires precise spatial information (screw positions, door bore dimensions, alignment). Realistic photography cannot reliably convey tolerances or labeled component positions. A schematic line drawing or annotated diagram is significantly more effective.
- **AI suitability:** Low — installation diagrams require spatial precision that AI image generation cannot guarantee. Prefer vector/diagram creation tools or adapted OEM diagrams.

#### Wiring / terminal connection (not yet catalogued)
- **Recommended style:** Schematic only
- **Rationale:** Electrical/wiring diagrams must be correct. AI-generated wiring images will invent connections. Any wiring diagram must come from verified OEM documentation or be created as clean schematic illustrations.
- **AI suitability:** Not suitable.

#### Product anatomy / callout (not yet catalogued)
- **Recommended style:** Hybrid — realistic product image with schematic callout overlays
- **Rationale:** An annotated view of the product (panel, sensor, keypad, indicators) requires both realistic product appearance and precise label placement. This is best achieved by taking a clean product photo and adding vector annotations — not by AI generation of the full composition.
- **AI suitability:** Partial — AI can produce the base product image; annotation layer must be added manually.

#### Downloads / documentation editorial (`downloads-docs`)
- **Recommended style:** Soft realistic editorial
- **Rationale:** This image has no instructional function — it accompanies a downloads section for visual texture. Mild stylization or editorial composition (product + manual on table) is appropriate. High precision is not required.
- **AI suitability:** High.

### 8.3 Summary Table

| Image Category | Recommended Style | AI Suitability | Key Constraint |
|---|---|---|---|
| Hero product | Realistic | High | Product geometry accuracy |
| Installed context | Realistic | High | Domestic/clean environment |
| Keypad/PIN | Semi-realistic | Medium | Avoid readable AI-generated key labels |
| Fingerprint use | Semi-realistic | High | Avoid deformed fingers |
| Language settings | Semi-realistic | High | Same as panel interaction |
| App pairing (context) | Realistic contextual | High | Phone screen must not show AI-invented UI |
| App pairing (UI detail) | Real capture only | Not suitable | Must be device capture |
| Troubleshooting | Semi-realistic | High | Restrained emotional register |
| Installation | Schematic / diagrammatic | Not suitable | Precision required |
| Wiring | Schematic only | Not suitable | Correctness required |
| Product anatomy callout | Hybrid | Partial | Annotation layer manual |
| Downloads editorial | Soft editorial | High | Low precision requirements |

---

## 9. HIGH-VALUE VISUAL SYSTEM UPGRADES

The following upgrades are directly compatible with the current lightweight project philosophy. They are ordered by estimated impact-to-effort ratio.

### 9.1 Per-Product Physical Descriptor Paragraph (Priority: High)

**What:** A short text block (3–5 sentences) per product describing its distinctive visible physical features — form factor, approximate dimensions, panel shape, panel color/finish, fingerprint sensor location, keypad type and position, indicator lights.

**Why:** This is the single highest-impact improvement to the prompt system. It would immediately reduce AI visual inconsistency across images of the same product, and across generations of the same product at different times. It costs almost nothing to write and dramatically improves prompt specificity.

**Where to add:** One new field in each AI image prompts file: `## Product visual descriptor`. This descriptor would be incorporated into all prompts for that product.

**Source:** Extract from OEM PDF product descriptions + any available product renders.

### 9.2 Prompt Expansion for Non-Orbit Products (Priority: High)

**What:** Expand each non-Orbit product's AI image prompts file from 3 entries to the full 11, following the e-Orbit structure.

**Why:** The current system has 40 un-prompted image slots across 5 products. Without prompts, production cannot begin. Since the e-Orbit prompt structure works well, the expansion is a direct adaptation exercise (substitute product name + add product descriptor paragraph).

**Effort:** Medium — largely mechanical adaptation with editorial review.

### 9.3 Image Status Tracking (Priority: High)

**What:** Add a lightweight status field to each matrix document entry (or create a per-product `<product>-asset-status.md` tracking file) with states: `planned` / `generated` / `selected` / `approved` / `published` / `replaced-by-real-capture`.

**Why:** Currently all images across all products are in state "pending" with no way to distinguish what has been generated, what has been approved, or what has been replaced. As production begins, tracking this will prevent confusion and duplicated work.

**Effort:** Low — can be added to existing matrix files.

### 9.4 Master Negative Prompt (Cross-Product) (Priority: Medium)

**What:** A single master negative prompt file or section in `User manuals/` that can be referenced by all product prompt files.

**Why:** Currently the master negative prompt exists only in e-Orbit's matrix file. The 5 other products do not have a master negative prompt — only slot 1 (hero) of each has a brief negative prompt. Standardizing this reduces effort per prompt and ensures consistent exclusions.

**Effort:** Very low — copy from e-Orbit, document as shared reference.

### 9.5 Aspect Ratio / Format Guide (Cross-Product) (Priority: Medium)

**What:** Add format guidance to non-Orbit product prompt files, using the same framework already defined in e-Orbit's matrix (16:9 hero, 4:3 article, 4:5 vertical interaction).

**Why:** Without format guidance, images produced for different products may have inconsistent crops, making it impossible to achieve visual coherence across the help center.

**Effort:** Very low — copy format guide from e-Orbit matrix to other products' documents.

### 9.6 Reference Image Storage (Priority: Medium)

**What:** For each product, store at least one approved canonical reference image in `assets/<product>/` with name `<product>-reference.jpg`. Source from OEM PDF renders or product catalogue images.

**Why:** A reference image protects against visual drift across AI generation sessions. When reviewing generated images, a reference image allows the reviewer to ask: "does this look like the right product?"

**Effort:** Low — extraction from existing PDFs or source files.

### 9.7 Image-Ready Manual Templates for Non-Orbit Products (Priority: Medium)

**What:** Create `<product> user manual - image-ready.md` versions for the five non-Orbit products, following the same `[IMAGEN SUGERIDA: ...]` marker structure as `e-Orbit user manual - image-ready.md`.

**Why:** The image-ready manual serves as the ground truth for which image slots are needed and where they are placed in the content flow. It makes the connection between images and manual sections explicit. Currently only e-Orbit has this.

**Effort:** Medium — requires adapting manual content from PDFs.

### 9.8 Shared App Context Prompt (Priority: Low-Medium)

**What:** Since all 6 products use Smart Life for app integration, define one shared prompt for the app-context image type (person + phone + door) that can be adapted with minor product-specific adjustments.

**Why:** The current system will generate 6 × 2 = 12 app-context images across products. The scenes are functionally identical. A shared base prompt with product-specific overlays reduces redundant work and ensures visual consistency across the app sections.

**Effort:** Low.

### 9.9 Validation Checklist for Non-Orbit Products (Priority: Low)

**What:** Create `<product> - manual validation checklist.md` for e-Flex, e-Nova, e-Prime, e-Shield, and e-Touch, following the e-Orbit checklist structure.

**Why:** The current validation mechanism (visual presence checks, editorial review, technical validation) exists only for e-Orbit. As non-Orbit products mature, a consistent validation artifact will support quality control.

**Effort:** Very low — direct adaptation of existing checklist.

---

## 10. CONCLUSION

### 10.1 System State Summary

The visual production system for Beslock product manuals is in a **well-planned but pre-production state**. The infrastructure is solid: naming conventions are defined, folder structures exist, image slots are catalogued, page-to-image mappings are established, and a generation workflow is documented.

However, **zero images have been produced**. The system is entirely in documentation/planning mode.

The **e-Orbit product** is the clear reference implementation — it has a complete and high-quality visual production stack (detailed prompts, structured matrix, image-ready manual, validation checklist, visual style guide, implementation guide). This stack should serve as the direct template for the other five products.

The **five non-Orbit products** have a lightweight first layer of visual production documentation but are missing approximately 8 of 11 prompt entries each, and have much lighter matrix and starter pack documents.

### 10.2 Operational Priorities

In order of impact for enabling visual production:

| Priority | Action | Estimated impact |
|---|---|---|
| 1 | Write physical descriptor paragraphs for all 6 products | Eliminates cross-session and cross-product visual inconsistency |
| 2 | Expand prompts to full 11 slots for 5 non-Orbit products | Unblocks production of 40 currently un-prompted image slots |
| 3 | Begin generation of e-Orbit images (infrastructure is ready) | Validates the workflow end-to-end before scaling |
| 4 | Add image status tracking to matrix docs | Enables production management across 66 total image slots |
| 5 | Source and store at least 1 reference image per product | Provides visual truth anchor for AI generation quality control |

### 10.3 System Architecture Assessment

**What works well:**
- File naming convention is clean, consistent, and deterministic
- Page-to-image mapping is explicit and useful for CMS/frontend integration
- The e-Orbit prompt system is well-structured and production-ready
- The philosophy (clarity over decoration, realistic but not commercial, AI as placeholder) is sound and well-articulated
- The modular prompt structure (master templates + per-slot specifics) is effective and extensible
- The asset folder structure and README convention are clean and appropriate for the current scale

**What is missing:**
- Product geometry protection (physical descriptors, canonical reference views)
- Full prompt coverage for 5 products
- Any image status tracking mechanism
- App/UI real-capture workflow and placeholder strategy
- Schematic/diagram production pathway for installation and anatomy image types
- Validation checklists for non-Orbit products

**What is consistent with the project philosophy:**
- All recommended upgrades are lightweight, text-based, and fit the current documentation-first approach
- None require new tooling or enterprise-level processes
- The progression from AI placeholders to real captures is structurally supported and should be preserved

### 10.4 Note on System Type

This system is not a generic image-generation workflow. It is a **visual reconstruction pipeline for a technical manual standardization project**. Images are being produced to replace missing or unusable OEM imagery in reconstructed technical documentation. The constraints and quality requirements are therefore those of technical illustration and documentary photography — not commercial design or marketing visual production. Future AI systems working on this pipeline should maintain this distinction: every image decision should be evaluated against the question "does this make the manual clearer and more accurate for a user who needs help with their product?" — not "does this look impressive?"
