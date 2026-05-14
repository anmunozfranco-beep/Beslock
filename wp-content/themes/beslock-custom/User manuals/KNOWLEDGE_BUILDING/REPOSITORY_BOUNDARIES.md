# REPOSITORY BOUNDARIES

Status: Active governance.
Scope: Where every kind of artifact belongs in the BESLOCK repository.
Purpose: Eliminate ambiguity, prevent duplication, enforce canonical sources.

---

## 1. What belongs in `User manuals/`

`wp-content/themes/beslock-custom/User manuals/` is the **knowledge core root**.

It contains:
- `KNOWLEDGE_BUILDING/` — governance documents (this directory).
- `ext-images/` — product nuclei (the canonical knowledge homes).
- Shared editorial standards: `manual-document-package-standard.md`, `installation-manual-template.md`, `manual-document-package-maturity-matrix.md`.
- Site-level delivery contracts (transitional, to be reduced as nuclei take over): `manual-web-integration-manifest.json`, `manual-web-integration-matrix.md`, `manual-review-draft-index.md`.
- Audits: `manual-standardization-current-state-audit.md`, `visual-system-current-state-audit.md`.
- Shared visual rules under `visual-system/` (rules and registries only, no product-specific files after migration).
- Review previews under `review-previews/` (transitional).
- `ai-project-context-export.md` (transitional context export).

It must **not** contain after migration:
- Product-specific PDFs at the root (e.g. `e-Flex_1.pdf`, `e-Shield_1.pdf`).
- Product-specific markdown manuals at the root (e.g. `e-Flex user manual.md`, `e-Touch installation manual.md`).
- Product-specific image-prompt files, generation matrices, starter packs, or installation templates at the root.
- Product-specific files anywhere outside `ext-images/<slug>/`.

Legacy product-specific files at the root are **transitional** and must be migrated into the appropriate nucleus per `PHASE_1_IMPLEMENTATION.md`.

---

## 2. What belongs in `ext-images/`

`User manuals/ext-images/` is the **product knowledge core root**, despite its historical name.

It contains:
- One subdirectory per product, each a complete nucleus, named by lowercase kebab-case slug (`e-flex/`, `e-nova/`, `e-orbit/`, `e-prime/`, `e-shield/`, `e-touch/`).
- An `ext-images/README.md` declaring the directory's role.

It must **not** contain:
- Loose PNGs at the root after migration (current `e-Flex.png`, `e-Nova.png`, `e-Prime.png`, `e-Shield.png`, `e-Touch.png` are compatibility-only and will be retired once each nucleus owns its canonical PNG).
- Cross-product folders.
- Shared utilities, prompts, or registries.
- Anything that is not a product nucleus or the README.

---

## 3. What belongs in nuclei

A nucleus contains everything product-specific. The exhaustive list is defined in `PRODUCT_NUCLEUS_RULES.md` §1. Summary:

- `source-of-truth/` — OEM originals + normalized derivatives + the canonical PNG + OEM visual evidence.
- `structured-knowledge/` — semantic JSON objects.
- `visual-system/` — visual profile, anchors, prompts, conditioning, QA.
- `publishing/` — channel-ready surfaces.
- `automation/` — orchestration manifest and run records.
- `metadata/` — lineage, product-domain manifest, validation ledger.

A nucleus **must not** contain:
- Files belonging to another product.
- Site-wide governance files.
- Tooling.
- Shared registries.
- Generated images in `source-of-truth/` (generated visuals live in `publishing/` or `visual-system/qa/`).

---

## 4. What is shared / global

Shared assets live outside any single nucleus, with explicit homes:

| Shared asset                                  | Home                                                                                  |
|-----------------------------------------------|---------------------------------------------------------------------------------------|
| Governance documents                          | `wp-content/themes/beslock-custom/User manuals/KNOWLEDGE_BUILDING/`                   |
| Editorial standards and templates             | `wp-content/themes/beslock-custom/User manuals/` (root level standard files)          |
| Shared visual rules and registries            | `wp-content/themes/beslock-custom/User manuals/visual-system/` (non-product portions) |
| Site-level delivery contracts                 | `wp-content/themes/beslock-custom/User manuals/manual-web-integration-*`              |
| Repository tooling                            | `tools/` and root scripts (`process_manuals.py`, `visual_generation.py`)              |
| ComfyUI workflow registry                     | `tools/comfy/`                                                                        |
| OCR pipeline                                  | `tools/manual_ocr/`                                                                   |
| Staging OCR outputs                           | `generated_manuals/<slug>/` (staging only, not canonical)                             |
| Visual generation staging                     | `output/visual-generation/`                                                           |
| Database fixtures                             | `database/`                                                                           |
| Docker / runtime                              | `docker/`, `docker-compose.yml`, `Makefile`                                           |
| WordPress runtime                             | `wp-admin/`, `wp-includes/`, `wp-content/plugins/`, `wp-content/themes/`              |
| Repository-root summaries (legacy/runtime)    | Repository root (`*_SUMMARY.md`, `ARCHITECTURE.md`, `BEM_GUIDELINES.md`, etc.)        |

Rule: a "shared" asset must be used by at least two products. A shared asset used by only one product must be moved into that product's nucleus.

---

## 5. Forbidden repository patterns

The following patterns are forbidden (or transitional with a known retirement plan):

1. Product-specific PDFs, manuals, prompt files, or matrices at `User manuals/` root.
2. Product-specific assets under `User manuals/assets/` (legacy; migrate into nucleus `source-of-truth/` or `visual-system/`).
3. Product-specific subfolders under `User manuals/visual-system/products/` (legacy; migrate into the nucleus `visual-system/`).
4. Product-specific files duplicated between root locations and the nucleus.
5. Generated images promoted into `source-of-truth/`.
6. Cross-product imports inside any nucleus.
7. Workflow JSONs used outside the registered `tools/comfy/` registry.
8. Hardcoded slug-to-path mappings in tooling (must resolve through the shared product registry plus per-product manifests).
9. Editing a delivery surface (web/PDF) as the primary truth update path.
10. "Shared" files used by only one product.
11. Compatibility PNGs at `ext-images/` root after the corresponding nucleus owns its canonical PNG.
12. Two `data/products.json` files (root vs theme) without a documented canonical-source decision.

---

## 6. Duplication prevention rules

- An artifact has exactly one canonical home. Copies are forbidden.
- If a copy is unavoidable for a runtime constraint (e.g. a build step), the copy is generated from the canonical source by tooling and is not edited by hand.
- Generated copies must declare their canonical source in a header or sidecar manifest.
- Lineage manifests must record any generated copy and its canonical source.
- Migration that moves an artifact into the nucleus must delete the legacy copy in the same operation, not later.

---

## 7. Canonical-source rules

For any class of artifact, the canonical source is named explicitly and is the only writable location. Other locations are read-only or generated.

| Artifact class                          | Canonical source                                                                  |
|-----------------------------------------|-----------------------------------------------------------------------------------|
| Product OEM documents                   | `ext-images/<slug>/source-of-truth/manuals/`                                      |
| Product canonical PNG                   | `ext-images/<slug>/source-of-truth/product-images/<Product>.png`                  |
| Product structured knowledge            | `ext-images/<slug>/structured-knowledge/`                                         |
| Product visual profile                  | `ext-images/<slug>/visual-system/references/<slug>-visual-profile.md`             |
| Product orchestration policy            | `ext-images/<slug>/automation/orchestrators/orchestration-manifest.json`          |
| Product lineage                         | `ext-images/<slug>/metadata/lineage/source-lineage.json`                          |
| Product-domain manifest                 | `ext-images/<slug>/metadata/manifests/product-domain-manifest.json`               |
| Product validation ledger               | `ext-images/<slug>/metadata/validation/validation-ledger.json`                    |
| ComfyUI workflows                       | `tools/comfy/` (registered, versioned, hashed)                                    |
| Shared terminology registry             | Shared registry under `User manuals/` (location to be ratified during migration)  |
| Shared product registry (slug → paths)  | Shared registry under `User manuals/` (location to be ratified during migration)  |
| Site delivery contract                  | `User manuals/manual-web-integration-manifest.json` (transitional; nucleus-only after migration) |

Rules:
- A read of a non-canonical location is allowed only if the non-canonical location is generated.
- A write to a non-canonical location is forbidden.
- Tooling that violates canonical-source rules is treated as a bug.

---

## 8. Transitional surfaces (to be retired)

The following surfaces exist today and must be retired after each product's nucleus is complete and all dependent tooling is switched:

- Product-specific files at `User manuals/` root.
- Product-specific files under `User manuals/assets/`.
- Product-specific files under `User manuals/visual-system/products/`.
- Product-specific OCR outputs in `generated_manuals/<slug>/` once promoted into the nucleus.
- Compatibility PNGs at `ext-images/` root once nucleus PNGs exist.
- Mixed-mode entries in `manual-web-integration-manifest.json` once the contract is rewritten to nucleus-only paths.
- Stale references in `User manuals/visual-system/production-control/global-image-registry.md` to nonexistent flat-path WebP anchors.

Retirement requires: complete lineage entries, migrated content, switched tooling, switched delivery contract. No partial retirements.
