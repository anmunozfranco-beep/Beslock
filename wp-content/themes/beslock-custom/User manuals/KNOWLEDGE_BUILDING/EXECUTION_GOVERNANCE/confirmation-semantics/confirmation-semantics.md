# Confirmation & Validation Semantics

## Confirmation types

| id | required_for |
|---|---|
| user-acknowledgement | warning surfacing |
| explicit-action | destructive steps (factory-reset, delete-credential) |
| device-feedback | step that depends on physical device response |
| validation-predicate | procedure completion |
| oem-confirmation | P0 safety-critical promotions only |

## Validation predicates

| procedure_class | predicate |
|---|---|
| pairing | device reports `paired` and round-trip ping succeeds |
| enrollment | device reports `enrolled` and credential-id is recorded |
| factory-reset | device reports `factory-default` and admin-state=no-admin |
| battery-replacement | battery-state=restored and device boots nominally |
| installation | install-state=verified-install and operational-state=normal |

## Rules

- Procedure completion requires both: terminal state reached AND validation-predicate satisfied.
- Destructive steps require explicit-action confirmation; user-acknowledgement is insufficient.
- Device-feedback failures within timeout default to `validation-failure` interruption.
- OEM-confirmation is mandatory for promoting any procedure to verified-truth at P0.
- Confirmation traces are recorded and feed knowledge-health monitoring.
