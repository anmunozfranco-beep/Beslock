# Beslock Visual System

## Purpose
This directory operationalizes the existing visual-planning documents into a stable technical visual reconstruction system.

The goal is not to replace the current documentation stack overnight. The goal is to add the missing operational layers needed to produce, review, track, and gradually replace documentation imagery while preserving product truth.

## System definition
This is a technical visual reconstruction pipeline.

It exists to:
- reconstruct missing instructional imagery
- preserve product geometry from minimal reference material
- support documentation clarity over aesthetics
- keep prompt logic modular and maintainable
- track production status with deterministic filenames and review gates

It is not a generic AI art workflow.

## Compatibility contract
During this upgrade, the current flat files at the root of User manuals remain valid.

Examples:
- `<Product> - AI image prompts.md`
- `<Product> - image generation matrix.md`
- `<Product> - implementation starter pack.md`
- `e-Orbit user manual - image-ready.md`

The new directory structure sits above those files as the operational control layer.

## Canonical inputs
- `../ext-images/*.webp`: current visual truth layer with one canonical product reference image per product
- `../generated_manuals/`: OCR and extraction outputs
- `../*.pdf`: OEM source manuals
- `products/<slug>/image-production-status.md`: execution state by image slot
- `shared/`: reusable prompt modules, rules, and review guides

## Operating model
1. Start from the product visual profile in `../ext-images/<slug>/`.
2. Classify the target image as realistic, semi-realistic, schematic, or hybrid.
3. Assemble the prompt from shared modules plus the product profile.
4. Generate variants and review against the visual-validation checklist.
5. Track the selected state in `products/<slug>/image-production-status.md`.
6. Publish only after the asset passes product-truth and documentation-clarity review.

## Directory map
```text
visual-system/
├── shared/
├── products/
└── production-control/
```

## Migration rule
Prefer adding new work here.
Do not duplicate or rewrite mature legacy docs unless the new file becomes the explicit canonical replacement.
