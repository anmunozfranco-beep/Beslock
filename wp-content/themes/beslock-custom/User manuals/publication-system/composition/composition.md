# Publication Composition Model

Seven publication types (user-manual, onboarding-guide, troubleshooting-guide, quick-start-guide, installation-guide, operational-faq, support-knowledge-article) with required sections and trust tier requirements.

## Publication types

- `user-manual` — audience: end-user; tier: trusted; required sections: overview, safety-warnings, installation-summary, operation, maintenance, troubleshooting-quickref, support
- `onboarding-guide` — audience: end-user; tier: trusted; required sections: welcome, prerequisites, first-use-flow, key-warnings, where-to-go-next
- `troubleshooting-guide` — audience: end-user; tier: trusted; required sections: symptom-index, diagnostic-tree, remediation-steps, escalation-criteria, support-contact
- `quick-start-guide` — audience: end-user; tier: trusted; required sections: unbox, minimal-setup, first-action, safety-callouts
- `installation-guide` — audience: installer; tier: trusted; required sections: site-requirements, tooling, stepwise-procedure, verification, handoff-checklist
- `operational-faq` — audience: end-user; tier: trusted-or-elevated-candidate; required sections: question, answer, related-procedures, confidence-band
- `support-knowledge-article` — audience: support-agent; tier: trusted-or-elevated-candidate; required sections: scenario, diagnosis, resolution, escalation-path, internal-notes

## Composition rules

- every publication is composed from knowledge-core nodes; no free-text injection by the renderer
- every required section is present or the publication is rejected at validation
- candidate-tier nodes MAY appear only when explicitly elevated by reviewer-of-scope and disclosed in the publication
- no publication mixes products without explicit cross-product manifest
- no publication compresses safety warnings; warnings render verbatim from source
- section order is governance-declared; renderer MUST NOT reorder
