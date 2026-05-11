# e-Nova Image Generation Matrix

## Purpose
This is the canonical e-Nova matrix inside the operational visual system.

It migrates the legacy flat planning sheet into the product-local control surface and adds the fields needed by the upgraded workflow:
- realism class
- prompt module references
- product-truth constraints
- direct status alignment with `image-production-status.md`

## Matrix

| ID | Filename | Page / Use | Class | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|
| IMG-001 | `e-nova-hero-main` | `/productos/e-nova` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | preserve the compact knob family and centered face sensor |
| IMG-002 | `e-nova-installed-context` | `/productos/e-nova/primeros-pasos` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | keep circular roses and compact proportions visible in context |
| IMG-003 | `e-nova-add-admin-action` | `/productos/e-nova/usuarios/agregar-administrador` | realistic | visual profile + fingerprint interaction + documentary style + interaction framing | alta | planned | use knob-face interaction; do not invent a flat control panel |
| IMG-004 | `e-nova-pin-use` | `/productos/e-nova/uso/pin` | hybrid | visual profile + documentary style + hybrid framing | media | planned | conditional slot; never add a keypad slab to the hardware |
| IMG-005 | `e-nova-fingerprint-use` | `/productos/e-nova/uso/huella` | realistic | visual profile + fingerprint interaction + documentary style + lighting | alta | planned | the sensor must stay centered on the exterior knob face |
| IMG-006 | `e-nova-language-settings` | `/productos/e-nova/configuracion/idioma` | hybrid | visual profile + documentary style + hybrid framing | media | planned | conditional slot; do not invent a screen or front display |
| IMG-007 | `e-nova-app-add-device` | `/productos/e-nova/app/agregar-dispositivo` | realistic | visual profile + app pairing + documentary style + app framing | alta | planned | phone is secondary to product identity |
| IMG-008 | `e-nova-link-qr` | `/productos/e-nova/app/vincular-por-qr` | realistic | visual profile + qr pairing + documentary style + app framing | media | planned | conditional slot; QR is contextual only |
| IMG-009 | `e-nova-troubleshoot-fingerprint` | `/productos/e-nova/solucion-de-problemas/no-reconoce-huella` | semi-realistic | visual profile + fingerprint interaction + troubleshooting | alta | planned | keep the compact knob and centered sensor clearly visible |
| IMG-010 | `e-nova-troubleshoot-app-connection` | `/productos/e-nova/solucion-de-problemas/no-conecta-a-la-app` | semi-realistic | visual profile + troubleshooting + app pairing | media | planned | do not let the phone obscure the knob geometry |
| IMG-011 | `e-nova-downloads-docs` | `descargas / documentación` | hybrid | visual profile + documentary style + editorial still-life framing | baja | planned | preserve e-Nova identity even in editorial support imagery |

## Production logic
- Generate 3 variants per first-wave asset.
- Review against `visual-validation.md` and `../../shared/generation-guides/review-checklist.md`.
- Move status from `planned` to `generated` only when raw outputs exist.
- Move to `selected` only after a variant wins on both clarity and product truth.
- Publish only after explicit validation.

## First-wave pilot set
1. IMG-001
2. IMG-002
3. IMG-005
4. IMG-007
5. IMG-009

## Conditional slots
- IMG-004 `e-nova-pin-use`
- IMG-006 `e-nova-language-settings`
- IMG-008 `e-nova-link-qr`

These remain planned but should not move into production until the feature flow is confirmed in the real product or validated documentation.

## Legacy compatibility note
The root-level files remain useful historical planning inputs:
- `../../../e-Nova - AI image prompts.md`
- `../../../e-Nova - image generation matrix.md`

For new production work, this file is now the operational source of truth for e-Nova.