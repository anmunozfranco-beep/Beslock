# e-Prime
## Revision de fuentes suplementarias OEM

## 1. Objetivo
Separar que aportan realmente los nuevos PDFs de e-Prime, que paginas son repeticion del OEM ya conocido, que dibujos enriquecen el contexto visual, y como deben entrar al estandar documental de Beslock.

## 2. Fuentes revisadas
- `e-Prime_1.pdf` -> manual tecnico corto en espanol con dibujos de layout, instalacion, cambio de direccion, funciones y precauciones
- `e-Prime_2.pdf` -> manual OEM mas amplio en chino, con layout, instalacion, flujo de inicializacion, administradores y operacion

## 3. Renders generados
- `assets/e-prime/pdf-renders/e-prime-1/page-01.png`
- `assets/e-prime/pdf-renders/e-prime-1/page-02.png`
- `assets/e-prime/pdf-renders/e-prime-1/page-03.png`
- `assets/e-prime/pdf-renders/e-prime-1/page-04.png`
- `assets/e-prime/pdf-renders/e-prime-1/page-05.png`
- `assets/e-prime/pdf-renders/e-prime-1/page-06.png`
- `assets/e-prime/pdf-renders/e-prime-1/contact-sheet.png`
- `assets/e-prime/pdf-renders/e-prime-2/page-01.png`
- `assets/e-prime/pdf-renders/e-prime-2/page-02.png`
- `assets/e-prime/pdf-renders/e-prime-2/page-03.png`
- `assets/e-prime/pdf-renders/e-prime-2/page-04.png`
- `assets/e-prime/pdf-renders/e-prime-2/page-05.png`
- `assets/e-prime/pdf-renders/e-prime-2/page-06.png`
- `assets/e-prime/pdf-renders/e-prime-2/page-07.png`
- `assets/e-prime/pdf-renders/e-prime-2/contact-sheet.png`

## 4. Clasificacion pagina por pagina

| Fuente | Paginas | Tipo real | Valor para Beslock | Decision editorial |
|---|---|---|---|---|
| `e-Prime_1.pdf` | 1 | portada con dibujo lineal del producto | medio | usar como referencia de identidad general, no como hero final |
| `e-Prime_1.pdf` | 2 | layout rotulado del hardware | alto | usar para reforzar geometria, nombres de zonas y contexto visual |
| `e-Prime_1.pdf` | 3 | despiece e instalacion con eje cuadrado | alto | usar para manual de instalacion y para prompts de montaje |
| `e-Prime_1.pdf` | 4 | pasos de instalacion | alto | usar como base primaria de instalacion normalizada |
| `e-Prime_1.pdf` | 5 | cambio de direccion + funciones del producto | alto | usar para manual de instalacion y conocimiento del producto |
| `e-Prime_1.pdf` | 6 | precauciones y bateria | medio-alto | usar como soporte de seguridad y mantenimiento |
| `e-Prime_2.pdf` | 1 a 3 | layout + instalacion + cambio de direccion en chino | medio | confirma la estructura OEM ya absorbida por OCR; valor principal de respaldo |
| `e-Prime_2.pdf` | 4 a 7 | flujos de inicializacion, administrador y operacion | medio | mayormente repeticion o confirmacion del manual OEM ya procesado en `../../../../generated_manuals/e-prime/manual.md` |

## 5. Conocimiento nuevo util para producto e imagenes
- e-Prime mantiene una placa larga y muy delgada con manijas rectas centradas y un cuerpo visual mas fino que e-Flex
- el keypad esta en la zona superior de la placa exterior y el aro azul permanece en el hub de la manija
- el modulo interior conserva un compartimiento de baterias, perilla interior y boton `SET` de inicializacion
- el eje cuadrado debe sobresalir `10 a 30 mm` desde la superficie de la puerta
- si el grosor de puerta supera ese rango de saliente, el husillo debe recortarse o pedirse a medida
- el producto soporta doble verificacion y declara hasta `9 administradores` y `300 usuarios` en la ficha corta, en contraste con el OCR previo que marcaba `100 usuarios`
- usa `4 pilas AA (1.5V)` y energia de emergencia `5V`

## 6. Repeticion y conflictos detectados
- `e-Prime_2.pdf` repite en gran parte el mismo OEM ya reflejado en `../../../../generated_manuals/e-prime/manual.md`
- existe conflicto de capacidad total: la ficha corta habla de `300 usuarios`, mientras el OCR previo del manual largo hablaba de `100 usuarios`
- no aparecio una plantilla de perforacion 1:1 comparable a la de e-Shield; lo nuevo para instalacion es una guia ilustrada de montaje, no un patron definitivo de corte a escala real

## 7. Decision Beslock
- usar `e-Prime_1.pdf` como fuente suplementaria principal para instalacion, geometria y contexto visual
- usar `e-Prime_2.pdf` como respaldo visual y confirmacion del OEM ya integrado al OCR principal
- normalizar un documento tecnico adicional de instalacion para e-Prime, pero dejar explicito que el PDF disponible es una guia de montaje, no una plantilla de perforacion 1:1

## 8. Impacto aplicado en el repo
- perfil visual de `e-Prime` ampliado con señales de layout interior, eje cuadrado y montaje
- prompts base de `e-Prime` reforzados para conservar la delgadez de la placa y la lectura correcta de instalacion
- nuevo `e-Prime installation manual.md` creado como base de instalacion normalizada
- nuevo `e-Prime - installation template standard.md` creado como anexo tecnico normalizado para la guia de instalacion disponible