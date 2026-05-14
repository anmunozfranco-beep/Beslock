# Operational Console Modeling

Six operator consoles, design-only — no implementation in this layer.

## Consoles

- `runtime-console` — audience: runtime-operator; surfaces: flow start, retrieval-package preview, approve/reject/demote
- `reviewer-console` — audience: reviewer; surfaces: queue claim, side-by-side OEM, evidence attach, approve/reject
- `escalation-console` — audience: escalation-supervisor; surfaces: incoming handoffs, trigger explanation, route choices
- `governance-console` — audience: governance-maintainer; surfaces: reviewer registry, scope edits (within charter), emergency demotion
- `audit-console` — audience: operational-auditor; surfaces: read-only event stream, replay, finding emission
- `continuity-console` — audience: runtime-operator + escalation-supervisor; surfaces: checkpoint timeline, resume-from-checkpoint, snapshot inspect

## Console design rules

- consoles are operator surfaces, not consumer applications
- consoles never render speculative content; only declared events and packages
- consoles always show provenance + confidence + uncertainty alongside any recommendation
- consoles never expose actions outside the operator's declared scope
- consoles emit append-only events for every operator action
- consoles are out of scope here as implementations; this layer is design-only
