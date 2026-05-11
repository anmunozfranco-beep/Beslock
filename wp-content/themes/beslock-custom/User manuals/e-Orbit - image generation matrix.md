# e-Orbit
## Matriz de imágenes para DALL·E u otra IA gráfica

## 1. Objetivo del documento
Este documento organiza las imágenes necesarias para la implementación inicial del centro de ayuda de `e-Orbit`, especialmente para:

- home / hub
- primeros pasos
- páginas tarea
- troubleshooting
- descargas
- apoyos visuales del MVP Fase 1

Está pensado para que diseño, contenido o producción visual puedan:
- priorizar imágenes
- redactar prompts consistentes
- producir variantes
- controlar estilo visual
- mapear cada imagen a una página concreta

---

## 2. Recomendaciones generales para generación con IA

### Estilo visual recomendado
Usar un estilo:
- limpio
- técnico
- realista
- contemporáneo
- útil para documentación
- no publicitario en exceso

### Evitar
- fondos recargados
- renders demasiado futuristas
- interfaces inventadas poco realistas
- manos deformes
- texto pequeño generado dentro de imagen
- iconografía confusa
- exceso de brillos o dramatismo

### Recomendación práctica
Cuando la imagen sea de producto:
- preferir fondo neutro o entorno doméstico limpio
- mostrar claramente la cerradura
- iluminación natural o controlada
- ángulos útiles para explicar

Cuando sea de uso:
- mostrar interacción clara
- una acción por imagen
- composición simple
- foco en el punto de uso

Cuando sea de app:
- idealmente usar captura real
- si no existe, usar mockup muy sobrio y claramente identificable como apoyo visual

---

## 3. Campos recomendados para la matriz
Cada imagen debería registrar:

- `id`
- `pagina`
- `tipo_de_imagen`
- `objetivo`
- `descripcion_visual`
- `prompt_base`
- `negative_prompt`
- `formato`
- `prioridad`
- `estado`
- `notas`

---

## 4. Matriz priorizada para MVP Fase 1

### Imagen 1
**ID:** IMG-001  
**Página:** `/productos/e-orbit`  
**Nombre sugerido:** Hero principal del producto  
**Tipo de imagen:** producto / hero  
**Objetivo:** mostrar e-Orbit como cerradura inteligente instalada y clara visualmente  
**Descripción visual:** cerradura inteligente moderna instalada en una puerta residencial elegante, vista limpia del panel exterior, ambiente realista, fondo neutro o interior contemporáneo  
**Prompt base:**  
Cerradura inteligente moderna e-Orbit instalada en una puerta residencial, vista frontal en ángulo leve, diseño limpio y elegante, ambiente interior contemporáneo, iluminación natural suave, enfoque en el producto, composición clara para centro de ayuda, fotografía realista de producto, fondo ordenado, tonos neutros, alta definición  
**Negative prompt:**  
texto dentro de la imagen, demasiados objetos decorativos, manos deformes, perspectiva extrema, estilo futurista exagerado, luces de neón, render plástico, fondo recargado, elementos flotantes, interfaz falsa  
**Formato:** horizontal 16:9  
**Prioridad:** alta  
**Estado:** pendiente  
**Notas:** usar como imagen principal del hub

### Imagen 2
**ID:** IMG-002  
**Página:** `/productos/e-orbit/primeros-pasos`  
**Nombre sugerido:** Producto instalado en contexto real  
**Tipo de imagen:** uso / contexto  
**Objetivo:** mostrar el producto ya instalado y listo para uso  
**Descripción visual:** puerta instalada con e-Orbit en contexto residencial limpio, sensación de producto listo para configurar  
**Prompt base:**  
Cerradura inteligente instalada en una puerta moderna de apartamento o casa, vista de contexto real, ambiente limpio y ordenado, estilo documental, fotografía realista, luz natural, composición útil para guía de primeros pasos, enfoque claro en la cerradura y la puerta  
**Negative prompt:**  
desorden, oscuridad excesiva, estilo publicitario dramático, ángulos extremos, texto incrustado, distorsiones, objetos irrelevantes  
**Formato:** horizontal 4:3  
**Prioridad:** alta  
**Estado:** pendiente  
**Notas:** útil para primeros pasos y también instalación

### Imagen 3
**ID:** IMG-003  
**Página:** `/productos/e-orbit/usuarios/agregar-administrador`  
**Nombre sugerido:** Interacción con panel para crear administrador  
**Tipo de imagen:** acción / uso  
**Objetivo:** apoyar visualmente la idea de configuración inicial de usuarios  
**Descripción visual:** mano adulta interactuando con el panel táctil o teclado de la cerradura, enfoque claro en el área del panel  
**Prompt base:**  
Primer plano de una persona adulta usando el panel de una cerradura inteligente moderna en una puerta, interacción clara con el teclado o superficie táctil, enfoque en la acción de configuración, fotografía realista, luz suave, fondo discreto, estilo técnico y limpio para centro de ayuda  
**Negative prompt:**  
dedos deformes, manos extra, texto ilegible en pantalla, interfaz inventada compleja, fondo recargado, estilo futurista, colores exagerados  
**Formato:** vertical 4:5  
**Prioridad:** alta  
**Estado:** pendiente  
**Notas:** si luego se obtiene captura real, esta imagen puede quedar como apoyo secundario

### Imagen 4
**ID:** IMG-004  
**Página:** `/productos/e-orbit/uso/pin`  
**Nombre sugerido:** Uso del teclado para PIN  
**Tipo de imagen:** detalle de producto  
**Objetivo:** mostrar claramente el uso del teclado o zona de ingreso numérico  
**Descripción visual:** primer plano del teclado de la cerradura, dedo acercándose o presionando, composición muy clara  
**Prompt base:**  
Primer plano detallado del teclado de una cerradura inteligente moderna, una mano adulta ingresando un PIN, enfoque nítido en la superficie del teclado, fotografía realista de producto, iluminación suave, composición minimalista y técnica, fondo desenfocado discreto  
**Negative prompt:**  
números raros, texto inventado muy visible, manos deformes, reflejos excesivos, estética futurista exagerada, ruido visual  
**Formato:** vertical 4:5  
**Prioridad:** media  
**Estado:** pendiente  
**Notas:** no depender de números visibles correctos

### Imagen 5
**ID:** IMG-005  
**Página:** `/productos/e-orbit/uso/huella`  
**Nombre sugerido:** Uso del lector de huella  
**Tipo de imagen:** detalle de producto  
**Objetivo:** mostrar cómo se apoya el dedo sobre el sensor  
**Descripción visual:** dedo apoyado naturalmente en lector de huella de la cerradura  
**Prompt base:**  
Primer plano realista de una persona usando el lector de huella de una cerradura inteligente, dedo apoyado de manera natural sobre el sensor, composición clara y didáctica, fotografía técnica, iluminación suave, fondo neutro desenfocado, alta definición  
**Negative prompt:**  
dedos deformes, sensor irreconocible, luces extrañas, apariencia robótica, composición recargada, texto dentro de imagen  
**Formato:** vertical 4:5  
**Prioridad:** alta  
**Estado:** pendiente  
**Notas:** muy importante para soporte y troubleshooting

### Imagen 6
**ID:** IMG-006  
**Página:** `/productos/e-orbit/configuracion/idioma`  
**Nombre sugerido:** Interacción con panel de configuración  
**Tipo de imagen:** acción / detalle  
**Objetivo:** acompañar el flujo de cambio de idioma  
**Descripción visual:** panel de cerradura activo en proceso de configuración, mano interactuando  
**Prompt base:**  
Cerradura inteligente moderna con panel activo en modo de configuración, mano adulta interactuando con el dispositivo, fotografía realista, estilo técnico, enfoque en el panel, fondo simple y limpio, composición para artículo de ayuda  
**Negative prompt:**  
texto ilegible protagonista, interfaz fantasiosa, manos deformes, fondo recargado, reflejos extremos, estilo sci-fi  
**Formato:** vertical 4:5  
**Prioridad:** alta  
**Estado:** pendiente  
**Notas:** ideal combinar después con captura real o diagrama simple

### Imagen 7
**ID:** IMG-007  
**Página:** `/productos/e-orbit/app/agregar-dispositivo`  
**Nombre sugerido:** Uso de app para agregar dispositivo  
**Tipo de imagen:** app / contexto de uso  
**Objetivo:** mostrar el inicio del flujo desde el celular  
**Descripción visual:** persona sosteniendo smartphone frente a la puerta con la cerradura, sensación de vinculación inicial  
**Prompt base:**  
Persona adulta sosteniendo un smartphone frente a una puerta con cerradura inteligente moderna, escena de configuración de dispositivo, fotografía realista, ambiente doméstico limpio, composición clara, enfoque compartido entre celular y cerradura, estilo documental y tecnológico sobrio  
**Negative prompt:**  
pantalla con texto falso demasiado visible, manos deformes, perspectiva rara, fondo desordenado, estética publicitaria exagerada, interfaz fantasiosa  
**Formato:** horizontal 4:3  
**Prioridad:** alta  
**Estado:** pendiente  
**Notas:** si la app real se captura, esta imagen funciona como contextual

### Imagen 8
**ID:** IMG-008  
**Página:** `/productos/e-orbit/app/vincular-por-qr`  
**Nombre sugerido:** Escaneo o vinculación por QR  
**Tipo de imagen:** acción / app + producto  
**Objetivo:** explicar visualmente el encuentro entre celular y cerradura durante el flujo QR  
**Descripción visual:** smartphone mostrando código QR frente a la cerradura, escena clara y ordenada  
**Prompt base:**  
Escena realista de vinculación entre smartphone y cerradura inteligente mediante código QR, teléfono mostrando un código QR visible pero genérico frente a la cerradura, ambiente interior limpio, fotografía técnica y clara, composición didáctica, alta definición, iluminación controlada  
**Negative prompt:**  
QR deformado, texto inventado protagonista, manos extra, pantallas irreales, estilo futurista, luces de neón, fondo recargado  
**Formato:** horizontal 4:3  
**Prioridad:** alta  
**Estado:** pendiente  
**Notas:** no usar como prueba técnica del QR, solo como apoyo visual conceptual

### Imagen 9
**ID:** IMG-009  
**Página:** `/productos/e-orbit/solucion-de-problemas/no-reconoce-huella`  
**Nombre sugerido:** Problema de lectura de huella  
**Tipo de imagen:** troubleshooting / uso  
**Objetivo:** ilustrar una situación de fallo de reconocimiento  
**Descripción visual:** usuario intentando usar huella con gesto neutral de duda, foco en lector  
**Prompt base:**  
Escena realista de una persona intentando usar el lector de huella de una cerradura inteligente y encontrando una dificultad, gesto sutil de duda, enfoque en el lector y la interacción, fotografía documental, ambiente limpio, composición clara para artículo de solución de problemas  
**Negative prompt:**  
drama exagerado, gestos caricaturescos, manos deformes, fondo recargado, estética de anuncio, texto incrustado  
**Formato:** vertical 4:5  
**Prioridad:** media  
**Estado:** pendiente  
**Notas:** mantener tono sobrio, no alarmista

### Imagen 10
**ID:** IMG-010  
**Página:** `/productos/e-orbit/solucion-de-problemas/no-conecta-a-la-app`  
**Nombre sugerido:** Problema de conexión con app  
**Tipo de imagen:** troubleshooting / app  
**Objetivo:** ilustrar fallo de conexión entre celular y cerradura  
**Descripción visual:** persona con smartphone frente a cerradura, sensación de intento de conexión sin dramatismo  
**Prompt base:**  
Escena realista de una persona intentando conectar una cerradura inteligente con una aplicación móvil, smartphone en mano frente a la puerta, gesto leve de revisión o espera, ambiente doméstico limpio, composición clara y sobria para solución de problemas, fotografía realista  
**Negative prompt:**  
errores falsos gigantes en pantalla, dramatismo excesivo, fondo recargado, manos deformes, interfaz inventada compleja, estética futurista  
**Formato:** horizontal 4:3  
**Prioridad:** media  
**Estado:** pendiente  
**Notas:** si luego hay captura real de error, dejar esta como imagen secundaria

### Imagen 11
**ID:** IMG-011  
**Página:** descargas / documentación  
**Nombre sugerido:** Documentación del producto  
**Tipo de imagen:** apoyo editorial  
**Objetivo:** acompañar la sección de manuales y descargas  
**Descripción visual:** composición limpia con producto + documentos impresos o tablet con manual  
**Prompt base:**  
Composición editorial realista con una cerradura inteligente moderna junto a documentos o manuales técnicos en una mesa limpia, estilo minimalista, fotografía sobria, ambiente profesional y ordenado, útil para sección de descargas o documentación  
**Negative prompt:**  
papeles desordenados, texto protagonista ilegible, estética corporativa rígida, saturación visual, fondo recargado  
**Formato:** horizontal 16:9  
**Prioridad:** baja  
**Estado:** pendiente  
**Notas:** opcional para Fase 1, útil para enriquecer descargas

---

## 5. Prompts maestros por categoría

### A. Producto hero
**Prompt maestro:**  
Cerradura inteligente moderna instalada en una puerta residencial, fotografía realista de producto, ambiente limpio y contemporáneo, iluminación natural suave, enfoque claro en la cerradura, composición ordenada, fondo neutro, estilo técnico y elegante para centro de ayuda, alta definición

### B. Acción de uso
**Prompt maestro:**  
Persona adulta interactuando con una cerradura inteligente moderna en una puerta residencial, fotografía realista, acción clara y única, composición limpia, iluminación suave, ambiente doméstico ordenado, enfoque en el punto de interacción, estilo documental para centro de ayuda

### C. App + producto
**Prompt maestro:**  
Persona usando un smartphone junto a una cerradura inteligente moderna, escena realista de configuración o vinculación, ambiente interior limpio, composición clara y didáctica, enfoque equilibrado entre celular y cerradura, fotografía técnica y sobria

### D. Troubleshooting
**Prompt maestro:**  
Escena realista de uso de cerradura inteligente con una pequeña dificultad técnica, gesto sutil de revisión o duda, composición sobria, ambiente limpio, enfoque claro en la interacción, fotografía documental para artículo de solución de problemas

---

## 6. Negative prompt maestro sugerido
**Negative prompt maestro:**  
texto incrustado, letras ilegibles, interfaz falsa compleja, manos deformes, dedos extra, perspectiva extrema, fondo recargado, estilo futurista exagerado, luces de neón, render plástico, objetos irrelevantes, dramatismo excesivo, composición caótica, baja resolución

---

## 7. Guía rápida de formato por uso

### Hero principal
- horizontal 16:9

### Página de artículo
- horizontal 4:3 o vertical 4:5

### Tarjetas / listados
- cuadrado 1:1 o vertical 4:5

### Miniaturas de descargas
- horizontal 16:9

---

## 8. Prioridad real de producción para arrancar implementación

### Producir primero
- IMG-001 Hero principal
- IMG-002 Producto instalado
- IMG-003 Agregar administrador
- IMG-005 Uso del lector de huella
- IMG-006 Configuración / idioma
- IMG-007 Agregar dispositivo en app
- IMG-008 Vinculación por QR

### Producir después
- IMG-004 PIN
- IMG-009 Problema de huella
- IMG-010 Problema de conexión app
- IMG-011 Descargas

---

## 9. Recomendación operativa
Para implementación real, te sugiero trabajar así:

### Paso 1
Generar **1 a 3 variantes por imagen prioritaria**

### Paso 2
Elegir una por:
- claridad
- realismo
- utilidad documental
- consistencia con el producto

### Paso 3
Ajustar con una segunda ronda si hace falta:
- ángulo
- fondo
- mano/interacción
- iluminación
- encuadre

### Paso 4
Nombrar archivos de forma consistente:
- `e-orbit-hero-main.jpg`
- `e-orbit-add-admin.jpg`
- `e-orbit-fingerprint-use.jpg`
- `e-orbit-app-add-device.jpg`

---

## 10. Recomendación final
Este documento sirve como base de producción visual con IA y puede usarse en paralelo con la implementación.
