# Contextual Warning Escalation

## Levels

- **informational** — {"rank": 0, "must_acknowledge": false}
- **advisory** — {"rank": 1, "must_acknowledge": false}
- **caution** — {"rank": 2, "must_acknowledge": true}
- **warning** — {"rank": 3, "must_acknowledge": true}
- **critical** — {"rank": 4, "must_acknowledge": true}
- **irreversible** — {"rank": 5, "must_acknowledge": true, "requires_explicit_action": true}
- **emergency** — {"rank": 6, "must_acknowledge": true, "requires_explicit_action": true}

## Rules

- **severity-driven** — {"rule": "severity-level=warning -> minimum caution; severity-level in {blocked,unsafe} -> minimum warning"}
- **interruption-driven** — {"rule": "interruption during destructive step -> escalate to critical"}
- **unsafe-state-driven** — {"rule": "entering an unsafe state -> warning + mandatory-warning surface"}
- **recovery-driven** — {"rule": "recovery in progress -> all subsequent steps escalate one level"}
- **irreversible-driven** — {"rule": "irreversible operations -> always 'irreversible' level + explicit-action confirmation"}
- **emergency-driven** — {"rule": "operational-mode=emergency -> emergency level on any non-safety step blocking continuation"}
- **evidence-driven** — {"rule": "confidence-level in {inferred,ocr-derived,ambiguous} -> attach 'advisory' disclosure to operational claims"}

## Invariants

- warnings can be escalated by adaptation but never demoted
- an explicit-action confirmation cannot be replaced by acknowledgement
- warnings declared by knowledge-core or composition are non-removable
- every escalation must record its trigger predicate (auditable)
