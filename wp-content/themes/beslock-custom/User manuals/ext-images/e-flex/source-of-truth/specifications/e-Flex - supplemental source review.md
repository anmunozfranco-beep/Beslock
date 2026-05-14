# e-Flex
## Revision de fuente suplementaria OEM

## 1. Objetivo
Separar que aporta realmente `e-Flex_1.pdf`, que paginas son repeticion OEM, que dibujos enriquecen el contexto visual y como debe integrarse este conocimiento al paquete documental de Beslock.

## 2. Fuente revisada
- `e-Flex_1.pdf` -> manual corto en ingles con layout, instalacion, cambio de direccion, precauciones, flujos de administracion, mini-programa de WeChat y provisioning por `TUYA`

## 3. Renders generados
- `assets/e-flex/pdf-renders/e-flex-1/page-01.png`
- `assets/e-flex/pdf-renders/e-flex-1/page-02.png`
- `assets/e-flex/pdf-renders/e-flex-1/page-03.png`
- `assets/e-flex/pdf-renders/e-flex-1/page-04.png`
- `assets/e-flex/pdf-renders/e-flex-1/page-05.png`
- `assets/e-flex/pdf-renders/e-flex-1/page-06.png`
- `assets/e-flex/pdf-renders/e-flex-1/page-07.png`
- `assets/e-flex/pdf-renders/e-flex-1/page-08.png`
- `assets/e-flex/pdf-renders/e-flex-1/contact-sheet.png`

## 4. Clasificacion pagina por pagina

| Pagina | Tipo real | Valor para Beslock | Decision editorial |
|---|---|---|---|
| 1 | layout del producto | alto | usar para reforzar geometria exterior/interior, bateria, reset y llave mecanica |
| 2 | despiece e instalacion | alto | usar como base de manual de instalacion y contexto visual de montaje |
| 3 | cambio de direccion + funciones del producto | alto | usar para instalacion y conocimiento del hardware |
| 4 | precauciones + flujo de administradores | medio-alto | usar para soporte editorial y operacion local, no como plantilla visual principal |
| 5 | flujo de user settings | medio | confirma la estructura OEM de configuracion local |
| 6 | flujo de lock settings | medio | confirma always open, dual verification, alarma y silencio |
| 7 | mini-programa WeChat por QR | medio | tratar como flujo OEM observado, no como experiencia universal garantizada |
| 8 | `Doodle/TUYA APP` y alta de red 2.4G | alto | usar para manual de app normalizado y contexto visual de vinculacion |

## 5. Conocimiento nuevo util para producto e imagenes
- el interior muestra compartimiento de baterias, boton `Reset` dentro del battery compartment, control interior simple y placa larga trasera
- el exterior confirma keypad superior, lector de huella en la cara de la manija y acceso a llave mecanica
- la instalacion usa eje cuadrado con saliente recomendado de `10 a 30 mm`
- si el grosor de puerta excede ese rango de saliente, el husillo debe cortarse o pedirse a medida
- la fuente OEM corta confirma modo siempre abierto, doble verificacion, alarma anti-palanca, silencio, control de volumen y cambio de idioma chino/ingles
- la vinculacion de app se describe con red `2.4G`, app `TUYA` y secuencia local `*+# -> wireless settings -> add network`

## 6. Repeticion y limites
- la nueva fuente no es una plantilla de perforacion 1:1; es una guia ilustrada de instalacion y operacion
- parte de la logica de producto ya estaba presente en `../../../../generated_manuals/e-flex/manual.md`
- el bloque de mini-programa `WeChat` debe tratarse como opcion OEM observada, no como promesa transversal de la linea comercial

## 7. Decision Beslock
- usar `e-Flex_1.pdf` como fuente suplementaria principal para instalacion, layout y provisioning de app
- crear manual de instalacion y manual de app normalizados a partir de esta fuente
- crear un anexo tecnico de instalacion que explique que hoy no existe una plantilla 1:1 de perforacion dentro del material recibido

## 8. Impacto aplicado en el repo
- perfil visual de `e-Flex` ampliado con layout interior y detalles de montaje
- prompts base de `e-Flex` reforzados con identidad fisica mas precisa
- nuevo `e-Flex installation manual.md` creado como base de instalacion normalizada
- nuevo `e-Flex app manual.md` creado como base normalizada de app
- nuevo `e-Flex - installation template standard.md` creado como anexo tecnico para la guia de instalacion disponible