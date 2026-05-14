# e-Touch AI Image Prompts

## Purpose
This is the canonical e-Touch prompt pack inside the reset manual-imagery system.

All new work in this file follows `../../shared/visual-rules/manual-image-reset-policy.md`.
Use only `schematic` or `hybrid` classes, treat exterior/interior/edge as separate views, and allow human presence only as a hand silhouette when a contact cue is essential.

## Reference basis
- Use the isolated transparent PNG reference in `../../../ext-images/` as the geometry anchor for every new composition.
- Build this cycle from zero; do not inherit crops, overlays, or framing from older generated outputs.
- Re-check the product visual profile before changing handle, keypad, sensor, or interior relationships.

## Shared negative base
marketing glamor, cinematic drama, photorealistic lifestyle staging, full human figure, human face, body-led scene, invented UI text, fake labels, wrong geometry, mixed interior and exterior hardware in one frame, wrong lock-edge mechanism, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

## Prompt pack

### 1. e-touch-hero-main
- Class: hybrid
- View side: exterior
- Format: 16:9 horizontal
- Use: hub principal y referencia exterior
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: exterior-full
- Prompt:
  ilustracion hibrida tecnica de la cara exterior de e-Touch instalada en una puerta, rosetas circulares, manija exterior negra brillante con numerales integrados y sensor de huella en la base, sin personas ni panel frontal inventado
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 2. e-touch-installed-context
- Class: hybrid
- View side: interior
- Format: 4:3 horizontal
- Use: primeros pasos con vista interior instalada
- Modules: visual profile + documentary style + hybrid framing + manual-image-reset-policy
- Product slice: interior-full
- Prompt:
  ilustracion hibrida tecnica de la cara interior de e-Touch instalada, manija interior mas limpia y minimalista, composicion clara, sin mostrar la cara exterior al mismo tiempo
- Negative prompt:
  photorealistic people, mixed hardware sides, exaggerated lifestyle context, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 3. e-touch-add-admin-action
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: agregar administrador
- Modules: visual profile + interaction module + hybrid framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico hibrido de alta de administrador en e-Touch mostrando una silueta de dedo acercandose solo a la zona numerica integrada en la manija exterior, sin inventar panel aparte
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 4. e-touch-pin-use
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: uso de PIN o password
- Modules: visual profile + keypad or credential abstraction + schematic framing + manual-image-reset-policy
- Product slice: exterior-interaction-zone
- Prompt:
  grafico esquematico de uso de PIN en e-Touch usando la zona numerica integrada en la manija como referencia estructural, sin secuencia legible y sin teclado plano
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 5. e-touch-fingerprint-use
- Class: hybrid
- View side: exterior
- Format: 4:5 vertical
- Use: uso de huella
- Modules: visual profile + fingerprint interaction + hybrid framing + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico hibrido de uso de huella en e-Touch con silueta de dedo en el sensor circular de la base de la manija exterior, manteniendo visibles roseta y numerales integrados
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 6. e-touch-language-settings
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: ajustes o idioma
- Modules: visual profile + schematic controls + manual-image-reset-policy
- Product slice: control-zone
- Prompt:
  grafico esquematico de flujo condicional de configuracion para e-Touch usando la manija y la cara interior como anclas contextuales, sin inventar display
- Negative prompt:
  photorealistic people, fake UI proof, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 7. e-touch-app-add-device
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: alta de dispositivo en app
- Modules: visual profile + app pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Touch exterior con smartphone simplificado para alta Bluetooth o Tuya, telefono secundario al producto y sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 8. e-touch-link-qr
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: vinculacion por QR
- Modules: visual profile + qr pairing + hybrid framing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de e-Touch exterior con smartphone simplificado y QR generico contextual, sin persona visible
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 9. e-touch-troubleshoot-fingerprint
- Class: schematic
- View side: exterior
- Format: 4:5 vertical
- Use: troubleshooting de huella
- Modules: visual profile + fingerprint interaction + troubleshooting + manual-image-reset-policy
- Product slice: exterior-sensor-zone
- Prompt:
  grafico esquematico de diagnostico del sensor de base en e-Touch con silueta de dedo opcional y foco en la manija exterior
- Negative prompt:
  full human figure, realistic hand photo, extra fingers, wrong interaction zone, readable fake text, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 10. e-touch-troubleshoot-app-connection
- Class: hybrid
- View side: exterior
- Format: 4:3 horizontal
- Use: troubleshooting de app
- Modules: visual profile + troubleshooting + app pairing + manual-image-reset-policy
- Product slice: app-context
- Prompt:
  composicion hibrida de revision de conexion entre e-Touch y smartphone simplificado, sin tapar la geometria de rosetas y manija
- Negative prompt:
  full human figure, fake readable app UI, phone-only frame, mixed hardware sides, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 11. e-touch-downloads-docs
- Class: hybrid
- View side: neutral
- Format: 16:9 horizontal
- Use: descargas y documentacion
- Modules: visual profile + editorial still-life + hybrid framing + manual-image-reset-policy
- Product slice: product-plus-document
- Prompt:
  composicion hibrida de e-Touch con documentacion tecnica o soporte, sin estetica lifestyle
- Negative prompt:
  corporate brochure styling, mixed hardware sides, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

### 12. e-touch-edge-mechanism-reference
- Class: schematic
- View side: edge
- Format: 4:3 horizontal
- Use: referencia del mecanismo de canto
- Modules: visual profile + product-truth policy + manual-image-reset-policy
- Product slice: edge-mechanism
- Prompt:
  grafico esquematico tecnico del canto de puerta de e-Touch con deadbolt, eje cuadrado y familia de mecanismo consistente con la fuente OEM corta, sin inventar una segunda variante de pestillo
- Negative prompt:
  invented lock body, mixed latch family, decorative cutaway fiction, keypad slab, tall escutcheon plate, knob silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

## Reset-first generation order
1. IMG-012
2. IMG-001
3. IMG-002
4. IMG-005
5. IMG-003

## Conditional or gated slots
- IMG-006 `e-touch-language-settings`
- IMG-008 `e-touch-link-qr`

## Notes
- Do not reuse any legacy published winner as a prompt baseline for the reset cycle.
- Keep exterior, interior, and edge imagery separated into distinct frames.
- Add labels, arrows, and numbered callouts later in editorial composition rather than inside the generated image.
