# e-Nova AI Image Prompts

## Purpose
This is the canonical e-Nova prompt pack inside the reset manual-imagery system.

All new work in this file follows `../../shared/visual-rules/manual-image-reset-policy.md`.
Use only `schematic` or `hybrid` classes, treat exterior/interior/edge as separate views, and allow human presence only as a hand silhouette when a contact cue is essential.

## Reference basis
- Use the isolated transparent PNG reference in `../../../ext-images/` as the geometry anchor for every new composition.
- Build this cycle from zero; do not inherit crops, overlays, or framing from older generated outputs.
- Re-check the product visual profile before changing handle, keypad, sensor, or interior relationships.

## Shared negative base
marketing glamor, cinematic drama, photorealistic lifestyle staging, full human figure, human face, body-led scene, invented UI text, fake labels, wrong geometry, mixed interior and exterior hardware in one frame, wrong lock-edge mechanism, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

## Prompt pack

### 1. e-nova-hero-main
- Class: hybrid
- View side: exterior
- Format: 16:9 horizontal
- Use: hub principal y referencia exterior
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: exterior-full
- Prompt:
  ilustracion hibrida tecnica de la cara exterior de e-Nova instalada en una puerta, perilla inteligente compacta con rosetas circulares, sensor centrado con aro azul en la cara exterior, contexto minimo de puerta, sin personas ni interiores mezclados, claridad de manual por encima de ambientacion
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 2. e-nova-installed-context
- Class: hybrid
- View side: interior
- Format: 4:3 horizontal
- Use: primeros pasos con vista interior instalada
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: interior-full
- Prompt:
  ilustracion hibrida tecnica de la cara interior de e-Nova instalada, perilla interior y zona de thumbturn visibles, composicion limpia, puerta real simplificada, sin mostrar la cara exterior al mismo tiempo
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 3. e-nova-add-admin-action
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: agregar administrador
- Modules: visual profile + interaction module + hybrid framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico hibrido de e-Nova mostrando solo una silueta de dedo acercandose al sensor centrado de la perilla exterior para representar el alta de administrador, sin inventar panel frontal ni keypad
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 4. e-nova-pin-use
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: uso de PIN o password
- Modules: visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico esquematico editorial para explicar acceso por PIN en e-Nova sin inventar teclado fisico, usando la perilla exterior solo como ancla contextual y dejando cualquier codigo fuera de la imagen
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 5. e-nova-fingerprint-use
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: uso de huella
- Modules: visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico hibrido de uso de huella en e-Nova con una silueta de dedo alineada al sensor centrado de la perilla exterior, roseta y volumen compacto claramente legibles
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 6. e-nova-language-settings
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: ajustes o idioma
- Modules: visual profile + schematic controls + manual-image-reset-policy
- Product slice: control-zone
- Prompt:
  grafico esquematico de configuracion condicional para e-Nova usando la cara interior o la perilla como ancla contextual, sin inventar pantalla ni panel frontal
- Negative prompt:
  photorealistic people, fake UI proof, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 7. e-nova-app-add-device
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: alta de dispositivo en app
- Modules: visual profile + app pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Nova exterior con smartphone simplificado para alta de dispositivo, telefono secundario al producto, sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 8. e-nova-link-qr
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: vinculacion por QR
- Modules: visual profile + qr pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Nova exterior con smartphone simplificado y QR generico contextual, sin persona visible y sin instrucciones legibles en pantalla
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 9. e-nova-troubleshoot-fingerprint
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: troubleshooting de huella
- Modules: visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico esquematico de diagnostico del sensor frontal de e-Nova con silueta de dedo opcional, foco en el centro de la perilla y sin dramatismo
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 10. e-nova-troubleshoot-app-connection
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: troubleshooting de app
- Modules: visual profile + troubleshooting + app pairing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de revision de conexion entre e-Nova y smartphone simplificado, producto dominante y sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 11. e-nova-downloads-docs
- Class: hybrid
- View side: neutral
- Format: 16:9 horizontal
- Use: descargas y documentacion
- Modules: visual profile + editorial still-life + hybrid framing + manual-image-reset-policy
- Product slice: product-plus-document
- Prompt:
  composicion hibrida de e-Nova con ficha tecnica o soporte documental en un entorno neutro, sin estetica publicitaria
- Negative prompt:
  corporate brochure styling, mixed hardware sides, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

### 12. e-nova-edge-mechanism-reference
- Class: schematic
- View side: edge
- Format: 4:3 horizontal
- Use: referencia del mecanismo de canto
- Modules: visual profile + product-truth policy + manual-image-reset-policy
- Product slice: edge-mechanism
- Prompt:
  no generar esta pieza hasta validar con OEM el mecanismo exacto de canto para e-Nova; cuando exista referencia, fijar una sola familia de pestillo para todo el paquete y no inventar variantes
- Negative prompt:
  invented lock body, mixed latch family, decorative cutaway fiction, lever lock silhouette, keypad slab, escutcheon plate, camera cluster, fingerprint sensor away from knob center, rim-lock interior box

## Reset-first generation order
1. IMG-001
2. IMG-002
3. IMG-005
4. IMG-007
5. IMG-003

## Conditional or gated slots
- IMG-004 `e-nova-pin-use`
- IMG-006 `e-nova-language-settings`
- IMG-008 `e-nova-link-qr`

## Blocked technical slots
- IMG-012 `e-nova-edge-mechanism-reference`

## Notes
- Do not reuse any legacy published winner as a prompt baseline for the reset cycle.
- Keep exterior, interior, and edge imagery separated into distinct frames.
- Add labels, arrows, and numbered callouts later in editorial composition rather than inside the generated image.
