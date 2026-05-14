# e-Touch
## Revision de fuente suplementaria OEM

## 1. Objetivo
Determinar que aporta realmente `e-Touch_1.pdf`, separar lo util para instalacion, app y contexto visual, y dejar explicito que parte del PDF es solo apoyo editorial o repeticion OEM.

## 2. Fuente revisada
- `e-Touch_1.pdf` -> PDF OEM corto de dos paginas renderizadas, con layout del producto, packing list, diagrama de montaje, pasos de instalacion, onboarding en app y bloques de configuracion/soporte

## 3. Renders generados
- `assets/e-touch/pdf-renders/e-touch-1/page-01.png`
- `assets/e-touch/pdf-renders/e-touch-1/page-02.png`
- `assets/e-touch/pdf-renders/e-touch-1/contact-sheet.png`

## 4. Clasificacion por pagina renderizada

| Render | Bloques principales | Valor para Beslock | Decision editorial |
|---|---|---|---|
| `assets/e-touch/pdf-renders/e-touch-1/page-01.png` | layout del producto, packing list, diagrama explotado, pasos de instalacion, alta de administrador, onboarding `Tuya Smart` / `Smart Life` | alto | usar para manual de instalacion, manual de app y refuerzo del perfil visual |
| `assets/e-touch/pdf-renders/e-touch-1/page-02.png` | gestion de miembros, huellas, passwords temporales, normally-open mode, emergency unlock, reset, parametros, QA | alto | usar para manual de app, soporte operativo y claims tecnicos cautelosos |

## 5. Lo que es solo repeticion o bajo valor
- introduccion corporativa y disclaimer OEM: bajo valor operativo
- warranty card y bloque de posventa: valor documental, pero no define comportamiento del producto
- parte del texto de Q&A repite problemas basicos de bateria o cableado ya inferibles desde el uso general

## 6. Conocimiento nuevo util
- el producto usa rosetas circulares con manija horizontal y numerales iluminados sobre la propia manija exterior
- el sensor de huella se concentra en el area circular cercana a la base de la manija exterior
- el conjunto incluye `front handle`, `rear handle`, `rear cover with battery`, `connecting pipe` largo/corto, `deadbolt`, `E-key`, `fix screw` y `cover screw`
- la instalacion usa eje cuadrado y ajuste de longitud de tornilleria segun grosor de puerta
- el PDF muestra respaldo por `micro-USB` para energia de emergencia y baterias `4 AAA 1.5V`
- el flujo OEM de app usa `Tuya Smart APP`, toma `Smart Life APP` como ejemplo y trabaja por Bluetooth, no por Wi-Fi
- la guia OEM describe capacidades de referencia de hasta `100` huellas, `100` passwords y `100` tarjetas, pero estos numeros deben tratarse como claim OEM pendiente de confirmacion comercial

## 7. Clasificacion documental Beslock
- si soporta manual de instalacion normalizado
- si soporta manual de app normalizado
- si soporta anexo tecnico de instalacion tipo `guide-only`
- no soporta una plantilla 1:1 de perforacion en el material recibido

## 8. Decision Beslock
- integrar `e-Touch_1.pdf` como fuente suplementaria principal para montaje, onboarding Bluetooth y soporte tecnico basico
- crear `e-Touch installation manual.md`
- crear `e-Touch app manual.md`
- crear `e-Touch - installation template standard.md` como anexo tecnico normalizado que deja explicito que hoy no existe plantilla 1:1

## 9. Impacto aplicado en el repo
- perfil visual de `e-Touch` ampliado con geometria OEM suplementaria
- prompts de imagen reforzados para preservar la identidad de manija con numerales integrados
- manual de uso final enriquecido con contexto tecnico y de vinculacion
- starter pack actualizado para reflejar el nuevo paquete documental extendido