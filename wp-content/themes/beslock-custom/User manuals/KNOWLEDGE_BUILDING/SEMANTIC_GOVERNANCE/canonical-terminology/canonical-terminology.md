# Canonical terminology registry

_Schema: `semantic-governance/1.0` · canonical terminology layer · generated 2026-05-13T17:11:48Z._

## Purpose

A platform-wide canonical terminology registry. Each entry declares one
canonical name and the synonyms (across English, Spanish, brand names and
abbreviations) that resolve to it. Detection-only: this registry is consulted
during conflict scans and during retrieval expansion. It does not rename
existing files.

## Registry

| Canonical | Domain | Synonyms |
|---|---|---|
| `administrator` | terminology | `administrador`, `admin` |
| `user` | terminology | `usuario` |
| `fingerprint` | terminology | `huella`, `huella-dactilar` |
| `pin` | terminology | `contrasena`, `contrasena`, `password`, `codigo`, `codigo` |
| `temporary-password` | terminology | `virtual-password`, `contrasena-temporal`, `contrasena-temporal`, `clave-temporal` |
| `factory-reset` | terminology | `reset`, `restablecer`, `restablecer-de-fabrica`, `restauracion-de-fabrica` |
| `qr-pairing` | terminology | `qr`, `vincular-por-qr`, `alta-del-dispositivo-por-qr`, `pair-by-qr` |
| `ez-mode-pairing` | terminology | `ez-mode`, `pair-by-ez-mode`, `alta-del-dispositivo-por-wi-fi-ez-mode`, `app-pairing-ez-mode` |
| `tuya-smart-app` | terminology | `tuya`, `tuya-smart`, `tongtong-app`, `smart-life` |
| `wi-fi` | terminology | `wifi` |
| `register-fingerprint` | procedure | `registrar-una-huella`, `enrol-fingerprint`, `enroll-fingerprint` |
| `register-pin` | procedure | `registrar-una-contrasena-o-pin`, `registrar-una-contrasena`, `registrar-una-contrasena`, `add-pin`, `set-pin` |
| `add-administrator` | procedure | `agregar-un-administrador` |
| `add-user` | procedure | `agregar-un-usuario` |
| `change-language` | procedure | `cambiar-el-idioma` |
| `pair-with-app` | procedure | `conectar-la-cerradura-a-la-aplicacion`, `conectar-la-cerradura-a-la-aplicacion`, `primeros-pasos`, `local-onboarding` |
| `member-management` | procedure | `gestion-de-miembros`, `gestion-de-miembros` |

## Authoring rules

1. Canonical names are kebab-case, lowercase, ASCII-only.
2. Synonyms include language variants (es-CO baseline + en), brand variants,
   abbreviations and common typos.
3. Adding a new canonical requires (a) an entry here, (b) a check that no
   existing canonical already covers the concept, (c) a re-scan via
   `tools/knowledge_normalize_audit.py` to surface any new conflicts.
4. Changing a canonical requires a deprecation entry — the previous canonical
   becomes a synonym and is never silently dropped.

## Companion files

- [`canonical-terminology.json`](canonical-terminology.json) — machine-readable form of the table above.
