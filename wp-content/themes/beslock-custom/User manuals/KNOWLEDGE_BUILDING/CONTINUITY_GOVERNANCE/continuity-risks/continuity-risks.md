# Unresolved Continuity Risks

- **no-context-store** — {"severity": "high", "summary": "context schema modelled here; no persistent store contract yet (by design — modeling-only)", "cross_ref": "future runtime contract"}
- **no-checkpoint-registry** — {"severity": "high", "summary": "interruption-continuity cannot resolve checkpoint anchors per procedure", "cross_ref": "execution/checkpoints + decision/cancel-vs-rollback"}
- **no-incident-id-emitter** — {"severity": "high", "summary": "history queries and inheritance bind to incident-id; no upstream emitter", "cross_ref": "future runtime contract"}
- **no-confidence-tier-on-nodes** — {"severity": "high", "summary": "inheritance and history rules depend on per-node confidence not yet emitted", "cross_ref": "knowledge-core/provenance"}
- **no-session-signal-emitter** — {"severity": "medium", "summary": "session-aware adaptations are contractual; signals not yet emitted", "cross_ref": "this layer / future emitter"}
- **no-escalation-package-emitter** — {"severity": "medium", "summary": "escalation packages are specified; no emitter wired", "cross_ref": "decision/escalation + execution"}
- **concurrent-timeline-linkage-undeclared** — {"severity": "medium", "summary": "concurrent timelines (e.g., troubleshooting during onboarding) need explicit linkage emitter", "cross_ref": "this layer / timeline rules"}
- **shared-concepts-undeclared** — {"severity": "medium", "summary": "cross-product collisions complicate context-product binding for shared accounts", "cross_ref": "validation/entity"}
- **intent-clarity-detector-missing** — {"severity": "medium", "summary": "incomplete-onboarding-flag relies on intent declarations not yet wired", "cross_ref": "adaptive/intent-clarity + decision"}
