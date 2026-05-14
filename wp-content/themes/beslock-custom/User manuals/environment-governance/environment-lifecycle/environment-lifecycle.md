# Environment Lifecycle Governance

Seven lifecycle states + nine declared transitions; every transition is a governance action.

## States

- `proposed` — declared but not provisioned
- `provisioned` — infrastructure declared; not yet receiving traffic
- `active` — receiving traffic under declared supervision level
- `under-review` — active with elevated audit; promotion or demotion pending
- `deprecated` — frozen at last state; reads only; no new writes
- `quarantined` — isolated due to safety event; no traffic; replay-only access
- `retired` — tombstoned; provenance retained; no infra; no surfaces

## Transitions

- `proposed` → `provisioned` — actor: governance-maintainer; requires: charter approval + trust-zone assignment
- `provisioned` → `active` — actor: governance-maintainer; requires: promotion gates from layer 22 satisfied
- `active` → `under-review` — actor: operational-auditor; requires: raised finding or health indicator threshold
- `under-review` → `active` — actor: governance-maintainer + auditor co-sign; requires: finding closed; no open critical health indicators
- `under-review` → `quarantined` — actor: escalation-supervisor; requires: safety event or replay drift > floor
- `active` → `deprecated` — actor: governance-maintainer; requires: successor environment in active state
- `deprecated` → `retired` — actor: governance-maintainer + auditor co-sign; requires: no open references; provenance archived
- `quarantined` → `active` — actor: governance-maintainer + auditor co-sign; requires: incident closed; replay deterministic; rollback verified
- `quarantined` → `retired` — actor: governance-maintainer + auditor co-sign; requires: incident review complete; environment unrecoverable

## Invariants

- every transition is a governance action with a declared actor and rationale
- no environment may be silently retired; deprecation precedes retirement
- no quarantined environment may resume active state without auditor co-signature
- every transition emits an environment-lifecycle-trace event
- tombstones are immutable; retired environments are never re-activated under the same id
