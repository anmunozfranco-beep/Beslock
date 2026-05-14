# Governed Manual Assembly Flow

Six-step governed flow: knowledge-core → contextual assembly → publication rendering → reviewer validation → publication promotion → runtime-consumable outputs.

## Flow

- step 1 — `knowledge-core` (actor: knowledge-core/1.0; produces: selected source nodes per manifest)
- step 2 — `contextual-assembly` (actor: assembly pipeline (TASK 2); produces: structured-runtime publication candidate)
- step 3 — `publication-rendering` (actor: renderer per format (TASK 4); produces: format-specific outputs (markdown, web, pdf-ready, support-article, visual-prompt))
- step 4 — `reviewer-validation` (actor: reviewer-of-scope (layer 23); produces: validation decision + attribution)
- step 5 — `publication-promotion` (actor: promotion workflow; produces: versioned publication artifact)
- step 6 — `runtime-consumable-output` (actor: RUNTIME_IMPLEMENTATION; produces: assembled response with embedded provenance + confidence)

## Manual assembly rules

- no step in this flow may be skipped
- no automation compresses steps 4 + 5 (reviewer judgment + promotion)
- publication promotion is a distinct act from candidate promotion (layer 23)
- runtime-consumable outputs MUST cite the publication version they were derived from
- first publication of any new manual is observation-only against pilots (layer 28) before broad delivery
