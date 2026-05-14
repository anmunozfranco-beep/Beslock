# Controlled production activation

Production activation is APPEND-ONLY across an explicit lifecycle:
production-candidate → production-approved → production-active → superseded;
rollback-candidate is observable from any pre-superseded state.
No silent production replacement. No overwrite semantics.
