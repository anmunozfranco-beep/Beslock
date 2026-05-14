# Operational Value Prioritization

Weighted scoring rubric and ranking of all candidate runtime realizations. Safety > readiness > value.

## Dimensions

- `operational-value` (weight: 0.2, 1 (low) — 5 (high))
- `implementation-complexity` (weight: 0.15, 1 (high complexity) — 5 (low complexity))
- `runtime-readiness` (weight: 0.15, 1 (not ready) — 5 (fully gated))
- `cognition-maturity` (weight: 0.15, 1 (immature) — 5 (mature))
- `user-impact` (weight: 0.1, 1 (low) — 5 (high))
- `deployment-safety` (weight: 0.15, 1 (unsafe) — 5 (safe by construction))
- `governance-stability` (weight: 0.1, 1 (unstable) — 5 (stable))

## Candidates (ranked)

- `contextual-retrieval` — score: 4.7 — destructive: False — blocking: 0 — realizable now: True
- `procedural-assembly-runtime` — score: 4.1 — destructive: False — blocking: 0 — realizable now: True
- `operational-copilot` — score: 3.7 — destructive: False — blocking: 3 — realizable now: False
- `onboarding-runtime` — score: 3.4 — destructive: False — blocking: 2 — realizable now: False
- `troubleshooting-runtime` — score: 2.85 — destructive: False — blocking: 3 — realizable now: False
- `administrator-assistant` — score: 2.1 — destructive: True — blocking: 3 — realizable now: False

## Rules

- Safety > readiness > value: deployment-safety and runtime-readiness dominate value when ranking ties or near-ties occur.
- Any candidate with a destructive surface is automatically gated to supervised-runtime phase or higher; never realized in prototype.
- A candidate with one or more blocking risks is non-realizable regardless of weighted score.
- Soft risks degrade the realization to the next-safer stage but do not block.
- Score updates require evidence; ad-hoc reweighting is unsafe.
