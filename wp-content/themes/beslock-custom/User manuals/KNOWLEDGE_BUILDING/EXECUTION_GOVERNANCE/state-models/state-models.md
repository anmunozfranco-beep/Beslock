# State Models

| id | states | initial | terminal | safe_states | unsafe_states |
|---|---|---|---|---|---|
| lock-state | locked, unlocking, unlocked, lockout | locked |  | locked, unlocked | lockout |
| pairing-state | unpaired, pairing, paired, pairing-failed | unpaired | paired | unpaired, paired | pairing-failed |
| enrollment-state | unenrolled, enrolling, enrolled, enrollment-failed | unenrolled | enrolled | unenrolled, enrolled | enrollment-failed |
| battery-state | nominal, low-battery, replacement-in-progress, restored, depleted | nominal |  | nominal, restored | depleted |
| operational-state | normal, warning, troubleshooting, recovery, blocked | normal |  | normal | blocked |
| install-state | uninstalled, mounting, wired, configured, verified-install | uninstalled | verified-install | uninstalled, verified-install |  |
| admin-state | no-admin, admin-pending, admin-set, admin-locked-out | no-admin | admin-set | no-admin, admin-set | admin-locked-out |

## Allowed transitions

| model | from | to | guard |
|---|---|---|---|
| lock-state | locked | unlocking | valid-credential-presented |
| lock-state | unlocking | unlocked | credential-accepted |
| lock-state | unlocking | locked | credential-rejected |
| lock-state | unlocked | locked | auto-relock OR manual-lock |
| lock-state | unlocking | lockout | max-failed-attempts |
| lock-state | lockout | locked | lockout-timer-elapsed OR admin-override |
| pairing-state | unpaired | pairing | pairing-mode-activated |
| pairing-state | pairing | paired | pairing-confirmed |
| pairing-state | pairing | pairing-failed | timeout OR network-error |
| pairing-state | pairing-failed | unpaired | user-acknowledged-failure |
| enrollment-state | unenrolled | enrolling | enrollment-started |
| enrollment-state | enrolling | enrolled | credential-captured-and-confirmed |
| enrollment-state | enrolling | enrollment-failed | capture-rejected OR timeout |
| enrollment-state | enrollment-failed | unenrolled | retry-acknowledged |
| battery-state | nominal | low-battery | voltage-below-threshold |
| battery-state | low-battery | replacement-in-progress | replacement-procedure-started |
| battery-state | replacement-in-progress | restored | battery-installed-and-verified |
| battery-state | low-battery | depleted | voltage-critical |
| battery-state | depleted | replacement-in-progress | emergency-power-applied OR replacement-started |
| operational-state | normal | warning | warning-trigger-fired |
| operational-state | warning | normal | warning-acknowledged-and-cleared |
| operational-state | warning | troubleshooting | symptom-observed |
| operational-state | troubleshooting | recovery | recovery-procedure-started |
| operational-state | recovery | normal | recovery-completed-and-verified |
| operational-state | troubleshooting | blocked | tier-4-or-5-required |
| install-state | uninstalled | mounting | install-procedure-started |
| install-state | mounting | wired | mechanical-mount-complete |
| install-state | wired | configured | wiring-and-power-confirmed |
| install-state | configured | verified-install | install-validation-passed |
| admin-state | no-admin | admin-pending | admin-setup-started |
| admin-state | admin-pending | admin-set | admin-credential-confirmed |
| admin-state | admin-set | admin-locked-out | admin-credential-lost OR factory-reset-required |
| admin-state | admin-locked-out | no-admin | factory-reset-completed |
