# Knowledge prioritization

_Schema: `experience-governance/1.0` · knowledge priority model · generated 2026-05-13T17:27:13Z._

## Prioritization dimensions

| Dimension | Definition |
|---|---|
| `prio.operational-criticality` | How essential the knowledge is to using the lock at all. |
| `prio.user-frequency` | How often a typical user needs the knowledge. |
| `prio.support-burden` | How much support time is spent on the underlying topic. |
| `prio.failure-impact` | Consequence of getting the knowledge wrong (lockout, data-loss, hardware damage). |
| `prio.onboarding-importance` | Whether the knowledge is required for a successful first use. |
| `prio.safety-importance` | Whether the knowledge protects users or property. |

## Tiers

| Tier | Label | Rule |
|---|---|---|
| `P0` | Critical-path | Required to operate the lock or to recover from a critical failure. |
| `P1` | High-frequency | Daily-to-weekly user need. |
| `P2` | Onboarding-key | Required for safe first use even if not high-frequency afterwards. |
| `P3` | Support-driver | Drives a measurable fraction of support tickets. |
| `P4` | Reference | Read on demand; not required for daily use. |
| `P5` | Edge / advanced | Power-user or rare scenarios. |

## Assignments (canonical procedures)

| Concept | Tier |
|---|---|
| `procedure.unlock-pin` | `P0` |
| `procedure.unlock-fingerprint` | `P0` |
| `procedure.battery-replacement` | `P0` |
| `procedure.emergency-power` | `P0` |
| `procedure.add-administrator` | `P2` |
| `procedure.register-pin` | `P2` |
| `procedure.register-fingerprint` | `P2` |
| `procedure.pair-with-app` | `P2` |
| `procedure.add-user` | `P3` |
| `procedure.member-management` | `P3` |
| `procedure.firmware-update` | `P4` |
| `procedure.qr-pairing` | `P3` |
| `procedure.ez-mode-pairing` | `P3` |
| `procedure.factory-reset` | `P5` |
| `procedure.change-language` | `P4` |

## Consumer rules

- Surfaces presenting limited real-estate (chatbot card list, AR overlay,
  short SMS) MUST sort by tier ascending then by user frequency descending.
- A `P0` concept MUST always be reachable in ≤2 interactions from any
  consumer surface.
- `P5` concepts MUST be reachable, but MAY be hidden behind an "advanced"
  affordance.

## Companion file

- [`priority-assignments.json`](priority-assignments.json)
