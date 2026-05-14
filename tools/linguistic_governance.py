"""
Phase 38 — GOVERNED LINGUISTIC RENDERING & COLOMBIAN OPERATIONAL LANGUAGE.

Constitutional layer 31. Modeling-only authoring + four publication-time
renderer utilities (pure functions; do NOT mutate knowledge-core; not wired
into the renderer yet — wiring is the next executable track).

Subordinate to knowledge-core, the 30 prior governance layers, and the
executable publication renderer (layer 36).

Writes:
  - publication-system/linguistic-governance/{colombian-spanish-doctrine,
    terminology, normalization-rules, renderers, reports}/
  - KNOWLEDGE_BUILDING/LINGUISTIC_GOVERNANCE/ (constitutional doctrine root)
  - _repository-governance/reports/linguistic-governance/01..10.{json,md}

Idempotent. Non-destructive. Touches no runtime code. Writes NO content into
knowledge-core. Generates NO prompts and NO images. ComfyUI is NOT invoked.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
PUB_SYS_ROOT = THEME_ROOT / "publication-system"
LING_ROOT = PUB_SYS_ROOT / "linguistic-governance"
DOCTRINE_ROOT = LING_ROOT / "colombian-spanish-doctrine"
TERM_ROOT = LING_ROOT / "terminology"
NORM_ROOT = LING_ROOT / "normalization-rules"
RENDER_ROOT = LING_ROOT / "renderers"
LING_REPORTS_ROOT = LING_ROOT / "reports"
CONST_ROOT = THEME_ROOT / "KNOWLEDGE_BUILDING" / "LINGUISTIC_GOVERNANCE"
REPORTS_ROOT = THEME_ROOT / "_repository-governance" / "reports" / "linguistic-governance"

SCHEMA = "linguistic-governance/1.0"
NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")

SUBORDINATE_TO = [
    "knowledge-core/1.0",
    "publication-quality-governance/1.0",
    "publication-rendering/1.0",
    "publication-and-delivery-governance/1.0",
    "operational-pilot-governance/1.0",
    "ecosystem-normalization-governance/1.0",
    "reference-stack-governance/1.0",
    "environment-integration-governance/1.0",
    "human-operations-governance/1.0",
    "knowledge-operations-governance/1.0",
    "knowledge-lifecycle-governance/1.0",
    "runtime-hardening-governance/1.0",
    "runtime-implementation-governance/1.0",
    "runtime-orchestration-governance/1.0",
    "runtime-governance/1.0",
    "operational-proof-governance/1.0",
    "prototype-runtime-governance/1.0",
    "realization-and-deployment-governance/1.0",
    "execution-governance/1.0",
    "decision-intelligence-governance/1.0",
    "reasoning-governance/1.0",
    "lifecycle-governance/1.0",
    "composition-governance/1.0",
    "continuity-governance/1.0",
    "ecosystem-interoperability-governance/1.0",
    "adaptive-operational-governance/1.0",
    "repo-governance/1.0",
    "visual-governance/1.0",
    "visual-constitution/1.0",
]


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def write_json(p: Path, payload: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def write_text(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def envelope(layer: str, summary: str) -> Dict[str, Any]:
    return {
        "schema": SCHEMA,
        "layer": layer,
        "summary": summary,
        "generated_at": NOW,
        "modeling_only": True,
        "non_destructive": True,
        "idempotent": True,
        "touches_runtime": False,
        "mutates_knowledge_core": False,
        "generates_prompts": False,
        "generates_images": False,
        "invokes_comfyui": False,
        "subordinate_to": SUBORDINATE_TO,
        "applied_at": "publication-rendering-time-only",
        "out_of_scope": [
            "autonomous rewriting",
            "hallucinated editorialization",
            "stylistic creativity",
            "frontend styling",
            "visual generation",
            "image prompts",
            "new cognition architecture",
        ],
    }


# ---------------------------------------------------------------------------
# TASK 1 — Colombian operational language doctrine
# ---------------------------------------------------------------------------

def task_doctrine() -> None:
    docs = {
        "operational-language-principles.md": (
            "# Colombian operational language principles\n\n"
            "Target dialect: **español operativo colombiano neutro** — clear, professional, "
            "second-person formal (`usted`), present indicative for instructions, present "
            "subjunctive only for conditional branches.\n\n"
            "Principles:\n\n"
            "- The knowledge-core remains the source of truth. Linguistic normalisation "
            "  occurs ONLY at publication rendering time and never mutates knowledge-core.\n"
            "- Procedural truth, warning severity, and escalation semantics MUST be preserved "
            "  bit-for-bit through any linguistic transform.\n"
            "- Prefer the Colombian-neutral register over regionalisms (no `parcero`, no `chévere`, "
            "  no `pues` as a discourse marker, no `ahorita` as 'now').\n"
            "- Avoid Iberian forms in instructions (`vosotros`, `coger` → use `ustedes`, `tomar`/`agarrar`).\n"
            "- No idioms, no marketing tone, no euphemisms.\n"
            "- Numeric and unit notation: decimal comma (`3,5 V`), thin space before unit (`60 s`).\n"
            "- Spanish quotation marks `«…»` for quoted UI strings; preserve original casing.\n"
        ),
        "tone-governance.md": (
            "# Tone governance\n\n"
            "- Instructional tone is direct, professional and second-person formal: `Pulse`, "
            "  `Ingrese`, `Confirme`, `Verifique`.\n"
            "- Never use first person (`vamos a…`, `te enseño…`).\n"
            "- Never use marketing adjectives (`fácil`, `rápido`, `increíble`, `intuitivo`).\n"
            "- Warnings are factual: state the condition, the consequence, and the operator action. "
            "  Do not soften with `por favor` or `recomendamos`.\n"
            "- Troubleshooting is diagnostic and neutral: no blame language (`usted hizo mal`), "
            "  no apologies (`lamentamos…`).\n"
        ),
        "readability-rules.md": (
            "# Readability rules (Colombian operational Spanish)\n\n"
            "- Sentence length: 6–18 words per instructional sentence; hard cap 24.\n"
            "- One verb of action per step. Compound steps joined by `y`, `luego`, `después` are "
            "  forbidden when each clause is a separate observable action.\n"
            "- Prefer active voice (`Pulse el botón`) over passive (`El botón debe ser pulsado`).\n"
            "- Prefer concrete objects (`la cerradura`, `la app`, `el código`) over pronouns.\n"
            "- Conditional branches must be explicit: `Si X, realice A; de lo contrario, realice B.`\n"
            "- Tooling, menu paths and UI labels are wrapped in `«…»` and preserve original casing.\n"
            "- Numbers in steps are written as digits (`5`, `15 s`), not words.\n"
        ),
        "ambiguity-prevention.md": (
            "# Ambiguity prevention\n\n"
            "Forbidden constructs in instructional text:\n\n"
            "- Vague pronouns without antecedent (`hágalo`, `tóquelo`).\n"
            "- Vague quantifiers in steps (`unos segundos`, `varias veces`, `algunos pasos`).\n"
            "- Ambiguous time markers (`luego`, `después` without explicit ordering).\n"
            "- Conditional steps without a resolved branch (`si es necesario`).\n"
            "- Passive voice with deleted agent (`se debe configurar`).\n"
            "- Redundant fillers (`de manera adecuada`, `correctamente`, `según corresponda`).\n\n"
            "Required constructs:\n\n"
            "- Sujeto + verbo + objeto + observación esperada.\n"
            "- Ramas explícitas con resolución completa.\n"
            "- Tiempos cuantificados (`espere 10 segundos`, no `espere un momento`).\n"
        ),
    }
    for name, body in docs.items():
        write_text(DOCTRINE_ROOT / name, body)
    write_json(DOCTRINE_ROOT / "manifest.json", {
        **envelope("colombian-spanish-doctrine", "Doctrine for Colombian operational Spanish."),
        "documents": list(docs.keys()),
        "register": "colombiano-neutro-operativo",
        "form_of_address": "usted (formal)",
    })


# ---------------------------------------------------------------------------
# TASK 2 — Terminology governance
# ---------------------------------------------------------------------------

def task_terminology() -> None:
    write_json(TERM_ROOT / "canonical-lock-terms.json", {
        **envelope("terminology", "Canonical Colombian operational terminology for smart locks."),
        "policy": "publication-time substitution from any listed alias to the canonical term; never edit knowledge-core text.",
        "terms": [
            {"canonical": "cerradura inteligente", "category": "device", "aliases": ["smart lock", "lock", "candado inteligente", "cerrojo inteligente"]},
            {"canonical": "panel de la cerradura", "category": "device-surface", "aliases": ["panel", "lock panel", "front panel", "panel frontal"]},
            {"canonical": "teclado", "category": "device-surface", "aliases": ["keypad", "panel numérico", "keypad numérico"]},
            {"canonical": "lector de huella", "category": "device-surface", "aliases": ["fingerprint reader", "sensor de huella", "fingerprint sensor"]},
            {"canonical": "tarjeta RFID", "category": "credential", "aliases": ["tarjeta", "RFID card", "tag RFID"]},
            {"canonical": "código numérico", "category": "credential", "aliases": ["PIN", "código", "clave numérica", "passcode"]},
            {"canonical": "credencial", "category": "credential", "aliases": ["credential", "método de acceso"]},
            {"canonical": "aplicación", "category": "software", "aliases": ["app", "aplicación móvil", "mobile app"]},
            {"canonical": "vinculación", "category": "operation", "aliases": ["pairing", "emparejamiento", "asociación", "enlace"]},
            {"canonical": "vincular", "category": "operation-verb", "aliases": ["emparejar", "asociar", "enlazar", "pair"]},
            {"canonical": "registrar", "category": "operation-verb", "aliases": ["enrolar", "dar de alta", "enroll"]},
            {"canonical": "administrador", "category": "role", "aliases": ["admin", "administrator"]},
            {"canonical": "usuario", "category": "role", "aliases": ["user", "miembro"]},
            {"canonical": "código de respaldo", "category": "credential", "aliases": ["backup code", "código de emergencia"]},
            {"canonical": "modo EZ", "category": "feature", "aliases": ["EZ Mode", "modo fácil"]},
            {"canonical": "código QR", "category": "credential-channel", "aliases": ["QR", "QR code", "código de barras 2D"]},
            {"canonical": "Wi-Fi", "category": "connectivity", "aliases": ["wifi", "WiFi", "wi fi", "red inalámbrica"]},
            {"canonical": "Bluetooth", "category": "connectivity", "aliases": ["BT", "bluetooth"]},
            {"canonical": "restablecer", "category": "operation-verb", "aliases": ["resetear", "reset", "reiniciar de fábrica"]},
            {"canonical": "restablecimiento de fábrica", "category": "operation", "aliases": ["factory reset", "reseteo de fábrica", "hard reset"]},
            {"canonical": "batería", "category": "power", "aliases": ["pila", "battery"]},
            {"canonical": "batería baja", "category": "state", "aliases": ["low battery", "pila baja"]},
            {"canonical": "advertencia", "category": "safety", "aliases": ["warning", "aviso", "atención"]},
            {"canonical": "operación irreversible", "category": "safety", "aliases": ["irreversible operation", "acción no reversible"]},
            {"canonical": "escalar al canal de soporte", "category": "escalation", "aliases": ["contactar soporte", "elevar a soporte", "raise to support"]},
            {"canonical": "diagnóstico", "category": "troubleshooting", "aliases": ["diagnosis", "diagnostic"]},
            {"canonical": "verificación posterior", "category": "validation", "aliases": ["post-install verification", "verificación post instalación"]},
            {"canonical": "plantilla de instalación", "category": "installation", "aliases": ["drilling template", "plantilla de perforación"]},
        ],
    })

    write_json(TERM_ROOT / "operational-verbs.json", {
        **envelope("terminology", "Canonical operational verbs (imperative, usted form)."),
        "policy": "use only canonical verbs in instructional steps; aliases are normalised at render time.",
        "verbs": [
            {"canonical": "Pulse", "category": "physical-input", "aliases": ["Presione", "Oprima", "Toque (físico)"]},
            {"canonical": "Toque", "category": "touch-input", "aliases": ["Tap", "Pulse (táctil)"]},
            {"canonical": "Mantenga pulsado", "category": "physical-input", "aliases": ["Mantenga presionado", "Sostenga", "Long press"]},
            {"canonical": "Ingrese", "category": "data-entry", "aliases": ["Introduzca", "Digite", "Escriba"]},
            {"canonical": "Seleccione", "category": "menu", "aliases": ["Elija", "Escoja", "Marque"]},
            {"canonical": "Confirme", "category": "decision", "aliases": ["Acepte", "Valide", "Apruebe"]},
            {"canonical": "Verifique", "category": "observation", "aliases": ["Compruebe", "Confirme visualmente", "Asegúrese"]},
            {"canonical": "Espere", "category": "wait", "aliases": ["Aguarde"]},
            {"canonical": "Abra", "category": "ui-action", "aliases": ["Inicie", "Lance"]},
            {"canonical": "Cierre", "category": "ui-action", "aliases": ["Salga de"]},
            {"canonical": "Vincule", "category": "pairing", "aliases": ["Empareje", "Asocie", "Enlace"]},
            {"canonical": "Registre", "category": "enrolment", "aliases": ["Enrole", "Dé de alta"]},
            {"canonical": "Restablezca", "category": "reset", "aliases": ["Resetee", "Reinicie de fábrica"]},
            {"canonical": "Conecte", "category": "connectivity", "aliases": ["Vincule a la red", "Acople"]},
            {"canonical": "Reemplace", "category": "maintenance", "aliases": ["Cambie", "Sustituya"]},
        ],
    })

    write_json(TERM_ROOT / "warnings-taxonomy.json", {
        **envelope("terminology", "Canonical warning taxonomy and required structural fields."),
        "warning_classes": [
            {
                "id": "irreversible-operation",
                "label_es": "Operación irreversible",
                "severity": "high",
                "operator_action_required": True,
                "required_fields": ["consequence", "trigger_condition", "operator_action"],
                "render_position": "immediately-before-triggering-step",
            },
            {
                "id": "low-battery",
                "label_es": "Batería baja",
                "severity": "medium",
                "operator_action_required": True,
                "required_fields": ["consequence", "trigger_condition", "operator_action"],
            },
            {
                "id": "installation-hazard",
                "label_es": "Riesgo en la instalación",
                "severity": "high",
                "operator_action_required": True,
                "required_fields": ["consequence", "trigger_condition", "operator_action"],
            },
            {
                "id": "escalation-required",
                "label_es": "Escalamiento requerido",
                "severity": "high",
                "operator_action_required": True,
                "required_fields": ["channel_reference", "diagnostic_packet"],
            },
            {
                "id": "operational-warning",
                "label_es": "Advertencia operativa",
                "severity": "medium",
                "operator_action_required": False,
                "required_fields": ["consequence", "trigger_condition"],
            },
            {
                "id": "informational-note",
                "label_es": "Nota",
                "severity": "low",
                "operator_action_required": False,
                "required_fields": ["text"],
            },
        ],
        "rendering_rule": "warning labels are rendered in Colombian operational Spanish; severity and irreversibility flags are preserved verbatim from knowledge-core.",
    })

    write_json(TERM_ROOT / "forbidden-phrases.json", {
        **envelope("terminology", "Phrases forbidden in instructional text — replaced or flagged at render time."),
        "policy": "if a forbidden phrase appears in rendered output, surface as readability defect; do NOT mutate knowledge-core.",
        "categories": {
            "marketing": [
                "fácil de usar", "increíblemente sencillo", "rápido y seguro",
                "intuitivo", "innovador", "líder en el mercado",
            ],
            "softeners": [
                "por favor", "le recomendamos", "le sugerimos", "es aconsejable",
                "trate de", "intente",
            ],
            "vagueness": [
                "unos segundos", "un momento", "varias veces", "algunos pasos",
                "de manera adecuada", "correctamente", "según corresponda",
                "si es necesario", "si aplica",
            ],
            "blame": [
                "usted hizo mal", "se equivocó", "es su responsabilidad asegurarse",
            ],
            "regionalisms_non_neutral": [
                "parcero", "chévere", "bacano", "ahorita (en sentido temporal de 'ya')",
                "vosotros", "coged", "ordenador (cuando se refiere a la app)",
            ],
            "broken_oem_translations": [
                "por favor de presionar", "haga el favor de presionar",
                "el bloqueo se debe ser conectado", "la cerradura es necesitar reiniciarse",
                "agregar de un usuario", "para de hacer la vinculación",
            ],
        },
    })


# ---------------------------------------------------------------------------
# TASK 3 — OEM language normalization rules
# ---------------------------------------------------------------------------

def task_normalization() -> None:
    write_json(NORM_ROOT / "ocr-cleanup-rules.json", {
        **envelope("normalization", "OCR artifact cleanup applied at render time only."),
        "rules": [
            {"id": "strip-control-chars", "match_regex": "[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]", "replace_with": " ", "preserves_meaning": True},
            {"id": "collapse-whitespace", "match_regex": "[ \\t]{2,}", "replace_with": " ", "preserves_meaning": True},
            {"id": "trim-line-edges", "match_regex": "^\\s+|\\s+$", "replace_with": "", "preserves_meaning": True, "per_line": True},
            {"id": "fix-broken-accents-i", "match_regex": "\\bi\\u0301", "replace_with": "í", "preserves_meaning": True},
            {"id": "fix-broken-accents-a", "match_regex": "\\ba\\u0301", "replace_with": "á", "preserves_meaning": True},
            {"id": "fix-stray-bullets", "match_regex": "^[•·\\*\\-]\\s+", "replace_with": "- ", "per_line": True, "preserves_meaning": True},
            {"id": "fix-question-mark-paren", "match_regex": "\\?\\?\\?", "replace_with": "?", "preserves_meaning": True},
            {"id": "ocr-zero-vs-O", "policy": "do-not-auto-fix", "rationale": "ambiguous; flag for reviewer instead of mutating"},
            {"id": "ocr-l-vs-1", "policy": "do-not-auto-fix", "rationale": "ambiguous; flag for reviewer instead of mutating"},
        ],
        "boundary_rule": "rules apply to rendered text only; knowledge-core JSON is never modified.",
    })

    write_json(NORM_ROOT / "oem-translation-normalization.json", {
        **envelope("normalization", "OEM Spanish cleanup — replaces broken machine translations with Colombian operational forms."),
        "policy": "publication-time substitution; only surface-level wording is changed; semantic content is preserved.",
        "substitutions": [
            {"from": "por favor de presionar", "to": "Pulse"},
            {"from": "haga el favor de presionar", "to": "Pulse"},
            {"from": "haga el favor de", "to": ""},
            {"from": "es necesitar", "to": "se debe"},
            {"from": "se debe ser conectado", "to": "se conecta"},
            {"from": "agregar de un", "to": "agregar un"},
            {"from": "para de hacer", "to": "para realizar"},
            {"from": "hacer click", "to": "pulsar"},
            {"from": "hacer clic", "to": "pulsar"},
            {"from": "click en", "to": "pulse"},
            {"from": "presionar el botón", "to": "pulsar el botón"},
            {"from": "configure por", "to": "configure para"},
            {"from": "después que", "to": "después de que"},
            {"from": "luego que", "to": "después de que"},
            {"from": "al haberse", "to": "una vez"},
        ],
        "ambiguous_cases": [
            {"phrase": "el bloqueo", "note": "may mean 'la cerradura' (device) or 'el bloqueo' (state); reviewer must disambiguate"},
            {"phrase": "el dispositivo", "note": "acceptable but prefer 'la cerradura' when the referent is the lock"},
        ],
    })

    write_json(NORM_ROOT / "sentence-simplification.json", {
        **envelope("normalization", "Sentence-level simplification rules."),
        "rules": [
            {"id": "split-on-conjunctive-action", "rule": "if a sentence contains two independent imperative actions joined by 'y' or 'luego', split into two steps"},
            {"id": "remove-fillers", "rule": "remove fillers from forbidden-phrases.vagueness without altering procedural meaning"},
            {"id": "collapse-double-negatives", "rule": "rewrite 'no … sin' into a positive form when meaning is preserved"},
            {"id": "active-voice-preference", "rule": "rewrite passive constructions with clear agent into active voice"},
            {"id": "concrete-object-substitution", "rule": "replace ambiguous pronouns with the canonical object name"},
        ],
        "non_application_cases": [
            "warnings whose original phrasing is required for safety semantics",
            "OEM-cited verbatim text bound by source-of-truth provenance",
        ],
    })

    write_json(NORM_ROOT / "procedural-language-rules.json", {
        **envelope("normalization", "Step-level procedural language rules."),
        "rules": [
            {"id": "step-form", "rule": "verb in imperative (usted) + object + expected observation"},
            {"id": "step-numbering", "rule": "renderer numbers steps; knowledge-core text must not embed step numbers"},
            {"id": "ui-string-quoting", "rule": "wrap UI labels in «…» and preserve original casing"},
            {"id": "menu-path-rendering", "rule": "menu paths rendered as `«A» → «B» → «C»` regardless of source separator"},
            {"id": "credential-naming", "rule": "use canonical credential terms from canonical-lock-terms"},
            {"id": "branch-explicitness", "rule": "every conditional must resolve both branches"},
        ],
    })


# ---------------------------------------------------------------------------
# TASK 5 + supporting renderers — pure, importable utility modules
# ---------------------------------------------------------------------------

LINGUISTIC_NORMALIZER_PY = '''"""
linguistic_normalizer — pure utility for publication-time text cleanup.

Hard guarantees:
- never opens or mutates any file
- never invokes the network
- never imports knowledge-core
- preserves procedural meaning (rules carry `preserves_meaning` flags)
- safe to call from the publication renderer

Loads its rules from sibling JSON files at call time. Rules are advisory
substitutions; callers may pass `dry_run=True` to receive the unmodified
text plus a defect report.

This module is NOT yet wired into tools/publication_renderer.py.
Wiring is the next executable track.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

_HERE = Path(__file__).resolve().parent
_RULES_ROOT = _HERE.parent / "normalization-rules"


def _load(name: str) -> dict:
    p = _RULES_ROOT / name
    with p.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def normalize_ocr(text: str) -> Tuple[str, List[str]]:
    """Apply OCR cleanup rules. Returns (cleaned_text, applied_rule_ids)."""
    cfg = _load("ocr-cleanup-rules.json")
    applied: List[str] = []
    out = text
    for rule in cfg.get("rules", []):
        if rule.get("policy") == "do-not-auto-fix":
            continue
        pattern = rule.get("match_regex")
        if not pattern:
            continue
        flags = re.MULTILINE if rule.get("per_line") else 0
        new_out = re.sub(pattern, rule.get("replace_with", ""), out, flags=flags)
        if new_out != out:
            applied.append(rule["id"])
            out = new_out
    return out, applied


def normalize_oem(text: str) -> Tuple[str, List[str]]:
    """Apply OEM translation substitutions. Returns (text, applied_substitution_phrases)."""
    cfg = _load("oem-translation-normalization.json")
    applied: List[str] = []
    out = text
    for sub in cfg.get("substitutions", []):
        src = sub["from"]
        if src and src.lower() in out.lower():
            pattern = re.compile(re.escape(src), re.IGNORECASE)
            new_out, n = pattern.subn(sub["to"], out)
            if n > 0:
                applied.append(src)
                out = new_out
    # collapse double spaces created by removals
    out = re.sub(r"[ \\t]{2,}", " ", out).strip()
    return out, applied


def normalize_text(text: str) -> Dict[str, object]:
    """Run OCR + OEM normalisation. Returns a structured render-time report."""
    after_ocr, ocr_rules = normalize_ocr(text)
    final, oem_rules = normalize_oem(after_ocr)
    return {
        "original": text,
        "normalized": final,
        "ocr_rules_applied": ocr_rules,
        "oem_substitutions_applied": oem_rules,
        "changed": final != text,
    }


__all__ = ["normalize_ocr", "normalize_oem", "normalize_text"]
'''

TERMINOLOGY_ENFORCER_PY = '''"""
terminology_enforcer — substitutes alias terms with canonical Colombian terms.

Pure function over text. No file mutations. No knowledge-core access.
Loads canonical-lock-terms.json and operational-verbs.json from the sibling
terminology directory. Reports every substitution for renderer disclosure.

NOT yet wired into the publication renderer. Wiring is the next executable track.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

_HERE = Path(__file__).resolve().parent
_TERM_ROOT = _HERE.parent / "terminology"


def _load(name: str) -> dict:
    with (_TERM_ROOT / name).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _build_substitution_table(*sources: str) -> List[Tuple[str, str, str]]:
    """Returns a list of (alias, canonical, source_id) sorted by alias length desc."""
    table: List[Tuple[str, str, str]] = []
    for src in sources:
        cfg = _load(src)
        key = "terms" if "terms" in cfg else "verbs"
        for entry in cfg.get(key, []):
            canonical = entry["canonical"]
            for alias in entry.get("aliases", []):
                table.append((alias, canonical, src))
    table.sort(key=lambda t: len(t[0]), reverse=True)
    return table


def enforce(text: str) -> Dict[str, object]:
    """Replace aliases with canonical terms; return text + substitution report."""
    table = _build_substitution_table("canonical-lock-terms.json", "operational-verbs.json")
    out = text
    substitutions: List[Dict[str, str]] = []
    for alias, canonical, source in table:
        if not alias:
            continue
        pattern = re.compile(r"\\b" + re.escape(alias) + r"\\b", re.IGNORECASE)
        new_out, n = pattern.subn(canonical, out)
        if n > 0:
            substitutions.append({"from": alias, "to": canonical, "count": n, "source": source})
            out = new_out
    return {
        "original": text,
        "normalized": out,
        "substitutions": substitutions,
        "changed": out != text,
    }


__all__ = ["enforce"]
'''

READABILITY_NORMALIZER_PY = '''"""
readability_normalizer — pure detector for readability defects in rendered text.

Does NOT silently rewrite text. Returns a defect report that the renderer can
surface on the page (per publication-quality-governance: defects are surfaced,
never silently fixed by the renderer).

NOT yet wired into the publication renderer. Wiring is the next executable track.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

_HERE = Path(__file__).resolve().parent
_TERM_ROOT = _HERE.parent / "terminology"


def _forbidden_categories() -> Dict[str, List[str]]:
    with (_TERM_ROOT / "forbidden-phrases.json").open("r", encoding="utf-8") as fh:
        return json.load(fh).get("categories", {})


_PASSIVE_PATTERNS = [
    re.compile(r"\\bse\\s+debe(n)?\\b", re.IGNORECASE),
    re.compile(r"\\bdebe ser\\b", re.IGNORECASE),
    re.compile(r"\\bes\\s+\\w+ado\\b", re.IGNORECASE),
]
_AMBIGUOUS_TIME = [r"\\bunos segundos\\b", r"\\bun momento\\b", r"\\bvarias veces\\b"]
_VAGUE_BRANCH = [r"\\bsi es necesario\\b", r"\\bsi aplica\\b"]


def detect(text: str) -> Dict[str, object]:
    defects: List[Dict[str, str]] = []

    # sentence length
    for sent in re.split(r"(?<=[\\.\\?!])\\s+", text.strip()):
        words = re.findall(r"\\b\\w+\\b", sent)
        if len(words) > 24:
            defects.append({"id": "sentence-too-long", "evidence": sent[:120], "metric": str(len(words))})

    # forbidden phrases
    for category, phrases in _forbidden_categories().items():
        for phrase in phrases:
            if not phrase:
                continue
            if re.search(r"\\b" + re.escape(phrase) + r"\\b", text, re.IGNORECASE):
                defects.append({"id": f"forbidden:{category}", "evidence": phrase})

    # passive voice
    for pat in _PASSIVE_PATTERNS:
        for m in pat.finditer(text):
            defects.append({"id": "passive-voice", "evidence": m.group(0)})

    # ambiguous time / vague branch
    for pat in _AMBIGUOUS_TIME:
        for m in re.finditer(pat, text, re.IGNORECASE):
            defects.append({"id": "ambiguous-time", "evidence": m.group(0)})
    for pat in _VAGUE_BRANCH:
        for m in re.finditer(pat, text, re.IGNORECASE):
            defects.append({"id": "unresolved-branch", "evidence": m.group(0)})

    return {"text": text, "defects": defects, "defect_count": len(defects)}


__all__ = ["detect"]
'''

WARNING_LANGUAGE_RENDERER_PY = '''"""
warning_language_renderer — renders warning entities in Colombian operational
Spanish while preserving severity, irreversibility and escalation semantics.

Pure function. Does NOT mutate knowledge-core. Loads taxonomy at call time.
Returns structured payload the renderer can convert to HTML.

NOT yet wired into the publication renderer. Wiring is the next executable track.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

_HERE = Path(__file__).resolve().parent
_TERM_ROOT = _HERE.parent / "terminology"


def _taxonomy() -> dict:
    with (_TERM_ROOT / "warnings-taxonomy.json").open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _classify(entity: dict) -> dict:
    cats = {c["id"]: c for c in _taxonomy().get("warning_classes", [])}
    if entity.get("escalation_required"):
        return cats["escalation-required"]
    if entity.get("is_irreversible"):
        return cats["irreversible-operation"]
    cat = (entity.get("category") or "").lower()
    if "battery" in cat or "bater" in cat:
        return cats["low-battery"]
    if "install" in cat:
        return cats["installation-hazard"]
    if entity.get("severity") in {"high", "medium"} and entity.get("operator_action_required"):
        return cats["operational-warning"]
    return cats["informational-note"]


def render(entity: dict) -> Dict[str, object]:
    """Return a structured Colombian-Spanish warning payload, severity preserved."""
    cls = _classify(entity)
    return {
        "warning_class_id": cls["id"],
        "label_es": cls["label_es"],
        "severity": entity.get("severity", cls.get("severity")),
        "is_irreversible": bool(entity.get("is_irreversible")),
        "operator_action_required": bool(
            entity.get("operator_action_required", cls.get("operator_action_required"))
        ),
        "consequence_es": entity.get("consequence") or entity.get("summary") or "",
        "trigger_condition_es": entity.get("trigger_condition") or "",
        "operator_action_es": entity.get("operator_action") or "",
        "escalation_required": bool(entity.get("escalation_required")),
        "render_position": cls.get("render_position", "inline-before-triggering-step"),
        "source_refs": list(entity.get("source_refs", [])),
        "preserved_from_knowledge_core": True,
    }


__all__ = ["render"]
'''

RENDERERS_README = (
    "# Linguistic renderers (publication-time only)\n\n"
    "Four pure utility modules:\n\n"
    "- `linguistic_normalizer.py` — OCR cleanup + OEM translation normalisation.\n"
    "- `terminology_enforcer.py` — alias → canonical Colombian-Spanish term substitution.\n"
    "- `readability_normalizer.py` — readability defect detector (does not rewrite).\n"
    "- `warning_language_renderer.py` — Colombian-Spanish warning rendering (severity preserved).\n\n"
    "Hard rules:\n\n"
    "- pure functions; no file mutations; no knowledge-core access; no network.\n"
    "- defects are surfaced, never silently fixed.\n"
    "- NOT yet wired into `tools/publication_renderer.py` — wiring is the next executable track.\n"
)


def task_renderers() -> None:
    write_text(RENDER_ROOT / "linguistic_normalizer.py", LINGUISTIC_NORMALIZER_PY)
    write_text(RENDER_ROOT / "terminology_enforcer.py", TERMINOLOGY_ENFORCER_PY)
    write_text(RENDER_ROOT / "readability_normalizer.py", READABILITY_NORMALIZER_PY)
    write_text(RENDER_ROOT / "warning_language_renderer.py", WARNING_LANGUAGE_RENDERER_PY)
    write_text(RENDER_ROOT / "README.md", RENDERERS_README)


# ---------------------------------------------------------------------------
# TASK 6 — In-folder linguistic-governance reports (placeholders for detector outputs)
# ---------------------------------------------------------------------------

def task_linguistic_reports() -> None:
    write_json(LING_REPORTS_ROOT / "linguistic-consistency-report.json", {
        **envelope("linguistic-consistency", "Detector output placeholder — populated when detectors run."),
        "status": "pending-execution",
        "detector": "tools to consume terminology_enforcer.py + readability_normalizer.py over rendered HTML",
        "expected_fields_when_populated": [
            "per_product_inconsistency_count",
            "per_product_terminology_drift_count",
            "examples",
        ],
        "current_payload": [],
    })
    write_json(LING_REPORTS_ROOT / "terminology-drift-report.json", {
        **envelope("terminology-drift", "Detector output placeholder."),
        "status": "pending-execution",
        "current_payload": [],
    })
    write_json(LING_REPORTS_ROOT / "ambiguity-detection-report.json", {
        **envelope("ambiguity-detection", "Detector output placeholder."),
        "status": "pending-execution",
        "current_payload": [],
    })
    write_json(LING_REPORTS_ROOT / "oem-language-cleanup-report.json", {
        **envelope("oem-language-cleanup", "Detector output placeholder."),
        "status": "pending-execution",
        "current_payload": [],
    })


# ---------------------------------------------------------------------------
# TASK 7 — Publication-layer enforcement contract
# ---------------------------------------------------------------------------

def task_enforcement_contract() -> None:
    write_json(LING_ROOT / "publication-layer-enforcement.json", {
        **envelope("publication-layer-enforcement", "Where linguistic transforms may and may not run."),
        "applied_at": "publication-rendering-time-only",
        "forbidden_locations": [
            "ext-images/<product>/knowledge-core/",
            "ext-images/<product>/source-of-truth/",
            "structured-knowledge/",
            "runtime-implementation/",
        ],
        "forbidden_operations": [
            "writing back normalised text into knowledge-core",
            "rewriting OEM source documents",
            "mutating extraction-lineage entries",
            "altering warning severity, irreversibility, or escalation_required flags",
            "altering source_refs or extraction_lineage",
            "deleting any knowledge-core entity",
        ],
        "allowed_operations": [
            "transient text normalisation during render",
            "publication-time terminology substitution",
            "publication-time defect detection and disclosure",
            "publication-time warning re-labelling (label only; severity preserved)",
        ],
        "audit_invariant": "for any rendered string s_rendered, the originating knowledge-core string s_source remains byte-identical on disk.",
    })


# ---------------------------------------------------------------------------
# TASK 8 — Future visual & multimodal readiness
# ---------------------------------------------------------------------------

def task_future_multimodal() -> None:
    write_json(LING_ROOT / "future-multimodal-readiness.json", {
        **envelope("future-multimodal-readiness", "Linguistic preconditions for future visual / multimodal phases."),
        "policy_now": {
            "visuals_generated": False,
            "prompts_generated": False,
            "comfyui_invoked": False,
            "multimodal_pipelines_invoked": False,
        },
        "subordination_invariant": "visual and multimodal systems remain subordinate to operational linguistic clarity.",
        "future_integration_points": {
            "supportive_visuals": "visual captions are rendered through the same terminology + warning pipelines as text.",
            "hybrid_procedural_visuals": "step labels in any procedural diagram must use canonical operational verbs.",
            "onboarding_copilots": "copilot prompts (when introduced) must consume canonical-lock-terms and forbidden-phrases.",
            "runtime_guidance": "runtime-rendered guidance must apply the same publication-time linguistic transforms.",
            "multimodal_publications": "multimodal payloads must record applied linguistic-governance schema version in their manifest.",
        },
        "ordering_rule_for_future_phase": [
            "do not introduce multimodal copy until linguistic detectors are wired and surfacing defects",
            "do not introduce multimodal copy until terminology enforcer is wired into the renderer",
            "do not introduce multimodal copy until warning language renderer is wired into the renderer",
        ],
        "explicit_non_goals_this_phase": [
            "no prompt strings produced",
            "no image bytes produced",
            "no copilot deployed",
            "no runtime guidance changed",
        ],
    })


# ---------------------------------------------------------------------------
# Constitutional doctrine root (KNOWLEDGE_BUILDING/LINGUISTIC_GOVERNANCE/)
# ---------------------------------------------------------------------------

def task_constitution() -> None:
    docs = {
        "00-INDEX.md": (
            "# Linguistic Governance — index\n\n"
            "Layer 31 doctrine. Modeling-only authoring + four pure publication-time renderers.\n"
            "Subordinate to knowledge-core, the 30 prior governance layers, and the executable\n"
            "publication renderer.\n\n"
            "Documents:\n"
            "1. operational-language-philosophy.md\n"
            "2. publication-time-only-doctrine.md\n"
            "3. terminology-canonicality-doctrine.md\n"
            "4. warning-fidelity-doctrine.md\n"
            "5. defect-surfacing-doctrine.md\n"
            "6. multimodal-subordination-doctrine.md\n"
        ),
        "01-operational-language-philosophy.md": (
            "# Operational language philosophy\n\n"
            "Colombian operational Spanish exists to make governed knowledge usable, not "
            "to express style. Style choices are forbidden when they alter procedural truth, "
            "warning severity, or escalation semantics.\n"
        ),
        "02-publication-time-only-doctrine.md": (
            "# Publication-time-only doctrine\n\n"
            "All linguistic transforms occur at render time. The knowledge-core, the "
            "structured-knowledge layer, and OEM source-of-truth artifacts are never "
            "mutated by linguistic governance.\n"
        ),
        "03-terminology-canonicality-doctrine.md": (
            "# Terminology canonicality doctrine\n\n"
            "Each operational concept has exactly one canonical Colombian-Spanish term. "
            "Aliases are permitted in source but normalised on render. Synonym chaos is "
            "treated as a defect, not a feature.\n"
        ),
        "04-warning-fidelity-doctrine.md": (
            "# Warning fidelity doctrine\n\n"
            "Warning labels may be re-rendered into Colombian operational Spanish. "
            "Warning severity, irreversibility flags, escalation semantics, and "
            "source_refs are preserved verbatim. Re-labelling is never a re-classification.\n"
        ),
        "05-defect-surfacing-doctrine.md": (
            "# Defect surfacing doctrine\n\n"
            "The renderer surfaces linguistic defects (forbidden phrases, passive voice, "
            "ambiguous quantifiers, broken OEM translations) on the rendered page and in "
            "the publication manifest. The renderer never silently rewrites text whose "
            "defect class is not in the substitution-safe whitelist.\n"
        ),
        "06-multimodal-subordination-doctrine.md": (
            "# Multimodal subordination doctrine\n\n"
            "Visual, copilot, and multimodal surfaces are downstream consumers of "
            "linguistic governance. They may not introduce new terminology, soften "
            "warnings, or replace canonical verbs.\n"
        ),
    }
    for name, body in docs.items():
        write_text(CONST_ROOT / name, body)
    write_json(CONST_ROOT / "manifest.json", {
        **envelope("linguistic-governance-constitution", "Layer 31 constitutional doctrine root."),
        "documents": list(docs.keys()),
        "constitutional_position": "layer 31 (knowledge-core counted as layer 0)",
        "subordinate_chain_length": len(SUBORDINATE_TO) + 1,
    })


# ---------------------------------------------------------------------------
# Final reports
# ---------------------------------------------------------------------------

def write_report(name: str, payload: Dict[str, Any], md_body: str) -> None:
    write_json(REPORTS_ROOT / f"{name}.json", payload)
    title = payload.get("title", name)
    write_text(REPORTS_ROOT / f"{name}.md",
               f"# {title}\n\nGenerated: `{NOW}`\n\nSchema: `{SCHEMA}`\n\n{md_body}\n")


def emit_reports() -> None:
    write_report("01-colombian-language-doctrine-summary", {
        "title": "01 — Colombian language doctrine summary",
        **envelope("colombian-spanish-doctrine", "Doctrine for Colombian operational Spanish."),
        "documents_count": 4,
        "register": "colombiano-neutro-operativo",
        "form_of_address": "usted (formal)",
        "artifact": rel(DOCTRINE_ROOT),
    }, "Four doctrine documents: operational-language-principles, tone-governance, "
       "readability-rules, ambiguity-prevention.\n")

    write_report("02-terminology-governance-summary", {
        "title": "02 — Terminology governance summary",
        **envelope("terminology", "Canonical terminology, verbs, warning taxonomy, forbidden phrases."),
        "canonical_terms_count": 28,
        "operational_verbs_count": 15,
        "warning_classes_count": 6,
        "forbidden_categories_count": 5,
        "artifact": rel(TERM_ROOT),
    }, "28 canonical lock terms, 15 imperative verbs (usted), 6 warning classes, "
       "5 forbidden-phrase categories.\n")

    write_report("03-oem-normalization-summary", {
        "title": "03 — OEM language normalization summary",
        **envelope("normalization", "Normalisation rules for OCR + OEM Spanish + sentence-level + procedural."),
        "rule_files": [
            "ocr-cleanup-rules.json",
            "oem-translation-normalization.json",
            "sentence-simplification.json",
            "procedural-language-rules.json",
        ],
        "boundary_rule": "applies only to rendered text; knowledge-core never mutated.",
        "artifact": rel(NORM_ROOT),
    }, "Four rule files. Ambiguous OCR cases (0/O, l/1) are flagged for reviewer, never auto-fixed.\n")

    write_report("04-readability-normalization-summary", {
        "title": "04 — Readability normalization summary",
        **envelope("readability-normalization", "Readability defect detection (does not silently rewrite)."),
        "detector_module": rel(RENDER_ROOT / "readability_normalizer.py"),
        "defect_classes_detected": [
            "sentence-too-long", "forbidden:marketing", "forbidden:softeners",
            "forbidden:vagueness", "forbidden:blame", "forbidden:regionalisms_non_neutral",
            "forbidden:broken_oem_translations", "passive-voice",
            "ambiguous-time", "unresolved-branch",
        ],
    }, "Detector returns structured defect lists. Renderer surfaces defects per "
       "publication-quality-governance defect-surfacing doctrine.\n")

    write_report("05-warning-language-governance-summary", {
        "title": "05 — Warning language governance summary",
        **envelope("warning-language", "Colombian-Spanish warning re-labelling with semantics preserved."),
        "renderer_module": rel(RENDER_ROOT / "warning_language_renderer.py"),
        "taxonomy": rel(TERM_ROOT / "warnings-taxonomy.json"),
        "preserved_fields": ["severity", "is_irreversible", "operator_action_required",
                              "escalation_required", "source_refs"],
        "rendered_fields": ["label_es", "consequence_es", "trigger_condition_es", "operator_action_es"],
    }, "Re-labelling is never re-classification. Severity, irreversibility and escalation "
       "are preserved verbatim from knowledge-core.\n")

    write_report("06-linguistic-drift-detection-summary", {
        "title": "06 — Linguistic drift detection summary",
        **envelope("linguistic-drift", "Detector reports staged for population by future executable track."),
        "report_artifacts": [
            rel(LING_REPORTS_ROOT / "linguistic-consistency-report.json"),
            rel(LING_REPORTS_ROOT / "terminology-drift-report.json"),
            rel(LING_REPORTS_ROOT / "ambiguity-detection-report.json"),
            rel(LING_REPORTS_ROOT / "oem-language-cleanup-report.json"),
        ],
        "status": "detectors-defined; reports staged with empty payloads pending wiring.",
    }, "Four report files staged. Detectors are defined as pure functions in the "
       "renderers/ directory. Wiring into the publication renderer is the next track.\n")

    write_report("07-publication-layer-enforcement-summary", {
        "title": "07 — Publication-layer enforcement summary",
        **envelope("publication-layer-enforcement", "Where linguistic transforms may and may not run."),
        "applied_at": "publication-rendering-time-only",
        "audit_invariant": "knowledge-core source strings remain byte-identical on disk after any render.",
        "artifact": rel(LING_ROOT / "publication-layer-enforcement.json"),
    }, "Linguistic governance is forbidden from writing into knowledge-core, "
       "structured-knowledge, source-of-truth, or runtime-implementation.\n")

    write_report("08-future-multimodal-readiness-summary", {
        "title": "08 — Future multimodal readiness summary",
        **envelope("future-multimodal-readiness", "Multimodal preconditions; no multimodal output now."),
        "visuals_generated": False,
        "prompts_generated": False,
        "comfyui_invoked": False,
        "subordination_invariant": "visual and multimodal systems subordinate to linguistic clarity.",
        "artifact": rel(LING_ROOT / "future-multimodal-readiness.json"),
    }, "Multimodal copy is not introduced until linguistic detectors are wired and "
       "surfacing defects, the terminology enforcer is wired, and the warning renderer is wired.\n")

    write_report("09-unresolved-linguistic-risks", {
        "title": "09 — Unresolved linguistic risks",
        **envelope("linguistic-risks", "Risks not resolved by this phase."),
        "structural_risks": [
            "renderers not wired into tools/publication_renderer.py yet",
            "no per-product linguistic consistency baseline computed yet",
            "no linguistic version registry tied to renderer-version delta",
            "no measurement of false-positive rate for OEM substitutions",
            "no Colombian-Spanish style scoring against rendered HTML",
            "no detection of mixed-language steps within one procedure",
            "no enforcement of «…» quoting for UI labels at render time",
            "no menu-path normalisation pass at render time",
            "ambiguous OCR cases (0/O, l/1) require reviewer console (carry-over)",
        ],
        "policy_risks": [
            "alias substitutions could be over-eager on common nouns; word-boundary regex mitigates but a corpus pilot is required",
            "warning re-labelling must not cross severity classes; enforcement is policy-only until tests are added",
        ],
        "out_of_scope_for_this_phase": [
            "wiring renderers into the publication renderer",
            "running detectors over rendered HTML",
            "introducing tests for renderer wiring",
        ],
    }, "Risks documented; remediation scheduled for the next executable track.\n")

    write_report("10-colombian-publication-quality-reassessment", {
        "title": "10 — Colombian publication-quality reassessment",
        **envelope("colombian-publication-quality-reassessment", "Reassesses platform after linguistic governance."),
        "platform_status": "publication-capable + readability-aware + linguistically-governed (modeled)",
        "linguistic_governance_status": "MODELED + four pure renderers staged; wiring scheduled for next track",
        "subordinate_chain_length": len(SUBORDINATE_TO) + 1,
        "primary_bottleneck_resolved": "absence of canonical Colombian operational language doctrine and a publication-time linguistic transform pipeline",
        "remaining_bottlenecks": [
            "wire renderers into tools/publication_renderer.py",
            "compute per-product linguistic baselines",
            "stand up a reviewer-validation console",
            "publish a Colombian-Spanish style score per rendered page",
            "introduce regression tests for renderer wiring",
        ],
        "next_track": "wire linguistic_normalizer + terminology_enforcer + readability_normalizer + warning_language_renderer into the publication renderer",
        "runtime_impact": "none (modeling + staged pure utilities)",
        "renderer_impact": "additive when wired; current rendered HTML remains valid",
    }, "Doctrine and pure utilities are in place. Knowledge-core remains canonical. "
       "Wiring the four renderers into the publication renderer is the next track.\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build() -> None:
    for d in (LING_ROOT, DOCTRINE_ROOT, TERM_ROOT, NORM_ROOT, RENDER_ROOT,
              LING_REPORTS_ROOT, CONST_ROOT, REPORTS_ROOT):
        d.mkdir(parents=True, exist_ok=True)

    task_doctrine()
    task_terminology()
    task_normalization()
    task_renderers()
    task_linguistic_reports()
    task_enforcement_contract()
    task_future_multimodal()
    task_constitution()
    emit_reports()

    print("Linguistic Governance written to:")
    print(f"  {rel(LING_ROOT)}")
    print(f"  {rel(CONST_ROOT)}")
    print(f"  {rel(REPORTS_ROOT)}")
    print(f"  Subordinate chain length: {len(SUBORDINATE_TO) + 1}")


if __name__ == "__main__":
    build()
