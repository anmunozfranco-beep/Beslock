# e-Touch Selected Assets Register

## Purpose
Use this register to record the single winning asset per slot before a stable file is committed into this folder.

All previous winners are quarantined from the 2026-05-13 reset. Do not reuse them as the starting baseline for new selection.

## Reset register

| Stable filename | Slot | Current state | Winning variant | Publish target | Notes |
|---|---|---|---|---|---|
| `e-touch-hero-main` | 1 | published | reset-local-png-rebuild | `e-touch-hero-main.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-installed-context` | 2 | published | reset-local-png-rebuild | `e-touch-installed-context.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-add-admin-action` | 3 | published | reset-local-png-rebuild | `e-touch-add-admin-action.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-pin-use` | 4 | published | reset-local-png-rebuild | `e-touch-pin-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-fingerprint-use` | 5 | published | reset-local-png-rebuild | `e-touch-fingerprint-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-language-settings` | 6 | published | reset-local-png-rebuild | `e-touch-language-settings.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-app-add-device` | 7 | published | reset-local-png-rebuild | `e-touch-app-add-device.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-link-qr` | 8 | published | reset-local-png-rebuild | `e-touch-link-qr.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-troubleshoot-fingerprint` | 9 | published | reset-local-png-rebuild | `e-touch-troubleshoot-fingerprint.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-troubleshoot-app-connection` | 10 | published | reset-local-png-rebuild | `e-touch-troubleshoot-app-connection.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-downloads-docs` | 11 | published | reset-local-png-rebuild | `e-touch-downloads-docs.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-touch-edge-mechanism-reference` | 12 | planned | pending | `e-touch-edge-mechanism-reference.webp` | new reset slot; use it to lock the mechanism family before broader production |

## State rule
- `planned`: no reset-era raw outputs reviewed yet
- `generated`: raw outputs exist and can be reviewed
- `selected`: one reset-era variant chosen
- `approved`: selected output passed reset validation
- `published`: stable file committed after the reset cycle, not from the quarantined legacy batch