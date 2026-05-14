# Deprecation Governance

## Deprecation reasons

| id | requires successor |
|---|---|
| `superseded-by-newer-version` | True |
| `ontology-rule-change` | False |
| `oem-correction` | True |
| `evidence-retracted` | False |
| `duplicate-canonicalized-away` | True |
| `product-discontinued` | False |
| `policy-restricted` | False |

## Rules

- Deprecation is reversible until archival; archival is terminal.
- Lineage links (predecessor/successor) MUST be recorded on every transition.
- Deprecated artifacts remain readable; surfaces must render a deprecation badge.
- Superseded artifacts MUST link to their successor; orphaned supersession is a blocking debt.
- Stale terminology is deprecated, never deleted; aliases preserve historical references.
- Obsolete workflows retain ordering and warnings for forensic audit.
- Silent destruction of any semantic artifact is a governance violation.
