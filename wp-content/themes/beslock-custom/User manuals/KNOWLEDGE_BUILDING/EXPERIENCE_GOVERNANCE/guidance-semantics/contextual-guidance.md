# Contextual guidance semantics

_Schema: `experience-governance/1.0` · guidance triggers · generated 2026-05-13T17:27:13Z._

## Trigger registry

| Trigger | Intensity | Interrupts flow | Rule |
|---|---|---|---|
| `trigger.first-time-procedure` | high | no | Surface step-by-step guidance the first time a user attempts a procedure. |
| `trigger.high-risk-procedure` | very-high | yes | Surface confirmation + explicit risk note before factory-reset, firmware-update, emergency-power. |
| `trigger.failure-prone-step` | medium | no | Inline visual reinforcement on steps with documented failure modes. |
| `trigger.warning-blocking` | very-high | yes | Hard interrupt (modal-equivalent) for safety + data-loss + lockout warnings. |
| `trigger.warning-non-blocking` | low | no | Inline banner for low-battery, weak-wifi, suboptimal-but-allowed states. |
| `trigger.troubleshooting-escalation` | high | no | Offer escalation path after N failed self-diagnosis attempts. |
| `trigger.onboarding-branch` | medium | no | Branch onboarding when role choice is detected (admin vs user, app-paired vs local-only). |
| `trigger.contextual-visual` | medium | no | Surface a visual when component-visibility map indicates the step references a non-obvious component. |
| `trigger.cross-product-divergence` | low | no | Surface a divergence note when the procedure differs from the platform default for this product. |

## Interruption budget

- Hard interrupts: reserved for `trigger.high-risk-procedure` and
  `trigger.warning-blocking`.
- Inline reinforcement: default for all other triggers.
- A surface MUST NOT exceed two hard interrupts in a single onboarding
  session.

## Composition rules

1. Triggers are evaluated per step, not per page.
2. Triggers stack additively; a single step may fire multiple triggers.
3. The highest-intensity trigger wins the presentation contract.
4. Visual reinforcement (`trigger.contextual-visual`) is bound by the visual
   constitution; conditioning comes from `component-visibility`.

## Companion file

- [`guidance-triggers.json`](guidance-triggers.json)
