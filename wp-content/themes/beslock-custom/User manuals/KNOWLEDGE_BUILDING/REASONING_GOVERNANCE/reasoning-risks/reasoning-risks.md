# Unresolved Reasoning Risks

- **thin-troubleshooting-corpus** — {"severity": "high", "summary": "abductive/troubleshooting chains have insufficient declared alternatives on 5/6 products", "cross_ref": "validation/maturity + decision + adaptive"}
- **no-confidence-tier-on-nodes** — {"severity": "high", "summary": "uncertainty propagation is heuristic without per-node confidence", "cross_ref": "knowledge-core/provenance"}
- **no-checkpoint-registry** — {"severity": "high", "summary": "recovery-reasoning lacks anchors; refined hypotheses cannot bind to a known good state", "cross_ref": "execution/checkpoints"}
- **no-causal-edges-emitted** — {"severity": "high", "summary": "causal relations are modelled here but not emitted as edges in knowledge-core", "cross_ref": "knowledge-core/graph"}
- **predicate-coverage-incomplete** — {"severity": "medium", "summary": "validation predicates exist for 5 procedure classes; chain confirmation is otherwise inferred", "cross_ref": "execution/validation-predicates"}
- **intent-clarity-detector-missing** — {"severity": "medium", "summary": "intent-conflict detection is contractual; no live detector", "cross_ref": "adaptive/intent-clarity + decision"}
- **context-vector-not-emitted** — {"severity": "medium", "summary": "state-dependent reasoning depends on a context-vector emitter not yet wired", "cross_ref": "adaptive/context-vector"}
- **shared-concepts-undeclared** — {"severity": "medium", "summary": "cross-product collisions create authority-conflict ambiguity", "cross_ref": "validation/entity"}
- **hypothesis-store-not-emitted** — {"severity": "medium", "summary": "hypothesis lifecycle is modelled here; no upstream store yet", "cross_ref": "this layer / future store contract"}
- **reasoning-provenance-not-emitted** — {"severity": "medium", "summary": "auditable trail requires upstream emitter", "cross_ref": "execution/snapshot-hash + decision/provenance"}
