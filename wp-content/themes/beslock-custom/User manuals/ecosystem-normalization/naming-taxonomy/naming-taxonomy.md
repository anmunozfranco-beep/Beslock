# Naming & Taxonomy Stabilization

Canonical terms with single definitions; deprecated aliases listed; future drift forbidden.

## Canonical terms

- `package` — an emitted runtime artifact bundling retrieved nodes + manifest; deprecated aliases: bundle, envelope
- `manifest` — an append-only declarative record describing a package, deployment, environment, composition, or governance event
- `node` — a single knowledge-core JSON record retrieved by the runtime
- `candidate` — a node at the lowest trust tier; never used in irreversible-adjacent contexts without escalation
- `supervision-receipt` — the append-only record bound to every operator action proving supervision occurred (owner: HUMAN_OPERATIONS_GOVERNANCE)
- `checkpoint` — a declared decision boundary in an executable workflow
- `trust-zone` — a declared infrastructure region with a fixed trust tier (owner: ENVIRONMENT_AND_INTEGRATION_GOVERNANCE)
- `trust-tier` — a declared confidence weighting applied to a node (verified-oem, verified-internal, high, ocr-derived, medium, inferred-operational, low, candidate, unresolved, unknown) (owner: RUNTIME_HARDENING_GOVERNANCE)
- `slice` — a bounded executable runtime composition (product × kinds × halt conditions) (owner: REFERENCE_STACK_GOVERNANCE)
- `composition` — a declared assembly of canonical-stack modules for a specific environment
- `operator` — a human acting under a declared profile (runtime/reviewer/governance/escalation/oem/auditor)
- `channel` — an append-only NDJSON event stream emitted by the observability system

## Prohibitions

- no synonym proliferation (one term, one meaning)
- no abbreviation of canonical terms in schemas or doctrine
- no informal aliases inside builder code or doctrine prose
- no reuse of a canonical term with a different meaning in any layer
- no introduction of new canonical terms without a doctrine entry
