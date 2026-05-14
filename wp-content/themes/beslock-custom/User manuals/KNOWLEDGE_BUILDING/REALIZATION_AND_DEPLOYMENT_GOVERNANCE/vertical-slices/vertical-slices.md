# Vertical Slice Realization

Declared catalog of vertical realization slices, each with supervision posture and exit criteria.

## Slices

- `slice-A-read-only-retrieval` — candidate: contextual-retrieval — kind: first-runtime / proof-of-value
- `slice-B-procedural-assembly` — candidate: procedural-assembly-runtime — kind: second proof-of-value
- `slice-C-supervised-onboarding-pilot` — candidate: onboarding-runtime — kind: supervised pilot (gated)
- `slice-D-supervised-copilot-pilot` — candidate: operational-copilot — kind: supervised pilot (gated)
- `slice-E-troubleshooting-controlled-pilot` — candidate: troubleshooting-runtime — kind: deferred (corpus-bound)
- `slice-F-administrator-controlled-trial` — candidate: administrator-assistant — kind: deferred (destructive surface; requires OEM channel)

## Rules

- First slice MUST be read-only and have no blocking risks.
- Each slice declares supervision posture, exit criteria, and provenance requirements.
- Slices are sequenced by safety + readiness, not by value alone.
- A slice may not advance to the next staged-rollout phase until its exit criteria are satisfied with evidence.
- Deferred slices remain deferred until every declared blocking risk is resolved.
