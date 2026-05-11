#!/usr/bin/env python3
"""OCR ingestion pipeline for scanned/image-based product manuals.

Supports:
  - Automatic scanned/image PDF detection
  - OCR via OCRmyPDF (preferred), pdf2image+pytesseract (fallback), or PyMuPDF native
  - Robust logging and per-stage exception handling
  - Clean markdown and structured JSON output
  - Automatic extraction quality report
"""

from __future__ import annotations

import argparse
import io
import json
import logging
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# Optional dependency imports (graceful fallback if not installed)
# ---------------------------------------------------------------------------

try:
    import fitz  # type: ignore
except ImportError:  # pragma: no cover - runtime dependency
    fitz = None

try:
    import pytesseract  # type: ignore
except ImportError:  # pragma: no cover - runtime dependency
    pytesseract = None

try:
    from pdf2image import convert_from_path  # type: ignore
except ImportError:  # pragma: no cover - runtime dependency
    convert_from_path = None

try:
    from PIL import Image, ImageFilter, ImageOps  # type: ignore
except ImportError:  # pragma: no cover - runtime dependency
    Image = None
    ImageFilter = None
    ImageOps = None

# ---------------------------------------------------------------------------
# Patterns for structure detection
# ---------------------------------------------------------------------------

HEADING_PATTERN = re.compile(
    r"^(?:\d+(?:\.\d+)*[\.)]?\s+)?[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-/(),]{2,}$"
)
# Matches either "Paso 1:", "Step 2." style lines or parenthesized "(1)" step markers.
STEP_PATTERN = re.compile(r"^(?:(?:step|paso)\s*)?\d+[\).:-]\s+|^\(\d+\)\s+", re.IGNORECASE)
SPEC_PATTERN = re.compile(r"^([A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-/().]{2,60}):\s+(.+)$")
WARNING_PATTERN = re.compile(
    r"\b(warning|caution|danger|note|important|advertencia|precaución|peligro|nota)\b",
    re.IGNORECASE,
)
FEATURE_PATTERN = re.compile(r"^[\-\*\•]\s+.{10,}")
PAGE_NUMBER_PATTERN = re.compile(r"^\d{1,3}$")
SUSPICIOUS_SYMBOL_PATTERN = re.compile(r"[+|<>{}\[\]~`_\\]")
# Keep multilingual keyword coverage for current manuals (English + Spanish).
TROUBLESHOOTING_KEYWORDS = ("troubleshoot", "error", "problem", "issue", "fallo", "problema")
HEADING_KEYWORDS = (
    "manual",
    "instal",
    "config",
    "oper",
    "paso",
    "introdu",
    "parámetro",
    "spec",
    "app",
    "bluetooth",
    "gateway",
    "troubleshoot",
    "warning",
    "nota",
)
STEP_ACTION_KEYWORDS = (
    "install",
    "instale",
    "instalar",
    "presione",
    "pulse",
    "abra",
    "open",
    "gire",
    "ingrese",
    "introduzca",
    "conecte",
    "ajuste",
    "descargue",
    "toque",
    "seleccione",
    "siga",
    "active",
    "mantenga",
    "haga clic",
)
SPEC_KEYWORD_HINTS = (
    "modelo",
    "material",
    "tamaño",
    "grosor",
    "tipo",
    "vida",
    "capacidad",
    "longitud",
    "tasa",
    "temperatura",
    "corriente",
    "humedad",
    "voltaje",
    "tensión",
    "alimentación",
    "energía",
    "suministro",
    "bater",
    "consumo",
    "protecci",
)
PROTECTED_SHORT_KEYWORDS = ("paso", "step", "app")
MAX_SHORT_LINE_LENGTH = 8
MAX_SHORT_ALPHA_CHARS = 4
MIN_TOKENS_FOR_RATIO_CHECK = 4
MAX_SINGLE_CHAR_RATIO = 0.5
MAX_SHORT_TOKEN_RATIO = 0.75
MAX_TOTAL_CHARS_SHORT_TOKENS = 12
MIN_ALPHA_RATIO_WITH_SYMBOLS = 0.7
MIN_LENGTH_FOR_ALPHA_CHECK = 10
MIN_ALPHA_RATIO_LONG_LINE = 0.45
MAX_SPEC_VALUE_WORDS = 22
SPEC_UNITS_PATTERN = re.compile(r"(?:°c|°f|mm|cm|kg|mah|ah|ma|ua|rh|%|usb|aa|kv)\b", re.IGNORECASE)
# Character-density heuristic (avg chars/page -> confidence) used when OCR engines
# do not expose confidence scores (e.g., OCRmyPDF + native text extraction path).
TEXT_CONFIDENCE_THRESHOLDS: tuple[tuple[int, float], ...] = (
    (1200, 92.0),
    (700, 88.0),
    (300, 80.0),
)
MIN_TEXT_CONFIDENCE = 70.0
REQUIRED_SECTION_SPECS = "Technical Specifications"
REQUIRED_SECTION_STEPS = "Setup Steps"
REQUIRED_SECTION_APP = "App Instructions"

# Product-manual keyword sets for section matching
SECTION_KEYWORDS: dict[str, list[str]] = {
    "Installation": ["install", "mount", "wiring", "instalación", "montaje", "cableado"],
    "Configuration": ["config", "setup", "setting", "configurar", "ajuste", "parámetro"],
    "Operation": ["operation", "use", "open", "unlock", "apertura", "operación", "uso"],
    "Specifications": ["specification", "parameter", "especificación", "parámetro técnico"],
    "App Instructions": ["app", "application", "bluetooth", "wifi", "pair", "aplicación", "emparejar"],
    "Warnings": ["warning", "caution", "danger", "advertencia", "precaución", "peligro"],
    "Troubleshooting": ["troubleshoot", "error", "problem", "solución", "problema", "fallo"],
    "Maintenance": ["battery", "clean", "batería", "limpieza", "mantenimiento"],
    "Features": ["feature", "function", "característica", "función", "capacidad"],
}

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Section:
    title: str
    content: list[str]
    semantic_category: str = "General"


@dataclass
class OcrMethodResult:
    method: str
    success: bool
    pages_processed: int
    avg_confidence: float
    error: str = ""


@dataclass
class ManualStructure:
    source_pdf: str
    scanned_pdf: bool
    pages: int
    ocr_method: str
    avg_confidence: float
    sections: list[dict[str, Any]]
    specifications: list[dict[str, str]]
    steps: list[str]
    app_instructions: list[str]
    troubleshooting: list[str]
    warnings: list[str]
    features: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def setup_logging(log_file: Path | None = None) -> logging.Logger:
    logger = logging.getLogger("manual_ocr")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    logger.propagate = False
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


# Module-level logger (replaced per-run in process_manual)
_log: logging.Logger = logging.getLogger("manual_ocr")


# ---------------------------------------------------------------------------
# Dependency checks
# ---------------------------------------------------------------------------


def check_dependencies() -> dict[str, bool]:
    """Return availability map for each optional dependency."""
    return {
        "pymupdf": fitz is not None,
        "pytesseract": pytesseract is not None,
        "pdf2image": convert_from_path is not None,
        "pillow": Image is not None,
        "ocrmypdf": shutil.which("ocrmypdf") is not None,
        "tesseract": shutil.which("tesseract") is not None,
        "pdftoppm": shutil.which("pdftoppm") is not None,
    }


def require_minimum_dependencies(deps: dict[str, bool]) -> None:
    """Raise if we cannot do OCR at all."""
    can_ocr = (
        deps["pymupdf"]
        and (deps["pdf2image"] or deps["pdftoppm"])
        and deps["pytesseract"]
        and deps["tesseract"]
        and deps["pillow"]
    )
    can_native = deps["pymupdf"]
    if not can_ocr and not can_native:
        raise RuntimeError(
            "Insufficient dependencies. Need at minimum: pymupdf + pillow + "
            "(pdf2image/pdftoppm) + pytesseract + tesseract binary. "
            "Install with: pip install -r requirements.txt && "
            "apt-get install tesseract-ocr poppler-utils"
        )


# ---------------------------------------------------------------------------
# PDF discovery
# ---------------------------------------------------------------------------


def list_input_pdfs(input_path: Path) -> list[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        return [input_path]
    if input_path.is_dir():
        return sorted(p for p in input_path.rglob("*.pdf") if p.is_file())
    return []


def slug_from_pdf_name(pdf_name: str) -> str:
    """Build stable product slugs from manual PDF names."""
    base = re.sub(r"\.pdf$", "", pdf_name, flags=re.IGNORECASE).strip()
    base = re.sub(r"\buser\s*manual\b", "", base, flags=re.IGNORECASE).strip()
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base.lower()).strip("-")
    return base or "manual"


# ---------------------------------------------------------------------------
# Scanned PDF detection
# ---------------------------------------------------------------------------


def detect_scanned_pdf(pdf_path: Path, min_text_chars: int = 300) -> tuple[bool, int, int]:
    """Return (is_scanned, page_count, total_text_chars)."""
    if fitz is None:
        return True, 0, 0

    with fitz.open(str(pdf_path)) as doc:
        pages = len(doc)
        text_chars = 0
        image_pages = 0

        for page in doc:
            text = page.get_text("text") or ""
            text_chars += len(text.strip())
            if page.get_images(full=True):
                image_pages += 1

    scanned = text_chars < min_text_chars or image_pages >= max(1, pages // 2)
    return scanned, pages, text_chars


# ---------------------------------------------------------------------------
# OCR methods
# ---------------------------------------------------------------------------


def run_ocrmypdf(
    input_pdf: Path, output_pdf: Path, language: str, force_ocr: bool
) -> OcrMethodResult:
    """Attempt OCR via ocrmypdf. Returns result descriptor."""
    if shutil.which("ocrmypdf") is None:
        return OcrMethodResult("ocrmypdf", False, 0, 0.0, "ocrmypdf binary not found")

    cmd = ["ocrmypdf", "--skip-text", "--optimize", "1", "-l", language]
    if force_ocr:
        cmd = ["ocrmypdf", "--force-ocr", "--optimize", "1", "-l", language]
    cmd += [str(input_pdf), str(output_pdf)]

    _log.debug("Running: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        err = result.stderr.strip()
        _log.warning("ocrmypdf failed (rc=%d): %s", result.returncode, err)
        return OcrMethodResult("ocrmypdf", False, 0, 0.0, err)

    _log.info("ocrmypdf succeeded → %s", output_pdf.name)
    return OcrMethodResult("ocrmypdf", True, 0, 0.0)


def preprocess_image(image: "Image.Image") -> "Image.Image":
    """Grayscale + autocontrast + denoise + threshold for better OCR accuracy."""
    gray = ImageOps.grayscale(image)
    contrast = ImageOps.autocontrast(gray)
    denoised = contrast.filter(ImageFilter.MedianFilter(size=3))
    thresholded = denoised.point(lambda px: 255 if px > 150 else 0)
    return thresholded


def _render_pages_with_fitz(pdf_path: Path, dpi: int) -> list["Image.Image"]:
    """Render PDF pages to PIL images using PyMuPDF (avoids poppler dependency)."""
    if fitz is None or Image is None:
        return []
    scale = dpi / 72.0
    mat = fitz.Matrix(scale, scale)
    images: list[Image.Image] = []
    with fitz.open(str(pdf_path)) as doc:
        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            images.append(Image.open(io.BytesIO(img_bytes)))
    return images


def extract_text_with_ocr(
    pdf_path: Path,
    image_output_dir: Path,
    dpi: int,
    language: str,
) -> tuple[list[str], float]:
    """Extract text via pdf2image+pytesseract (or fitz render fallback).

    Returns (pages_text, avg_confidence).
    """
    if pytesseract is None:
        raise RuntimeError("pytesseract not available")

    # Try pdf2image first, fall back to fitz rendering
    pages: list[Image.Image] = []
    if convert_from_path is not None:
        try:
            _log.debug("Converting PDF to images with pdf2image at %d DPI", dpi)
            pages = convert_from_path(str(pdf_path), dpi=dpi)
        except Exception as exc:
            _log.warning("pdf2image failed (%s); falling back to fitz rendering", exc)

    if not pages:
        _log.debug("Using fitz rendering as image source at %d DPI", dpi)
        pages = _render_pages_with_fitz(pdf_path, dpi)

    if not pages:
        raise RuntimeError("Could not render PDF pages for OCR")

    ocr_pages: list[str] = []
    all_confs: list[float] = []

    for index, page in enumerate(pages, start=1):
        _log.debug("OCR page %d/%d", index, len(pages))
        cleaned = preprocess_image(page)
        image_path = image_output_dir / f"page_{index:03d}.png"
        cleaned.save(image_path)

        # Collect confidence alongside text
        try:
            data = pytesseract.image_to_data(
                cleaned, lang=language, config="--psm 6", output_type=pytesseract.Output.DICT
            )
            confs = [float(c) for c in data["conf"] if c != -1 and float(c) >= 0]
            if confs:
                all_confs.extend(confs)
        except Exception:
            pass

        text = pytesseract.image_to_string(cleaned, lang=language, config="--psm 6")
        ocr_pages.append(text)

    avg_conf = sum(all_confs) / len(all_confs) if all_confs else 0.0
    return ocr_pages, avg_conf


def extract_text_native(pdf_path: Path) -> list[str]:
    """Extract embedded text directly with PyMuPDF (text-based PDFs only)."""
    if fitz is None:
        return []

    pages_text: list[str] = []
    with fitz.open(str(pdf_path)) as doc:
        for page in doc:
            pages_text.append(page.get_text("text") or "")
    return pages_text


def estimate_text_confidence(pages_text: list[str]) -> float:
    """Estimate confidence from average non-empty characters per page."""
    non_empty_pages = [page for page in pages_text if (page or "").strip()]
    if not non_empty_pages:
        return 0.0
    total_chars = sum(len(page.strip()) for page in non_empty_pages)
    avg_chars_per_page = total_chars / len(non_empty_pages)
    for min_chars_per_page, confidence in TEXT_CONFIDENCE_THRESHOLDS:
        if avg_chars_per_page >= min_chars_per_page:
            return confidence
    return MIN_TEXT_CONFIDENCE


# ---------------------------------------------------------------------------
# Text cleaning and normalization
# ---------------------------------------------------------------------------


def clean_ocr_noise(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"\n +", "\n", text)
    # Remove isolated single-character lines (common OCR noise), then re-collapse
    text = re.sub(r"(?m)^[^a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ\n]{1,2}$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_spacing(lines: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for line in lines:
        line = re.sub(r"\s+", " ", line).strip()
        if line and not is_noise_line(line):
            normalized.append(line)
    return normalized


def is_noise_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if PAGE_NUMBER_PATTERN.fullmatch(stripped):
        return True
    if re.fullmatch(r"[\W_]+", stripped):
        return True
    alnum = 0
    alpha = 0
    for ch in stripped:
        if ch.isalpha():
            alpha += 1
            alnum += 1
        elif ch.isalnum():
            alnum += 1
    if alnum < 2:
        return True
    if len(stripped) <= 3 and alpha <= 1 and not stripped.isdigit():
        return True
    if SUSPICIOUS_SYMBOL_PATTERN.search(stripped) and alpha < 6:
        return True
    stripped_lower = stripped.lower()
    if (
        len(stripped) <= MAX_SHORT_LINE_LENGTH
        and alpha <= MAX_SHORT_ALPHA_CHARS
        and not any(k in stripped_lower for k in PROTECTED_SHORT_KEYWORDS)
    ):
        return True
    tokens = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+", stripped)
    if tokens:
        single_char_tokens = sum(1 for t in tokens if len(t) == 1)
        if len(tokens) >= MIN_TOKENS_FOR_RATIO_CHECK:
            single_char_ratio = single_char_tokens / len(tokens)
            if single_char_ratio > MAX_SINGLE_CHAR_RATIO:
                return True
        short_tokens = sum(1 for t in tokens if len(t) <= 2)
        if (
            len(tokens) >= MIN_TOKENS_FOR_RATIO_CHECK
            and short_tokens / len(tokens) >= MAX_SHORT_TOKEN_RATIO
            and sum(len(t) for t in tokens) <= MAX_TOTAL_CHARS_SHORT_TOKENS
        ):
            return True
    if not STEP_PATTERN.match(stripped) and not SPEC_PATTERN.match(stripped):
        alpha_ratio = alpha / max(len(stripped), 1)
        if SUSPICIOUS_SYMBOL_PATTERN.search(stripped) and alpha_ratio < MIN_ALPHA_RATIO_WITH_SYMBOLS:
            return True
        if len(stripped) >= MIN_LENGTH_FOR_ALPHA_CHECK and alpha_ratio < MIN_ALPHA_RATIO_LONG_LINE:
            return True
    return False


def dedupe_preserve_order(lines: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for line in lines:
        key = line.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(line)
    return deduped


# ---------------------------------------------------------------------------
# Structure detection
# ---------------------------------------------------------------------------


def _classify_section(title: str) -> str:
    title_lower = title.lower()
    for category, keywords in SECTION_KEYWORDS.items():
        if any(kw in title_lower for kw in keywords):
            return category
    return "General"


def _is_probable_heading(line: str) -> bool:
    if STEP_PATTERN.match(line):
        return False
    if is_noise_line(line):
        return False
    if SPEC_PATTERN.match(line):
        return False
    if len(line) < 4 or len(line) > 110:
        return False
    words = line.split()
    if len(words) > 14:
        return False
    alpha_chars = sum(1 for ch in line if ch.isalpha())
    if alpha_chars < 3:
        return False
    line_lower = line.lower()
    numbered_heading = bool(re.match(r"^\d+(?:\.\d+)*\s+[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", line))
    has_keyword = any(kw in line_lower for kw in HEADING_KEYWORDS)
    if numbered_heading and len(words) < 3 and not has_keyword:
        return False
    if ":" in line and not numbered_heading and not has_keyword:
        return False
    if not (numbered_heading or has_keyword or line.isupper()):
        return False
    return bool(HEADING_PATTERN.match(line) or line.isupper() or numbered_heading)


def detect_sections(lines: list[str]) -> list[Section]:
    sections: list[Section] = [Section(title="Overview", content=[], semantic_category="General")]

    for line in lines:
        if _is_probable_heading(line):
            cat = _classify_section(line)
            sections.append(Section(title=line.title(), content=[], semantic_category=cat))
            continue
        sections[-1].content.append(line)

    filtered = [s for s in sections if s.content]
    if not filtered and lines:
        return [Section(title="Overview", content=lines, semantic_category="General")]
    return filtered


def detect_specification_tables(lines: list[str]) -> list[dict[str, str]]:
    specs: list[dict[str, str]] = []
    for line in lines:
        match = SPEC_PATTERN.match(line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            key_lower = key.lower()
            value_lower = value.lower()
            value_words = len(value.split())
            has_numeric = bool(re.search(r"\d", value))
            has_unit = bool(SPEC_UNITS_PATTERN.search(value_lower))
            key_hint = any(hint in key_lower for hint in SPEC_KEYWORD_HINTS)
            if key_lower in {"nota", "note", "atención", "attention", "administrador", "tecla"}:
                continue
            if len(key.split()) > 8 or not value:
                continue
            if value_words > MAX_SPEC_VALUE_WORDS:
                continue
            if not (has_numeric or has_unit or key_hint):
                continue
            specs.append({"name": key, "value": value})
    unique: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for spec in specs:
        key = (spec["name"].lower(), spec["value"].lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(spec)
    return unique


def preserve_ordered_steps(lines: list[str]) -> list[str]:
    steps: list[str] = []
    for line in lines:
        if not STEP_PATTERN.match(line):
            continue
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in STEP_ACTION_KEYWORDS):
            steps.append(line)
    return dedupe_preserve_order(steps)


def detect_app_instructions(lines: list[str]) -> list[str]:
    keywords = ("app", "aplicación", "bluetooth", "wifi", "emparejar", "pair", "application")
    return dedupe_preserve_order([line for line in lines if any(kw in line.lower() for kw in keywords)])


def detect_warnings(lines: list[str]) -> list[str]:
    return dedupe_preserve_order([line for line in lines if WARNING_PATTERN.search(line)])


def detect_features(lines: list[str]) -> list[str]:
    feature_keywords = ("función", "feature", "modo", "alarma", "bluetooth", "wifi", "seguridad")
    features: list[str] = []
    for line in lines:
        if not FEATURE_PATTERN.match(line):
            continue
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in feature_keywords):
            features.append(line)
    return dedupe_preserve_order(features)


def detect_troubleshooting(lines: list[str]) -> list[str]:
    matches: list[str] = []
    for line in lines:
        line_lower = line.lower()
        if any(kw in line_lower for kw in TROUBLESHOOTING_KEYWORDS):
            matches.append(line)
    return dedupe_preserve_order(matches)


# ---------------------------------------------------------------------------
# Output builders
# ---------------------------------------------------------------------------


def build_markdown(
    sections: list[Section],
    specs: list[dict[str, str]],
    steps: list[str],
    warnings: list[str],
    features: list[str],
    app_instructions: list[str],
    troubleshooting: list[str],
    source_name: str,
    ocr_method: str,
    avg_confidence: float,
) -> str:
    """Generate AI-ready markdown from extracted content."""
    md_lines: list[str] = [
        f"# {source_name}",
        "",
        f"> **OCR method:** {ocr_method}  ",
        f"> **Confidence:** {avg_confidence:.1f}%  ",
        f"> **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "---",
        "",
    ]

    for section in sections:
        heading_prefix = "##"
        md_lines.append(f"{heading_prefix} {section.title}")
        md_lines.append("")
        for line in section.content:
            if STEP_PATTERN.match(line):
                md_lines.append(f"- [ ] {line}")
            elif WARNING_PATTERN.search(line):
                md_lines.append(f"> ⚠️ {line}")
            else:
                md_lines.append(line)
        md_lines.append("")

    if features:
        md_lines.extend(["## Features", ""])
        for feat in features:
            md_lines.append(f"- {feat.lstrip('-*• ').strip()}")
        md_lines.append("")

    if specs:
        md_lines.extend(["## Technical Specifications", "", "| Parameter | Value |", "|---|---|"])
        for spec in specs:
            md_lines.append(f"| {spec['name']} | {spec['value']} |")
        md_lines.append("")

    if steps:
        md_lines.extend(["## Setup Steps", ""])
        for i, step in enumerate(steps, start=1):
            md_lines.append(f"{i}. {step}")
        md_lines.append("")

    if app_instructions:
        md_lines.extend(["## App Setup", ""])
        for i, line in enumerate(app_instructions, start=1):
            md_lines.append(f"{i}. {line}")
        md_lines.append("")

    if warnings:
        md_lines.extend(["## Warnings & Notes", ""])
        for w in warnings:
            md_lines.append(f"> ⚠️ {w}")
        md_lines.append("")

    if troubleshooting:
        md_lines.extend(["## Troubleshooting", ""])
        for i, line in enumerate(troubleshooting, start=1):
            md_lines.append(f"{i}. {line}")
        md_lines.append("")

    return "\n".join(md_lines).strip() + "\n"


def build_json_structure(
    source_pdf: Path,
    scanned_pdf: bool,
    page_count: int,
    ocr_method: str,
    avg_confidence: float,
    sections: list[Section],
    specs: list[dict[str, str]],
    steps: list[str],
    app_instructions: list[str],
    troubleshooting: list[str],
    warnings: list[str],
    features: list[str],
) -> ManualStructure:
    return ManualStructure(
        source_pdf=str(source_pdf),
        scanned_pdf=scanned_pdf,
        pages=page_count,
        ocr_method=ocr_method,
        avg_confidence=round(avg_confidence, 1),
        sections=[
            {
                "title": s.title,
                "semantic_category": s.semantic_category,
                "content": s.content,
            }
            for s in sections
        ],
        specifications=specs,
        steps=steps,
        app_instructions=app_instructions,
        troubleshooting=troubleshooting,
        warnings=warnings,
        features=features,
        metadata={
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "downstream_use": ["woocommerce", "technical_manual", "faq", "installation_guide"],
        },
    )


def _quality_label(avg_confidence: float, total_chars: int) -> str:
    if avg_confidence >= 85 and total_chars > 500:
        return "Good"
    if avg_confidence >= 70 and total_chars > 200:
        return "Acceptable"
    if total_chars > 100:
        return "Poor"
    return "Failed"


def build_extraction_report(
    source_pdf: Path,
    scanned_pdf: bool,
    page_count: int,
    ocr_method_results: list[OcrMethodResult],
    final_method: str,
    avg_confidence: float,
    sections: list[Section],
    total_chars: int,
    warnings: list[str],
    specs: list[dict[str, str]],
    steps: list[str],
    app_instructions: list[str],
    troubleshooting: list[str],
) -> str:
    """Generate a markdown extraction quality report."""
    quality = _quality_label(avg_confidence, total_chars)
    detected_cats = sorted({s.semantic_category for s in sections if s.semantic_category != "General"})
    missing_required = []
    if not specs:
        missing_required.append(REQUIRED_SECTION_SPECS)
    if not steps:
        missing_required.append(REQUIRED_SECTION_STEPS)
    if not app_instructions:
        missing_required.append(REQUIRED_SECTION_APP)

    lines: list[str] = [
        "# Extraction Report",
        "",
        f"**Source file:** `{source_pdf.name}`  ",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Summary",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| PDF type | {'Scanned / image-based' if scanned_pdf else 'Text-based'} |",
        f"| Pages processed | {page_count} |",
        f"| Final OCR method | {final_method} |",
        f"| Average OCR confidence | {avg_confidence:.1f}% |",
        f"| Extraction quality | **{quality}** |",
        f"| Total text characters | {total_chars:,} |",
        f"| Sections detected | {len(sections)} |",
        f"| Specifications detected | {len(specs)} |",
        f"| Setup steps detected | {len(steps)} |",
        f"| Warning notes detected | {len(warnings)} |",
        "",
        "## OCR Methods Attempted",
        "",
    ]

    for r in ocr_method_results:
        status = "✅ Success" if r.success else "❌ Failed"
        lines.append(f"- **{r.method}**: {status}" + (f" — {r.error}" if r.error else ""))

    lines += [
        "",
        "## Detected Semantic Sections",
        "",
    ]
    if detected_cats:
        for cat in detected_cats:
            lines.append(f"- {cat}")
    else:
        lines.append("- (no specific categories detected)")

    lines += [
        "",
        "## Section Index",
        "",
    ]
    for i, s in enumerate(sections, start=1):
        lines.append(f"{i}. **{s.title}** ({s.semantic_category}) — {len(s.content)} lines")

    lines += [
        "",
        "## Quality Notes",
        "",
    ]
    if quality == "Good":
        lines.append("- Extraction quality is good. The content should be usable for manual generation.")
    elif quality == "Acceptable":
        lines.append("- Extraction quality is acceptable. Some manual review may be needed in dense or noisy areas.")
    elif quality == "Poor":
        lines.append("- Extraction quality is poor. Manual correction of the raw text is recommended before use.")
    else:
        lines.append("- Extraction failed or produced no usable text. Try a higher DPI or a different OCR engine.")

    if avg_confidence < 70:
        lines.append("- Low OCR confidence detected. Consider rescanning or improving image quality.")
    if not specs:
        lines.append("- No technical specification table was automatically detected.")
    if not steps:
        lines.append("- No numbered setup steps were automatically detected.")
    if troubleshooting:
        lines.append(f"- Troubleshooting candidates detected: {len(troubleshooting)}.")
    if missing_required:
        lines.append("- Missing expected sections: " + ", ".join(missing_required) + ".")

    lines += [
        "",
        "## Downstream Readiness",
        "",
        "Generated artifacts are organized for use in:",
        "",
        "- **WooCommerce product pages** — use `manual.json` `.specifications` and `.sections`",
        "- **Technical manuals** — use `manual.md` as a structured draft base",
        "- **FAQs** — extract from `manual.json` `.sections` with category `Troubleshooting`",
        "- **Installation guides** — extract from `manual.json` `.sections` with category `Installation`",
        "",
    ]

    return "\n".join(lines)


def write_outputs(
    output_dir: Path,
    raw_text: str,
    markdown: str,
    structured: ManualStructure,
    report: str,
    skip_json: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manual_raw.txt").write_text(raw_text, encoding="utf-8")
    (output_dir / "manual.md").write_text(markdown, encoding="utf-8")
    (output_dir / "extraction_report.md").write_text(report, encoding="utf-8")
    if not skip_json:
        (output_dir / "manual.json").write_text(
            json.dumps(asdict(structured), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# ---------------------------------------------------------------------------
# Main processing entry point
# ---------------------------------------------------------------------------


def process_manual(
    input_pdf: Path,
    output_root: Path,
    dpi: int,
    language: str,
    force_ocr: bool,
    skip_json: bool,
    batch_mode: bool,
) -> None:
    global _log

    manual_output = output_root / slug_from_pdf_name(input_pdf.name) if batch_mode else output_root
    log_file = manual_output / "extraction.log"
    _log = setup_logging(log_file)

    _log.info("=== Processing: %s ===", input_pdf.name)

    deps = check_dependencies()
    _log.debug("Dependency status: %s", deps)
    require_minimum_dependencies(deps)

    # --- Detection ---
    _log.info("Detecting PDF type...")
    try:
        scanned, pages, text_chars = detect_scanned_pdf(input_pdf)
    except Exception as exc:
        _log.warning("PDF detection failed (%s); assuming scanned", exc)
        scanned, pages, text_chars = True, 0, 0

    _log.info("PDF type: %s | pages=%d | text_chars=%d", "scanned" if scanned else "text-based", pages, text_chars)

    image_output_dir = manual_output / "extracted_images"
    image_output_dir.mkdir(parents=True, exist_ok=True)

    method_results: list[OcrMethodResult] = []
    ocr_pages: list[str] = []
    avg_confidence = 0.0
    final_method = "native"

    # --- OCR pipeline ---
    if scanned or force_ocr:

        # Stage 1: OCRmyPDF
        searchable_pdf = manual_output / f"{input_pdf.stem}.searchable.pdf"
        ocrmypdf_result = run_ocrmypdf(input_pdf, searchable_pdf, language, force_ocr)
        method_results.append(ocrmypdf_result)
        ocr_source = searchable_pdf if ocrmypdf_result.success and searchable_pdf.exists() else input_pdf

        if ocrmypdf_result.success and searchable_pdf.exists():
            _log.info("OCRmyPDF succeeded; extracting text from searchable PDF")
            try:
                ocr_pages = extract_text_native(searchable_pdf)
                avg_confidence = estimate_text_confidence(ocr_pages)
                final_method = "ocrmypdf"
                pages = pages or len(ocr_pages)
                method_results.append(
                    OcrMethodResult("ocrmypdf_native_text", True, len(ocr_pages), avg_confidence)
                )
            except Exception as exc:
                _log.warning(
                    "Searchable PDF text extraction failed for %s: %s",
                    searchable_pdf.name,
                    exc,
                )
                ocr_pages = []
                method_results.append(OcrMethodResult("ocrmypdf_native_text", False, 0, 0.0, str(exc)))

        # Stage 2 fallback: pdf2image + pytesseract
        if not ocr_pages and deps["pytesseract"] and deps["tesseract"]:
            _log.info("Running fallback pdf2image+pytesseract OCR on %s...", ocr_source.name)
            try:
                ocr_pages, avg_confidence = extract_text_with_ocr(
                    ocr_source, image_output_dir, dpi=dpi, language=language
                )
                final_method = "pytesseract"
                pages = pages or len(ocr_pages)
                _log.info("pytesseract OCR complete: %d pages, avg_conf=%.1f%%", len(ocr_pages), avg_confidence)
                method_results.append(
                    OcrMethodResult("pytesseract", True, len(ocr_pages), avg_confidence)
                )
            except Exception as exc:
                _log.warning("pytesseract OCR failed: %s", exc)
                method_results.append(OcrMethodResult("pytesseract", False, 0, 0.0, str(exc)))

        # Stage 3: PyMuPDF native fallback (for partially text PDFs)
        if not ocr_pages:
            _log.info("Falling back to PyMuPDF native text extraction...")
            try:
                ocr_pages = extract_text_native(input_pdf)
                final_method = "pymupdf_native"
                avg_confidence = estimate_text_confidence(ocr_pages)
                pages = pages or len(ocr_pages)
                _log.info("Native extraction complete: %d pages", len(ocr_pages))
                method_results.append(
                    OcrMethodResult("pymupdf_native", True, len(ocr_pages), avg_confidence)
                )
            except Exception as exc:
                _log.error("PyMuPDF native extraction also failed: %s", exc)
                method_results.append(OcrMethodResult("pymupdf_native", False, 0, 0.0, str(exc)))

    else:
        # Text-based PDF: direct native extraction
        _log.info("Text-based PDF — using native PyMuPDF extraction")
        try:
            ocr_pages = extract_text_native(input_pdf)
            final_method = "pymupdf_native"
            avg_confidence = estimate_text_confidence(ocr_pages)
            pages = pages or len(ocr_pages)
            method_results.append(OcrMethodResult("pymupdf_native", True, len(ocr_pages), avg_confidence))
        except Exception as exc:
            _log.error("Native extraction failed: %s", exc)
            method_results.append(OcrMethodResult("pymupdf_native", False, 0, 0.0, str(exc)))

    if not ocr_pages:
        _log.error("All extraction methods failed. No text could be extracted.")

    # --- Post-processing ---
    raw_text = clean_ocr_noise("\n\n".join(ocr_pages))
    total_chars = len(raw_text)
    _log.info("Raw text: %d characters after cleaning", total_chars)

    lines = normalize_spacing(raw_text.splitlines())
    sections = detect_sections(lines)
    specs = detect_specification_tables(lines)
    steps = preserve_ordered_steps(lines)
    app_instructions = detect_app_instructions(lines)
    troubleshooting = detect_troubleshooting(lines)
    warnings = detect_warnings(lines)
    features = detect_features(lines)

    _log.info(
        "Structure: sections=%d specs=%d steps=%d warnings=%d features=%d app=%d",
        len(sections), len(specs), len(steps), len(warnings), len(features), len(app_instructions),
    )

    # --- Build outputs ---
    markdown = build_markdown(
        sections, specs, steps, warnings, features, app_instructions, troubleshooting,
        source_name=input_pdf.stem.replace("-", " ").title(),
        ocr_method=final_method,
        avg_confidence=avg_confidence,
    )
    structured = build_json_structure(
        input_pdf, scanned or force_ocr, pages, final_method, avg_confidence,
        sections, specs, steps, app_instructions, troubleshooting, warnings, features,
    )
    report = build_extraction_report(
        input_pdf, scanned or force_ocr, pages, method_results, final_method,
        avg_confidence, sections, total_chars, warnings, specs, steps, app_instructions, troubleshooting,
    )

    write_outputs(manual_output, raw_text, markdown, structured, report, skip_json)
    _log.info("Outputs written to: %s", manual_output)
    _log.info(
        "✓ %s: scanned=%s pages=%d avg_confidence=%.1f%% method=%s",
        input_pdf.name, scanned, pages, avg_confidence, final_method,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OCR ingestion workflow for product manual PDFs")
    parser.add_argument("--input", required=True, help="Input PDF file or directory with PDFs")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    parser.add_argument("--dpi", type=int, default=300, help="Image render DPI for OCR")
    parser.add_argument(
        "--language",
        default="spa+eng",
        help="Tesseract language(s), e.g. spa, eng, spa+eng",
    )
    parser.add_argument("--force-ocr", action="store_true", help="Force OCR even for text PDFs")
    parser.add_argument("--skip-json", action="store_true", help="Skip manual.json output")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    pdfs = list_input_pdfs(input_path)
    if not pdfs:
        print(f"Error: No PDF files found in: {input_path}", file=sys.stderr)
        return 1

    exit_code = 0
    for pdf in pdfs:
        try:
            process_manual(
                input_pdf=pdf,
                output_root=output_path,
                dpi=args.dpi,
                language=args.language,
                force_ocr=args.force_ocr,
                skip_json=args.skip_json,
                batch_mode=input_path.is_dir(),
            )
        except Exception as exc:
            print(f"✗ Failed processing {pdf}: {exc}", file=sys.stderr)
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
