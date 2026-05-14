# Unresolved Adaptive Risks

- **thin-troubleshooting-corpus** — {"severity": "high", "summary": "symptom-first branching has limited eligible paths on 5/6 products", "cross_ref": "validation/maturity + execution/troubleshooting-readiness"}
- **warning-corpus-gap** — {"severity": "high", "summary": "escalation cannot fire 'mandatory-warning surface' on 2 products", "cross_ref": "validation/warnings + execution/safeguards"}
- **no-confidence-tier-on-nodes** — {"severity": "high", "summary": "confidence-aware guidance currently relies on heuristic mapping; per-node confidence not yet emitted by knowledge-core", "cross_ref": "knowledge-core/provenance"}
- **no-fallback-registry** — {"severity": "high", "summary": "degraded-mode substitution cannot resolve targets without a registered fallback list per procedure", "cross_ref": "execution/fallback + composition"}
- **context-vector-not-emitted** — {"severity": "medium", "summary": "context dimensions are modelled here but no upstream emitter populates them yet", "cross_ref": "future runtime contract"}
- **intent-clarity-detector-missing** — {"severity": "medium", "summary": "ambiguous-intent branch is contractual; no live detector", "cross_ref": "execution/intent-rules"}
- **skill-inference-undefined** — {"severity": "medium", "summary": "user-role assumed declared; inference path not modelled here by design", "cross_ref": "future product-surface contract"}
- **shared-concepts-undeclared** — {"severity": "medium", "summary": "cross-product collisions block uniform adaptation across the family", "cross_ref": "validation/entity"}
- **adaptation-precedence-conflicts** — {"severity": "low", "summary": "rare overlapping triggers may produce ambiguous order; precedence rules cover declared cases", "cross_ref": "this layer / precedence"}
