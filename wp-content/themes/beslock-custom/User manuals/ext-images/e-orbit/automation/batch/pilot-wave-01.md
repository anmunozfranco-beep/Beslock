# e-Orbit Pilot Wave 01

## Purpose
This packet prepares the first end-to-end production pilot for e-Orbit without pretending that raw outputs already exist in the repository.

The pilot scope matches the current dashboard instruction and the first-wave set defined in `../../visual-system/generation-matrices/image-generation-matrix.md`.

## Pilot scope

| Slot | Asset ID | Stable filename | Class | Why it is in the pilot |
|---|---|---|---|---|
| 1 | IMG-001 | `e-orbit-hero-main` | realistic | highest-priority product identity anchor |
| 2 | IMG-002 | `e-orbit-installed-context` | realistic | verifies installed-context readability |
| 5 | IMG-005 | `e-orbit-fingerprint-use` | realistic | protects the handle-top sensor position |
| 7 | IMG-007 | `e-orbit-app-add-device` | realistic | checks phone-plus-product balance |
| 8 | IMG-008 | `e-orbit-link-qr` | realistic | verifies contextual QR treatment without inventing proof |

## Prompt sources
- `../../visual-system/prompts/ai-image-prompts.md`
- `../../visual-system/generation-matrices/image-generation-matrix.md`
- `../../visual-system/validations/visual-validation.md`
- `pilot-wave-01-variant-pack.md`
- `../../../../visual-system/shared/generation-guides/review-checklist.md`

## Execution sequence
1. Read `../../visual-system/references/e-orbit-visual-profile.md` before generating any slot.
2. Generate 3 variants for each pilot asset outside this folder.
3. Review each variant against `../../visual-system/validations/visual-validation.md` and `../../../../visual-system/shared/generation-guides/review-checklist.md`.
4. Move slot state from `planned` to `generating` only while variants are actively being created.
5. Move slot state to `generated` only when at least one reviewable raw output exists.
6. Choose one winning variant per slot only if product truth still holds.
7. Move slot state to `selected` only after the winner is logged in `../../metadata/traceability/selected-assets-register.md`.
8. Commit the stable output in this folder only after the selected image also reaches `approved` and then `published`.

## Temporary raw-output naming rule
Do not commit temporary variants to Git.

Use the following local-only naming convention during generation and review:
- `e-orbit-hero-main__v01`
- `e-orbit-hero-main__v02`
- `e-orbit-hero-main__v03`
- repeat the same pattern for the other pilot filenames

## Per-slot review focus

| Stable filename | Protected truth | Reject when |
|---|---|---|
| `e-orbit-hero-main` | tall vertical body, upper sensor cluster, distinct handle | the result collapses into a generic keypad lock |
| `e-orbit-installed-context` | installed door context still shows the tall silhouette | the context hides the features that distinguish e-Orbit |
| `e-orbit-fingerprint-use` | fingerprint sensor stays on the upper exterior handle | the touch drifts to the front panel or another zone |
| `e-orbit-app-add-device` | phone remains secondary to lock identity | the phone dominates or the lock becomes generic |
| `e-orbit-link-qr` | QR remains contextual only | the QR is treated as technical proof or readable product truth |

## Exit criteria for a publishable pilot
- 5 pilot slots have at least one reviewed raw variant.
- Each selected winner passes all product-specific checks in `../../visual-system/validations/visual-validation.md`.
- Each selected winner passes all shared checks in `../../../../visual-system/shared/generation-guides/review-checklist.md`.
- `../../metadata/traceability/selected-assets-register.md` contains one chosen variant and one stable filename per pilot asset.
- `../../visual-system/qa/image-production-status.md` reflects the actual slot states instead of the initial planning state.

## Notes
- Because this repository does not yet contain raw generated outputs for e-Orbit, this file is a run-ready packet, not evidence that generation already happened.
- If app UI detail becomes instructional rather than contextual, replace the AI phone screen with a real capture before publication.