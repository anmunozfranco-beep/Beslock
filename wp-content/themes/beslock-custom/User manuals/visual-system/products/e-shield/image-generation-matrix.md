# e-Shield Image Generation Matrix

## Purpose
This is the canonical e-Shield matrix inside the operational visual system.

It migrates the legacy flat planning sheet into the product-local control surface and adds the fields needed by the upgraded workflow:
- realism class
- prompt module references
- product-truth constraints
- direct status alignment with `image-production-status.md`

## Matrix

| ID | Filename | Page / Use | Class | Prompt modules | Priority | Status | Product-truth note |
|---|---|---|---|---|---|---|---|
| IMG-001 | `e-shield-hero-main` | `/productos/e-shield` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | preserve the split-body architecture, top sensor, and keypad order |
| IMG-002 | `e-shield-installed-context` | `/productos/e-shield/primeros-pasos` | realistic | visual profile + documentary style + lighting + hero framing | alta | planned | keep the exterior slab and interior box visibly distinct in context |
| IMG-003 | `e-shield-add-admin-action` | `/productos/e-shield/usuarios/agregar-administrador` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | alta | planned | use the keypad on the exterior slab |
| IMG-004 | `e-shield-pin-use` | `/productos/e-shield/uso/pin` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | media | planned | keypad digits are contextual only |
| IMG-005 | `e-shield-fingerprint-use` | `/productos/e-shield/uso/huella` | realistic | visual profile + fingerprint interaction + documentary style + lighting | alta | planned | the sensor must stay above the keypad on the exterior slab |
| IMG-006 | `e-shield-language-settings` | `/productos/e-shield/configuracion/idioma` | semi-realistic | visual profile + keypad interaction + documentary style + interaction framing | alta | planned | configuration scene must not depend on generated text |
| IMG-007 | `e-shield-app-add-device` | `/productos/e-shield/app/agregar-dispositivo` | realistic | visual profile + app pairing + documentary style + app framing | alta | planned | phone is secondary to product identity |
| IMG-008 | `e-shield-link-qr` | `/productos/e-shield/app/vincular-por-qr` | realistic | visual profile + qr pairing + documentary style + app framing | media | planned | QR is contextual only and conditional on the real flow |
| IMG-009 | `e-shield-troubleshoot-fingerprint` | `/productos/e-shield/solucion-de-problemas/no-reconoce-huella` | semi-realistic | visual profile + fingerprint interaction + troubleshooting | media | planned | keep the top-sensor troubleshooting zone visible |
| IMG-010 | `e-shield-troubleshoot-app-connection` | `/productos/e-shield/solucion-de-problemas/no-conecta-a-la-app` | semi-realistic | visual profile + troubleshooting + app pairing | media | planned | do not let the phone obscure the exterior slab |
| IMG-011 | `e-shield-downloads-docs` | `descargas / documentación` | hybrid | visual profile + documentary style + editorial still-life framing | baja | planned | preserve e-Shield identity even in editorial support imagery |

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
- `../../../e-Shield - AI image prompts.md`
- `../../../e-Shield - image generation matrix.md`

For new production work, this file is now the operational source of truth for e-Shield.
