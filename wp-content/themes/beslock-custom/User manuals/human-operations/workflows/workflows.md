# Executable Workflow Design

Seven declared executable workflows with checkpoints, halt conditions, and primary actors.

## Workflows

- `onboarding-execution` — actor: runtime-operator; checkpoints: pre-emission, post-emission; halts on: safety-demote
- `troubleshooting-execution` — actor: runtime-operator; checkpoints: pre-emission, candidate-only-disclosure; halts on: candidate-only + irreversible-adjacent
- `escalation-review` — actor: escalation-supervisor; checkpoints: accept-handoff, route-decision, post-route; halts on: unresolved disagreement
- `candidate-review` — actor: reviewer; checkpoints: evidence-pull, approve-or-reject, post-audit; halts on: missing-binding
- `oem-verification` — actor: oem-reviewer; checkpoints: binding-attached, dual-review, post-supersession; halts on: dual-review-disagreement
- `rollback-handling` — actor: governance-maintainer; checkpoints: target-confirm, fanout-preview, post-rollback; halts on: fanout-exceeds-declared-scope
- `runtime-incident-review` — actor: operational-auditor; checkpoints: incident-claim, replay-validate, finding-emit; halts on: replay-drift-exceeds-floor

## Workflow invariants

- every workflow step is a declared checkpoint with a declared decision set
- every workflow halt is a declared, observable event — never a silent stall
- every workflow emits an append-only orchestration-trace record
- no workflow may auto-resume after a halt without an operator decision
- no workflow may bypass its declared checkpoints under any condition
