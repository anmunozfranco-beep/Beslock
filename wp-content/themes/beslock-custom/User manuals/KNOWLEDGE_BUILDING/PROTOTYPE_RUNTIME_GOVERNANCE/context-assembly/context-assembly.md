# Contextual Assembly Execution

Four declared assembly flows merging procedures, warnings, prerequisites, troubleshooting, escalation, continuity, and adaptive guidance.

## Flows

- `procedures+warnings+prerequisites` — merges: procedure-nodes, mandatory-warnings, prerequisite-records
- `troubleshooting+causal+continuity` — merges: diagnostic-nodes, causal-edges, continuity-state
- `escalation+continuity+adaptive` — merges: escalation-predicate-result, continuity-snapshot, adaptation-record
- `onboarding+adaptive+supervision` — merges: onboarding-nodes, adaptation-record, supervision-receipt

## Rules

- Mandatory warnings cannot be suppressed in any assembly.
- Prerequisite gaps block assembly emission; they do not silently degrade guidance.
- Continuity state is read-only at assembly time; mutations require declared continuity flow.
- Adaptive precedence (knowledge-core > adaptive) is invariant.
- Assembly emits a single bound assembly-package per run-step.
