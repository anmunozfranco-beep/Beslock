# Onboarding Composition

| id | always_on | audience_scope | package | interruption_budget |
|---|---|---|---|---|
| first-time-user | True | beginner | onboarding-package | 2 |
| installer-onboarding | False | installer | installation-package | 2 |
| administrator-onboarding | False | administrator | administrator-setup-package | 1 |
| app-onboarding | False | beginner | onboarding-package | 2 |
| safe-operational-activation | True | beginner | onboarding-package | 2 |

## Rules

- Always-on flows are non-skippable; their inclusion is enforced by the composition layer, not the consumer.
- Interruption budget is hard-capped per session; exceeding it is a composition error.
- Onboarding flows compose with cognitive-load-map; very-high-load procedures MUST chunk + confirm.
- Audience scope is enforced; mismatched audience composition is rejected.
