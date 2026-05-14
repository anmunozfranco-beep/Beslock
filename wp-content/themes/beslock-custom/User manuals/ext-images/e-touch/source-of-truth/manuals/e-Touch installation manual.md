# e-Touch
## Manual de instalacion normalizado para Beslock

## 1. Objetivo
Ordenar la instalacion fisica de e-Touch usando la guia OEM suplementaria disponible, sin confundirla con una plantilla de perforacion a escala real.

## 2. Arquitectura fisica observada
e-Touch se instala como un conjunto compacto de rosetas circulares y manijas, no como una cerradura de placa larga.

El PDF suplementario confirma estos componentes:
- `front handle`
- `rear handle`
- `rear cover with battery`
- `deadbolt`
- `connecting pipe` largo y corto
- tornillos de fijacion y tapa
- `E-key`
- buckle cover y piezas de montaje

## 3. Compatibilidad antes de montar
Antes de fijar el conjunto:
- valida el sentido de apertura interior/exterior y la direccion del pestillo
- confirma que la posicion del agujero se ajuste a la posicion real del cuerpo de cerradura
- elige la longitud de tornilleria o separadores segun el grosor de la puerta
- prepara el paso del eje cuadrado y del cableado antes de cerrar las manijas

## 4. Rol de la guia OEM disponible
![Guia OEM de e-Touch](assets/e-touch/pdf-renders/e-touch-1/page-01.png)

La fuente nueva funciona como guia de montaje paso a paso.
No funciona como plantilla 1:1 de perforacion.

Reglas de uso:
1. usar el PDF para orden de montaje, identidad de piezas y orientacion del pestillo
2. no derivar cotas finales de perforacion desde una captura reducida del PDF
3. si el proveedor entrega una plantilla 1:1 despues, esa fuente debe mandar sobre esta guia

## 5. Secuencia base de instalacion
Segun la guia visual OEM:
1. pasa el eje cuadrado junto con el cableado por el cuerpo de la cerradura
2. ajusta la posicion del orificio segun la posicion real del lock body
3. selecciona los tornillos segun el grosor de la puerta y aprietalos
4. abre la tapa de baterias para preparar la alimentacion interior
5. instala el `deadbolt`
6. instala y fija la manija en la puerta
7. conecta el puerto del circuito del lock
8. aprieta los tornillos y asegura la tapa de baterias

## 6. Energia y cierre del montaje
La fuente OEM confirma:
- alimentacion principal por `4 AAA 1.5V`
- energia de emergencia por `micro-USB`
- llave mecanica de respaldo (`E-key`)

Antes de cerrar el trabajo:
1. instala las baterias nuevas
2. confirma que la tapa trasera quede bien fijada
3. verifica que la manija exterior despierte al tacto
4. conserva al menos una llave mecanica fuera de la puerta

## 7. Alta tecnica inicial del administrador
El PDF incluye un alta local inicial util para pruebas de instalacion:
- pulsacion corta del boton de ajuste `s1` para agregar administrador o usuario
- pulsacion larga de `s1` para forzar inicializacion del sistema
- tecla `s2` para abrir o cerrar rapido el modo normalmente abierto

En estado inicial, la guia indica que puede registrarse huella o password desde la parte interior para crear el primer administrador.

## 8. Validacion despues de instalar
Despues del montaje, valida:
- alineacion de rosetas y manijas
- respuesta del area numerica integrada en la manija exterior
- lectura de huella en la base circular exterior
- apertura con administrador registrado
- acceso por llave mecanica y respaldo `micro-USB`

## 9. Problemas y cautelas basicas
- si el equipo no responde, revisa primero bateria, cableado y conexion del circuito antes de desmontar
- la fuente OEM recuerda reemplazar baterias con regularidad para evitar fugas
- cuando la bateria esta baja, el indicador puede encender en rojo y aun dejar un numero limitado de aperturas residuales
- no cierres el trabajo sin probar pestillo, huella, password y energia de emergencia

## 10. Relacion con el paquete documental
Este documento convive con:
- `e-Touch user manual - image-ready.md`
- `e-Touch app manual.md`
- `e-Touch - installation template standard.md`
- `e-Touch - supplemental source review.md`

## 11. Estado editorial
La guia suplementaria permite normalizar la instalacion de e-Touch con suficiente confianza.

Sigue pendiente para un nivel tecnico mas alto:
- plantilla 1:1 de perforacion
- confirmacion fisica de espesores compatibles y de cualquier cota exacta no visible en el PDF corto