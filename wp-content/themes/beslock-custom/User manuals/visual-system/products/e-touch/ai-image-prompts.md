# e-Touch AI Image Prompts

## Purpose
This is the canonical e-Touch prompt pack inside the operational visual system.

It migrates the legacy flat prompt document into the product-local control surface and rewrites it around the new system rules:
- product truth from `../../../ext-images/e-touch/e-touch-visual-profile.md`
- realism class from `../../shared/visual-rules/realism-vs-schematic.md`
- reusable modules from `../../shared/`

## Assembly rule
Build each prompt from:
1. e-Touch visual profile
2. image class
3. interaction module when needed
4. documentary style
5. lighting standard
6. master negative prompt plus e-Touch-specific restrictions

## Shared negative base
marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
keypad slab, tall escutcheon plate, knob lock silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, fingerprint sensor on a separate panel, bulky smart-lock body, generic front display

## Prompt pack

### 1. e-touch-hero-main
- Class: realistic
- Use: hub principal y orientación del producto
- Modules: visual profile + documentary style + lighting standard + realism rules + framing rules (hero)
- Prompt:
  e-Touch instalada en una puerta residencial real, cerradura inteligente minimalista con manija exterior negra brillante y rosetas circulares, números integrados directamente sobre la manija exterior, sensor de huella cerca de la base de la manija, composición clara y sobria, iluminación neutra suave, reflejos controlados sobre el acabado negro, fotografía documental técnica, alta definición, sin estética publicitaria exagerada
- Negative prompt:
  marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look, keypad slab, tall escutcheon plate, knob lock silhouette, camera cluster, face-recognition panel, fingerprint sensor on handle tip, bulky smart-lock body, generic front display
- Format: 16:9 horizontal

### 2. e-touch-installed-context
- Class: realistic
- Use: primeros pasos e identidad instalada
- Modules: visual profile + documentary style + lighting standard + framing rules (hero)
- Prompt:
  e-Touch ya instalada y lista para uso en una puerta de apartamento o casa, set de manija inteligente con rosetas circulares visibles, numerales sobre la manija exterior y sensor de huella cerca de la base, ambiente doméstico limpio, fotografía documental sobria, luz natural equilibrada, materiales negros creíbles, composición útil para guía técnica
- Negative prompt:
  generic smart lock, flat keypad panel, knob silhouette, camera cluster, elongated escutcheon plate, exaggerated reflections, cluttered background, oversized hardware, low resolution
- Format: 4:3 horizontal

### 3. e-touch-add-admin-action
- Class: semi-realistic
- Use: agregar administrador
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  primer plano realista de una mano adulta interactuando con la zona numérica integrada en la manija exterior de e-Touch, roseta circular visible, sensor de huella cerca de la base de la manija, acción única y clara de configuración, composición limpia, fondo discreto, iluminación suave, estilo técnico documental
- Negative prompt:
  keypad slab on flat panel, wrong lock family, handle tip sensor, deformed hand, extra fingers, extreme angle, cluttered frame, fake readable interface, bulky lock body
- Format: 4:5 vertical

### 4. e-touch-pin-use
- Class: semi-realistic
- Use: ingreso por PIN
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  detalle de e-Touch mostrando una mano adulta usando la zona numérica integrada en la manija exterior, números como parte de la estructura física del producto, sensor de huella cerca de la base, enfoque claro en la acción, iluminación neutra, fotografía de ayuda sobria y de alta claridad
- Negative prompt:
  flat keypad slab, readable fake digits carrying instruction meaning, knob silhouette, escutcheon plate, wrong sensor location, deformed fingers, noisy reflections, cluttered frame
- Format: 4:5 vertical

### 5. e-touch-fingerprint-use
- Class: realistic
- Use: registrar huella y soporte de huella
- Modules: visual profile + fingerprint interaction + documentary style + lighting standard + framing rules (interaction)
- Prompt:
  primer plano realista de una persona usando el sensor de huella de e-Touch ubicado cerca de la base de la manija exterior, dedo alineado naturalmente con la zona de contacto real, roseta circular visible, números integrados sobre la manija aún reconocibles, fondo neutro desenfocado, reflejos suaves sobre negro, composición didáctica, fotografía documental
- Negative prompt:
  touching the handle tip, fingerprint sensor on a separate panel, knob silhouette, keypad slab, camera cluster, deformed hand, extra fingers, glowing sci-fi sensor, low resolution
- Format: 4:5 vertical

### 6. e-touch-language-settings
- Class: hybrid
- Use: configuración o idioma solo si el flujo real lo justifica
- Modules: visual profile + documentary style + realism rules + framing rules (hybrid)
- Prompt:
  escena híbrida y sobria para configuración de e-Touch con el producto realista instalado en puerta, manija inteligente con rosetas circulares claramente reconocible, sin inventar una pantalla o panel frontal en el hardware, composición limpia para artículo de ayuda, tratamiento visual técnico y controlado
- Negative prompt:
  front display on the lock, keypad slab, readable fake settings text on the hardware, knob silhouette, escutcheon plate, bulky product body, cluttered background
- Format: 4:5 vertical

### 7. e-touch-app-add-device
- Class: realistic
- Use: agregar dispositivo en app
- Modules: visual profile + app pairing + documentary style + lighting standard + framing rules (app pairing)
- Prompt:
  persona adulta sosteniendo un smartphone cerca de una puerta con e-Touch instalada, manija inteligente minimalista claramente visible con rosetas circulares y sensor de huella en la base de la manija, escena calmada de vinculación inicial, ambiente doméstico limpio, fotografía documental sobria, teléfono usado solo como apoyo contextual, alta definición
- Negative prompt:
  phone-only composition, fake readable app flow, keypad slab, knob lock body, camera cluster, marketing pose, cluttered background, exaggerated lifestyle styling
- Format: 4:3 horizontal

### 8. e-touch-link-qr
- Class: realistic
- Use: vinculación por QR solo si el flujo real existe para este producto
- Modules: visual profile + qr pairing + documentary style + framing rules (app pairing)
- Prompt:
  escena realista de vinculación contextual por QR entre smartphone y e-Touch, manija inteligente con numerales integrados y rosetas circulares claramente visible, código QR genérico en el teléfono como señal editorial, ambiente interior limpio, composición didáctica y sobria, fotografía técnica
- Negative prompt:
  scannable technical QR, keypad slab, knob silhouette, front display, fake instructions on screen, clutter, neon effects, oversized product
- Format: 4:3 horizontal

### 9. e-touch-troubleshoot-fingerprint
- Class: semi-realistic
- Use: no reconoce huella
- Modules: visual profile + fingerprint interaction + troubleshooting + documentary style
- Prompt:
  escena sobria de troubleshooting con una persona revisando el sensor de huella de e-Touch cerca de la base de la manija exterior, gesto neutro de comprobación, producto claramente visible con rosetas circulares y numerales integrados, composición limpia, ambiente doméstico ordenado, fotografía documental para solución de problemas
- Negative prompt:
  alarmist acting, wrong sensor position, keypad slab, knob geometry, dramatic lighting, deformed hands, cluttered background
- Format: 4:5 vertical

### 10. e-touch-troubleshoot-app-connection
- Class: semi-realistic
- Use: no conecta a la app
- Modules: visual profile + troubleshooting + app pairing + documentary style
- Prompt:
  persona revisando una conexión de app frente a e-Touch instalada, teléfono y manija inteligente visibles al mismo tiempo, producto minimalista con rosetas circulares, numerales integrados y sensor de base reconocible, gesto leve de espera o revisión, ambiente doméstico limpio, estilo técnico sobrio
- Negative prompt:
  giant fake error dialog, keypad slab, knob silhouette, phone dominating the frame, camera cluster, clutter, exaggerated frustration, neon glow
- Format: 4:3 horizontal

### 11. e-touch-downloads-docs
- Class: hybrid
- Use: descargas y documentación
- Modules: visual profile + documentary style + framing rules (hero)
- Prompt:
  composición editorial sobria con e-Touch junto a documentación técnica o una tablet sobre una superficie limpia, manija inteligente minimalista claramente reconocible con numerales integrados y sensor de base, tonos neutros, iluminación suave, utilidad documental por encima de estética comercial
- Negative prompt:
  corporate brochure styling, wrong lock geometry, readable fake document text as main evidence, keypad slab, cluttered desk, plastic render look, low resolution
- Format: 16:9 horizontal

## First-wave generation order
1. `e-touch-hero-main`
2. `e-touch-installed-context`
3. `e-touch-fingerprint-use`
4. `e-touch-app-add-device`
5. `e-touch-pin-use`

## Notes
- Use real app captures when UI detail matters.
- Do not generate e-Touch as if it had a separate front keypad slab.
- Keep the fingerprint sensor at the handle base and the numerals on the handle body itself.
- Treat `language-settings` and `link-qr` as conditional slots until the underlying feature flow is confirmed.
