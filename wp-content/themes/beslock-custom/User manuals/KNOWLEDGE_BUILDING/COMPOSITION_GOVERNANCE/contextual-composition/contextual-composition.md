# Contextual Composition

## Dimensions

| id | values |
|---|---|
| user-role | beginner, installer, administrator, support-tier, maintenance-operator, advanced |
| operational-stage | pre-install, install, first-use, routine-operation, maintenance, recovery |
| product-state | unconfigured, paired-app, admin-set, users-enrolled, low-battery, lockout, factory-default |
| troubleshooting-state | nominal, symptom-observed, tier1-active, tier3-escalated, vendor-escalated |
| onboarding-progress | not-started, in-progress, completed, abandoned |
| confidence-level | low, medium, high |
| maturity-level | normalized, canonicalized, verified, promoted |

## Profiles

| id | user_role | operational_stage | package | filters |
|---|---|---|---|---|
| beginner-installer | installer | install | installation-package | audience_scope=installer, maturity_floor=normalized |
| first-time-end-user | beginner | first-use | onboarding-package | audience_scope=beginner, interruption_budget=2 |
| administrator-setup | administrator | first-use | administrator-setup-package | audience_scope=administrator |
| maintenance-operator | maintenance-operator | maintenance | maintenance-package | audience_scope=maintenance |
| support-tier-troubleshoot | support-tier | recovery | troubleshooting-package | audience_scope=troubleshooting, maturity_floor=verified |
| emergency-recovery | beginner | recovery | recovery-package | audience_scope=maintenance, guidance_intensity=hard-interrupt |

## Rules

- Composition profile = (user_role, operational_stage, product_state, confidence_level, maturity_level).
- Missing dimensions default to most restrictive: beginner / pre-install / unconfigured / low / verified.
- Confidence-level=low forces an explicit confidence-warning attached to the assembled package.
- Maturity-level upgrades narrow the candidate set; downgrades require an audit reason.
- Composition is recomputed when any dimension changes; no stale composition surfaces.
