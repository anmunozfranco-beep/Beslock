# Knowledge consumption flow

_Schema: `experience-governance/1.0` · consumption model · generated 2026-05-13T17:27:13Z._

## Prerequisite chains

| Concept | Requires |
|---|---|
| `procedure.unlock-pin` | `procedure.register-pin` |
| `procedure.unlock-fingerprint` | `procedure.register-fingerprint` |
| `procedure.register-fingerprint` | `procedure.add-administrator`, `concept.management-menu-access` |
| `procedure.register-pin` | `procedure.add-administrator`, `concept.management-menu-access` |
| `procedure.add-user` | `procedure.add-administrator` |
| `procedure.add-administrator` | `procedure.first-power-on` |
| `procedure.first-power-on` | `procedure.battery-installation` |
| `procedure.pair-with-app` | `procedure.add-administrator`, `concept.companion-app-installed` |
| `procedure.qr-pairing` | `procedure.pair-with-app` |
| `procedure.ez-mode-pairing` | `procedure.pair-with-app` |
| `procedure.factory-reset` | `concept.data-loss-acknowledgement` |
| `procedure.firmware-update` | `procedure.pair-with-app`, `concept.stable-power-source` |
| `procedure.battery-replacement` | `concept.battery-bay-access` |
| `procedure.emergency-power` | `concept.9v-source-available` |
| `procedure.member-management` | `procedure.pair-with-app` |

## Learning paths

### Beginner — first 24 hours (`path.beginner`)

1. `procedure.battery-installation`
2. `procedure.first-power-on`
3. `procedure.add-administrator`
4. `procedure.register-pin`
5. `procedure.unlock-pin`

### Intermediate — first week (`path.intermediate`)

1. `procedure.register-fingerprint`
2. `procedure.unlock-fingerprint`
3. `procedure.add-user`
4. `procedure.pair-with-app`
5. `procedure.qr-pairing`

### Advanced — full ownership (`path.advanced`)

1. `procedure.member-management`
2. `procedure.firmware-update`
3. `procedure.factory-reset`
4. `procedure.emergency-power`


## Rules

1. A surface MUST NOT present a procedure before its prerequisites have been
   surfaced or marked as already-known.
2. A surface SHOULD detect prior completion by reading run records / user
   state and skip already-mastered prerequisites.
3. A surface MAY collapse adjacent low-load procedures into a single
   walkthrough; high-load procedures MUST stand alone.
4. Beginner → intermediate → advanced is the default ordering; surfaces MAY
   override only with editorial justification.

## Companion files

- [`prerequisites.json`](prerequisites.json)
- [`learning-paths.json`](learning-paths.json)
