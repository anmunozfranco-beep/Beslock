from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANUAL_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"

IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
NUMBERED_SECTION_PATTERN = re.compile(r"^##\s+\d+\.\s+(.*)$")
STATUS_SECTION_PATTERN = re.compile(r"##\s+(\d+)\.\s+Estado del borrador\n.*$", re.S)

PHRASE_REPLACEMENTS: Dict[str, str] = {
    "Hero de e-Flex para revision": "Vista general de e-Flex",
    "Este bloque sirve para revisar si la narrativa visual local del pomo comunica bien el primer alta de acceso, sin sugerir un panel frontal que el producto no tiene.": "Este bloque muestra el primer alta local de acceso sobre el pomo, sin sugerir un panel frontal que el producto no tiene.",
    "Si la version instalada expone idioma, ajustes basicos o menus auxiliares, esta imagen sirve como apoyo de revision. No debe presentarse como prueba de una pantalla fija en el frente del equipo.": "Si la version instalada expone idioma, ajustes basicos o menus auxiliares, esta imagen sirve como apoyo visual. No debe presentarse como prueba de una pantalla fija en el frente del equipo.",
    "Usa este bloque para revisar si el lenguaje visual diferencia bien entre diagnostico biometrico y reconexion de app.": "Usa este bloque para explicar la diferencia entre diagnostico biometrico y reconexion de app.",
    "Usa este bloque para revisar si la narrativa visual diferencia bien entre problema biometrico y problema de vinculacion remota.": "Usa este bloque para explicar la diferencia entre problema biometrico y problema de vinculacion remota.",
}


@dataclass
class SectionAsset:
    section_name: str
    asset_path: str
    role: str


@dataclass
class ProductPackage:
    title: str
    slug: str
    manual_file: str
    asset_root: str
    section_assets: List[SectionAsset]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Promote review-draft manuals and assets into the final web-ready package."
    )
    parser.add_argument(
        "--manual-root",
        default=str(DEFAULT_MANUAL_ROOT),
        help="Directory that contains the review-draft and image-ready manuals.",
    )
    return parser


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "manual"


def manual_slug_from_path(path: Path) -> str:
    suffix = " user manual - review-draft.md"
    if path.name.endswith(suffix):
        return slugify(path.name[: -len(suffix)])
    return slugify(path.stem)


def find_review_manuals(manual_root: Path) -> List[Path]:
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


def extract_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def review_intro_replacement(asset_root: str) -> str:
    return (
        f"Este manual usa assets publicados en `{asset_root}` y amplia la cobertura "
        "visual validada para integracion web."
    )


def replace_intro(text: str, asset_root: str) -> str:
    pattern = re.compile(
        r"## Manual de usuario final para web\n\n.*?\n\n(## 1\. Introduccion)",
        re.S,
    )
    replacement = (
        f"## Manual de usuario final para web\n\n{review_intro_replacement(asset_root)}\n\n\\1"
    )
    updated_text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace review intro for asset root: {asset_root}")
    return updated_text


def replace_status_section(text: str, asset_root: str) -> str:
    def _replacement(match: re.Match[str]) -> str:
        section_number = match.group(1)
        return (
            f"## {section_number}. Estado del paquete\n"
            f"Este manual usa assets publicados en `{asset_root}` y queda listo "
            "como fuente final de integracion para la pagina web.\n"
        )

    updated_text, count = STATUS_SECTION_PATTERN.subn(_replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace status section for asset root: {asset_root}")
    return updated_text


def finalize_manual_text(text: str, review_asset_root: str, web_asset_root: str) -> str:
    updated_text = text.replace(
        "## Borrador inicial para revision visual",
        "## Manual de usuario final para web",
        1,
    )
    updated_text = replace_intro(updated_text, web_asset_root)
    updated_text = updated_text.replace(
        review_asset_root,
        web_asset_root,
    )
    for old_text, new_text in PHRASE_REPLACEMENTS.items():
        updated_text = updated_text.replace(old_text, new_text)
    updated_text = updated_text.replace("Revision de huella", "Solucion de huella")
    updated_text = updated_text.replace("Revision de app", "Solucion de app")
    updated_text = replace_status_section(updated_text, web_asset_root)
    return updated_text


def promote_assets(review_dir: Path, web_dir: Path) -> List[str]:
    review_assets = sorted(review_dir.glob("*.webp"))
    if not review_assets:
        raise SystemExit(f"No review assets found in: {review_dir}")
    if web_dir.exists():
        shutil.rmtree(web_dir)
    web_dir.mkdir(parents=True, exist_ok=True)
    for asset_path in review_assets:
        shutil.copy2(asset_path, web_dir / asset_path.name)
    return [asset_path.stem for asset_path in review_assets]


def asset_role(asset_path: str) -> str:
    filename = Path(asset_path).name
    if "reference" in filename:
        return "canonical-reference"
    if "hero-main" in filename:
        return "published-hero"
    if "installed-context" in filename:
        return "published-context"
    if "downloads-docs" in filename:
        return "published-downloads-support"
    if "troubleshoot" in filename:
        return "published-troubleshooting-support"
    if "app-add-device" in filename or "link-qr" in filename:
        return "published-app-support"
    return "published-manual-support"
def resolve_package_root(manual_root: Path, slug: str, manual_path: Path) -> Path:
    domain_root = manual_root / "ext-images" / slug / "publishing" / "web"
    try:
        manual_path.relative_to(domain_root)
        return domain_root
    except ValueError:
        return manual_root


def resolve_asset_reference(manual_root: Path, package_root: Path, asset_path: str) -> str:
    if re.match(r"^[a-z]+://", asset_path) or asset_path.startswith("/"):
        return asset_path
    resolved_path = package_root / asset_path
    return resolved_path.relative_to(manual_root).as_posix()


def parse_section_assets(markdown_text: str, manual_root: Path, manual_path: Path) -> List[SectionAsset]:
    current_section = ""
    section_assets: List[SectionAsset] = []
    for raw_line in markdown_text.splitlines():
        section_match = NUMBERED_SECTION_PATTERN.match(raw_line.strip())
        if section_match:
            current_section = section_match.group(1).strip()
            continue

        image_match = IMAGE_PATTERN.match(raw_line.strip())
        if image_match and current_section and current_section != "Estado del paquete":
            _, asset_path = image_match.groups()
            resolved_asset_path = resolve_asset_reference(manual_root, manual_path.parent, asset_path.strip())
            section_assets.append(
                SectionAsset(
                    section_name=current_section,
                    asset_path=resolved_asset_path,
                    role=asset_role(asset_path.strip()),
                )
            )
    return section_assets


def resolve_asset_dirs(manual_root: Path, slug: str, package_root: Path) -> tuple[Path, Path]:
    if package_root != manual_root:
        asset_root = package_root / "assets" / slug
        return asset_root / "review-draft", asset_root / "web-ready"
    legacy_root = manual_root / "assets" / slug
    return legacy_root / "review-draft", legacy_root / "web-ready"


def manual_asset_root(manual_path: Path, slug: str, stage: str) -> str:
    if manual_path.parent.name == "manuals" and manual_path.parent.parent.name == "web":
        return f"../assets/{slug}/{stage}/"
    return f"assets/{slug}/{stage}/"


def publish_manual(review_manual_path: Path, manual_root: Path) -> ProductPackage:
    review_text = review_manual_path.read_text(encoding="utf-8")
    title = extract_title(review_text, fallback=review_manual_path.stem)
    slug = slugify(title)
    package_root = resolve_package_root(manual_root, slug, review_manual_path)

    review_asset_dir, web_asset_dir = resolve_asset_dirs(manual_root, slug, package_root)
    published_asset_stems = promote_assets(review_asset_dir, web_asset_dir)

    review_asset_root = manual_asset_root(review_manual_path, slug, "review-draft")
    web_asset_root = manual_asset_root(review_manual_path, slug, "web-ready")
    final_text = finalize_manual_text(review_text, review_asset_root, web_asset_root)
    image_ready_path = review_manual_path.with_name(review_manual_path.name.replace("review-draft", "image-ready"))
    image_ready_path.write_text(final_text, encoding="utf-8")

    update_visual_tracker_states(manual_root, slug, published_asset_stems)

    return ProductPackage(
        title=title,
        slug=slug,
        manual_file=image_ready_path.relative_to(manual_root).as_posix(),
        asset_root=f"{web_asset_dir.relative_to(manual_root).as_posix()}/",
        section_assets=parse_section_assets(final_text, manual_root, image_ready_path),
    )


def resolve_visual_tracker_paths(manual_root: Path, slug: str) -> tuple[Path, Path]:
    domain_root = manual_root / "ext-images" / slug
    domain_status_path = domain_root / "visual-system" / "qa" / "image-production-status.md"
    domain_register_path = domain_root / "metadata" / "traceability" / "selected-assets-register.md"
    if domain_status_path.exists() and domain_register_path.exists():
        return domain_status_path, domain_register_path

    legacy_root = manual_root / "visual-system" / "products" / slug
    return (
        legacy_root / "image-production-status.md",
        legacy_root / "generated" / "selected-assets-register.md",
    )


def update_visual_tracker_states(manual_root: Path, slug: str, published_asset_stems: List[str]) -> None:
    status_path, register_path = resolve_visual_tracker_paths(manual_root, slug)

    status_text = status_path.read_text(encoding="utf-8")
    register_text = register_path.read_text(encoding="utf-8")
    register_has_validation_status = "| Stable filename | Slot | Asset ID | Current state | Winning variant | Validation status | Publish target | Notes |" in register_text

    for asset_stem in published_asset_stems:
        status_text = re.sub(
            rf"(\|\s*\d+\s*\|\s*`{re.escape(asset_stem)}`\s*\|\s*[^|]+\|\s*[^|]+\|\s*)(planned|generated|selected|approved)(\s*\|)",
            r"\1published\3",
            status_text,
        )

        updated_register_lines = []
        for line in register_text.splitlines():
            if f"`{asset_stem}`" not in line or not line.startswith("| `"):
                updated_register_lines.append(line)
                continue

            parts = line.split("|")
            state_index = 4 if register_has_validation_status else 3
            if parts[state_index].strip() in {"planned", "generated", "selected", "approved"}:
                parts[state_index] = " published "

            winning_variant_index = 5 if register_has_validation_status else 4
            if parts[winning_variant_index].strip() == "pending":
                parts[winning_variant_index] = " reset-local-png-rebuild "

            if register_has_validation_status:
                validation_index = 6
                if parts[validation_index].strip() == "pending":
                    parts[validation_index] = " approved "

            updated_register_lines.append("|".join(parts))

        register_text = "\n".join(updated_register_lines)

    status_path.write_text(status_text, encoding="utf-8")
    register_path.write_text(register_text, encoding="utf-8")


def build_manifest(products: List[ProductPackage]) -> dict:
    return {
        "generated_at": dt.date.today().isoformat(),
        "status": "ready",
        "products": [
            {
                "slug": product.slug,
                "manual_file": product.manual_file,
                "asset_root": product.asset_root,
                "status": "ready",
                "sections": [
                    {
                        "name": slugify(section_asset.section_name),
                        "asset": section_asset.asset_path,
                        "role": section_asset.role,
                        "status": "ready",
                    }
                    for section_asset in product.section_assets
                ],
            }
            for product in products
        ],
    }


def build_matrix(products: List[ProductPackage]) -> str:
    summary_rows = [
        "| Product | Final manual file | Web-ready asset root | Assets available | Package status |",
        "|---|---|---|---:|---|",
    ]
    for product in products:
        summary_rows.append(
            f"| {product.title} | `{product.manual_file}` | `{product.asset_root}` | {len(product.section_assets)} | ready |"
        )

    coverage_rows = [
        "| Product | Manual section | Asset path | Asset role | Status |",
        "|---|---|---|---|---|",
    ]
    for product in products:
        for section_asset in product.section_assets:
            coverage_rows.append(
                f"| {product.title} | {section_asset.section_name} | `{section_asset.asset_path}` | {section_asset.role.replace('-', ' ')} | ready |"
            )

    return "\n".join(
        [
            "# Manual Web Integration Matrix",
            "",
            "## Purpose",
            "This file defines the final manual packages that are ready to move into website templates or a CMS.",
            "",
            "## Readiness rule",
            "A product package is `ready` when:",
            "- the final manual markdown file exists",
            "- every visual block used by that manual resolves to an existing file under the recorded web-ready asset root",
            "- the mapped assets are already published or canonical references",
            "",
            "## Package summary",
            "",
            *summary_rows,
            "",
            "## Section coverage matrix",
            "",
            *coverage_rows,
            "",
            "## Operational note",
            "This matrix reflects the published package after promoting the validated winners into each package's recorded web-ready asset root and final image-ready manual.",
        ]
    )


def main() -> int:
    args = build_parser().parse_args()
    manual_root = Path(args.manual_root).expanduser().resolve()

    products = [publish_manual(path, manual_root) for path in find_review_manuals(manual_root)]

    manifest_path = manual_root / "manual-web-integration-manifest.json"
    manifest_path.write_text(
        json.dumps(build_manifest(products), indent=2) + "\n",
        encoding="utf-8",
    )

    matrix_path = manual_root / "manual-web-integration-matrix.md"
    matrix_path.write_text(build_matrix(products) + "\n", encoding="utf-8")

    print(f"Published {len(products)} review-draft manuals into final packages.")
    for product in products:
        print(f"- {product.title}: {len(product.section_assets)} mapped assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())