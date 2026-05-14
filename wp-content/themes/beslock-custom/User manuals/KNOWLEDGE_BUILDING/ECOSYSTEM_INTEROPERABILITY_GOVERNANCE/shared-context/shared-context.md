# Shared Operational Context

Declared shared-context kinds and inheritance rules across runtimes.

## Shared context kinds

- `shared-operational-memory` — scope: ecosystem-session — mutability: append-only
- `shared-troubleshooting-context` — scope: ecosystem-session + incident-id — mutability: append-only
- `cross-runtime-continuity` — scope: incident-id — mutability: append-only
- `shared-escalation-state` — scope: incident-id — mutability: monotonic (tier only rises)
- `context-inheritance-record` — scope: ecosystem-session — mutability: append-only; non-inheritable signals filtered
- `federated-operational-session` — scope: ecosystem-session — mutability: open/close lifecycle; no in-place edit
- `shared-skill-model` — scope: ecosystem-session — mutability: read-only inside a session
- `shared-confidence-tier` — scope: per-node — mutability: immutable across boundary

## Inheritable signals

- context-vector
- skill-model
- open-warnings (acknowledged or not)
- incident-id
- session-id
- active-package references (read-only)

## Non-inheritable signals

- destructive-confirmation
- irreversibility-acknowledgement
- explicit-action-receipt
- operator-identity (re-asserted per runtime)
- supervised-resume token

## Rules

- Shared context kinds are declared; ad-hoc shared state is forbidden.
- Shared context is append-only or monotonic; in-place edits are unsafe.
- Non-inheritable signals are filtered at the runtime boundary; receiver must re-acquire.
- Confidence tier is immutable across boundaries; receivers may not elevate.
- Shared context binds via incident-id (when emitter exists) or session-id (best-effort).
- Shared context cannot mutate knowledge-core under any circumstances.
