# e-Shield Image Generation Matrix

## Purpose
This is the canonical e-Shield matrix inside the reset manual-imagery system.

It rebuilds the slot plan from zero under the 2026-05-13 schematic or hybrid reset and adds view-side control so exterior, interior, and edge hardware are no longer mixed.

## Matrix

| ID | Filename | Page / Use | Class | View side | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|---|
| IMG-001 | `e-shield-hero-main` | /productos/e-shield | hybrid | exterior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | preserve the exterior slab, top sensor, and keypad order on the exterior only |
| IMG-002 | `e-shield-installed-context` | /productos/e-shield/primeros-pasos | hybrid | interior | visual profile + documentary style + hybrid framing + manual-image-reset-policy | alta | planned | show only the interior horizontal lock box |
| IMG-003 | `e-shield-add-admin-action` | /productos/e-shield/usuarios/agregar-administrador | hybrid | exterior | visual profile + interaction module + hybrid framing + manual-image-reset-policy | alta | planned | use the keypad on the exterior slab with hand silhouette only |
| IMG-004 | `e-shield-pin-use` | /productos/e-shield/uso/pin | schematic | exterior | visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy | media | planned | keypad numerals must be visible on the exterior slab |
| IMG-005 | `e-shield-fingerprint-use` | /productos/e-shield/uso/huella | hybrid | exterior | visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy | alta | planned | the sensor must stay above the keypad on the exterior slab |
| IMG-006 | `e-shield-language-settings` | /productos/e-shield/configuracion/idioma | schematic | exterior | visual profile + schematic controls + manual-image-reset-policy | media | planned | use the exterior slab as control anchor; do not invent settings proof |
| IMG-007 | `e-shield-app-add-device` | /productos/e-shield/app/agregar-dispositivo | hybrid | exterior | visual profile + app pairing + hybrid framing + manual-image-reset-policy | alta | planned | phone is secondary to product identity |
| IMG-008 | `e-shield-link-qr` | /productos/e-shield/app/vincular-por-qr | hybrid | exterior | visual profile + qr pairing + hybrid framing + manual-image-reset-policy | media | planned | conditional slot; QR is contextual only |
| IMG-009 | `e-shield-troubleshoot-fingerprint` | /productos/e-shield/solucion-de-problemas/no-reconoce-huella | schematic | exterior | visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy | media | planned | keep the top-sensor troubleshooting zone visible |
| IMG-010 | `e-shield-troubleshoot-app-connection` | /productos/e-shield/solucion-de-problemas/no-conecta-a-la-app | hybrid | exterior | visual profile + troubleshooting + app pairing + manual-image-reset-policy | media | planned | do not let the phone obscure the exterior slab |
| IMG-011 | `e-shield-downloads-docs` | descargas / documentacion | hybrid | neutral | visual profile + editorial still-life + hybrid framing + manual-image-reset-policy | baja | planned | preserve e-Shield identity even in support imagery |
| IMG-012 | `e-shield-edge-mechanism-reference` | /productos/e-shield/instalacion/mecanismo-de-canto | schematic | edge | visual profile + product-truth policy + manual-image-reset-policy | alta | planned | follow the OEM drilling template and rim-lock mechanism family consistently |

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
- IMG-008 `e-shield-link-qr`

## Legacy compatibility note
The flat root-level files remain as historical context only. Use `visual-system/products/e-shield/` for all new work.
