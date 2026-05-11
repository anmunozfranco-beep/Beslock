# e-Touch Image Generation Matrix

## Purpose
This is the canonical e-Touch matrix inside the operational visual system.

It migrates the legacy flat planning sheet into the product-local control surface and adds the fields needed by the upgraded workflow:
- realism class
- prompt module references
- product-truth constraints
- direct status alignment with `image-production-status.md`

## Matrix

| ID | Filename | Page / Use | Class | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|
| IMG-001 | `e-touch-hero-main` | `/productos/e-touch` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | preserve the round roses, handle numerals, and handle-base sensor |
| IMG-002 | `e-touch-installed-context` | `/productos/e-touch/primeros-pasos` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | keep the minimalist round-rose lever identity visible in context |
| IMG-003 | `e-touch-add-admin-action` | `/productos/e-touch/usuarios/agregar-administrador` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | alta | planned | use the numeral area on the handle, not a fake front panel |
| IMG-004 | `e-touch-pin-use` | `/productos/e-touch/uso/pin` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | alta | planned | numerals belong on the handle body itself |
| IMG-005 | `e-touch-fingerprint-use` | `/productos/e-touch/uso/huella` | realistic | visual profile + fingerprint interaction + documentary style + lighting | alta | planned | the sensor must stay near the exterior handle base |
| IMG-006 | `e-touch-language-settings` | `/productos/e-touch/configuracion/idioma` | hybrid | visual profile + documentary style + hybrid framing | media | planned | conditional slot; do not invent a display or front panel |
| IMG-007 | `e-touch-app-add-device` | `/productos/e-touch/app/agregar-dispositivo` | realistic | visual profile + app pairing + documentary style + app framing | alta | planned | phone is secondary to product identity |
| IMG-008 | `e-touch-link-qr` | `/productos/e-touch/app/vincular-por-qr` | realistic | visual profile + qr pairing + documentary style + app framing | media | planned | conditional slot; QR is contextual only |
| IMG-009 | `e-touch-troubleshoot-fingerprint` | `/productos/e-touch/solucion-de-problemas/no-reconoce-huella` | semi-realistic | visual profile + fingerprint interaction + troubleshooting | alta | planned | keep the handle-base sensor clearly visible |
| IMG-010 | `e-touch-troubleshoot-app-connection` | `/productos/e-touch/solucion-de-problemas/no-conecta-a-la-app` | semi-realistic | visual profile + troubleshooting + app pairing | media | planned | do not let the phone obscure the round-rose handle geometry |
| IMG-011 | `e-touch-downloads-docs` | `descargas / documentación` | hybrid | visual profile + documentary style + editorial still-life framing | baja | planned | preserve e-Touch identity even in editorial support imagery |

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
5. IMG-004

## Conditional slots
- IMG-006 `e-touch-language-settings`
- IMG-008 `e-touch-link-qr`

These remain planned but should not move into production until the feature flow is confirmed in the real product or validated documentation.

## Legacy compatibility note
The root-level files remain useful historical planning inputs:
- `../../../e-Touch - AI image prompts.md`
- `../../../e-Touch - image generation matrix.md`

For new production work, this file is now the operational source of truth for e-Touch.
