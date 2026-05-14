"""
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
        pattern = re.compile(r"\b" + re.escape(alias) + r"\b", re.IGNORECASE)
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
