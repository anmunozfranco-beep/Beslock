# Assets de e-Nova

## 1. Objetivo
Esta carpeta está pensada para almacenar los assets visuales de `e-Nova` usados en el manual, el centro de ayuda y futuras implementaciones web o CMS.

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
- `e-nova-hero-main.jpg`
- `e-nova-installed-context.jpg`
- `e-nova-add-admin-action.jpg`
- `e-nova-pin-use.jpg`
- `e-nova-fingerprint-use.jpg`
- `e-nova-language-settings.jpg`
- `e-nova-app-add-device.jpg`
- `e-nova-link-qr.jpg`
- `e-nova-troubleshoot-fingerprint.jpg`
- `e-nova-troubleshoot-app-connection.jpg`
- `e-nova-downloads-docs.jpg`

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
└── e-nova/
    ├── ai-generated/
    ├── real-captures/
    ├── web-ready/
    └── thumbnails/
```

Por ahora puede mantenerse una sola carpeta mientras el volumen sea pequeño.

---

## 5. Mapeo sugerido entre imagen y página
- `e-nova-hero-main.jpg` → hub principal
- `e-nova-installed-context.jpg` → primeros pasos
- `e-nova-add-admin-action.jpg` → agregar administrador
- `e-nova-pin-use.jpg` → registrar PIN
- `e-nova-fingerprint-use.jpg` → registrar huella
- `e-nova-language-settings.jpg` → cambiar idioma
- `e-nova-app-add-device.jpg` → agregar dispositivo
- `e-nova-link-qr.jpg` → vincular por QR
- `e-nova-troubleshoot-fingerprint.jpg` → no reconoce huella
- `e-nova-troubleshoot-app-connection.jpg` → no conecta a la app
- `e-nova-downloads-docs.jpg` → descargas

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
