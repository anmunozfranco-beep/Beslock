# e-Prime AI Image Prompts

## Purpose
This is the canonical e-Prime prompt pack inside the reset manual-imagery system.

All new work in this file follows `../../shared/visual-rules/manual-image-reset-policy.md`.
Use only `schematic` or `hybrid` classes, treat exterior/interior/edge as separate views, and allow human presence only as a hand silhouette when a contact cue is essential.

## Reference basis
- Use the isolated transparent PNG reference in `../../../ext-images/` as the geometry anchor for every new composition.
- Build this cycle from zero; do not inherit crops, overlays, or framing from older generated outputs.
- Re-check the product visual profile before changing handle, keypad, sensor, or interior relationships.

## Shared negative base
marketing glamor, cinematic drama, photorealistic lifestyle staging, full human figure, human face, body-led scene, invented UI text, fake labels, wrong geometry, mixed interior and exterior hardware in one frame, wrong lock-edge mechanism, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

## Prompt pack

### 1. e-prime-hero-main
- Class: hybrid
- View side: exterior
- Format: 16:9 horizontal
- Use: hub principal y referencia exterior
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: exterior-full
- Prompt:
  ilustracion hibrida tecnica de la cara exterior de e-Prime instalada en una puerta, placa larga muy esbelta, area de control superior, manija centrada con aro azul en el cubo y ovalo inferior visible, sin personas
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 2. e-prime-installed-context
- Class: hybrid
- View side: interior
- Format: 4:3 horizontal
- Use: primeros pasos con vista interior instalada
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: interior-full
- Prompt:
  ilustracion hibrida tecnica de la cara interior de e-Prime instalada, placa interior esbelta con area mecanica inferior visible, sin mostrar la cara exterior en el mismo cuadro
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 3. e-prime-add-admin-action
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: agregar administrador
- Modules: visual profile + interaction module + hybrid framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico hibrido de alta de administrador en e-Prime con silueta de dedo acercandose al area superior de control, manteniendo visible el aro azul del cubo de la manija
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 4. e-prime-pin-use
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: uso de PIN o password
- Modules: visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico esquematico de PIN en e-Prime centrado en el area superior de control, sin secuencias legibles y manteniendo la identidad de placa esbelta
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 5. e-prime-fingerprint-use
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: uso de huella
- Modules: visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico hibrido de uso de huella en e-Prime con silueta de dedo sobre la zona del cubo de la manija exterior, aro azul visible y placa esbelta reconocible
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 6. e-prime-language-settings
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: ajustes o idioma
- Modules: visual profile + schematic controls + manual-image-reset-policy
- Product slice: control-zone
- Prompt:
  grafico esquematico de ajustes o idioma en e-Prime usando las zonas reales de control del exterior, sin menus falsos y sin personas
- Negative prompt:
  photorealistic people, fake UI proof, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 7. e-prime-app-add-device
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: alta de dispositivo en app
- Modules: visual profile + app pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Prime exterior con smartphone simplificado para alta en app, telefono secundario al producto y sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 8. e-prime-link-qr
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: vinculacion por QR
- Modules: visual profile + qr pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Prime exterior con smartphone simplificado y QR contextual, sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 9. e-prime-troubleshoot-fingerprint
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: troubleshooting de huella
- Modules: visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico esquematico de diagnostico del sensor en el cubo de la manija de e-Prime, con silueta de dedo opcional y foco en la zona correcta
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 10. e-prime-troubleshoot-app-connection
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: troubleshooting de app
- Modules: visual profile + troubleshooting + app pairing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de revision de conectividad entre e-Prime y smartphone simplificado, sin tapar la geometria esbelta
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 11. e-prime-downloads-docs
- Class: hybrid
- View side: neutral
- Format: 16:9 horizontal
- Use: descargas y documentacion
- Modules: visual profile + editorial still-life + hybrid framing + manual-image-reset-policy
- Product slice: product-plus-document
- Prompt:
  composicion hibrida de e-Prime con documentacion tecnica, manteniendo visible la placa esbelta, el aro del cubo y el ovalo inferior
- Negative prompt:
  corporate brochure styling, mixed hardware sides, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

### 12. e-prime-edge-mechanism-reference
- Class: schematic
- View side: edge
- Format: 4:3 horizontal
- Use: referencia del mecanismo de canto
- Modules: visual profile + product-truth policy + manual-image-reset-policy
- Product slice: edge-mechanism
- Prompt:
  grafico esquematico tecnico del canto de puerta de e-Prime basado en la guia OEM corta: cuerpo de cerradura, pestillo, eje cuadrado y familia de mecanismo coherentes en todo el paquete
- Negative prompt:
  invented lock body, mixed latch family, decorative cutaway fiction, knob silhouette, camera cluster, face-recognition screen, thick e-Flex-like plate, fingerprint sensor on handle tip, missing lower oval insert

## Reset-first generation order
1. IMG-012
2. IMG-001
3. IMG-002
4. IMG-005
5. IMG-003

## Conditional or gated slots
- IMG-008 `e-prime-link-qr`

## Notes
- Do not reuse any legacy published winner as a prompt baseline for the reset cycle.
- Keep exterior, interior, and edge imagery separated into distinct frames.
- Add labels, arrows, and numbered callouts later in editorial composition rather than inside the generated image.
