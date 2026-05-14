# User Intent Progression

## Intents

- install
- configure
- unlock
- pair-app
- enrol-user
- recover
- troubleshoot
- maintain
- administer
- factory-reset

## Transitions

| from | to | rationale |
|---|---|---|
| install | configure | post-install configuration kicks in |
| configure | pair-app | post-config app pairing |
| pair-app | enrol-user | post-pairing user enrolment |
| enrol-user | unlock | credential available -> first unlock |
| unlock | maintain | routine operation -> maintenance window |
| maintain | troubleshoot | anomaly observed during maintenance |
| troubleshoot | recover | recovery path identified |
| recover | unlock | post-recovery resume operation |
| recover | factory-reset | recovery requires reset |
| factory-reset | install | post-reset re-installation/re-configuration |
| administer | enrol-user | admin enrols new credential |
| administer | factory-reset | admin initiates reset |

## Rules

- User intent is declarative; the execution layer never infers intent silently from behaviour.
- Intent transitions are tracked; abrupt intent changes (e.g. troubleshoot -> install) require checkpoint recovery.
- Intent and operational-state must remain consistent; mismatched pairs are a composition error.
- Intent `factory-reset` automatically attaches hard-interrupting guidance triggers and irreversibility warnings.
