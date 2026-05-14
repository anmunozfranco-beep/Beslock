# e-Shield AI Image Prompts

## Purpose
This is the canonical e-Shield prompt pack inside the reset manual-imagery system.

All new work in this file follows `../../shared/visual-rules/manual-image-reset-policy.md`.
Use only `schematic` or `hybrid` classes, treat exterior/interior/edge as separate views, and allow human presence only as a hand silhouette when a contact cue is essential.

## Reference basis
- Use the isolated transparent PNG reference in `../../../ext-images/` as the geometry anchor for every new composition.
- Build this cycle from zero; do not inherit crops, overlays, or framing from older generated outputs.
- Re-check the product visual profile before changing handle, keypad, sensor, or interior relationships.

## Shared negative base
marketing glamor, cinematic drama, photorealistic lifestyle staging, full human figure, human face, body-led scene, invented UI text, fake labels, wrong geometry, mixed interior and exterior hardware in one frame, wrong lock-edge mechanism, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

## Prompt pack

### 1. e-shield-hero-main
- Class: hybrid
- View side: exterior
- Format: 16:9 horizontal
- Use: hub principal y referencia exterior
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: exterior-full
- Prompt:
  ilustracion hibrida tecnica de la cara exterior de e-Shield instalada en una puerta, slab vertical brillante con sensor superior y keypad debajo, sin personas y sin mostrar la caja interior
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 2. e-shield-installed-context
- Class: hybrid
- View side: interior
- Format: 4:3 horizontal
- Use: primeros pasos con vista interior instalada
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: interior-full
- Prompt:
  ilustracion hibrida tecnica de la cara interior de e-Shield instalada, caja horizontal interior y control frontal visibles, sin mostrar el slab exterior al mismo tiempo
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 3. e-shield-add-admin-action
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: agregar administrador
- Modules: visual profile + interaction module + hybrid framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico hibrido de alta de administrador en e-Shield con silueta de dedo acercandose al keypad del slab exterior, sensor superior aun reconocible
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 4. e-shield-pin-use
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: uso de PIN o password
- Modules: visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico esquematico de PIN en e-Shield centrado en el keypad del slab exterior, sin secuencias legibles y sin personas
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 5. e-shield-fingerprint-use
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: uso de huella
- Modules: visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico hibrido de uso de huella en e-Shield con silueta de dedo alineada al sensor circular por encima del keypad exterior
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 6. e-shield-language-settings
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: ajustes o idioma
- Modules: visual profile + schematic controls + manual-image-reset-policy
- Product slice: control-zone
- Prompt:
  grafico esquematico de ajustes o idioma para e-Shield usando el slab exterior como ancla de control, sin menus falsos
- Negative prompt:
  photorealistic people, fake UI proof, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 7. e-shield-app-add-device
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: alta de dispositivo en app
- Modules: visual profile + app pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Shield exterior con smartphone simplificado para alta de dispositivo, sin persona visible y con el slab dominante
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 8. e-shield-link-qr
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: vinculacion por QR
- Modules: visual profile + qr pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Shield exterior con smartphone simplificado y QR contextual, sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 9. e-shield-troubleshoot-fingerprint
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: troubleshooting de huella
- Modules: visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico esquematico de diagnostico del sensor superior en e-Shield con silueta de dedo opcional y foco en la zona correcta
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 10. e-shield-troubleshoot-app-connection
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: troubleshooting de app
- Modules: visual profile + troubleshooting + app pairing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de revision de conectividad entre e-Shield y smartphone simplificado, sin tapar el slab exterior
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 11. e-shield-downloads-docs
- Class: hybrid
- View side: neutral
- Format: 16:9 horizontal
- Use: descargas y documentacion
- Modules: visual profile + editorial still-life + hybrid framing + manual-image-reset-policy
- Product slice: product-plus-document
- Prompt:
  composicion hibrida de e-Shield con documentacion tecnica, manteniendo visible el slab exterior o la caja interior en piezas separadas, nunca ambos juntos
- Negative prompt:
  corporate brochure styling, mixed hardware sides, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

### 12. e-shield-edge-mechanism-reference
- Class: schematic
- View side: edge
- Format: 4:3 horizontal
- Use: referencia del mecanismo de canto
- Modules: visual profile + product-truth policy + manual-image-reset-policy
- Product slice: edge-mechanism
- Prompt:
  grafico esquematico tecnico del canto de puerta de e-Shield basado en la plantilla OEM y el setback de 60 mm, manteniendo una sola familia de cerrojo de rim-lock para todo el paquete
- Negative prompt:
  invented lock body, mixed latch family, decorative cutaway fiction, lever handle, round knob, long escutcheon plate, camera cluster, merged interior and exterior block, fingerprint sensor below the keypad

## Reset-first generation order
1. IMG-012
2. IMG-001
3. IMG-002
4. IMG-005
5. IMG-003

## Conditional or gated slots
- IMG-008 `e-shield-link-qr`

## Notes
- Do not reuse any legacy published winner as a prompt baseline for the reset cycle.
- Keep exterior, interior, and edge imagery separated into distinct frames.
- Add labels, arrows, and numbered callouts later in editorial composition rather than inside the generated image.
