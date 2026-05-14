# Version Governance

## Versioned axes

| axis | scheme | scope | breaking triggers |
|---|---|---|---|
| ontology | semver | global | domain-removed, field-removed, id-format-changed |
| schema | semver | per-schema | required-field-added, field-type-changed |
| terminology | calver | global | canonical-term-renamed-without-alias |
| workflow | semver | per-product | step-reordered, step-removed, warning-removed |
| procedure | semver | per-product | safety-step-removed, input-precondition-changed |
| governance-doc | revision | per-doctrine | principle-removed, authority-area-removed |
| product-release | oem-tag | per-product | hardware-revision, firmware-major-change |

## Rules

- Every versioned artifact records: previous-version, change-type (additive/breaking/corrective), change-rationale.
- Breaking changes MUST emit a change-impact report (see TASK 7) before promotion.
- Calver applies to terminology releases (terminology drifts slowly; date-anchored audit trail preferred).
- Governance doctrine is revision-numbered, not semver — principles do not 'minor-bump'.
- Product-release versions are OEM-authoritative; the knowledge center mirrors, never invents, them.
