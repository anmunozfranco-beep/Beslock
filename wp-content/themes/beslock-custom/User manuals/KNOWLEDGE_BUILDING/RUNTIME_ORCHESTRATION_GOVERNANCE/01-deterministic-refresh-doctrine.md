# Deterministic refresh doctrine

Every refresh is the deterministic image of a declared change-set against the dependency-graph. No refresh runs without a recorded upstream change. Outputs are reproducible: same change-set + same governance state -> same refresh-manifest.
