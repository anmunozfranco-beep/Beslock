#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import Dict, List, Tuple

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[1]
MANUAL_ROOT = REPO_ROOT / "wp-content/themes/beslock-custom/User manuals"
EXT_IMAGES_ROOT = MANUAL_ROOT / "ext-images"

FORMAT_DIMENSIONS: Dict[str, Tuple[int, int]] = {
    "16:9 horizontal": (1536, 864),
    "4:3 horizontal": (1408, 1056),
    "4:5 vertical": (1024, 1280),
}


@dataclass(frozen=True)
class ProductConfig:
    slug: str
    exterior_side: str
    sensor_point: Tuple[float, float]
    credential_point: Tuple[float, float]
    control_point: Tuple[float, float]


PRODUCTS: Dict[str, ProductConfig] = {
    "e-nova": ProductConfig(
        slug="e-nova",
        exterior_side="right",
        sensor_point=(0.78, 0.43),
        credential_point=(0.60, 0.44),
        control_point=(0.60, 0.44),
    ),
    "e-orbit": ProductConfig(
        slug="e-orbit",
        exterior_side="right",
        sensor_point=(0.52, 0.58),
        credential_point=(0.50, 0.31),
        control_point=(0.50, 0.26),
    ),
    "e-touch": ProductConfig(
        slug="e-touch",
        exterior_side="left",
        sensor_point=(0.23, 0.50),
        credential_point=(0.63, 0.47),
        control_point=(0.50, 0.47),
    ),
    "e-flex": ProductConfig(
        slug="e-flex",
        exterior_side="right",
        sensor_point=(0.79, 0.47),
        credential_point=(0.49, 0.23),
        control_point=(0.49, 0.26),
    ),
    "e-prime": ProductConfig(
        slug="e-prime",
        exterior_side="right",
        sensor_point=(0.52, 0.48),
        credential_point=(0.50, 0.23),
        control_point=(0.50, 0.27),
    ),
    "e-shield": ProductConfig(
        slug="e-shield",
        exterior_side="left",
        sensor_point=(0.50, 0.14),
        credential_point=(0.50, 0.39),
        control_point=(0.50, 0.31),
    ),
}

SLOT_SPECS = {
    "hero-main": {"format": "16:9 horizontal"},
    "installed-context": {"format": "4:3 horizontal"},
    "add-admin-action": {"format": "4:5 vertical"},
    "pin-use": {"format": "4:5 vertical"},
    "fingerprint-use": {"format": "4:5 vertical"},
    "language-settings": {"format": "4:5 vertical"},
    "app-add-device": {"format": "4:3 horizontal"},
    "link-qr": {"format": "4:3 horizontal"},
    "troubleshoot-fingerprint": {"format": "4:5 vertical"},
    "troubleshoot-app-connection": {"format": "4:3 horizontal"},
    "downloads-docs": {"format": "16:9 horizontal"},
}

REFERENCE_FILES: Dict[str, Tuple[str, ...]] = {
    "e-nova": ("e-Nova.png",),
    "e-orbit": ("e-Orbit.png",),
    "e-touch": ("e-Touch.png",),
    "e-flex": ("e-Flex.png",),
    "e-prime": ("e-Prime.png",),
    "e-shield": ("e-Shield.png", "e-Shiled.png"),
}


def load_reference(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def build_subject_mask(image: Image.Image) -> Image.Image:
    alpha = image.getchannel("A")
    alpha_min, alpha_max = alpha.getextrema()
    if alpha_max > 0 and alpha_min < 250:
        return alpha.point(lambda value: 255 if value >= 16 else 0, mode="L")

    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    src = image.load()
    dst = mask.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = src[x, y]
            if a <= 0:
                continue
            if min(r, g, b) < 230 and (255 - max(r, g, b) > 20 or max(r, g, b) - min(r, g, b) > 8):
                dst[x, y] = 255
    return mask


def resolve_reference_path(slug: str) -> Path:
    domain_reference_root = EXT_IMAGES_ROOT / slug / "source-of-truth" / "product-images"
    for filename in REFERENCE_FILES[slug]:
        for candidate in (domain_reference_root / filename, EXT_IMAGES_ROOT / filename):
            if candidate.exists():
                return candidate
    raise FileNotFoundError(
        f"No PNG reference found for {slug!r} in either {domain_reference_root} or {EXT_IMAGES_ROOT}"
    )


def product_display_name(slug: str) -> str:
    return slug.replace("-", " ").title().replace("E ", "e-")


def resolve_review_asset_dir(slug: str) -> Path:
    domain_manual = EXT_IMAGES_ROOT / slug / "publishing" / "web" / "manuals" / f"{product_display_name(slug)} user manual - review-draft.md"
    if domain_manual.exists():
        return domain_manual.parents[1] / "assets" / slug / "review-draft"
    return MANUAL_ROOT / "assets" / slug / "review-draft"


def resolve_review_manual_path(slug: str) -> Path:
    manual_name = f"{product_display_name(slug)} user manual - review-draft.md"
    domain_candidate = EXT_IMAGES_ROOT / slug / "publishing" / "web" / "manuals" / manual_name
    legacy_candidate = MANUAL_ROOT / manual_name

    for candidate in (domain_candidate, legacy_candidate):
        if candidate.exists():
            return candidate

    if domain_candidate.parent.exists():
        return domain_candidate
    return legacy_candidate


def asset_root_for_manual(path: Path, slug: str, stage: str) -> str:
    if path.parent.name == "manuals" and path.parent.parent.name == "web":
        return f"../assets/{slug}/{stage}/"
    return f"assets/{slug}/{stage}/"


def reset_generated_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def find_components(mask: Image.Image) -> List[Tuple[int, Tuple[int, int, int, int]]]:
    width, height = mask.size
    pixels = mask.load()
    visited = [[False] * width for _ in range(height)]
    components: List[Tuple[int, Tuple[int, int, int, int]]] = []
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 0 or visited[y][x]:
                continue
            queue = deque([(x, y)])
            visited[y][x] = True
            xs: List[int] = []
            ys: List[int] = []
            area = 0
            while queue:
                cx, cy = queue.popleft()
                xs.append(cx)
                ys.append(cy)
                area += 1
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < width and 0 <= ny < height and pixels[nx, ny] > 0 and not visited[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((nx, ny))
            if area < 10000:
                continue
            box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
            if box[1] > int(height * 0.75):
                continue
            components.append((area, box))
    components.sort(key=lambda item: item[1][0])
    return components


def isolate_target_component(mask: Image.Image, target_region: Tuple[int, int, int, int]) -> Image.Image:
    width, height = mask.size
    pixels = mask.load()
    visited = [[False] * width for _ in range(height)]
    best_pixels: List[Tuple[int, int]] = []
    best_overlap = -1
    best_area = -1

    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 0 or visited[y][x]:
                continue

            queue = deque([(x, y)])
            visited[y][x] = True
            component_pixels: List[Tuple[int, int]] = []
            overlap = 0

            while queue:
                cx, cy = queue.popleft()
                component_pixels.append((cx, cy))
                if target_region[0] <= cx < target_region[2] and target_region[1] <= cy < target_region[3]:
                    overlap += 1

                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < width and 0 <= ny < height and pixels[nx, ny] > 0 and not visited[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((nx, ny))

            area = len(component_pixels)
            if overlap > best_overlap or (overlap == best_overlap and area > best_area):
                best_pixels = component_pixels
                best_overlap = overlap
                best_area = area

    isolated = Image.new("L", (width, height), 0)
    dst = isolated.load()
    for px, py in best_pixels:
        dst[px, py] = 255
    return isolated


def strip_edge_matte(component: Image.Image) -> Image.Image:
    width, height = component.size
    source = component.load()
    visited = [[False] * width for _ in range(height)]
    queue = deque()

    def is_edge_matte(pixel: Tuple[int, int, int, int]) -> bool:
        r, g, b, a = pixel
        neutral = max(r, g, b) - min(r, g, b) <= 28
        if not neutral or a <= 0:
            return False
        return (a <= 168 and max(r, g, b) >= 150) or min(r, g, b) >= 214

    for x in range(width):
        for y in (0, height - 1):
            if not visited[y][x] and is_edge_matte(source[x, y]):
                visited[y][x] = True
                queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            if not visited[y][x] and is_edge_matte(source[x, y]):
                visited[y][x] = True
                queue.append((x, y))

    while queue:
        cx, cy = queue.popleft()
        for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx] and is_edge_matte(source[nx, ny]):
                visited[ny][nx] = True
                queue.append((nx, ny))

    cleaned = component.copy()
    pixels = cleaned.load()
    for y in range(height):
        for x in range(width):
            if visited[y][x]:
                pixels[x, y] = (255, 255, 255, 0)

    alpha = cleaned.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        return cleaned
    return cleaned.crop(bbox)


def pad_component(component: Image.Image, margin: int = 28) -> Image.Image:
    padded = Image.new("RGBA", (component.size[0] + margin * 2, component.size[1] + margin * 2), (255, 255, 255, 0))
    padded.alpha_composite(component, (margin, margin))
    return padded


def extract_component(image: Image.Image, mask: Image.Image, box: Tuple[int, int, int, int], padding: int = 18) -> Image.Image:
    padded = (
        max(0, box[0] - padding),
        max(0, box[1] - padding),
        min(image.size[0], box[2] + padding),
        min(image.size[1], box[3] + padding),
    )
    cropped = image.crop(padded)
    target_region = (
        box[0] - padded[0],
        box[1] - padded[1],
        box[2] - padded[0],
        box[3] - padded[1],
    )
    cropped_mask = isolate_target_component(mask.crop(padded), target_region).filter(ImageFilter.GaussianBlur(1.2))
    rgba = Image.new("RGBA", cropped.size, (255, 255, 255, 0))
    rgba.paste(cropped, (0, 0), cropped_mask)
    alpha = rgba.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        return rgba
    trimmed = strip_edge_matte(rgba.crop(bbox))
    return pad_component(trimmed)


def sanitize_component(slug: str, side: str, component: Image.Image) -> Image.Image:
    sanitized = component.copy()
    draw = ImageDraw.Draw(sanitized)
    width, height = sanitized.size

    if slug == "e-orbit" and side == "interior":
        screen_rect = (
            int(width * 0.10),
            int(height * 0.02),
            int(width * 0.74),
            int(height * 0.35),
        )
        draw.rounded_rectangle(screen_rect, radius=18, fill=(236, 232, 224, 255), outline=(140, 144, 150, 220), width=3)
        line_y = screen_rect[1] + 18
        for width_ratio in (0.64, 0.48, 0.58):
            row_width = int((screen_rect[2] - screen_rect[0] - 24) * width_ratio)
            draw.rounded_rectangle(
                (screen_rect[0] + 12, line_y, screen_rect[0] + 12 + row_width, line_y + 10),
                radius=5,
                fill=(172, 181, 191, 220),
            )
            line_y += 22

    return sanitized


def component_centers(components: List[Tuple[int, Tuple[int, int, int, int]]]) -> Dict[str, Tuple[int, int, int, int]]:
    boxes = [box for _, box in components[:2]]
    if len(boxes) != 2:
        raise RuntimeError("Expected exactly two hardware components in the product reference image.")
    left_box, right_box = boxes
    return {"left": left_box, "right": right_box}


def create_background(size: Tuple[int, int], accent: Tuple[int, int, int]) -> Image.Image:
    width, height = size
    background = Image.new("RGBA", size, (244, 240, 231, 255))
    draw = ImageDraw.Draw(background)
    for y in range(height):
        ratio = y / max(1, height - 1)
        tone = int(248 - 16 * ratio)
        draw.line((0, y, width, y), fill=(tone, tone - 2, tone - 6, 255))

    panel = Image.new("RGBA", (int(width * 0.88), int(height * 0.82)), (255, 255, 255, 0))
    panel_draw = ImageDraw.Draw(panel)
    panel_draw.rounded_rectangle((0, 0, panel.size[0] - 1, panel.size[1] - 1), radius=36, fill=(252, 249, 242, 255), outline=(218, 208, 190, 255), width=2)
    panel_draw.arc((36, 36, panel.size[0] - 36, panel.size[1] - 36), 0, 360, fill=accent + (48,), width=3)
    panel_draw.arc((80, 80, panel.size[0] - 80, panel.size[1] - 80), 45, 240, fill=accent + (34,), width=2)
    panel_draw.line((panel.size[0] * 0.15, panel.size[1] * 0.72, panel.size[0] * 0.85, panel.size[1] * 0.72), fill=accent + (28,), width=2)
    background.alpha_composite(panel, ((width - panel.size[0]) // 2, (height - panel.size[1]) // 2))
    return background


def add_shadow(canvas: Image.Image, product: Image.Image, position: Tuple[int, int]) -> None:
    shadow = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    alpha = product.getchannel("A")
    shadow_alpha = alpha.filter(ImageFilter.GaussianBlur(18))
    shadow_layer = Image.new("RGBA", product.size, (34, 42, 52, 90))
    shadow_layer.putalpha(shadow_alpha)
    shadow.alpha_composite(shadow_layer, (position[0] + 12, position[1] + 18))
    canvas.alpha_composite(shadow)


def place_product(canvas: Image.Image, product: Image.Image, max_width: int, max_height: int, center: Tuple[int, int]) -> Tuple[Image.Image, Tuple[int, int]]:
    scaled = ImageOps.contain(product, (max_width, max_height))
    position = (center[0] - scaled.size[0] // 2, center[1] - scaled.size[1] // 2)
    add_shadow(canvas, scaled, position)
    canvas.alpha_composite(scaled, position)
    return scaled, position


def local_point(position: Tuple[int, int], size: Tuple[int, int], normalized: Tuple[float, float]) -> Tuple[int, int]:
    return (position[0] + int(size[0] * normalized[0]), position[1] + int(size[1] * normalized[1]))


def draw_focus_ring(draw: ImageDraw.ImageDraw, point: Tuple[int, int], radius: int, color: Tuple[int, int, int]) -> None:
    x, y = point
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=color + (255,), width=5)
    draw.ellipse((x - radius - 14, y - radius - 14, x + radius + 14, y + radius + 14), outline=color + (120,), width=2)


def draw_hand_silhouette(draw: ImageDraw.ImageDraw, point: Tuple[int, int], scale: int, direction: str = "left") -> None:
    x, y = point
    palm_offset = -scale if direction == "left" else scale
    fingertip = [
        (x + palm_offset, y + scale * 2),
        (x + palm_offset + (22 if direction == "left" else -22), y + scale),
        (x + palm_offset + (18 if direction == "left" else -18), y - scale * 2),
        (x + palm_offset + (4 if direction == "left" else -4), y - scale * 4),
        (x, y - scale * 3),
        (x + (10 if direction == "left" else -10), y - scale),
    ]
    draw.rounded_rectangle(
        (
            min(x, x + palm_offset) - scale * 2,
            y + scale * 2,
            max(x, x + palm_offset) + scale * 4,
            y + scale * 8,
        ),
        radius=scale * 2,
        fill=(44, 52, 60, 220),
    )
    draw.polygon(fingertip, fill=(44, 52, 60, 220))
    draw.ellipse((x - scale // 2, y - scale // 2, x + scale // 2, y + scale // 2), fill=(44, 52, 60, 220))


def draw_door_context(draw: ImageDraw.ImageDraw, canvas_size: Tuple[int, int]) -> None:
    width, height = canvas_size
    left = int(width * 0.16)
    top = int(height * 0.10)
    right = int(width * 0.84)
    bottom = int(height * 0.92)
    draw.rounded_rectangle((left, top, right, bottom), radius=28, outline=(185, 176, 160, 255), width=5, fill=(248, 244, 236, 120))
    draw.line((int(width * 0.28), top, int(width * 0.28), bottom), fill=(205, 198, 185, 255), width=3)


def draw_connection(draw: ImageDraw.ImageDraw, start: Tuple[int, int], end: Tuple[int, int], broken: bool = False) -> None:
    color = (81, 126, 167, 255) if not broken else (188, 111, 88, 255)
    segments = 7
    for index in range(segments):
        if broken and index == segments // 2:
            continue
        fraction1 = index / segments
        fraction2 = min(1, (index + 0.55) / segments)
        x1 = int(start[0] + (end[0] - start[0]) * fraction1)
        y1 = int(start[1] + (end[1] - start[1]) * fraction1)
        x2 = int(start[0] + (end[0] - start[0]) * fraction2)
        y2 = int(start[1] + (end[1] - start[1]) * fraction2)
        draw.line((x1, y1, x2, y2), fill=color, width=6)
    if broken:
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        draw.line((mid_x - 18, mid_y - 18, mid_x + 18, mid_y + 18), fill=color, width=6)
        draw.line((mid_x + 18, mid_y - 18, mid_x - 18, mid_y + 18), fill=color, width=6)


def draw_smartphone(canvas: Image.Image, rect: Tuple[int, int, int, int], qr: bool = False) -> Tuple[int, int]:
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(rect, radius=30, fill=(35, 38, 42, 255), outline=(88, 96, 104, 255), width=4)
    inset = (rect[0] + 24, rect[1] + 30, rect[2] - 24, rect[3] - 34)
    draw.rounded_rectangle(inset, radius=18, fill=(246, 242, 232, 255))
    if qr:
        qr_size = min(inset[2] - inset[0], inset[3] - inset[1]) - 48
        qx = inset[0] + ((inset[2] - inset[0]) - qr_size) // 2
        qy = inset[1] + ((inset[3] - inset[1]) - qr_size) // 2
        cell = qr_size // 7
        for row in range(7):
            for col in range(7):
                if (row in {0, 6} or col in {0, 6} or (row + col) % 3 == 0) and not (row in {3} and col in {3}):
                    draw.rectangle((qx + col * cell, qy + row * cell, qx + (col + 1) * cell - 2, qy + (row + 1) * cell - 2), fill=(56, 61, 67, 255))
    else:
        y = inset[1] + 24
        for width_ratio in (0.72, 0.54, 0.66, 0.40):
            row_width = int((inset[2] - inset[0]) * width_ratio)
            draw.rounded_rectangle((inset[0] + 22, y, inset[0] + 22 + row_width, y + 16), radius=8, fill=(170, 181, 194, 255))
            y += 36
        draw.rounded_rectangle((inset[0] + 22, inset[3] - 84, inset[2] - 22, inset[3] - 26), radius=16, fill=(126, 154, 178, 255))
    return ((rect[0] + rect[2]) // 2, (rect[1] + rect[3]) // 2)


def draw_document_cards(canvas: Image.Image, anchor: Tuple[int, int]) -> None:
    draw = ImageDraw.Draw(canvas)
    ax, ay = anchor
    card_specs = [(-36, -18, (248, 244, 236, 255)), (26, 12, (242, 237, 228, 255))]
    for dx, dy, fill in card_specs:
        rect = (ax + dx, ay + dy, ax + dx + 230, ay + dy + 300)
        draw.rounded_rectangle(rect, radius=24, fill=fill, outline=(191, 182, 166, 255), width=3)
        row_y = rect[1] + 36
        for width_ratio in (0.68, 0.56, 0.72, 0.43, 0.61):
            row_width = int((rect[2] - rect[0] - 60) * width_ratio)
            draw.rounded_rectangle((rect[0] + 30, row_y, rect[0] + 30 + row_width, row_y + 14), radius=7, fill=(164, 174, 184, 255))
            row_y += 34


def hero_image(exterior: Image.Image, accent: Tuple[int, int, int], size: Tuple[int, int]) -> Image.Image:
    canvas = create_background(size, accent)
    place_product(canvas, exterior, int(size[0] * 0.42), int(size[1] * 0.68), (size[0] // 2, size[1] // 2 + 10))
    return canvas


def installed_context_image(interior: Image.Image, accent: Tuple[int, int, int], size: Tuple[int, int]) -> Image.Image:
    canvas = create_background(size, accent)
    draw = ImageDraw.Draw(canvas)
    draw_door_context(draw, size)
    place_product(canvas, interior, int(size[0] * 0.42), int(size[1] * 0.68), (size[0] // 2, int(size[1] * 0.52)))
    return canvas


def interaction_image(exterior: Image.Image, accent: Tuple[int, int, int], size: Tuple[int, int], point: Tuple[float, float], ring_color: Tuple[int, int, int]) -> Image.Image:
    canvas = create_background(size, accent)
    placed, pos = place_product(canvas, exterior, int(size[0] * 0.78), int(size[1] * 0.62), (size[0] // 2, int(size[1] * 0.46)))
    target = local_point(pos, placed.size, point)
    draw = ImageDraw.Draw(canvas)
    draw_focus_ring(draw, target, 24, ring_color)
    draw_hand_silhouette(draw, (target[0] - 20, target[1] + 18), 18, direction="left")
    return canvas


def pin_image(exterior: Image.Image, accent: Tuple[int, int, int], size: Tuple[int, int], point: Tuple[float, float]) -> Image.Image:
    canvas = create_background(size, accent)
    placed, pos = place_product(canvas, exterior, int(size[0] * 0.78), int(size[1] * 0.62), (size[0] // 2, int(size[1] * 0.46)))
    target = local_point(pos, placed.size, point)
    draw = ImageDraw.Draw(canvas)
    draw_focus_ring(draw, target, 24, (72, 112, 154))
    draw_hand_silhouette(draw, (target[0] - 16, target[1] + 20), 16, direction="left")
    pad_rect = (int(size[0] * 0.20), int(size[1] * 0.73), int(size[0] * 0.80), int(size[1] * 0.89))
    draw.rounded_rectangle(pad_rect, radius=24, fill=(251, 248, 241, 220), outline=(189, 181, 165, 255), width=3)
    cols, rows = 3, 4
    cell_w = (pad_rect[2] - pad_rect[0] - 80) / cols
    cell_h = (pad_rect[3] - pad_rect[1] - 48) / rows
    for row in range(rows):
        for col in range(cols):
            cx = int(pad_rect[0] + 40 + col * cell_w + cell_w / 2)
            cy = int(pad_rect[1] + 24 + row * cell_h + cell_h / 2)
            draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=(116, 126, 140, 255))
    return canvas


def settings_image(exterior: Image.Image, accent: Tuple[int, int, int], size: Tuple[int, int], point: Tuple[float, float]) -> Image.Image:
    canvas = create_background(size, accent)
    placed, pos = place_product(canvas, exterior, int(size[0] * 0.70), int(size[1] * 0.56), (size[0] // 2, int(size[1] * 0.42)))
    target = local_point(pos, placed.size, point)
    draw = ImageDraw.Draw(canvas)
    for offset, radius in ((-110, 18), (0, 22), (110, 18)):
        bubble = (target[0] + offset, int(size[1] * 0.78))
        draw_focus_ring(draw, bubble, radius, (126, 154, 178))
        draw.line((target[0], target[1] + 24, bubble[0], bubble[1] - radius - 18), fill=(126, 154, 178, 180), width=4)
    return canvas


def app_image(exterior: Image.Image, accent: Tuple[int, int, int], size: Tuple[int, int], qr: bool = False, broken: bool = False) -> Image.Image:
    canvas = create_background(size, accent)
    placed, pos = place_product(canvas, exterior, int(size[0] * 0.38), int(size[1] * 0.68), (int(size[0] * 0.34), size[1] // 2))
    phone_center = draw_smartphone(canvas, (int(size[0] * 0.62), int(size[1] * 0.18), int(size[0] * 0.84), int(size[1] * 0.82)), qr=qr)
    product_anchor = (pos[0] + placed.size[0] - 10, pos[1] + placed.size[1] // 2)
    draw = ImageDraw.Draw(canvas)
    draw_connection(draw, product_anchor, (phone_center[0] - 90, phone_center[1]), broken=broken)
    return canvas


def docs_image(exterior: Image.Image, accent: Tuple[int, int, int], size: Tuple[int, int]) -> Image.Image:
    canvas = create_background(size, accent)
    place_product(canvas, exterior, int(size[0] * 0.28), int(size[1] * 0.62), (int(size[0] * 0.30), size[1] // 2 + 10))
    draw_document_cards(canvas, (int(size[0] * 0.58), int(size[1] * 0.30)))
    return canvas


def accent_for_slug(slug: str) -> Tuple[int, int, int]:
    accents = {
        "e-nova": (83, 119, 142),
        "e-orbit": (72, 112, 154),
        "e-touch": (74, 136, 122),
        "e-flex": (105, 124, 154),
        "e-prime": (90, 130, 173),
        "e-shield": (118, 112, 150),
    }
    return accents[slug]


def build_assets_for_product(config: ProductConfig) -> None:
    reference_path = resolve_reference_path(config.slug)
    image = load_reference(reference_path)
    mask = build_subject_mask(image)
    boxes = component_centers(find_components(mask))
    exterior_box = boxes[config.exterior_side]
    interior_box = boxes["left" if config.exterior_side == "right" else "right"]
    exterior = sanitize_component(config.slug, "exterior", extract_component(image, mask, exterior_box))
    interior = sanitize_component(config.slug, "interior", extract_component(image, mask, interior_box))
    review_dir = resolve_review_asset_dir(config.slug)
    reset_generated_dir(review_dir)
    accent = accent_for_slug(config.slug)

    generated = {
        f"{config.slug}-hero-main.webp": hero_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["hero-main"]["format"]]),
        f"{config.slug}-installed-context.webp": installed_context_image(interior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["installed-context"]["format"]]),
        f"{config.slug}-add-admin-action.webp": interaction_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["add-admin-action"]["format"]], config.control_point, (109, 153, 177)),
        f"{config.slug}-pin-use.webp": pin_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["pin-use"]["format"]], config.credential_point),
        f"{config.slug}-fingerprint-use.webp": interaction_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["fingerprint-use"]["format"]], config.sensor_point, (79, 163, 176)),
        f"{config.slug}-language-settings.webp": settings_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["language-settings"]["format"]], config.control_point),
        f"{config.slug}-app-add-device.webp": app_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["app-add-device"]["format"]]),
        f"{config.slug}-link-qr.webp": app_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["link-qr"]["format"]], qr=True),
        f"{config.slug}-troubleshoot-fingerprint.webp": interaction_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["troubleshoot-fingerprint"]["format"]], config.sensor_point, (195, 120, 96)),
        f"{config.slug}-troubleshoot-app-connection.webp": app_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["troubleshoot-app-connection"]["format"]], broken=True),
        f"{config.slug}-downloads-docs.webp": docs_image(exterior, accent, FORMAT_DIMENSIONS[SLOT_SPECS["downloads-docs"]["format"]]),
    }
    for filename, rendered in generated.items():
        rendered.convert("RGB").save(review_dir / filename, format="WEBP", quality=94, method=6)


def normalize_review_draft_manual(path: Path, slug: str) -> None:
    text = path.read_text(encoding="utf-8")
    web_asset_root = asset_root_for_manual(path, slug, "web-ready")
    review_asset_root = asset_root_for_manual(path, slug, "review-draft")
    updated = text.replace(f"assets/{slug}/web-ready/", web_asset_root)
    updated = updated.replace(f"assets/{slug}/review-draft/", review_asset_root)
    replacements = {
        "Este borrador mezcla assets ya publicados en `assets/e-prime/web-ready/` con winners seleccionados en `assets/e-prime/review-draft/` para revisar un manual mas completo antes de aprobar publicacion final.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar el manual completo antes de publicacion final.",
        "Este borrador mezcla assets ya publicados en `assets/e-prime/review-draft/` con winners seleccionados en `assets/e-prime/review-draft/` para revisar un manual mas completo antes de aprobar publicacion final.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar el manual completo antes de publicacion final.",
        "Este borrador mezcla assets ya publicados en `assets/e-flex/web-ready/` con winners seleccionados en `assets/e-flex/review-draft/` para revisar el paquete completo antes de publicacion final.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar el paquete completo antes de publicacion final.",
        "Este borrador mezcla assets ya publicados en `assets/e-flex/review-draft/` con winners seleccionados en `assets/e-flex/review-draft/` para revisar el paquete completo antes de publicacion final.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar el paquete completo antes de publicacion final.",
        "Este borrador mezcla assets ya publicados en `assets/e-shield/web-ready/` con winners seleccionados en `assets/e-shield/review-draft/` para revisar la cobertura completa del manual antes de aprobacion final.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar la cobertura completa del manual antes de aprobacion final.",
        "Este borrador mezcla assets ya publicados en `assets/e-shield/review-draft/` con winners seleccionados en `assets/e-shield/review-draft/` para revisar la cobertura completa del manual antes de aprobacion final.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar la cobertura completa del manual antes de aprobacion final.",
        "Este borrador mantiene los assets finales ya publicados y agrega winners seleccionados en `assets/e-orbit/review-draft/` para revisar la cobertura del manual completo antes de aprobar publicacion definitiva.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar la cobertura del manual completo antes de aprobar publicacion definitiva.",
        "Este borrador usa assets ya publicados y winners seleccionados en `assets/e-touch/review-draft/` para revisar una version inicial del manual sin perder la identidad de manija con numerales integrados.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar una version integral del manual sin arrastrar la generacion anterior.",
        "Este borrador usa assets finales ya publicados y winners seleccionados en `assets/e-nova/review-draft/` para revisar una version mas completa del manual sin inventar hardware que el producto no tiene.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar una version mas completa del manual sin inventar hardware que el producto no tiene.",
        "Este borrador mantiene assets publicados y winners de `review-draft` para revisar un flujo mas completo sin afectar todavia el paquete final.": "Este borrador usa exclusivamente assets `review-draft` del reset visual 2026-05-13 para revisar un flujo mas completo sin afectar todavia el paquete final.",
        "Este archivo es una version inicial de revision. Los assets de `review-draft` vienen de winners seleccionados y aun no reemplazan el paquete final `image-ready`.": "Este archivo es una version integral de revision. Los assets `review-draft` fueron reconstruidos bajo el reset visual 2026-05-13 y quedan listos para inspeccion antes de publicar el paquete final.",
    }
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    for slug, config in PRODUCTS.items():
        build_assets_for_product(config)
        normalize_review_draft_manual(resolve_review_manual_path(config.slug), config.slug)
    print("Generated reset-era review-draft assets and normalized review manuals.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())