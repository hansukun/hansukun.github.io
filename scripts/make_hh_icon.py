"""Build the Happy Haus Toys favicon: the logo art on its scalloped cream badge, 180x180.

Run: python scripts/make_hh_icon.py
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "works" / "happy-haus-toys" / "assets"
SIZE = 180
SS = 4  # supersample for smooth scallops
CREAM = (255, 250, 240, 255)


def badge(size: int) -> Image.Image:
    """Same shape as the CSS .badge mask: 11 semicircle scallops on a circle of radius 84 in a 200 box."""
    s = size / 200
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [(100 + 84 * math.cos(2 * math.pi * i / 11 - math.pi / 2), 100 + 84 * math.sin(2 * math.pi * i / 11 - math.pi / 2)) for i in range(11)]
    d.polygon([(x * s, y * s) for x, y in pts], fill=CREAM)
    for i in range(11):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % 11]
        mx, my, r = (x0 + x1) / 2, (y0 + y1) / 2, math.dist((x0, y0), (x1, y1)) / 2
        d.ellipse(((mx - r) * s, (my - r) * s, (mx + r) * s, (my + r) * s), fill=CREAM)
    return img


def main() -> None:
    big = SIZE * SS
    icon = badge(big)
    art = Image.open(ASSETS / "logo-art.png").convert("RGBA")
    w = int(big * 0.7)
    art = art.resize((w, round(art.height * w / art.width)), Image.LANCZOS)
    icon.alpha_composite(art, ((big - art.width) // 2, (big - art.height) // 2))
    icon.resize((SIZE, SIZE), Image.LANCZOS).save(ASSETS / "icon.png")
    print(f"wrote {ASSETS / 'icon.png'}")


if __name__ == "__main__":
    main()
