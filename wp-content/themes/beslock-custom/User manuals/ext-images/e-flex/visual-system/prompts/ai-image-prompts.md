# e-Flex AI Image Prompts

## Purpose
This is the canonical e-Flex prompt pack inside the reset manual-imagery system.

All new work in this file follows `../../shared/visual-rules/manual-image-reset-policy.md`.
Use only `schematic` or `hybrid` classes, treat exterior/interior/edge as separate views, and allow human presence only as a hand silhouette when a contact cue is essential.

## Reference basis
- Use the isolated transparent PNG reference in `../../../ext-images/` as the geometry anchor for every new composition.
- Build this cycle from zero; do not inherit crops, overlays, or framing from older generated outputs.
- Re-check the product visual profile before changing handle, keypad, sensor, or interior relationships.

## Shared negative base
marketing glamor, cinematic drama, photorealistic lifestyle staging, full human figure, human face, body-led scene, invented UI text, fake labels, wrong geometry, mixed interior and exterior hardware in one frame, wrong lock-edge mechanism, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

## Prompt pack

### 1. e-flex-hero-main
- Class: hybrid
- View side: exterior
- Format: 16:9 horizontal
- Use: hub principal y referencia exterior
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: exterior-full
- Prompt:
  ilustracion hibrida tecnica de la cara exterior de e-Flex instalada en una puerta, placa larga, keypad superior, manija recta y sensor de huella en la cara de la manija, sin personas
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 2. e-flex-installed-context
- Class: hybrid
- View side: interior
- Format: 4:3 horizontal
- Use: primeros pasos con vista interior instalada
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: interior-full
- Prompt:
  ilustracion hibrida tecnica de la cara interior de e-Flex instalada, placa larga interior con bateria y controles simples sugeridos, sin mostrar la cara exterior en el mismo cuadro
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 3. e-flex-add-admin-action
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: agregar administrador
- Modules: visual profile + interaction module + hybrid framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico hibrido de alta de administrador en e-Flex con silueta de dedo acercandose al keypad superior del panel exterior, manteniendo visible la placa larga
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 4. e-flex-pin-use
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: uso de PIN o password
- Modules: visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico esquematico de PIN en e-Flex centrado en el keypad superior de la placa exterior, sin secuencias legibles ni menus incrustados
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 5. e-flex-fingerprint-use
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: uso de huella
- Modules: visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico hibrido de uso de huella en e-Flex con silueta de dedo alineada al sensor de la cara de la manija exterior, placa larga y manija aun reconocibles
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 6. e-flex-language-settings
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: ajustes o idioma
- Modules: visual profile + schematic controls + manual-image-reset-policy
- Product slice: control-zone
- Prompt:
  grafico esquematico de ajustes o idioma en e-Flex centrado en las zonas reales de control del exterior, sin personas ni menus falsos
- Negative prompt:
  photorealistic people, fake UI proof, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 7. e-flex-app-add-device
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: alta de dispositivo en app
- Modules: visual profile + app pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Flex exterior con smartphone simplificado para alta de dispositivo, producto dominante y sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 8. e-flex-link-qr
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: vinculacion por QR
- Modules: visual profile + qr pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Flex exterior con smartphone simplificado y QR contextual, sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 9. e-flex-troubleshoot-fingerprint
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: troubleshooting de huella
- Modules: visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico esquematico de diagnostico del sensor en la manija de e-Flex, con silueta de dedo opcional y foco en la zona correcta
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 10. e-flex-troubleshoot-app-connection
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: troubleshooting de app
- Modules: visual profile + troubleshooting + app pairing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de revision de conexion entre e-Flex y smartphone simplificado, sin tapar la geometria de placa larga
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 11. e-flex-downloads-docs
- Class: hybrid
- View side: neutral
- Format: 16:9 horizontal
- Use: descargas y documentacion
- Modules: visual profile + editorial still-life + hybrid framing + manual-image-reset-policy
- Product slice: product-plus-document
- Prompt:
  composicion hibrida de e-Flex con documentacion tecnica, manteniendo visible la placa larga y el sensor de manija
- Negative prompt:
  corporate brochure styling, mixed hardware sides, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

### 12. e-flex-edge-mechanism-reference
- Class: schematic
- View side: edge
- Format: 4:3 horizontal
- Use: referencia del mecanismo de canto
- Modules: visual profile + product-truth policy + manual-image-reset-policy
- Product slice: edge-mechanism
- Prompt:
  grafico esquematico tecnico del canto de puerta de e-Flex basado en la guia OEM: cuerpo de cerradura, pestillo, eje cuadrado y familia de mecanismo consistentes con la misma instalacion en todo el paquete
- Negative prompt:
  invented lock body, mixed latch family, decorative cutaway fiction, knob silhouette, camera cluster, face-recognition screen, split-body architecture, fingerprint sensor moved to the keypad panel, missing long-plate body

## Reset-first generation order
1. IMG-012
2. IMG-001
3. IMG-002
4. IMG-005
5. IMG-003

## Conditional or gated slots
- IMG-008 `e-flex-link-qr`

## Notes
- Do not reuse any legacy published winner as a prompt baseline for the reset cycle.
- Keep exterior, interior, and edge imagery separated into distinct frames.
- Add labels, arrows, and numbered callouts later in editorial composition rather than inside the generated image.
