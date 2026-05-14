# PRODUCT NUCLEUS RULES

Status: Active governance.
Scope: Rules that every product nucleus under `ext-images/<slug>/` must obey.
Reference implementation: `ext-images/e-orbit/`.

---

## 1. Mandatory folder structure

Every product nucleus must contain exactly these six top-level folders:

```
ext-images/<product-slug>/
├── source-of-truth/
│   ├── manuals/                       # Normalized OEM manuals + retained originals
│   ├── specifications/                # Technical evidence (normalized + originals)
│   ├── product-images/
│   │   └── <Product>.png              # The single canonical PNG
│   └── visual-evidence/               # OEM diagrams, UI snippets, icons, installation cues
├── structured-knowledge/
│   ├── manual.json                    # Normalized manual structure
│   ├── features/
│   │   └── capabilities.json
│   ├── procedures/
│   │   └── procedure-catalog.json
│   ├── glossary.json
│   ├── workflows.json
│   └── semantic-relations/
│       └── knowledge-graph.json
├── visual-system/
│   ├── references/
│   │   └── <slug>-visual-profile.md
│   ├── anchors/                       # Geometry/anchor maps derived from canonical PNG
│   ├── prompts/                       # Product-local prompt packs
│   ├── conditioning/                  # ControlNet/IPAdapter inputs derived from canonical PNG
│   └── qa/                            # Visual QA trackers and selected-asset registers
├── publishing/
│   ├── web/                           # Web-ready surfaces
│   ├── pdf/                           # PDF-ready surfaces
│   └── support/                       # Support-system surfaces
├── automation/
│   ├── orchestrators/
│   │   └── orchestration-manifest.json
│   └── runs/                          # Run records, workflow bindings
└── metadata/
    ├── lineage/
    │   └── source-lineage.json
    ├── manifests/
    │   └── product-domain-manifest.json
    └── validation/
        └── validation-ledger.json
```

A nucleus that lacks any of the six top-level folders is non-conforming. A folder may be empty during early Phase 1, but it must exist with a placeholder README explaining why.

---

## 2. Self-contained domain rules

A nucleus must function in isolation:
- All product-specific truth, knowledge, visuals, and manifests live inside it.
- Nothing inside the nucleus may resolve a path that points into another product's nucleus.
- Tooling must be able to operate on a single nucleus without loading another product's files.
- Removing all other nuclei from the repository must not break the nucleus's internal references.

A nucleus may reference shared registries (terminology, workflow registry, product registry) but never another product's nucleus.

---

## 3. Product isolation principles

- One product, one nucleus.
- A nucleus's slug is its identity. Slugs are lowercase, kebab-case, and stable across the repository.
- Product identity (capabilities, geometry, procedures, visuals) is declared exclusively inside the nucleus.
- A change to one product's truth must not require editing another product's files.
- A bug or stale entry in one nucleus must not propagate to another nucleus.

---

## 4. Allowed shared assets

The following may live outside any single nucleus and be referenced by all of them:
- Shared terminology registry.
- Shared editorial rules.
- Shared visual rules and shared prompt components (snippets only, not product-specific prompts).
- Shared ComfyUI workflow registry under `tools/comfy/`.
- Shared product registry mapping slugs to nucleus paths.
- Shared production dashboards.
- Repository tooling under `tools/` and root scripts (`process_manuals.py`, `visual_generation.py`).

A shared asset must be used by at least two products. A "shared" asset used by only one product must be moved into that product's nucleus.

---

## 5. Forbidden cross-product contamination

The following are forbidden:
- Importing another product's PNG, manual, structured-knowledge file, or prompt.
- Defining another product's geometry, sensor layout, or UI inside this nucleus.
- Generating support visuals for product A using product B's canonical PNG as conditioning.
- Sharing run records, validation ledgers, or lineage entries across products.
- Bundling multiple products in a single delivery surface stored inside one product's `publishing/`.
- Hardcoded fallbacks of the form "if product A is missing, use product B".

Cross-product comparison data (e.g. capability matrices) belongs in shared registries, not inside any single nucleus.

---

## 6. Provenance requirements

Every artifact promoted into the nucleus must declare its origin.

- Every file in `structured-knowledge/` carries `source_refs` to files in `source-of-truth/` or an explicit validation flag.
- Every visual derivative in `visual-system/` carries a reference to the canonical PNG and to any OEM visual evidence used.
- Every approved support visual under `publishing/` or `visual-system/qa/` carries the workflow registry entry, workflow hash, seed, parameters, and approval state.
- Every entry in `metadata/lineage/source-lineage.json` records: source file, normalized derivative, structured derivative (if any), delivery file (if any).

"Unknown source" is a blocking condition. It does not pass silently.

---

## 7. Asset ownership rules

Ownership matrix:

| Asset class                          | Owner location                                                   |
|--------------------------------------|------------------------------------------------------------------|
| OEM source documents                 | `source-of-truth/manuals/` or `source-of-truth/specifications/`  |
| Canonical PNG                        | `source-of-truth/product-images/<Product>.png`                   |
| OEM visual evidence                  | `source-of-truth/visual-evidence/`                               |
| Structured knowledge JSON            | `structured-knowledge/`                                          |
| Visual profile and anchor maps       | `visual-system/references/`, `visual-system/anchors/`            |
| Prompt packs (product-specific)      | `visual-system/prompts/`                                         |
| Conditioning assets                  | `visual-system/conditioning/`                                    |
| QA trackers, selected-asset register | `visual-system/qa/`                                              |
| Orchestration manifest               | `automation/orchestrators/orchestration-manifest.json`           |
| Run records                          | `automation/runs/`                                               |
| Lineage manifest                     | `metadata/lineage/source-lineage.json`                           |
| Product-domain manifest              | `metadata/manifests/product-domain-manifest.json`                |
| Validation ledger                    | `metadata/validation/validation-ledger.json`                     |
| Channel-ready delivery surfaces      | `publishing/<channel>/`                                          |

Rules:
- An asset has exactly one owner location.
- Duplicates between root locations and the nucleus are forbidden after migration is complete.
- Generated support visuals are owned by `publishing/` or `visual-system/qa/`, never by `source-of-truth/`.

---

## 8. Conformance checklist

A nucleus is conforming when:
1. All six top-level folders exist.
2. The canonical PNG exists at the prescribed path.
3. `metadata/lineage/source-lineage.json` exists and validates.
4. `metadata/manifests/product-domain-manifest.json` exists and lists approved sources.
5. `metadata/validation/validation-ledger.json` exists, even if empty.
6. No file inside the nucleus references another product's nucleus.
7. No product-specific copy of this product's content exists outside the nucleus.

A nucleus that fails any check is non-conforming and must not be cited as a delivery source.
