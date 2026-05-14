# Ecosystem Self-Orientation

This document orients a new operator to the ecosystem in 60 seconds.

## Three immovable surfaces

1. `runtime-implementation/` — the Python runtime. Governance phases NEVER touch it.
2. `wp-content/themes/beslock-custom/User manuals/ext-images/<product>/source-of-truth/` — raw OEM/field artefacts. Read-only by every governance phase.
3. `wp-content/themes/beslock-custom/User manuals/ext-images/<product>/knowledge-core/` — canonical per-product semantic entries. Read-only by every governance phase except its own builder.

## Two write surfaces governance phases USE

1. `wp-content/themes/beslock-custom/User manuals/<governance-folder>/` — modeling output of each phase.
2. `wp-content/themes/beslock-custom/User manuals/_repository-governance/reports/<phase>/` — 10-section final reports per phase.

## When a new file lands

Open `source-of-truth-governance/governance/intake-routing/intake-pipeline.json` and walk the 10 steps.
Use `routing-examples/` for concrete precedents. If anything is ambiguous, invoke `intake-consultation/`.

## When a publication needs to change

Do NOT edit `publication-system/generated-publications/` by hand. Edit knowledge-core (with reviewer
lineage) and re-run `tools/publication_renderer.py`.

## When a warning needs to change

Warnings live in knowledge-core. Severity, irreversibility, escalation flags are immutable at
publication-render time per linguistic-governance (layer 31) + warning-fidelity doctrine.
