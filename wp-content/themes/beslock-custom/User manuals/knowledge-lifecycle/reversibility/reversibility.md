# Reversible Promotion Governance

Append-only promotion/demotion events, invalidation propagation, runtime-safe demotion, lineage preservation.

## Reversible promotion rules

- every promotion is recorded as an append-only `promotion-event` with prior_state, new_state, rationale, reviewer(s), and binding ids
- every promotion is reversible by an equal-or-higher governance decision
- rollback emits a `demotion-event` referencing the original promotion-event id
- rollback never deletes the promotion-event; both events coexist in lineage

## Invalidation propagation

- invalidation of a source → fan out to all bound nodes (BFS over oem_binding edges)
- invalidation of an inference rule → fan out to all inferred nodes that cited it
- fan-out is bounded by the declared lineage edges only; no inferred fan-out
- each fanned-out demotion is its own append-only event

## Runtime-safe demotion

- demotion never mutates retrieval-trace history; it only changes future retrievals
- demotion of a node currently inside a live supervised slice halts the slice
- demotion never silently lowers a slice's confidence after emission
- demotion of a record bound to an active continuity-checkpoint forces re-checkpoint

## Deprecated node handling

- deprecated nodes remain readable; retrieval ranks them at weight 0
- deprecated nodes carry `superseded_by` pointer(s)
- deprecated nodes are excluded from `oem-verified` and `operationally-proven` rollups
- deprecated nodes are not eligible for re-promotion without an explicit governance decision

## Historical lineage preservation

- every node carries an append-only `lineage` array of state transitions
- lineage entries are content-addressed and signed by the actor
- archival preserves lineage in a separate read-only domain
- lineage is never overwritten; it is only appended
