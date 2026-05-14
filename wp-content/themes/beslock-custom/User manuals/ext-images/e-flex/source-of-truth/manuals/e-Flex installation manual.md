# e-Flex
## Manual de instalacion normalizado para Beslock

## 1. Objetivo
Ordenar la preparacion de puerta, el montaje del cuerpo de cerradura y la validacion inicial de e-Flex usando la fuente OEM suplementaria disponible.

## 2. Que vas a instalar
e-Flex usa una arquitectura de placas largas frontal y trasera con:
- keypad superior en el panel exterior
- sensor de huella en la cara de la manija exterior
- compartimiento de baterias y boton `Reset` en el conjunto interior
- llave mecanica y alimentacion de emergencia en el conjunto exterior

## 3. Compatibilidad fisica antes de perforar
Valida estas condiciones antes de montar:
- el montaje usa panel frontal, panel trasero y cuerpo de cerradura separados
- el eje cuadrado debe sobresalir entre `10 y 30 mm` desde la superficie de la puerta
- si el saliente real excede ese rango, el husillo debe recortarse o pedirse a medida
- confirma mano de apertura y sentido del pestillo antes de fijar paneles

## 4. Que necesitas antes de empezar
- guia OEM disponible en `e-Flex_1.pdf`
- acceso a ambas caras y al canto de la puerta
- herramientas para cuerpo de cerradura, pernos y tornillos de montaje
- 4 baterias AA nuevas para la validacion inicial
- acceso a energia de emergencia y llave mecanica para la prueba final

## 5. Usar la guia de instalacion disponible
![Guia de instalacion de e-Flex](assets/e-flex/pdf-renders/e-flex-1/page-02.png)

La fuente nueva aporta una guia de montaje, no una plantilla 1:1 de perforacion.

Reglas de uso:
1. usa el PDF para secuencia, orientacion y despiece
2. no derives perforaciones finales a escala real desde una captura del PDF
3. confirma la mano de apertura antes de cambiar direccion de manija o pestillo

## 6. Preparar la puerta y el cuerpo del cerrojo
Secuencia base:
1. ajusta la direccion del pestillo segun el metodo de apertura de la puerta
2. inserta el cuerpo del cerrojo en el orificio preparado
3. aprieta los tornillos de montaje del cuerpo del cerrojo
4. confirma que el pestillo se mueva suavemente antes de presentar los paneles

## 7. Montar panel exterior e interior
Orden practico de montaje:
1. ajusta la direccion de la manija segun la apertura de la puerta
2. instala y aprieta los pernos de montaje en el panel frontal
3. inserta el resorte de manija en el panel trasero
4. coloca el eje cuadrado y recortalo si el grosor real de la puerta lo exige
5. pasa el cable de datos por el orificio superior correspondiente
6. alinea la manija y el eje cuadrado, y presiona el panel frontal contra la puerta
7. conecta el cable de datos al panel trasero
8. alinea el panel trasero con el eje y la barra de cerradura
9. aprieta los tornillos solo hasta corregir alineacion fina
10. cuando el pestillo se mueva sin friccion, completa el apriete final

## 8. Cambio de direccion
![Cambio de direccion de e-Flex](assets/e-flex/pdf-renders/e-flex-1/page-03.png)

### Cambio de direccion de la manija
1. afloja el tornillo de cambio de direccion
2. gira la manija `180°` hacia la parte superior de la cerradura
3. gira el cambiador de direccion
4. vuelve a apretar el tornillo

### Cambio de direccion del cuerpo del pestillo
1. empuja el interruptor de cambio hacia arriba
2. presiona el pestillo
3. gira el pestillo `180°`
4. completa el apriete final del tornillo de direccion

Nota critica:
- no retires los tornillos del orificio de la manija durante el cambio de direccion

## 9. Energia e inicializacion
Para la prueba inicial:
1. instala 4 baterias AA alcalinas de alto rendimiento
2. si el equipo fue manipulado durante montaje o prueba, realiza una inicializacion para limpiar huellas o datos temporales
3. valida el desbloqueo usando huella o contrasena inicial solo como prueba tecnica local
4. si el movimiento no es suave, corrige alineacion antes de cerrar con la tapa de baterias

## 10. Validacion despues de instalar
Antes de cerrar el trabajo, valida:
- la manija opera sin friccion ni juego excesivo
- el pestillo corre libre
- el keypad y el panel despiertan correctamente
- el boton `Reset` y el compartimiento de baterias quedan accesibles
- la llave mecanica y la energia de emergencia siguen disponibles

## 11. Precauciones clave
Segun la guia OEM:
- no cuelgues objetos en la manija
- aplica presion moderada al registrar huellas
- cambia las baterias con regularidad para evitar fugas
- despues de la primera alerta de bateria baja aun puede haber alrededor de `100` aperturas, pero conviene reemplazar pilas cuanto antes
- tras `5` intentos incorrectos consecutivos, el equipo puede bloquearse durante varios minutos

## 12. Relacion con el paquete documental
Dentro del paquete Beslock de e-Flex, este documento convive con:
- `e-Flex user manual - image-ready.md`
- `e-Flex app manual.md`
- `e-Flex - installation template standard.md`
- `e-Flex - supplemental source review.md`

## 13. Estado editorial
La base de instalacion queda suficientemente soportada por `e-Flex_1.pdf` y por el OEM ya procesado en `../../../../generated_manuals/e-flex/manual.md`.

Sigue pendiente para una version final de cliente:
- una plantilla de perforacion 1:1 si el proveedor la entrega
- validacion fisica del tiempo exacto de bloqueo y de cualquier password inicial que la guia corta mencione