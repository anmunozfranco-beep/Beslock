# Experience Governance Charter

_Schema: `experience-governance/1.0` · experience-governance constitution · generated 2026-05-13T17:27:13Z._

## Purpose

This charter defines the constitutional layer of **knowledge experience**.
It governs how the knowledge core is presented to users, how guidance is
triggered, how onboarding branches, how troubleshooting escalates and how
operational complexity is bounded.

Experience governance is distinct from:

- knowledge governance (`KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/`) — owns terminology, identifiers, conflicts, retrieval contracts.
- knowledge-center architecture (`KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/`) — owns ontology, maturity tiers, retrieval strategy.
- visual governance (`KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/`) — owns visual policy.
- runtime governance (`visual-system/_governance/`) — operational rules.

## Principles

1. **Experience descends from knowledge.** Every user-facing interaction is a
   projection of canonical knowledge; experience MAY refine presentation, MAY
   NOT redefine semantics.
2. **Progressive disclosure by default.** Show what is needed for the
   current step; hide complexity until the user is ready for it.
3. **Interruption is a budget.** Hard interrupts are reserved for safety,
   data-loss and lockout risks. Everything else is inline.
4. **Onboarding is safety-first.** The first 24 hours optimise for safe
   recovery awareness, not for feature exposure.
5. **Troubleshooting respects tiers.** Self-recovery before reconfiguration,
   reconfiguration before factory-reset, factory-reset before support
   contact, support before RMA.
6. **Cognitive load is a design budget.** Procedures with high failure
   cost and low recoverability MUST receive the strongest guidance.
7. **Subordination of all surfaces.** Chatbot, onboarding assistant,
   troubleshooting assistant, contextual UI, adaptive docs, dynamic
   rendering and multimodal assistance are subordinate to the knowledge
   core. None of them originates knowledge.

## Authorities

| Concern | Authority | Location |
|---|---|---|
| User journeys                  | Experience Governance | `experience-semantics/user-journeys/` |
| Knowledge consumption flow     | Experience Governance | `knowledge-consumption/` |
| Contextual guidance triggers   | Experience Governance | `guidance-semantics/` |
| Cognitive load model           | Experience Governance | `cognitive-modeling/` |
| Troubleshooting escalation     | Experience Governance | `troubleshooting-experience/` |
| Onboarding flows               | Experience Governance | `onboarding-semantics/` |
| Knowledge prioritization       | Experience Governance | `knowledge-priority/` |
| Procedural verbs / IDs         | Semantic Governance   | `KNOWLEDGE_BUILDING/SEMANTIC_GOVERNANCE/` |
| Maturity tiers                 | Knowledge Center      | `KNOWLEDGE_BUILDING/KNOWLEDGE_CENTER/knowledge-maturity/` |
| Visual policy                  | Visual Governance     | `KNOWLEDGE_BUILDING/VISUAL_GOVERNANCE/` |

## Amendment policy

A change in experience governance MUST NOT change canonical semantics. If a
change requires renaming a concept or changing a procedure's identity, the
amendment first goes through Semantic Governance.
