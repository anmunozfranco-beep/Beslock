# ARCHITECTURE MIGRATION MASTER PROMPT

Status: Active governance.
Owner: BESLOCK Product Knowledge Core.
Scope: Repository-wide migration from manual-centric organization to product knowledge nuclei.

---

## 1. Purpose

This document is the master architectural definition for migrating BESLOCK from a manual-centric repository (root-level PDFs, scattered `*-image-ready.md`, ad-hoc `assets/`, ad-hoc `visual-system/products/`, OCR dumps in `generated_manuals/`) into a product-nucleus architecture rooted at:

```
wp-content/themes/beslock-custom/User manuals/ext-images/<product-slug>/
```

Every other governance file in `KNOWLEDGE_BUILDING/` derives from this document.

---

## 2. Nucleus architecture

A product nucleus is the single canonical home for every product-specific artifact. Each nucleus owns six top-level responsibilities:

```
ext-images/<product-slug>/
├── source-of-truth/        # OEM originals + the single canonical PNG + raw evidence
├── structured-knowledge/   # Semantic JSON objects (capabilities, procedures, glossary, workflows, knowledge-graph)
├── visual-system/          # Visual profiles, anchor maps, prompt packs, QA trackers
├── publishing/             # Channel-ready delivery surfaces (web, PDF, support)
├── automation/             # Orchestration manifests, run records, workflow bindings
└── metadata/               # Lineage, provenance, product-domain manifest, validation ledgers
```

The reference implementation is `ext-images/e-orbit/`. All other products migrate toward that shape.

Rules:
- A product nucleus is self-contained. It must function without referencing any other product's files.
- A product nucleus is the only place that may declare canonical product truth.
- Nothing outside `ext-images/<slug>/` is permitted to redefine that product's identity, geometry, procedures, capabilities, or visual constraints.

---

## 3. ext-images philosophy

`ext-images/` is not an image folder. It is the multimodal knowledge root.

- It holds product nuclei, not loose images.
- The name is historical; the directory's role is **product knowledge core**, covering text, structured knowledge, visual evidence, automation manifests, and provenance.
- Loose PNGs at the root of `ext-images/` (e.g. `e-Flex.png`, `e-Nova.png`) are compatibility-only and must be retired once each product's nucleus owns its canonical PNG under `source-of-truth/product-images/`.

---

## 4. Product isolation rules

- One product, one nucleus. No shared product folders.
- No product nucleus may import, reference, or depend on another product's files.
- Cross-product comparison data lives in shared registries (see `REPOSITORY_BOUNDARIES.md`), not inside any single nucleus.
- A change to one product must not require editing another product's files.
- Tooling must resolve product paths through manifests, not through hardcoded sibling-product assumptions.

---

## 5. Shared vs product separation

Product-specific (must live inside the nucleus):
- OEM source documents.
- The canonical product PNG.
- Normalized source manuals.
- Visual profiles, anchor maps, prompt packs.
- Structured knowledge objects.
- QA trackers and validation ledgers.
- Publishing outputs for that product.
- Lineage and orchestration manifests for that product.

Shared (may live outside nuclei):
- Shared terminology registry.
- Shared editorial rules.
- Shared visual rules.
- Shared prompt components.
- Shared ComfyUI workflow registry.
- Shared production dashboards.
- Repository tooling under `tools/` and root scripts (`process_manuals.py`, `visual_generation.py`).

Forbidden in shared scope:
- Any product-specific text, image, prompt, or manifest.
- Any "shared" file that is actually only used by one product.

---

## 6. Repository restructuring goals

End-state targets:
1. Every product has exactly one nucleus, with the six required top-level folders.
2. No product-specific content remains in:
   - `wp-content/themes/beslock-custom/User manuals/` root,
   - `wp-content/themes/beslock-custom/User manuals/assets/`,
   - `wp-content/themes/beslock-custom/User manuals/visual-system/products/`,
   - `generated_manuals/<slug>/` once Phase 1 outputs have been promoted into the nucleus.
3. The site-level delivery contract (`manual-web-integration-manifest.json`, `manual-web-integration-matrix.md`) resolves every product through its nucleus, never through legacy flat paths.
4. Compatibility PNGs at the `ext-images/` root are removed.
5. Every tool resolves product paths via a shared product registry plus per-product manifests, with no hardcoded slug-to-path assumptions.

Migration is sequenced per product. e-Orbit is the reference. Other products migrate one at a time, completing Phase 1 and Phase 2 before Phase 3 cutover.

---

## 7. Provenance requirements

Every artifact inside a nucleus must declare where it came from.

- File-level: every normalized or derived file must trace to an OEM source or the canonical PNG.
- Semantic-level: every structured-knowledge claim must carry `source_refs` to a normalized source-of-truth file or an explicit validation flag.
- Visual-level: every approved support visual must declare the canonical PNG, the workflow registry entry, the workflow hash, the seed, and the parameters that produced it.

No artifact may be promoted into the nucleus without provenance. "Unknown source" is a blocking state, not a passive default.

---

## 8. Lineage requirements

Lineage is recorded at three levels and persisted per nucleus in `metadata/lineage/source-lineage.json`:

- **File lineage**: source file → normalized file → structured file → delivery file.
- **Semantic lineage**: source section → semantic object → delivery slice.
- **Visual lineage**: canonical PNG or OEM diagram → conditioning asset → workflow run → approved support visual.

Rules:
- OEM originals and normalized derivatives must both be recorded, but only one of them is the active truth at any given level.
- Historical artifacts may be retained only when they add traceability and are explicitly marked historical-only.
- Lineage must be present before any legacy file is removed.

---

## 9. Multimodal knowledge strategy

The product nucleus is multimodal by design:

- **Text knowledge**: normalized manuals, structured-knowledge JSON, glossary, validation ledger.
- **Visual knowledge**: canonical PNG, OEM visual evidence, anchor maps, conditioning assets, approved support visuals.
- **Procedural knowledge**: capabilities, procedures, workflows, troubleshooting, warnings.
- **Operational knowledge**: orchestration manifests, run records, QA trackers.
- **Relational knowledge**: knowledge-graph edges between capabilities, components, procedures, and visual constraints.

All modalities share the same identity: the product slug, the canonical PNG, and the OEM evidence set. No modality is allowed to redefine the product on its own. Generated visuals never become product truth; they are downstream derivatives.

---

## 10. Authority

This master prompt overrides any conflicting guidance in legacy summaries (`HEADER_*`, `PRODUCT_CARD_*`, `LEGACY_RUNTIME_AUDIT_SUMMARY.md`, etc.) for matters of product knowledge architecture. Legacy summaries remain valid only for the runtime/frontend concerns they originally addressed.
