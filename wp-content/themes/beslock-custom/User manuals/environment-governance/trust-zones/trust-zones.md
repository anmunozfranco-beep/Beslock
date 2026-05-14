# Infrastructure Trust Zones

Six declared trust zones, including a categorically prohibited zone.

## Zones

- `trusted-operational-zone` — highest trust; reads are unrestricted; writes require governance pipeline auth
- `semi-trusted-ingestion-zone` — may read trusted-zone provenance; may write only to staging
- `reviewer-controlled-zone` — reviewer-bounded; may stage decisions; may not directly mutate production
- `escalation-zone` — append-only; isolated from new emissions until decision
- `quarantined-runtime-zone` — no emission; read-only access to provenance; awaits operator decision
- `prohibited-operational-zone` — categorically forbidden; integration with these zones is a governance violation

## Invariants

- every artifact, sandbox, and integration is mapped to exactly one trust zone
- no zone may inherit privileges from another; trust is declared per-zone
- no prohibited zone is ever introduced as a 'temporary' integration
- zone changes are governance actions; they are dual-audited
- every zone has a declared revocation path
