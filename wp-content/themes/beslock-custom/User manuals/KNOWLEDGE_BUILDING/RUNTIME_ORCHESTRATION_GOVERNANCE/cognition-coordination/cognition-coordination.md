# Cognition Coordination Contracts

Declared bilateral contracts between cognition systems. Violations are runtime errors, not warnings.

## Contracts

- `retrieval↔composition` — retrieval → composition
- `composition↔adaptive` — composition → adaptive
- `adaptive↔reasoning` — adaptive → reasoning
- `reasoning↔decision` — reasoning → decision
- `decision↔escalation` — decision → escalation
- `decision↔execution` — decision → execution
- `execution↔continuity` — execution → continuity
- `continuity↔retrieval` — continuity → retrieval
- `escalation↔continuity` — escalation → continuity
- `validation↔all` — validation → all
- `experience↔adaptive` — experience → adaptive
- `lifecycle↔composition` — lifecycle → composition
- `knowledge-core↔retrieval` — knowledge-core → retrieval

## Rules

- Coordination contracts are bilateral and declared; runtime cannot invent new edges.
- Coordination contract violations are runtime errors, not warnings.
- Coordination is observable: every cross-contract message emits provenance.
- Coordination preserves directionality (read-only into knowledge-core; append-only into continuity).
- Coordination cannot bridge two systems via an undeclared intermediary.
- Coordination never elevates confidence, never promotes P-tier, never reassigns role.
- Coordination across destructive surfaces requires the explicit-action gate before message acceptance.
