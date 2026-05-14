"""
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
    re.compile(r"\bse\s+debe(n)?\b", re.IGNORECASE),
    re.compile(r"\bdebe ser\b", re.IGNORECASE),
    re.compile(r"\bes\s+\w+ado\b", re.IGNORECASE),
]
_AMBIGUOUS_TIME = [r"\bunos segundos\b", r"\bun momento\b", r"\bvarias veces\b"]
_VAGUE_BRANCH = [r"\bsi es necesario\b", r"\bsi aplica\b"]


def detect(text: str) -> Dict[str, object]:
    defects: List[Dict[str, str]] = []

    # sentence length
    for sent in re.split(r"(?<=[\.\?!])\s+", text.strip()):
        words = re.findall(r"\b\w+\b", sent)
        if len(words) > 24:
            defects.append({"id": "sentence-too-long", "evidence": sent[:120], "metric": str(len(words))})

    # forbidden phrases
    for category, phrases in _forbidden_categories().items():
        for phrase in phrases:
            if not phrase:
                continue
            if re.search(r"\b" + re.escape(phrase) + r"\b", text, re.IGNORECASE):
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
