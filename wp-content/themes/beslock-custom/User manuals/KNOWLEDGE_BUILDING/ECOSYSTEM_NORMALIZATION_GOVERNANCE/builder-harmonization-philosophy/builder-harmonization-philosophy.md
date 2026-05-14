# Builder Harmonization Philosophy

Builders are the canonical authors; one helper, one topology, idempotent.

## Principles

- Builders are the canonical authors of governance artifacts.
- Builders share a single helper (`write_pair`) and a single output topology.
- Builders are idempotent and non-destructive; re-runs converge on the same artifacts.
- Builders emit a final summary line so operators can verify outputs.
