# e-Orbit Selected Assets Register

## Purpose
Use this register to record the single winning asset per slot before a stable file is committed into this folder.

All previous winners are quarantined from the 2026-05-13 reset. Do not reuse them as the starting baseline for new selection.

## Reset register

| Stable filename | Slot | Asset ID | Current state | Winning variant | Validation status | Publish target | Notes |
|---|---|---|---|---|---|---|---|
| `e-orbit-hero-main` | 1 | IMG-001 | published | reset-local-png-rebuild | approved | `e-orbit-hero-main.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-installed-context` | 2 | IMG-002 | published | reset-local-png-rebuild | approved | `e-orbit-installed-context.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-add-admin-action` | 3 | IMG-003 | published | reset-local-png-rebuild | approved | `e-orbit-add-admin-action.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-pin-use` | 4 | IMG-004 | published | reset-local-png-rebuild | approved | `e-orbit-pin-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-fingerprint-use` | 5 | IMG-005 | published | reset-local-png-rebuild | approved | `e-orbit-fingerprint-use.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-language-settings` | 6 | IMG-006 | published | reset-local-png-rebuild | approved | `e-orbit-language-settings.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-app-add-device` | 7 | IMG-007 | published | reset-local-png-rebuild | approved | `e-orbit-app-add-device.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-link-qr` | 8 | IMG-008 | published | reset-local-png-rebuild | approved | `e-orbit-link-qr.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-troubleshoot-fingerprint` | 9 | IMG-009 | published | reset-local-png-rebuild | approved | `e-orbit-troubleshoot-fingerprint.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-troubleshoot-app-connection` | 10 | IMG-010 | published | reset-local-png-rebuild | approved | `e-orbit-troubleshoot-app-connection.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-downloads-docs` | 11 | IMG-011 | published | reset-local-png-rebuild | approved | `e-orbit-downloads-docs.webp` | reset baseline; ignore any previous published winner for this slot |
| `e-orbit-edge-mechanism-reference` | 12 | IMG-012 | planned | pending | pending | `e-orbit-edge-mechanism-reference.webp` | new reset slot; blocked until OEM edge reference or commercial lock-body selection is confirmed |

## State rule
- `planned`: no reset-era raw outputs reviewed yet
- `generated`: raw outputs exist and can be reviewed
- `selected`: one reset-era variant chosen
- `approved`: selected output passed reset validation
- `published`: stable file committed after the reset cycle, not from the quarantined legacy batch