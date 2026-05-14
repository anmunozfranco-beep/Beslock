# Publication Lineage & Traceability

Six lineage facets (provenance traceability, source-node lineage, confidence disclosure, reviewer attribution, publication-version lineage, runtime-generation auditability). Lineage is mandatory and immutable.

## Facets

- `provenance-traceability` — guarantee: every published section traces to one or more knowledge-core source nodes by id
- `source-node-lineage` — guarantee: source nodes carry trust-tier + last-promotion timestamp at publication time
- `confidence-disclosure` — guarantee: publication exposes the confidence band of its weakest contributing section
- `reviewer-attribution` — guarantee: promotion of any contributing candidate node is attributed to a named reviewer-of-scope
- `publication-version-lineage` — guarantee: each publication carries a version id + the manifest hash of its assembly inputs
- `runtime-generation-auditability` — guarantee: publications assembled at runtime emit an assembly receipt referencing inputs, audience, and format

## Lineage rules

- lineage is mandatory; a publication missing any facet is invalid
- lineage is immutable post-publication; corrections produce a new version, never a silent edit
- assembly receipts are sandbox-tier in pilot phase (layer 25, layer 28) and promoted with the publication
- no lineage facet may be omitted by audience filter; only its rendering may vary
- lineage MUST link forward to revocation: revocation of a contributing node SHALL flag dependent publications
