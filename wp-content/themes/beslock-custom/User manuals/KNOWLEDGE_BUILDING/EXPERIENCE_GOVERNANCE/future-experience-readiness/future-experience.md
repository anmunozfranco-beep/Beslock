# Future experience readiness

_Schema: `experience-governance/1.0` · future experience surfaces · generated 2026-05-13T17:27:13Z._

## Subordination

Every future experience surface — chatbot guidance, onboarding assistants,
troubleshooting assistants, contextual UI guidance, adaptive documentation,
progressive manuals, dynamic knowledge rendering, multimodal assistance — is
**subordinate to the knowledge core** and bound by this charter.

## Surface contracts

| Surface | Required inputs | Constraints |
|---|---|---|
| Chatbot guidance        | priority assignments + maturity gate ≥ canonical + journey context | Must surface provenance, must respect interruption budget. |
| Onboarding assistant    | onboarding-flows.json + cognitive-load.json + safe-first-use rule | Must always run safe-first-use before optional flows. |
| Troubleshooting assistant | escalation-model.json + symptom-category map + run records | Must respect tier escalation rules; never auto-jumps two tiers. |
| Contextual UI guidance  | guidance-triggers.json + component-visibility | Must apply highest-intensity trigger; visual reinforcement bound by visual constitution. |
| Adaptive documentation  | learning-paths + prerequisites + maturity gate | Surfaces only what the user is ready for; collapses already-mastered prerequisites. |
| Progressive manuals     | priority assignments + cognitive load | Reorders sections by tier; never drops P0/P2 content. |
| Dynamic knowledge rendering | knowledge-graph + publication-intent | Per-channel formatting via Knowledge Center retrieval strategy. |
| Multimodal assistance   | terminology synonyms + procedural-semantics + visual semantics | Voice + visual + text must converge on the same canonical procedure id. |

## Out of scope

- Implementing any of the above surfaces (rendering, runtime, frontend).
- Generating images, PDFs, or final manuals.
- Building chatbot or assistant runtimes.
- Optimising rendering systems.

These remain explicitly out of scope until separate, dedicated phases.
