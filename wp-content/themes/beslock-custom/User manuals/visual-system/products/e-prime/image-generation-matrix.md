# e-Prime Image Generation Matrix

## Purpose
This is the canonical e-Prime matrix inside the operational visual system.

It migrates the legacy flat planning sheet into the product-local control surface and adds the fields needed by the upgraded workflow:
- realism class
- prompt module references
- product-truth constraints
- direct status alignment with `image-production-status.md`

## Matrix

| ID | Filename | Page / Use | Class | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|
| IMG-001 | `e-prime-hero-main` | `/productos/e-prime` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | preserve the slim plate, lever-hub ring, and lower oval insert |
| IMG-002 | `e-prime-installed-context` | `/productos/e-prime/primeros-pasos` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | keep the installed slim long-plate identity visible in context |
| IMG-003 | `e-prime-add-admin-action` | `/productos/e-prime/usuarios/agregar-administrador` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | alta | planned | use the upper control area while keeping the hub ring visible |
| IMG-004 | `e-prime-pin-use` | `/productos/e-prime/uso/pin` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | media | planned | keypad digits are contextual only |
| IMG-005 | `e-prime-fingerprint-use` | `/productos/e-prime/uso/huella` | realistic | visual profile + fingerprint interaction + documentary style + lighting | alta | planned | the sensor must stay at the lever hub |
| IMG-006 | `e-prime-language-settings` | `/productos/e-prime/configuracion/idioma` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | alta | planned | configuration scene must not depend on generated text |
| IMG-007 | `e-prime-app-add-device` | `/productos/e-prime/app/agregar-dispositivo` | realistic | visual profile + app pairing + documentary style + app framing | alta | planned | phone is secondary to product identity |
| IMG-008 | `e-prime-link-qr` | `/productos/e-prime/app/vincular-por-qr` | realistic | visual profile + qr pairing + documentary style + app framing | media | planned | QR is contextual only, not technical proof |
| IMG-009 | `e-prime-troubleshoot-fingerprint` | `/productos/e-prime/solucion-de-problemas/no-reconoce-huella` | semi-realistic | visual profile + fingerprint interaction + troubleshooting | media | planned | keep the hub-ring sensor visible in the failure scene |
| IMG-010 | `e-prime-troubleshoot-app-connection` | `/productos/e-prime/solucion-de-problemas/no-conecta-a-la-app` | semi-realistic | visual profile + troubleshooting + app pairing | media | planned | do not let the phone obscure the slim long-plate geometry |
| IMG-011 | `e-prime-downloads-docs` | `descargas / documentación` | hybrid | visual profile + documentary style + editorial still-life framing | baja | planned | preserve e-Prime identity even in editorial support imagery |

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
- `../../../e-Prime - AI image prompts.md`
- `../../../e-Prime - image generation matrix.md`

For new production work, this file is now the operational source of truth for e-Prime.
