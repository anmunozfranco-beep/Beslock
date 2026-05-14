# Runtime Sandboxing & Isolation

Six sandbox patterns; reproducible, append-only, no writes to higher-trust zones.

## Patterns

- `runtime-sandbox` — execute retrieval + assembly + escalation under bounded scope; no outbound writes
- `unsafe-runtime-containment` — any runtime that fails a safety predicate is demoted to a quarantine sandbox; emission is suspended
- `escalation-quarantine` — slices on escalation hold are isolated from new emissions until escalation-supervisor decision
- `reviewer-safe-execution` — reviewer actions execute in a sandbox that cannot reach production write paths
- `provenance-safe-isolation` — provenance records are mounted read-only into every sandbox; mutation paths require governance pipeline auth
- `replay-safe-environment` — replay sandbox executes against frozen orchestration-trace input; outputs go to a side channel, never to production

## Invariants

- every sandbox declares its inputs, outputs, and isolation guarantees
- no sandbox writes to a higher-trust environment
- no sandbox shares mutable state with another sandbox
- every sandbox emits an append-only execution log
- every sandbox is reproducible: same inputs → same outputs
