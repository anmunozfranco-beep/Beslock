# Replay & Deterministic Validation (Phase 27, Layer 21)

## Purpose
Provide a real, deterministic re-execution path for any captured flow run
so that retrieval drift, corpus regressions, or accidental scoring
changes are detected explicitly instead of being absorbed silently.

## What was added
- `runtime/replay.py`:
  - `replay_run(run_id)` — index `orchestration-trace` for the matching
    `flow-start` event, walk every captured `retrieval-trace` event for
    that run, re-execute `retrieval.retrieve()` with the captured
    `(product, query, kind)` triple, and compare the captured node-id
    set to the replayed node-id set.
  - Synthetic empty packages (those whose manifest carries
    `extra.empty=True`, fabricated by `flows.py` when a kind slot is
    intentionally unused) are explicitly skipped — they are not real
    retrieval calls and must not be counted as drift.
  - `replay_all()` — replay every captured run.
  - `summary(replays)` — emit a `runtime-replay/1.0` summary record.
- `cli.py replay` — new subcommand: `replay [--run-id ID]`. Returns
  exit code 0 on full determinism, 1 on detected drift, 2 on unknown
  run id.

## Determinism contract
A replay is **deterministic** when, for every non-synthetic captured
retrieval, the sorted set of node ids in the replayed package equals
the sorted set of node ids in the captured package. Score values are
**not** required to be bit-identical because confidence weighting is
declarative; node-id-set parity is the contract.

## What this does **not** do
- No ML re-training, no embeddings, no production replay-as-canary.
- No auto-rollback. Drift is reported, not corrected.
- No mutation of any captured trace; the NDJSON channels remain
  append-only ground truth.

## Test coverage
- `testing/test_hardening.py::ReplayDeterminismTests::test_replay_run_is_deterministic`
- `testing/test_hardening.py::ReplayDeterminismTests::test_replay_summary_shape`
- Full suite: 19 tests, all pass.
