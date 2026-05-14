# e-Nova Image Generation Matrix

## Purpose
This is the canonical e-Nova matrix inside the reset manual-imagery system.

It rebuilds the slot plan from zero under the 2026-05-13 schematic or hybrid reset and adds view-side control so exterior, interior, and edge hardware are no longer mixed.

## Matrix

| ID | Filename | Page / Use | Class | View side | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|---|
| IMG-001 | `e-nova-hero-main` | /productos/e-nova | hybrid | exterior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | preserve the compact knob family and centered face sensor on the exterior only |
| IMG-002 | `e-nova-installed-context` | /productos/e-nova/primeros-pasos | hybrid | interior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | show only the interior knob and thumbturn relationship, never both sides together |
| IMG-003 | `e-nova-add-admin-action` | /productos/e-nova/usuarios/agregar-administrador | hybrid | exterior | visual profile + interaction module + hybrid framing + manual-image-reset-policy | alta | planned | use knob-face interaction only; never invent a keypad slab |
| IMG-004 | `e-nova-pin-use` | /productos/e-nova/uso/pin | schematic | exterior | visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy | media | planned | conditional slot; explain credential logic without fabricating hardware |
| IMG-005 | `e-nova-fingerprint-use` | /productos/e-nova/uso/huella | hybrid | exterior | visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy | alta | planned | the sensor must stay centered on the exterior knob face |
| IMG-006 | `e-nova-language-settings` | /productos/e-nova/configuracion/idioma | schematic | exterior | visual profile + schematic controls + manual-image-reset-policy | media | planned | conditional slot; do not invent a screen or front display |
| IMG-007 | `e-nova-app-add-device` | /productos/e-nova/app/agregar-dispositivo | hybrid | exterior | visual profile + app pairing + hybrid framing + manual-image-reset-policy | alta | planned | phone is secondary to the compact knob identity |
| IMG-008 | `e-nova-link-qr` | /productos/e-nova/app/vincular-por-qr | hybrid | exterior | visual profile + qr pairing + hybrid framing + manual-image-reset-policy | media | planned | conditional slot; QR is contextual only |
| IMG-009 | `e-nova-troubleshoot-fingerprint` | /productos/e-nova/solucion-de-problemas/no-reconoce-huella | schematic | exterior | visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy | media | planned | keep the compact knob and centered sensor clearly visible |
| IMG-010 | `e-nova-troubleshoot-app-connection` | /productos/e-nova/solucion-de-problemas/no-conecta-a-la-app | hybrid | exterior | visual profile + troubleshooting + app pairing + manual-image-reset-policy | media | planned | do not let the phone obscure knob geometry |
| IMG-011 | `e-nova-downloads-docs` | descargas / documentacion | hybrid | neutral | visual profile + editorial still-life + hybrid framing + manual-image-reset-policy | baja | planned | preserve e-Nova identity even in support imagery |
| IMG-012 | `e-nova-edge-mechanism-reference` | /productos/e-nova/instalacion/mecanismo-de-canto | schematic | edge | visual profile + product-truth policy + manual-image-reset-policy | alta | planned | blocked until OEM edge mechanism reference exists |

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

## Conditional slots
- IMG-004 `e-nova-pin-use`
- IMG-006 `e-nova-language-settings`
- IMG-008 `e-nova-link-qr`

## Blocked technical slots
- IMG-012 `e-nova-edge-mechanism-reference`

## Legacy compatibility note
The flat root-level files remain as historical context only. Use `visual-system/products/e-nova/` for all new work.
