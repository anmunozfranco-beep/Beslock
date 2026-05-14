# Runtime Consistency Validation

Validates that the executable runtime is consistent with declared governance; carry-over gaps are catalogued, not introduced.

## Findings

- `retrieval-uses-confidence-weights` — consistent: retrieval.py applies CONFIDENCE_WEIGHTS declared in config.py; weights match RUNTIME_HARDENING_GOVERNANCE schema
- `candidate-only-marker-flows-end-to-end` — consistent: retrieval sets manifest.extra.candidate_only; assembly._evaluate_escalation reads it; ESCALATION emits trigger
- `replay-skips-empty-packages` — consistent: replay.py skips manifest.extra.empty=True; tests pass 19/19
- `observability-channels-bounded` — consistent: channels.py allows only declared channel names; orchestration/retrieval/escalation/continuity/replay/operational-audit-log
- `supervision-receipt-not-yet-runtime-field` — gap (declared, not enforced): HUMAN_OPERATIONS_GOVERNANCE declares supervision-receipt; runtime CLI does not yet emit one as a separate field; flows.operator is a free string (carry-over: phase 30)
- `composition-manifest-not-yet-emitted` — gap (declared, not enforced): REFERENCE_STACK_GOVERNANCE declares composition-manifest at startup; runtime does not yet emit it (carry-over: phase 32)
- `interop-contract-registry-absent` — gap (declared, not enforced): REFERENCE_STACK_GOVERNANCE declares contract registry; absent in code (carry-over: phase 32)
- `incident-trace-channel-not-provisioned` — gap (declared, not enforced): ENVIRONMENT_AND_INTEGRATION_GOVERNANCE declares incident-trace; channels.py has no `incident-trace` entry (carry-over: phase 31)
- `no-divergent-runtime-assumptions-detected` — consistent: all runtime modules subscribe to a single config.ALLOWED_DOMAINS + a single CONFIDENCE_WEIGHTS dict; no module redefines either
- `no-replay-incompatibilities-detected` — consistent: replay re-executes against captured (product, query, kind); deterministic; tests pass

## Consistency rules

- every runtime module uses canonical terms only (TASK 5)
- every runtime module reads ALLOWED_DOMAINS and CONFIDENCE_WEIGHTS from a single config source
- every runtime module emits to declared channels only
- every runtime gap above is recorded as a carry-over; no new gaps are introduced
- every runtime change is preceded by a governance action documented in this layer's canonical-references
