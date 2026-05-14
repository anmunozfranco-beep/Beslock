# Contradiction & Conflict Reasoning

## Conflict Types

- **evidence-conflict** — {"description": "two evidence nodes disagree on the same claim"}
- **procedure-conflict** — {"description": "two procedures prescribe contradictory steps for the same situation"}
- **predicate-conflict** — {"description": "two validation predicates yield opposite results on the same state"}
- **state-conflict** — {"description": "current state cannot match the precondition of any eligible branch"}
- **intent-conflict** — {"description": "declared intent contradicts current operational state"}
- **recovery-signal-conflict** — {"description": "recovery indicators disagree (e.g., partial success + failure flag)"}
- **authority-conflict** — {"description": "two layers claim authority over the same decision"}

## Resolution Rules

- no conflict may be resolved silently
- evidence-conflict at verified-truth tier escalates to OEM (P0 procedures)
- procedure-conflict requires composition-layer disambiguation (declared owner)
- predicate-conflict halts the chain and emits validation-finding
- state-conflict requires recovery-reasoning or escalation
- intent-conflict requires ask-disambiguation (non-destructive) or escalate
- authority-conflict resolves by the declared layer ordering (knowledge-core wins; adaptive/decision/reasoning never override)
- every conflict event is recorded for knowledge-health intake

## Unsafe Reasoning Indicators

- abductive conclusion presented as verified
- chain crossing an unsafe state without escalation
- consequence claimed without declared causal link
- recovery asserted without checkpoint anchor
- destructive recommendation under low/ambiguous confidence
