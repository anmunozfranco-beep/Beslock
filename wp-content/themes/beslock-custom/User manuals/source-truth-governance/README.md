# Source-Truth Governance (Layer 32)

Multimodal evidence classification, ingestion contracts, trust model,
lineage, cross-modal grounding, lifecycle, and conflict governance.

Modeling-only. Knowledge-core, source-of-truth, and runtime are NEVER
mutated by this layer. No ML, no embeddings, no prompts, no images.

Subdirectories:

- `evidence-classification/` — canonical evidence classes
- `ingestion-contracts/` — per-format ingestion contracts
- `evidence-trust-model.json` — trust hierarchy
- `multimodal-lineage/` — five-track lineage + cross-modal references
- `cross-modal-grounding/` — non-ML grounding contracts
- `ingestion-lifecycle/` — lifecycle state machine
- `evidence-conflict-governance/` — conflict detection + resolution
- `future-multimodal-readiness.json` — downstream interface contract
