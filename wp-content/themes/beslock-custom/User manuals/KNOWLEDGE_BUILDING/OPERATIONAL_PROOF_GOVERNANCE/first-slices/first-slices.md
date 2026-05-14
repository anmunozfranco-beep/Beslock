# First Executable Slice Selection

Weighted ranking of executable proof-of-value candidates. Safety > runtime risk > value. Destructive surfaces are out of scope for proof.

## Selection criteria

- `operational-value` (weight: 0.2)
- `runtime-risk-inverse` (weight: 0.2)
- `validates-architecture` (weight: 0.15)
- `validates-retrieval` (weight: 0.15)
- `validates-assembly` (weight: 0.15)
- `validates-coherence` (weight: 0.15)

## Candidates (ranked)

- `contextual-retrieval-proof` — score: 4.5 — destructive: False — blocking: 0 — proof eligible: True
- `procedural-assistance-proof` — score: 4.45 — destructive: False — blocking: 0 — proof eligible: True
- `onboarding-guidance-proof` — score: 3.8 — destructive: False — blocking: 2 — proof eligible: False
- `troubleshooting-guidance-proof` — score: 3.5 — destructive: False — blocking: 3 — proof eligible: False
- `operational-recovery-assistance-proof` — score: 3.45 — destructive: False — blocking: 3 — proof eligible: False
- `administrator-guidance-proof` — score: 2.6 — destructive: True — blocking: 3 — proof eligible: False

## Rules

- First executable slice MUST be read-only and have no blocking risks.
- Destructive surfaces are out of scope for proof-of-value.
- Soft risks degrade the slice to operator-observed mode but do not block.
- Score updates require evidence; ad-hoc reweighting is unsafe.
- Selected slice must validate retrieval + assembly + coherence simultaneously.
