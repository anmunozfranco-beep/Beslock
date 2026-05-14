# e-Touch
## Manual de app normalizado para Beslock

## 1. Objetivo
Separar el flujo de vinculacion Bluetooth y gestion desde app para e-Touch, usando la evidencia OEM suplementaria disponible.

## 2. Ecosistema observado
La fuente OEM menciona dos nombres de app en el mismo flujo:
- `Tuya Smart APP` como app a descargar
- `Smart Life APP` como interfaz de ejemplo para explicar funciones

Regla editorial Beslock:
- tratar ambas como parte del mismo ecosistema Tuya
- no presentar Wi-Fi ni gateway cuando la fuente muestra claramente alta por Bluetooth

## 3. Requisitos antes de vincular
- tener una cuenta en la app o completar el registro inicial
- activar Bluetooth en el telefono
- permanecer cerca de la cerradura durante el alta
- contar con un administrador registrado cuando el flujo ya no este en estado inicial

## 4. Flujo OEM base de alta
![Onboarding OEM de e-Touch](assets/e-touch/pdf-renders/e-touch-1/page-01.png)

La secuencia observada en el PDF es:
1. abrir `Tuya Smart` o `Smart Life`
2. tocar `Add device`
3. entrar a `Security monitoring`
4. elegir `Smart Door Lock`
5. iniciar la distribucion Bluetooth
6. despertar la cerradura tocando el keypad integrado o el lector de huella
7. esperar a que el telefono detecte el equipo y confirmar el alta
8. la cerradura emite dos avisos tipo `drip` cuando la vinculacion termina correctamente

## 5. Pantalla principal y funciones vistas en OEM
El OCR y la pagina suplementaria muestran estas familias de funciones:
- `Unlocking Record`
- `Smart Linkage`
- `Settings`
- gestion de miembros de familia y otros miembros
- gestion de huellas
- gestion de passwords
- passwords temporales u offline

La pagina debe presentar estas funciones como capacidades OEM observadas, no como promesa exacta de cada build comercial.

## 6. Miembros y permisos
La guia distingue entre `family member` y `other member`.

Uso editorial recomendado:
- explicar que el administrador decide permisos y ventanas de tiempo
- explicar que un miembro puede perder acceso cuando expira el periodo asignado
- no prometer cada etiqueta exacta de UI sin validacion sobre hardware real

## 7. Huellas y passwords desde app
La fuente OEM sugiere:
- alta de huellas vinculada al miembro correspondiente
- gestion de password normal y password temporal
- posibilidad de generar passwords temporales, recurrentes u offline dentro del ecosistema de app

Antes de publicarlo como feature comercial cerrada, conviene validar cada subtipo en la variante real vendida por Beslock.

## 8. Normally-open mode y soporte remoto basico
La fuente OEM muestra manejo de `normally-open mode` y record de aperturas.

Regla editorial:
- describir este modo como funcion disponible cuando la configuracion del administrador lo habilita
- explicar que la app ayuda a revisar registros y ajustes, pero no mezclar este bloque con el manual de instalacion fisica

## 9. Reset y recuperacion
![Soporte OEM de e-Touch](assets/e-touch/pdf-renders/e-touch-1/page-02.png)

El PDF muestra dos metodos de reset y borrado total:
- metodo fisico con pulsacion prolongada en un orificio o punto interno
- metodo autenticado con una secuencia local y verificacion del administrador

Este bloque debe mantenerse como informacion de soporte y no como accion de uso cotidiano.

## 10. Limites de evidencia
- la fuente no describe un flujo Wi-Fi ni una nube separada; el onboarding visible es Bluetooth
- no hay evidencia suficiente aqui para asegurar automatizaciones avanzadas sin validacion adicional
- las capacidades numericas de usuarios y credenciales siguen siendo claims OEM pendientes de confirmacion comercial

## 11. Estado editorial
Este manual de app queda normalizado como base operativa minima para e-Touch.

Antes de una version final para cliente conviene validar:
- nombre exacto de la app que se publicara en soporte
- si `Smart Life` y `Tuya Smart` se mantendran como equivalentes en la implementacion comercial
- subtipos reales de passwords temporales disponibles