# e-Orbit
## Implementation starter pack for content and AI-generated images

## 1. Objective
This document connects the initial implementation of the e-Orbit help center with the first batch of AI-generated images.

It is intended to help with:
- MVP Phase 1 implementation
- content and image coordination
- file naming and organization
- prioritization of visual assets
- integration planning in CMS or frontend

---

## 2. Priority pages for Phase 1
Initial implementation should prioritize these pages:

- `/productos/e-orbit`
- `/productos/e-orbit/primeros-pasos`
- `/productos/e-orbit/usuarios/agregar-administrador`
- `/productos/e-orbit/usuarios/agregar-usuario`
- `/productos/e-orbit/uso/pin`
- `/productos/e-orbit/uso/huella`
- `/productos/e-orbit/configuracion/idioma`
- `/productos/e-orbit/app/agregar-dispositivo`
- `/productos/e-orbit/app/vincular-por-qr`
- `/productos/e-orbit/solucion-de-problemas/no-reconoce-huella`
- `/productos/e-orbit/solucion-de-problemas/no-conecta-a-la-app`

---

## 3. Priority image assets
Produce these first:

1. `e-orbit-hero-main.jpg`
2. `e-orbit-installed-context.jpg`
3. `e-orbit-add-admin-action.jpg`
4. `e-orbit-fingerprint-use.jpg`
5. `e-orbit-language-settings.jpg`
6. `e-orbit-app-add-device.jpg`
7. `e-orbit-link-qr.jpg`

Produce later:

8. `e-orbit-pin-use.jpg`
9. `e-orbit-troubleshoot-fingerprint.jpg`
10. `e-orbit-troubleshoot-app-connection.jpg`
11. `e-orbit-downloads-docs.jpg`

---

## 4. Suggested asset-to-page mapping

### Hub
- page: `/productos/e-orbit`
- main image: `e-orbit-hero-main.jpg`

### First steps
- page: `/productos/e-orbit/primeros-pasos`
- main image: `e-orbit-installed-context.jpg`

### Add administrator
- page: `/productos/e-orbit/usuarios/agregar-administrador`
- main image: `e-orbit-add-admin-action.jpg`

### PIN
- page: `/productos/e-orbit/uso/pin`
- main image: `e-orbit-pin-use.jpg`

### Fingerprint
- page: `/productos/e-orbit/uso/huella`
- main image: `e-orbit-fingerprint-use.jpg`

### Language
- page: `/productos/e-orbit/configuracion/idioma`
- main image: `e-orbit-language-settings.jpg`

### Add device in app
- page: `/productos/e-orbit/app/agregar-dispositivo`
- main image: `e-orbit-app-add-device.jpg`

### Pair by QR
- page: `/productos/e-orbit/app/vincular-por-qr`
- main image: `e-orbit-link-qr.jpg`

### Fingerprint troubleshooting
- page: `/productos/e-orbit/solucion-de-problemas/no-reconoce-huella`
- main image: `e-orbit-troubleshoot-fingerprint.jpg`

### App connection troubleshooting
- page: `/productos/e-orbit/solucion-de-problemas/no-conecta-a-la-app`
- main image: `e-orbit-troubleshoot-app-connection.jpg`

---

## 5. Suggested folder organization
If the repo later stores the actual generated images, a clean structure could be:

```text
User manuals/
├── e-Orbit user manual.pdf
├── e-Orbit - image generation matrix.md
├── e-Orbit - AI image prompts.md
├── e-Orbit - implementation starter pack.md
└── assets/
    └── e-orbit/
        ├── e-orbit-hero-main.jpg
        ├── e-orbit-installed-context.jpg
        ├── e-orbit-add-admin-action.jpg
        ├── e-orbit-fingerprint-use.jpg
        ├── e-orbit-language-settings.jpg
        ├── e-orbit-app-add-device.jpg
        ├── e-orbit-link-qr.jpg
        ├── e-orbit-troubleshoot-fingerprint.jpg
        ├── e-orbit-troubleshoot-app-connection.jpg
        └── e-orbit-downloads-docs.jpg
```

---

## 6. Integration checklist
Use this checklist before connecting the images to the site:

- [ ] The file exists
- [ ] The image is visually clear
- [ ] The image matches the intended page
- [ ] The image does not depend on generated text being correct
- [ ] The crop works for the intended placement
- [ ] The file name is consistent
- [ ] The asset is optimized for web if needed

---

## 7. Suggested generation workflow

### Step 1
Generate 3 variants for each priority image.

### Step 2
Select one variant based on:
- clarity
- realism
- documentary usefulness
- consistency with the product

### Step 3
Refine chosen images if needed by changing:
- angle
- lighting
- background
- hand position
- framing

### Step 4
Export the chosen version using the final file name.

---

## 8. Implementation recommendation
Start the implementation now with:
- text content already structured
- placeholder image names already defined
- AI-generated assets produced in parallel

This allows frontend or CMS work to move without waiting for a perfect final visual package.

---

## 9. Final note
These documents are intended to support the first implementation cycle and reduce improvisation across content, design, and UI work.
