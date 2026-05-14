# e-Orbit AI Image Prompts

## Purpose
This is the canonical e-Orbit prompt pack inside the reset manual-imagery system.

All new work in this file follows `../../shared/visual-rules/manual-image-reset-policy.md`.
Use only `schematic` or `hybrid` classes, treat exterior/interior/edge as separate views, and allow human presence only as a hand silhouette when a contact cue is essential.

## Reference basis
- Use the isolated transparent PNG reference in `../../../ext-images/` as the geometry anchor for every new composition.
- Build this cycle from zero; do not inherit crops, overlays, or framing from older generated outputs.
- Re-check the product visual profile before changing handle, keypad, sensor, or interior relationships.

## Shared negative base
marketing glamor, cinematic drama, photorealistic lifestyle staging, full human figure, human face, body-led scene, invented UI text, fake labels, wrong geometry, mixed interior and exterior hardware in one frame, wrong lock-edge mechanism, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

## Prompt pack

### 1. e-orbit-hero-main
- Class: hybrid
- View side: exterior
- Format: 16:9 horizontal
- Use: hub principal y referencia exterior
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: exterior-full
- Prompt:
  ilustracion hibrida tecnica de la cara exterior de e-Orbit instalada en una puerta, cuerpo alto monolitico, cluster superior de camara o sensores visible, display y keypad separados, manija exterior esculpida con sensor de huella en la parte superior, sin personas
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 2. e-orbit-installed-context
- Class: hybrid
- View side: interior
- Format: 4:3 horizontal
- Use: primeros pasos con vista interior instalada
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: interior-full
- Prompt:
  ilustracion hibrida tecnica de la cara interior de e-Orbit instalada, pantalla interior alta y thumbturn inferior claramente visibles, composicion limpia, sin mostrar la cara exterior en el mismo cuadro
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 3. e-orbit-add-admin-action
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: agregar administrador
- Modules: visual profile + interaction module + hybrid framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico hibrido de alta de administrador en e-Orbit con silueta de dedo acercandose solo al keypad frontal, numerales como referencia estructural y cluster superior aun reconocible
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 4. e-orbit-pin-use
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: uso de PIN o password
- Modules: visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico esquematico de ingreso por PIN en e-Orbit mostrando el keypad frontal como zona de accion, sin secuencias legibles ni menus incrustados
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 5. e-orbit-fingerprint-use
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: uso de huella
- Modules: visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico hibrido de uso de huella en e-Orbit con silueta de dedo alineada al sensor en la parte superior de la manija exterior, manteniendo visible el cuerpo alto
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 6. e-orbit-language-settings
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: ajustes o idioma
- Modules: visual profile + schematic controls + manual-image-reset-policy
- Product slice: control-zone
- Prompt:
  grafico esquematico de ajustes o idioma para e-Orbit centrado en display y keypad como zonas de control, sin texto tecnico legible y sin personas
- Negative prompt:
  photorealistic people, fake UI proof, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 7. e-orbit-app-add-device
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: alta de dispositivo en app
- Modules: visual profile + app pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Orbit exterior con smartphone simplificado para alta en Smart Life o Tuya, telefono secundario al producto y sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 8. e-orbit-link-qr
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: vinculacion por QR
- Modules: visual profile + qr pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Orbit exterior con smartphone simplificado en contexto QR, codigo solo como pista contextual, sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 9. e-orbit-troubleshoot-fingerprint
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: troubleshooting de huella
- Modules: visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico esquematico de diagnostico del sensor de manija en e-Orbit, con silueta de dedo opcional y foco claro en la zona correcta
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 10. e-orbit-troubleshoot-app-connection
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: troubleshooting de app
- Modules: visual profile + troubleshooting + app pairing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de diagnostico de conectividad entre e-Orbit y smartphone simplificado, producto dominante y sin cuerpo humano
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 11. e-orbit-downloads-docs
- Class: hybrid
- View side: neutral
- Format: 16:9 horizontal
- Use: descargas y documentacion
- Modules: visual profile + editorial still-life + hybrid framing + manual-image-reset-policy
- Product slice: product-plus-document
- Prompt:
  composicion hibrida de e-Orbit con soporte documental o ficha tecnica, manteniendo visible el cluster superior y la identidad NF14
- Negative prompt:
  corporate brochure styling, mixed hardware sides, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

### 12. e-orbit-edge-mechanism-reference
- Class: schematic
- View side: edge
- Format: 4:3 horizontal
- Use: referencia del mecanismo de canto
- Modules: visual profile + product-truth policy + manual-image-reset-policy
- Product slice: edge-mechanism
- Prompt:
  no generar esta pieza hasta validar cual cuerpo de cerradura comercial usa e-Orbit entre 6068, 85 o 90; cuando el OEM lo confirme, fijar esa familia como unica referencia de canto para todo el paquete
- Negative prompt:
  invented lock body, mixed latch family, decorative cutaway fiction, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

## Reset-first generation order
1. IMG-001
2. IMG-002
3. IMG-005
4. IMG-007
5. IMG-003

## Blocked technical slots
- IMG-012 `e-orbit-edge-mechanism-reference`

## Notes
- Do not reuse any legacy published winner as a prompt baseline for the reset cycle.
- Keep exterior, interior, and edge imagery separated into distinct frames.
- Add labels, arrows, and numbered callouts later in editorial composition rather than inside the generated image.
