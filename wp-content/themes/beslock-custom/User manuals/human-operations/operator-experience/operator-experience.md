# Operator Experience Model

Six declared operator profiles + interaction principles for safe, supervised use.

## Operator profiles

- `runtime-operator` — surface: supervised flow CLI; decisions: approve, reject, demote
- `reviewer` — surface: reviewer-workbench panels; decisions: approve, reject, request-evidence, open-dispute
- `governance-maintainer` — surface: governance console; decisions: assign, revoke, scope-edit (within charter)
- `escalation-supervisor` — surface: escalation console; decisions: accept-handoff, route, halt-slice, request-dual-review
- `oem-reviewer` — surface: OEM evidence panel; decisions: bind-source, reject-source, supersede-source
- `operational-auditor` — surface: audit console (read-only); decisions: raise-finding, request-replay

## Interaction principles

- Every operator action emits a supervision-receipt; no silent action exists.
- Every operator surface declares its scope; out-of-scope actions are not exposed.
- Every operator decision is reversible by an equal-or-higher governance decision.
- Operators see provenance before they see conclusions.
- Operators see uncertainty before they see recommendations.
