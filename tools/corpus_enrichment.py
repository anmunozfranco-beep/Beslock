"""
Phase 27 (part 1) — Operational corpus enrichment (additive, non-destructive).

For each declared product, writes CANDIDATE supplemental records into new
sibling folders under `<product>/knowledge-core/`:

  troubleshooting-expanded/   — 7 symptom categories per product
  warnings-expanded/          — 7 warning categories per product
  continuity-checkpoints/     — 6 checkpoint kinds per product
  causal-graphs/              — symptom→cause edges + hypothesis chains
  confidence-tiers/           — per-product confidence tier manifest

All records carry:
  schema_version: knowledge-core/1.0
  validation_status: "candidate-pending-review"
  confidence: "candidate"   (NOT "verified", NOT "medium")
  source_refs: this builder + the operational categories doctrine

The runtime is configured to down-weight `candidate` confidence and to surface
candidate-only retrievals via escalation. No existing per-product file is
mutated. Every write is idempotent.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THEME_ROOT = REPO_ROOT / "wp-content" / "themes" / "beslock-custom" / "User manuals"
EXT_IMAGES = THEME_ROOT / "ext-images"

PRODUCTS = ["e-flex", "e-nova", "e-orbit", "e-prime", "e-shield", "e-touch"]

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SOURCE_REF = "tools/corpus_enrichment.py"


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

TS_CATEGORIES = [
    {"slug": "pairing-failures",            "summary_es": "fallo al vincular la cerradura con la app o el módulo OEM",
     "symptoms_es": ["la app no detecta la cerradura", "la vinculación se interrumpe a mitad de proceso",
                     "la cerradura aparece como ya vinculada en otro dispositivo"]},
    {"slug": "enrollment-failures",         "summary_es": "fallo al registrar huella, pin, llave o credencial",
     "symptoms_es": ["el lector de huella no responde", "la huella se rechaza repetidamente",
                     "la cerradura cierra el alta sin guardar el credencial"]},
    {"slug": "battery-issues",              "summary_es": "comportamiento anómalo asociado a baja batería o alimentación inestable",
     "symptoms_es": ["la cerradura se reinicia sola", "la cerradura no abre a pesar de credencial válido",
                     "indicador de batería en estado crítico antes de lo esperado"]},
    {"slug": "connectivity-failures",       "summary_es": "fallo de conectividad bluetooth/wifi o gateway opcional",
     "symptoms_es": ["la app pierde la conexión durante la operación",
                     "la cerradura no aparece en el escaneo bluetooth",
                     "el gateway opcional no reporta estado"]},
    {"slug": "lock-state-inconsistencies",  "summary_es": "el estado físico no coincide con el estado reportado por la app",
     "symptoms_es": ["la app dice abierto y la cerradura está cerrada (o viceversa)",
                     "tras corte de energía el estado reportado no se refresca",
                     "la cerradura indica error de sensor de estado"]},
    {"slug": "administrator-access-recovery","summary_es": "el administrador perdió acceso o no puede recuperar control de la cerradura",
     "symptoms_es": ["el administrador olvidó su credencial maestro",
                     "la cuenta administradora ya no figura en la app",
                     "no se puede iniciar el flujo de recuperación de administrador"]},
    {"slug": "app-synchronization-issues",  "summary_es": "la app no refleja cambios realizados en la cerradura o viceversa",
     "symptoms_es": ["las credenciales nuevas no aparecen en la app",
                     "los logs de la cerradura no se sincronizan",
                     "los cambios de configuración no se aplican"]},
]

WARN_CATEGORIES = [
    {"slug": "operational",            "summary_es": "advertencias operacionales generales antes de ejecutar procedimientos críticos"},
    {"slug": "irreversible-operation", "summary_es": "advertencia: esta operación no se puede deshacer sin reinstalación o reset de fábrica"},
    {"slug": "unsafe-state",           "summary_es": "advertencia: la cerradura está en un estado donde no es seguro continuar"},
    {"slug": "installation",           "summary_es": "advertencias relativas a la instalación física y eléctrica"},
    {"slug": "low-battery",            "summary_es": "advertencias activadas por niveles críticos de batería"},
    {"slug": "recovery",               "summary_es": "advertencias específicas a flujos de recuperación operacional"},
    {"slug": "escalation-required",    "summary_es": "advertencia: este escenario requiere escalamiento al canal OEM o soporte autorizado"},
]

CHECKPOINT_KINDS = [
    {"slug": "onboarding",          "summary_es": "punto de control de continuidad durante el alta inicial"},
    {"slug": "pairing",             "summary_es": "punto de control de continuidad durante la vinculación"},
    {"slug": "enrollment",          "summary_es": "punto de control de continuidad durante el registro de credenciales"},
    {"slug": "troubleshooting",     "summary_es": "punto de control de continuidad durante un flujo de diagnóstico"},
    {"slug": "battery-replacement", "summary_es": "punto de control de continuidad durante el reemplazo de baterías"},
    {"slug": "recovery",            "summary_es": "punto de control de continuidad durante un flujo de recuperación"},
]

CONFIDENCE_TIERS = [
    {"id": "verified-oem",         "rank": 5, "description": "verificado contra documentación OEM oficial"},
    {"id": "verified-internal",    "rank": 4, "description": "verificado por revisión interna sobre fuente OEM"},
    {"id": "ocr-derived",          "rank": 3, "description": "extraído por OCR a partir de manual original; pendiente de revisión"},
    {"id": "inferred-operational", "rank": 2, "description": "guía operacional inferida; requiere validación humana"},
    {"id": "candidate",            "rank": 1, "description": "candidato pendiente de revisión; no apto para producción"},
    {"id": "unresolved",           "rank": 0, "description": "ambigüedad no resuelta; el runtime debe escalar"},
]


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def _write_json(path: Path, payload: dict) -> bool:
    payload = dict(payload)
    payload.setdefault("schema_version", "knowledge-core/1.0")
    payload.setdefault("updated_at", NOW)
    body = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == body:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return True


def _candidate_meta(node_id: str, product: str, kind: str, channels: list[str]) -> dict:
    return {
        "id": node_id,
        "type": kind,
        "product": product,
        "language": "es-CO",
        "validation_status": "candidate-pending-review",
        "confidence": "candidate",
        "ocr_dependency": "none",
        "channel_targets": channels,
        "source_refs": [SOURCE_REF, "doctrine: corpus-enrichment categories"],
        "extraction_lineage": [f"corpus-enrichment/{kind}/{node_id}"],
        "surface": "runtime-corpus",
        "menu_path": "",
    }


def write_troubleshooting(product: str) -> int:
    base = EXT_IMAGES / product / "knowledge-core" / "troubleshooting-expanded"
    written = 0
    for cat in TS_CATEGORIES:
        node_id = f"ts-{cat['slug']}-candidate"
        payload = {
            **_candidate_meta(node_id, product, "troubleshooting-candidate",
                              ["support", "rag", "api"]),
            "summary": cat["summary_es"],
            "category": cat["slug"],
            "symptoms": cat["symptoms_es"],
            "diagnostic_questions": [
                "¿se puede reproducir el síntoma de forma consistente?",
                "¿en qué momento del flujo aparece (alta, vinculación, uso normal, recuperación)?",
                "¿hay eventos recientes (cambio de batería, reset, actualización)?",
            ],
            "candidate_causes": [
                "candidato pendiente de revisión OEM",
            ],
            "next_actions": [
                "elevar el caso al canal de revisión OEM antes de operar",
                "registrar el síntoma observado en el log operacional",
            ],
            "escalation_required": True,
        }
        if _write_json(base / f"{node_id}.json", payload):
            written += 1
    return written


def write_warnings(product: str) -> int:
    base = EXT_IMAGES / product / "knowledge-core" / "warnings-expanded"
    written = 0
    for cat in WARN_CATEGORIES:
        node_id = f"warn-{cat['slug']}-candidate"
        payload = {
            **_candidate_meta(node_id, product, "warning-candidate",
                              ["web", "support", "rag", "api"]),
            "summary": cat["summary_es"],
            "category": cat["slug"],
            "severity": "high" if cat["slug"] in {"irreversible-operation", "unsafe-state",
                                                  "escalation-required"} else "medium",
            "is_irreversible": cat["slug"] == "irreversible-operation",
            "is_safety_blocking": cat["slug"] in {"unsafe-state", "irreversible-operation",
                                                  "escalation-required"},
            "operator_action_required": True,
            "candidate_text_es": cat["summary_es"],
            "must_be_attached_to_kinds": ["onboarding", "pairing",
                                          "fingerprint-enrollment",
                                          "battery-recovery",
                                          "operational-procedures"],
        }
        if _write_json(base / f"{node_id}.json", payload):
            written += 1
    return written


def write_checkpoints(product: str) -> int:
    base = EXT_IMAGES / product / "knowledge-core" / "continuity-checkpoints"
    written = 0
    for ck in CHECKPOINT_KINDS:
        node_id = f"ckpt-{ck['slug']}-candidate"
        payload = {
            **_candidate_meta(node_id, product, "continuity-checkpoint-candidate",
                              ["rag", "api"]),
            "summary": ck["summary_es"],
            "flow": ck["slug"],
            "is_safe_interrupt_point": True,
            "is_safe_resume_point": True,
            "required_state_keys": ["timeline_id", "context_vector", "last_step_id",
                                    "operator_id", "incident_id"],
            "non_inheritable_signals": ["operator_one_time_token", "ephemeral_session_secret"],
            "resume_preconditions": [
                "operador autenticado",
                "no hay advertencias bloqueantes pendientes",
                "el estado físico de la cerradura coincide con el último checkpoint",
            ],
        }
        if _write_json(base / f"{node_id}.json", payload):
            written += 1
    return written


def write_causal(product: str) -> int:
    base = EXT_IMAGES / product / "knowledge-core" / "causal-graphs"
    written = 0
    edges = []
    for cat in TS_CATEGORIES:
        edges.append({
            "from_symptom": f"sym-{cat['slug']}",
            "to_cause": f"cause-{cat['slug']}-pending-review",
            "evidence": "candidate-pending-review",
            "confidence": "candidate",
        })
    payload = {
        **_candidate_meta(f"causal-graph-{product}-candidate", product,
                          "causal-graph-candidate", ["rag", "api"]),
        "summary": "grafo candidato de relaciones síntoma→causa para el runtime de troubleshooting",
        "edges": edges,
        "hypothesis_chains": [
            {
                "id": f"hyp-{cat['slug']}-candidate",
                "symptom": f"sym-{cat['slug']}",
                "ordered_hypotheses": [
                    {"id": "h1", "label": "verificar prerequisitos del flujo",         "status": "pending"},
                    {"id": "h2", "label": "verificar estado físico de la cerradura",   "status": "pending"},
                    {"id": "h3", "label": "verificar canal OEM / app sincronizada",    "status": "pending"},
                ],
                "termination_outcomes": ["resolved", "escalated", "halted"],
            }
            for cat in TS_CATEGORIES
        ],
    }
    if _write_json(base / f"causal-graph-{product}-candidate.json", payload):
        written += 1
    return written


def write_confidence(product: str) -> int:
    base = EXT_IMAGES / product / "knowledge-core" / "confidence-tiers"
    payload = {
        **_candidate_meta(f"confidence-tier-manifest-{product}", product,
                          "confidence-tier-manifest", ["rag", "api"]),
        "summary": "manifiesto de tiers de confianza usado por el runtime para ranking y disclosure",
        "tiers": CONFIDENCE_TIERS,
        "default_tier_per_kind": {
            "operational-procedures":   "ocr-derived",
            "warnings":                 "ocr-derived",
            "troubleshooting":          "candidate",
            "onboarding":               "ocr-derived",
            "escalation":               "inferred-operational",
            "adaptive-guidance":        "inferred-operational",
            "fingerprint-enrollment":   "ocr-derived",
            "pairing":                  "ocr-derived",
            "battery-recovery":         "candidate",
        },
        "runtime_ranking_weight": {
            "verified-oem":         1.0,
            "verified-internal":    0.95,
            "ocr-derived":          0.85,
            "inferred-operational": 0.65,
            "candidate":            0.40,
            "unresolved":           0.10,
        },
    }
    return 1 if _write_json(base / f"confidence-tier-manifest-{product}.json", payload) else 0


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    counts = {p: {"troubleshooting": 0, "warnings": 0, "checkpoints": 0,
                  "causal": 0, "confidence": 0} for p in PRODUCTS}
    for product in PRODUCTS:
        counts[product]["troubleshooting"] = write_troubleshooting(product)
        counts[product]["warnings"]        = write_warnings(product)
        counts[product]["checkpoints"]     = write_checkpoints(product)
        counts[product]["causal"]          = write_causal(product)
        counts[product]["confidence"]      = write_confidence(product)

    totals = {k: sum(counts[p][k] for p in PRODUCTS) for k in
              ("troubleshooting", "warnings", "checkpoints", "causal", "confidence")}
    print("Operational corpus enrichment complete (additive, non-destructive).")
    for p in PRODUCTS:
        print(f"  {p}: {counts[p]}")
    print(f"  totals: {totals}")
    print(f"  grand total candidate records written this run: {sum(totals.values())}")


if __name__ == "__main__":
    build()
