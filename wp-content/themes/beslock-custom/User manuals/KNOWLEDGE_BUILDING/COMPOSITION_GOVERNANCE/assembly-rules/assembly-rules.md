# Operational Assembly Rules

| id | rule |
|---|---|
| warnings-follow-procedures | Every procedure assembled into a package MUST carry the warnings scoped to it. |
| prerequisites-are-transitive | Prerequisites expand transitively up to depth 3; circular dependencies are blocking findings. |
| visual-attached-when-physical | Procedures with `surface=physical-installation` MUST attach visual-intent + component-visibility. |
| troubleshooting-pulls-recovery | Troubleshooting symptoms MUST resolve to ≥1 recovery procedure or an explicit escalation tier. |
| onboarding-pulls-guidance | Onboarding assemblies MUST attach guidance-triggers and a cognitive-load assessment per included procedure. |
| guidance-respects-budget | Onboarding interruption budget ≤ 2 hard-interrupting triggers per session. |
| safety-constraints-non-droppable | Safety-critical warnings (P0) cannot be dropped from any assembly that contains the related procedure. |
| maturity-floor-enforced | Default maturity floor `normalized`; publication packages `verified`; RAG-bound packages `canonical-knowledge`. |
| deterministic-order | Assembly ordering is deterministic: declared step-index first, then priority tier, then artifact-id. |
