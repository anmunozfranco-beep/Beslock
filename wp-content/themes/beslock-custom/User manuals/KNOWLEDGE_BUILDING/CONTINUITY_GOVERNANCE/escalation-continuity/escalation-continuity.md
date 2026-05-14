# Continuity-Safe Escalation

## Escalation Package Fields

- incident-id
- product-id + serial-or-identifier (when declared)
- current operational-state-vector
- active timeline + last completed stage
- decision-trace-ref
- reasoning-chain-ref
- open hypotheses + lifecycle-state
- open warnings + acknowledgement state
- history references (failed paths, attempted recoveries)
- confidence summary (tier counts)
- OEM-required flags
- provenance bundle

## Rules

- escalation never strips context; it summarizes with provenance
- escalation packages are read-only snapshots; receivers cannot mutate the originating context
- OEM handoff requires a complete escalation package including OEM-required flags
- support handoff preserves the incident-id; child sessions inherit by reference
- unresolved-history must be propagated, never silently closed
- escalation package generation is deterministic from declared inputs

## Handoff Kinds

- **tier-2-handoff** — {"audience": "advanced/installer/administrator"}
- **tier-3-handoff** — {"audience": "vendor/dealer support"}
- **tier-4-handoff** — {"audience": "OEM technical support"}
- **tier-5-handoff** — {"audience": "OEM RMA / replacement"}
