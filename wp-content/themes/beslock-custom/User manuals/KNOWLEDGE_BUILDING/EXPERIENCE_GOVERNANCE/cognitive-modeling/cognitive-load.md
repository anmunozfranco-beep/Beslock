# Cognitive load modeling

_Schema: `experience-governance/1.0` · cognitive load model · generated 2026-05-13T17:27:13Z._

## Dimensions

| Dimension | Definition |
|---|---|
| `dim.procedural-density` | Steps per minute of expected user time. |
| `dim.memory-burden` | Number of items the user must hold in working memory simultaneously. |
| `dim.role-switching` | Number of role transitions (admin↔user, app↔lock) the procedure forces. |
| `dim.modality-switching` | Transitions between physical, app and audio modalities. |
| `dim.failure-cost` | Cost of a single mis-step (e.g. lockout, data-loss, broken hardware). |
| `dim.recoverability` | How easily an error is undone within the same flow. |
| `dim.terminology-ambiguity` | Density of synonyms or unfamiliar terms in the procedure surface. |

## Per-procedure load assessment

| Procedure | Load | Dominant dimensions |
|---|---|---|
| `procedure.factory-reset` | very-high | `dim.failure-cost`, `dim.recoverability` |
| `procedure.emergency-power` | very-high | `dim.failure-cost`, `dim.modality-switching` |
| `procedure.firmware-update` | high | `dim.failure-cost`, `dim.role-switching` |
| `procedure.pair-with-app` | high | `dim.modality-switching`, `dim.role-switching` |
| `procedure.register-fingerprint` | medium | `dim.procedural-density` |
| `procedure.add-administrator` | medium | `dim.role-switching` |
| `procedure.add-user` | medium | `dim.role-switching` |
| `procedure.register-pin` | low | `dim.memory-burden` |
| `procedure.unlock-pin` | low | — |
| `procedure.unlock-fingerprint` | low | — |
| `procedure.battery-replacement` | low | — |

## Design rules

1. `very-high` load procedures MUST receive the highest guidance intensity
   and MUST be flanked by recovery context.
2. `high` load procedures SHOULD provide an explicit success-state
   confirmation and a documented rollback.
3. `low` load procedures SHOULD NOT trigger hard interrupts.
4. A procedure whose load is `very-high` and whose recoverability is poor
   MUST appear in onboarding even if it is rare.

## Companion file

- [`cognitive-load.json`](cognitive-load.json)
