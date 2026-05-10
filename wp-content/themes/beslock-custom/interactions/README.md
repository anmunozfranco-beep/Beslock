# Beslock Product Interactions

## Objetivo
Implementar en Beslock un sistema unificado de interacciones de producto que soporte:

- reseñas (`review`)
- consultas (`question`)
- respuestas (`reply`)

El trabajo se divide en dos stages claramente separados:

### Stage 1 — Contingencia
Sistema de respaldo y restauración:
- `interactions.json`
- `exporter_interactions.zip`
- `importer_interactions.zip`

### Stage 2 — Operación diaria
Sistema frontend de captura de:
- reseñas
- consultas

---

## Principios rectores

### 1. Fuente operativa única
La operación cotidiana debe vivir en:
- WooCommerce / WordPress comments + meta
- extensiones necesarias para distinguir tipos

### 2. Separación estricta de responsabilidades
#### Stage 1
Solo backup / restore / migración / contingencia

#### Stage 2
Solo captura diaria, moderación y visualización normal

### 3. Moderación obligatoria
Toda nueva reseña o consulta:
- entra siempre en moderación
- nunca se publica automáticamente

### 4. Identidad mínima
Toda nueva interacción debe tener al menos uno:
- nombre
- email

---

## Estructura objetivo

```text
wp-content/themes/beslock-custom/interactions/
  interactions.json
  exporter_interactions.zip
  importer_interactions.zip
  README.md
```

---

## Modelo conceptual unificado

### Entidad base
`interaction`

### Tipos
- `review`
- `question`
- `reply`

### Campos comunes
- producto
- autor
- contenido
- estado
- timestamps
- relación padre/hijo

### Campos específicos
#### review
- rating obligatorio

#### question
- sin rating

#### reply
- `parent_interaction_id`

---

## Stage 1 — Interactions Backup & Restore

### Objetivo
Permitir exportar e importar las interacciones del producto para recuperación o migración.

### Alcance
- serialización estructurada
- overwrite obligatorio en importación
- resolución por producto
- preservación de jerarquía y estado

### Exclusiones
- no render frontend
- no captura diaria
- no moderación diaria

### Estructura del snapshot
El archivo `interactions.json` debe soportar:
- reviews
- questions
- replies

### Convenciones
- carpeta: `interactions`
- snapshot: `interactions.json`
- exportador: `exporter_interactions.zip`
- importador: `importer_interactions.zip`

---

## Stage 2 — Frontend Product Interactions

### Objetivo
Habilitar una caja visible y permanente en el `single-product` para que usuarios envíen:
- reseñas
- consultas

### Ubicación
- debajo del bloque tabs `Características / Reviews`
- fuera del contenedor de tabs
- siempre visible

### Comportamiento
- selector entre `reseña` y `consulta`
- validación según tipo
- envío a la fuente operativa real
- moderación obligatoria

### Restricción
Stage 2 no debe leer ni depender de `interactions.json`.

---

## Reglas globales

### Moderación
Todas las nuevas entradas del frontend:
- `pending` por defecto

### Render público
#### Reviews
Se muestran como reseñas

#### Questions
Se muestran como preguntas/consultas

### Regla
No mezclar consultas como si fueran reseñas

### Identidad pública
- mostrar nombre si existe
- si no existe nombre, mostrar email

---

## Flujo operativo general

### Flujo diario
1. Usuario entra a producto
2. Ve tabs + bloque de interacciones
3. Envía reseña o consulta
4. Queda pendiente
5. Admin modera
6. Se publica si corresponde

### Flujo contingencia
1. Se genera `interactions.json`
2. Ante migración o recuperación, importer lo lee
3. Se restauran/sobrescriben las interacciones

---

## Checklist de trabajo

### Fase 1
- [ ] Crear carpeta `interactions/`
- [ ] Definir schema de `interactions.json`
- [ ] Definir `review`, `question`, `reply`
- [ ] Definir overwrite obligatorio
- [ ] Definir exporter
- [ ] Definir importer
- [ ] Documentar flujo de backup/restore

### Fase 2
- [ ] Ubicar bloque debajo del tabset
- [ ] Hacerlo siempre visible
- [ ] Crear selector `reseña / consulta`
- [ ] Validar `review`
- [ ] Validar `question`
- [ ] Garantizar moderación obligatoria
- [ ] Mantener separación visual entre reviews y questions
- [ ] Validar responsive y accesibilidad

---

## Backlog resumido

### A. Modelo de interacciones
- definir entidad base
- definir tipos
- definir reglas de identidad

### B. Infraestructura de contingencia
- carpeta
- snapshot
- exporter
- importer
- documentación

### C. Frontend de operación diaria
- bloque visible en single product
- selector de tipo
- formulario review
- formulario question
- mensajes
- moderación

### D. Validación end-to-end
- review → pending
- question → pending
- export/import
- restauración

---

## Criterio de éxito
El proyecto es exitoso si:

1. las interacciones del producto pueden respaldarse y restaurarse
2. usuarios pueden enviar reseñas y consultas desde frontend
3. todo entra a moderación
4. la operación diaria sigue usando una sola fuente
5. el sistema de contingencia no interfiere en el flujo normal
