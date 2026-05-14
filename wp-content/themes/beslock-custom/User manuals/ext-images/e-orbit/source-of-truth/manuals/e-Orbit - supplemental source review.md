# e-Orbit
## Revision de fuentes suplementarias OEM

## 1. Objetivo
Determinar que aportan realmente `e-Orbit_1.xls` y `e-Orbit_2.pdf`, separar conocimiento util de app, especificaciones y contexto visual, y dejar explicito que estas fuentes no equivalen a una plantilla 1:1 de instalacion.

## 2. Fuentes revisadas
- `e-Orbit_2.pdf` -> manual OEM corto de 17 paginas con portada, tabla de especificaciones, parametros de entorno, flujos locales de configuracion y bloques de app `Smart Life` / `Tuya`
- `e-Orbit_1.xls` -> hoja de especificaciones `NF14` con materiales, capacidades, metodos de apertura, bateria, dimensiones, espesores de puerta, colores, idiomas y notas de resistencia al agua

## 3. Renders generados
- `pdf-renders/e-orbit-2/page-01.png` a `pdf-renders/e-orbit-2/page-17.png`
- `pdf-renders/e-orbit-2/contact-sheet.png`

## 4. Clasificacion del PDF por bloques

| Bloque | Contenido real | Valor para Beslock | Decision editorial |
|---|---|---|---|
| Pagina 1 | portada y dibujo lineal del producto | medio | usar para reforzar silueta y proporciones del producto |
| Paginas 2-3 | tabla de especificaciones, ambiente de trabajo, bateria, Micro USB, bloqueo por intentos | alto | usar para soporte tecnico, claims y cautelas editoriales |
| Paginas 4-7 | alta de usuarios, password virtual, borrado, configuracion del sistema, idioma, red, autenticacion dual, reconocimiento | alto | usar para enriquecer manual de uso y conocimiento OEM de menus |
| Paginas 8-10 | onboarding en `Smart Life`, alta por QR y por Wi-Fi / `EZ Mode` | alto | usar como base del manual de app normalizado |
| Paginas 11, 14, 15 y 17 | capturas de apoyo con poco texto unico | medio-bajo | usar como apoyo visual, no como fuente principal de copy |
| Paginas 12-13 | desbloqueo remoto, registros y gestion de miembros | alto | usar en manual de app y descripcion de funciones remotas |
| Pagina 16 | passwords temporales de un solo uso e ilimitadas | alto | usar para documentar tipos de password temporales observados |

## 5. Aporte real del XLS
La hoja `Sheet1` agrega datos tecnicos valiosos:
- modelo `NF14`
- material: `Aluminum Alloy + Tempered Glass`
- metodos de apertura: reconocimiento facial, palma, huella, password, tarjeta IC y app
- bateria recargable de `7.2V / 4200mAh`
- `Tuya WiFi` integrado, sin gateway adicional
- grosor de puerta aplicable: `38-120 mm`
- cuerpo de cerradura estandar `6068`, con opcion `85 / 90`
- dimensiones de panel frontal `425 x 69 x 49 mm` y panel trasero `430 x 70 x 70 mm`
- compatibilidad declarada con `Alexa`
- nota comercial importante: `IP68` solo por pedido especial; el panel trasero no es impermeable y se sugiere comunicar `IP66`

Tambien agrega una tabla de cambio de idioma en Tuya mediante `888#` y codigos numericos por idioma.

## 6. Repeticion o bajo valor
- la portada y varias capturas de app son utiles como apoyo visual, pero no deben tratarse como prueba exhaustiva del flujo comercial final
- no hay pasos de montaje fisico, despiece, perforacion ni plantilla de corte en las nuevas fuentes
- la UI exacta de app puede variar entre `Smart Life`, `Tuya Smart` y variantes de proveedor como `Tongtong`

## 7. Decision sobre plantilla de instalacion
Con estas fuentes no es seguro crear una plantilla de instalacion real.

Motivo:
- no hay cotas de perforacion
- no hay centros de agujeros ni backset detallado
- no hay escala de impresion ni dibujo de corte
- las dimensiones generales del cuerpo no alcanzan para derivar una drilling template confiable

Si mas adelante aparece un esquema con posiciones de perforacion, cotas funcionales y referencia de escala, Beslock si podria derivar un anexo tecnico o normalizar la plantilla OEM correspondiente.

## 8. Decision Beslock
- crear `e-Orbit app manual.md`
- actualizar el manual de uso final con datos OEM nuevos de energia, apertura y app
- reforzar perfil visual y prompts con material, proporciones y restricciones tecnicas
- mantener `manual de instalacion` y `plantilla de instalacion` como pendientes hasta recibir fuente fisica real de montaje o perforacion

## 9. Impacto aplicado en el repo
- nuevo `e-Orbit app manual.md`
- nuevo `e-Orbit - supplemental source review.md`
- `e-Orbit user manual - image-ready.md` enriquecido
- `ext-images/e-orbit/visual-system/references/e-orbit-visual-profile.md` reforzado
- `e-Orbit - AI image prompts.md` reforzado
- `e-Orbit - implementation starter pack.md` actualizado
- matriz documental actualizada para reflejar `app manual` disponible y `installation/template` aun pendientes