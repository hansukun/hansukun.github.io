"""Draws the site's pixel art from text grids. Run: python scripts/make_sprites.py

Writes assets/game/hans-walk.png (64x48: 4 walk frames x 2 colour rows) and
assets/game/glove.png (16x11). One character per pixel; "." is transparent.
Design: docs/superpowers/specs/2026-09-25-jrpg-accents-design.md
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "game"

Rgba = tuple[int, int, int, int]
CLEAR: Rgba = (0, 0, 0, 0)


def rgb(hex_: str) -> Rgba:
    h = hex_.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255


# ---- mini-Hans ----------------------------------------------------------------

CELL_W, CELL_H = 16, 24

HEAD = [
    "......OOOOO.....",
    "....OOHHHHHOO...",
    "...OHHHhhHHHHO..",
    "..OHHHhhhHHHHHO.",
    "..OHHHHHHHHHHHHO",
    ".OHHHHHHHHHHHHO.",
    ".OHHHHHHHHhHHHHO",
    ".OHHHHHHSHSSHSO.",
    ".OHHHHSSSSSSSSO.",
    ".OHHHHSSSSHHSSO.",
    "..OHHssSSSSeSSO.",
    "..OHHssSSSSeSSO.",
    "...OHSSSSSSSmO..",
    "....OOSSSSSOO...",
    ".....OssSO......",
]

BODIES = {
    "stand": [
        "....OTTTTTO.....",
        "...OTtTTTTTO....",
        "...OTtTTLTTO....",
        "...OTtTSSTTO....",
        "....OJJJJJO.....",
        "....OJJjJJO.....",
        "....OWWOWWWO....",
        "....OOOOOOOO....",
    ],
    "stepA": [
        "....OTTTTTO.....",
        "...OTtTTTTTO....",
        "...OTtTTLTTOSO..",
        "...OTTTTTTTOO...",
        "...OJJJJJJO.....",
        "..OJJO..OJJO....",
        ".OWWWO...OWWWO..",
        ".OOOOO...OOOOO..",
    ],
    "stepB": [
        "....OTTTTTO.....",
        "...OTtTTTTTO....",
        ".OSOTtTTLTTO....",
        "..OOTtTTTTTO....",
        "....OJJJJJJO....",
        "...OJJO.OJJO....",
        "..OWWWO.OWWWO...",
        "..OOOOO.OOOOO...",
    ],
}

# (body, bob): in bob frames the head is drawn 1px lower.
FRAMES = [("stand", False), ("stepA", True), ("stand", False), ("stepB", True)]
LOGOS = ["#3b6cff", "#22c55e"]   # sheet row 0: portfolio blue, row 1: Settled green

SPRITE_COLOURS = {
    "O": "#07070a",   # outline
    "H": "#1c1d26",   # hair
    "h": "#46527a",   # hair sheen
    "S": "#f6d3b3",   # skin
    "s": "#dba987",   # skin shade
    "e": "#07070a",   # eye
    "m": "#c98b72",   # mouth
    "T": "#24262e",   # tee
    "t": "#4b4f60",   # tee highlight
    "J": "#2d3f6f",   # jeans
    "j": "#1f2b4d",   # jeans shade
    "W": "#ececf1",   # sneakers
}
SHADOW: Rgba = (0, 0, 0, 140)   # rgba(0,0,0,.55) on row 23, x 4-11

# ---- glove ----------------------------------------------------------------------

GLOVE = [
    "................",
    ".OOOOOOOOOOOOOO.",
    "OccWWWWWWWWWWWWO",
    "OccWWWWWWWWWWWWO",
    "OccWWWWWWWWWWWWO",
    "OccWWWWWOOOOOOO.",
    "OccWkkkkO.......",
    "OccWWWWWO.......",
    "OccWkkkkO.......",
    "OccWWWWWO.......",
    ".OOOOOOO........",
]
GLOVE_COLOURS = {"O": "#000000", "W": "#ffffff", "c": "#b8c4d6", "k": "#8894a8"}


# ---- drawing --------------------------------------------------------------------

def grid_errors(name: str, grid: list[str], width: int, height: int, keys: set[str]) -> list[str]:
    errors = []
    if len(grid) != height:
        errors.append(f"{name}: {len(grid)} rows, expected {height}")
    for y, row in enumerate(grid):
        if len(row) != width:
            errors.append(f"{name} row {y}: {len(row)} columns, expected {width}")
        bad = sorted({ch for ch in row if ch != "." and ch not in keys})
        if bad:
            errors.append(f"{name} row {y}: unknown keys {''.join(bad)}")
    return errors


def paint(img: Image.Image, rows: list[str], colours: dict[str, Rgba],
          ox: int = 0, oy: int = 0, drop_rows: int = 0) -> None:
    """Paints rows top to bottom; rows before `drop_rows` land 1px lower."""
    for y, row in enumerate(rows):
        dy = 1 if y < drop_rows else 0
        for x, ch in enumerate(row):
            if ch != ".":
                img.putpixel((ox + x, oy + y + dy), colours[ch])


def draw_frame(sheet: Image.Image, ox: int, oy: int, body: str, bob: bool, logo: str) -> None:
    colours = {k: rgb(v) for k, v in SPRITE_COLOURS.items()}
    colours["L"] = rgb(logo)
    for x in range(4, 12):
        sheet.putpixel((ox + x, oy + CELL_H - 1), SHADOW)
    paint(sheet, HEAD + BODIES[body], colours, ox, oy, drop_rows=len(HEAD) if bob else 0)


def main() -> int:
    sprite_keys = set(SPRITE_COLOURS) | {"L"}
    errors = grid_errors("head", HEAD, CELL_W, 15, sprite_keys)
    for name, body in BODIES.items():
        errors += grid_errors(name, body, CELL_W, 8, sprite_keys)
    errors += grid_errors("glove", GLOVE, 16, 11, set(GLOVE_COLOURS))
    if errors:
        print("\n".join(errors))
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGBA", (CELL_W * len(FRAMES), CELL_H * len(LOGOS)), CLEAR)
    for r, logo in enumerate(LOGOS):
        for i, (body, bob) in enumerate(FRAMES):
            draw_frame(sheet, i * CELL_W, r * CELL_H, body, bob, logo)
    sheet.save(OUT / "hans-walk.png", optimize=True)

    glove = Image.new("RGBA", (16, 11), CLEAR)
    paint(glove, GLOVE, {k: rgb(v) for k, v in GLOVE_COLOURS.items()})
    glove.save(OUT / "glove.png", optimize=True)

    print(f"wrote assets/game/hans-walk.png ({sheet.width}x{sheet.height}) and assets/game/glove.png (16x11)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
