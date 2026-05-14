# Vertical Slice Identification

## Candidates

- **onboarding-guidance** — {"value": "high", "risk": "medium", "destructive_surface": "low (no factory-reset / firmware ops)", "evidence_readiness": "medium (onboarding procedures present across 6/6 products)", "predicate_coverage": "partial (pairing/enrollment predicates declared)", "preferred_score": 8, "rationale": "high user value, mostly non-destructive, predicates partially declared, fallback registry not strictly required"}
- **procedural-retrieval** — {"value": "high", "risk": "low", "destructive_surface": "none (read-only)", "evidence_readiness": "high (knowledge-core nodes addressable)", "predicate_coverage": "n/a (no execution)", "preferred_score": 9, "rationale": "safest first runtime; pure read; activates ACCESS_AND_CONSUMPTION + COMPOSITION contracts without execution risk"}
- **contextual-operational-assembly** — {"value": "high", "risk": "low", "destructive_surface": "none (assembly only)", "evidence_readiness": "high", "predicate_coverage": "n/a (no execution)", "preferred_score": 8, "rationale": "exercises COMPOSITION + ADAPTIVE precedence without crossing execution boundaries"}
- **troubleshooting-guidance** — {"value": "high", "risk": "high", "destructive_surface": "medium (may surface escalation paths)", "evidence_readiness": "low (thin troubleshooting corpus on 5/6 products)", "predicate_coverage": "low", "preferred_score": 4, "rationale": "blocked by thin-troubleshooting-corpus + missing causal edges + missing checkpoint registry"}
- **administrator-assistance** — {"value": "medium", "risk": "high", "destructive_surface": "high (admin actions, factory-reset, delete-users)", "evidence_readiness": "medium", "predicate_coverage": "partial (factory-reset predicate declared)", "preferred_score": 3, "rationale": "destructive surface; require OEM channel + role-declaration + checkpoint registry before runtime"}
- **recovery-assistance** — {"value": "medium", "risk": "high", "destructive_surface": "medium", "evidence_readiness": "low", "predicate_coverage": "low", "preferred_score": 3, "rationale": "blocked by no-checkpoint-registry + no-causal-edges; cannot anchor recovery deterministically"}

## Selection

- primary first slice: procedural-retrieval (read-only, lowest risk, exercises ACCESS_AND_CONSUMPTION + COMPOSITION contracts)
- secondary second slice: contextual-operational-assembly (still non-executive; exercises ADAPTIVE precedence and COMPOSITION rules)
- third slice (gated): onboarding-guidance, only after checkpoint registry + intent-declaration channel are wired
- deferred: troubleshooting-guidance, administrator-assistance, recovery-assistance (blocked by declared high-severity risks)

## Rules

- no slice is realized while any of its declared blocking-risks remains unresolved
- each slice declares: scope, evidence readiness, predicate coverage, destructive surface, blocking risks, exit criteria
- no slice may extend its surface at runtime; surface is declared at packaging time
- slices are read-only by default; any executive behaviour requires an explicit, governed extension
