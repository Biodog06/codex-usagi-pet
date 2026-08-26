#!/usr/bin/env python3
"""Build occasional idle Easter eggs into the Codex pet spritesheet.

The Codex pet runtime does not expose per-action probability settings.  This
script keeps the standard atlas intact and stores a long, irregular timeline
inside an animated WebP.  During an Easter egg, all six idle cells contain the
same action frame so the runtime's own idle-column clock cannot desynchronise
the action.
"""

from __future__ import annotations

import math
import os
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
LEGACY_SPRITESHEET = ROOT / "spritesheet.webp"
SPRITESHEET = ROOT / "spritesheet.png"
SPECIAL_ACTIONS = ROOT / "assets" / "special-actions.png"
PREVIEW = ROOT / "assets" / "idle-easter-eggs.gif"

CELL_W = 192
CELL_H = 208
ATLAS_SIZE = (1536, 2288)
IDLE_COLUMNS = range(6)

# Each tuple is (normal-idle delay in milliseconds, action name).  The long,
# uneven cycle makes the two approved actions feel occasional and random.
SCHEDULE = (
    (31_000, "grass"),
    (47_000, "clamp"),
    (23_000, "grass"),
    (56_000, "clamp"),
    (38_000, "clamp"),
    (29_000, "grass"),
)

ACTION_DURATIONS = {
    "grass": (190, 170, 180, 210, 180, 360),
    "clamp": (260, 170, 150, 170, 230, 420),
}


def _pixel_data(image: Image.Image):
    getter = getattr(image, "get_flattened_data", None)
    return getter() if getter is not None else image.getdata()


def _checker_color(x: int, y: int) -> tuple[int, int, int]:
    """Return the exact checkerboard color used by special-actions.png."""
    # The contact sheet uses 12 px squares and alternates at the crop origin.
    return (244, 244, 244) if ((x // 12) + (y // 12)) % 2 == 0 else (218, 218, 218)


def _largest_subject_component(cell: Image.Image) -> list[list[bool]]:
    """Find the character while discarding frame numbers and green dividers."""
    rgb = cell.convert("RGB")
    pixels = rgb.load()
    candidate = [[False] * CELL_W for _ in range(CELL_H)]

    for y in range(CELL_H):
        for x in range(CELL_W):
            r, g, b = pixels[x, y]
            bg = _checker_color(x, y)
            distance = math.sqrt(sum((c - q) ** 2 for c, q in zip((r, g, b), bg)))
            green_divider = g > 120 and g > r * 2 and g > b * 1.25
            candidate[y][x] = distance > 2.0 and not green_divider

    visited = [[False] * CELL_W for _ in range(CELL_H)]
    components: list[list[tuple[int, int]]] = []
    for y in range(CELL_H):
        for x in range(CELL_W):
            if not candidate[y][x] or visited[y][x]:
                continue
            queue = deque([(x, y)])
            visited[y][x] = True
            component: list[tuple[int, int]] = []
            while queue:
                px, py = queue.popleft()
                component.append((px, py))
                for ny in range(max(0, py - 1), min(CELL_H, py + 2)):
                    for nx in range(max(0, px - 1), min(CELL_W, px + 2)):
                        if candidate[ny][nx] and not visited[ny][nx]:
                            visited[ny][nx] = True
                            queue.append((nx, ny))
            components.append(component)

    if not components:
        raise RuntimeError("No subject found in special-action cell")

    subject = max(components, key=len)
    mask = [[False] * CELL_W for _ in range(CELL_H)]
    for x, y in subject:
        mask[y][x] = True
    return mask


def _restore_transparency(cell: Image.Image) -> Image.Image:
    """Recover the transparent sprite from the published checkerboard preview."""
    rgb = cell.convert("RGB")
    pixels = rgb.load()
    mask = _largest_subject_component(rgb)
    out = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    dst = out.load()
    outline = (91, 45, 31)

    for y in range(CELL_H):
        for x in range(CELL_W):
            if not mask[y][x]:
                continue

            c = pixels[x, y]
            bg = _checker_color(x, y)
            is_boundary = any(
                nx < 0
                or nx >= CELL_W
                or ny < 0
                or ny >= CELL_H
                or not mask[ny][nx]
                for ny in range(y - 1, y + 2)
                for nx in range(x - 1, x + 2)
            )
            if not is_boundary:
                dst[x, y] = (*c, 255)
                continue

            observed = math.sqrt(sum((a - b) ** 2 for a, b in zip(c, bg)))
            full_edge = math.sqrt(sum((a - b) ** 2 for a, b in zip(outline, bg)))
            alpha = max(0.0, min(1.0, observed / full_edge))
            if alpha < 0.035:
                continue
            restored = tuple(
                max(0, min(255, round((channel - (1.0 - alpha) * base) / alpha)))
                for channel, base in zip(c, bg)
            )
            dst[x, y] = (*restored, round(alpha * 255))

    return out


def extract_action_frames() -> dict[str, list[Image.Image]]:
    sheet = Image.open(SPECIAL_ACTIONS).convert("RGB")
    if sheet.size != (1152, 468):
        raise RuntimeError(f"Unexpected special-actions size: {sheet.size}")

    rows = {"grass": 26, "clamp": 260}
    actions: dict[str, list[Image.Image]] = {}
    for name, top in rows.items():
        actions[name] = []
        for column in range(6):
            box = (column * CELL_W, top, (column + 1) * CELL_W, top + CELL_H)
            actions[name].append(_restore_transparency(sheet.crop(box)))
    return actions


def _action_atlas(base: Image.Image, action_frame: Image.Image) -> Image.Image:
    frame = base.copy()
    empty = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    for column in IDLE_COLUMNS:
        x = column * CELL_W
        frame.paste(empty, (x, 0))
        frame.alpha_composite(action_frame, (x, 0))
    return frame


def _save_preview(actions: dict[str, list[Image.Image]]) -> None:
    preview_frames: list[Image.Image] = []
    durations: list[int] = []
    for name in ("grass", "clamp"):
        for frame, duration in zip(actions[name], ACTION_DURATIONS[name]):
            canvas = Image.new("RGBA", (CELL_W, CELL_H), (255, 255, 255, 255))
            canvas.alpha_composite(frame)
            preview_frames.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE))
            durations.append(duration)
        durations[-1] += 600
    preview_frames[0].save(
        PREVIEW,
        save_all=True,
        append_images=preview_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )


def _zero_transparent_rgb(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    rgba.putdata(
        [(0, 0, 0, 0) if a == 0 else (r, g, b, a) for r, g, b, a in _pixel_data(rgba)]
    )
    return rgba


def build() -> None:
    source_path = SPRITESHEET if SPRITESHEET.exists() else LEGACY_SPRITESHEET
    with Image.open(source_path) as source:
        source.seek(0)
        base = _zero_transparent_rgb(source)
    if base.size != ATLAS_SIZE:
        raise RuntimeError(f"Unexpected atlas size: {base.size}")

    actions = extract_action_frames()
    timeline: list[Image.Image] = []
    durations: list[int] = []
    for idle_delay, name in SCHEDULE:
        timeline.append(base.copy())
        durations.append(idle_delay)
        for action_frame, duration in zip(actions[name], ACTION_DURATIONS[name]):
            timeline.append(_action_atlas(base, action_frame))
            durations.append(duration)

    temp_path = SPRITESHEET.with_name("spritesheet.building.png")
    timeline[0].save(
        temp_path,
        format="PNG",
        save_all=True,
        append_images=timeline[1:],
        duration=durations,
        loop=0,
        disposal=0,
        blend=0,
        optimize=True,
    )
    os.replace(temp_path, SPRITESHEET)
    _save_preview(actions)

    with Image.open(SPRITESHEET) as check:
        if check.size != ATLAS_SIZE or getattr(check, "n_frames", 1) != len(timeline):
            raise RuntimeError("Animated spritesheet verification failed")
        check.seek(0)
        decoded_base = check.convert("RGBA")
        if ImageChops.difference(decoded_base, base).getbbox() is not None:
            raise RuntimeError("Normal idle frame changed during APNG encoding")
        base_non_idle = decoded_base.crop((0, CELL_H, ATLAS_SIZE[0], ATLAS_SIZE[1]))
        for index in range(check.n_frames):
            check.seek(index)
            decoded = check.convert("RGBA")
            if ImageChops.difference(
                decoded.crop((0, CELL_H, ATLAS_SIZE[0], ATLAS_SIZE[1])), base_non_idle
            ).getbbox() is not None:
                raise RuntimeError(f"Non-idle rows changed in APNG frame {index}")
            if any(
                alpha == 0 and (red or green or blue)
                for red, green, blue, alpha in _pixel_data(decoded)
            ):
                raise RuntimeError(f"Transparent RGB residue in APNG frame {index}")

    print(f"Built {len(timeline)}-frame APNG atlas: {SPRITESHEET}")
    print(f"Idle cycle: {sum(durations) / 1000:.1f}s")
    print(f"Preview: {PREVIEW}")


if __name__ == "__main__":
    build()
