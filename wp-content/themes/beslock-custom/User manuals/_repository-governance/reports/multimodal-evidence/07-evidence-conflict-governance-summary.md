# 7 — Evidence conflict governance

- **conflict_kind_count**: 6
- **blocking_kinds**: ["visual-inconsistencies", "firmware-publication-drift"]
- **policy**: ["Higher trust tier wins.", "On equal trust tier: most recent reviewer-validated artefact wins.", "On equal trust tier and equal validation date: ESCALATE — block publication.", "Visual inconsistencies BLOCK publication of the bound procedure until resolved.", "Firmware/publication drift BLOCKS publication of affected entries.", "Outdated-evidence transitions to 'superseded' via lineage, never silent overwrite."]
- **escalation_required_when_unresolvable**: true
