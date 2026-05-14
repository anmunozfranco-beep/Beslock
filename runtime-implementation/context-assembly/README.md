# Context Assembly

Real executable assembly. Merges procedure + warnings + prerequisites +
troubleshooting + continuity-state + adaptive-guidance into a bound
assembly-package.

Implementation: [runtime/assembly.py](../runtime/assembly.py).

## Invariants

- Mandatory warnings cannot be suppressed.
- Prerequisite gaps block guidance emission.
- Adaptive precedence (knowledge-core > adaptive) is invariant.
- Confidence is never elevated to compensate for missing inputs.
- Escalation tier is computed and recorded; tier is monotonic across the run.
