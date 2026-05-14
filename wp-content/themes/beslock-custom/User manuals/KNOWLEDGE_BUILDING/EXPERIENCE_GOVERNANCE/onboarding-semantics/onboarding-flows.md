# Onboarding semantics

_Schema: `experience-governance/1.0` · onboarding flows · generated 2026-05-13T17:27:13Z._

## Flows

| ID | Label | Branch trigger | Steps | Exit state |
|---|---|---|---:|---|
| `onboarding.first-time-user` | First-time end user | `no-admin-yet OR no-companion-app` | 6 | User can unlock independently and knows recovery basics. |
| `onboarding.installation` | Installation onboarding | `physical-mount-required` | 7 | Hardware mounted and verified; ready for credential setup. |
| `onboarding.app` | App onboarding | `user-opts-into-companion-app` | 5 | Lock visible in companion app; admin can manage remotely. |
| `onboarding.admin` | Administrator onboarding | `first-admin-or-admin-handover` | 6 | Administrator fully provisioned and informed about recovery. |
| `onboarding.safe-first-use` | Safe first use | `always-after-installation` | 5 | User has been exposed to the four most common recovery scenarios before they are needed. |

## Branch policy

- Onboarding is composed of independent flows. The user enters the union of
  flows whose branch conditions hold.
- `onboarding.safe-first-use` ALWAYS runs after `onboarding.installation`
  and before any optional flow; it is non-skippable.
- `onboarding.app` is opt-in; users without app intent skip it without
  penalty.

## Safe-first-use rule

The four scenarios surfaced in `onboarding.safe-first-use` (mechanical-key
test, first-unlock test, lockout behaviour, low-battery + emergency-power)
account for the majority of avoidable support tickets. They MUST be
exposed to the user before the user is left to operate the lock alone.

## Companion file

- [`onboarding-flows.json`](onboarding-flows.json)
