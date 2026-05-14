# Beslock Experience Governance

_Schema: `experience-governance/1.0` · index · generated 2026-05-13T17:27:13Z._

This folder is the **constitutional + modeling layer for knowledge
experience**. It models how users consume the knowledge core; it does not
implement chatbots, onboarding apps, troubleshooting assistants or
documentation surfaces.

## Documents

- [`00-charter.md`](00-charter.md)
- [`experience-semantics/user-journeys/user-journeys.md`](experience-semantics/user-journeys/user-journeys.md)
- [`experience-semantics/user-journeys/user-journeys.json`](experience-semantics/user-journeys/user-journeys.json)
- [`knowledge-consumption/consumption-flow.md`](knowledge-consumption/consumption-flow.md)
- [`knowledge-consumption/prerequisites.json`](knowledge-consumption/prerequisites.json)
- [`knowledge-consumption/learning-paths.json`](knowledge-consumption/learning-paths.json)
- [`guidance-semantics/contextual-guidance.md`](guidance-semantics/contextual-guidance.md)
- [`guidance-semantics/guidance-triggers.json`](guidance-semantics/guidance-triggers.json)
- [`cognitive-modeling/cognitive-load.md`](cognitive-modeling/cognitive-load.md)
- [`cognitive-modeling/cognitive-load.json`](cognitive-modeling/cognitive-load.json)
- [`troubleshooting-experience/escalation-model.md`](troubleshooting-experience/escalation-model.md)
- [`troubleshooting-experience/escalation-model.json`](troubleshooting-experience/escalation-model.json)
- [`onboarding-semantics/onboarding-flows.md`](onboarding-semantics/onboarding-flows.md)
- [`onboarding-semantics/onboarding-flows.json`](onboarding-semantics/onboarding-flows.json)
- [`knowledge-priority/priority-model.md`](knowledge-priority/priority-model.md)
- [`knowledge-priority/priority-assignments.json`](knowledge-priority/priority-assignments.json)
- [`future-experience-readiness/future-experience.md`](future-experience-readiness/future-experience.md)

## Sibling constitutional layers

- Visual governance: [`../VISUAL_GOVERNANCE/00-CONSTITUTION.md`](../VISUAL_GOVERNANCE/00-CONSTITUTION.md)
- Knowledge center: [`../KNOWLEDGE_CENTER/00-architecture.md`](../KNOWLEDGE_CENTER/00-architecture.md)
- Semantic governance: [`../SEMANTIC_GOVERNANCE/00-charter.md`](../SEMANTIC_GOVERNANCE/00-charter.md)

## Hard guarantees

- No artifact under `ext-images/<slug>/knowledge-core/` was modified.
- No governance file under `visual-system/_governance/` was modified.
- No Comfy / orchestration / visual-generation file was modified.
- No PDF, image, chatbot runtime or frontend was generated or built.
- All experience modeling is descriptive of the knowledge core; it adds no
  new product knowledge.
