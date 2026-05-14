# Contextual Execution Flows

## Flows

- **retrieval-execution-flow** — {"steps": ["receive query intent", "validate against declared intents", "resolve via ACCESS_AND_CONSUMPTION", "apply consumption gates", "emit retrieval provenance", "return read-only result"]}
- **contextual-assembly-execution-flow** — {"steps": ["receive request + context vector", "apply ADAPTIVE precedence", "compose via COMPOSITION rules", "validate composition", "emit assembly provenance", "return assembled package"]}
- **reasoning-invocation-flow** — {"steps": ["bind context", "open reasoning chain", "evaluate causal links + predicates", "track hypotheses", "terminate (concluded / inconclusive / escalated)", "emit chain provenance"]}
- **escalation-flow** — {"steps": ["detect trigger", "monotonic tier increment", "build escalation package via CONTINUITY", "hand off (read-only)", "append escalation-history", "emit provenance"]}
- **interruption-flow** — {"steps": ["detect interruption case", "halt destructive boundaries", "preserve checkpoints + provenance", "emit interruption event", "await resume / cancel / escalate"]}
- **continuity-restoration-flow** — {"steps": ["load context schema", "verify session+product", "re-evaluate last predicate", "re-acknowledge open warnings/escalations", "verify checkpoint anchor", "rebind hypotheses", "emit restoration provenance"]}

## Rules

- every flow declares its steps; runtime may not insert undeclared steps
- every flow emits provenance at completion or failure
- flows are reproducible from declared inputs
- flows respect contract guarantees of the layers they invoke
- destructive flows always include an explicit-action step
