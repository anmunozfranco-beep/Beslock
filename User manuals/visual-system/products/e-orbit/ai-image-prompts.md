# e-Orbit AI Image Prompts

## Purpose
This is the canonical e-Orbit prompt pack inside the operational visual system.

It migrates the legacy flat prompt document into the product-local control surface and rewrites it around the new system rules:
- product truth from `../../../ext-images/e-orbit/e-orbit-visual-profile.md`
- realism class from `../../shared/visual-rules/realism-vs-schematic.md`
- reusable modules from `../../shared/`

## Assembly rule
Build each prompt from:
1. e-Orbit visual profile
2. image class
3. interaction module when needed
4. documentary style
5. lighting standard
6. master negative prompt plus e-Orbit-specific restrictions

## Shared negative base
marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, missing interior screen, rim-lock box geometry

## Prompt pack

### 1. e-orbit-hero-main
- Class: realistic
- Use: hub principal y orientación del producto
- Modules: visual profile + documentary style + lighting standard + realism rules + framing rules (hero)
- Prompt:
  e-Orbit instalada en una puerta residencial real, cerradura inteligente alta de cuerpo monolítico con panel frontal brillante, conjunto superior de sensores o cámara visible, zona de display separada, teclado táctil en el frente, manija exterior robusta y esculpida con sensor de huella cerca de la parte superior de la manija, fotografía documental técnica, ambiente interior limpio, luz neutra suave, reflejos controlados sobre superficies negras, composición útil para centro de ayuda, alta definición, sin estética publicitaria
- Negative prompt:
  marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look, standard keypad lever lock silhouette, knob lock silhouette, fingerprint sensor on the front panel, missing upper sensor cluster, merged display and handle, rim-lock box geometry
- Format: 16:9 horizontal

### 2. e-orbit-installed-context
- Class: realistic
- Use: primeros pasos e identidad instalada
- Modules: visual profile + documentary style + lighting standard + framing rules (hero)
- Prompt:
  e-Orbit ya instalada y lista para uso en una puerta de apartamento o casa, cuerpo alto y vertical claramente visible, conjunto superior de sensores presente, teclado frontal y manija exterior diferenciados, contexto doméstico sobrio y ordenado, luz natural equilibrada, fotografía documental realista, composición clara para guía técnica, materiales negros creíbles y reflejos suaves
- Negative prompt:
  marketing glamor, dramatic storytelling, wrong geometry, knob lock silhouette, simplified generic smart lock, cluttered background, dark unreadable panel, fake screen text, missing upper sensor cluster
- Format: 4:3 horizontal

### 3. e-orbit-add-admin-action
- Class: semi-realistic
- Use: agregar administrador
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  primer plano de una mano adulta interactuando con el área de teclado de e-Orbit instalada en una puerta, cuerpo alto del producto visible, conjunto superior de sensores aún reconocible, manija exterior separada del panel, acción única y clara de configuración de administrador, fotografía técnica sobria, fondo discreto, iluminación suave, encuadre vertical útil para documentación
- Negative prompt:
  deformed hands, extra fingers, fingerprint touch on wrong zone, fake readable interface, extreme angle, generic lever lock body, merged panel and handle, dramatic lighting, cluttered background
- Format: 4:5 vertical

### 4. e-orbit-pin-use
- Class: semi-realistic
- Use: ingreso de PIN
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  detalle de e-Orbit mostrando la mano de un usuario ingresando un PIN en la zona de teclado frontal, panel brillante legible, conjunto superior de sensores parcialmente visible, manija exterior separada, foco técnico en la acción, iluminación neutra, fotografía de ayuda de alta claridad
- Negative prompt:
  readable but wrong numbers, fake UI, wrong lock family, knob silhouette, fingerprint sensor on panel center, deformed fingers, noisy reflections, cluttered frame
- Format: 4:5 vertical

### 5. e-orbit-fingerprint-use
- Class: realistic
- Use: registrar huella y soporte de huella
- Modules: visual profile + fingerprint interaction + documentary style + lighting standard + framing rules (interaction)
- Prompt:
  primer plano realista de una persona usando el sensor de huella de e-Orbit en la parte superior de la manija exterior, dedo alineado de forma natural con el sensor real, panel frontal y cuerpo del producto aún reconocibles, reflejos suaves sobre negro brillante, fondo neutro desenfocado, composición didáctica, fotografía documental de alta definición
- Negative prompt:
  touching the front panel instead of the handle sensor, oversized glowing sensor effect, wrong handle shape, missing upper sensor cluster, deformed hand, extra fingers, low resolution, plastic render look
- Format: 4:5 vertical

### 6. e-orbit-language-settings
- Class: semi-realistic
- Use: cambiar idioma o configuración del panel
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  e-Orbit en escena de configuración mostrando mano adulta interactuando con la zona frontal de control, display y teclado claramente diferenciados, conjunto superior de sensores presente, composición limpia para artículo de ayuda, luz suave, realismo sobrio, sin depender de texto generado en pantalla
- Negative prompt:
  readable fake settings text, futuristic interface, missing sensors, generic keypad slab, deformed hand, extreme reflections, cluttered background
- Format: 4:5 vertical

### 7. e-orbit-app-add-device
- Class: realistic
- Use: agregar dispositivo en Smart Life
- Modules: visual profile + app pairing + documentary style + lighting standard + framing rules (app pairing)
- Prompt:
  persona adulta sosteniendo un smartphone cerca de una puerta con e-Orbit instalada, cerradura claramente reconocible con cuerpo alto, conjunto superior de sensores y manija exterior diferenciada, escena calmada de vinculación inicial, ambiente doméstico limpio, fotografía documental, pantalla del teléfono solo como apoyo contextual, alta definición
- Negative prompt:
  phone-only composition, fake readable app flow, marketing pose, wrong lock geometry, knob lock silhouette, missing handle sensor, dramatic lifestyle styling
- Format: 4:3 horizontal

### 8. e-orbit-link-qr
- Class: realistic
- Use: vinculación por QR
- Modules: visual profile + qr pairing + documentary style + framing rules (app pairing)
- Prompt:
  escena realista de vinculación por QR entre un smartphone y e-Orbit, teléfono cerca de la cerradura mostrando un código QR genérico como señal contextual, producto claramente identificable con sensores superiores, teclado frontal y manija exterior separados, fondo interior limpio, composición didáctica y sobria
- Negative prompt:
  scannable technical QR, fake detailed instructions on screen, wrong lock family, merged handle and panel, neon effects, floating UI, cluttered background
- Format: 4:3 horizontal

### 9. e-orbit-troubleshoot-fingerprint
- Class: semi-realistic
- Use: no reconoce huella
- Modules: visual profile + fingerprint interaction + troubleshooting + documentary style
- Prompt:
  escena sobria de troubleshooting con una persona revisando el sensor de huella de e-Orbit ubicado en la parte alta de la manija exterior, gesto neutro de comprobación, foco claro en la zona de contacto, producto aún identificable, fondo limpio, fotografía documental para solución de problemas
- Negative prompt:
  alarmist acting, exaggerated frustration, touching wrong sensor location, wrong lock silhouette, deformed hands, dramatic lighting, cluttered background
- Format: 4:5 vertical

### 10. e-orbit-troubleshoot-app-connection
- Class: semi-realistic
- Use: no conecta a la app
- Modules: visual profile + troubleshooting + app pairing + documentary style
- Prompt:
  persona revisando una conexión de app frente a e-Orbit instalada, teléfono y cerradura visibles al mismo tiempo, producto mantiene su cuerpo alto con sensores superiores, teclado y manija diferenciados, gesto leve de espera o revisión, ambiente doméstico ordenado, estilo técnico sobrio
- Negative prompt:
  giant fake error dialog, marketing scene, wrong lock family, missing upper sensor cluster, phone dominating the frame, clutter, neon glow
- Format: 4:3 horizontal

### 11. e-orbit-downloads-docs
- Class: hybrid
- Use: descargas y documentación
- Modules: visual profile + documentary style + framing rules (hero)
- Prompt:
  composición editorial sobria con e-Orbit junto a documentación técnica o una tablet en una superficie limpia, producto claramente reconocible con cuerpo alto, sensores superiores y manija robusta, tonos neutros, iluminación suave, utilidad documental por encima de estética comercial
- Negative prompt:
  corporate brochure styling, unreadable document text as key content, wrong lock geometry, cluttered desk, plastic render, low resolution
- Format: 16:9 horizontal

## First-wave generation order
1. `e-orbit-hero-main`
2. `e-orbit-installed-context`
3. `e-orbit-fingerprint-use`
4. `e-orbit-app-add-device`
5. `e-orbit-link-qr`
6. `e-orbit-add-admin-action`
7. `e-orbit-language-settings`

## Notes
- Use real app captures when UI detail matters.
- Reject any output that moves the fingerprint sensor from the exterior handle to the front panel.
- Reject any output that removes the upper sensor cluster.
