#!/usr/bin/env python3
"""Batch OCR-to-markdown pipeline for all manuals in `User manuals/`."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from tools.manual_ocr.extract_manual import list_input_pdfs, process_manual


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process all product manuals to generated_manuals/")
    parser.add_argument("--input", default="User manuals", help="Input directory containing PDF manuals")
    parser.add_argument("--output", default="generated_manuals", help="Output root directory")
    parser.add_argument("--dpi", type=int, default=300, help="OCR DPI")
    parser.add_argument("--language", default="spa+eng", help="Tesseract language(s)")
    parser.add_argument("--force-ocr", action="store_true", help="Force OCR even for text PDFs")
    parser.add_argument("--skip-json", action="store_true", help="Skip JSON output")
    return parser


def write_batch_report(output_dir: Path, successes: list[str], failures: list[dict[str, str]]) -> None:
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "successful_manuals": successes,
        "failed_manuals": failures,
        "success_count": len(successes),
        "failure_count": len(failures),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "batch_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        "# OCR Batch Summary",
        "",
        f"- Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"- Successful manuals: {len(successes)}",
        f"- Failed manuals: {len(failures)}",
        "",
        "## Successful",
        "",
    ]
    if successes:
        lines.extend(f"- {name}" for name in successes)
    else:
        lines.append("- (none)")

    lines += ["", "## Failed", ""]
    if failures:
        for fail in failures:
            lines.append(f"- {fail['file']}: {fail['error']}")
    else:
        lines.append("- (none)")

    (output_dir / "batch_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    pdfs = list_input_pdfs(input_path)
    if not pdfs:
        print(f"No PDF files found in: {input_path}")
        return 1

    successes: list[str] = []
    failures: list[dict[str, str]] = []
    for pdf in pdfs:
        try:
            process_manual(
                input_pdf=pdf,
                output_root=output_path,
                dpi=args.dpi,
                language=args.language,
                force_ocr=args.force_ocr,
                skip_json=args.skip_json,
                batch_mode=True,
            )
            successes.append(pdf.name)
        except Exception as exc:
            failures.append({"file": pdf.name, "error": str(exc)})
            print(f"✗ Failed processing {pdf.name}: {exc}")

    write_batch_report(output_path, successes, failures)
    print(f"Batch complete. Success={len(successes)} Failure={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
