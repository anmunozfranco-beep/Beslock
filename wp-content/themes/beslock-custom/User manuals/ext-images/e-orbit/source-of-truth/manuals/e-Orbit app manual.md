# e-Orbit
## Manual de app normalizado para Beslock

## 1. Objetivo
Separar el flujo de vinculacion, gestion remota y passwords temporales de e-Orbit en un documento dedicado, usando como fuente principal `e-Orbit_2.pdf` y como apoyo tecnico `e-Orbit_1.xls`.

## 2. Alcance real de la fuente
Las fuentes nuevas soportan con bastante claridad:
- alta del dispositivo en `Smart Life` / `Tuya`
- configuracion de red del equipo
- desbloqueo remoto
- consulta de registros
- gestion de miembros
- passwords temporales

Tambien aparece `Tongtong APP` en la hoja tecnica, pero el flujo ilustrado del PDF esta centrado en `Smart Life`.

## 3. Ecosistema de app observado
Las fuentes muestran estas variantes:
- `Smart Life` como ejemplo de interfaz de app
- `Tuya` / `Tuya Smart` como ecosistema y modulo Wi-Fi integrado
- `Tongtong APP` como variante OEM mencionada en la hoja tecnica

Regla editorial Beslock:
- presentar `Smart Life` / `Tuya` como flujo principal observado
- tratar `Tongtong` como variante de proveedor que requiere confirmacion comercial antes de publicarse como ruta primaria

## 4. Requisitos antes de vincular
- tener la app instalada e iniciar sesion
- disponer de una red Wi-Fi compatible con el alta del equipo
- permanecer cerca de la cerradura durante el proceso
- saber que la configuracion de red solo admite un telefono movil a la vez
- tener presente que una nueva configuracion de red puede borrar la distribucion anterior

La hoja tecnica indica que el producto usa `Tuya WiFi` integrado y no requiere gateway adicional.

## 5. Alta del dispositivo por QR
La ruta OEM observada es:
1. abrir `Smart Life`
2. tocar `+` para `Add device`
3. entrar en `Camera&Lock`
4. elegir `Video Lock (Wi-Fi)`
5. seguir la pantalla `Reset the device`
6. seleccionar la red Wi-Fi e introducir la contrasena
7. poner la cerradura en modo de red
8. apuntar el codigo QR del telefono a la camara de la cerradura
9. cuando la cerradura emita el aviso sonoro, confirmar que se ha oido y esperar el alta

## 6. Alta del dispositivo por Wi-Fi / EZ Mode
El PDF tambien muestra una variante de alta:
1. abrir `Camera&Lock`
2. elegir `Lock (Wi-Fi)`
3. seleccionar la red Wi-Fi e introducir la contrasena
4. entrar a `Reset the device`
5. seleccionar `EZ Mode`
6. si falla la distribucion, cambiar a otro modo de distribucion o usar el hotspot indicado por la app

Regla editorial:
- documentar este camino como alternativa de recuperacion o fallback
- no mezclar QR y `EZ Mode` como si fueran un solo paso

## 7. Desbloqueo remoto y registros
Segun el PDF:
- cuando un visitante pulsa el timbre, el telefono puede recibir una solicitud de desbloqueo remoto
- la app permite hablar con el visitante
- el desbloqueo remoto se completa deslizando el control de apertura
- eventos como timbre, usuario ilegal, bateria baja y desbloqueo pueden revisarse en registros

## 8. Gestion de miembros
La guia OEM muestra `Gestion de miembros` con este flujo general:
1. entrar a la seccion de miembros
2. usar `+` para agregar otros miembros
3. introducir el nombre del miembro
4. entrar a la informacion del miembro
5. gestionar el modo de desbloqueo
6. vincular el numero de usuario correspondiente

La nota OEM aclara que el `codigo de usuario` se genera al agregar la cerradura.

## 9. Passwords temporales
El PDF muestra al menos estos tipos:
- password de un solo uso
- password ilimitada

La guia indica que la password de un solo uso:
- se genera como un conjunto de diez digitos
- debe usarse dentro de las 6 horas posteriores a su generacion
- solo puede usarse una vez dentro del periodo de validez

La pantalla tambien sugiere variantes con tiempo efectivo o de implementacion, por lo que conviene validar sobre hardware real si la build comercial expone mas tipos ademas de los dos legibles en la fuente.

## 10. Limites y cautelas
- la UI exacta puede variar entre `Smart Life`, `Tuya Smart` y variantes OEM
- la fuente revisada no debe usarse para prometer cada etiqueta exacta de menu sin validacion en equipo real
- la hoja tecnica menciona `Alexa`, pero esa compatibilidad debe confirmarse en la variante comercial concreta antes de destacarla en venta

## 11. Estado editorial
Este manual de app queda normalizado como base operativa minima para e-Orbit.

Sigue pendiente para una version final mas fuerte:
- validacion del flujo exacto de red en hardware real
- confirmacion de la variante principal de app a publicar
- verificacion comercial de compatibilidad `Alexa` y de las variantes de password temporal