# Knowledge Diff & Lineage Tooling

Deterministic, read-only diffs and lineage walks computed from append-only logs.

## Diff kinds

- `node-diff` — two versions of a node by id; structural + semantic field-level diff
- `binding-diff` — current vs prior_binding_id chain
- `trust-tier-diff` — tier transitions over time
- `lineage-walk` — promotion/demotion event chain for a node
- `evidence-walk` — binding chain from node to OEM source artifact
- `rollback-walk` — rollback chain referencing original promotion ids

## Lineage views

- operational-history: chronological event stream per node
- promotion-lineage: state transitions only
- evidence-lineage: binding records only
- rollback-lineage: demotions referencing promotions
- trust-evolution-visualization: tier-over-time per node (data; no rendering layer)

## Invariants

- diffs are deterministic and reproducible from append-only logs
- lineage is never reconstructed; it is read directly from the event store
- diffs do not mutate; they only report
- diffs respect scope (per product, per domain); cross-product diffs are forbidden
