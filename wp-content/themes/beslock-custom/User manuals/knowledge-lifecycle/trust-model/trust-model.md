# Trust Evolution Model

Tiers, transitions, inheritance floor, decay, stale-knowledge detection, dispute propagation.

## Trust tiers

- `candidate` (weight 0.4, runtime: soft-escalation)
- `low-confidence` (weight 0.5, runtime: supervised-only)
- `ocr-derived` (weight 0.85, runtime: supervised)
- `inferred` (weight 0.65, runtime: supervised + traversal evidence)
- `reviewer-confirmed` (weight 0.92, runtime: supervised)
- `oem-verified` (weight 1.0, runtime: supervised primary)
- `operationally-proven` (weight 1.0, runtime: supervised primary + replay-validated)

## Trust transitions

- trust raises only through declared promotion gates
- trust may decay (see decay rules) but never silently
- trust inheritance: a derived node inherits the floor of its source tiers, not the ceiling
- dispute propagation: a disputed source caps all derived nodes at `low-confidence` until resolved

## Trust decay rules

- OEM source supersession → all bound nodes demote to candidate pending re-review
- stale OCR pipeline version (older than declared floor) → demote to candidate
- reviewer revocation → records that reviewer signed alone revert to ocr-derived/inferred
- operational-incident on a node in supervised use → demote one tier + open dispute
- retention-period elapsed without re-validation → demote to candidate

## Stale-knowledge detection

- stale = `updated_at` older than the per-tier max_age
- stale = bound to a source artifact that has been superseded
- stale = bound to a reviewer whose signoff scope has changed
- detected stale records are queued for re-review, not silently kept
