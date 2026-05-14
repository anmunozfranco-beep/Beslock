# Global knowledge ontology

_Schema: `knowledge-center/1.0` · canonical ontology layer · generated 2026-05-13T16:54:29Z._

## Purpose

Define the shared semantic primitives that span the Beslock product line. Per-product knowledge nuclei use these shared concepts as their vocabulary; product-specific concepts extend them, they do not replace them.

## Shared entity concepts

| ID | Label | Definition |
|---|---|---|
| `entity.lock-body` | lock body | Outer hardware shell mounted on the door. |
| `entity.keypad` | keypad | Touch or capacitive input surface accepting numeric codes. |
| `entity.fingerprint-sensor` | fingerprint sensor | Capacitive biometric sensor for enrolment and verification. |
| `entity.handle` | handle | Lever or knob actuating the latch. |
| `entity.deadbolt` | deadbolt | Sliding bolt mechanism actuated independently of the latch. |
| `entity.latch` | latch | Spring-loaded retracting tongue for door retention. |
| `entity.battery-bay` | battery bay | Compartment housing the AA cells (interior side). |
| `entity.emergency-port` | emergency power port | External contact point for emergency battery jump. |
| `entity.indicator-led` | indicator LED | Status indicator (colour and pattern carry meaning). |
| `entity.mortise` | mortise mechanism | Through-door mechanism connecting interior and exterior. |
| `entity.app` | companion app | Mobile companion application for pairing and management. |

## Shared procedure concepts

| ID | Label |
|---|---|
| `procedure.pairing-app` | Pair lock with app |
| `procedure.enrol-fingerprint` | Enrol fingerprint |
| `procedure.add-pin-code` | Add PIN code |
| `procedure.remove-user` | Remove user |
| `procedure.factory-reset` | Factory reset |
| `procedure.battery-replacement` | Replace batteries |
| `procedure.emergency-power` | Apply emergency power |
| `procedure.unlock-mechanical` | Unlock with mechanical key |
| `procedure.unlock-pin` | Unlock with PIN |
| `procedure.unlock-fingerprint` | Unlock with fingerprint |
| `procedure.firmware-update` | Firmware update |

## Shared warning concepts

| ID | Label |
|---|---|
| `warning.low-battery` | Low-battery warning |
| `warning.lockout-after-attempts` | Temporary lockout after failed attempts |
| `warning.tamper-alert` | Tamper alert |
| `warning.factory-reset-data-loss` | Factory reset clears all users |

## Shared capability concepts

| ID | Label |
|---|---|
| `capability.pin-unlock` | PIN unlock |
| `capability.fingerprint-unlock` | Fingerprint unlock |
| `capability.app-unlock` | App unlock |
| `capability.mechanical-key` | Mechanical key fallback |
| `capability.emergency-power` | Emergency external power |
| `capability.audit-log` | Access audit log |
| `capability.firmware-update` | Firmware update |

## Shared visual-intent concepts

| ID | Label |
|---|---|
| `visual-intent.hero` | Hero identification image |
| `visual-intent.installation` | Installation diagram |
| `visual-intent.exploded-anatomy` | Exploded anatomy |
| `visual-intent.battery-replacement` | Battery replacement step |
| `visual-intent.fingerprint-enrol` | Fingerprint enrolment step |
| `visual-intent.app-pairing` | App pairing context |
| `visual-intent.factory-reset` | Factory reset sequence |
| `visual-intent.emergency-power` | Emergency power application |

## Inheritance rule

1. Per-product nuclei reference shared concept IDs verbatim.
2. A product-specific extension adds a sub-id, e.g. `entity.keypad.e-touch.capacitive-grid-3x4`.
3. Shared concepts are immutable; their IDs are stable across products and versions.
4. Adding a shared concept requires a new entry in this ontology and a new entry in the relevant per-product schema.

## Reusable semantic primitives

- **Identifier**: stable, lowercase, dot-separated, no spaces.
- **Provenance pointer**: `{source: <oem-evidence-id>, span: <page-and-region>, extracted_at: <iso-timestamp>}`.
- **Maturity tier**: one of the eight values defined in the maturity model.
- **Locale tag**: defaults to `es-CO`; localized variants append the BCP-47 tag.
- **Channel target**: zero or more values from the publication-channel registry.

## Inventory snapshot

Per-product file counts in each semantic domain (real, observed at generation time):

| Product | entities | procedures | workflows | warnings | terminology | capabilities | specifications | troubleshooting | procedural-semantics | visual-intent | visual-risk | publication-intent | component-visibility | provenance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| e-flex | 2 | 0 | 3 | 2 | 8 | 3 | 0 | 0 | 9 | 6 | 4 | 1 | 1 | 1 |
| e-nova | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| e-orbit | 2 | 0 | 9 | 10 | 20 | 4 | 1 | 0 | 24 | 7 | 3 | 1 | 1 | 1 |
| e-prime | 2 | 0 | 2 | 4 | 7 | 3 | 0 | 0 | 9 | 5 | 3 | 1 | 1 | 1 |
| e-shield | 2 | 0 | 9 | 3 | 5 | 2 | 0 | 1 | 13 | 6 | 4 | 1 | 1 | 1 |
| e-touch | 2 | 0 | 1 | 1 | 7 | 2 | 0 | 0 | 4 | 5 | 4 | 1 | 1 | 1 |
| **totals** | **12** | **0** | **24** | **20** | **47** | **15** | **1** | **1** | **59** | **30** | **19** | **6** | **6** | **6** |
