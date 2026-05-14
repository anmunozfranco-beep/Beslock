# e-Prime
## Manual de app normalizado para Beslock

## 1. Objetivo
Explicar la vinculacion de e-Prime con red 2.4G y app movil a partir de la fuente OEM disponible, sin mezclar este flujo con el manual de uso ni con el manual de instalacion.

## 2. Fuente y alcance real
La fuente OCR disponible para app es breve.
Su bloque util se resume en:
- mini-programa de WeChat por QR
- `Doodle` / `TUYA APP`
- vinculacion de red `2.4G`
- secuencia local sobre la cerradura para activar el alta en red

Por eso este documento normaliza el flujo base, pero no pretende cubrir todos los modulos de la app.

## 3. Requisitos antes de vincular
- la cerradura debe tener al menos un administrador registrado
- el telefono debe tener instalada la app `TUYA`
- la red disponible debe ser `2.4G`
- debes estar junto a la cerradura para completar el alta

## 4. Flujo OEM base de vinculacion
Segun la fuente OCR, el flujo local de referencia es:
1. en la cerradura, despierta la pantalla con `*+#`
2. verifica la informacion de administrador
3. presiona `2` para `wireless settings`
4. presiona `1` para `add network`
5. abre `TUYA APP` en el telefono
6. sigue el asistente de la app para completar la distribucion de red

## 5. Alta desde la app
La guia OEM no muestra todos los textos internos de la aplicacion, asi que Beslock debe describir el flujo asi:
1. abre la app `TUYA`
2. elige agregar un nuevo dispositivo de cerradura inteligente
3. confirma la red `2.4G`
4. mantente cerca de la cerradura durante el proceso
5. completa el enlace y valida que el equipo aparezca en la cuenta

## 6. Mini-programa y QR
La fuente tambien indica que el codigo QR puede escanearse con `WeChat` para usar el mini-programa de apertura.

Regla editorial:
- tratar este flujo como opcion OEM observada
- no presentarlo como la unica experiencia de app si la implementacion comercial usa principalmente `TUYA`

## 7. Validacion despues del alta
Despues de enlazar el equipo:
- confirma que la cerradura aparece en la app
- valida una accion basica de sincronizacion o consulta de estado
- verifica que el alta no haya dejado la cerradura en modo de red abierto
- si el flujo falla, repite la secuencia local `*+#` con permisos de administrador

## 8. Limites de evidencia
- la fuente OEM disponible no detalla una guia extensa de modulos internos
- no hay suficiente evidencia aqui para describir historiales, usuarios remotos o automatizaciones avanzadas con el mismo nivel de certeza
- la app debe presentarse en Beslock como `TUYA` con red `2.4G`, salvo que una validacion posterior del producto comercial confirme otra variante

## 9. Estado editorial
Este manual de app queda normalizado como base operativa minima.

Antes de una version final para cliente, conviene validar en equipo real:
- nombres exactos de menus y botones de la app
- si el mini-programa de `WeChat` sigue vigente en la version comercial
- cualquier funcion remota adicional no visible en la fuente OEM resumida