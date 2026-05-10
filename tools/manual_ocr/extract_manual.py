#!/usr/bin/env python3
"""OCR ingestion pipeline for scanned/image-based product manuals."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


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

HEADING_PATTERN = re.compile(
    r"^(?:\d+(?:\.\d+)*[\.)]?\s+)?[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-/(),]{2,}$"
)
STEP_PATTERN = re.compile(r"^(?:paso\s*)?\d+[\).:-]\s+", re.IGNORECASE)
SPEC_PATTERN = re.compile(r"^([A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-/().]{2,60}):\s+(.+)$")


@dataclass
class Section:
    title: str
    content: list[str]


@dataclass
class ManualStructure:
    source_pdf: str
    scanned_pdf: bool
    pages: int
    sections: list[dict[str, Any]]
    specifications: list[dict[str, str]]
    steps: list[str]
    app_instructions: list[str]


def require_dependencies() -> None:
    missing = []
    if fitz is None:
        missing.append("pymupdf")
    if pytesseract is None:
        missing.append("pytesseract")
    if convert_from_path is None:
        missing.append("pdf2image")
    if Image is None or ImageFilter is None or ImageOps is None:
        missing.append("pillow")
    if missing:
        raise RuntimeError(
            "Missing Python dependencies: "
            + ", ".join(sorted(set(missing)))
            + ". Install with: pip install -r requirements.txt"
        )


def list_input_pdfs(input_path: Path) -> list[Path]:
    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        return [input_path]
    if input_path.is_dir():
        return sorted(p for p in input_path.rglob("*.pdf") if p.is_file())
    return []


def detect_scanned_pdf(pdf_path: Path, min_text_chars: int = 300) -> tuple[bool, int, int]:
    if fitz is None:
        return True, 0, 0

    with fitz.open(pdf_path) as doc:
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


def run_ocrmypdf(input_pdf: Path, output_pdf: Path, language: str, force_ocr: bool) -> bool:
    if shutil.which("ocrmypdf") is None:
        return False

    cmd = ["ocrmypdf", "--skip-text", "--optimize", "1", "-l", language]
    if force_ocr:
        cmd = ["ocrmypdf", "--force-ocr", "--optimize", "1", "-l", language]
    cmd += [str(input_pdf), str(output_pdf)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(f"ocrmypdf failed for {input_pdf.name}: {stderr}")
    return True


def preprocess_image(image: "Image.Image") -> "Image.Image":
    gray = ImageOps.grayscale(image)
    contrast = ImageOps.autocontrast(gray)
    denoised = contrast.filter(ImageFilter.MedianFilter(size=3))
    thresholded = denoised.point(lambda px: 255 if px > 150 else 0)
    return thresholded


def extract_text_with_ocr(pdf_path: Path, image_output_dir: Path, dpi: int, language: str) -> list[str]:
    pages = convert_from_path(str(pdf_path), dpi=dpi)
    ocr_pages: list[str] = []

    for index, page in enumerate(pages, start=1):
        cleaned = preprocess_image(page)
        image_path = image_output_dir / f"page_{index:03d}.png"
        cleaned.save(image_path)
        text = pytesseract.image_to_string(cleaned, lang=language, config="--psm 6")
        ocr_pages.append(text)

    return ocr_pages


def extract_text_native(pdf_path: Path) -> list[str]:
    if fitz is None:
        return []

    pages_text: list[str] = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pages_text.append(page.get_text("text") or "")
    return pages_text


def clean_ocr_noise(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"\n +", "\n", text)
    return text.strip()


def normalize_spacing(lines: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for line in lines:
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            normalized.append(line)
    return normalized


def detect_sections(lines: list[str]) -> list[Section]:
    sections: list[Section] = [Section(title="Contenido", content=[])]

    for line in lines:
        if len(line) <= 110 and (HEADING_PATTERN.match(line) or line.isupper()):
            sections.append(Section(title=line.title(), content=[]))
            continue
        sections[-1].content.append(line)

    return [section for section in sections if section.content or section.title != "Contenido"]


def detect_specification_tables(lines: list[str]) -> list[dict[str, str]]:
    specs: list[dict[str, str]] = []
    for line in lines:
        match = SPEC_PATTERN.match(line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            if len(key.split()) <= 6 and value:
                specs.append({"name": key, "value": value})
    return specs


def preserve_ordered_steps(lines: list[str]) -> list[str]:
    return [line for line in lines if STEP_PATTERN.match(line)]


def detect_app_instructions(lines: list[str]) -> list[str]:
    keywords = ("app", "aplicación", "bluetooth", "wifi", "emparejar", "pair")
    return [line for line in lines if any(keyword in line.lower() for keyword in keywords)]


def build_markdown(sections: list[Section], specs: list[dict[str, str]], steps: list[str]) -> str:
    md_lines: list[str] = []
    for section in sections:
        md_lines.append(f"## {section.title}")
        md_lines.append("")
        for line in section.content:
            if STEP_PATTERN.match(line):
                md_lines.append(f"- [ ] {line}")
            else:
                md_lines.append(line)
        md_lines.append("")

    if specs:
        md_lines.extend(["## Especificaciones", "", "| Campo | Valor |", "|---|---|"])
        for spec in specs:
            md_lines.append(f"| {spec['name']} | {spec['value']} |")
        md_lines.append("")

    if steps:
        md_lines.extend(["## Pasos detectados", ""])
        for step in steps:
            md_lines.append(f"1. {step}")
        md_lines.append("")

    return "\n".join(md_lines).strip() + "\n"


def build_json_structure(
    source_pdf: Path,
    scanned_pdf: bool,
    page_count: int,
    sections: list[Section],
    specs: list[dict[str, str]],
    steps: list[str],
    app_instructions: list[str],
) -> ManualStructure:
    return ManualStructure(
        source_pdf=str(source_pdf),
        scanned_pdf=scanned_pdf,
        pages=page_count,
        sections=[{"title": section.title, "content": section.content} for section in sections],
        specifications=specs,
        steps=steps,
        app_instructions=app_instructions,
    )


def write_outputs(
    output_dir: Path,
    raw_text: str,
    markdown: str,
    structured: ManualStructure,
    skip_json: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manual_raw.txt").write_text(raw_text, encoding="utf-8")
    (output_dir / "manual.md").write_text(markdown, encoding="utf-8")
    if not skip_json:
        (output_dir / "manual.json").write_text(
            json.dumps(asdict(structured), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def process_manual(
    input_pdf: Path,
    output_root: Path,
    dpi: int,
    language: str,
    force_ocr: bool,
    skip_json: bool,
    batch_mode: bool,
) -> None:
    scanned, pages, text_chars = detect_scanned_pdf(input_pdf)
    manual_output = output_root / input_pdf.stem if batch_mode else output_root

    image_output_dir = manual_output / "extracted_images"
    image_output_dir.mkdir(parents=True, exist_ok=True)

    searchable_pdf = manual_output / f"{input_pdf.stem}.searchable.pdf"
    ocr_source_pdf = input_pdf

    if scanned or force_ocr:
        used_ocrmypdf = run_ocrmypdf(input_pdf, searchable_pdf, language, force_ocr)
        if used_ocrmypdf:
            ocr_source_pdf = searchable_pdf

    if scanned or force_ocr:
        pages_text = extract_text_with_ocr(ocr_source_pdf, image_output_dir, dpi=dpi, language=language)
    else:
        pages_text = extract_text_native(ocr_source_pdf)
    raw_text = clean_ocr_noise("\n\n".join(pages_text))

    lines = normalize_spacing(raw_text.splitlines())
    sections = detect_sections(lines)
    specs = detect_specification_tables(lines)
    steps = preserve_ordered_steps(lines)
    app_instructions = detect_app_instructions(lines)

    markdown = build_markdown(sections, specs, steps)
    structured = build_json_structure(
        input_pdf,
        scanned or force_ocr,
        pages or len(pages_text),
        sections,
        specs,
        steps,
        app_instructions,
    )

    write_outputs(manual_output, raw_text, markdown, structured, skip_json)

    print(
        f"✓ {input_pdf.name}: scanned={scanned} text_chars={text_chars} "
        f"-> {manual_output}"
    )


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

    try:
        require_dependencies()
        pdfs = list_input_pdfs(input_path)
        if not pdfs:
            raise FileNotFoundError(f"No PDF files found in: {input_path}")

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
            except Exception as exc:  # pragma: no cover - operational error handling
                print(f"✗ Failed processing {pdf}: {exc}", file=sys.stderr)

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
