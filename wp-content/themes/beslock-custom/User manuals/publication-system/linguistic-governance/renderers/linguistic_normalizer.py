"""
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
    out = re.sub(r"[ \t]{2,}", " ", out).strip()
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
