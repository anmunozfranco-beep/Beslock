# Unresolved Runtime Risks

- **no-context-vector-emitter** — {"severity": "high", "summary": "context-acquisition stage cannot bind without an upstream emitter", "cross_ref": "adaptive + continuity"}
- **no-confidence-tier-on-nodes** — {"severity": "high", "summary": "uncertainty propagation, decision confidence, reasoning chains all depend on per-node confidence not yet emitted", "cross_ref": "knowledge-core/provenance"}
- **no-checkpoint-registry** — {"severity": "high", "summary": "interruption + recovery flows degrade to restart-from-safe-state", "cross_ref": "execution + continuity + decision"}
- **no-fallback-registry** — {"severity": "high", "summary": "alternative-path execution flows cannot resolve targets", "cross_ref": "adaptive + decision"}
- **no-incident-id-emitter** — {"severity": "high", "summary": "history queries and escalation packages cannot bind across sessions", "cross_ref": "continuity"}
- **no-provenance-emitter** — {"severity": "high", "summary": "runtime requires upstream provenance emission for replay determinism", "cross_ref": "execution/snapshot-hash + decision + reasoning + continuity"}
- **thin-troubleshooting-corpus** — {"severity": "high", "summary": "guidance-package for troubleshooting cannot be released on 5/6 products", "cross_ref": "validation/maturity"}
- **warning-corpus-gap** — {"severity": "high", "summary": "mandatory-warning surface cannot fire on 2 products at runtime", "cross_ref": "validation/warnings"}
- **oem-channel-contract-missing** — {"severity": "high", "summary": "tier-4/5 handoff cannot complete without OEM channel contract", "cross_ref": "decision/escalation + continuity/handoff"}
- **no-causal-edges-emitted** — {"severity": "medium", "summary": "reasoning-invocation flow degrades when causal edges are not addressable", "cross_ref": "reasoning/causality"}
- **no-hypothesis-store** — {"severity": "medium", "summary": "reasoning flow cannot persist hypotheses across resume", "cross_ref": "reasoning/hypothesis-tracking"}
- **schema-version-pinning-not-enforced** — {"severity": "medium", "summary": "runtime must pin schema versions; no upstream pin contract yet", "cross_ref": "this layer / contracts"}
