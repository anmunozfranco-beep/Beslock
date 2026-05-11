# e-Flex Image Generation Matrix

## Purpose
This is the canonical e-Flex matrix inside the operational visual system.

It migrates the legacy flat planning sheet into the product-local control surface and adds the fields needed by the upgraded workflow:
- realism class
- prompt module references
- product-truth constraints
- direct status alignment with `image-production-status.md`

## Matrix

| ID | Filename | Page / Use | Class | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|
| IMG-001 | `e-flex-hero-main` | `/productos/e-flex` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | preserve the long plate, upper keypad panel, and handle-face sensor |
| IMG-002 | `e-flex-installed-context` | `/productos/e-flex/primeros-pasos` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | keep the installed long-plate lever identity visible in context |
| IMG-003 | `e-flex-add-admin-action` | `/productos/e-flex/usuarios/agregar-administrador` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | alta | planned | use the upper front panel for admin action |
| IMG-004 | `e-flex-pin-use` | `/productos/e-flex/uso/pin` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | media | planned | keypad digits are contextual only |
| IMG-005 | `e-flex-fingerprint-use` | `/productos/e-flex/uso/huella` | realistic | visual profile + fingerprint interaction + documentary style + lighting | alta | planned | the sensor must stay on the exterior handle face |
| IMG-006 | `e-flex-language-settings` | `/productos/e-flex/configuracion/idioma` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | alta | planned | configuration scene must not depend on generated text |
| IMG-007 | `e-flex-app-add-device` | `/productos/e-flex/app/agregar-dispositivo` | realistic | visual profile + app pairing + documentary style + app framing | alta | planned | phone is secondary to product identity |
| IMG-008 | `e-flex-link-qr` | `/productos/e-flex/app/vincular-por-qr` | realistic | visual profile + qr pairing + documentary style + app framing | media | planned | QR is contextual only, not technical proof |
| IMG-009 | `e-flex-troubleshoot-fingerprint` | `/productos/e-flex/solucion-de-problemas/no-reconoce-huella` | semi-realistic | visual profile + fingerprint interaction + troubleshooting | media | planned | keep the handle-face sensor visible in the failure scene |
| IMG-010 | `e-flex-troubleshoot-app-connection` | `/productos/e-flex/solucion-de-problemas/no-conecta-a-la-app` | semi-realistic | visual profile + troubleshooting + app pairing | media | planned | do not let the phone obscure the long-plate geometry |
| IMG-011 | `e-flex-downloads-docs` | `descargas / documentación` | hybrid | visual profile + documentary style + editorial still-life framing | baja | planned | preserve e-Flex identity even in editorial support imagery |

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
4. IMG-003
5. IMG-007
6. IMG-004

## Legacy compatibility note
The root-level files remain useful historical planning inputs:
- `../../../e-Flex - AI image prompts.md`
- `../../../e-Flex - image generation matrix.md`

For new production work, this file is now the operational source of truth for e-Flex.
