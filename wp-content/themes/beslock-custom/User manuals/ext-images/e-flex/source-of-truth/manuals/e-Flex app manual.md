# e-Flex
## Manual de app normalizado para Beslock

## 1. Objetivo
Explicar el flujo base de vinculacion de e-Flex con `TUYA APP` y la red `2.4G`, sin mezclarlo con instalacion mecanica ni con el manual de uso.

## 2. Alcance real de la fuente
La fuente OEM suplementaria muestra un flujo de alta corto y dos referencias de ecosistema:
- `TUYA APP`
- mini-programa `WeChat` por QR

La evidencia fuerte esta en la provision de red y en la secuencia local sobre la cerradura.

## 3. Requisitos antes de vincular
- debe existir al menos un administrador en la cerradura
- el telefono debe tener instalada `TUYA APP`
- la red debe ser `2.4G`
- debes estar junto a la cerradura para completar el proceso

## 4. Secuencia local en la cerradura
La fuente OEM resume este flujo local:
1. despierta la pantalla con `*+#`
2. verifica la informacion del administrador
3. presiona `2` para `wireless settings`
4. presiona `1` para `add network`

## 5. Alta desde TUYA APP
Una vez habilitado el modo de red en la cerradura:
1. abre `TUYA APP`
2. agrega una nueva cerradura inteligente desde la categoria correcta
3. confirma la red `2.4G`
4. sigue el asistente de la app hasta completar el enlace
5. valida que el equipo aparezca correctamente en la cuenta

## 6. QR y mini-programa de WeChat
La guia tambien indica que el QR puede escanearse con `WeChat` para usar el mini-programa de apertura.

Regla editorial:
- tratar este flujo como opcion OEM observada
- no presentarlo como canal unico ni como experiencia principal si la implementacion comercial usa `TUYA` como ruta primaria

## 7. Validacion despues del alta
Despues de enlazar el equipo:
- confirma presencia del dispositivo en la app
- valida una sincronizacion o lectura basica de estado
- revisa que el equipo salga correctamente del modo de red abierto
- si el flujo falla, repite la secuencia local con permisos de administrador

## 8. Limites de evidencia
- la guia corta no aporta un mapa completo de modulos internos de la app
- no hay suficiente evidencia aqui para prometer flujos avanzados de automatizacion o permisos remotos detallados
- la experiencia de Beslock debe describirse como vinculacion `TUYA` sobre red `2.4G`, con mini-programa `WeChat` solo como apoyo OEM observado

## 9. Estado editorial
Este manual de app queda normalizado como base operativa minima.

Antes de una version final para cliente conviene validar:
- nombre exacto de la app en la implementacion comercial
- vigencia real del mini-programa de `WeChat`
- textos exactos de menus y botones durante el alta