# Unresolved Decision Risks

- **thin-troubleshooting-corpus** — {"severity": "high", "summary": "branching/recommendations have limited eligible paths on 5/6 products", "cross_ref": "validation/maturity + execution + adaptive"}
- **no-confidence-tier-on-nodes** — {"severity": "high", "summary": "decision confidence is heuristic; per-node confidence not yet emitted by knowledge-core", "cross_ref": "knowledge-core/provenance + adaptive"}
- **no-fallback-registry** — {"severity": "high", "summary": "alternative-path-recommendation cannot resolve targets without registered fallbacks", "cross_ref": "adaptive/fallback"}
- **no-checkpoint-registry** — {"severity": "high", "summary": "cancel-vs-rollback decision degrades to cancel-no-state-change", "cross_ref": "execution/checkpoints"}
- **intent-clarity-detector-missing** — {"severity": "medium", "summary": "ask-disambiguation-vs-proceed is contractual; no live detector", "cross_ref": "adaptive/intent-clarity"}
- **context-vector-not-emitted** — {"severity": "medium", "summary": "decision determinism depends on a context-vector emitter not yet wired", "cross_ref": "adaptive/context-vector"}
- **shared-concepts-undeclared** — {"severity": "medium", "summary": "cross-product collisions cause ambiguous tie-breakers", "cross_ref": "validation/entity"}
- **oem-confirmation-channel-missing** — {"severity": "medium", "summary": "OEM-required resolutions cannot complete without an OEM channel contract", "cross_ref": "lifecycle/promotion-gates"}
- **decision-provenance-not-emitted** — {"severity": "medium", "summary": "auditable trail requires upstream emitter (modelled here, not implemented)", "cross_ref": "execution/snapshot-hash"}
