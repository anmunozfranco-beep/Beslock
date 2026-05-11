# e-Shield AI Image Prompts

## Purpose
This is the canonical e-Shield prompt pack inside the operational visual system.

It migrates the legacy flat prompt document into the product-local control surface and rewrites it around the new system rules:
- product truth from `../../../ext-images/e-shield/e-shield-visual-profile.md`
- realism class from `../../shared/visual-rules/realism-vs-schematic.md`
- reusable modules from `../../shared/`

## Assembly rule
Build each prompt from:
1. e-Shield visual profile
2. image class
3. interaction module when needed
4. documentary style
5. lighting standard
6. master negative prompt plus e-Shield-specific restrictions

## Shared negative base
marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
lever lock silhouette, knob lock silhouette, long escutcheon plate, camera cluster, face-recognition screen, merged exterior and interior bodies, handle added to the slab, horizontal exterior slab, missing interior box

## Prompt pack

### 1. e-shield-hero-main
- Class: realistic
- Use: hub principal y orientación del producto
- Modules: visual profile + documentary style + lighting standard + realism rules + framing rules (hero)
- Prompt:
  e-Shield instalada en una puerta residencial real, cerradura inteligente de arquitectura split-body con módulo exterior vertical estrecho y brillante, sensor de huella circular con aro azul cerca de la parte superior, teclado numérico debajo del sensor, módulo interior separado con caja horizontal claramente distinguible, iluminación neutra suave, reflejos controlados, composición clara para centro de ayuda, fotografía documental técnica, alta definición, sin estética comercial exagerada
- Negative prompt:
  marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look, lever lock silhouette, knob lock silhouette, long escutcheon plate, camera cluster, face-recognition screen, merged exterior and interior bodies, handle added to the slab, horizontal exterior slab, missing interior box
- Format: 16:9 horizontal

### 2. e-shield-installed-context
- Class: realistic
- Use: primeros pasos e identidad instalada
- Modules: visual profile + documentary style + lighting standard + framing rules (hero)
- Prompt:
  e-Shield ya instalada y lista para uso en una puerta de apartamento o casa, módulo exterior vertical estrecho con sensor de huella superior y teclado debajo claramente visibles, caja interior separada y horizontal reconocible, ambiente doméstico limpio y realista, fotografía documental sobria, luz natural equilibrada, materiales negros creíbles, composición útil para guía técnica
- Negative prompt:
  generic smart lock, handle added to exterior, merged body, knob silhouette, camera cluster, exaggerated reflections, cluttered background, oversized hardware, low resolution
- Format: 4:3 horizontal

### 3. e-shield-add-admin-action
- Class: semi-realistic
- Use: agregar administrador
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  primer plano realista de una mano adulta interactuando con el teclado del módulo exterior vertical de e-Shield, sensor de huella superior aún visible, cuerpo exterior delgado y sin manija, acción única y clara de configuración, composición limpia, fondo discreto, iluminación suave, estilo técnico documental
- Negative prompt:
  handle-based interaction, lever lock body, knob lock body, keypad moved away from the exterior slab, deformed hand, extra fingers, extreme angle, fake readable interface, cluttered frame
- Format: 4:5 vertical

### 4. e-shield-pin-use
- Class: semi-realistic
- Use: ingreso por PIN
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  detalle de e-Shield mostrando una mano adulta usando el teclado del módulo exterior vertical, sensor de huella superior y forma estrecha del cuerpo aún reconocibles, acción clara, iluminación neutra, fotografía de ayuda sobria y de alta claridad, sin depender de números generados como prueba técnica
- Negative prompt:
  readable fake digits carrying instruction meaning, handle on the slab, knob silhouette, camera cluster, merged lock bodies, deformed fingers, noisy reflections, cluttered frame
- Format: 4:5 vertical

### 5. e-shield-fingerprint-use
- Class: realistic
- Use: registrar huella y soporte de huella
- Modules: visual profile + fingerprint interaction + documentary style + lighting standard + framing rules (interaction)
- Prompt:
  primer plano realista de una persona usando el sensor de huella de e-Shield ubicado cerca de la parte superior del módulo exterior vertical, dedo alineado naturalmente con la zona de contacto real, teclado debajo aún reconocible, forma estrecha del cuerpo preservada, fondo neutro desenfocado, reflejos suaves sobre negro, composición didáctica, fotografía documental
- Negative prompt:
  touching the keypad instead of the fingerprint sensor, handle added to the slab, knob silhouette, camera cluster, merged exterior and interior bodies, deformed hand, extra fingers, glowing sci-fi sensor, low resolution
- Format: 4:5 vertical

### 6. e-shield-language-settings
- Class: semi-realistic
- Use: configuración o idioma
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  escena sobria de configuración para e-Shield con mano adulta interactuando en el módulo exterior vertical, sensor superior y teclado bien diferenciados, sin manija añadida, composición limpia para artículo de ayuda, iluminación suave, realismo técnico, sin depender de texto generado en pantalla
- Negative prompt:
  readable fake settings text, handle-based product, knob silhouette, camera cluster, futuristic interface, cluttered background, extreme reflections, merged bodies
- Format: 4:5 vertical

### 7. e-shield-app-add-device
- Class: realistic
- Use: agregar dispositivo en app
- Modules: visual profile + app pairing + documentary style + lighting standard + framing rules (app pairing)
- Prompt:
  persona adulta sosteniendo un smartphone cerca de una puerta con e-Shield instalada, módulo exterior vertical con sensor superior y teclado visibles, caja interior separada reconocible cuando el encuadre lo permita, escena calmada de vinculación inicial, ambiente doméstico limpio, fotografía documental sobria, teléfono usado solo como apoyo contextual, alta definición
- Negative prompt:
  phone-only composition, fake readable app flow, lever lock body, knob lock, camera cluster, marketing pose, cluttered background, exaggerated lifestyle styling, merged lock bodies
- Format: 4:3 horizontal

### 8. e-shield-link-qr
- Class: realistic
- Use: vinculación por QR solo si el flujo real existe para este producto
- Modules: visual profile + qr pairing + documentary style + framing rules (app pairing)
- Prompt:
  escena realista de vinculación contextual por QR entre smartphone y e-Shield, módulo exterior vertical estrecho con sensor superior y teclado claramente visible, código QR genérico en el teléfono como señal editorial, ambiente interior limpio, composición didáctica y sobria, fotografía técnica
- Negative prompt:
  scannable technical QR, handle added to slab, knob silhouette, camera cluster, fake instructions on screen, clutter, neon effects, merged bodies, missing interior box
- Format: 4:3 horizontal

### 9. e-shield-troubleshoot-fingerprint
- Class: semi-realistic
- Use: no reconoce huella
- Modules: visual profile + fingerprint interaction + troubleshooting + documentary style
- Prompt:
  escena sobria de troubleshooting con una persona revisando el sensor de huella superior de e-Shield, gesto neutro de comprobación, módulo exterior estrecho y teclado debajo aún visibles, composición limpia, ambiente doméstico ordenado, fotografía documental para solución de problemas
- Negative prompt:
  alarmist acting, wrong sensor position, handle on exterior slab, knob silhouette, dramatic lighting, deformed hands, cluttered background, merged bodies
- Format: 4:5 vertical

### 10. e-shield-troubleshoot-app-connection
- Class: semi-realistic
- Use: no conecta a la app
- Modules: visual profile + troubleshooting + app pairing + documentary style
- Prompt:
  persona revisando una conexión de app frente a e-Shield instalada, teléfono y módulo exterior visibles al mismo tiempo, cuerpo exterior vertical con sensor superior y teclado reconocibles, gesto leve de espera o revisión, ambiente doméstico limpio, estilo técnico sobrio
- Negative prompt:
  giant fake error dialog, lever lock silhouette, knob silhouette, phone dominating the frame, camera cluster, clutter, exaggerated frustration, neon glow, merged bodies
- Format: 4:3 horizontal

### 11. e-shield-downloads-docs
- Class: hybrid
- Use: descargas y documentación
- Modules: visual profile + documentary style + framing rules (hero)
- Prompt:
  composición editorial sobria con e-Shield junto a documentación técnica o una tablet sobre una superficie limpia, módulo exterior vertical y caja interior separados claramente reconocibles, sensor superior y teclado visibles, tonos neutros, iluminación suave, utilidad documental por encima de estética comercial
- Negative prompt:
  corporate brochure styling, wrong lock geometry, readable fake document text as main evidence, handle on exterior slab, cluttered desk, plastic render look, low resolution, merged bodies
- Format: 16:9 horizontal

## First-wave generation order
1. `e-shield-hero-main`
2. `e-shield-installed-context`
3. `e-shield-fingerprint-use`
4. `e-shield-add-admin-action`
5. `e-shield-app-add-device`
6. `e-shield-pin-use`

## Notes
- Use real app captures when UI detail matters.
- Keep the exterior slab vertical, handle-free, and distinct from the interior box.
- Keep the fingerprint sensor above the keypad on the exterior body.
- Treat `link-qr` as conditional until the underlying feature flow is confirmed.
