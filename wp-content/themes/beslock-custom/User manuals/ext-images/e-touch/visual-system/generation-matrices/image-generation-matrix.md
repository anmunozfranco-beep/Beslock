# e-Touch Image Generation Matrix

## Purpose
This is the canonical e-Touch matrix inside the reset manual-imagery system.

It rebuilds the slot plan from zero under the 2026-05-13 schematic or hybrid reset and adds view-side control so exterior, interior, and edge hardware are no longer mixed.

## Matrix

| ID | Filename | Page / Use | Class | View side | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|---|
| IMG-001 | `e-touch-hero-main` | /productos/e-touch | hybrid | exterior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | preserve round roses, handle numerals, and handle-base sensor on the exterior only |
| IMG-002 | `e-touch-installed-context` | /productos/e-touch/primeros-pasos | hybrid | interior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | show the cleaner interior handle only, never both sides together |
| IMG-003 | `e-touch-add-admin-action` | /productos/e-touch/usuarios/agregar-administrador | hybrid | exterior | visual profile + interaction module + hybrid framing + manual-image-reset-policy | alta | planned | use the numeral area on the handle; no fake front panel |
| IMG-004 | `e-touch-pin-use` | /productos/e-touch/uso/pin | schematic | exterior | visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy | media | planned | numerals belong on the handle body itself and must remain visible |
| IMG-005 | `e-touch-fingerprint-use` | /productos/e-touch/uso/huella | hybrid | exterior | visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy | alta | planned | the sensor must stay near the exterior handle base |
| IMG-006 | `e-touch-language-settings` | /productos/e-touch/configuracion/idioma | schematic | exterior | visual profile + schematic controls + manual-image-reset-policy | media | planned | conditional slot; keep integrated handle numerals visible and do not invent a display |
| IMG-007 | `e-touch-app-add-device` | /productos/e-touch/app/agregar-dispositivo | hybrid | exterior | visual profile + app pairing + hybrid framing + manual-image-reset-policy | alta | planned | phone is secondary to product identity |
| IMG-008 | `e-touch-link-qr` | /productos/e-touch/app/vincular-por-qr | hybrid | exterior | visual profile + qr pairing + hybrid framing + manual-image-reset-policy | media | planned | conditional slot; QR is contextual only |
| IMG-009 | `e-touch-troubleshoot-fingerprint` | /productos/e-touch/solucion-de-problemas/no-reconoce-huella | schematic | exterior | visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy | media | planned | keep the handle-base sensor clearly visible |
| IMG-010 | `e-touch-troubleshoot-app-connection` | /productos/e-touch/solucion-de-problemas/no-conecta-a-la-app | hybrid | exterior | visual profile + troubleshooting + app pairing + manual-image-reset-policy | media | planned | do not let the phone obscure round-rose geometry |
| IMG-011 | `e-touch-downloads-docs` | descargas / documentacion | hybrid | neutral | visual profile + editorial still-life + hybrid framing + manual-image-reset-policy | baja | planned | preserve e-Touch identity even in support imagery |
| IMG-012 | `e-touch-edge-mechanism-reference` | /productos/e-touch/instalacion/mecanismo-de-canto | schematic | edge | visual profile + product-truth policy + manual-image-reset-policy | alta | planned | fix the deadbolt family from the OEM reference and keep it unchanged across the set |

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
- IMG-006 `e-touch-language-settings`
- IMG-008 `e-touch-link-qr`

## Legacy compatibility note
The flat root-level files remain as historical context only. Use `visual-system/products/e-touch/` for all new work.
