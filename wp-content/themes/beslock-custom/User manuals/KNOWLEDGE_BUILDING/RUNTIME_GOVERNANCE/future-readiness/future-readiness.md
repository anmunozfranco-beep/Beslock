# Future Runtime Readiness

## Future Consumers

- **onboarding-copilot** — {"gates": ["context-vector emitter", "intent declaration channel", "checkpoint registry on onboarding", "predicate coverage on pairing+enrollment", "provenance emitter"]}
- **troubleshooting-assistant** — {"gates": ["symptom corpus >= 10/product", "causal edges emitted", "hypothesis store contract", "branch provenance log"]}
- **contextual-operational-assistant** — {"gates": ["context-vector emitter", "decision provenance log", "reasoning provenance log", "fallback registry"]}
- **multimodal-runtime-system** — {"gates": ["visual-risk reclassification freeze", "visual-intent attached to physical-installation", "evidence-disclosure renderer contract"]}
- **future-visual-assistance** — {"gates": ["visual-risk reclassification freeze", "fallback registry for visual-unavailable contexts"]}
- **adaptive-operational-runtime** — {"gates": ["context store contract", "session-signal emitter", "OEM channel contract", "all four 'high' runtime risks resolved for the chosen slice"]}

## First-Runtime Assessment

```json
{
  "primary_first_slice": "procedural-retrieval",
  "rationale": "read-only; no destructive surface; activates ACCESS_AND_CONSUMPTION + COMPOSITION + CONTINUITY (snapshot only) without execution risk",
  "blocking_risks_for_primary": [],
  "soft_risks_for_primary": [
    "no-provenance-emitter (degrades replay determinism but does not block read-only retrieval)"
  ],
  "exit_criteria": [
    "declared query intents resolvable",
    "stable surfaces enumerated",
    "consumption gates enforceable read-side",
    "provenance manifest attached to each retrieval-package"
  ],
  "secondary_slice": "contextual-operational-assembly",
  "blocking_risks_for_secondary": [
    "no-context-vector-emitter (degraded mode possible: use safest defaults)"
  ],
  "deferred_slices": [
    "onboarding-guidance",
    "troubleshooting-guidance",
    "administrator-assistance",
    "recovery-assistance"
  ],
  "deferred_blocking_summary": [
    "onboarding-guidance: requires checkpoint registry + intent declaration + predicate coverage",
    "troubleshooting-guidance: requires symptom corpus >= 10/product + causal edges + hypothesis store",
    "administrator-assistance: requires OEM channel contract + role declaration + checkpoint registry",
    "recovery-assistance: requires checkpoint registry + causal edges + hypothesis store"
  ],
  "doctrine": "no slice is realised while any declared blocking-risk for that slice remains unresolved"
}
```
