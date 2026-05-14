# e-Prime Selected Assets Register

## Purpose
Use this register to record the single winning asset per slot before a stable file is committed into this folder.

All previous winners are quarantined from the 2026-05-13 reset. Do not reuse them as the starting baseline for new selection.

## Reset register

| Stable filename | Slot | Current state | Winning variant | Publish target | Notes |
|---|---|---|---|---|---|
| `e-prime-hero-main` | 1 | published | reset-local-png-rebuild | `e-prime-hero-main.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-installed-context` | 2 | published | reset-local-png-rebuild | `e-prime-installed-context.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-add-admin-action` | 3 | published | reset-local-png-rebuild | `e-prime-add-admin-action.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-pin-use` | 4 | published | reset-local-png-rebuild | `e-prime-pin-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-fingerprint-use` | 5 | published | reset-local-png-rebuild | `e-prime-fingerprint-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-language-settings` | 6 | published | reset-local-png-rebuild | `e-prime-language-settings.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-app-add-device` | 7 | published | reset-local-png-rebuild | `e-prime-app-add-device.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-link-qr` | 8 | published | reset-local-png-rebuild | `e-prime-link-qr.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-troubleshoot-fingerprint` | 9 | published | reset-local-png-rebuild | `e-prime-troubleshoot-fingerprint.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-troubleshoot-app-connection` | 10 | published | reset-local-png-rebuild | `e-prime-troubleshoot-app-connection.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-downloads-docs` | 11 | published | reset-local-png-rebuild | `e-prime-downloads-docs.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-prime-edge-mechanism-reference` | 12 | planned | pending | `e-prime-edge-mechanism-reference.webp` | new reset slot; use it to lock the mechanism family before broader production |

## State rule
- `planned`: no reset-era raw outputs reviewed yet
- `generated`: raw outputs exist and can be reviewed
- `selected`: one reset-era variant chosen
- `approved`: selected output passed reset validation
- `published`: stable file committed after the reset cycle, not from the quarantined legacy batch