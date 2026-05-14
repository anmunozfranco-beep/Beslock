from __future__ import annotations

import argparse
import html
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANUAL_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
DEFAULT_OUTPUT_DIR = DEFAULT_MANUAL_ROOT / "review-previews"

IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")


@dataclass
class ReviewManual:
    title: str
    source_path: Path
    output_path: Path
    html_body: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render review-draft user manuals into browser-friendly HTML previews."
    )
    parser.add_argument(
        "--manual-root",
        default=str(DEFAULT_MANUAL_ROOT),
        help="Directory that contains the review-draft markdown manuals.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where the HTML previews will be written.",
    )
    return parser


def manual_slug_from_path(path: Path) -> str:
    suffix = " user manual - review-draft.md"
    if path.name.endswith(suffix):
        return slugify(path.name[: -len(suffix)])
    return slugify(path.stem)


def find_manuals(manual_root: Path) -> List[Path]:
    manuals_by_slug = {}
    for path in sorted(manual_root.glob("* user manual - review-draft.md")):
        manuals_by_slug[manual_slug_from_path(path)] = path

    ext_images_root = manual_root / "ext-images"
    if ext_images_root.exists():
        for path in sorted(ext_images_root.glob("*/publishing/web/manuals/* user manual - review-draft.md")):
            manuals_by_slug[manual_slug_from_path(path)] = path

    manuals = [manuals_by_slug[slug] for slug in sorted(manuals_by_slug)]
    if not manuals:
        raise SystemExit(f"No review-draft manuals found in: {manual_root}")
    return manuals


def slugify(stem: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return slug or "manual-review"


def escape_inline(text: str) -> str:
    escaped = html.escape(text, quote=True)
    return INLINE_CODE_PATTERN.sub(lambda match: f"<code>{html.escape(match.group(1), quote=True)}</code>", escaped)


def normalize_asset_path(raw_path: str, source_path: Path, output_dir: Path) -> str:
    stripped = raw_path.strip()
    if re.match(r"^[a-z]+://", stripped) or stripped.startswith("/"):
        return stripped
  target_path = (source_path.parent / stripped).resolve()
  return Path(os.path.relpath(target_path, output_dir)).as_posix()


def render_image(line: str, source_path: Path, output_dir: Path) -> str | None:
    match = IMAGE_PATTERN.fullmatch(line.strip())
    if not match:
        return None
    alt_text, raw_path = match.groups()
  src = normalize_asset_path(raw_path, source_path, output_dir)
    alt = html.escape(alt_text.strip(), quote=True)
    return (
        '<figure class="manual-image">'
      f'<img src="{src}" alt="{alt}" />'
        f'<figcaption>{alt}</figcaption>'
        "</figure>"
    )


def render_list(items: Iterable[str], ordered: bool) -> str:
    tag = "ol" if ordered else "ul"
    rendered_items = "".join(f"<li>{escape_inline(item)}</li>" for item in items)
    return f"<{tag}>{rendered_items}</{tag}>"


def render_markdown(markdown_text: str, source_path: Path, output_dir: Path) -> str:
    lines = markdown_text.splitlines()
    html_parts: List[str] = []
    paragraph_lines: List[str] = []
    unordered_items: List[str] = []
    ordered_items: List[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(line.strip() for line in paragraph_lines)
            html_parts.append(f"<p>{escape_inline(text)}</p>")
            paragraph_lines = []

    def flush_lists() -> None:
        nonlocal unordered_items, ordered_items
        if unordered_items:
            html_parts.append(render_list(unordered_items, ordered=False))
            unordered_items = []
        if ordered_items:
            html_parts.append(render_list(ordered_items, ordered=True))
            ordered_items = []

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_lists()
            continue

        image_html = render_image(stripped, source_path, output_dir)
        if image_html:
            flush_paragraph()
            flush_lists()
            html_parts.append(image_html)
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flush_lists()
            html_parts.append(f"<h2>{escape_inline(stripped[3:])}</h2>")
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            flush_lists()
            html_parts.append(f"<h1>{escape_inline(stripped[2:])}</h1>")
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if ordered_items:
                flush_lists()
            unordered_items.append(stripped[2:].strip())
            continue

        ordered_match = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if ordered_match:
            flush_paragraph()
            if unordered_items:
                flush_lists()
            ordered_items.append(ordered_match.group(2).strip())
            continue

        paragraph_lines.append(stripped)

    flush_paragraph()
    flush_lists()
    return "\n".join(html_parts)


def extract_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def render_document(title: str, body_html: str, source_name: str) -> str:
    escaped_title = html.escape(title, quote=True)
    escaped_source = html.escape(source_name, quote=True)
    return f"""<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{escaped_title} - Review Preview</title>
  <style>
    :root {{
      --paper: #f6f1e6;
      --ink: #13212e;
      --muted: #5d6a73;
      --frame: #dbcdb4;
      --card: #fffdf8;
      --accent: #7a3419;
      --shadow: rgba(19, 33, 46, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(122, 52, 25, 0.10), transparent 28%),
        linear-gradient(180deg, #f3ecdc 0%, var(--paper) 100%);
    }}
    .shell {{
      max-width: 980px;
      margin: 0 auto;
      padding: 32px 20px 64px;
    }}
    .masthead {{
      background: rgba(255, 253, 248, 0.72);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(122, 52, 25, 0.15);
      border-radius: 24px;
      padding: 20px 22px;
      box-shadow: 0 14px 40px var(--shadow);
      margin-bottom: 28px;
    }}
    .masthead a {{
      color: var(--accent);
      text-decoration: none;
      font-size: 0.95rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .masthead p {{
      margin: 10px 0 0;
      color: var(--muted);
    }}
    article {{
      background: var(--card);
      border: 1px solid var(--frame);
      border-radius: 28px;
      padding: 32px;
      box-shadow: 0 18px 44px var(--shadow);
    }}
    h1, h2 {{
      font-weight: 600;
      line-height: 1.12;
      margin: 0 0 16px;
    }}
    h1 {{
      font-size: clamp(2.2rem, 5vw, 3.3rem);
      color: var(--accent);
      margin-bottom: 18px;
    }}
    h2 {{
      font-size: clamp(1.4rem, 3vw, 2rem);
      margin-top: 30px;
      padding-top: 18px;
      border-top: 1px solid rgba(219, 205, 180, 0.9);
    }}
    p, li {{
      font-size: 1.05rem;
      line-height: 1.75;
      margin: 0;
    }}
    p + p {{ margin-top: 12px; }}
    ul, ol {{
      margin: 14px 0 0 24px;
      padding: 0;
      display: grid;
      gap: 8px;
    }}
    code {{
      font-family: "SFMono-Regular", Consolas, monospace;
      background: rgba(19, 33, 46, 0.06);
      padding: 0.12rem 0.38rem;
      border-radius: 6px;
      font-size: 0.94em;
    }}
    .manual-image {{
      margin: 24px 0 0;
      display: grid;
      gap: 10px;
    }}
    .manual-image img {{
      width: 100%;
      border-radius: 20px;
      border: 1px solid rgba(19, 33, 46, 0.08);
      background: #f4efe5;
      box-shadow: 0 18px 34px rgba(19, 33, 46, 0.12);
    }}
    .manual-image figcaption {{
      color: var(--muted);
      font-size: 0.92rem;
    }}
    @media (max-width: 640px) {{
      .shell {{ padding: 18px 14px 42px; }}
      article {{ padding: 22px 18px; border-radius: 22px; }}
      .masthead {{ padding: 16px 18px; border-radius: 18px; }}
    }}
  </style>
</head>
<body>
  <div class=\"shell\">
    <div class=\"masthead\">
      <a href=\"index.html\">Volver al indice de revision</a>
      <p>Fuente: {escaped_source}</p>
    </div>
    <article>
      {body_html}
    </article>
  </div>
</body>
</html>
"""


def render_index(manuals: List[ReviewManual], output_dir: Path) -> str:
    cards = []
    for manual in manuals:
        cards.append(
            """
        <a class=\"card\" href=\"{href}\">
          <span class=\"eyebrow\">Review draft</span>
          <h2>{title}</h2>
          <p>{source}</p>
        </a>
          """.format(
              href=html.escape(manual.output_path.name, quote=True),
              title=html.escape(manual.title, quote=True),
                source=html.escape(manual.source_path.name, quote=True),
            ).strip()
        )

        rendered_cards = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Manual Review Drafts</title>
  <style>
    :root {{
      --bg: #efe4cf;
      --ink: #1a2430;
      --muted: #5f6870;
      --card: rgba(255, 252, 245, 0.78);
      --accent: #8c3d16;
      --border: rgba(140, 61, 22, 0.16);
      --shadow: rgba(26, 36, 48, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top right, rgba(140, 61, 22, 0.10), transparent 30%),
        linear-gradient(180deg, #f7efe1 0%, var(--bg) 100%);
    }}
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 42px 20px 60px;
    }}
    .hero {{
      margin-bottom: 28px;
      padding: 28px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 26px;
      box-shadow: 0 20px 44px var(--shadow);
    }}
    h1 {{
      margin: 0;
      font-size: clamp(2.4rem, 5vw, 3.6rem);
      color: var(--accent);
      line-height: 1.08;
    }}
    .hero p {{
      max-width: 760px;
      font-size: 1.08rem;
      line-height: 1.75;
      color: var(--muted);
      margin: 14px 0 0;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 18px;
    }}
    .card {{
      display: block;
      padding: 22px;
      text-decoration: none;
      color: inherit;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 22px;
      box-shadow: 0 18px 32px var(--shadow);
      transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
    }}
    .card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 24px 40px rgba(26, 36, 48, 0.16);
      border-color: rgba(140, 61, 22, 0.28);
    }}
    .eyebrow {{
      display: inline-block;
      margin-bottom: 10px;
      font-size: 0.82rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
    }}
    .card h2 {{
      margin: 0;
      font-size: 1.6rem;
      line-height: 1.18;
    }}
    .card p {{
      margin: 10px 0 0;
      color: var(--muted);
      line-height: 1.6;
      font-size: 0.98rem;
    }}
  </style>
</head>
<body>
  <main>
    <section class=\"hero\">
      <h1>Manual Review Drafts</h1>
      <p>Paquete de revision del reset visual 2026-05-13: manuales con assets schematicos o hibridos, sin figuras humanas completas y listos para validacion antes de publicacion.</p>
    </section>
    <section class=\"grid\">
      {rendered_cards}
    </section>
  </main>
</body>
</html>
"""


def render_manual_file(markdown_path: Path, output_dir: Path) -> ReviewManual:
    markdown_text = markdown_path.read_text(encoding="utf-8")
    title = extract_title(markdown_text, fallback=markdown_path.stem)
    output_name = f"{slugify(markdown_path.stem)}.html"
    output_path = output_dir / output_name
  html_body = render_markdown(markdown_text, markdown_path, output_dir)
    output_path.write_text(
        render_document(title=title, body_html=html_body, source_name=markdown_path.name),
        encoding="utf-8",
    )
    return ReviewManual(
        title=title,
        source_path=markdown_path,
        output_path=output_path,
        html_body=html_body,
    )


def resolve_output_dir(markdown_path: Path, manual_root: Path, fallback_output_dir: Path) -> Path:
    ext_images_root = manual_root / "ext-images"
    try:
        relative_path = markdown_path.relative_to(ext_images_root)
    except ValueError:
        return fallback_output_dir

    if len(relative_path.parts) >= 4 and relative_path.parts[1:4] == ("publishing", "web", "manuals"):
        slug = relative_path.parts[0]
        return ext_images_root / slug / "publishing" / "web" / "review-previews"
    return fallback_output_dir


def main() -> int:
    args = build_parser().parse_args()
    manual_root = Path(args.manual_root).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    use_default_output_dir = output_dir == DEFAULT_OUTPUT_DIR.resolve()

    grouped_manuals = {}
    rendered_manuals = []
    for path in find_manuals(manual_root):
        target_output_dir = output_dir
        if use_default_output_dir:
            target_output_dir = resolve_output_dir(path, manual_root, output_dir)
        target_output_dir.mkdir(parents=True, exist_ok=True)
        manual = render_manual_file(path, target_output_dir)
        grouped_manuals.setdefault(target_output_dir, []).append(manual)
        rendered_manuals.append(manual)

    print(f"Rendered {len(rendered_manuals)} manual previews across {len(grouped_manuals)} directories.")
    for target_output_dir in sorted(grouped_manuals):
        index_path = target_output_dir / "index.html"
        index_path.write_text(render_index(grouped_manuals[target_output_dir], target_output_dir), encoding="utf-8")
        print(f"Index: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())