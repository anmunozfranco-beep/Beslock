# e-Orbit Image Generation Matrix

## Purpose
This is the canonical e-Orbit matrix inside the reset manual-imagery system.

It rebuilds the slot plan from zero under the 2026-05-13 schematic or hybrid reset and adds view-side control so exterior, interior, and edge hardware are no longer mixed.

## Matrix

| ID | Filename | Page / Use | Class | View side | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|---|
| IMG-001 | `e-orbit-hero-main` | /productos/e-orbit | hybrid | exterior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | keep upper sensor cluster, front panel, and sculpted exterior handle visible on the exterior only |
| IMG-002 | `e-orbit-installed-context` | /productos/e-orbit/primeros-pasos | hybrid | interior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | show only the interior screen-plus-thumbturn relationship |
| IMG-003 | `e-orbit-add-admin-action` | /productos/e-orbit/usuarios/agregar-administrador | hybrid | exterior | visual profile + interaction module + hybrid framing + manual-image-reset-policy | alta | planned | keep keypad and handle as distinct zones and use hand silhouette only |
| IMG-004 | `e-orbit-pin-use` | /productos/e-orbit/uso/pin | schematic | exterior | visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy | media | planned | keypad numerals stay structural; never rely on a literal code |
| IMG-005 | `e-orbit-fingerprint-use` | /productos/e-orbit/uso/huella | hybrid | exterior | visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy | alta | planned | the sensor must stay on the upper exterior handle |
| IMG-006 | `e-orbit-language-settings` | /productos/e-orbit/configuracion/idioma | schematic | exterior | visual profile + schematic controls + manual-image-reset-policy | media | planned | use control zones only; do not use generated menus as settings proof |
| IMG-007 | `e-orbit-app-add-device` | /productos/e-orbit/app/agregar-dispositivo | hybrid | exterior | visual profile + app pairing + hybrid framing + manual-image-reset-policy | alta | planned | phone is secondary to product identity and Smart Life or Tuya context |
| IMG-008 | `e-orbit-link-qr` | /productos/e-orbit/app/vincular-por-qr | hybrid | exterior | visual profile + qr pairing + hybrid framing + manual-image-reset-policy | media | planned | QR is contextual only, not technical proof |
| IMG-009 | `e-orbit-troubleshoot-fingerprint` | /productos/e-orbit/solucion-de-problemas/no-reconoce-huella | schematic | exterior | visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy | media | planned | keep the handle-top sensor visible in the failure view |
| IMG-010 | `e-orbit-troubleshoot-app-connection` | /productos/e-orbit/solucion-de-problemas/no-conecta-a-la-app | hybrid | exterior | visual profile + troubleshooting + app pairing + manual-image-reset-policy | media | planned | do not let the phone dominate or obscure the lock geometry |
| IMG-011 | `e-orbit-downloads-docs` | descargas / documentacion | hybrid | neutral | visual profile + editorial still-life + hybrid framing + manual-image-reset-policy | baja | planned | preserve e-Orbit identity even in support imagery |
| IMG-012 | `e-orbit-edge-mechanism-reference` | /productos/e-orbit/instalacion/mecanismo-de-canto | schematic | edge | visual profile + product-truth policy + manual-image-reset-policy | alta | planned | blocked until the commercial lock-body family is confirmed |

## Production logic
- Start the reset cycle from zero; ignore previous selected or published winners when forming new prompts.
- Review against `visual-validation.md`, `../../shared/generation-guides/review-checklist.md`, and `../../shared/visual-rules/manual-image-reset-policy.md`.
- Keep every slot in `planned` until new reset-era raw outputs exist.
- Promote a slot only after it passes side separation, mechanism consistency, and no-full-human checks.

## Reset-first wave
1. IMG-001
2. IMG-002
3. IMG-005
4. IMG-007
5. IMG-003

## Blocked technical slots
- IMG-012 `e-orbit-edge-mechanism-reference`

## Legacy compatibility note
The flat root-level files remain as historical context only. Use `ext-images/e-orbit/visual-system/` for all new work.
