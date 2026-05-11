# Assets de e-Shield

## 1. Objetivo
Esta carpeta está pensada para almacenar los assets visuales de `e-Shield` usados en el manual, el centro de ayuda y futuras implementaciones web o CMS.

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
- `e-shield-hero-main.jpg`
- `e-shield-installed-context.jpg`
- `e-shield-add-admin-action.jpg`
- `e-shield-pin-use.jpg`
- `e-shield-fingerprint-use.jpg`
- `e-shield-language-settings.jpg`
- `e-shield-app-add-device.jpg`
- `e-shield-link-qr.jpg`
- `e-shield-troubleshoot-fingerprint.jpg`
- `e-shield-troubleshoot-app-connection.jpg`
- `e-shield-downloads-docs.jpg`

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
└── e-shield/
    ├── ai-generated/
    ├── real-captures/
    ├── web-ready/
    └── thumbnails/
```

Por ahora puede mantenerse una sola carpeta mientras el volumen sea pequeño.

---

## 5. Mapeo sugerido entre imagen y página
- `e-shield-hero-main.jpg` → hub principal
- `e-shield-installed-context.jpg` → primeros pasos
- `e-shield-add-admin-action.jpg` → agregar administrador
- `e-shield-pin-use.jpg` → registrar PIN
- `e-shield-fingerprint-use.jpg` → registrar huella
- `e-shield-language-settings.jpg` → cambiar idioma
- `e-shield-app-add-device.jpg` → agregar dispositivo
- `e-shield-link-qr.jpg` → vincular por QR
- `e-shield-troubleshoot-fingerprint.jpg` → no reconoce huella
- `e-shield-troubleshoot-app-connection.jpg` → no conecta a la app
- `e-shield-downloads-docs.jpg` → descargas

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
