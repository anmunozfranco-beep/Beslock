# Feedback-Driven Corpus Evolution

Seven-step governed loop: runtime observation → aggregation → reviewer triage → candidate authoring → trust evaluation → promotion → runtime improvement.

## Loop

- step 1 — `runtime observation` (actor: runtime; produces: instrumented signal (TASK 2))
- step 2 — `aggregation` (actor: telemetry pipeline; produces: hotspot / friction / retrieval finding (TASKs 3-5))
- step 3 — `reviewer triage` (actor: reviewer-of-scope; produces: enrichment request OR closure with rationale)
- step 4 — `candidate authoring` (actor: knowledge operator; produces: candidate knowledge node (layer 23))
- step 5 — `trust evaluation` (actor: reviewer ecosystem; produces: promotion decision (single or dual review per scope))
- step 6 — `promotion` (actor: promotion workflow; produces: trusted corpus update)
- step 7 — `runtime improvement` (actor: runtime; produces: next-cycle observations (loop closes))

## Rules

- no step in this flow may be skipped
- no automation may compress steps 3 + 4 + 5 (the human-judgment band)
- every promotion carries provenance back to the originating signal cluster
- loop is observation-only on the first iteration of every new pilot product
- signal → corpus changes are governed; never inferred and applied silently
