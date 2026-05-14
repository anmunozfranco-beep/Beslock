# User journey semantics

_Schema: `experience-governance/1.0` · user-journey model · generated 2026-05-13T17:27:13Z._

## Purpose

Model the operational journeys a real user undertakes with a Beslock product.
Per-product specialisation extends these archetypes; it does not invent
parallel journeys.

## Journey archetypes

| ID | Label | Criticality | Guidance intensity | Phases |
|---|---|---|---|---:|
| `journey.first-installation` | First installation | critical | high | 8 |
| `journey.first-unlock` | First unlock | high | medium | 4 |
| `journey.first-app-pairing` | First app pairing | high | high | 5 |
| `journey.administrator-setup` | Administrator setup | high | medium | 5 |
| `journey.user-enrolment` | User enrolment | medium | medium | 5 |
| `journey.battery-replacement` | Battery replacement | medium | low | 5 |
| `journey.emergency-recovery` | Emergency recovery | critical | very-high | 6 |
| `journey.factory-reset-recovery` | Factory reset recovery | critical | very-high | 5 |
| `journey.troubleshooting-escalation` | Troubleshooting escalation | high | high | 5 |

## Schema

```json
{
  "id": "journey.<slug>",
  "label": "<human label>",
  "actors": ["installer", "admin-owner", "regular-user", "support"],
  "phases": ["..."],
  "trigger": "<plain-language event>",
  "success_state": "<observable end state>",
  "failure_modes": ["..."],
  "guidance_intensity": "low | medium | high | very-high",
  "criticality": "low | medium | high | critical"
}
```

## Cross-journey rules

- A journey MUST reference canonical procedure IDs from the ontology.
- A journey MAY reference per-product specialisations via the shared concept
  membership map (Knowledge Center).
- A journey MUST declare its success state and at least its three most
  common failure modes.
- A journey's `guidance_intensity` determines the default contextual
  guidance trigger profile (see `guidance-semantics/`).

## Companion file

- [`user-journeys.json`](user-journeys.json) — machine-readable archetype set.
