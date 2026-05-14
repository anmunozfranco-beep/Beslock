# e-Nova Selected Assets Register

## Purpose
Use this register to record the single winning asset per slot before a stable file is committed into this folder.

All previous winners are quarantined from the 2026-05-13 reset. Do not reuse them as the starting baseline for new selection.

## Reset register

| Stable filename | Slot | Current state | Winning variant | Publish target | Notes |
|---|---|---|---|---|---|
| `e-nova-hero-main` | 1 | published | reset-local-png-rebuild | `e-nova-hero-main.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-installed-context` | 2 | published | reset-local-png-rebuild | `e-nova-installed-context.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-add-admin-action` | 3 | published | reset-local-png-rebuild | `e-nova-add-admin-action.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-pin-use` | 4 | published | reset-local-png-rebuild | `e-nova-pin-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-fingerprint-use` | 5 | published | reset-local-png-rebuild | `e-nova-fingerprint-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-language-settings` | 6 | published | reset-local-png-rebuild | `e-nova-language-settings.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-app-add-device` | 7 | published | reset-local-png-rebuild | `e-nova-app-add-device.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-link-qr` | 8 | published | reset-local-png-rebuild | `e-nova-link-qr.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-troubleshoot-fingerprint` | 9 | published | reset-local-png-rebuild | `e-nova-troubleshoot-fingerprint.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-troubleshoot-app-connection` | 10 | published | reset-local-png-rebuild | `e-nova-troubleshoot-app-connection.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-downloads-docs` | 11 | published | reset-local-png-rebuild | `e-nova-downloads-docs.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-nova-edge-mechanism-reference` | 12 | planned | pending | `e-nova-edge-mechanism-reference.webp` | new reset slot; blocked until OEM edge reference or commercial lock-body selection is confirmed |

## State rule
- `planned`: no reset-era raw outputs reviewed yet
- `generated`: raw outputs exist and can be reviewed
- `selected`: one reset-era variant chosen
- `approved`: selected output passed reset validation
- `published`: stable file committed after the reset cycle, not from the quarantined legacy batch