# Beslock Manual Document Package Standard

## 1. Objetivo
Definir los tipos documentales que puede tener cada producto dentro de `User manuals/` y fijar una regla progresiva que funcione incluso cuando todavia no existen fuentes de instalacion o app para todos los modelos.

## 2. Regla base
No todos los productos tienen que publicar el mismo numero de documentos al mismo tiempo.

La ausencia de una fuente valida no obliga a inventar un manual.
La ausencia de una fuente valida obliga a dejar el tipo documental como pendiente.

## 3. Tipos documentales Beslock

### A. Manual de uso
Uso principal:
- operacion diaria
- alta de usuarios
- accesos
- troubleshooting
- soporte y descargas

Formato objetivo:
- markdown final para contenido web o CMS

Patron actual:
- `<Product> user manual - image-ready.md`

### B. Manual de instalacion
Uso principal:
- compatibilidad fisica
- preparacion de puerta
- perforacion y montaje
- energia inicial
- validacion post-instalacion

Formato objetivo:
- markdown normalizado, aunque todavia no tenga paquete visual final propio

Patron recomendado:
- `<Product> installation manual.md`

### C. Manual de app
Uso principal:
- login o alta en la app
- vinculacion del equipo
- gestion de miembros
- contrasenas temporales
- gateway o funciones remotas cuando existan

Formato objetivo:
- markdown normalizado, derivado de fuente OEM o flujo validado

Patron recomendado:
- `<Product> app manual.md`

### D. Plantilla de instalacion
Uso principal:
- perforacion
- corte
- referencia de mano de apertura
- control de escala de impresion

Formato objetivo:
- PDF OEM original preservado
- markdown normalizado complementario que explique uso, QA y limites del documento

Patron recomendado:
- PDF fuente original en `User manuals/`
- markdown companero: `<Product> - installation template standard.md`

## 4. Politica de activacion por producto
Un producto puede estar en una de estas situaciones:

### Core package
- manual de uso

### Extended package
- manual de uso
- manual de instalacion y/o manual de app

### Technical companion package
- uno o mas anexos tecnicos como plantilla de instalacion

Esto significa que un producto puede tener hoy solo manual de uso y manana sumar manual de instalacion o plantilla, sin romper el estandar.

## 5. Requisitos minimos por tipo documental

| Tipo | Fuente minima aceptable | No hacer |
|---|---|---|
| Manual de uso | manual OEM, OCR legible, contenido validado | inventar menus o codigos no confirmados |
| Manual de instalacion | seccion de instalacion OEM, ficha tecnica confiable, plantilla o validacion fisica | derivar montaje fino solo desde una imagen publicitaria |
| Manual de app | guia OEM de app, OCR util, flujo validado en dispositivo | mezclar onboarding de app con manual de uso sin separar contexto |
| Plantilla de instalacion | PDF OEM de perforacion o corte | reconstruir cotas finales desde OCR cuando el PDF original existe |

## 6. Reglas de evidencia
- marcar como pendientes los codigos o secuencias que no hayan sido validados en hardware real
- si la plantilla existe, la plantilla impresa manda sobre cualquier OCR de medidas
- usar el perfil visual del producto para evitar deriva geometrica en imagenes nuevas
- separar siempre contenido operativo de contenido meramente grafico o repetido

## 7. Reglas de publicacion
- el manual de uso puede tener superficie `image-ready` y `web-ready`
- manual de instalacion y manual de app pueden existir primero como markdown normalizado aunque aun no tengan integracion final al manifest web
- la plantilla de instalacion nunca reemplaza al manual de instalacion; lo acompana
- no crear placeholders vacios solo para completar una matriz documental

## 8. Estado actual del estandar
Hoy Beslock no tiene referencias de instalacion o app igualmente maduras para todos los productos.

Por eso, este estandar se aplica de forma progresiva:
- cuando existe fuente valida, se normaliza el documento
- cuando no existe fuente valida, se deja constancia de la ausencia y no se fuerza un deliverable final falso

## 8.1 Plantilla reusable
La estructura base reusable para nuevos manuales de instalacion vive en:
- `installation-manual-template.md`

Debe usarse como armazon editorial y no como fuente tecnica.
La fuente tecnica siempre debe venir del PDF OEM, la plantilla de perforacion o la validacion real del producto.

## 9. Primer caso de referencia
`e-Shield` pasa a ser el primer caso explicito con:
- manual de uso final
- manual de instalacion normalizado
- manual de app normalizado
- plantilla de instalacion tratada como documento tecnico separado