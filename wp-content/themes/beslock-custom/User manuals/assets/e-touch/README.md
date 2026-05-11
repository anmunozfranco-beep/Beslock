# Assets de e-Touch

## 1. Objetivo
Esta carpeta está pensada para almacenar los assets visuales de `e-Touch` usados en el manual, el centro de ayuda y futuras implementaciones web o CMS.

Su propósito es:
- mantener una estructura ordenada
- separar documentación de imágenes
- facilitar reemplazos futuros
- permitir convivir imágenes generadas por IA y capturas reales

---

## 2. Convención de nombres
Usar nombres de archivo:
- en minúsculas
- con guiones medios
- sin espacios
- sin acentos
- descriptivos

### Ejemplos recomendados
- `e-touch-hero-main.jpg`
- `e-touch-installed-context.jpg`
- `e-touch-add-admin-action.jpg`
- `e-touch-pin-use.jpg`
- `e-touch-fingerprint-use.jpg`
- `e-touch-language-settings.jpg`
- `e-touch-app-add-device.jpg`
- `e-touch-link-qr.jpg`
- `e-touch-troubleshoot-fingerprint.jpg`
- `e-touch-troubleshoot-app-connection.jpg`
- `e-touch-downloads-docs.jpg`

---

## 3. Tipos de assets que pueden guardarse aquí
- imágenes generadas por IA
- capturas reales del equipo
- capturas reales de la app
- imágenes procesadas para web
- miniaturas o recortes finales

---

## 4. Recomendación de organización
Si el volumen crece, se puede subdividir así:

```text
assets/
└── e-touch/
    ├── ai-generated/
    ├── real-captures/
    ├── web-ready/
    └── thumbnails/
```

Por ahora puede mantenerse una sola carpeta mientras el volumen sea pequeño.

---

## 5. Mapeo sugerido entre imagen y página
- `e-touch-hero-main.jpg` → hub principal
- `e-touch-installed-context.jpg` → primeros pasos
- `e-touch-add-admin-action.jpg` → agregar administrador
- `e-touch-pin-use.jpg` → registrar PIN
- `e-touch-fingerprint-use.jpg` → registrar huella
- `e-touch-language-settings.jpg` → cambiar idioma
- `e-touch-app-add-device.jpg` → agregar dispositivo
- `e-touch-link-qr.jpg` → vincular por QR
- `e-touch-troubleshoot-fingerprint.jpg` → no reconoce huella
- `e-touch-troubleshoot-app-connection.jpg` → no conecta a la app
- `e-touch-downloads-docs.jpg` → descargas

---

## 6. Checklist antes de agregar un asset
- [ ] El archivo tiene nombre consistente
- [ ] La imagen corresponde a una página o módulo real
- [ ] La calidad visual es suficiente
- [ ] No depende de texto generado poco confiable
- [ ] El recorte funciona para su uso previsto
- [ ] El archivo final está optimizado si va a web

---

## 7. Recomendación operativa
Usar primero imágenes IA como apoyo inicial y sustituirlas por capturas reales cuando existan mejores evidencias visuales del producto o la app.
