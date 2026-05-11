# e-Nova AI Image Prompts

## Purpose
This is the canonical e-Nova prompt pack inside the operational visual system.

It migrates the legacy flat prompt document into the product-local control surface and rewrites it around the new system rules:
- product truth from `../../../ext-images/e-nova/e-nova-visual-profile.md`
- realism class from `../../shared/visual-rules/realism-vs-schematic.md`
- reusable modules from `../../shared/`

## Assembly rule
Build each prompt from:
1. e-Nova visual profile
2. image class
3. interaction module when needed
4. documentary style
5. lighting standard
6. master negative prompt plus e-Nova-specific restrictions

## Shared negative base
marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
lever lock silhouette, keypad slab, tall escutcheon plate, front panel display, camera cluster, rim-lock box geometry, off-center fingerprint sensor, oversized smart-home gadget proportions

## Prompt pack

### 1. e-nova-hero-main
- Class: realistic
- Use: hub principal y orientación del producto
- Modules: visual profile + documentary style + lighting standard + realism rules + framing rules (hero)
- Prompt:
  e-Nova instalada en una puerta residencial real, cerradura inteligente compacta de tipo pomo con rosetas circulares, acabado negro limpio, sensor de huella centrado en la cara del pomo exterior con aro azul sutil, geometría redonda y proporcionada, contexto doméstico sobrio, iluminación neutra suave, reflejos controlados sobre superficies curvas, fotografía documental técnica, composición clara para centro de ayuda, alta definición, sin estética comercial exagerada
- Negative prompt:
  marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look, lever lock silhouette, keypad slab, tall escutcheon plate, front panel display, camera cluster, rim-lock box geometry, off-center fingerprint sensor
- Format: 16:9 horizontal

### 2. e-nova-installed-context
- Class: realistic
- Use: primeros pasos e identidad instalada
- Modules: visual profile + documentary style + lighting standard + framing rules (hero)
- Prompt:
  e-Nova ya instalada y lista para uso en una puerta de apartamento o casa, cerradura de pomo inteligente compacta con sensor de huella centrado en la cara del pomo exterior, rosetas circulares visibles, ambiente doméstico limpio y realista, fotografía documental sobria, luz natural equilibrada, materiales negros creíbles, composición clara para guía técnica
- Negative prompt:
  generic smart lock, knob replaced by handle, keypad panel, camera cluster, exaggerated reflections, fake screen text, cluttered background, oversized hardware, low resolution
- Format: 4:3 horizontal

### 3. e-nova-add-admin-action
- Class: realistic
- Use: agregar administrador
- Modules: visual profile + fingerprint interaction + documentary style + framing rules (interaction)
- Prompt:
  primer plano realista de una mano adulta configurando o iniciando un registro de administrador en e-Nova mediante interacción clara con el pomo exterior, sensor de huella centrado visible en la cara del pomo, geometría circular del producto intacta, composición limpia, una sola acción, fondo discreto, iluminación suave, estilo técnico documental
- Negative prompt:
  keypad interaction on a flat panel, lever lock body, wrong sensor position, deformed hand, extra fingers, extreme angle, cluttered frame, fake interface text
- Format: 4:5 vertical

### 4. e-nova-pin-use
- Class: hybrid
- Use: acceso por PIN solo si la función existe y está validada
- Modules: visual profile + documentary style + realism rules + framing rules (hybrid)
- Prompt:
  representación híbrida y documental de e-Nova en una puerta real, manteniendo el pomo inteligente compacto y su sensor de huella centrado, escena de acceso por código tratada como apoyo editorial sin inventar un panel numérico en el hardware, composición clara, estética técnica sobria, producto realista con apoyo visual mínimo fuera del cuerpo de la cerradura
- Negative prompt:
  keypad slab attached to the lock, readable fake digits on the product, lever lock silhouette, tall escutcheon plate, front display, wrong proportions, futuristic UI overlays, clutter
- Format: 4:5 vertical

### 5. e-nova-fingerprint-use
- Class: realistic
- Use: registrar huella y soporte de huella
- Modules: visual profile + fingerprint interaction + documentary style + lighting standard + framing rules (interaction)
- Prompt:
  primer plano realista de una persona usando el sensor de huella de e-Nova en el centro del pomo exterior, dedo alineado naturalmente con la zona de contacto real, roseta circular visible, fondo neutro desenfocado, reflejos suaves sobre negro, composición didáctica de alta claridad, fotografía documental
- Negative prompt:
  touching the wrong area, off-center fingerprint sensor, lever geometry, keypad slab, camera cluster, deformed hand, extra fingers, glowing sci-fi sensor, low resolution
- Format: 4:5 vertical

### 6. e-nova-language-settings
- Class: hybrid
- Use: configuración o idioma solo después de validar el flujo real
- Modules: visual profile + documentary style + realism rules + framing rules (hybrid)
- Prompt:
  escena híbrida de configuración para e-Nova con el producto realista instalado en puerta, pomo exterior claramente reconocible, sensor centrado visible, tratamiento visual sobrio que sugiera configuración sin inventar pantalla o panel frontal en el hardware, composición limpia para artículo de ayuda
- Negative prompt:
  front display on the lock, keypad slab, readable fake settings text on the hardware, lever lock silhouette, camera cluster, oversized product body, cluttered background
- Format: 4:5 vertical

### 7. e-nova-app-add-device
- Class: realistic
- Use: agregar dispositivo en app
- Modules: visual profile + app pairing + documentary style + lighting standard + framing rules (app pairing)
- Prompt:
  persona adulta sosteniendo un smartphone cerca de una puerta con e-Nova instalada, pomo inteligente compacto claramente visible con sensor centrado, escena calmada de vinculación inicial, ambiente doméstico limpio, fotografía documental sobria, teléfono usado solo como apoyo contextual, alta definición
- Negative prompt:
  phone-only composition, fake readable app flow, lever lock body, keypad slab, camera cluster, marketing pose, cluttered background, exaggerated lifestyle styling
- Format: 4:3 horizontal

### 8. e-nova-link-qr
- Class: realistic
- Use: vinculación por QR solo si el flujo real existe para este producto
- Modules: visual profile + qr pairing + documentary style + framing rules (app pairing)
- Prompt:
  escena realista de vinculación contextual por QR entre smartphone y e-Nova, pomo inteligente compacto con sensor centrado claramente visible, código QR genérico en el teléfono como señal editorial, ambiente interior limpio, composición didáctica y sobria, fotografía técnica
- Negative prompt:
  scannable technical QR, keypad slab, lever lock silhouette, front display, fake instructions on screen, clutter, neon effects, oversized product
- Format: 4:3 horizontal

### 9. e-nova-troubleshoot-fingerprint
- Class: semi-realistic
- Use: no reconoce huella
- Modules: visual profile + fingerprint interaction + troubleshooting + documentary style
- Prompt:
  escena sobria de troubleshooting con una persona revisando el sensor de huella centrado de e-Nova, gesto neutro de comprobación, pomo exterior compacto claramente visible, composición limpia, ambiente doméstico ordenado, fotografía documental orientada a solución de problemas
- Negative prompt:
  alarmist acting, wrong sensor position, keypad slab, lever geometry, dramatic lighting, deformed hands, cluttered background
- Format: 4:5 vertical

### 10. e-nova-troubleshoot-app-connection
- Class: semi-realistic
- Use: no conecta a la app
- Modules: visual profile + troubleshooting + app pairing + documentary style
- Prompt:
  persona revisando una conexión de app frente a e-Nova instalada, teléfono y pomo inteligente visibles al mismo tiempo, producto compacto con rosetas circulares y sensor centrado, gesto leve de espera o revisión, ambiente doméstico limpio, estilo técnico sobrio
- Negative prompt:
  giant fake error dialog, lever lock silhouette, keypad slab, phone dominating the frame, camera cluster, clutter, exaggerated frustration, neon glow
- Format: 4:3 horizontal

### 11. e-nova-downloads-docs
- Class: hybrid
- Use: descargas y documentación
- Modules: visual profile + documentary style + framing rules (hero)
- Prompt:
  composición editorial sobria con e-Nova junto a documentación técnica o una tablet sobre una superficie limpia, pomo inteligente compacto claramente reconocible con sensor centrado, tonos neutros, iluminación suave, utilidad documental por encima de estética comercial
- Negative prompt:
  corporate brochure styling, wrong lock geometry, readable fake document text as main evidence, keypad slab, cluttered desk, plastic render look, low resolution
- Format: 16:9 horizontal

## First-wave generation order
1. `e-nova-hero-main`
2. `e-nova-installed-context`
3. `e-nova-fingerprint-use`
4. `e-nova-app-add-device`
5. `e-nova-troubleshoot-fingerprint`

## Notes
- Use real app captures when UI detail matters.
- Do not generate keypad-led imagery as if e-Nova had a flat numeric panel on the lock body.
- Treat `pin-use`, `language-settings`, and `link-qr` as conditional slots until the underlying feature flow is confirmed.