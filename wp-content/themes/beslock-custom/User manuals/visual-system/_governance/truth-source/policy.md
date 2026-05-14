# Truth-source PNG policy

_Schema: `visual-governance/1.0` · canonical policy · generated 2026-05-13T16:14:38Z._

## Intent

The single canonical PNG at `ext-images/<slug>/source-of-truth/product-images/<Product>.png` is the absolute visual source of truth. Every generated visual must extend / infer / contextualise / operationalise this PNG. Generation must NEVER redesign hardware, change geometry, invent components, relocate sensors, modify proportions or hallucinate mechanical systems.

## Authoritative source documents

This policy is a CONSOLIDATION POINTER. The rules themselves remain in the source documents listed below. Editing this policy does NOT edit the sources; conflicts are reported in `_repository-governance/reports/visual-governance/`.

- `KNOWLEDGE_BUILDING/PRODUCT_VISUAL_TRUTH.md`
- `KNOWLEDGE_BUILDING/PHASE_1_IMPLEMENTATION.md`
- `KNOWLEDGE_BUILDING/KNOWLEDGE_CORE_PRINCIPLES.md`
- `visual-system/shared/visual-rules/product-truth-policy.md`

## Fallback Surfaces Use Canonical Png

- hero / primary product imagery (web, PDF, support)
- catalog imagery used for purchase decisions
- specification-sheet imagery
- imagery cited as 'product image' in delivery contracts
- imagery rendered next to legal text, certifications, warranty
- imagery accompanying technical specifications
- onboarding imagery used for product identification

## Fallback Rule

If visual QA cannot certify a generated/composited output meets tolerance checks, the canonical PNG is used directly. There is no degraded-quality fallback chain.
