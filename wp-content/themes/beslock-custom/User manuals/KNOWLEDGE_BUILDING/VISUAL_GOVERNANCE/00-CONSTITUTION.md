# Beslock Visual Constitution

_Schema: `visual-constitution/1.0` · master constitutional document · generated 2026-05-13T16:25:41Z._

## Mission

The Beslock visual system exists to produce **deterministic, instructional, mechanically consistent visualisations of real Beslock products** so that customers, installers, support agents, and automated assistants can answer concrete operational questions without ambiguity. The visual system is part of the product knowledge layer, not a marketing surface.

## Absolute principle

> **Maximum operational clarity.** Not marketing aesthetics. Not cinematic storytelling. Not decorative AI art.

Every doctrine in this constitution descends from this principle.

## Architectural pillars

1. **Truth-source primacy.** A single canonical PNG per product is the absolute visual ground truth. All other visuals extend, infer, contextualise or operationalise that PNG; they never redesign it.
2. **Mechanical consistency.** Each product preserves the same hardware identity across every visual that depicts it: silhouette, sensor positions, keypad grid, handle geometry, latch/deadbolt structure, mounting layout, materials.
3. **Hands-only human policy.** No faces, no bodies, no lifestyle. Hands appear only as instructional silhouettes when a procedure literally requires touch context.
4. **Schematic / hybrid only.** Cinematic, marketing, photoreal-human and decorative styles are forbidden. Schematic and hybrid technical illustration are the only sanctioned modes for new work.
5. **Comfy-native rendering.** ComfyUI is the sole approved rendering runtime. Every approved visual is produced through a registered, hashed, reviewer-approved workflow conditioned on the canonical PNG.
6. **Semantic orchestration.** Generation is driven by the semantic layer (visual-intent, component-visibility, procedural-semantics, visual-risk, publication-intent) — not by free prompting.
7. **Provenance-bound lineage.** Every approved visual has an immutable run record linking it to a canonical PNG, a workflow version, conditioning inputs, and an approver. No run record means not approved.
8. **Validation-first promotion.** A visual is not in a product nucleus until it passes the manual review checklist, the per-product validation passes, and (when implemented) the automated tolerance gates.
9. **Risk-tiered rigour.** Visuals that affect installation, operation, troubleshooting, pairing, safety or locking behaviour carry the strictest constraints, the lowest inference tolerance, and the highest validation bar.
10. **Single canonical governance.** This document is the platform's visual constitution. The runtime authority is `visual-system/_governance/`. There are no parallel standards.

## Governance hierarchy

| Level | Layer | Location | Role |
|---:|---|---|---|
| 1 | Canonical doctrine | `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` (this folder) | Constitutional / architectural / conceptual. Explains *why*. |
| 2 | Runtime governance | `visual-system/_governance/` | Operational, modular policies. Enforces *what* and *how*. |
| 3 | Per-product implementation | `ext-images/<slug>/visual-system/` and `ext-images/<slug>/knowledge-core/` | Local implementation: prompts, generation matrices, visual profiles, semantic intent / risk / publication maps. |
| 4 | Execution / orchestration | `tools/visual_generation.py`, `tools/comfy/`, `ext-images/<slug>/automation/` | The Comfy runtime, the orchestration manifests and the immutable run records. |

## Navigation

Doctrine documents (this folder):

- [`doctrine/01-purpose-and-philosophy.md`](doctrine/01-purpose-and-philosophy.md)
- [`doctrine/02-truth-source-doctrine.md`](doctrine/02-truth-source-doctrine.md)
- [`doctrine/03-mechanical-consistency-doctrine.md`](doctrine/03-mechanical-consistency-doctrine.md)
- [`doctrine/04-human-interaction-doctrine.md`](doctrine/04-human-interaction-doctrine.md)
- [`doctrine/05-rendering-style-doctrine.md`](doctrine/05-rendering-style-doctrine.md)
- [`doctrine/06-comfy-constitution.md`](doctrine/06-comfy-constitution.md)
- [`doctrine/07-semantic-orchestration-doctrine.md`](doctrine/07-semantic-orchestration-doctrine.md)
- [`doctrine/08-validation-philosophy.md`](doctrine/08-validation-philosophy.md)
- [`doctrine/09-visual-risk-philosophy.md`](doctrine/09-visual-risk-philosophy.md)
- [`doctrine/10-publication-philosophy.md`](doctrine/10-publication-philosophy.md)
- [`doctrine/11-lineage-and-provenance-doctrine.md`](doctrine/11-lineage-and-provenance-doctrine.md)

Hierarchy and runtime linkage:

- [`hierarchy/governance-hierarchy.md`](hierarchy/governance-hierarchy.md)
- [`hierarchy/runtime-linkage-map.json`](hierarchy/runtime-linkage-map.json)

Future extensibility:

- [`extensibility/future-extensibility.md`](extensibility/future-extensibility.md)

## Hard guarantees of this promotion

- The runtime governance tree at `visual-system/_governance/` was not modified.
- Per-product prompts, generation matrices, visual profiles and semantic JSON were not modified.
- ComfyUI workflows under `tools/comfy/` were not modified.
- No image was generated by this phase.

## Amendment policy

Changing a doctrine requires updating this folder first, then propagating the change into `visual-system/_governance/<domain>/policy.md`. Direct edits to runtime governance that contradict the constitution are out of policy and must be reverted, then re-introduced through this folder.
