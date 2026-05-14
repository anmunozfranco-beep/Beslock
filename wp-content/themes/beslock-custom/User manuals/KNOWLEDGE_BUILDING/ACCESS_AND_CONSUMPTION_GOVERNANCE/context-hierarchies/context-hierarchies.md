# Hierarchies

| id | audience | knowledge_scope | exclude |
|---|---|---|---|
| beginner | first-time end-user | terminology, warnings, by-onboarding (safe-first-use) | admin-procedures, advanced-configuration |
| installer | physical installer | install, warnings, visual-intent (physical-installation), specifications | app-onboarding, advanced-configuration |
| administrator | lock administrator | administrator-setup, user-enrolment, operation, workflows | installer-only-procedures |
| troubleshooting | support-tier responder | troubleshooting, warnings, procedural-semantics | onboarding-marketing-copy |
| maintenance | owner / serviceperson | battery-replacement, factory-reset-recovery, warnings | initial-onboarding |
| advanced-configuration | power-user / integrator | all-promoted, capabilities, specifications | beginner-flows |


## Rules

- Audience scopes are declarative: an artifact may belong to multiple scopes, but inclusion is opt-in per artifact.
- Access calls without an audience scope default to the most restrictive (beginner).
- Hierarchy filters compose with access-governance filters; the stricter wins.
- Hierarchy assignment is a knowledge-center responsibility; access layer enforces, does not author.
