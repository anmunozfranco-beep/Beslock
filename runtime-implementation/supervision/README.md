# Supervision

Real operator review checkpoints with append-only supervision receipts.

Implementation: [runtime/supervision.py](../runtime/supervision.py).

## Checkpoints

`pre-emission`, `post-emission`, `pre-handoff`, `pre-completion`, `post-anomaly`.

## Decisions

`approve` / `reject` / `request-more-info` / `escalate` / `demote`.

## Properties

- Every supervision boundary emits a `SupervisionReceipt` with operator id +
  timestamp + payload summary.
- Operator may not relax safety-preserving adaptations.
- Operator may not downgrade irreversibility warnings.
- `reject` and `demote` are blocking; only `approve` advances the slice.

## Try

Interactive (waits for stdin):

```bash
.venv/bin/python runtime-implementation/cli.py flow onboarding \
  --product e-prime --query "vincular cerradura"
```

Non-interactive (auto-approve for harness use):

```bash
.venv/bin/python runtime-implementation/cli.py flow onboarding \
  --product e-prime --query "vincular cerradura" --approve
```
