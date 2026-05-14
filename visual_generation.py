#!/usr/bin/env python3
"""Visual generation automation scaffold for the Beslock visual system."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import mimetypes
import os
import re
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib import error, parse, request

try:
    from PIL import Image, ImageFilter, ImageStat
except ImportError:  # pragma: no cover - handled at runtime when scoring is used.
    Image = None
    ImageFilter = None
    ImageStat = None


REPO_ROOT = Path(__file__).resolve().parent
THEME_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom"
VISUAL_SYSTEM_ROOT = THEME_ROOT / "User manuals/visual-system"
REGISTRY_PATH = VISUAL_SYSTEM_ROOT / "production-control/global-image-registry.md"
DEFAULT_MANIFESTS_DIR = REPO_ROOT / "output/visual-generation/manifests"
DEFAULT_RUNS_DIR = REPO_ROOT / "output/visual-generation/runs"
DEFAULT_REFERENCE_PREP_DIR = REPO_ROOT / "output/visual-generation/reference-prep"
DEFAULT_COMPOSITES_DIR = REPO_ROOT / "output/visual-generation/composites"
DEFAULT_MANUAL_GRAPHICS_DIR = REPO_ROOT / "output/visual-generation/manual-graphics"
LOCAL_ENV_PATH = REPO_ROOT / ".env.local"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
FORMAT_DIMENSIONS: Dict[str, Tuple[int, int]] = {
    "16:9 horizontal": (1536, 864),
    "4:3 horizontal": (1408, 1056),
    "4:5 vertical": (1024, 1280),
    "1:1 square": (1024, 1024),
}
VISUAL_MODE_BY_CLASS: Dict[str, str] = {
    "realistic": "documentary-realistic",
    "semi-realistic": "instructional-simplified",
    "schematic": "schematic-outline",
    "hybrid": "hybrid-product-shell",
}
TOKEN_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "into",
    "only",
    "para",
    "con",
    "sin",
    "del",
    "las",
    "los",
    "una",
    "uno",
    "por",
    "que",
    "como",
    "sobre",
    "desde",
    "usar",
    "show",
    "step",
    "manual",
    "lock",
    "image",
}


@dataclass(frozen=True)
class ProductPaths:
    slug: str
    product_name: str
    reference_image: Path
    visual_profile: Path
    status_tracker: Path
    validation_checklist: Path
    product_root: Path
    prompt_pack: Path
    generation_matrix: Path
    selected_assets_register: Path
    manual_json: Path


class CloudApiError(RuntimeError):
    """Raised when the Comfy Cloud API returns an error response."""


def load_local_env(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or key in os.environ:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        os.environ[key] = value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export visual-generation manifests and run external generation workflows."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser(
        "export",
        help="Export machine-readable manifests from the visual-system markdown files.",
    )
    export_parser.add_argument(
        "--product",
        action="append",
        dest="products",
        help="Product slug to export. Repeat to export multiple products. Defaults to all canonical products.",
    )
    export_parser.add_argument(
        "--output",
        default=str(DEFAULT_MANIFESTS_DIR),
        help="Directory where manifest JSON files will be written.",
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Render workflow variants from a manifest and optionally submit them to Comfy Cloud.",
    )
    run_parser.add_argument("--manifest", required=True, help="Path to an exported manifest JSON file.")
    run_parser.add_argument(
        "--workflow",
        required=True,
        help="Workflow JSON exported from ComfyUI in API format.",
    )
    run_parser.add_argument(
        "--output",
        default=str(DEFAULT_RUNS_DIR),
        help="Base directory for rendered workflows, job metadata, and downloaded outputs.",
    )
    run_parser.add_argument(
        "--job",
        action="append",
        dest="jobs",
        help="Job filename or asset ID to run. Repeat to filter to multiple jobs.",
    )
    run_parser.add_argument(
        "--variant-count",
        type=int,
        default=3,
        help="Number of variants to render per selected manifest job.",
    )
    run_parser.add_argument("--positive-node", required=True, help="Node ID that receives the positive prompt.")
    run_parser.add_argument("--positive-field", default="text", help="Input field for the positive prompt node.")
    run_parser.add_argument("--negative-node", help="Node ID that receives the negative prompt.")
    run_parser.add_argument("--negative-field", default="text", help="Input field for the negative prompt node.")
    run_parser.add_argument("--seed-node", help="Node ID that receives the variant seed.")
    run_parser.add_argument("--seed-field", default="seed", help="Input field for the seed node.")
    run_parser.add_argument(
        "--reference-image-node",
        help="LoadImage-style node ID that should receive the uploaded product reference image filename.",
    )
    run_parser.add_argument(
        "--reference-image-field",
        default="image",
        help="Input field for the reference image node.",
    )
    run_parser.add_argument(
        "--width-node",
        help="Node ID that receives width derived from the manifest format field.",
    )
    run_parser.add_argument("--width-field", default="width", help="Input field for the width node.")
    run_parser.add_argument(
        "--height-node",
        help="Node ID that receives height derived from the manifest format field.",
    )
    run_parser.add_argument("--height-field", default="height", help="Input field for the height node.")
    run_parser.add_argument(
        "--filename-prefix-node",
        help="SaveImage or SaveWebP node ID whose filename prefix should be stamped per candidate.",
    )
    run_parser.add_argument(
        "--filename-prefix-field",
        default="filename_prefix",
        help="Input field for the filename prefix node.",
    )
    run_parser.add_argument(
        "--size-node",
        help="Node ID that receives a preset size string such as 1024x1024 or 1536x1024.",
    )
    run_parser.add_argument(
        "--size-field",
        default="size",
        help="Input field for the preset size node.",
    )
    run_parser.add_argument(
        "--size-mode",
        choices=("manifest", "openai-gpt-image"),
        default="manifest",
        help="How to derive the preset size string when --size-node is provided.",
    )
    run_parser.add_argument(
        "--base-url",
        default="https://cloud.comfy.org",
        help="Comfy Cloud base URL.",
    )
    run_parser.add_argument(
        "--api-key-env",
        default="COMFY_CLOUD_API_KEY",
        help="Environment variable containing the Comfy Cloud API key.",
    )
    run_parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Polling timeout in seconds when --wait is enabled.",
    )
    run_parser.add_argument(
        "--poll-interval",
        type=float,
        default=2.0,
        help="Polling interval in seconds when --wait is enabled.",
    )
    run_parser.add_argument(
        "--wait",
        action="store_true",
        help="Wait for each submitted job to complete and download outputs.",
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render workflow variants and metadata without calling the Comfy Cloud API.",
    )

    score_parser = subparsers.add_parser(
        "score",
        help="Run basic local scoring on downloaded candidate outputs.",
    )
    score_parser.add_argument("--manifest", required=True, help="Path to an exported manifest JSON file.")
    score_parser.add_argument(
        "--run-dir",
        help="Specific run directory to score. Defaults to the latest run for the manifest product.",
    )
    score_parser.add_argument(
        "--output",
        help="Optional explicit path for the score summary JSON. Defaults to <run-dir>/score-summary.json.",
    )

    writeback_parser = subparsers.add_parser(
        "writeback",
        help="Write selected or generated states back into the canonical markdown trackers.",
    )
    writeback_parser.add_argument(
        "--manifest",
        required=True,
        help="Path to an exported manifest JSON file.",
    )
    writeback_parser.add_argument(
        "--run-dir",
        help="Specific run directory to sync back. Defaults to the latest run for the manifest product.",
    )
    writeback_parser.add_argument(
        "--score-summary",
        help="Optional explicit path to a score-summary.json file. Defaults to <run-dir>/score-summary.json.",
    )
    writeback_parser.add_argument(
        "--job",
        action="append",
        dest="jobs",
        help="Job filename or asset ID to sync. Repeat to filter to multiple jobs.",
    )
    writeback_parser.add_argument(
        "--state",
        choices=("generated", "selected"),
        default="selected",
        help="Tracker state to write back. `selected` uses score-summary winners, `generated` uses run-summary coverage.",
    )
    writeback_parser.add_argument(
        "--validation-status",
        default="pending",
        help="Validation status to write into selected-assets-register rows when that column exists.",
    )
    writeback_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview tracker updates without modifying markdown files.",
    )

    prep_parser = subparsers.add_parser(
        "prepare-reference",
        help="Create a controlled reference pack with a transparent cutout, mask, and centered guide image.",
    )
    prep_parser.add_argument("--input", required=True, help="Path to the source product reference image.")
    prep_parser.add_argument(
        "--output-dir",
        help="Directory where the prepared reference pack will be written. Defaults under output/visual-generation/reference-prep/.",
    )
    prep_parser.add_argument(
        "--crop-box",
        help="Optional crop box as left,top,right,bottom before extracting the subject.",
    )
    prep_parser.add_argument(
        "--white-threshold",
        type=int,
        default=245,
        help="Pixels at or above this brightness are treated as removable white background.",
    )
    prep_parser.add_argument(
        "--rolloff",
        type=int,
        default=18,
        help="Brightness rolloff below the white threshold used to feather the extracted alpha.",
    )
    prep_parser.add_argument(
        "--blur-radius",
        type=float,
        default=1.5,
        help="Gaussian blur radius for softening the extracted alpha mask.",
    )
    prep_parser.add_argument(
        "--tight-padding",
        type=int,
        default=20,
        help="Padding in pixels around the detected subject in the transparent cutout.",
    )
    prep_parser.add_argument(
        "--canvas-size",
        default="1024x1024",
        help="Centered controlled-reference canvas size as WIDTHxHEIGHT.",
    )
    prep_parser.add_argument(
        "--canvas-padding",
        type=int,
        default=48,
        help="Minimum padding kept between the subject and the centered canvas edge.",
    )

    composite_parser = subparsers.add_parser(
        "composite",
        help="Composite an exact product cutout over a generated background for hybrid product-truth renders.",
    )
    composite_parser.add_argument("--background", required=True, help="Path to the generated background image.")
    composite_parser.add_argument("--foreground", required=True, help="Path to the prepared foreground cutout image.")
    composite_parser.add_argument(
        "--mask",
        help="Optional explicit grayscale mask path. Defaults to the alpha channel from --foreground.",
    )
    composite_parser.add_argument("--output", required=True, help="Path where the composite image will be written.")
    composite_parser.add_argument(
        "--fit-height-ratio",
        type=float,
        default=0.82,
        help="Foreground target height as a fraction of the background height.",
    )
    composite_parser.add_argument(
        "--anchor",
        choices=("center", "bottom-center"),
        default="bottom-center",
        help="Foreground anchor placement inside the background frame.",
    )
    composite_parser.add_argument(
        "--x-offset",
        type=int,
        default=0,
        help="Horizontal pixel offset applied after anchor placement.",
    )
    composite_parser.add_argument(
        "--y-offset",
        type=int,
        default=0,
        help="Vertical pixel offset applied after anchor placement.",
    )
    composite_parser.add_argument(
        "--shadow-opacity",
        type=int,
        default=72,
        help="Drop-shadow opacity from 0 to 255.",
    )
    composite_parser.add_argument(
        "--shadow-blur",
        type=float,
        default=18.0,
        help="Gaussian blur radius used for the drop shadow.",
    )
    composite_parser.add_argument(
        "--shadow-offset-x",
        type=int,
        default=0,
        help="Horizontal drop-shadow offset in pixels.",
    )
    composite_parser.add_argument(
        "--shadow-offset-y",
        type=int,
        default=22,
        help="Vertical drop-shadow offset in pixels.",
    )

    manual_graphics_parser = subparsers.add_parser(
        "manual-graphics-brief",
        help="Emit a strict manual-graphics brief from manifest jobs and optional run artifacts.",
    )
    manual_graphics_parser.add_argument(
        "--manifest",
        required=True,
        help="Path to an exported manifest JSON file.",
    )
    manual_graphics_parser.add_argument(
        "--job",
        action="append",
        dest="jobs",
        help="Job filename or asset ID to package into a manual-graphics brief. Repeat to select multiple jobs.",
    )
    manual_graphics_parser.add_argument(
        "--run-dir",
        help="Optional run directory whose candidate outputs should be referenced in the brief.",
    )
    manual_graphics_parser.add_argument(
        "--output-dir",
        help="Directory where the brief JSON and Markdown files will be written.",
    )

    return parser


def normalize_slug(product_name: str) -> str:
    return product_name.strip().lower().replace(" ", "-")


def strip_code(value: str) -> str:
    cleaned = value.strip()
    if cleaned.startswith("`") and cleaned.endswith("`"):
        return cleaned[1:-1]
    return cleaned


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def split_markdown_row(row: str) -> List[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def find_markdown_table(
    lines: List[str], required_headers: Iterable[str]
) -> Tuple[int, int, List[str], List[Dict[str, str]]]:
    required = set(required_headers)
    index = 0

    while index < len(lines):
        if not lines[index].strip().startswith("|"):
            index += 1
            continue

        start = index
        block: List[str] = []
        while index < len(lines) and lines[index].strip().startswith("|"):
            block.append(lines[index])
            index += 1

        if len(block) < 2:
            continue

        headers = split_markdown_row(block[0])
        if not required.issubset(headers):
            continue

        rows: List[Dict[str, str]] = []
        for row_line in block[2:]:
            cells = split_markdown_row(row_line)
            if len(cells) != len(headers):
                continue
            rows.append({header: strip_code(cell) for header, cell in zip(headers, cells)})

        return start, index, headers, rows

    raise SystemExit(f"Could not find markdown table with headers: {', '.join(required_headers)}")


def format_markdown_cell(header: str, value: Any) -> str:
    text = str(value).strip() if value is not None else ""
    if not text:
        return ""
    if header in {"Filename", "Stable filename", "Publish target"}:
        return text if text.startswith("`") and text.endswith("`") else f"`{text}`"
    return text


def render_markdown_table(headers: List[str], rows: List[Dict[str, str]]) -> List[str]:
    rendered = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for row in rows:
        cells = [format_markdown_cell(header, row.get(header, "")) for header in headers]
        rendered.append("| " + " | ".join(cells) + " |")
    return rendered


def sort_rows_by_slot(rows: List[Dict[str, str]]) -> None:
    def slot_key(row: Dict[str, str]) -> Tuple[int, Any]:
        slot_value = row.get("Slot", "")
        try:
            return (0, int(slot_value))
        except (TypeError, ValueError):
            return (1, slot_value)

    if any("Slot" in row for row in rows):
        rows.sort(key=slot_key)


def parse_markdown_table(table_text: str) -> List[Dict[str, str]]:
    rows = [line for line in table_text.splitlines() if line.strip().startswith("|")]
    if len(rows) < 2:
        return []

    headers = split_markdown_row(rows[0])
    parsed_rows: List[Dict[str, str]] = []
    for row in rows[2:]:
        cells = split_markdown_row(row)
        if len(cells) != len(headers):
            continue
        parsed_rows.append({header: cell for header, cell in zip(headers, cells)})
    return parsed_rows


def collect_section(lines: List[str], header: str) -> str:
    for index, line in enumerate(lines):
        if line.strip() != header:
            continue

        collected: List[str] = []
        for candidate in lines[index + 1 :]:
            if candidate.startswith("## "):
                break
            if candidate.strip():
                collected.append(candidate.strip())
        return " ".join(collected).strip()
    return ""


def normalize_prompt_key(key: str) -> str:
    normalized = key.strip().lower().replace(" ", "_")
    return normalized.replace("-", "_")


def flush_multiline_prompt_field(
    entry: Dict[str, Any], current_key: Optional[str], buffer: List[str]
) -> None:
    if not current_key:
        return
    entry[current_key] = "\n".join(line.rstrip() for line in buffer).strip()


def parse_prompt_pack(path: Path) -> Dict[str, Any]:
    lines = read_text(path).splitlines()
    shared_negative_base = collect_section(lines, "## Shared negative base")
    product_negative_additions = collect_section(lines, "## Product-specific negative additions")
    prompts: List[Dict[str, Any]] = []

    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.startswith("### "):
            index += 1
            continue

        raw_title = line[4:].strip()
        order_text, _, prompt_name = raw_title.partition(". ")
        prompt_entry: Dict[str, Any] = {
            "order": int(order_text) if order_text.isdigit() else raw_title,
            "filename": prompt_name or raw_title,
        }
        index += 1
        current_key: Optional[str] = None
        buffer: List[str] = []

        while index < len(lines) and not lines[index].startswith("### "):
            current_line = lines[index]
            stripped = current_line.strip()
            if stripped.startswith("- "):
                flush_multiline_prompt_field(prompt_entry, current_key, buffer)
                current_key = None
                buffer = []

                content = stripped[2:]
                if content.endswith(":"):
                    current_key = normalize_prompt_key(content[:-1])
                elif ": " in content:
                    key, value = content.split(": ", 1)
                    prompt_entry[normalize_prompt_key(key)] = value.strip()
            elif current_key and stripped:
                buffer.append(stripped)

            index += 1

        flush_multiline_prompt_field(prompt_entry, current_key, buffer)
        prompt_entry["shared_negative_base"] = shared_negative_base
        prompt_entry["product_negative_additions"] = product_negative_additions
        prompts.append(prompt_entry)

    return {
        "shared_negative_base": shared_negative_base,
        "product_negative_additions": product_negative_additions,
        "prompts": prompts,
    }


def split_prompt_field_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw_items = value
    else:
        raw_items = re.split(r"[\n;,|]+", str(value))

    cleaned: List[str] = []
    seen = set()
    for item in raw_items:
        text = str(item).strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(text)
    return cleaned


def prompt_filename_query(filename: str) -> str:
    parts = [part.strip() for part in filename.split("-") if part.strip()]
    if len(parts) > 2 and parts[0] == "e":
        return " ".join(parts[2:])
    return filename.replace("-", " ")


def tokenize_text(*values: Any) -> List[str]:
    tokens: List[str] = []
    seen = set()
    for value in values:
        if value is None:
            continue
        for token in re.findall(r"[0-9A-Za-zÀ-ÿ]+", str(value).lower()):
            if len(token) < 3 or token in TOKEN_STOPWORDS:
                continue
            if token in seen:
                continue
            seen.add(token)
            tokens.append(token)
    return tokens


def derive_visual_mode(prompt_entry: Dict[str, Any]) -> str:
    explicit = str(prompt_entry.get("visual_mode", "")).strip()
    if explicit:
        return explicit
    prompt_class = str(prompt_entry.get("class", "")).strip().lower()
    return VISUAL_MODE_BY_CLASS.get(prompt_class, "documentary-realistic")


def derive_product_slice(prompt_entry: Dict[str, Any]) -> str:
    explicit = str(prompt_entry.get("product_slice", "")).strip()
    if explicit:
        return explicit

    filename = str(prompt_entry.get("filename", "")).lower()
    if any(tag in filename for tag in ("language-settings", "add-admin-action", "pin-use")):
        return "upper-front-panel"
    if "fingerprint" in filename:
        return "handle-sensor-zone"
    if "downloads-docs" in filename:
        return "product-plus-document"
    if "troubleshoot" in filename:
        return "interaction-zone"
    return "full-product"


def requires_visible_keypad_numerals(prompt_entry: Dict[str, Any]) -> bool:
    filename = str(prompt_entry.get("filename", "")).strip().lower()
    if not filename:
        return False
    if any(tag in filename for tag in ("app", "link-qr", "fingerprint", "downloads-docs", "troubleshoot")):
        return False
    if "e-nova" in filename:
        return False
    if not any(tag in filename for tag in ("add-admin-action", "pin-use", "language-settings")):
        return False

    modules = str(prompt_entry.get("modules", "")).strip().lower()
    prompt = str(prompt_entry.get("prompt", "")).strip().lower()
    manual_keywords = str(prompt_entry.get("manual_keywords", "")).strip().lower()

    keypad_signals = any(
        signal in " ".join((modules, prompt, manual_keywords))
        for signal in (
            "keypad interaction",
            "zona numérica",
            "zona de teclado",
            "teclado",
            "numerales integrados",
            "handle numerals",
            "keypad",
            "digits",
            "numerals",
        )
    )
    anti_signals = any(
        signal in prompt
        for signal in (
            "sin añadir teclado físico",
            "sin teclado físico inventado",
            "sin inventar un panel externo",
            "sin inventar pantalla o panel frontal",
            "sin inventar paneles o interfaces externas",
        )
    )
    return keypad_signals and not anti_signals


def derive_text_truth_policy(prompt_entry: Dict[str, Any], visual_mode: str) -> str:
    explicit = str(prompt_entry.get("text_truth_policy", "")).strip()
    if explicit:
        if explicit in {"no-readable-ui", "labels-added-later"} and requires_visible_keypad_numerals(prompt_entry):
            return "keypad-numerals-visible"
        return explicit

    if requires_visible_keypad_numerals(prompt_entry):
        return "keypad-numerals-visible"

    filename = str(prompt_entry.get("filename", "")).lower()
    if "app" in filename or "qr" in filename:
        return "screen-context-only"
    if any(tag in filename for tag in ("language-settings", "pin-use", "add-admin-action")):
        return "no-readable-ui"
    if "schematic" in visual_mode:
        return "labels-added-later"
    return "no-fabricated-technical-text"


def derive_overlay_plan(
    prompt_entry: Dict[str, Any],
    visual_mode: str,
    product_slice: str,
    text_truth_policy: str,
) -> str:
    explicit = str(prompt_entry.get("overlay_plan", "")).strip()
    if explicit:
        return explicit
    if "schematic" in visual_mode:
        return "outline callouts + numbered arrows + editorial labels"
    if product_slice != "full-product":
        return "tight crop + focus ring + optional callout labels"
    if text_truth_policy in {"screen-context-only", "no-readable-ui"}:
        return "editorial cleanup of accidental readable UI"
    return "none"


def derive_manual_graphics_lane(
    prompt_entry: Dict[str, Any],
    visual_mode: str,
    product_slice: str,
    overlay_plan: str,
) -> str:
    explicit = str(prompt_entry.get("manual_graphics_lane", "")).strip()
    if explicit:
        return explicit

    prompt_class = str(prompt_entry.get("class", "")).strip().lower()
    if "schematic" in visual_mode:
        return "manual-graphics"
    if prompt_class == "hybrid":
        return "hybrid-composite"
    if product_slice != "full-product" or overlay_plan != "none":
        return "prompt-plus-editorial"
    return "prompt-only"


def derive_instructional_goal(
    prompt_entry: Dict[str, Any], matrix_row: Dict[str, str], product_slice: str
) -> str:
    explicit = str(prompt_entry.get("instructional_goal", "")).strip()
    if explicit:
        return explicit

    use_text = str(prompt_entry.get("use", "")).strip() or strip_code(matrix_row.get("Page / Use", ""))
    if not use_text:
        use_text = str(prompt_entry.get("filename", "")).strip()
    return (
        f"apoyar el paso del manual '{use_text}' mostrando con claridad {product_slice} "
        "y la acción exacta sin inventar texto técnico"
    )


def match_manual_sections(
    manual_data: Dict[str, Any], prompt_entry: Dict[str, Any], matrix_row: Dict[str, str]
) -> List[Dict[str, Any]]:
    sections = manual_data.get("sections", [])
    if not sections:
        return []

    section_hints = split_prompt_field_list(prompt_entry.get("manual_section_hints", ""))
    manual_keywords = split_prompt_field_list(prompt_entry.get("manual_keywords", ""))
    query_tokens = tokenize_text(
        prompt_filename_query(str(prompt_entry.get("filename", ""))),
        prompt_entry.get("use", ""),
        matrix_row.get("Page / Use", ""),
        prompt_entry.get("instructional_goal", ""),
        prompt_entry.get("product_slice", ""),
        " ".join(section_hints),
        " ".join(manual_keywords),
    )

    matches: List[Dict[str, Any]] = []
    for index, section in enumerate(sections):
        title = str(section.get("title", "")).strip()
        semantic_category = str(section.get("semantic_category", "")).strip()
        content_lines = [str(item).strip() for item in section.get("content", []) if str(item).strip()]
        section_text = " ".join([title, semantic_category, *content_lines]).lower()
        title_lower = title.lower()
        score = 0
        matched_terms: List[str] = []

        for hint in section_hints:
            normalized = hint.lower()
            if normalized and normalized in title_lower:
                score += 12
                matched_terms.append(hint)
            elif normalized and normalized in section_text:
                score += 8
                matched_terms.append(hint)

        for keyword in manual_keywords:
            normalized = keyword.lower()
            if normalized and normalized in title_lower:
                score += 8
                matched_terms.append(keyword)
            elif normalized and normalized in section_text:
                score += 4
                matched_terms.append(keyword)

        for token in query_tokens:
            if token in title_lower:
                score += 3
                matched_terms.append(token)
            elif token in section_text:
                score += 1
                matched_terms.append(token)

        if score <= 0:
            continue

        excerpt = " ".join(content_lines[:6]).strip()
        matches.append(
            {
                "index": index,
                "title": title,
                "semantic_category": semantic_category,
                "score": score,
                "matched_terms": split_prompt_field_list(matched_terms),
                "excerpt": excerpt,
            }
        )

    matches.sort(key=lambda item: (-item["score"], item["index"]))
    if not section_hints and not manual_keywords:
        matches = [item for item in matches if item["score"] >= 4]
    return matches[:3]


def derive_intent_confidence(matches: List[Dict[str, Any]]) -> str:
    if not matches:
        return "low"
    top_score = matches[0].get("score", 0)
    if top_score >= 18:
        return "high"
    if top_score >= 8:
        return "medium"
    return "low"


def build_editorial_tasks(lane: str, product_slice: str, overlay_plan: str, text_truth_policy: str) -> List[str]:
    tasks: List[str] = []
    if lane == "manual-graphics":
        tasks.extend(
            [
                "Generate a simplified base with clean margins for later editorial labeling.",
                "Add arrows, callouts, and numbered labels outside the model output.",
                "Replace any accidental readable UI with editorial typography or icons.",
            ]
        )
    elif lane == "hybrid-composite":
        tasks.extend(
            [
                "Prepare an exact product slice or shell before final layout.",
                "Use a clean generated or photographed background plate.",
                "Composite the exact product geometry before adding labels or callouts.",
            ]
        )
    elif lane == "prompt-plus-editorial":
        tasks.extend(
            [
                "Generate a clean instructional base with uncluttered negative space.",
                "Apply post-generation crops and callouts around the active interaction zone.",
            ]
        )
    else:
        tasks.append("Use the model output as the base image, then run manual product-truth review.")

    if product_slice != "full-product":
        tasks.append(f"Crop or frame the final layout around {product_slice}.")
    if overlay_plan != "none":
        tasks.append(f"Overlay plan: {overlay_plan}.")
    if text_truth_policy == "no-readable-ui":
        tasks.append("Do not let generated settings text become technical proof in the final manual graphic.")
    if text_truth_policy == "keypad-numerals-visible":
        tasks.append(
            "Keep the keypad numerals visible as part of the hardware while removing fabricated menus or extra technical text."
        )
    if text_truth_policy == "screen-context-only":
        tasks.append("Keep all app or QR content contextual; replace any precise UI proof with editorial assets.")
    return tasks


def describe_product_slice(product_slice: str) -> str:
    mapping = {
        "upper-front-panel": "mostrar solo la zona superior de control o panel frontal",
        "handle-sensor-zone": "centrar la imagen en la manija y el sensor de huella",
        "product-plus-document": "mostrar el producto junto con el soporte documental, no una escena completa",
        "interaction-zone": "mostrar solo la zona de interacción necesaria para el paso",
        "full-product": "mantener el producto completo visible",
    }
    return mapping.get(product_slice, product_slice)


def describe_visual_mode(visual_mode: str) -> str:
    mapping = {
        "documentary-realistic": "realismo documental sobrio",
        "instructional-simplified": "semi-realismo instruccional con ruido visual reducido",
        "schematic-outline": "gráfico esquemático y contextual con trazos simplificados",
        "hybrid-product-shell": "modo híbrido con geometría real del producto y simplificación editorial",
    }
    return mapping.get(visual_mode, visual_mode)


def describe_text_truth_policy(text_truth_policy: str) -> str:
    mapping = {
        "keypad-numerals-visible": "los numerales físicos del keypad deben verse claros y legibles, sin inventar menús ni texto técnico adicional",
        "no-readable-ui": "no renderizar texto, dígitos o menús legibles como evidencia técnica",
        "screen-context-only": "si aparece una pantalla, que sea solo contextual y no una prueba técnica",
        "labels-added-later": "las etiquetas y textos se agregan después en edición, no dentro de la imagen generada",
        "no-fabricated-technical-text": "no inventar texto técnico, nombres de funciones ni mensajes precisos",
    }
    return mapping.get(text_truth_policy, text_truth_policy)


def sanitize_manual_excerpt(excerpt: str, text_truth_policy: str) -> str:
    text = " ".join(str(excerpt).split()).strip()
    if not text:
        return ""

    if text_truth_policy in {"no-readable-ui", "labels-added-later"}:
        text = re.sub(r'["“”«»][^"“”«»]*["“”«»]', "mensaje editorial", text)
        text = re.sub(r"\b\d+\b", "secuencia editorial", text)
        text = text.replace("*", "tecla de acceso")
        text = text.replace("#", "tecla de confirmación")
        text = re.sub(r"\s+", " ", text).strip(" -;,.:")
    elif text_truth_policy == "keypad-numerals-visible":
        text = re.sub(r'["“”«»][^"“”«»]*["“”«»]', "mensaje editorial", text)
        text = re.sub(r"\b\d{3,}\b", "código editorial", text)
        text = re.sub(r"\s+", " ", text).strip(" -;,.:")

    if len(text) > 220:
        text = text[:217].rstrip(" ,;:.") + "..."
    return text


def build_prompt_contract(base_prompt: str, image_intent: Dict[str, Any]) -> str:
    lines = [base_prompt.strip()]
    lines.append(f"Objetivo instruccional estricto: {image_intent['instructional_goal']}.")
    lines.append(f"Modo visual requerido: {describe_visual_mode(image_intent['visual_mode'])}.")
    lines.append(f"Recorte o foco del producto: {describe_product_slice(image_intent['product_slice'])}.")
    lines.append(f"Política de verdad textual: {describe_text_truth_policy(image_intent['text_truth_policy'])}.")
    if image_intent.get("text_truth_policy") == "keypad-numerals-visible":
        lines.append(
            "Los numerales físicos del keypad deben permanecer visibles y legibles como parte del hardware, sin destacar una secuencia concreta como si fuera la instrucción oficial."
        )

    matched_sections = image_intent.get("matched_sections", [])
    intent_confidence = str(image_intent.get("intent_confidence", "")).strip().lower()
    if matched_sections and intent_confidence in {"medium", "high"}:
        titles = ", ".join(match["title"] for match in matched_sections[:2])
        lines.append(f"Alinear la escena con estas secciones del manual: {titles}.")
        excerpt = sanitize_manual_excerpt(
            matched_sections[0].get("excerpt", ""),
            str(image_intent.get("text_truth_policy", "")).strip(),
        )
        if excerpt:
            context_label = "Contexto textual a apoyar"
            if image_intent.get("text_truth_policy") in {"no-readable-ui", "labels-added-later"}:
                context_label = "Contexto procedimental a apoyar"
            lines.append(f"{context_label}: {excerpt}")

    lane = image_intent.get("manual_graphics_lane")
    if lane == "manual-graphics":
        lines.append(
            "Priorizar claridad esquemática y contextual sobre realismo; dejar espacio limpio para callouts editoriales."
        )
    elif lane == "hybrid-composite":
        lines.append(
            "Preservar la silueta exterior y las zonas protegidas para una etapa híbrida posterior con recortes u overlays."
        )
    elif lane == "prompt-plus-editorial":
        lines.append(
            "Mantener fondo y composición limpios para permitir recortes, flechas y anotaciones editoriales posteriores."
        )

    return "\n".join(line for line in lines if line)


def build_negative_prompt_contract(base_negative_prompt: str, image_intent: Dict[str, Any]) -> str:
    extra_clauses: List[str] = []
    lane = image_intent.get("manual_graphics_lane")
    text_truth_policy = image_intent.get("text_truth_policy")

    if text_truth_policy == "keypad-numerals-visible":
        extra_clauses.append(
            "blank keypad, missing printed numerals, unreadable numeric pad, melted keypad labels, fabricated settings menus, fabricated function labels, highlighted code sequence presented as the official code"
        )
    elif text_truth_policy == "no-readable-ui":
        extra_clauses.append(
            "readable settings text, readable menu labels, readable technical digits, readable keypad numerals, literal code sequences"
        )
    elif text_truth_policy == "screen-context-only":
        extra_clauses.append("readable app flow, readable QR, screen used as technical proof")
    elif text_truth_policy == "labels-added-later":
        extra_clauses.append(
            "baked-in arrows, baked-in labels, embedded technical typography, embedded digits, readable keypad numerals, literal code sequences"
        )
    else:
        extra_clauses.append("fabricated technical text, precise fake instructions, readable proof text")

    if image_intent.get("product_slice") != "full-product":
        extra_clauses.append("full product hero framing when only a local product slice is needed")

    if lane == "manual-graphics":
        extra_clauses.append("photorealistic hero render, cinematic styling, decorative lifestyle background")
    elif lane == "prompt-plus-editorial":
        extra_clauses.append("busy background leaving no room for editorial callouts")
    elif lane == "hybrid-composite":
        extra_clauses.append("reinterpreted shell geometry, altered protected zones")

    clauses = [base_negative_prompt.strip(), *extra_clauses]
    return ", ".join(clause for clause in clauses if clause)


def build_image_intent(
    prompt_entry: Dict[str, Any], matrix_row: Dict[str, str], manual_data: Dict[str, Any]
) -> Dict[str, Any]:
    visual_mode = derive_visual_mode(prompt_entry)
    product_slice = derive_product_slice(prompt_entry)
    text_truth_policy = derive_text_truth_policy(prompt_entry, visual_mode)
    overlay_plan = derive_overlay_plan(prompt_entry, visual_mode, product_slice, text_truth_policy)
    manual_graphics_lane = derive_manual_graphics_lane(
        prompt_entry,
        visual_mode,
        product_slice,
        overlay_plan,
    )
    matched_sections = match_manual_sections(manual_data, prompt_entry, matrix_row)

    image_intent = {
        "instructional_goal": derive_instructional_goal(prompt_entry, matrix_row, product_slice),
        "visual_mode": visual_mode,
        "product_slice": product_slice,
        "text_truth_policy": text_truth_policy,
        "overlay_plan": overlay_plan,
        "manual_graphics_lane": manual_graphics_lane,
        "manual_section_hints": split_prompt_field_list(prompt_entry.get("manual_section_hints", "")),
        "manual_keywords": split_prompt_field_list(prompt_entry.get("manual_keywords", "")),
        "matched_sections": matched_sections,
        "intent_confidence": derive_intent_confidence(matched_sections),
    }
    image_intent["editorial_tasks"] = build_editorial_tasks(
        manual_graphics_lane,
        product_slice,
        overlay_plan,
        text_truth_policy,
    )
    return image_intent


def parse_registry() -> List[ProductPaths]:
    registry_rows = parse_markdown_table(read_text(REGISTRY_PATH))
    products: List[ProductPaths] = []

    for row in registry_rows:
        product_name = row["Product"]
        slug = normalize_slug(product_name)
        reference_image = (REGISTRY_PATH.parent / strip_code(row["Reference image"])).resolve()
        visual_profile = (REGISTRY_PATH.parent / strip_code(row["Visual profile"])).resolve()
        status_tracker = (REGISTRY_PATH.parent / strip_code(row["Status tracker"])).resolve()
        validation_checklist = (REGISTRY_PATH.parent / strip_code(row["Validation checklist"])).resolve()
        product_root = status_tracker.parent

        products.append(
            ProductPaths(
                slug=slug,
                product_name=product_name,
                reference_image=reference_image,
                visual_profile=visual_profile,
                status_tracker=status_tracker,
                validation_checklist=validation_checklist,
                product_root=product_root,
                prompt_pack=product_root / "ai-image-prompts.md",
                generation_matrix=product_root / "image-generation-matrix.md",
                selected_assets_register=product_root / "generated/selected-assets-register.md",
                manual_json=REPO_ROOT / "generated_manuals" / slug / "manual.json",
            )
        )

    return products


def parse_by_filename(
    table_rows: List[Dict[str, str]], filename_key: str = "Filename"
) -> Dict[str, Dict[str, str]]:
    rows_by_filename: Dict[str, Dict[str, str]] = {}
    for row in table_rows:
        filename = strip_code(row.get(filename_key, ""))
        if filename:
            rows_by_filename[filename] = row
    return rows_by_filename


def format_to_dimensions(format_description: str) -> Tuple[int, int]:
    return FORMAT_DIMENSIONS.get(format_description.strip(), (1024, 1024))


def build_job_record(
    prompt_entry: Dict[str, Any],
    matrix_rows: Dict[str, Dict[str, str]],
    status_rows: Dict[str, Dict[str, str]],
    register_rows: Dict[str, Dict[str, str]],
    manual_data: Dict[str, Any],
) -> Dict[str, Any]:
    filename = prompt_entry["filename"]
    matrix_row = matrix_rows.get(filename, {})
    status_row = status_rows.get(filename, {})
    register_row = register_rows.get(filename, {})
    format_description = prompt_entry.get("format", "")
    dimensions = format_to_dimensions(format_description)
    current_state = strip_code(register_row.get("Current state", "")) or strip_code(
        status_row.get("Status", matrix_row.get("Status", "planned"))
    )
    base_prompt = prompt_entry.get("prompt", "")
    base_negative_prompt = prompt_entry.get("negative_prompt", "")
    image_intent = build_image_intent(prompt_entry, matrix_row, manual_data)
    prompt_contract_fields = {
        "visual_mode": image_intent["visual_mode"],
        "product_slice": image_intent["product_slice"],
        "instructional_goal": image_intent["instructional_goal"],
        "text_truth_policy": image_intent["text_truth_policy"],
        "overlay_plan": image_intent["overlay_plan"],
        "manual_section_hints": image_intent["manual_section_hints"],
        "manual_keywords": image_intent["manual_keywords"],
    }

    return {
        "order": prompt_entry["order"],
        "asset_id": strip_code(matrix_row.get("ID", "")),
        "filename": filename,
        "publish_target": strip_code(register_row.get("Publish target", "")) or f"{filename}.webp",
        "class": prompt_entry.get("class", strip_code(status_row.get("Class", ""))),
        "use": prompt_entry.get("use", ""),
        "page_or_use": strip_code(matrix_row.get("Page / Use", "")),
        "priority": strip_code(matrix_row.get("Priority", "")),
        "status": strip_code(status_row.get("Status", matrix_row.get("Status", "planned"))),
        "notes": strip_code(status_row.get("Notes", "")),
        "product_truth_note": strip_code(matrix_row.get("Product-truth note", "")),
        "prompt_modules": prompt_entry.get("modules", ""),
        "base_prompt": base_prompt,
        "prompt": build_prompt_contract(base_prompt, image_intent),
        "base_negative_prompt": base_negative_prompt,
        "negative_prompt": build_negative_prompt_contract(base_negative_prompt, image_intent),
        "prompt_contract_fields": prompt_contract_fields,
        "image_intent": image_intent,
        "manual_graphics_lane": image_intent["manual_graphics_lane"],
        "editorial_tasks": image_intent["editorial_tasks"],
        "format": format_description,
        "dimensions": {"width": dimensions[0], "height": dimensions[1]},
        "current_state": current_state,
        "winning_variant": strip_code(register_row.get("Winning variant", "")) or "pending",
        "validation_status": strip_code(register_row.get("Validation status", "")) or "pending",
    }


def build_manifest(paths: ProductPaths) -> Dict[str, Any]:
    prompt_pack = parse_prompt_pack(paths.prompt_pack)
    matrix_rows = parse_by_filename(parse_markdown_table(read_text(paths.generation_matrix)))
    status_rows = parse_by_filename(parse_markdown_table(read_text(paths.status_tracker)))
    register_rows = parse_by_filename(
        parse_markdown_table(read_text(paths.selected_assets_register)), filename_key="Stable filename"
    )
    manual_data = read_json(paths.manual_json) if paths.manual_json.exists() else {}

    jobs = [
        build_job_record(prompt_entry, matrix_rows, status_rows, register_rows, manual_data)
        for prompt_entry in prompt_pack["prompts"]
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product": {
            "name": paths.product_name,
            "slug": paths.slug,
            "reference_image": repo_relative(paths.reference_image),
            "visual_profile": repo_relative(paths.visual_profile),
            "validation_checklist": repo_relative(paths.validation_checklist),
            "status_tracker": repo_relative(paths.status_tracker),
            "prompt_pack": repo_relative(paths.prompt_pack),
            "generation_matrix": repo_relative(paths.generation_matrix),
            "selected_assets_register": repo_relative(paths.selected_assets_register),
            "manual_json": repo_relative(paths.manual_json) if paths.manual_json.exists() else None,
        },
        "manual_context": {
            "source_pdf": manual_data.get("source_pdf"),
            "sections_count": len(manual_data.get("sections", [])),
            "section_titles": [section.get("title") for section in manual_data.get("sections", [])[:12]],
        },
        "image_intent_policy": {
            "strict_from_manual_json": True,
            "prompt_contract_fields": [
                "visual_mode",
                "product_slice",
                "instructional_goal",
                "text_truth_policy",
                "overlay_plan",
                "manual_section_hints",
                "manual_keywords",
            ],
            "manual_graphics_lanes": [
                "prompt-only",
                "prompt-plus-editorial",
                "hybrid-composite",
                "manual-graphics",
            ],
        },
        "prompt_rules": {
            "shared_negative_base": prompt_pack["shared_negative_base"],
            "product_negative_additions": prompt_pack["product_negative_additions"],
        },
        "jobs": jobs,
    }


def export_manifests(products: Optional[List[str]], output_dir: Path) -> int:
    selected_slugs = {slug.strip().lower() for slug in products or []}
    available_products = parse_registry()
    manifests_written = 0

    output_dir.mkdir(parents=True, exist_ok=True)
    index: List[Dict[str, str]] = []

    for product_paths in available_products:
        if selected_slugs and product_paths.slug not in selected_slugs:
            continue

        manifest = build_manifest(product_paths)
        manifest_path = output_dir / f"{product_paths.slug}-generation-manifest.json"
        write_json(manifest_path, manifest)
        index.append(
            {
                "slug": product_paths.slug,
                "manifest": repo_relative(manifest_path),
            }
        )
        manifests_written += 1
        print(f"Exported manifest: {manifest_path}")

    if selected_slugs and manifests_written != len(selected_slugs):
        exported = {entry["slug"] for entry in index}
        missing = sorted(selected_slugs - exported)
        raise SystemExit(f"Unknown or unavailable product slug(s): {', '.join(missing)}")

    index_path = output_dir / "manifest-index.json"
    write_json(index_path, index)
    print(f"Wrote manifest index: {index_path}")
    return 0


def deterministic_seed(slug: str, filename: str, variant_index: int) -> int:
    seed_source = f"{slug}|{filename}|{variant_index}".encode("utf-8")
    digest = hashlib.sha256(seed_source).hexdigest()
    return int(digest[:8], 16) % 2147483647


def load_manifest(path: Path) -> Dict[str, Any]:
    manifest = read_json(path)
    if "product" not in manifest or "jobs" not in manifest:
        raise SystemExit(f"Invalid manifest file: {path}")
    return manifest


def load_product_paths(product_slug: str) -> ProductPaths:
    for product_paths in parse_registry():
        if product_paths.slug == product_slug:
            return product_paths
    raise SystemExit(f"Unknown manifest product slug: {product_slug}")


def filter_manifest_jobs(manifest: Dict[str, Any], selected_jobs: Optional[List[str]]) -> List[Dict[str, Any]]:
    jobs = manifest["jobs"]
    if not selected_jobs:
        return jobs

    requested = {value.strip() for value in selected_jobs}
    filtered = [
        job for job in jobs if job.get("filename") in requested or job.get("asset_id") in requested
    ]
    available = {job.get("filename") for job in jobs} | {job.get("asset_id") for job in jobs}
    missing = sorted(requested - available)
    if missing:
        raise SystemExit(f"Unknown manifest job selector(s): {', '.join(missing)}")
    return filtered


def build_writeback_records(
    manifest: Dict[str, Any],
    run_dir: Path,
    state: str,
    selected_jobs: Optional[List[str]],
    validation_status: str,
    score_summary_path: Optional[Path] = None,
) -> Dict[str, Dict[str, Any]]:
    manifest_jobs = filter_manifest_jobs(manifest, selected_jobs)
    manifest_jobs_by_filename = {job["filename"]: job for job in manifest_jobs}

    if state == "generated":
        run_summary_path = run_dir / "run-summary.json"
        if not run_summary_path.exists():
            raise SystemExit(f"Missing run summary: {run_summary_path}")

        run_summary = read_json(run_summary_path)
        records: Dict[str, Dict[str, Any]] = {}
        for run_job in run_summary.get("jobs", []):
            filename = run_job.get("filename")
            if filename not in manifest_jobs_by_filename:
                continue
            records[filename] = {
                "job": manifest_jobs_by_filename[filename],
                "state": "generated",
                "winning_variant": "pending",
                "validation_status": validation_status,
            }
        return records

    score_summary_path = score_summary_path or (run_dir / "score-summary.json")
    if not score_summary_path.exists():
        raise SystemExit(f"Missing score summary: {score_summary_path}")

    score_summary = read_json(score_summary_path)
    records = {}
    for scored_job in score_summary.get("jobs", []):
        filename = scored_job.get("filename")
        if filename not in manifest_jobs_by_filename:
            continue
        winning_variant = scored_job.get("recommended_variant")
        if not winning_variant:
            raise SystemExit(f"Missing recommended variant for {filename} in {score_summary_path}")
        records[filename] = {
            "job": manifest_jobs_by_filename[filename],
            "state": "selected",
            "winning_variant": winning_variant,
            "validation_status": validation_status,
        }
    return records


def build_status_row(headers: List[str], record: Dict[str, Any]) -> Dict[str, str]:
    job = record["job"]
    row = {header: "" for header in headers}
    row.update(
        {
            "Slot": str(job.get("order", "")),
            "Filename": job.get("filename", ""),
            "Class": job.get("class", ""),
            "Status": record["state"],
            "Notes": job.get("notes", ""),
        }
    )
    return row


def build_register_row(headers: List[str], record: Dict[str, Any]) -> Dict[str, str]:
    job = record["job"]
    row = {header: "" for header in headers}
    row.update(
        {
            "Stable filename": job.get("filename", ""),
            "Slot": str(job.get("order", "")),
            "Asset ID": job.get("asset_id", ""),
            "Current state": record["state"],
            "Winning variant": record["winning_variant"],
            "Validation status": record["validation_status"],
            "Publish target": job.get("publish_target", f"{job.get('filename', '')}.webp"),
            "Notes": job.get("notes", ""),
        }
    )
    return row


def update_status_tracker(
    path: Path, records: Dict[str, Dict[str, Any]], dry_run: bool
) -> Tuple[int, int]:
    lines = read_text(path).splitlines()
    start, end, headers, rows = find_markdown_table(lines, {"Filename", "Status"})
    rows_by_filename = {row.get("Filename", ""): row for row in rows}
    updated = 0
    added = 0

    for filename, record in records.items():
        row = rows_by_filename.get(filename)
        if row is None:
            rows.append(build_status_row(headers, record))
            added += 1
            continue

        row["Status"] = record["state"]
        if "Class" in headers:
            row["Class"] = record["job"].get("class", "")
        updated += 1

    sort_rows_by_slot(rows)
    rendered_lines = lines[:start] + render_markdown_table(headers, rows) + lines[end:]
    if not dry_run:
        write_text(path, "\n".join(rendered_lines) + "\n")
    return updated, added


def update_selected_assets_register(
    path: Path, records: Dict[str, Dict[str, Any]], dry_run: bool
) -> Tuple[int, int]:
    lines = read_text(path).splitlines()
    start, end, headers, rows = find_markdown_table(lines, {"Stable filename", "Current state"})
    rows_by_filename = {row.get("Stable filename", ""): row for row in rows}
    updated = 0
    added = 0

    for filename, record in records.items():
        row = rows_by_filename.get(filename)
        if row is None:
            rows.append(build_register_row(headers, record))
            added += 1
            continue

        if "Asset ID" in headers and not row.get("Asset ID"):
            row["Asset ID"] = record["job"].get("asset_id", "")
        row["Current state"] = record["state"]
        if "Winning variant" in headers and record["state"] == "selected":
            row["Winning variant"] = record["winning_variant"]
        elif "Winning variant" in headers and not row.get("Winning variant"):
            row["Winning variant"] = record["winning_variant"]
        if "Validation status" in headers:
            row["Validation status"] = record["validation_status"]
        if "Publish target" in headers and not row.get("Publish target"):
            row["Publish target"] = record["job"].get("publish_target", "")
        updated += 1

    sort_rows_by_slot(rows)
    rendered_lines = lines[:start] + render_markdown_table(headers, rows) + lines[end:]
    if not dry_run:
        write_text(path, "\n".join(rendered_lines) + "\n")
    return updated, added


def ensure_node_input(workflow: Dict[str, Any], node_id: Optional[str]) -> None:
    if not node_id:
        return
    if node_id not in workflow:
        raise SystemExit(f"Workflow does not contain node {node_id}")
    if "inputs" not in workflow[node_id]:
        workflow[node_id]["inputs"] = {}


def set_node_input(workflow: Dict[str, Any], node_id: Optional[str], field_name: str, value: Any) -> None:
    if not node_id:
        return
    ensure_node_input(workflow, node_id)
    workflow[node_id]["inputs"][field_name] = value


def build_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def derive_size_value(width: int, height: int, mode: str) -> str:
    if mode == "openai-gpt-image":
        if width == height:
            return "1024x1024"
        if width > height:
            return "1536x1024"
        return "1024x1536"
    return f"{width}x{height}"


def render_workflow_variant(
    workflow_template: Dict[str, Any],
    manifest: Dict[str, Any],
    job: Dict[str, Any],
    variant_index: int,
    args: argparse.Namespace,
    uploaded_reference_name: Optional[str],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    workflow = copy.deepcopy(workflow_template)
    seed = deterministic_seed(manifest["product"]["slug"], job["filename"], variant_index)
    candidate_label = f"v{variant_index:02d}"

    set_node_input(workflow, args.positive_node, args.positive_field, job["prompt"])
    set_node_input(workflow, args.negative_node, args.negative_field, job["negative_prompt"])
    set_node_input(workflow, args.seed_node, args.seed_field, seed)
    set_node_input(
        workflow,
        args.reference_image_node,
        args.reference_image_field,
        uploaded_reference_name,
    )

    width = job["dimensions"]["width"]
    height = job["dimensions"]["height"]
    size_value = derive_size_value(width, height, args.size_mode)
    set_node_input(workflow, args.size_node, args.size_field, size_value)
    set_node_input(workflow, args.width_node, args.width_field, width)
    set_node_input(workflow, args.height_node, args.height_field, height)

    filename_prefix = f"{job['filename']}-{candidate_label}"
    set_node_input(workflow, args.filename_prefix_node, args.filename_prefix_field, filename_prefix)

    metadata = {
        "candidate_label": candidate_label,
        "variant_index": variant_index,
        "seed": seed,
        "filename_prefix": filename_prefix,
        "size": size_value,
    }
    return workflow, metadata


def json_headers(api_key: str) -> Dict[str, str]:
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }


def api_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None,
    body: Optional[bytes] = None,
) -> bytes:
    full_url = url
    if params:
        full_url = f"{url}?{parse.urlencode(params)}"

    req = request.Request(full_url, data=body, headers=headers, method=method)
    try:
        with request.urlopen(req) as response:
            return response.read()
    except error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        raise CloudApiError(f"HTTP {exc.code} calling {full_url}: {payload}") from exc
    except error.URLError as exc:
        raise CloudApiError(f"Failed to call {full_url}: {exc}") from exc


def api_get_json(base_url: str, api_key: str, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    raw = api_request("GET", f"{base_url}{path}", {"X-API-Key": api_key}, params=params)
    return json.loads(raw.decode("utf-8"))


def api_post_json(base_url: str, api_key: str, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    raw = api_request(
        "POST",
        f"{base_url}{path}",
        json_headers(api_key),
        body=json.dumps(payload).encode("utf-8"),
    )
    return json.loads(raw.decode("utf-8"))


def build_multipart_body(
    fields: Dict[str, str],
    file_field: str,
    filename: str,
    file_bytes: bytes,
    content_type: str,
) -> Tuple[bytes, str]:
    boundary = f"----BeslockBoundary{uuid.uuid4().hex}"
    body = bytearray()

    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        (
            f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
    )
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return bytes(body), boundary


def upload_image(base_url: str, api_key: str, image_path: Path) -> Dict[str, Any]:
    content_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    file_bytes = image_path.read_bytes()
    body, boundary = build_multipart_body(
        fields={"type": "input", "overwrite": "false", "subfolder": "beslock"},
        file_field="image",
        filename=image_path.name,
        file_bytes=file_bytes,
        content_type=content_type,
    )
    raw = api_request(
        "POST",
        f"{base_url}/api/upload/image",
        {
            "X-API-Key": api_key,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        body=body,
    )
    return json.loads(raw.decode("utf-8"))


def get_job_status(base_url: str, api_key: str, prompt_id: str) -> str:
    response = api_get_json(base_url, api_key, f"/api/job/{prompt_id}/status")
    return response["status"]


def poll_for_completion(
    base_url: str,
    api_key: str,
    prompt_id: str,
    timeout_seconds: int,
    poll_interval: float,
) -> str:
    start = time.time()
    while time.time() - start < timeout_seconds:
        status = get_job_status(base_url, api_key, prompt_id)
        if status in {"completed", "success"}:
            return status
        if status in {"failed", "cancelled"}:
            return status
        time.sleep(poll_interval)
    raise TimeoutError(f"Job {prompt_id} did not complete within {timeout_seconds}s")


def download_output_file(
    base_url: str,
    api_key: str,
    filename: str,
    subfolder: str,
    output_type: str,
) -> bytes:
    return api_request(
        "GET",
        f"{base_url}/api/view",
        {"X-API-Key": api_key},
        params={"filename": filename, "subfolder": subfolder, "type": output_type},
    )


def save_job_outputs(
    base_url: str,
    api_key: str,
    outputs: Dict[str, Any],
    candidate_dir: Path,
) -> List[str]:
    downloaded: List[str] = []
    for node_outputs in outputs.values():
        for key in ("images", "video", "audio"):
            for file_info in node_outputs.get(key, []):
                filename = file_info["filename"]
                subfolder = file_info.get("subfolder", "")
                output_type = file_info.get("type", "output")
                file_bytes = download_output_file(base_url, api_key, filename, subfolder, output_type)
                output_path = candidate_dir / filename
                output_path.write_bytes(file_bytes)
                downloaded.append(repo_relative(output_path))
    return downloaded


def run_manifest(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser().resolve()
    workflow_path = Path(args.workflow).expanduser().resolve()
    output_root = Path(args.output).expanduser().resolve()
    base_url = args.base_url.rstrip("/")
    manifest = load_manifest(manifest_path)
    selected_jobs = filter_manifest_jobs(manifest, args.jobs)
    workflow_template = read_json(workflow_path)

    run_root = output_root / manifest["product"]["slug"] / build_run_id()
    run_root.mkdir(parents=True, exist_ok=True)
    write_json(run_root / "manifest.snapshot.json", manifest)

    run_summary: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product": manifest["product"],
        "manifest": repo_relative(manifest_path),
        "workflow_template": repo_relative(workflow_path),
        "run_dir": repo_relative(run_root),
        "dry_run": args.dry_run,
        "wait_for_completion": args.wait,
        "variant_count": args.variant_count,
        "jobs": [],
    }

    api_key = None
    if not args.dry_run:
        api_key = os.environ.get(args.api_key_env)
        if not api_key:
            raise SystemExit(
                f"Set {args.api_key_env} before calling the Comfy Cloud runner, or use --dry-run."
            )

    uploaded_reference_name = None
    if args.reference_image_node:
        reference_image_path = REPO_ROOT / manifest["product"]["reference_image"]
        if not reference_image_path.exists():
            raise SystemExit(f"Reference image not found: {reference_image_path}")
        if args.dry_run:
            uploaded_reference_name = reference_image_path.name
        else:
            upload_result = upload_image(base_url, api_key, reference_image_path)
            uploaded_reference_name = upload_result["name"]
            run_summary["uploaded_reference_image"] = upload_result

    for job in selected_jobs:
        for variant_index in range(1, args.variant_count + 1):
            rendered_workflow, metadata = render_workflow_variant(
                workflow_template,
                manifest,
                job,
                variant_index,
                args,
                uploaded_reference_name,
            )
            candidate_dir = run_root / "candidates" / job["filename"] / metadata["candidate_label"]
            candidate_dir.mkdir(parents=True, exist_ok=True)
            workflow_render_path = candidate_dir / "workflow.rendered.json"
            write_json(workflow_render_path, rendered_workflow)

            job_record: Dict[str, Any] = {
                "asset_id": job["asset_id"],
                "filename": job["filename"],
                "status": "rendered",
                "format": job["format"],
                "dimensions": job["dimensions"],
                "seed": metadata["seed"],
                "variant_index": metadata["variant_index"],
                "candidate_label": metadata["candidate_label"],
                "candidate_dir": repo_relative(candidate_dir),
                "workflow_path": repo_relative(workflow_render_path),
                "prompt_excerpt": job["prompt"][:160],
                "downloaded_files": [],
            }

            if not args.dry_run:
                submit_payload = {
                    "prompt": rendered_workflow,
                    "extra_data": {
                        "api_key_comfy_org": api_key,
                        "product_slug": manifest["product"]["slug"],
                        "asset_id": job["asset_id"],
                        "filename": job["filename"],
                        "candidate_label": metadata["candidate_label"],
                    },
                }
                submit_result = api_post_json(base_url, api_key, "/api/prompt", submit_payload)
                prompt_id = submit_result["prompt_id"]
                job_record["prompt_id"] = prompt_id
                job_record["submit_result"] = submit_result
                job_record["status"] = "submitted"

                if args.wait:
                    final_status = poll_for_completion(
                        base_url,
                        api_key,
                        prompt_id,
                        timeout_seconds=args.timeout,
                        poll_interval=args.poll_interval,
                    )
                    job_record["status"] = final_status
                    job_detail = api_get_json(base_url, api_key, f"/api/jobs/{prompt_id}")
                    write_json(candidate_dir / "job.detail.json", job_detail)
                    if final_status in {"completed", "success"}:
                        job_record["downloaded_files"] = save_job_outputs(
                            base_url,
                            api_key,
                            job_detail.get("outputs", {}),
                            candidate_dir,
                        )
                    else:
                        job_record["execution_error"] = job_detail.get("execution_error")

            write_json(candidate_dir / "job.record.json", job_record)
            run_summary["jobs"].append(job_record)

    write_json(run_root / "run-summary.json", run_summary)
    print(f"Run artifacts written to: {run_root}")
    return 0


def find_latest_run_dir(product_slug: str) -> Path:
    product_runs_root = DEFAULT_RUNS_DIR / product_slug
    if not product_runs_root.exists():
        raise SystemExit(f"No runs found for {product_slug} under {product_runs_root}")

    candidates = sorted(path for path in product_runs_root.iterdir() if path.is_dir())
    if not candidates:
        raise SystemExit(f"No runs found for {product_slug} under {product_runs_root}")
    return candidates[-1]


def list_candidate_images(candidate_dir: Path, downloaded_files: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    for relative_path in downloaded_files:
        absolute = REPO_ROOT / relative_path
        if absolute.suffix.lower() in IMAGE_EXTENSIONS and absolute.exists():
            paths.append(absolute)

    if paths:
        return paths

    return sorted(
        path for path in candidate_dir.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def compute_file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_edge_energy(grayscale_image: Any) -> float:
    pixels = list(grayscale_image.getdata())
    width, height = grayscale_image.size
    if width < 2 or height < 2:
        return 0.0

    total = 0
    samples = 0
    for y in range(height):
        row_offset = y * width
        for x in range(width - 1):
            total += abs(pixels[row_offset + x] - pixels[row_offset + x + 1])
            samples += 1
    for y in range(height - 1):
        row_offset = y * width
        next_row_offset = (y + 1) * width
        for x in range(width):
            total += abs(pixels[row_offset + x] - pixels[next_row_offset + x])
            samples += 1
    return total / max(samples, 1)


def analyze_image(path: Path, expected_format: str, hash_counts: Dict[str, int]) -> Dict[str, Any]:
    if Image is None or ImageStat is None:
        raise SystemExit(
            "Pillow is required for scoring. Install the existing Python requirements before using `score`."
        )

    file_hash = compute_file_hash(path)
    with Image.open(path) as image:
        width, height = image.size
        grayscale = image.convert("L")
        grayscale.thumbnail((512, 512))
        brightness = ImageStat.Stat(grayscale).mean[0]
        contrast = ImageStat.Stat(grayscale).stddev[0]
        edge_energy = compute_edge_energy(grayscale)

    expected_width, expected_height = format_to_dimensions(expected_format)
    expected_ratio = expected_width / expected_height
    actual_ratio = width / height if height else 0.0
    ratio_delta = abs(actual_ratio - expected_ratio)

    flags: List[str] = []
    score = 100.0

    if ratio_delta > 0.08:
        flags.append("aspect_ratio_mismatch")
        score -= 20
    elif ratio_delta > 0.03:
        flags.append("aspect_ratio_drift")
        score -= 8

    if min(width, height) < min(expected_width, expected_height) * 0.75:
        flags.append("undersized")
        score -= 18

    if edge_energy < 10:
        flags.append("blur_risk_high")
        score -= 20
    elif edge_energy < 16:
        flags.append("blur_risk_medium")
        score -= 10

    if contrast < 22:
        flags.append("low_contrast")
        score -= 8
    if brightness < 45:
        flags.append("too_dark")
        score -= 6
    elif brightness > 225:
        flags.append("too_bright")
        score -= 6

    if hash_counts[file_hash] > 1:
        flags.append("exact_duplicate")
        score -= 35

    return {
        "path": repo_relative(path),
        "width": width,
        "height": height,
        "actual_ratio": round(actual_ratio, 4),
        "expected_ratio": round(expected_ratio, 4),
        "ratio_delta": round(ratio_delta, 4),
        "brightness": round(brightness, 2),
        "contrast": round(contrast, 2),
        "edge_energy": round(edge_energy, 2),
        "file_hash": file_hash,
        "flags": flags,
        "score": round(max(score, 0.0), 2),
    }


def flatten_flags(image_reports: List[Dict[str, Any]]) -> List[str]:
    unique: List[str] = []
    seen = set()
    for image_report in image_reports:
        for flag in image_report.get("flags", []):
            if flag in seen:
                continue
            seen.add(flag)
            unique.append(flag)
    return unique


def score_manifest(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = load_manifest(manifest_path)
    run_dir = Path(args.run_dir).expanduser().resolve() if args.run_dir else find_latest_run_dir(manifest["product"]["slug"])
    run_summary_path = run_dir / "run-summary.json"
    if not run_summary_path.exists():
        raise SystemExit(f"Missing run summary: {run_summary_path}")

    run_summary = read_json(run_summary_path)

    all_image_paths: List[Path] = []
    job_images: Dict[str, List[Path]] = {}
    for job in run_summary.get("jobs", []):
        candidate_dir = REPO_ROOT / job["candidate_dir"]
        image_paths = list_candidate_images(candidate_dir, job.get("downloaded_files", []))
        job_key = f"{job['filename']}::{job['candidate_label']}"
        job_images[job_key] = image_paths
        all_image_paths.extend(image_paths)

    hash_counts: Dict[str, int] = defaultdict(int)
    for image_path in all_image_paths:
        hash_counts[compute_file_hash(image_path)] += 1

    grouped_candidates: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    score_summary: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest": repo_relative(manifest_path),
        "run_dir": repo_relative(run_dir),
        "requires_manual_truth_check": True,
        "jobs": [],
    }

    for job in run_summary.get("jobs", []):
        job_key = f"{job['filename']}::{job['candidate_label']}"
        image_reports = [
            analyze_image(image_path, job.get("format", ""), hash_counts) for image_path in job_images[job_key]
        ]
        image_reports.sort(key=lambda item: item["score"], reverse=True)

        candidate_report = {
            "asset_id": job["asset_id"],
            "filename": job["filename"],
            "candidate_label": job["candidate_label"],
            "variant_index": job["variant_index"],
            "seed": job["seed"],
            "status": job["status"],
            "candidate_dir": job["candidate_dir"],
            "prompt_id": job.get("prompt_id"),
            "images": image_reports,
            "best_image": image_reports[0]["path"] if image_reports else None,
            "score": image_reports[0]["score"] if image_reports else 0.0,
            "flags": flatten_flags(image_reports) if image_reports else ["missing_outputs"],
        }

        candidate_dir = REPO_ROOT / job["candidate_dir"]
        write_json(candidate_dir / "score-report.json", candidate_report)
        grouped_candidates[job["filename"]].append(candidate_report)

    for filename, candidates in grouped_candidates.items():
        candidates.sort(key=lambda item: item["score"], reverse=True)
        score_summary["jobs"].append(
            {
                "filename": filename,
                "asset_id": candidates[0]["asset_id"] if candidates else None,
                "recommended_variant": candidates[0]["candidate_label"] if candidates else None,
                "recommended_score": candidates[0]["score"] if candidates else 0.0,
                "candidates": candidates,
            }
        )

    score_summary["jobs"].sort(key=lambda item: item["filename"])
    output_path = Path(args.output).expanduser().resolve() if args.output else run_dir / "score-summary.json"
    write_json(output_path, score_summary)
    print(f"Score summary written to: {output_path}")
    return 0


def writeback_manifest(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = load_manifest(manifest_path)
    run_dir = (
        Path(args.run_dir).expanduser().resolve()
        if args.run_dir
        else find_latest_run_dir(manifest["product"]["slug"])
    )
    score_summary_path = (
        Path(args.score_summary).expanduser().resolve()
        if args.score_summary
        else run_dir / "score-summary.json"
    )

    records = build_writeback_records(
        manifest,
        run_dir=run_dir,
        state=args.state,
        selected_jobs=args.jobs,
        validation_status=args.validation_status,
        score_summary_path=score_summary_path,
    )
    if not records:
        raise SystemExit("No matching jobs found to write back.")

    product_paths = load_product_paths(manifest["product"]["slug"])
    status_updated, status_added = update_status_tracker(
        product_paths.status_tracker,
        records,
        dry_run=args.dry_run,
    )
    register_updated, register_added = update_selected_assets_register(
        product_paths.selected_assets_register,
        records,
        dry_run=args.dry_run,
    )

    mode = "Previewed" if args.dry_run else "Updated"
    print(
        f"{mode} status tracker: {product_paths.status_tracker} "
        f"(updated {status_updated}, added {status_added})"
    )
    print(
        f"{mode} selected assets register: {product_paths.selected_assets_register} "
        f"(updated {register_updated}, added {register_added})"
    )
    return 0


def require_pillow(command_name: str) -> None:
    if Image is None or ImageFilter is None:
        raise SystemExit(
            f"Pillow is required for {command_name}. Install the existing Python requirements before using `{command_name}`."
        )


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def parse_box_arg(value: str) -> Tuple[int, int, int, int]:
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 4:
        raise SystemExit("Crop boxes must use left,top,right,bottom.")

    try:
        left, top, right, bottom = (int(part) for part in parts)
    except ValueError as exc:
        raise SystemExit("Crop boxes must contain integers only.") from exc

    if right <= left or bottom <= top:
        raise SystemExit("Crop boxes must satisfy right > left and bottom > top.")
    return left, top, right, bottom


def parse_size_arg(value: str) -> Tuple[int, int]:
    normalized = value.lower().replace("x", ",")
    parts = [part.strip() for part in normalized.split(",") if part.strip()]
    if len(parts) != 2:
        raise SystemExit("Sizes must use WIDTHxHEIGHT.")

    try:
        width, height = (int(part) for part in parts)
    except ValueError as exc:
        raise SystemExit("Sizes must contain integers only.") from exc

    if width <= 0 or height <= 0:
        raise SystemExit("Sizes must be positive.")
    return width, height


def sanitize_stem(path: Path) -> str:
    return normalize_slug(path.stem.replace("_", " "))


def report_path(path: Optional[Path]) -> Optional[str]:
    if path is None:
        return None
    try:
        return repo_relative(path)
    except ValueError:
        return str(path)


def knockout_white_background(
    image: "Image.Image",
    white_threshold: int,
    rolloff: int,
    blur_radius: float,
) -> Tuple["Image.Image", "Image.Image"]:
    rgba = image.convert("RGBA")
    pixels = list(rgba.getdata())
    alpha_values: List[int] = []
    safe_rolloff = max(1, rolloff)
    cutoff = clamp(float(white_threshold), 0.0, 255.0)

    for red, green, blue, _ in pixels:
        brightness = (red + green + blue) / 3.0
        if brightness >= cutoff:
            alpha = 0
        elif brightness <= cutoff - safe_rolloff:
            alpha = 255
        else:
            alpha = int(((cutoff - brightness) / safe_rolloff) * 255)
        alpha_values.append(alpha)

    alpha_mask = Image.new("L", rgba.size)
    alpha_mask.putdata(alpha_values)
    if blur_radius > 0:
        alpha_mask = alpha_mask.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    cutout = rgba.copy()
    cutout.putalpha(alpha_mask)
    return cutout, alpha_mask


def expand_bbox(
    bbox: Tuple[int, int, int, int], image_size: Tuple[int, int], padding: int
) -> Tuple[int, int, int, int]:
    left, top, right, bottom = bbox
    width, height = image_size
    return (
        max(0, left - padding),
        max(0, top - padding),
        min(width, right + padding),
        min(height, bottom + padding),
    )


def fit_size_within(bounds: Tuple[int, int], canvas_size: Tuple[int, int]) -> Tuple[int, int]:
    src_width, src_height = bounds
    max_width, max_height = canvas_size
    if src_width <= 0 or src_height <= 0:
        raise SystemExit("Invalid subject dimensions for compositing.")

    scale = min(max_width / src_width, max_height / src_height)
    target_width = max(1, int(round(src_width * scale)))
    target_height = max(1, int(round(src_height * scale)))
    return target_width, target_height


def centered_canvas(
    subject: "Image.Image", canvas_size: Tuple[int, int], background: Tuple[int, int, int, int]
) -> "Image.Image":
    canvas = Image.new("RGBA", canvas_size, background)
    x_pos = (canvas_size[0] - subject.width) // 2
    y_pos = (canvas_size[1] - subject.height) // 2
    canvas.alpha_composite(subject, (x_pos, y_pos))
    return canvas


def prepare_reference_pack(args: argparse.Namespace) -> int:
    require_pillow("prepare-reference")
    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Reference image not found: {input_path}")

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else DEFAULT_REFERENCE_PREP_DIR / sanitize_stem(input_path)
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    source = Image.open(input_path).convert("RGBA")
    crop_box = parse_box_arg(args.crop_box) if args.crop_box else (0, 0, source.width, source.height)
    cropped = source.crop(crop_box)
    cutout, alpha_mask = knockout_white_background(
        cropped,
        white_threshold=args.white_threshold,
        rolloff=args.rolloff,
        blur_radius=args.blur_radius,
    )

    bbox = alpha_mask.getbbox()
    if bbox is None:
        raise SystemExit("Could not detect a non-white subject in the reference image.")

    padded_bbox = expand_bbox(bbox, cutout.size, args.tight_padding)
    tight_cutout = cutout.crop(padded_bbox)
    tight_mask = alpha_mask.crop(padded_bbox)

    canvas_width, canvas_height = parse_size_arg(args.canvas_size)
    inner_bounds = (
        max(1, canvas_width - (args.canvas_padding * 2)),
        max(1, canvas_height - (args.canvas_padding * 2)),
    )
    fit_width, fit_height = fit_size_within((tight_cutout.width, tight_cutout.height), inner_bounds)
    resample = getattr(Image, "Resampling", Image)
    resized_cutout = tight_cutout.resize((fit_width, fit_height), resample.LANCZOS)
    resized_mask = tight_mask.resize((fit_width, fit_height), resample.LANCZOS)

    centered_transparent = centered_canvas(resized_cutout, (canvas_width, canvas_height), (0, 0, 0, 0))
    centered_white = centered_canvas(resized_cutout, (canvas_width, canvas_height), (255, 255, 255, 255)).convert("RGB")
    centered_mask = Image.new("L", (canvas_width, canvas_height), 0)
    mask_x = (canvas_width - resized_mask.width) // 2
    mask_y = (canvas_height - resized_mask.height) // 2
    centered_mask.paste(resized_mask, (mask_x, mask_y))

    transparent_path = output_dir / "subject-cutout.png"
    mask_path = output_dir / "subject-mask.png"
    centered_transparent_path = output_dir / "subject-centered.png"
    centered_white_path = output_dir / "subject-centered-white.png"
    centered_mask_path = output_dir / "subject-centered-mask.png"
    metadata_path = output_dir / "reference-prep.json"

    tight_cutout.save(transparent_path)
    tight_mask.save(mask_path)
    centered_transparent.save(centered_transparent_path)
    centered_white.save(centered_white_path)
    centered_mask.save(centered_mask_path)

    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": report_path(input_path),
        "output_dir": report_path(output_dir),
        "crop_box": {"left": crop_box[0], "top": crop_box[1], "right": crop_box[2], "bottom": crop_box[3]},
        "detected_bbox": {"left": bbox[0], "top": bbox[1], "right": bbox[2], "bottom": bbox[3]},
        "padded_bbox": {
            "left": padded_bbox[0],
            "top": padded_bbox[1],
            "right": padded_bbox[2],
            "bottom": padded_bbox[3],
        },
        "white_threshold": args.white_threshold,
        "rolloff": args.rolloff,
        "blur_radius": args.blur_radius,
        "canvas_size": {"width": canvas_width, "height": canvas_height},
        "canvas_padding": args.canvas_padding,
        "artifacts": {
            "subject_cutout": report_path(transparent_path),
            "subject_mask": report_path(mask_path),
            "subject_centered": report_path(centered_transparent_path),
            "subject_centered_white": report_path(centered_white_path),
            "subject_centered_mask": report_path(centered_mask_path),
        },
    }
    write_json(metadata_path, metadata)
    print(f"Prepared reference pack: {output_dir}")
    return 0


def load_mask_image(path: Path, size: Tuple[int, int]) -> "Image.Image":
    mask_image = Image.open(path).convert("L")
    if mask_image.size != size:
        resample = getattr(Image, "Resampling", Image)
        mask_image = mask_image.resize(size, resample.LANCZOS)
    return mask_image


def composite_hybrid_render(args: argparse.Namespace) -> int:
    require_pillow("composite")
    background_path = Path(args.background).expanduser().resolve()
    foreground_path = Path(args.foreground).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    mask_path = Path(args.mask).expanduser().resolve() if args.mask else None

    if not background_path.exists():
        raise SystemExit(f"Background image not found: {background_path}")
    if not foreground_path.exists():
        raise SystemExit(f"Foreground image not found: {foreground_path}")
    if mask_path and not mask_path.exists():
        raise SystemExit(f"Mask image not found: {mask_path}")

    background = Image.open(background_path).convert("RGBA")
    foreground = Image.open(foreground_path).convert("RGBA")
    target_height = max(1, int(round(background.height * args.fit_height_ratio)))
    target_width = max(1, int(round(foreground.width * (target_height / foreground.height))))
    resample = getattr(Image, "Resampling", Image)
    resized_foreground = foreground.resize((target_width, target_height), resample.LANCZOS)

    if mask_path:
        foreground_mask = load_mask_image(mask_path, resized_foreground.size)
        resized_foreground.putalpha(foreground_mask)
    else:
        foreground_mask = resized_foreground.getchannel("A")

    if args.anchor == "center":
        x_pos = (background.width - resized_foreground.width) // 2
        y_pos = (background.height - resized_foreground.height) // 2
    else:
        x_pos = (background.width - resized_foreground.width) // 2
        y_pos = background.height - resized_foreground.height

    x_pos += args.x_offset
    y_pos += args.y_offset

    composite = background.copy()
    if args.shadow_opacity > 0 and args.shadow_blur > 0:
        shadow_alpha = foreground_mask.point(
            lambda value: int(clamp((value / 255.0) * args.shadow_opacity, 0.0, 255.0))
        )
        shadow_layer = Image.new("RGBA", resized_foreground.size, (0, 0, 0, 0))
        shadow_layer.putalpha(shadow_alpha)
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=args.shadow_blur))
        composite.alpha_composite(
            shadow_layer,
            (x_pos + args.shadow_offset_x, y_pos + args.shadow_offset_y),
        )

    composite.alpha_composite(resized_foreground, (x_pos, y_pos))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    composite.convert("RGB").save(output_path)

    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "background": report_path(background_path),
        "foreground": report_path(foreground_path),
        "mask": report_path(mask_path),
        "output": report_path(output_path),
        "fit_height_ratio": args.fit_height_ratio,
        "anchor": args.anchor,
        "offsets": {"x": args.x_offset, "y": args.y_offset},
        "shadow": {
            "opacity": args.shadow_opacity,
            "blur": args.shadow_blur,
            "offset_x": args.shadow_offset_x,
            "offset_y": args.shadow_offset_y,
        },
    }
    write_json(output_path.with_suffix(".json"), metadata)
    print(f"Wrote composite image: {output_path}")
    return 0


def collect_run_assets_for_jobs(run_dir: Path) -> Dict[str, List[Dict[str, Any]]]:
    run_summary_path = run_dir / "run-summary.json"
    if not run_summary_path.exists():
        raise SystemExit(f"Missing run summary: {run_summary_path}")

    run_summary = read_json(run_summary_path)
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for run_job in run_summary.get("jobs", []):
        candidate_dir = REPO_ROOT / run_job["candidate_dir"]
        image_paths = [
            report_path(path)
            for path in list_candidate_images(candidate_dir, run_job.get("downloaded_files", []))
        ]
        grouped[run_job["filename"]].append(
            {
                "candidate_label": run_job.get("candidate_label"),
                "candidate_dir": run_job.get("candidate_dir"),
                "prompt_id": run_job.get("prompt_id"),
                "status": run_job.get("status"),
                "images": image_paths,
            }
        )
    return grouped


def render_manual_graphics_brief_markdown(brief: Dict[str, Any]) -> str:
    image_intent = brief.get("image_intent", {})
    lines = [
        f"# Manual Graphics Brief: {brief['filename']}",
        "",
        "## Job",
        f"- Product: {brief['product_name']}",
        f"- Asset ID: {brief['asset_id']}",
        f"- Class: {brief['class']}",
        f"- Lane: {brief['manual_graphics_lane']}",
        f"- Publish target: {brief['publish_target']}",
        "",
        "## Image intent",
        f"- Instructional goal: {image_intent.get('instructional_goal', '')}",
        f"- Visual mode: {image_intent.get('visual_mode', '')}",
        f"- Product slice: {image_intent.get('product_slice', '')}",
        f"- Text truth policy: {image_intent.get('text_truth_policy', '')}",
        f"- Overlay plan: {image_intent.get('overlay_plan', '')}",
        f"- Intent confidence: {image_intent.get('intent_confidence', '')}",
        "",
        "## Manual anchors",
    ]

    matches = image_intent.get("matched_sections", [])
    if matches:
        for match in matches:
            lines.append(
                f"- {match.get('title', '')} [{match.get('semantic_category', '')}] :: {match.get('excerpt', '')}"
            )
    else:
        lines.append("- No manual sections matched; refine manual_section_hints or manual_keywords.")

    lines.extend(
        [
            "",
            "## Editorial tasks",
        ]
    )
    for task in brief.get("editorial_tasks", []):
        lines.append(f"- {task}")

    lines.extend(
        [
            "",
            "## Prompt contract",
            brief.get("resolved_prompt", ""),
            "",
            "## Negative contract",
            brief.get("resolved_negative_prompt", ""),
            "",
            "## References",
            f"- Reference image: {brief.get('reference_image', '')}",
            f"- Visual profile: {brief.get('visual_profile', '')}",
            f"- Manual JSON: {brief.get('manual_json', '')}",
        ]
    )

    run_assets = brief.get("run_assets", [])
    if run_assets:
        lines.extend(["", "## Candidate outputs"])
        for asset in run_assets:
            image_list = ", ".join(asset.get("images", [])) or "no images"
            lines.append(
                f"- {asset.get('candidate_label', 'candidate')} :: {asset.get('status', '')} :: {image_list}"
            )

    return "\n".join(lines).strip() + "\n"


def write_manual_graphics_briefs(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = load_manifest(manifest_path)
    selected_jobs = filter_manifest_jobs(manifest, args.jobs)
    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else DEFAULT_MANUAL_GRAPHICS_DIR / manifest["product"]["slug"]
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    run_assets: Dict[str, List[Dict[str, Any]]] = {}
    run_dir = Path(args.run_dir).expanduser().resolve() if args.run_dir else None
    if run_dir:
        run_assets = collect_run_assets_for_jobs(run_dir)

    for job in selected_jobs:
        if "image_intent" not in job or "manual_graphics_lane" not in job:
            raise SystemExit(
                "Manifest is missing strict image intent metadata. Re-export the manifest before creating a manual graphics brief."
            )

        brief = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "manifest": report_path(manifest_path),
            "run_dir": report_path(run_dir),
            "product_name": manifest["product"]["name"],
            "product_slug": manifest["product"]["slug"],
            "reference_image": manifest["product"]["reference_image"],
            "visual_profile": manifest["product"]["visual_profile"],
            "manual_json": manifest["product"].get("manual_json"),
            "filename": job["filename"],
            "asset_id": job.get("asset_id"),
            "class": job.get("class"),
            "publish_target": job.get("publish_target"),
            "manual_graphics_lane": job.get("manual_graphics_lane"),
            "image_intent": job.get("image_intent", {}),
            "editorial_tasks": job.get("editorial_tasks", []),
            "prompt_contract_fields": job.get("prompt_contract_fields", {}),
            "base_prompt": job.get("base_prompt", ""),
            "resolved_prompt": job.get("prompt", ""),
            "resolved_negative_prompt": job.get("negative_prompt", ""),
            "run_assets": run_assets.get(job["filename"], []),
        }
        json_path = output_dir / f"{job['filename']}-manual-graphics-brief.json"
        markdown_path = output_dir / f"{job['filename']}-manual-graphics-brief.md"
        write_json(json_path, brief)
        write_text(markdown_path, render_manual_graphics_brief_markdown(brief))
        print(f"Wrote manual graphics brief: {json_path}")
        print(f"Wrote manual graphics brief: {markdown_path}")

    return 0


def main() -> int:
    load_local_env(LOCAL_ENV_PATH)
    args = build_parser().parse_args()

    if args.command == "export":
        return export_manifests(args.products, Path(args.output).expanduser().resolve())
    if args.command == "run":
        return run_manifest(args)
    if args.command == "score":
        return score_manifest(args)
    if args.command == "writeback":
        return writeback_manifest(args)
    if args.command == "prepare-reference":
        return prepare_reference_pack(args)
    if args.command == "composite":
        return composite_hybrid_render(args)
    if args.command == "manual-graphics-brief":
        return write_manual_graphics_briefs(args)

    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())