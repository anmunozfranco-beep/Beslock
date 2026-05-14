# e-Flex Selected Assets Register

## Purpose
Use this register to record the single winning asset per slot before a stable file is committed into this folder.

All previous winners are quarantined from the 2026-05-13 reset. Do not reuse them as the starting baseline for new selection.

## Reset register

| Stable filename | Slot | Current state | Winning variant | Publish target | Notes |
|---|---|---|---|---|---|
| `e-flex-hero-main` | 1 | published | reset-local-png-rebuild | `e-flex-hero-main.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-installed-context` | 2 | published | reset-local-png-rebuild | `e-flex-installed-context.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-add-admin-action` | 3 | published | reset-local-png-rebuild | `e-flex-add-admin-action.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-pin-use` | 4 | published | reset-local-png-rebuild | `e-flex-pin-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-fingerprint-use` | 5 | published | reset-local-png-rebuild | `e-flex-fingerprint-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-language-settings` | 6 | published | reset-local-png-rebuild | `e-flex-language-settings.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-app-add-device` | 7 | published | reset-local-png-rebuild | `e-flex-app-add-device.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-link-qr` | 8 | published | reset-local-png-rebuild | `e-flex-link-qr.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-troubleshoot-fingerprint` | 9 | published | reset-local-png-rebuild | `e-flex-troubleshoot-fingerprint.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-troubleshoot-app-connection` | 10 | published | reset-local-png-rebuild | `e-flex-troubleshoot-app-connection.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-downloads-docs` | 11 | published | reset-local-png-rebuild | `e-flex-downloads-docs.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-flex-edge-mechanism-reference` | 12 | planned | pending | `e-flex-edge-mechanism-reference.webp` | new reset slot; use it to lock the mechanism family before broader production |

## State rule
- `planned`: no reset-era raw outputs reviewed yet
- `generated`: raw outputs exist and can be reviewed
- `selected`: one reset-era variant chosen
- `approved`: selected output passed reset validation
- `published`: stable file committed after the reset cycle, not from the quarantined legacy batch