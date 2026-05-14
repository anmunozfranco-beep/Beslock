# ext-images

## Purpose
`ext-images/` is now the multimodal product knowledge root for BESLOCK.

This directory is no longer a flat image repository. It is the product-domain base for:
- verified source-of-truth assets
- structured product knowledge
- deterministic visual-generation inputs
- publishing outputs
- automation orchestration
- metadata lineage and traceability

## Active migration state
`e-orbit/` is the first migrated product domain and is now the canonical e-Orbit root.

Its product-domain structure is organized around:
- `source-of-truth/`
- `structured-knowledge/`
- `visual-system/`
- `publishing/`
- `automation/`
- `metadata/`

Shared cross-product surfaces now live under `shared/`.

The remaining flat root PNG files are temporary compatibility surfaces for products that have not yet been migrated into their own domains.

## Canonical rule
For a migrated product, the canonical product reference must live inside that product domain under `source-of-truth/product-images/`.

For e-Orbit, the canonical transparent cutout is now:
- `e-orbit/source-of-truth/product-images/e-Orbit.png`

## Visual generation rule
All future image generation must route through ComfyUI workflows. Prompt packs, masks, conditioning assets, validations, and outputs inside a product domain must remain traceable back to the product, slot, workflow, prompt, and source references.

## Non-goals
Do not use this directory for decorative moodboards, generic inspiration, or unverified AI reinterpretations of hardware.
