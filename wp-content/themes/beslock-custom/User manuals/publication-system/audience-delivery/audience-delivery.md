# Audience-Aware Delivery

Six audiences (end-user, installer, reviewer, operator, governance-maintainer, support-agent) with declared visibility profiles. Audience changes visibility only, never substance.

## Audiences

- `end-user` — vocabulary: non-technical; internal notes: False; provenance summary: True; full provenance: False; confidence band: True
- `installer` — vocabulary: trade-technical; internal notes: False; provenance summary: True; full provenance: False; confidence band: True
- `reviewer` — vocabulary: doctrine-technical; internal notes: True; provenance summary: True; full provenance: True; confidence band: True
- `operator` — vocabulary: operational; internal notes: True; provenance summary: True; full provenance: True; confidence band: True
- `governance-maintainer` — vocabulary: doctrine-technical; internal notes: True; provenance summary: True; full provenance: True; confidence band: True
- `support-agent` — vocabulary: operational; internal notes: True; provenance summary: True; full provenance: False; confidence band: True

## Audience rules

- audience filters affect VISIBILITY only; the underlying assembled publication is identical across audiences
- no audience may receive content sourced from a tier above its declared trust scope (layer 25)
- audience-aware rendering is governance-declared; no per-publication override
- PII / operator-identifying material is never rendered for end-user, installer, or support-agent audiences
- confidence band is rendered for every audience that consumes the publication
