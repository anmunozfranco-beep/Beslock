# e-Prime
## Manual de instalacion normalizado para Beslock

## 1. Objetivo
Ordenar la preparacion de puerta, el montaje de paneles y la validacion inicial de e-Prime usando las fuentes OEM disponibles sin mezclar instalacion con uso diario o app.

## 2. Que vas a instalar
e-Prime es una cerradura de placa larga y delgada con:
- panel exterior brillante con keypad en la zona superior
- manija recta centrada con aro azul en el hub
- inserto oval inferior en la cara frontal
- panel interior con compartimiento de baterias, perilla interior y boton `SET`

## 3. Compatibilidad fisica antes de perforar
Valida estas condiciones antes de montar:
- el producto usa cuerpo de cerradura y paneles delantero/trasero separados
- el eje cuadrado debe sobresalir entre `10 y 30 mm` desde la superficie de la puerta
- si el saliente real no cae en ese rango, el husillo debe recortarse o pedirse a medida
- confirma mano de apertura y sentido de pestillo antes de fijar paneles

## 4. Que necesitas antes de empezar
- guia OEM de instalacion disponible en `e-Prime_1.pdf`
- acceso a ambas caras y al canto de la puerta
- herramientas compatibles con el cuerpo del cerrojo y los tornillos de montaje
- 4 pilas AA nuevas para la prueba inicial
- llave mecanica de respaldo y acceso a fuente de 5V para emergencia

## 5. Usar la guia de instalacion disponible
![Guia de instalacion de e-Prime](assets/e-prime/pdf-renders/e-prime-1/page-04.png)

La fuente nueva de e-Prime aporta una guia ilustrada de montaje, no una plantilla de perforacion 1:1.

Reglas de uso:
1. usa el PDF como referencia de secuencia y orientacion de piezas
2. no derives perforaciones finales a escala real desde una captura de este PDF
3. valida el sentido de apertura antes de cambiar direccion de manija o pestillo

## 6. Preparar la puerta y el cerrojo
Secuencia base:
1. ajusta la direccion del pestillo segun el metodo de apertura de la puerta
2. inserta el cuerpo del cerrojo en el hueco preparado
3. aprieta los tornillos de montaje del cuerpo del cerrojo
4. confirma que el pestillo corre libre antes de presentar los paneles

## 7. Montar el panel exterior e interior
Orden practico de montaje:
1. ajusta la direccion de la manija segun la apertura de la puerta
2. instala los pernos de montaje en el panel frontal y prepara el resorte de manija para el panel trasero
3. inserta el eje cuadrado y cortalo si el grosor real de la puerta lo exige
4. pasa el cable de datos por el orificio superior correspondiente
5. alinea el orificio cuadrado de la manija con el eje y presiona el panel frontal contra la puerta
6. conecta el cable de datos al panel trasero
7. alinea el panel trasero con el eje cuadrado y la barra de cerradura
8. aprieta los tornillos de montaje solo hasta poder corregir la alineacion fina
9. cuando el pestillo se mueva suavemente, completa el apriete final

## 8. Cambio de direccion
![Cambio de direccion de e-Prime](assets/e-prime/pdf-renders/e-prime-1/page-05.png)

### Cambio de direccion de la manija
1. afloja el tornillo de cambio de direccion
2. gira la manija `180°` hacia la parte superior de la cerradura
3. gira el cambiador de direccion
4. vuelve a apretar el tornillo

### Cambio de direccion del cuerpo de cerradura
1. empuja el interruptor de cambio hacia arriba
2. presiona el pestillo
3. gira el pestillo `180°`

Nota critica:
- no retires los tornillos del orificio de la manija al cambiar la direccion

## 9. Energia e inicializacion
Para la prueba inicial:
1. instala 4 pilas AA alcalinas de alto rendimiento
2. realiza la inicializacion para borrar datos de prueba de instalacion si el equipo es nuevo o ya fue manipulado
3. valida apertura por huella o por contrasena inicial solo como prueba tecnica local
4. coloca la tapa de baterias una vez que el movimiento mecanico y la verificacion sean correctos

## 10. Validacion despues de instalar
Antes de cerrar el trabajo, valida:
- la manija trabaja sin friccion ni holgura excesiva
- el pestillo corre libre y no roza
- el panel exterior queda recto y estable
- el panel interior no fuerza el cableado ni el eje cuadrado
- la perilla interior, la llave mecanica y la energia de emergencia de `5V` siguen accesibles

## 11. Precauciones clave
Segun la fuente corta en espanol:
- no cuelgues objetos en la manija
- no presiones en exceso el lector de huellas al registrar usuarios
- reemplaza las baterias al menos una vez cada seis meses para reducir riesgo de fuga
- tras la primera alerta de bateria baja todavia puede haber alrededor de `100` aperturas disponibles, pero conviene cambiar las pilas de inmediato
- despues de `5` intentos incorrectos consecutivos la cerradura puede quedar inoperable durante `90 segundos`

## 12. Relacion con el paquete documental
Dentro del paquete Beslock de e-Prime, este documento convive con:
- `e-Prime user manual - image-ready.md`
- `e-Prime - installation template standard.md`
- `e-Prime - supplemental source review.md`

Documento aun pendiente en forma dedicada:
- manual de app normalizado

## 13. Estado editorial
La base de instalacion ya esta suficientemente soportada por `e-Prime_1.pdf` y por el OEM largo ya procesado en `../../../../generated_manuals/e-prime/manual.md`.

Lo que sigue pendiente antes de una version final de cliente:
- confirmar el patron exacto de perforacion con una plantilla 1:1 si el proveedor la entrega
- validar en producto real la capacidad total final cuando la ficha corta y el manual largo no coinciden