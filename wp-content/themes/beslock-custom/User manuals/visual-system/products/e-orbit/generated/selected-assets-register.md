# e-Orbit Selected Assets Register

## Purpose
Use this register to record the single winning asset per slot before a stable file is committed into this folder.

Do not mark an entry as `published` until the selected output has passed `../visual-validation.md` and `../../shared/generation-guides/review-checklist.md`.

## Pilot wave register

| Stable filename | Slot | Asset ID | Current state | Winning variant | Validation status | Publish target | Notes |
|---|---|---|---|---|---|---|---|
| `e-orbit-hero-main` | 1 | IMG-001 | planned | pending | pending | `e-orbit-hero-main.webp` | hero anchor |
| `e-orbit-installed-context` | 2 | IMG-002 | planned | pending | pending | `e-orbit-installed-context.webp` | installed context |
| `e-orbit-fingerprint-use` | 5 | IMG-005 | planned | pending | pending | `e-orbit-fingerprint-use.webp` | handle-top sensor protected |
| `e-orbit-app-add-device` | 7 | IMG-007 | planned | pending | pending | `e-orbit-app-add-device.webp` | phone secondary to lock |
| `e-orbit-link-qr` | 8 | IMG-008 | planned | pending | pending | `e-orbit-link-qr.webp` | QR remains contextual |

## State rule
- `planned`: no raw outputs reviewed yet
- `generated`: raw outputs exist and can be reviewed
- `selected`: one winning variant chosen
- `approved`: selected output passed product and shared validation
- `published`: stable file committed in this folder

## Publishing note
Use the stable filename column as the final committed asset name.
Keep raw variants outside Git until a winner exists.