# e-Flex AI Image Prompts

## Purpose
This is the canonical e-Flex prompt pack inside the operational visual system.

It migrates the legacy flat prompt document into the product-local control surface and rewrites it around the new system rules:
- product truth from `../../../ext-images/e-flex/e-flex-visual-profile.md`
- realism class from `../../shared/visual-rules/realism-vs-schematic.md`
- reusable modules from `../../shared/`

## Assembly rule
Build each prompt from:
1. e-Flex visual profile
2. image class
3. interaction module when needed
4. documentary style
5. lighting standard
6. master negative prompt plus e-Flex-specific restrictions

## Shared negative base
marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
knob lock silhouette, camera cluster, face-recognition screen, fingerprint sensor on the plate, fingerprint sensor on the handle tip, keypad moved off the upper front panel, split rim-lock box geometry, bulky futuristic redesign

## Prompt pack

### 1. e-flex-hero-main
- Class: realistic
- Use: hub principal y orientación del producto
- Modules: visual profile + documentary style + lighting standard + realism rules + framing rules (hero)
- Prompt:
  e-Flex instalada en una puerta residencial real, cerradura inteligente de palanca con placa vertical larga y bordes redondeados, panel frontal brillante en la zona superior, manija recta horizontal, sensor de huella circular con aro azul sutil sobre la cara de la manija exterior, acabado negro creíble, iluminación neutra suave, reflejos controlados, composición clara para centro de ayuda, fotografía documental técnica, alta definición, sin estética comercial exagerada
- Negative prompt:
  marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look, knob lock silhouette, camera cluster, face-recognition screen, fingerprint sensor on the plate, fingerprint sensor on the handle tip, keypad moved off the upper front panel, split rim-lock box geometry
- Format: 16:9 horizontal

### 2. e-flex-installed-context
- Class: realistic
- Use: primeros pasos e identidad instalada
- Modules: visual profile + documentary style + lighting standard + framing rules (hero)
- Prompt:
  e-Flex ya instalada y lista para uso en una puerta de apartamento o casa, cerradura de palanca con placa larga claramente visible, panel superior brillante, manija recta horizontal y sensor de huella en la cara de la manija exterior, ambiente doméstico limpio y realista, fotografía documental sobria, luz natural equilibrada, materiales negros creíbles, composición útil para guía técnica
- Negative prompt:
  generic smart lock, knob silhouette, fingerprint sensor on panel, flat rim-lock box, camera cluster, exaggerated reflections, cluttered background, oversized hardware, low resolution
- Format: 4:3 horizontal

### 3. e-flex-add-admin-action
- Class: semi-realistic
- Use: agregar administrador
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  primer plano realista de una mano adulta interactuando con la zona de teclado superior de e-Flex, placa larga vertical visible, manija horizontal reconocible y sensor de huella aún ubicado sobre la cara de la manija, acción única y clara de configuración, composición limpia, fondo discreto, iluminación suave, estilo técnico documental
- Negative prompt:
  fingerprint touch on the handle instead of keypad for this scene, knob lock body, keypad moved to another area, deformed hand, extra fingers, extreme angle, fake readable interface, cluttered frame
- Format: 4:5 vertical

### 4. e-flex-pin-use
- Class: semi-realistic
- Use: ingreso por PIN
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  detalle de e-Flex mostrando una mano adulta usando la zona numérica del panel superior brillante, placa larga y manija exterior aún reconocibles, acción clara, iluminación neutra, fotografía de ayuda sobria y de alta claridad, sin depender de números generados como prueba técnica
- Negative prompt:
  readable fake digits carrying instruction meaning, knob silhouette, keypad on handle, fingerprint sensor on plate, camera cluster, deformed fingers, noisy reflections, cluttered frame
- Format: 4:5 vertical

### 5. e-flex-fingerprint-use
- Class: realistic
- Use: registrar huella y soporte de huella
- Modules: visual profile + fingerprint interaction + documentary style + lighting standard + framing rules (interaction)
- Prompt:
  primer plano realista de una persona usando el sensor de huella de e-Flex ubicado en la cara de la manija exterior, dedo alineado naturalmente con la zona de contacto real, panel superior y placa larga aún reconocibles, fondo neutro desenfocado, reflejos suaves sobre negro, composición didáctica, fotografía documental
- Negative prompt:
  touching the panel instead of the handle sensor, fingerprint sensor on the plate, handle tip sensor, knob silhouette, camera cluster, deformed hand, extra fingers, glowing sci-fi sensor, low resolution
- Format: 4:5 vertical

### 6. e-flex-language-settings
- Class: semi-realistic
- Use: configuración o idioma
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  escena sobria de configuración para e-Flex con mano adulta interactuando en el panel frontal superior, placa larga, panel brillante y manija exterior bien diferenciados, composición limpia para artículo de ayuda, iluminación suave, realismo técnico, sin depender de texto generado en pantalla
- Negative prompt:
  readable fake settings text, knob silhouette, fingerprint sensor on wrong zone, camera cluster, futuristic interface, cluttered background, extreme reflections
- Format: 4:5 vertical

### 7. e-flex-app-add-device
- Class: realistic
- Use: agregar dispositivo en app
- Modules: visual profile + app pairing + documentary style + lighting standard + framing rules (app pairing)
- Prompt:
  persona adulta sosteniendo un smartphone cerca de una puerta con e-Flex instalada, cerradura de palanca con placa larga claramente visible, panel superior brillante, sensor de huella en la cara de la manija exterior, escena calmada de vinculación inicial, ambiente doméstico limpio, fotografía documental sobria, teléfono usado solo como apoyo contextual, alta definición
- Negative prompt:
  phone-only composition, fake readable app flow, knob lock body, camera cluster, marketing pose, cluttered background, exaggerated lifestyle styling, missing long plate
- Format: 4:3 horizontal

### 8. e-flex-link-qr
- Class: realistic
- Use: vinculación por QR
- Modules: visual profile + qr pairing + documentary style + framing rules (app pairing)
- Prompt:
  escena realista de vinculación contextual por QR entre smartphone y e-Flex, cerradura de palanca con placa larga y panel superior claramente visible, código QR genérico en el teléfono como señal editorial, ambiente interior limpio, composición didáctica y sobria, fotografía técnica
- Negative prompt:
  scannable technical QR, knob silhouette, camera cluster, fake instructions on screen, clutter, neon effects, fingerprint sensor on wrong area, oversized product
- Format: 4:3 horizontal

### 9. e-flex-troubleshoot-fingerprint
- Class: semi-realistic
- Use: no reconoce huella
- Modules: visual profile + fingerprint interaction + troubleshooting + documentary style
- Prompt:
  escena sobria de troubleshooting con una persona revisando el sensor de huella de e-Flex en la cara de la manija exterior, gesto neutro de comprobación, placa larga y panel superior aún visibles, composición limpia, ambiente doméstico ordenado, fotografía documental para solución de problemas
- Negative prompt:
  alarmist acting, wrong sensor position, knob silhouette, fingerprint sensor on panel, dramatic lighting, deformed hands, cluttered background
- Format: 4:5 vertical

### 10. e-flex-troubleshoot-app-connection
- Class: semi-realistic
- Use: no conecta a la app
- Modules: visual profile + troubleshooting + app pairing + documentary style
- Prompt:
  persona revisando una conexión de app frente a e-Flex instalada, teléfono y cerradura visibles al mismo tiempo, placa larga, panel superior y manija horizontal reconocibles, gesto leve de espera o revisión, ambiente doméstico limpio, estilo técnico sobrio
- Negative prompt:
  giant fake error dialog, knob silhouette, phone dominating the frame, camera cluster, clutter, exaggerated frustration, neon glow, missing long plate
- Format: 4:3 horizontal

### 11. e-flex-downloads-docs
- Class: hybrid
- Use: descargas y documentación
- Modules: visual profile + documentary style + framing rules (hero)
- Prompt:
  composición editorial sobria con e-Flex junto a documentación técnica o una tablet sobre una superficie limpia, cerradura de palanca con placa larga claramente reconocible, panel superior brillante y sensor de manija visibles, tonos neutros, iluminación suave, utilidad documental por encima de estética comercial
- Negative prompt:
  corporate brochure styling, wrong lock geometry, readable fake document text as main evidence, knob silhouette, cluttered desk, plastic render look, low resolution
- Format: 16:9 horizontal

## First-wave generation order
1. `e-flex-hero-main`
2. `e-flex-installed-context`
3. `e-flex-fingerprint-use`
4. `e-flex-add-admin-action`
5. `e-flex-app-add-device`
6. `e-flex-pin-use`

## Notes
- Use real app captures when UI detail matters.
- Keep the fingerprint sensor on the handle face, not on the plate.
- Keep the keypad restricted to the upper front panel.
- Do not let e-Flex drift into knob-lock or camera-lock families.
