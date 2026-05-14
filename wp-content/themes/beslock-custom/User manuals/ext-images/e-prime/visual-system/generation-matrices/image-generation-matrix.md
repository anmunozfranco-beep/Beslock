# e-Prime Image Generation Matrix

## Purpose
This is the canonical e-Prime matrix inside the reset manual-imagery system.

It rebuilds the slot plan from zero under the 2026-05-13 schematic or hybrid reset and adds view-side control so exterior, interior, and edge hardware are no longer mixed.

## Matrix

| ID | Filename | Page / Use | Class | View side | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|---|
| IMG-001 | `e-prime-hero-main` | /productos/e-prime | hybrid | exterior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | preserve the slim plate, lever-hub ring, and lower oval insert on the exterior only |
| IMG-002 | `e-prime-installed-context` | /productos/e-prime/primeros-pasos | hybrid | interior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | show only the interior plate and lower mechanical zone |
| IMG-003 | `e-prime-add-admin-action` | /productos/e-prime/usuarios/agregar-administrador | hybrid | exterior | visual profile + interaction module + hybrid framing + manual-image-reset-policy | alta | planned | use the upper control area while keeping the hub ring visible |
| IMG-004 | `e-prime-pin-use` | /productos/e-prime/uso/pin | schematic | exterior | visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy | media | planned | credential interaction stays in the upper control area |
| IMG-005 | `e-prime-fingerprint-use` | /productos/e-prime/uso/huella | hybrid | exterior | visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy | alta | planned | the sensor must stay at the lever hub |
| IMG-006 | `e-prime-language-settings` | /productos/e-prime/configuracion/idioma | schematic | exterior | visual profile + schematic controls + manual-image-reset-policy | media | planned | use real control zones only; do not invent settings menus |
| IMG-007 | `e-prime-app-add-device` | /productos/e-prime/app/agregar-dispositivo | hybrid | exterior | visual profile + app pairing + hybrid framing + manual-image-reset-policy | alta | planned | phone is secondary to product identity |
| IMG-008 | `e-prime-link-qr` | /productos/e-prime/app/vincular-por-qr | hybrid | exterior | visual profile + qr pairing + hybrid framing + manual-image-reset-policy | media | planned | QR is contextual only, not technical proof |
| IMG-009 | `e-prime-troubleshoot-fingerprint` | /productos/e-prime/solucion-de-problemas/no-reconoce-huella | schematic | exterior | visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy | media | planned | keep the hub-ring sensor visible in the failure scene |
| IMG-010 | `e-prime-troubleshoot-app-connection` | /productos/e-prime/solucion-de-problemas/no-conecta-a-la-app | hybrid | exterior | visual profile + troubleshooting + app pairing + manual-image-reset-policy | media | planned | do not let the phone obscure the slim long-plate geometry |
| IMG-011 | `e-prime-downloads-docs` | descargas / documentacion | hybrid | neutral | visual profile + editorial still-life + hybrid framing + manual-image-reset-policy | baja | planned | preserve e-Prime identity even in support imagery |
| IMG-012 | `e-prime-edge-mechanism-reference` | /productos/e-prime/instalacion/mecanismo-de-canto | schematic | edge | visual profile + product-truth policy + manual-image-reset-policy | alta | planned | fix the OEM-backed latch and spindle family before broader production |

## Production logic
- Start the reset cycle from zero; ignore previous selected or published winners when forming new prompts.
- Review against `visual-validation.md`, `../../shared/generation-guides/review-checklist.md`, and `../../shared/visual-rules/manual-image-reset-policy.md`.
- Keep every slot in `planned` until new reset-era raw outputs exist.
- Promote a slot only after it passes side separation, mechanism consistency, and no-full-human checks.

## Reset-first wave
1. IMG-012
2. IMG-001
3. IMG-002
4. IMG-005
5. IMG-003

## Conditional slots
- IMG-008 `e-prime-link-qr`

## Legacy compatibility note
The flat root-level files remain as historical context only. Use `visual-system/products/e-prime/` for all new work.
