# Interoperability Safety Governance

Hard boundaries on cross-runtime behavior. Unsafe federation states. Escalation- and supervision-required interoperability.

## Interoperability-safe cognition

- Cross-runtime cognition is bounded by declared contracts; outside the contracts is undefined.
- Cross-runtime cognition is read-only into knowledge-core, append-only into shared continuity.
- Cross-runtime cognition cannot elevate confidence or promote P-tier.
- Cross-runtime cognition preserves supervision posture.
- Cross-runtime cognition emits provenance at every boundary crossing.

## Prohibited cross-runtime behaviors

- Mutating knowledge-core from a non-owning runtime.
- Mutating shared continuity in place (only append-only allowed).
- Lowering escalation tier across a runtime boundary.
- Stripping provenance from a cross-runtime message.
- Bridging two runtimes via an undeclared intermediary.
- Auto-resuming destructive activity at a receiver runtime.
- Sharing private cognition state across boundaries.
- Triggering image generation, PDF rendering, or any rendered artefact via federation.
- Federating across runtimes with mismatched schemas.
- Promoting P-tier or elevating confidence at a federation boundary.
- Inheriting non-inheritable signals (e.g. destructive-confirmation).

## Unsafe federation states

- schema-mismatch + any non-escalation cross-runtime message
- tier-4/5 escalation + no declared receiver
- delegated-step + supervision posture downgraded
- co-execution + overlapping scopes without declared arbitration
- degraded participant at L3+ + non-degraded federation level (mismatch)
- cross-runtime destructive path proposed
- shared-context update under uncertain-confidence (must escalate)

## Escalation-required interoperability

- ambiguity at a federation boundary
- contradiction between two runtimes' chain-records on the same incident-id
- schema-mismatch detected mid-session
- delegated runtime fails its declared completion conditions
- receiver runtime rejects a handoff (handoff-failed)
- OEM channel contract absent at tier-4/5

## Supervision-required federation states

- any handoff
- any delegation that touches a destructive surface inside the receiver runtime
- any ecosystem-broadcast at tier-3+
- any restoration that crosses a runtime boundary
- any degraded-federation transition into L3+

## Federated-runtime safety boundaries

- Knowledge-core remains the single source of truth across the federation.
- Lifecycle P-tier gates are enforced at the federation boundary.
- Visual-risk freeze contract applies at every federation boundary involving visual-assistance.
- Irreversibility safeguards (two-token gate) are not bypassable via federation.
- Provenance is mandatory at every cross-runtime crossing; unattributable messages are dropped.
