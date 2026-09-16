"""Crop raw 1240x2772 device captures into assets/screens/.

Usage: python scripts/crop_screens.py <raw_dir>
Expects <raw_dir>/<name>.png for each name in SCREENS.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "screens"
SCREENS = ["month", "month-settled", "template", "history", "settings"]

# Crop box in source pixels: below the status bar, above the ad banner / tab bar.
# Tuned for a 1240x2772 capture; adjust TOP/BOTTOM after eyeballing the raw files.
TOP = 130
BOTTOM = 2162          # 2162 - 130 = 2032 px tall -> 1240:2032 = 720:1180
TARGET_W = 720


def crop(name: str, raw_dir: Path) -> None:
    src = raw_dir / f"{name}.png"
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if (w, h) != (1240, 2772):
        print(f"warning: {src.name} is {w}x{h}, crop box assumes 1240x2772")
    out = im.crop((0, TOP, w, min(BOTTOM, h)))
    scale = TARGET_W / out.width
    out = out.resize((TARGET_W, round(out.height * scale)), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    out.save(OUT / f"{name}.png", optimize=True)
    out.save(OUT / f"{name}.webp", quality=85, method=6)
    print(f"{name}: {out.width}x{out.height}")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    raw_dir = Path(sys.argv[1])
    for name in SCREENS:
        crop(name, raw_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
