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

### Schema v1 for `interactions.json`

#### Root structure
```json
{
  "schema_version": "1.0",
  "exported_at": "2026-05-10T17:00:00Z",
  "source": {
    "site_url": "https://beslock.com.co",
    "platform": "wordpress-woocommerce",
    "theme": "beslock-custom"
  },
  "interactions": []
}
```

#### Root fields
- `schema_version` (`string`, required)
- `exported_at` (`string`, required, ISO 8601 UTC)
- `source` (`object`, required)
- `interactions` (`array`, required)

#### Interaction base structure
Each interaction item must include:
- `interaction_id`
- `interaction_type`
- `product`
- `author`
- `content`
- `status`
- `thread`
- `timestamps`

#### Common fields
- `interaction_id`: required stable identifier
- `interaction_type`: `review`, `question`, or `reply`
- `product.product_id`: original numeric reference when available
- `product.sku`: primary reconciliation key for restore
- `product.slug`: recommended fallback key
- `product.name`: required product label
- `author.name`: optional individually
- `author.email`: optional individually
- `author.display_name`: required; use name first, email as fallback
- `content.title`: optional or empty
- `content.body`: required
- `status`: `approved`, `pending`, `spam`, or `trash`
- `thread.parent_interaction_id`: null for roots, required for replies
- `thread.is_admin_response`: boolean, required
- `timestamps.created_at`: required, ISO 8601 UTC
- `timestamps.updated_at`: required, ISO 8601 UTC

#### Type-specific rules
##### Review
- `rating` is required
- `rating` must be an integer from 1 to 5

##### Question
- `rating` must be omitted or null

##### Reply
- `thread.parent_interaction_id` is required
- `rating` must be omitted or null unless a future rule explicitly allows it

#### Validation rules
1. Every interaction must include at least one of:
   - `author.name`
   - `author.email`
2. `author.display_name` must resolve to:
   - `author.name` if present
   - otherwise `author.email`
3. `review` requires `rating`
4. `question` does not use `rating`
5. `reply` requires `thread.parent_interaction_id`
6. Product data must be sufficient for restore reconciliation:
   - prefer `sku`
   - fallback to `slug`
   - always include `name`

#### Example JSON
```json
{
  "schema_version": "1.0",
  "exported_at": "2026-05-10T17:00:00Z",
  "source": {
    "site_url": "https://beslock.com.co",
    "platform": "wordpress-woocommerce",
    "theme": "beslock-custom"
  },
  "interactions": [
    {
      "interaction_id": 101,
      "interaction_type": "review",
      "product": {
        "product_id": 123,
        "sku": "E-PRIME",
        "slug": "e-prime",
        "name": "E-Prime"
      },
      "author": {
        "name": "Carlos",
        "email": "carlos@email.com",
        "display_name": "Carlos"
      },
      "content": {
        "title": "",
        "body": "Excelente producto, fácil de instalar."
      },
      "rating": 5,
      "status": "approved",
      "thread": {
        "parent_interaction_id": null,
        "is_admin_response": false
      },
      "timestamps": {
        "created_at": "2026-05-08T16:10:00Z",
        "updated_at": "2026-05-09T18:30:00Z"
      }
    },
    {
      "interaction_id": 102,
      "interaction_type": "question",
      "product": {
        "product_id": 123,
        "sku": "E-PRIME",
        "slug": "e-prime",
        "name": "E-Prime"
      },
      "author": {
        "name": "",
        "email": "cliente@email.com",
        "display_name": "cliente@email.com"
      },
      "content": {
        "title": "",
        "body": "¿Funciona con puerta metálica?"
      },
      "status": "pending",
      "thread": {
        "parent_interaction_id": null,
        "is_admin_response": false
      },
      "timestamps": {
        "created_at": "2026-05-10T09:20:00Z",
        "updated_at": "2026-05-10T09:20:00Z"
      }
    },
    {
      "interaction_id": 103,
      "interaction_type": "reply",
      "product": {
        "product_id": 123,
        "sku": "E-PRIME",
        "slug": "e-prime",
        "name": "E-Prime"
      },
      "author": {
        "name": "Equipo Beslock",
        "email": "info@beslock.com.co",
        "display_name": "Equipo Beslock"
      },
      "content": {
        "title": "",
        "body": "Sí, funciona con puertas metálicas compatibles."
      },
      "status": "approved",
      "thread": {
        "parent_interaction_id": 102,
        "is_admin_response": true
      },
      "timestamps": {
        "created_at": "2026-05-10T10:00:00Z",
        "updated_at": "2026-05-10T10:00:00Z"
      }
    }
  ]
}
```

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

### Implementación actual de Stage 1
- plugin source exporter: `wp-content/plugins/beslock-interactions-exporter/`
- plugin source importer: `wp-content/plugins/beslock-interactions-importer/`
- paquete instalable exporter: `wp-content/themes/beslock-custom/interactions/exporter_interactions.zip`
- paquete instalable importer: `wp-content/themes/beslock-custom/interactions/importer_interactions.zip`
- el importer aplica overwrite por producto resolviendo en este orden: `sku`, `slug`, `name`
- el exporter declara `post_type = product` en su query para evitar que WooCommerce excluya reseñas e interacciones de producto en consultas globales de comentarios
- si una interacción proviene del importer, el exporter preserva `interaction_id`, `thread.parent_interaction_id` y `product.product_id` originales usando meta `beslock_original_*`
- la validación actual conserva `54/54` interacciones y los IDs canónicos, pero una exportación fresca local todavía difiere en `product.sku` porque el exporter serializa el SKU real del catálogo WooCommerce; en un diff textual también cambian `exported_at`, `source.site_url` y el orden de `interactions` (el exporter serializa en orden `comment_date_gmt` ascendente)

---

## Checklist de trabajo

### Fase 1
- [x] Crear carpeta `interactions/`
- [x] Definir schema de `interactions.json`
- [x] Definir `review`, `question`, `reply`
- [x] Definir overwrite obligatorio
- [x] Definir exporter
- [x] Definir importer
- [x] Documentar flujo de backup/restore

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
