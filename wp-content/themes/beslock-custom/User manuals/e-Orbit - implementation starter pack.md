# e-Orbit
## Paquete inicial de implementación para contenido e imágenes IA

## 1. Objetivo
Este documento conecta la implementación inicial del centro de ayuda de e-Orbit con el primer lote de imágenes generadas por IA.

Está pensado para ayudar con:
- implementación del MVP Fase 1
- coordinación entre contenido e imágenes
- nombrado y organización de archivos
- priorización de assets visuales
- planeación de integración en CMS o frontend

---

## 2. Páginas prioritarias para Fase 1
La implementación inicial debería priorizar estas páginas:

- `/productos/e-orbit`
- `/productos/e-orbit/primeros-pasos`
- `/productos/e-orbit/usuarios/agregar-administrador`
- `/productos/e-orbit/usuarios/agregar-usuario`
- `/productos/e-orbit/uso/pin`
- `/productos/e-orbit/uso/huella`
- `/productos/e-orbit/configuracion/idioma`
- `/productos/e-orbit/app/agregar-dispositivo`
- `/productos/e-orbit/app/vincular-por-qr`
- `/productos/e-orbit/solucion-de-problemas/no-reconoce-huella`
- `/productos/e-orbit/solucion-de-problemas/no-conecta-a-la-app`

---

## 3. Assets visuales prioritarios
Producir primero:

1. `e-orbit-hero-main.jpg`
2. `e-orbit-installed-context.jpg`
3. `e-orbit-add-admin-action.jpg`
4. `e-orbit-fingerprint-use.jpg`
5. `e-orbit-language-settings.jpg`
6. `e-orbit-app-add-device.jpg`
7. `e-orbit-link-qr.jpg`

Producir después:

8. `e-orbit-pin-use.jpg`
9. `e-orbit-troubleshoot-fingerprint.jpg`
10. `e-orbit-troubleshoot-app-connection.jpg`
11. `e-orbit-downloads-docs.jpg`

---

## 4. Mapeo sugerido entre asset y página

### Hub
- página: `/productos/e-orbit`
- imagen principal: `e-orbit-hero-main.jpg`

### Primeros pasos
- página: `/productos/e-orbit/primeros-pasos`
- imagen principal: `e-orbit-installed-context.jpg`

### Agregar administrador
- página: `/productos/e-orbit/usuarios/agregar-administrador`
- imagen principal: `e-orbit-add-admin-action.jpg`

### PIN
- página: `/productos/e-orbit/uso/pin`
- imagen principal: `e-orbit-pin-use.jpg`

### Huella
- página: `/productos/e-orbit/uso/huella`
- imagen principal: `e-orbit-fingerprint-use.jpg`

### Idioma
- página: `/productos/e-orbit/configuracion/idioma`
- imagen principal: `e-orbit-language-settings.jpg`

### Agregar dispositivo en app
- página: `/productos/e-orbit/app/agregar-dispositivo`
- imagen principal: `e-orbit-app-add-device.jpg`

### Vincular por QR
- página: `/productos/e-orbit/app/vincular-por-qr`
- imagen principal: `e-orbit-link-qr.jpg`

### Troubleshooting de huella
- página: `/productos/e-orbit/solucion-de-problemas/no-reconoce-huella`
- imagen principal: `e-orbit-troubleshoot-fingerprint.jpg`

### Troubleshooting de app
- página: `/productos/e-orbit/solucion-de-problemas/no-conecta-a-la-app`
- imagen principal: `e-orbit-troubleshoot-app-connection.jpg`

---

## 5. Organización sugerida de carpetas
Si más adelante el repositorio almacena las imágenes generadas, una estructura limpia podría ser:

```text
User manuals/
├── e-Orbit user manual.pdf
├── e-Orbit - image generation matrix.md
├── e-Orbit - AI image prompts.md
├── e-Orbit - implementation starter pack.md
└── assets/
    └── e-orbit/
        ├── e-orbit-hero-main.jpg
        ├── e-orbit-installed-context.jpg
        ├── e-orbit-add-admin-action.jpg
        ├── e-orbit-fingerprint-use.jpg
        ├── e-orbit-language-settings.jpg
        ├── e-orbit-app-add-device.jpg
        ├── e-orbit-link-qr.jpg
        ├── e-orbit-troubleshoot-fingerprint.jpg
        ├── e-orbit-troubleshoot-app-connection.jpg
        └── e-orbit-downloads-docs.jpg
```

---

## 6. Checklist de integración
Usar esta lista antes de conectar las imágenes al sitio:

- [ ] El archivo existe
- [ ] La imagen es visualmente clara
- [ ] La imagen corresponde a la página esperada
- [ ] La imagen no depende de texto generado correcto
- [ ] El recorte funciona para el uso previsto
- [ ] El nombre de archivo es consistente
- [ ] El asset está optimizado para web si hace falta

---

## 7. Flujo recomendado de generación

### Paso 1
Generar 3 variantes para cada imagen prioritaria.

### Paso 2
Elegir una variante por:
- claridad
- realismo
- utilidad documental
- consistencia con el producto

### Paso 3
Refinar las elegidas si hace falta cambiando:
- ángulo
- iluminación
- fondo
- posición de la mano
- encuadre

### Paso 4
Exportar la versión elegida con el nombre final de archivo.

---

## 8. Recomendación de implementación
Empezar la implementación ya con:
- contenido estructurado
- nombres de archivos definidos
- assets IA producidos en paralelo

Esto permite que frontend o CMS avancen sin esperar un paquete visual final perfecto.

---

## 9. Recomendación final
Estos documentos sirven para apoyar el primer ciclo de implementación y reducir improvisación entre contenido, diseño y UI.
