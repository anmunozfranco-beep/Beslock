# e-Prime AI Image Prompts

## Purpose
This is the canonical e-Prime prompt pack inside the operational visual system.

It migrates the legacy flat prompt document into the product-local control surface and rewrites it around the new system rules:
- product truth from `../../../ext-images/e-prime/e-prime-visual-profile.md`
- realism class from `../../shared/visual-rules/realism-vs-schematic.md`
- reusable modules from `../../shared/`

## Assembly rule
Build each prompt from:
1. e-Prime visual profile
2. image class
3. interaction module when needed
4. documentary style
5. lighting standard
6. master negative prompt plus e-Prime-specific restrictions

## Shared negative base
marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look

## Product-specific negative additions
heavy long-plate silhouette, knob lock silhouette, camera cluster, face-recognition screen, fingerprint sensor on handle tip, fingerprint sensor on panel center, missing lower oval insert, bulky futuristic redesign

## Prompt pack

### 1. e-prime-hero-main
- Class: realistic
- Use: hub principal y orientación del producto
- Modules: visual profile + documentary style + lighting standard + realism rules + framing rules (hero)
- Prompt:
  e-Prime instalada en una puerta residencial real, cerradura inteligente de palanca con placa vertical muy delgada y acabado negro brillante en la cara exterior, manija recta centrada, aro azul en el hub de la manija exterior, zona superior de control integrada y óvalo inferior presente bajo la manija, iluminación neutra suave, reflejos controlados, composición clara para centro de ayuda, fotografía documental técnica, alta definición, sin estética comercial exagerada
- Negative prompt:
  marketing glamor, cinematic drama, futuristic redesign, invented UI text, fake labels, wrong geometry, extra cameras, extra sensors, warped handles, distorted proportions, unreadable reflections, deformed hands, extra fingers, floating objects, cluttered background, neon lighting, low resolution, plastic render look, heavy long-plate silhouette, knob lock silhouette, camera cluster, face-recognition screen, fingerprint sensor on handle tip, fingerprint sensor on panel center, missing lower oval insert
- Format: 16:9 horizontal

### 2. e-prime-installed-context
- Class: realistic
- Use: primeros pasos e identidad instalada
- Modules: visual profile + documentary style + lighting standard + framing rules (hero)
- Prompt:
  e-Prime ya instalada y lista para uso en una puerta de apartamento o casa, cerradura de palanca con placa larga y muy delgada claramente visible, cara exterior brillante, manija recta con aro azul en el hub, inserto oval inferior presente, ambiente doméstico limpio y realista, fotografía documental sobria, luz natural equilibrada, materiales negros creíbles, composición útil para guía técnica
- Negative prompt:
  generic smart lock, heavy e-Flex-like body, knob silhouette, fingerprint sensor on wrong location, camera cluster, exaggerated reflections, cluttered background, oversized hardware, low resolution
- Format: 4:3 horizontal

### 3. e-prime-add-admin-action
- Class: semi-realistic
- Use: agregar administrador
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  primer plano realista de una mano adulta interactuando con la zona superior de control de e-Prime, placa larga y delgada visible, manija recta centrada con aro azul en el hub aún reconocible, óvalo inferior presente, acción única y clara de configuración, composición limpia, fondo discreto, iluminación suave, estilo técnico documental
- Negative prompt:
  fingerprint touch on the hub instead of keypad for this scene, heavy e-Flex silhouette, knob lock body, keypad moved to another area, deformed hand, extra fingers, extreme angle, fake readable interface, cluttered frame
- Format: 4:5 vertical

### 4. e-prime-pin-use
- Class: semi-realistic
- Use: ingreso por PIN
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  detalle de e-Prime mostrando una mano adulta usando la zona numérica o táctil superior, placa delgada brillante, manija exterior y aro azul del hub aún reconocibles, inserto oval inferior presente, acción clara, iluminación neutra, fotografía de ayuda sobria y de alta claridad, sin depender de números generados como prueba técnica
- Negative prompt:
  readable fake digits carrying instruction meaning, heavy long-plate body, knob silhouette, keypad on handle, missing lower oval insert, camera cluster, deformed fingers, noisy reflections, cluttered frame
- Format: 4:5 vertical

### 5. e-prime-fingerprint-use
- Class: realistic
- Use: registrar huella y soporte de huella
- Modules: visual profile + fingerprint interaction + documentary style + lighting standard + framing rules (interaction)
- Prompt:
  primer plano realista de una persona usando el sensor de huella de e-Prime ubicado en el hub de la manija exterior, dedo alineado naturalmente con el aro azul real, placa larga y delgada aún reconocible, inserto oval inferior presente, fondo neutro desenfocado, reflejos suaves sobre negro, composición didáctica, fotografía documental
- Negative prompt:
  touching the panel instead of the hub sensor, fingerprint sensor on handle tip, fingerprint sensor on panel center, heavy e-Flex silhouette, knob lock, camera cluster, deformed hand, extra fingers, glowing sci-fi sensor, low resolution
- Format: 4:5 vertical

### 6. e-prime-language-settings
- Class: semi-realistic
- Use: configuración o idioma
- Modules: visual profile + keypad interaction + documentary style + framing rules (interaction)
- Prompt:
  escena sobria de configuración para e-Prime con mano adulta interactuando en la zona superior de control, placa delgada brillante, manija exterior y hub con aro azul bien diferenciados, inserto oval inferior visible, composición limpia para artículo de ayuda, iluminación suave, realismo técnico, sin depender de texto generado en pantalla
- Negative prompt:
  readable fake settings text, heavy body, knob silhouette, fingerprint sensor on wrong zone, camera cluster, futuristic interface, cluttered background, extreme reflections, missing lower oval insert
- Format: 4:5 vertical

### 7. e-prime-app-add-device
- Class: realistic
- Use: agregar dispositivo en app
- Modules: visual profile + app pairing + documentary style + lighting standard + framing rules (app pairing)
- Prompt:
  persona adulta sosteniendo un smartphone cerca de una puerta con e-Prime instalada, cerradura de palanca con placa larga y delgada claramente visible, cara exterior brillante, aro azul en el hub de la manija y óvalo inferior presentes, escena calmada de vinculación inicial, ambiente doméstico limpio, fotografía documental sobria, teléfono usado solo como apoyo contextual, alta definición
- Negative prompt:
  phone-only composition, fake readable app flow, heavy e-Flex body, knob lock body, camera cluster, marketing pose, cluttered background, exaggerated lifestyle styling, missing lower oval insert
- Format: 4:3 horizontal

### 8. e-prime-link-qr
- Class: realistic
- Use: vinculación por QR
- Modules: visual profile + qr pairing + documentary style + framing rules (app pairing)
- Prompt:
  escena realista de vinculación contextual por QR entre smartphone y e-Prime, cerradura de palanca con placa larga y delgada, cara brillante y aro azul en el hub claramente visibles, código QR genérico en el teléfono como señal editorial, ambiente interior limpio, composición didáctica y sobria, fotografía técnica
- Negative prompt:
  scannable technical QR, heavy body, knob silhouette, camera cluster, fake instructions on screen, clutter, neon effects, fingerprint sensor on wrong area, missing lower oval insert
- Format: 4:3 horizontal

### 9. e-prime-troubleshoot-fingerprint
- Class: semi-realistic
- Use: no reconoce huella
- Modules: visual profile + fingerprint interaction + troubleshooting + documentary style
- Prompt:
  escena sobria de troubleshooting con una persona revisando el sensor de huella de e-Prime en el hub de la manija exterior, gesto neutro de comprobación, placa delgada, cara brillante y óvalo inferior aún visibles, composición limpia, ambiente doméstico ordenado, fotografía documental para solución de problemas
- Negative prompt:
  alarmist acting, wrong sensor position, heavy body, knob silhouette, dramatic lighting, deformed hands, cluttered background, missing lower oval insert
- Format: 4:5 vertical

### 10. e-prime-troubleshoot-app-connection
- Class: semi-realistic
- Use: no conecta a la app
- Modules: visual profile + troubleshooting + app pairing + documentary style
- Prompt:
  persona revisando una conexión de app frente a e-Prime instalada, teléfono y cerradura visibles al mismo tiempo, placa larga y delgada, manija recta con aro azul en el hub y óvalo inferior reconocibles, gesto leve de espera o revisión, ambiente doméstico limpio, estilo técnico sobrio
- Negative prompt:
  giant fake error dialog, knob silhouette, heavy body, phone dominating the frame, camera cluster, clutter, exaggerated frustration, neon glow, missing lower oval insert
- Format: 4:3 horizontal

### 11. e-prime-downloads-docs
- Class: hybrid
- Use: descargas y documentación
- Modules: visual profile + documentary style + framing rules (hero)
- Prompt:
  composición editorial sobria con e-Prime junto a documentación técnica o una tablet sobre una superficie limpia, cerradura de palanca con placa larga y delgada claramente reconocible, cara exterior brillante, aro azul en el hub y óvalo inferior visibles, tonos neutros, iluminación suave, utilidad documental por encima de estética comercial
- Negative prompt:
  corporate brochure styling, wrong lock geometry, readable fake document text as main evidence, knob silhouette, cluttered desk, plastic render look, low resolution, missing lower oval insert
- Format: 16:9 horizontal

## First-wave generation order
1. `e-prime-hero-main`
2. `e-prime-installed-context`
3. `e-prime-fingerprint-use`
4. `e-prime-add-admin-action`
5. `e-prime-app-add-device`
6. `e-prime-pin-use`

## Notes
- Use real app captures when UI detail matters.
- Keep the fingerprint sensor at the lever hub, not at the tip or on the panel.
- Preserve the lower oval insert in medium and wide shots.
- Do not let e-Prime drift into e-Flex's heavier silhouette.
