# Procedural semantic normalization

_Schema: `semantic-governance/1.0` · procedural normalization spec · generated 2026-05-13T17:11:48Z._

## Purpose

Normalize action verbs, action granularity, procedural sequencing and
operational state transitions across all per-product procedural-semantics
artifacts.

## Canonical action verbs

| Verb |
|---|
| `press` |
| `hold` |
| `tap` |
| `swipe` |
| `scan` |
| `unlock` |
| `lock` |
| `enroll` |
| `register` |
| `remove` |
| `pair` |
| `unpair` |
| `confirm` |
| `cancel` |
| `reset` |
| `restart` |
| `power-cycle` |
| `install` |
| `uninstall` |
| `mount` |
| `dismount` |
| `configure` |
| `select` |
| `open` |
| `close` |
| `insert` |
| `extract` |
| `replace` |
| `wait` |
| `verify` |
| `observe` |

## Verb synonyms (auto-mapped during conflict detection)

| Found token | Maps to canonical |
|---|---|
| `abrir` | `open` |
| `agregar` | `add` |
| `bloquear` | `lock` |
| `cancelar` | `cancel` |
| `cerrar` | `close` |
| `configurar` | `configure` |
| `confirmar` | `confirm` |
| `desbloquear` | `unlock` |
| `desinstalar` | `uninstall` |
| `deslizar` | `swipe` |
| `desmontar` | `dismount` |
| `desvincular` | `unpair` |
| `eliminar` | `remove` |
| `escanear` | `scan` |
| `esperar` | `wait` |
| `extraer` | `extract` |
| `inscribir` | `enroll` |
| `insertar` | `insert` |
| `instalar` | `install` |
| `mantener` | `hold` |
| `mantener-presionado` | `hold` |
| `montar` | `mount` |
| `observar` | `observe` |
| `presionar` | `press` |
| `reemplazar` | `replace` |
| `registrar` | `register` |
| `reiniciar` | `restart` |
| `restablecer` | `reset` |
| `seleccionar` | `select` |
| `set` | `configure` |
| `tocar` | `tap` |
| `verificar` | `verify` |
| `vincular` | `pair` |

## Action granularity

- A procedure step represents **one user-observable action** (one button
  press, one swipe, one selection) or **one observable system state change**
  (one LED change, one tone, one screen transition).
- Multi-action steps must be decomposed before promotion.
- Implicit waits become explicit `wait` steps with a duration field.

## Sequencing contract

- Steps are 1-indexed and totally ordered.
- Branches (success / failure / retry) are modelled as sub-procedures with
  explicit links, not as inline conditionals.
- Cross-procedure links use canonical procedure IDs from the ontology.

## State-transition vocabulary

- `unlocked`, `locked`, `paired`, `unpaired`, `enrolled`, `removed`,
  `factory-default`, `low-battery`, `lockout`, `firmware-updating`.

## Companion files

- [`procedural-normalization.json`](procedural-normalization.json) — machine-readable verb registry + synonym map.
