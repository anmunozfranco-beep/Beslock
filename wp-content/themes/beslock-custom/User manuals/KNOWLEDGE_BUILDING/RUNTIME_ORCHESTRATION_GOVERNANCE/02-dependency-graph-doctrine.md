# Dependency-graph doctrine

Dependencies are declared, not inferred. The graph is the single source of truth for what is downstream of what. Any node not declared in the graph is treated as having NO dependents and MUST be reviewer-attested before being added.
