# Safe Execution Governance

## Safeguards

| id | applies_to | reason |
|---|---|---|
| irreversibility-warning | factory-reset, delete-all-users, firmware-rollback |  |
| double-confirmation | factory-reset, delete-all-users |  |
| battery-precondition | firmware-upgrade, factory-reset | low-battery may brick mid-operation |
| network-precondition | app-pairing, remote-unlock | 2.4G band requirement |
| physical-presence | factory-reset, battery-replacement | remote initiation forbidden |
| mandatory-warning-surface | all destructive procedures | warning must reach user before step starts |

## Escalation thresholds

| trigger | escalate_to |
|---|---|
| 3 consecutive validation-failures | tier-2 |
| pairing-failed after 3 retries | tier-3 |
| lockout (max-failed-attempts) ≥ 2 cycles | tier-3 |
| depleted + replacement fails | tier-4 (vendor) |
| firmware-bricked | tier-5 (RMA) |

## Irreversible operations

- factory-reset
- delete-all-users
- firmware-rollback
