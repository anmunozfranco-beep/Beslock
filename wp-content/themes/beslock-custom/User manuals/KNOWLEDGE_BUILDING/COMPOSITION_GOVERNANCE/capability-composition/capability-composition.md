# Capability-Based Assembly

| id | primitives_query |
|---|---|
| fingerprint-management | entities=fingerprint-sensor + procedures matching enrol/delete fingerprint + warnings scoped to fingerprint |
| app-pairing | workflows surface=mobile-app + terminology(2.4G, TUYA APP) + warnings(network) |
| remote-unlock | capability(remote-unlock) + procedures + warnings + connectivity-prereqs |
| emergency-recovery | procedures(factory-reset, emergency-power) + warnings(safety-critical) + guidance-trigger(hard-interrupt) |
| battery-management | procedures(battery-replacement) + warnings(low-battery) + specifications(battery) |
| administrator-control | workflows(administrator-setup, user-enrolment) + capability(admin) + warnings(privilege) |

## Rules

- Capability assemblies are document-agnostic; they query the knowledge-core by semantic predicate, not by source file.
- A capability assembly MUST resolve in every product where the capability is declared; absent capabilities are reported as gaps.
- Capability assemblies attach the union of warnings, prerequisites, and visual references across constituent primitives.
- Capability ids are stable across products; per-product specialisation lives in the knowledge-core, not in the capability id.
