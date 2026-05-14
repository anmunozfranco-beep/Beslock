# e-Shield
## Revision de fuentes suplementarias OEM

## 1. Objetivo
Separar el valor real de los nuevos PDFs de e-Shield para Beslock: que sirve como conocimiento de producto, que sirve como contexto visual para generar imagenes, que es repeticion OEM, y que debe vivir como documento adicional dentro del paquete documental.

## 2. Fuentes revisadas
- `e-Shield_1.pdf` -> ficha OEM breve de 2 paginas para `SMART OUTDOOR LOCK NX5`
- `e-Shied_2.pdf` -> plantilla de perforacion de 1 pagina titulada `Plantilla de instalacion`

## 3. Renders generados
- `assets/e-shield/pdf-renders/e-shield-1/page-01.png`
- `assets/e-shield/pdf-renders/e-shield-1/page-02.png`
- `assets/e-shield/pdf-renders/e-shield-2/page-01.png`
- `assets/e-shield/pdf-renders/e-shield-1/contact-sheet.png`
- `assets/e-shield/pdf-renders/e-shield-2/contact-sheet.png`

## 4. Clasificacion pagina por pagina

| Fuente | Pagina | Tipo real | Valor para Beslock | Decision editorial |
|---|---|---|---|---|
| `e-Shield_1.pdf` | 1 | ficha tecnica + diagrama de producto + resumen funcional | alto para contexto visual y conocimiento base | usar geometria, componentes, bateria de emergencia, alarma por intentos y password virtual; no copiar el password inicial OEM como contenido final |
| `e-Shield_1.pdf` | 2 izquierda | continuidad de menu OEM | medio-bajo | usar solo como referencia interna; hay repeticion y contradicciones en conteos de usuarios |
| `e-Shield_1.pdf` | 2 derecha | tabla de especificaciones | alto | usar para enriquecer perfil visual, criterio de instalacion y conocimiento del producto |
| `e-Shied_2.pdf` | 1 | plantilla de perforacion / corte | alto pero de otro tipo | normalizar como documento adicional separado, no mezclarlo con manual de uso |

## 5. Conocimiento nuevo util para producto e imagenes
- el hardware suplementario confirma la arquitectura `split rim lock`: modulo exterior vertical separado de una caja interior horizontal
- el modulo exterior mantiene un lector circular con aro azul en la parte superior y un keypad 3x4 debajo
- el modulo interior muestra un solo boton circular visible en la cara de la caja
- referencia OEM de tamanos: frente `145 x 58 x 50 mm`, caja interior `130 x 110 x 50 mm`
- compatibilidad fisica declarada: puertas de `30 a 110 mm`
- alimentacion declarada: `4 AA` con respaldo `USB`
- seguridad OEM declarada: cilindro `Class C`, anti-black-box, anti-tailgating, anti-peeping y password virtual

## 6. Ruido, repeticion y conflictos detectados
- el bloque `System Settings` del PDF suplementario repite texto de `Restore Factory Settings`, por lo que no debe tomarse como flujo limpio
- la hoja OEM mezcla conteos contradictorios: un bloque habla de `10` administradores y `240` usuarios, mientras la tabla de especificaciones habla de `9` administradores y `91` usuarios por modalidad
- el password inicial `123456` debe tratarse como referencia OEM pendiente de validacion, no como texto listo para publicar
- la plantilla de instalacion no es un manual de uso ni un manual de app; es un artefacto de perforacion para imprimir y usar a escala

## 7. Decision Beslock
- usar `e-Shield_1.pdf` como fuente suplementaria de geometria, medidas, alimentacion y criterios de seguridad
- usar la plantilla `e-Shied_2.pdf` como documento adicional separado del manual de uso, el manual de instalacion y el manual de app
- mantener el PDF original para impresion a escala 100%
- usar el markdown normalizado para explicar orientacion, uso correcto, QA y relacion con el resto del paquete documental

## 8. Impacto aplicado en el repo
- perfil visual de `e-Shield` ampliado con proporciones y señales geometricas del hardware OEM
- prompts base de `e-Shield` reforzados para evitar deriva hacia cerraduras tipo manija, pomo o deadbolt generico
- nuevo `e-Shield installation manual.md` creado como base de instalacion normalizada
- nueva plantilla normalizada creada como documento Beslock independiente