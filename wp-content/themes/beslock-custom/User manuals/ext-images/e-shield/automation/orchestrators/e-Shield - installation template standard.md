# e-Shield
## Plantilla de instalacion normalizada para Beslock

## 1. Rol del documento
Este documento define como Beslock debe manejar la plantilla de perforacion asociada a e-Shield.

No reemplaza el PDF original de plantilla.
Su funcion es explicar uso, contexto, QA y relacion con el resto del paquete documental.

## 2. Fuente de origen
- archivo fuente: `e-Shied_2.pdf`
- titulo visible en la pagina: `Plantilla de instalacion`
- modelo visible en la plantilla: `TOCK XT - TWIN`
- nota editorial: el archivo fue entregado como parte del paquete de e-Shield; la equivalencia exacta de SKU debe validarse antes de publicar ese nombre como claim comercial

## 3. Posicion dentro del estandar Beslock
La plantilla de instalacion es un documento adicional al:
- manual de uso
- manual de instalacion
- manual de app

Su proposito no es explicar configuracion ni operacion.
Su proposito es permitir impresion, orientacion y perforacion correcta de la puerta.

## 4. Regla de uso operativo
1. imprimir el PDF original a escala `100%` y sin ajuste automatico
2. verificar si la hoja mostrada aplica a apertura derecha o si debe espejarse para apertura izquierda
3. alinear la zona `LATERAL DE PUERTA` exactamente con el canto de la puerta
4. usar la plantilla impresa como autoridad de perforacion; no reconstruir cotas finales a mano desde una transcripcion OCR

## 5. Medidas visibles y utiles para control
- retiro desde el borde: `60 mm`
- perforacion circular principal: `32 mm`
- perforaciones auxiliares redondas: `6 mm`
- perforacion auxiliar mayor: `25 mm`
- existe una abertura oblonga auxiliar en el lado interior; la plantilla impresa manda sobre cualquier lectura secundaria del render

## 6. Lectura Beslock de la plantilla
- cara izquierda de la hoja: parte interna de la puerta
- cara derecha de la hoja: parte externa de la puerta
- centro: referencia del lateral/canto de la puerta
- la hoja sirve para ubicar el patron de perforacion del cuerpo exterior y del cuerpo interior en una arquitectura de cerradura dividida

## 7. QA minimo antes de perforar
- confirmar mano de apertura correcta
- confirmar escala de impresion al `100%`
- confirmar espesor de puerta compatible con el producto (`30 a 110 mm`, segun la ficha suplementaria OEM)
- confirmar que el patron coincide con el cuerpo exterior vertical y la caja interior horizontal de e-Shield
- no perforar usando solo una captura o una reimpresion escalada desde web

## 8. Entregables Beslock asociados
- PDF original para descarga e impresion: `e-Shied_2.pdf`
- render de referencia para revision visual: `assets/e-shield/pdf-renders/e-shield-2/page-01.png`
- auditoria de fuente suplementaria: `e-Shield - supplemental source review.md`

## 9. Decision editorial
En el paquete documental de e-Shield, la plantilla de instalacion debe mantenerse como tipo documental independiente.

No debe fundirse con el manual de uso.
No debe resumirse como si fuera manual de app.
No debe reemplazar el manual de instalacion.

Debe convivir con ellos como anexo tecnico de perforacion y montaje.