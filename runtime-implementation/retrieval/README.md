# Retrieval

Real executable retrieval over knowledge-core JSON files.

Implementation: [runtime/retrieval.py](../runtime/retrieval.py).

## Supported kinds

`onboarding`, `troubleshooting`, `operational-procedures`, `warnings`,
`escalation`, `adaptive-guidance`, `fingerprint-enrollment`, `pairing`,
`battery-recovery`.

## Properties

- Read-only over declared `knowledge-core/` domains only.
- Diacritic + lowercase token normalization.
- Jaccard-over-query scoring (deterministic, no ML).
- Surfaces ambiguity instead of resolving it silently.
- Every retrieval-package carries a `runtime-provenance/1.0` manifest with
  SHA-256 hashes of every source file.

## Try

```bash
.venv/bin/python runtime-implementation/cli.py retrieve \
  --product e-prime --query "vincular cerradura" --kind onboarding --top-k 5
```
