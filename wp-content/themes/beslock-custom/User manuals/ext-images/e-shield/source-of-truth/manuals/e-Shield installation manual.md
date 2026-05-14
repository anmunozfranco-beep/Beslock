# e-Shield
## Manual de instalacion normalizado para Beslock

## 1. Objetivo
Explicar la preparacion de puerta, el uso correcto de la plantilla, el montaje base del hardware y las validaciones minimas despues de instalar e-Shield.

Este documento no reemplaza la plantilla impresa ni una validacion fisica en banco.
Su funcion es ordenar el proceso y separar lo que ya esta soportado por fuente OEM de lo que aun debe confirmarse en equipo real.

## 2. Que vas a instalar
e-Shield usa una arquitectura de cerradura dividida:
- modulo exterior vertical con lector circular en la parte superior y keypad debajo
- caja interior horizontal separada
- cilindro de seguridad tipo Clase C
- alimentacion principal con 4 baterias AA
- respaldo de energia por USB

## 3. Compatibilidad fisica antes de perforar
Valida estas condiciones antes de tocar la puerta:
- grosor compatible de puerta: `30 a 110 mm`
- tipos de puerta declarados por la fuente OEM: hierro, acero inoxidable o patio
- mano de apertura correcta segun la plantilla impresa
- espacio suficiente para que la caja interior horizontal quede alineada y no choque con marcos, vidrios o herrajes cercanos

## 4. Que necesitas antes de empezar
- plantilla impresa a escala `100%`
- acceso a la cara interior, exterior y canto de la puerta
- herramientas compatibles con las perforaciones marcadas en la plantilla
- baterias AA nuevas para la prueba inicial
- llave mecanica de respaldo para validacion final

## 5. Usar la plantilla de instalacion
![Plantilla de instalacion de e-Shield](assets/e-shield/pdf-renders/e-shield-2/page-01.png)

La plantilla OEM es la autoridad para la perforacion.

Reglas de uso:
1. imprime el PDF original sin ajuste de escala
2. confirma si la hoja visible corresponde a apertura derecha o si debes espejarla para apertura izquierda
3. alinea la referencia de `LATERAL DE PUERTA` exactamente con el canto de la puerta
4. respeta el retiro de borde visible de `60 mm`
5. marca sobre la puerta solo despues de confirmar que la impresion no fue reducida ni ampliada

## 6. Preparar la puerta
La plantilla muestra un patron principal y perforaciones auxiliares.

Control previo:
- perforacion circular principal: `32 mm`
- perforaciones auxiliares redondas: `6 mm`
- perforacion auxiliar mayor: `25 mm`
- abertura oblonga auxiliar: usar la plantilla impresa como referencia final

Secuencia recomendada:
1. fija temporalmente la plantilla en la cara correcta de la puerta
2. marca centros y contornos sin mover la hoja
3. perfora de forma controlada y limpia las rebabas
4. revisa desde ambos lados que el paso del cilindro y del cuerpo exterior quede libre
5. valida que el canto de la puerta permita el recorrido del pestillo sin rozamiento

## 7. Montar el conjunto exterior e interior
Orden practico de montaje:
1. presenta el cuerpo exterior manteniendo el lector arriba y el keypad debajo
2. pasa el cilindro y los elementos de union por las perforaciones ya validadas
3. presenta la caja interior horizontal desde la cara interna
4. alinea ambos cuerpos sin torsion ni inclinacion
5. ajusta la fijacion de forma gradual y alternada para no descentrar el conjunto
6. comprueba que el pestillo semiautomatico y el conjunto de cierre trabajen sin forzar la puerta

## 8. Energia y encendido inicial
Para la puesta en marcha:
1. instala 4 baterias AA nuevas
2. activa el panel exterior y confirma respuesta del teclado
3. si no hay energia disponible, usa respaldo USB solo como alimentacion temporal de emergencia
4. si el equipo llega con datos previos, usa el boton interno `SET` y sigue el flujo de voz del equipo para restaurar el modo de fabrica

Nota editorial:
La secuencia exacta de teclas de restauracion aparece inconsistente entre OCR y ficha OEM, asi que no debe fijarse como claim definitivo hasta validar el hardware real.

## 9. Validacion despues de instalar
Antes de entregar el equipo o pasar a configuracion de usuarios, valida esto:
- la puerta cierra y abre sin roce anormal
- el cuerpo exterior queda vertical y la caja interior queda estable
- el teclado despierta y responde al tacto
- la llave mecanica abre y cierra correctamente
- el puerto USB de emergencia sigue accesible
- el boton interior y el pestillo responden sin retrasos ni holguras anormales

## 10. Problemas frecuentes de instalacion
### La plantilla no coincide con la puerta
- revisa escala de impresion al `100%`
- confirma mano de apertura correcta
- no reconstruyas cotas a ojo desde una captura de pantalla

### El pestillo roza o no corre libre
- revisa alineacion entre cuerpo exterior, caja interior y eje del pestillo
- confirma que no haya rebabas o desviacion en la perforacion principal

### El panel no enciende
- verifica polaridad y carga de las 4 baterias AA
- usa USB solo como prueba de energia de emergencia
- confirma que el conector interno no haya quedado forzado durante el montaje

## 11. Relacion con el paquete documental
Dentro del estandar Beslock para e-Shield, este documento convive con:
- `e-Shield user manual - image-ready.md`
- `e-Shield - installation template standard.md`
- `e-Shield - supplemental source review.md`

Documento aun pendiente en forma dedicada:
- manual de app normalizado

## 12. Estado editorial
Este manual se apoya en tres fuentes: OCR del manual OEM existente, la ficha suplementaria `e-Shield_1.pdf` y la plantilla `e-Shied_2.pdf`.

La compatibilidad fisica, las medidas visibles y la arquitectura del hardware estan suficientemente soportadas para una base de instalacion normalizada.
La secuencia mecanica fina y cualquier combinacion exacta de teclas deben validarse sobre producto real antes de publicarse como instalacion definitiva para cliente final.