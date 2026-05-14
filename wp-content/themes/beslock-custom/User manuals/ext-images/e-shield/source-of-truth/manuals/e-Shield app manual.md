# e-Shield
## Manual de app normalizado para Beslock

## 1. Objetivo
Explicar el flujo principal de la app asociada a e-Shield sin mezclarlo con el manual de uso ni con el manual de instalacion.

La fuente OEM habla de la app `TECDOFY` y del uso opcional de `Gateway` para funciones remotas.
Mientras no exista validacion directa en hardware y cuenta real, este documento debe leerse como manual de app normalizado con prudencia editorial.

## 2. Que necesitas antes de empezar
- la cerradura debe estar instalada y energizada
- el celular principal debe tener Bluetooth activo
- la cerradura debe estar a corta distancia del telefono; la fuente OCR menciona hasta `8 metros` como referencia maxima
- si vas a usar funciones remotas, necesitas un Gateway enlazado a WiFi

## 3. Registro e inicio de sesion
La fuente OEM indica que el usuario puede registrarse con telefono movil o correo electronico.

Flujo base:
1. abre la app `TECDOFY`
2. registra la cuenta con telefono o email
3. confirma el codigo de verificacion
4. inicia sesion y verifica la cuenta si cambias de telefono

Validacion posterior:
- confirma que la cuenta conserva los datos de la cerradura al iniciar sesion desde el telefono principal

## 4. Agregar la cerradura
La primera vinculacion convierte al primer usuario en administrador original del equipo.

Secuencia recomendada:
1. toca el boton `+` para agregar una cerradura
2. selecciona el tipo de dispositivo correcto
3. activa el teclado o panel de la cerradura para entrar en modo de configuracion
4. sigue el flujo de alta desde la app
5. acepta o cambia el nombre del dispositivo

Nota editorial:
La fuente indica que una cerradura ya vinculada debe eliminarse primero de la app anterior antes de registrarse de nuevo.

## 5. Gestion del dispositivo
La app permite operaciones de mantenimiento y administracion cercana por Bluetooth.

Incluye, segun la fuente OCR:
- actualizacion de la cerradura
- calibracion de fecha y hora
- diagnostico de errores
- autorizacion de administrador adicional

Regla practica:
- realiza estas operaciones con el telefono junto a la cerradura cuando la fuente hable de Bluetooth local

## 6. eKeys y acceso compartido
El administrador original puede enviar distintos tipos de eKey desde la app.

Tipos visibles en la fuente:
- temporal
- permanente
- de un solo uso

Uso recomendado:
1. entra al modulo `eKeys`
2. toca `Enviar eKey`
3. elige el tipo de vigencia
4. completa los datos del usuario receptor
5. envia la llave y valida su vigencia en el historial

## 7. Contrasenas remotas
La fuente OEM describe un modulo dedicado a contrasenas.

Tipos visibles en OCR:
- permanente
- temporal
- de un solo uso
- ciclica
- personalizada

Flujo base:
1. entra a `Contrasenas`
2. toca `Enviar codigo de acceso`
3. selecciona el tipo de codigo
4. completa nombre y vigencia
5. genera el codigo
6. ingresa el codigo en la cerradura y confirma con `#` para registrarlo en el equipo

Notas utiles:
- un codigo permanente o temporal nuevo debe usarse dentro de las primeras `24 horas` para quedar activo
- la contrasena de un solo uso se describe como valida durante `6 horas`

## 8. Tarjetas RF y huellas
La fuente muestra dos modulos paralelos: `Tarjetas RF` y `Gestion de huellas`.

### Tarjetas RF
1. entra a `Tarjetas RF`
2. toca `Agregar tarjetas RF`
3. define nombre y tiempo de vigencia
4. acerca la tarjeta a la cerradura para completar el enlace

### Huellas
1. entra al modulo de huellas
2. inicia el alta
3. apoya el dedo `4 veces` segun la guia OEM
4. valida el desbloqueo despues del registro

## 9. Desbloqueo por Bluetooth
La app permite abrir la cerradura desde el boton con icono de candado cuando estas dentro de alcance.

Uso recomendado:
1. abre la pantalla del dispositivo
2. verifica conexion Bluetooth activa
3. toca el icono de candado para bloquear o desbloquear
4. confirma respuesta fisica de la cerradura

## 10. Modulos opcionales del sistema
La fuente OCR tambien muestra estos bloques:
- gestion de asistencia
- configuracion del sistema
- informacion de cuenta
- usuarios del dispositivo
- grupo de dispositivos
- transferir derechos de administrador
- servicio al cliente

No todos estos modulos tienen que aparecer en todas las versiones o regiones de la app.
Deben presentarse en Beslock como funciones condicionales sujetas a la version instalada.

## 11. Gateway y funciones remotas
e-Shield usa Bluetooth por defecto.
El `Gateway` actua como puente hacia una red domestica WiFi para funciones remotas.

La fuente OCR atribuye al Gateway estas capacidades:
- gestion remota del reloj
- consulta del historial de registros
- borrado o modificacion remota de contrasenas

Flujo base para agregar Gateway:
1. entra al apartado `Gateway`
2. toca `+`
3. selecciona el modelo de Gateway
4. introduce la clave WiFi y el nombre del Gateway
5. sigue el asistente hasta completar el enlace
6. vincula la cerradura al Gateway cuando aparezca dentro del alcance detectado

## 12. Advertencias editoriales
- `TECDOFY` debe tratarse como fuente OEM observada, no como claim final multiregion sin validacion adicional
- la app y los nombres exactos de botones pueden variar por version
- si la operacion depende de Bluetooth local, no debe describirse como flujo remoto puro
- las funciones de asistencia, grupos o soporte deben marcarse como opcionales cuando no haya prueba de version activa

## 13. Estado editorial
Este manual de app se apoya en OCR de la seccion OEM de aplicacion incluida dentro de la fuente principal de e-Shield.

Queda util como base normalizada de contenido.
Antes de publicarse como manual de app definitivo para cliente final, conviene validar:
- nombre real de la app en la implementacion comercial
- textos exactos de botones
- disponibilidad real de Gateway, asistencia y transferencia de administrador