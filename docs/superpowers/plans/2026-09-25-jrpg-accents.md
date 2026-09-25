# JRPG Accents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Final Fantasy / Suikoden-flavoured accents — a pixel glove cursor, a typed dialog box, a shine sweep, CRT scanlines, EXP bars, a "SETTLED!" phone moment and a walking pixel mini-Hans — to the portfolio and both Settled pages without changing either site's brand.

**Architecture:** Pixel art is drawn from text grids by `scripts/make_sprites.py` (Pillow) into `assets/game/*.png`. One shared, deferred, dependency-free `assets/game/game.js` provides the four behaviours CSS can't (typewriter, reveal-on-view, nav scroll-spy, sprite pause), each opted into by a `data-*` attribute; every visual effect is CSS in each page's existing inline `<style>`. `scripts/check_site.py` stays the static test suite; `tests/game-test.html` is an in-browser test page for `game.js`.

**Tech Stack:** HTML5, CSS3, vanilla JS (ES2017 syntax, no `??`/`?.`), Python 3.14 + Pillow 12 (already installed), `python -m http.server` via the `site` launch config, the built-in browser pane.

**Spec:** `docs/superpowers/specs/2026-09-25-jrpg-accents-design.md`

## Global Constraints

- Static files only: no build step, bundler, framework or third-party JS. The only script on any page is `<script src="…/assets/game/game.js" defer></script>` in `<head>`; no inline scripts on site pages (the test page is exempt — it is not a site page).
- All paths relative, never root-absolute. Portfolio uses `assets/game/…`; `settled/*.html` use `../assets/game/…`.
- Only external hosts: `fonts.googleapis.com`, `fonts.gstatic.com`, `www.linkedin.com` (plus the existing `*google.com` links on the privacy page).
- No colour changes. Tokens stay exactly: portfolio `--bg #0b0b0d`, `--grid #1c1c22`, `--surface #121216`, `--text #f4f4f5`, `--muted #a1a1aa`, `--dim #3f3f46`, `--accent #3b6cff`; Settled `--bg #0a0a0a`, `--card #141414`, `--border #262626`, `--text #f5f5f5`, `--muted #a3a3a3`, `--accent #22c55e`, `--overdue #ef4444`. Any new CSS colour is a `var(--token)` or `rgba()` of a token's RGB.
- Pixel art only at integer scale with `image-rendering: pixelated`. Glove 1× (16×11) everywhere. Sprite 2× (32×48) below the page's breakpoint, 3× (48×72) from it (portfolio `min-width: 720px`, Settled `min-width: 721px`).
- Glove only on nav links, `.btn`, and the `.app` card — never on cards that aren't links, inline links in text, footer links, or the disabled Play badge.
- Every animation sits inside `@media (prefers-reduced-motion: no-preference)`. Without JS the pages show their complete, final content.
- Copy: the portfolio footer's right side reads exactly `End of status screen · Thanks for viewing`. Skill cards read `Exp` … `7+ yrs` (uppercased by CSS). All other copy unchanged.
- Commit after every task; messages end with the line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Working directory for every command: `E:\Hans\Projects\Web App Dev Page` (branch `main`). Use the Write/Edit tools for multi-line file content (long Bash heredocs fail on Windows). Git's LF→CRLF warnings are fine.
- Browser checks: start the server with the built-in browser's `preview_start` `{name: "site"}` (serves the repo root at `http://127.0.0.1:8000`). Never start servers from Bash.

---

## File map

| Path | Responsibility |
|---|---|
| `scripts/make_sprites.py` | **New.** The pixel grids (mini-Hans walk cycle, glove) as text; validates and writes the PNGs. |
| `assets/game/hans-walk.png` | **New, generated.** 64×48 sheet: 4 frames × 16×24; row 0 blue logo pixel, row 1 green. |
| `assets/game/glove.png` | **New, generated.** 16×11 pointer glove. |
| `assets/game/game.js` | **New.** `window.hansGame.start(options)`; typewriter, reveal, scroll-spy, walker pause. Auto-starts unless `window.hansGameManual`. |
| `tests/game-test.html` | **New.** Fixtures + assertions for `game.js`; prints `ALL PASS` or failures into `#result`. |
| `scripts/check_site.py` | Modified. PNG-size check, one-deferred-script rule, `data-*` markup counts, new portfolio copy checks, Settled hero checks. |
| `index.html` | Modified. Portfolio: game CSS block, `data-*` attributes, EXP rows, walker, footer copy. |
| `settled/index.html` | Modified. Settled: game CSS block, reveal rework, hero dialog, phone swap, walker. |
| `settled/privacy.html` | Modified. Nav glove + walker only. |

---

### Task 1: Pixel art — `make_sprites.py` and the two PNGs

**Files:**
- Create: `scripts/make_sprites.py`
- Create (generated): `assets/game/hans-walk.png`, `assets/game/glove.png`
- Modify: `scripts/check_site.py` (docstring line 1, `check_screens` lines 181–198, `CHECKS` lines 359–371)

**Interfaces:**
- Produces: `assets/game/hans-walk.png` (64×48; frame *k* of row *r* at x = 16k, y = 24r; frame order stand, stepA, stand, stepB; row 0 blue, row 1 green) and `assets/game/glove.png` (16×11). Later tasks reference these by URL only.
- Produces: `png_size(path: Path) -> tuple[int, int]` in `check_site.py`.

- [ ] **Step 1: Write the failing check**

In `scripts/check_site.py`, replace line 1 with:

```python
"""Static checks for hansukun.github.io (portfolio + Settled). Run: python scripts/check_site.py"""
```

Replace the whole `check_screens` function and the `SCREENS` line above it with:

```python
SCREENS = ["month", "month-settled", "template", "history", "settings"]


def png_size(p: Path) -> tuple[int, int]:
    head = p.read_bytes()[:24]
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")   # IHDR


def check_screens(_: str) -> list[str]:
    out = []
    for s in SCREENS:
        for ext in ("webp", "png"):
            p = ROOT / "settled" / "assets" / "screens" / f"{s}.{ext}"
            if not p.exists():
                out.append(f"missing settled/assets/screens/{s}.{ext}")
                continue
            if ext == "png":
                w, h = png_size(p)
                if w != 720 or abs(h - 1180) > 4:
                    out.append(f"settled/assets/screens/{s}.png is {w}x{h}, expected 720x1180")
    return out


GAME_ASSETS = {"assets/game/hans-walk.png": (64, 48), "assets/game/glove.png": (16, 11)}


def check_game_assets(_: str) -> list[str]:
    out = []
    for f, want in GAME_ASSETS.items():
        p = ROOT / f
        if not p.exists():
            out.append(f"missing {f} (run python scripts/make_sprites.py)")
        elif png_size(p) != want:
            w, h = png_size(p)
            out.append(f"{f} is {w}x{h}, expected {want[0]}x{want[1]}")
    return out
```

In `CHECKS`, add after the `("screens", …)` line:

```python
    ("game-assets", check_game_assets, [None]),
```

- [ ] **Step 2: Run the checker to see it fail**

Run: `python scripts/check_site.py`
Expected: exit 1 with exactly these two failures:
```
[game-assets] missing assets/game/hans-walk.png (run python scripts/make_sprites.py)
[game-assets] missing assets/game/glove.png (run python scripts/make_sprites.py)
```

- [ ] **Step 3: Write `scripts/make_sprites.py`**

```python
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
```

- [ ] **Step 4: Generate the PNGs and run the checker**

Run: `python scripts/make_sprites.py`
Expected: `wrote assets/game/hans-walk.png (64x48) and assets/game/glove.png (16x11)`

Run: `python scripts/check_site.py`
Expected: `all checks passed`

- [ ] **Step 5: Confirm the validator catches a broken grid**

Temporarily delete one `.` from the end of the first `HEAD` row, run `python scripts/make_sprites.py`.
Expected: exit 1 with `head row 0: 15 columns, expected 16`. Restore the row, re-run: the success line again.

- [ ] **Step 6: Confirm generation is deterministic**

Run: `git add assets/game && python scripts/make_sprites.py && git status --short assets/game`
Expected: both PNGs listed as `A ` only — no ` M` (a re-run produced identical bytes).

- [ ] **Step 7: Eyeball the art**

Run: `python -c "from PIL import Image; im=Image.open('assets/game/hans-walk.png'); im.resize((im.width*8, im.height*8), Image.NEAREST).save('.superpowers/hans-walk-8x.png'); g=Image.open('assets/game/glove.png'); g.resize((g.width*8, g.height*8), Image.NEAREST).save('.superpowers/glove-8x.png')"`
Then Read `.superpowers/hans-walk-8x.png` and `.superpowers/glove-8x.png`. Expected: row 0 matches the approved `sprite-v3.html` preview (messy black hair with blue sheen, no glasses, black tee, blue logo pixel, jeans, white sneakers; frames 2 and 4 have the head 1px lower and legs apart); row 1 identical except a green logo pixel; the glove is a white glove pointing right with a grey cuff. (`.superpowers/` is gitignored.)

- [ ] **Step 8: Commit**

```bash
git add scripts/make_sprites.py scripts/check_site.py assets/game/hans-walk.png assets/game/glove.png
git commit -m "feat: pixel-art sprite sheet and glove, drawn from text grids

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: `game.js`, its test page, and the one-script rule

**Files:**
- Create: `tests/game-test.html`
- Create: `assets/game/game.js`
- Modify: `scripts/check_site.py` (imports, constants, `Page`, `check_files_exist`, `check_page_basics`)
- Modify: `index.html` (head), `settled/index.html` (head), `settled/privacy.html` (head)

**Interfaces:**
- Produces: `window.hansGame.start(options)` where `options` = `{ root?: ParentNode = document, reduced?: boolean (omit = follow prefers-reduced-motion and watch for changes), charMs?: number = 30, startDelay?: number = 400 }`. Auto-called once on page load unless `window.hansGameManual === true`.
- Produces: the `js` class on `<html>`; DOM contract used by Tasks 3–5:
  - `[data-type]` — typed box. Gets `.is-done` when finished (or immediately under reduced motion). While typing: `tabindex="0"`, children replaced by a screen-reader copy (first child) and an `aria-hidden="true"` typed copy.
  - `[data-reveal]` — gets `.is-in` once it is ≥20% in view (immediately under reduced motion or without IntersectionObserver).
  - `[data-spy]` on an `<a href="#id">` — gets `aria-current="true"` while section `#id` crosses the 45–50% band of the viewport; removed otherwise.
  - `[data-walker]` — gets `.is-paused` while off-screen, `.is-still` under reduced motion.
- Produces: `GAME_JS = "assets/game/game.js"` and `import os` in `check_site.py`.

- [ ] **Step 1: Write the test page**

Create `tests/game-test.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex">
  <title>game.js tests</title>
  <style>body { font: 14px/1.4 monospace; margin: 16px; } #result { white-space: pre; }</style>
</head>
<body>
  <pre id="result">running…</pre>

  <div id="reduced">
    <p id="t0" data-type>Hello <b>big</b> world.</p>
    <div id="r0" data-reveal>reduced reveal</div>
    <div id="w0" data-walker>reduced walker</div>
  </div>

  <div id="slow">
    <p id="t2" data-type>Slow text here.</p>
  </div>

  <div id="normal">
    <p id="t1" data-type>Hello <b>big</b> world.</p>
    <div id="r1" data-reveal>near reveal</div>
    <div id="w1" data-walker>near walker</div>
    <div style="height: 3000px"></div>
    <div id="r2" data-reveal>far reveal</div>
    <div id="w2" data-walker>far walker</div>
    <nav><a id="l1" data-spy href="#s1">one</a> <a id="l2" data-spy href="#s2">two</a></nav>
    <section id="s1" style="height: 120vh">section one</section>
    <section id="s2" style="height: 120vh">section two</section>
  </div>

  <script>window.hansGameManual = true;</script>
  <script src="../assets/game/game.js"></script>
  <script>
    const results = [];
    const check = (name, cond) => results.push((cond ? "PASS " : "FAIL ") + name);
    const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    const $ = (id) => document.getElementById(id);
    const typedCopy = (box) => box.querySelector('[aria-hidden="true"]');
    const stillHidden = (box) => !!typedCopy(box).querySelector('[style*="visibility"]');

    (async () => {
      hansGame.start({ root: $("reduced"), reduced: true });
      hansGame.start({ root: $("slow"), reduced: false, charMs: 1000, startDelay: 0 });
      hansGame.start({ root: $("normal"), reduced: false, charMs: 1, startDelay: 0 });

      check("html gets the js class", document.documentElement.classList.contains("js"));

      check("reduced: typed box is left as written", $("t0").textContent === "Hello big world." && !typedCopy($("t0")));
      check("reduced: typed box is marked done", $("t0").classList.contains("is-done"));

      const t1 = $("t1");
      check("typed copy is aria-hidden", !!typedCopy(t1));
      check("typed copy keeps <b>", !!(typedCopy(t1) && typedCopy(t1).querySelector("b")));
      check("screen-reader copy holds the full sentence", t1.firstElementChild.textContent === "Hello big world.");
      check("focusable while typing", t1.getAttribute("tabindex") === "0");
      check("starts with characters hidden", stillHidden(t1));
      await wait(400);
      check("finishes typing", t1.classList.contains("is-done") && !stillHidden(t1));
      check("not focusable once done", !t1.hasAttribute("tabindex"));

      const t2 = $("t2");
      check("slow box still typing", !t2.classList.contains("is-done"));
      t2.click();
      check("click skips to the end", t2.classList.contains("is-done") && !stillHidden(t2));

      check("reduced: reveal is immediate", $("r0").classList.contains("is-in"));
      check("reduced: walker is still", $("w0").classList.contains("is-still"));
      await wait(200);
      check("reveals an element in view", $("r1").classList.contains("is-in"));
      check("does not reveal an element far below", !$("r2").classList.contains("is-in"));
      check("walker in view is not paused", !$("w1").classList.contains("is-paused"));
      check("walker off-screen is paused", $("w2").classList.contains("is-paused"));
      check("no nav link current at the top", !document.querySelector("#normal [aria-current]"));

      $("r2").scrollIntoView({ block: "center" });
      await wait(300);
      check("reveals an element once scrolled to", $("r2").classList.contains("is-in"));
      check("walker resumes when scrolled to", !$("w2").classList.contains("is-paused"));

      $("s2").scrollIntoView();
      await wait(300);
      check("current link follows the section in view",
        $("l2").getAttribute("aria-current") === "true" && !$("l1").hasAttribute("aria-current"));

      const failed = results.filter((r) => r.startsWith("FAIL")).length;
      $("result").textContent = results.join("\n") + "\n" + (failed ? failed + " FAILED" : "ALL PASS");
      window.scrollTo(0, 0);
    })().catch((e) => { $("result").textContent = "ERROR " + e.message; });
  </script>
</body>
</html>
```

- [ ] **Step 2: Run the test page to see it fail**

Start the server with `preview_start` `{name: "site"}`, navigate the tab to `http://127.0.0.1:8000/tests/game-test.html`, then `get_page_text`.
Expected: the result reads `ERROR hansGame is not defined` (the script file doesn't exist yet).

- [ ] **Step 3: Write `assets/game/game.js`**

```js
/* Game accents for hansukun.github.io.
   Design: docs/superpowers/specs/2026-09-25-jrpg-accents-design.md
   Opt-in per element: [data-type] typewriter, [data-reveal] reveal-on-view,
   [data-spy] nav scroll-spy, [data-walker] sprite pause. Visuals live in each page's CSS. */
(() => {
  "use strict";
  document.documentElement.classList.add("js");

  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const hasIO = "IntersectionObserver" in window;
  const SR_ONLY = "position:absolute;width:1px;height:1px;margin:-1px;padding:0;" +
    "overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0";

  // Types a box's text one character at a time. Screen readers get an untouched copy;
  // the typed copy is aria-hidden and keeps its layout because hidden characters still
  // take up space.
  function typewriter(box, reduced, charMs, startDelay) {
    if (reduced) {
      box.classList.add("is-done");
      return { finish() {} };
    }
    const full = document.createElement("span");
    full.style.cssText = SR_ONLY;
    while (box.firstChild) full.appendChild(box.firstChild);
    const shown = full.cloneNode(true);
    shown.removeAttribute("style");
    shown.setAttribute("aria-hidden", "true");

    const textNodes = [];
    const walk = document.createTreeWalker(shown, NodeFilter.SHOW_TEXT);
    while (walk.nextNode()) textNodes.push(walk.currentNode);
    const chars = [];
    for (const node of textNodes) {
      const frag = document.createDocumentFragment();
      for (const ch of node.nodeValue) {
        const span = document.createElement("span");
        span.textContent = ch;
        span.style.visibility = "hidden";
        chars.push(span);
        frag.appendChild(span);
      }
      node.replaceWith(frag);
    }
    box.append(full, shown);
    box.tabIndex = 0;

    let next = 0;
    let timer = 0;
    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      chars.forEach((c) => { c.style.visibility = ""; });
      box.classList.add("is-done");
      box.removeAttribute("tabindex");
    };
    const tick = () => {
      if (next >= chars.length) return finish();
      chars[next++].style.visibility = "";
      timer = setTimeout(tick, charMs);
    };
    box.addEventListener("click", finish);
    box.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        finish();
      }
    });
    timer = setTimeout(tick, startDelay);
    return { finish };
  }

  // Adds .is-in to each element the first time it is at least 20% in view.
  function reveal(els, reduced) {
    if (reduced || !hasIO) {
      els.forEach((el) => el.classList.add("is-in"));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }
      }
    }, { threshold: 0.2 });
    els.forEach((el) => io.observe(el));
  }

  // Marks the nav link whose section crosses the middle of the viewport.
  function spy(links) {
    const bySection = new Map();
    for (const a of links) {
      const id = (a.getAttribute("href") || "").split("#")[1];
      const section = id && document.getElementById(id);
      if (section) bySection.set(section, a);
    }
    if (!bySection.size || !hasIO) return;
    const inBand = new Set();
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) inBand.add(e.target);
        else inBand.delete(e.target);
      }
      let current = null;
      bySection.forEach((a, section) => {
        if (!current && inBand.has(section)) current = section;
      });
      bySection.forEach((a, section) => {
        if (section === current) a.setAttribute("aria-current", "true");
        else a.removeAttribute("aria-current");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    bySection.forEach((a, section) => io.observe(section));
  }

  // Pauses a walking sprite while it is off-screen; holds it still under reduced motion.
  function walker(el, reduced) {
    if (reduced) el.classList.add("is-still");
    if (!hasIO) return;
    new IntersectionObserver((entries) => {
      for (const e of entries) el.classList.toggle("is-paused", !e.isIntersecting);
    }).observe(el);
  }

  function start(options) {
    const opts = options || {};
    const root = opts.root || document;
    const followSystem = opts.reduced === undefined;
    const reduced = followSystem ? motion.matches : opts.reduced;
    const charMs = "charMs" in opts ? opts.charMs : 30;
    const startDelay = "startDelay" in opts ? opts.startDelay : 400;
    const all = (sel) => Array.from(root.querySelectorAll(sel));

    const typers = all("[data-type]").map((box) => typewriter(box, reduced, charMs, startDelay));
    const reveals = all("[data-reveal]");
    reveal(reveals, reduced);
    spy(all("[data-spy]"));
    const walkers = all("[data-walker]");
    walkers.forEach((el) => walker(el, reduced));

    if (followSystem) {
      motion.addEventListener("change", () => {
        if (motion.matches) {
          typers.forEach((t) => t.finish());
          reveals.forEach((el) => el.classList.add("is-in"));
          walkers.forEach((el) => el.classList.add("is-still"));
        } else {
          walkers.forEach((el) => el.classList.remove("is-still"));
        }
      });
    }
  }

  window.hansGame = { start };
  if (!window.hansGameManual) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", () => start());
    else start();
  }
})();
```

- [ ] **Step 4: Run the test page to see it pass**

Reload `http://127.0.0.1:8000/tests/game-test.html`, wait ~2s, `get_page_text`.
Expected: 22 `PASS` lines and a final `ALL PASS`. `read_console_messages` with `onlyErrors: true` shows nothing.

- [ ] **Step 5: Write the failing one-script check**

In `scripts/check_site.py`:

Add `import os` to the imports (alphabetical, above `import re`).

After the `ALLOWED_EXTERNAL_HOSTS` line add:

```python
GAME_JS = "assets/game/game.js"
```

In `Page.__init__`, replace the two lines

```python
        self.script_srcs: list[str] = []
        self.inline_scripts = 0
```

with

```python
        self.scripts: list[dict[str, str | None]] = []
        self.inline_scripts = 0
```

In `Page.handle_starttag`, replace the `if tag == "script":` block with:

```python
        if tag == "script":
            self._in_script = True
            self.scripts.append(a)
            if "src" not in a:
                self.inline_scripts += 1
```

Add a helper after `host_of`:

```python
def rel(page: Page, target: str) -> str:
    """`target` (repo-root relative) as seen from `page`'s directory, with / separators."""
    return os.path.relpath(ROOT / target, page.dir).replace(os.sep, "/")
```

In `check_files_exist`, add `GAME_JS` to the list (after `"settled/assets/icon-512.png"`).

In `check_page_basics`, replace

```python
    if page.inline_scripts or page.script_srcs:
        out.append(f"{name}: pages must not contain <script>")
```

with

```python
    if page.inline_scripts:
        out.append(f"{name}: inline <script> is not allowed")
    want = rel(page, GAME_JS)
    if not (len(page.scripts) == 1 and page.scripts[0].get("src") == want and "defer" in page.scripts[0]):
        out.append(f'{name}: must load exactly one <script src="{want}" defer>')
```

- [ ] **Step 6: Run the checker to see it fail**

Run: `python scripts/check_site.py`
Expected: exit 1 with exactly three failures:
```
[basics] index.html: must load exactly one <script src="assets/game/game.js" defer>
[basics] settled/index.html: must load exactly one <script src="../assets/game/game.js" defer>
[basics] settled/privacy.html: must load exactly one <script src="../assets/game/game.js" defer>
```

- [ ] **Step 7: Load the script on all three pages**

In `index.html`, directly after the Google Fonts `<link rel="stylesheet" …>` line, add:

```html
  <script src="assets/game/game.js" defer></script>
```

In `settled/index.html` and `settled/privacy.html`, directly after their Google Fonts `<link rel="stylesheet" …>` line, add:

```html
  <script src="../assets/game/game.js" defer></script>
```

- [ ] **Step 8: Run the checker to see it pass**

Run: `python scripts/check_site.py`
Expected: `all checks passed`

Load `http://127.0.0.1:8000/` and run `javascript_tool`: `document.documentElement.className + " " + typeof hansGame`
Expected: `js object`. No console errors.

- [ ] **Step 9: Commit**

```bash
git add assets/game/game.js tests/game-test.html scripts/check_site.py index.html settled/index.html settled/privacy.html
git commit -m "feat: shared game.js with in-browser tests; pages load it

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Portfolio accents

**Files:**
- Modify: `scripts/check_site.py` (`PORTFOLIO_COPY`, `check_portfolio`, new `GAME_MARKUP` / `GAME_FORBID` / `check_game_markup`, `CHECKS`)
- Modify: `index.html` (end of `<style>`, `.btn-row` rule, nav links, `.lead`, skill cards, footer)

**Interfaces:**
- Consumes: `rel(page, target)` and `GAME_JS` from Task 2; the `data-*` contract and `.js` / `.is-in` / `.is-done` / `.is-paused` / `.is-still` classes from Task 2; `assets/game/glove.png`, `assets/game/hans-walk.png` from Task 1.
- Produces: `GAME_MARKUP: dict[str, dict[str, int]]` and `GAME_FORBID: dict[str, list[str]]` in `check_site.py` — Tasks 4 and 5 add their pages' entries.

- [ ] **Step 1: Write the failing checks**

In `scripts/check_site.py`, add `"End of status screen · Thanks for viewing",` as the last item of `PORTFOLIO_COPY`.

At the end of `check_portfolio`, before `return out`, add:

```python
    if "Built with plain HTML" in page.text:
        out.append(f"{name}: old 'Built with plain HTML & CSS' footer note is still there")
    if page.text.count("7+ yrs") != 3:
        out.append(f"{name}: each of the three skill cards needs an 'Exp … 7+ yrs' row")
```

After `check_portfolio`, add:

```python
# Expected counts of each game attribute per page; attributes are matched in markup only.
GAME_MARKUP: dict[str, dict[str, int]] = {
    PORTFOLIO: {"data-type": 1, "data-reveal": 3, "data-spy": 3, "data-walker": 1},
}
GAME_FORBID: dict[str, list[str]] = {}


def check_game_markup(name: str) -> list[str]:
    want = GAME_MARKUP.get(name)
    page = load(name)
    if want is None or page is None:
        return []
    out = []
    for attr, n in want.items():
        got = len(re.findall(rf"\s{attr}[\s>=]", page.html))
        if got != n:
            out.append(f"{name}: expected {n} x {attr}, found {got}")
    for asset in ("assets/game/glove.png", "assets/game/hans-walk.png"):
        ref = rel(page, asset)
        if f'url("{ref}")' not in page.html:
            out.append(f'{name}: CSS must use url("{ref}")')
    for s in GAME_FORBID.get(name, []):
        if s in page.html:
            out.append(f"{name}: must not contain {s!r}")
    return out
```

In `CHECKS`, add as the last entry:

```python
    ("game", check_game_markup, PAGES),
```

- [ ] **Step 2: Run the checker to see it fail**

Run: `python scripts/check_site.py`
Expected: exit 1; failures are exactly the portfolio ones:
```
[portfolio] index.html: copy 'End of status screen · Thanks for viewing' missing
[portfolio] index.html: old 'Built with plain HTML & CSS' footer note is still there
[portfolio] index.html: each of the three skill cards needs an 'Exp … 7+ yrs' row
[game] index.html: expected 1 x data-type, found 0
[game] index.html: expected 3 x data-reveal, found 0
[game] index.html: expected 3 x data-spy, found 0
[game] index.html: expected 1 x data-walker, found 0
[game] index.html: CSS must use url("assets/game/glove.png")
[game] index.html: CSS must use url("assets/game/hans-walk.png")
```

- [ ] **Step 3: Add the game CSS block**

In `index.html`, change `.btn-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }` to use `gap: 16px;` (room for the glove between buttons).

Insert this block immediately before `  </style>`:

```css
    /* ---- game accents — docs/superpowers/specs/2026-09-25-jrpg-accents-design.md ---- */

    /* glove cursor: 1x, fingertip overlapping the element's left edge by 2px */
    .nav-links a, .btn, .app { position: relative; }
    .nav-links a::before, .btn::before, .app::before {
      content: "";
      position: absolute; top: 50%; right: 100%;
      width: 16px; height: 11px;
      margin: -6px -2px 0 0;
      background: url("assets/game/glove.png") no-repeat;
      image-rendering: pixelated;
      visibility: hidden;
      pointer-events: none;
    }
    .btn:hover::before, .btn:focus-visible::before,
    .app:hover::before, .app:focus-visible::before { visibility: visible; }
    .nav-links a[aria-current] { color: var(--accent); }

    /* hero dialog box; game.js types into it and adds .is-done */
    .dialog {
      position: relative;
      max-width: 520px;
      padding: 14px 18px 24px;
      border: 2px solid var(--text);
      background: var(--surface);
      box-shadow: 4px 4px 0 var(--accent);
    }
    .dialog.is-done::after {
      content: "▼";
      content: "▼" / "";
      position: absolute; right: 10px; bottom: 4px;
      font-size: 11px;
      color: var(--accent);
    }

    /* hero: scanline stage, shine clip */
    .hero { position: relative; overflow: hidden; }
    .hero > .container { position: relative; }
    h1 .block { position: relative; clip-path: inset(0); }

    /* EXP bars on the skill cards */
    .exp {
      display: flex; align-items: center; gap: 8px;
      margin-top: 14px;
      font-family: var(--mono); font-size: 11px; letter-spacing: .06em; text-transform: uppercase;
      color: var(--muted);
    }
    .exp-bar { flex: 1; height: 6px; border: 1px solid var(--dim); }
    .exp-bar i { display: block; height: 100%; background: var(--accent); transform-origin: left; }

    /* walking mini-Hans on the footer's top border */
    .contact { padding-bottom: 80px; }
    .footer { position: relative; }
    .walker { position: absolute; left: 0; right: 0; bottom: calc(100% + 2px); height: 48px; pointer-events: none; }
    .walker i {
      position: absolute; left: 0; bottom: 0;
      width: 32px; height: 48px;
      background: url("assets/game/hans-walk.png") 0 0 / 400% 200% no-repeat;
      image-rendering: pixelated;
    }
    .walker.is-paused, .walker.is-paused i { animation-play-state: paused; }
    .walker.is-still, .walker.is-still i { animation: none; }
    .walker.is-still i { left: var(--gutter); }

    @media (min-width: 720px) {
      .nav-links { gap: 28px; }
      .nav-links a[aria-current]::before,
      .nav-links a:hover::before,
      .nav-links a:focus-visible::before { visibility: visible; }
      .contact { padding-bottom: 104px; }
      .walker { height: 72px; }
      .walker i { width: 48px; height: 72px; }
    }

    @media (prefers-reduced-motion: no-preference) {
      .nav-links a::before, .btn::before, .app::before { animation: glove-bob .7s steps(1, end) infinite; }
      .dialog.is-done::after { animation: blink 1s steps(1, end) infinite; }
      h1 .block::after {
        content: "";
        position: absolute; top: 0; bottom: 0; left: -40%;
        width: 30%;
        background: linear-gradient(90deg, transparent, rgba(244, 244, 245, .55), transparent);
        animation: shine 3.5s ease-in-out infinite;
        pointer-events: none;
      }
      .hero::before {
        content: "";
        position: absolute; inset: 0;
        background: linear-gradient(transparent calc(50% - 30px), rgba(59, 108, 255, .06), transparent calc(50% + 30px));
        animation: scan 6s linear infinite;
        pointer-events: none;
      }
      .js .card[data-reveal] .exp-bar i { transform: scaleX(0); transition: transform 1.2s ease-out var(--stagger, 0ms); }
      .js .card[data-reveal].is-in .exp-bar i { transform: none; }
      .walker { animation: walk 12s linear infinite; }
      .walker i { animation: walk-frames .64s steps(4) infinite; }
    }
    @media (prefers-reduced-motion: reduce) {
      .walker i { left: var(--gutter); }
    }

    @keyframes glove-bob { 0%, 100% { transform: none; } 50% { transform: translateX(-4px); } }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
    @keyframes shine {
      from { transform: translateX(0) skewX(-20deg); }
      60%, to { transform: translateX(560%) skewX(-20deg); }
    }
    @keyframes scan { from { transform: translateY(-55%); } to { transform: translateY(55%); } }
    @keyframes walk { from { transform: translateX(-48px); } to { transform: translateX(100%); } }
    @keyframes walk-frames { to { background-position-x: 133.333%; } }
```

Notes for the implementer: the block goes after the existing media queries on purpose, so `.contact { padding-bottom }` beats the mobile `.section { padding: 48px 0 }`. `background-position-x: 133.333%` with a 400%-wide background steps through frames 0→3 (`k/3` per frame). `translateX(560%)` of a band 30% as wide as the block carries it from −40% to past the right edge.

- [ ] **Step 4: Update the markup**

Nav — replace the three nav links:

```html
        <a href="#skills" data-spy>Skills</a>
        <a href="#apps" data-spy>Apps</a>
        <a href="#contact" data-spy>Contact</a>
```

Hero — change `<p class="lead">` to `<p class="lead dialog" data-type>` (its content stays exactly as is).

Skill cards — replace the three `<div class="card">…</div>` blocks inside `.skills` with:

```html
          <div class="card" data-reveal style="--stagger: 0ms">
            <h3>WordPress</h3>
            <p>Custom themes and plugins, block editor, WooCommerce, performance and hosting.</p>
            <div class="tags"><span class="tag">PHP</span><span class="tag">Gutenberg</span><span class="tag">ACF</span><span class="tag">WooCommerce</span></div>
            <div class="exp"><span>Exp</span><span class="exp-bar" aria-hidden="true"><i></i></span><span>7+ yrs</span></div>
          </div>
          <div class="card" data-reveal style="--stagger: 150ms">
            <h3>React</h3>
            <p>Component-driven front ends, hooks, state, and integration with REST/GraphQL APIs.</p>
            <div class="tags"><span class="tag">TypeScript</span><span class="tag">Next.js</span><span class="tag">Tailwind</span></div>
            <div class="exp"><span>Exp</span><span class="exp-bar" aria-hidden="true"><i></i></span><span>7+ yrs</span></div>
          </div>
          <div class="card" data-reveal style="--stagger: 300ms">
            <h3>Vue</h3>
            <p>Vue 3 with the Composition API, Pinia, and Nuxt for full apps and admin UIs.</p>
            <div class="tags"><span class="tag">Vue 3</span><span class="tag">Pinia</span><span class="tag">Nuxt</span></div>
            <div class="exp"><span>Exp</span><span class="exp-bar" aria-hidden="true"><i></i></span><span>7+ yrs</span></div>
          </div>
```

Footer — replace the whole `<footer class="footer">…</footer>` with:

```html
  <footer class="footer">
    <div class="walker" data-walker aria-hidden="true"><i></i></div>
    <div class="container">
      <span>© 2026 Hans De Guzman</span>
      <span>End of status screen · Thanks for viewing</span>
    </div>
  </footer>
```

- [ ] **Step 5: Run the checker to see it pass**

Run: `python scripts/check_site.py`
Expected: `all checks passed`

- [ ] **Step 6: Check it in the browser (desktop)**

Load `http://127.0.0.1:8000/` in the `site` tab at desktop size. Then:
1. Wait 5s; `javascript_tool`: `document.querySelector(".lead").classList.contains("is-done") && document.querySelector(".lead").firstElementChild.textContent` → the full tagline string.
2. Scroll to `#skills`, wait 2s; `javascript_tool`: `[...document.querySelectorAll(".skills .card")].every(c => c.classList.contains("is-in")) && document.querySelector('.nav-links a[href="#skills"]').getAttribute("aria-current")` → `"true"`.
3. `javascript_tool`: `getComputedStyle(document.querySelector('.nav-links a[href="#skills"]'), "::before").visibility` → `"visible"`.
4. Scroll to the bottom; `javascript_tool`: `document.querySelector(".walker").classList.contains("is-paused")` → `false`. Scroll to the top; same expression → `true`.
5. `javascript_tool`: `document.documentElement.scrollWidth <= innerWidth` → `true`.
6. Screenshot the hero (dialog with ▼, shine on WEB DEV), the skills section (full bars, `7+ YRS`), and the footer (sprite on the border line, new copy).
7. `read_console_messages` `onlyErrors: true` → none.

- [ ] **Step 7: Check it at phone width**

`resize_window` preset `mobile`, reload. Repeat checks 5 and 7; screenshot hero, skills and footer. Expected: dialog wraps without overflow, the nav shows no glove (active link is blue), the sprite is 32×48 and clears the contact buttons. `resize_window` preset `desktop` when done.

- [ ] **Step 8: Commit**

```bash
git add index.html scripts/check_site.py
git commit -m "feat: portfolio JRPG accents — glove, typed dialog, shine, scanline, EXP bars, walker

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Settled page accents

**Files:**
- Modify: `scripts/check_site.py` (`GAME_MARKUP`, `GAME_FORBID`, `check_hero`)
- Modify: `settled/index.html` (reduced-motion block lines 150–155, end of `<style>`, nav links, hero lead, hero phone, cards, strip figures, footer)

**Interfaces:**
- Consumes: `GAME_MARKUP`, `GAME_FORBID`, `check_game_markup` (Task 3); `game.js` contract (Task 2); sheet row 1 (green) of `hans-walk.png` and `glove.png` (Task 1).

- [ ] **Step 1: Write the failing checks**

In `scripts/check_site.py`, add to `GAME_MARKUP`:

```python
    "settled/index.html": {"data-type": 1, "data-reveal": 16, "data-spy": 2, "data-walker": 1},
```

and set:

```python
GAME_FORBID: dict[str, list[str]] = {"settled/index.html": ["animation-timeline"]}
```

At the end of `check_hero`, before `return out`, add:

```python
    if not re.search(r'class="phone hero-phone" data-reveal>.*?screens/month-settled\.webp', page.html, re.S):
        out.append(f"{name}: hero phone must stack month-settled for the SETTLED! moment")
    if '<span class="settled-pop" aria-hidden="true">Settled!</span>' not in page.html:
        out.append(f"{name}: hero phone needs the aria-hidden 'Settled!' pop")
```

- [ ] **Step 2: Run the checker to see it fail**

Run: `python scripts/check_site.py`
Expected: exit 1; failures only for `settled/index.html` — the two `[hero]` lines, four `[game] … expected … found 0` lines, the two `CSS must use url("../assets/game/…")` lines, and `must not contain 'animation-timeline'`.

- [ ] **Step 3: Replace the old scroll-reveal CSS**

In `settled/index.html`, delete this block (lines 150–155) entirely:

```css
    @media (prefers-reduced-motion: no-preference) {
      @supports (animation-timeline: view()) {
        .card, .strip figure { animation: rise .6s ease-out both; animation-timeline: view(); animation-range: entry 0% entry 30%; }
      }
      @keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
    }
```

- [ ] **Step 4: Add the game CSS block**

Insert immediately before `  </style>`:

```css
    /* ---- game accents — docs/superpowers/specs/2026-09-25-jrpg-accents-design.md ---- */

    /* glove cursor on nav links (desktop only), 1x */
    .nav-links a { position: relative; }
    .nav-links a::before {
      content: "";
      position: absolute; top: 50%; right: 100%;
      width: 16px; height: 11px;
      margin: -6px -2px 0 0;
      background: url("../assets/game/glove.png") no-repeat;
      image-rendering: pixelated;
      visibility: hidden;
      pointer-events: none;
    }
    .nav-links a[aria-current] { color: var(--accent); }

    /* hero dialog box */
    .dialog {
      position: relative;
      padding: 14px 18px 26px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
    }
    .dialog.is-done::after {
      content: "▼";
      content: "▼" / "";
      position: absolute; right: 14px; bottom: 6px;
      font-size: 11px;
      color: var(--accent);
    }

    /* hero phone: month-settled stacked on top, pop badge */
    .hero-phone .shot-settled { position: absolute; inset: 8px; opacity: 0; }
    .settled-pop {
      position: absolute; left: 50%; top: 42%; z-index: 1;
      padding: 6px 14px;
      border-radius: 999px;
      background: var(--accent);
      color: var(--bg);
      font-family: var(--mono); font-size: 14px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
      opacity: 0;
      transform: translate(-50%, -50%) scale(0);
      pointer-events: none;
    }

    /* walking mini-Hans (green row) on the footer's top border */
    .footer { position: relative; }
    .walker { position: absolute; left: 0; right: 0; bottom: calc(100% + 1px); height: 48px; pointer-events: none; }
    .walker i {
      position: absolute; left: 0; bottom: 0;
      width: 32px; height: 48px;
      background: url("../assets/game/hans-walk.png") 0 100% / 400% 200% no-repeat;
      image-rendering: pixelated;
    }
    .walker.is-paused, .walker.is-paused i { animation-play-state: paused; }
    .walker.is-still, .walker.is-still i { animation: none; }
    .walker.is-still i { left: var(--gutter); }

    @media (min-width: 721px) {
      .nav-links { gap: 30px; }
      .nav-links a[aria-current]::before,
      .nav-links a:hover::before,
      .nav-links a:focus-visible::before { visibility: visible; }
      .walker { height: 72px; }
      .walker i { width: 48px; height: 72px; }
    }

    @media (prefers-reduced-motion: no-preference) {
      .nav-links a::before { animation: glove-bob .7s steps(1, end) infinite; }
      .dialog.is-done::after { animation: blink 1s steps(1, end) infinite; }
      @supports ((-webkit-background-clip: text) or (background-clip: text)) {
        .hero h1 em {
          background: linear-gradient(100deg, var(--accent) 40%, rgba(245, 245, 245, .95) 50%, var(--accent) 60%) 100% 0 / 300% 100%;
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          animation: glint 3.5s ease-in-out infinite;
        }
      }
      .hero-phone::after {
        content: "";
        position: absolute; inset: 8px;
        border-radius: 28px;
        background: linear-gradient(transparent 48%, rgba(34, 197, 94, .12) 50%, transparent 52%) 0 100% / 100% 300% no-repeat;
        animation: phone-scan 4s linear infinite;
        pointer-events: none;
      }
      .hero-phone.is-in .shot-settled { animation: shot-in .6s ease-out 2.5s both; }
      .hero-phone.is-in .settled-pop { animation: pop 2.2s ease-out 2.8s both; }
      .js .card[data-reveal], .js .strip figure[data-reveal] {
        opacity: 0;
        transform: translateY(14px);
        transition: opacity .6s ease-out, transform .6s ease-out;
      }
      .js .card[data-reveal].is-in, .js .strip figure[data-reveal].is-in { opacity: 1; transform: none; }
      .walker { animation: walk 12s linear infinite; }
      .walker i { animation: walk-frames .64s steps(4) infinite; }
    }
    @media (prefers-reduced-motion: reduce) {
      .walker i { left: var(--gutter); }
    }

    @keyframes glove-bob { 0%, 100% { transform: none; } 50% { transform: translateX(-4px); } }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
    @keyframes glint { 0% { background-position: 100% 0; } 60%, 100% { background-position: 0 0; } }
    @keyframes phone-scan { to { background-position: 0 0; } }
    @keyframes shot-in { from { opacity: 0; } to { opacity: 1; } }
    @keyframes pop {
      0% { opacity: 0; transform: translate(-50%, -50%) scale(0); }
      15% { opacity: 1; transform: translate(-50%, -50%) scale(1.25); }
      25%, 80% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
      100% { opacity: 0; transform: translate(-50%, -50%) scale(1); }
    }
    @keyframes walk { from { transform: translateX(-48px); } to { transform: translateX(100%); } }
    @keyframes walk-frames { to { background-position-x: 133.333%; } }
```

- [ ] **Step 5: Update the markup**

Nav — change `<a href="#features">Features</a>` to `<a href="#features" data-spy>Features</a>` and `<a href="#pricing">Pricing</a>` to `<a href="#pricing" data-spy>Pricing</a>`.

Hero lead — change `<p class="lead">` to `<p class="lead dialog" data-type>` (content unchanged).

Hero phone — replace

```html
          <div class="phone">
            <picture>
              <source srcset="assets/screens/month.webp" type="image/webp">
              <img src="assets/screens/month.png" alt="Settled's month screen: pools of expenses with a checkbox per item, due dates, and a progress bar of what's been paid" width="720" height="1180" fetchpriority="high">
            </picture>
          </div>
```

with

```html
          <div class="phone hero-phone" data-reveal>
            <picture>
              <source srcset="assets/screens/month.webp" type="image/webp">
              <img src="assets/screens/month.png" alt="Settled's month screen: pools of expenses with a checkbox per item, due dates, and a progress bar of what's been paid" width="720" height="1180" fetchpriority="high">
            </picture>
            <picture class="shot-settled">
              <source srcset="assets/screens/month-settled.webp" type="image/webp">
              <img src="assets/screens/month-settled.png" alt="" width="720" height="1180" loading="lazy">
            </picture>
            <span class="settled-pop" aria-hidden="true">Settled!</span>
          </div>
```

Cards and strip figures — run:

```bash
sed -i -E 's/<div class="card( price( price--accent)?)?">/<div class="card\1" data-reveal>/' settled/index.html
sed -i 's/<figure>/<figure data-reveal>/' settled/index.html
grep -o ' data-reveal[ >]' settled/index.html | wc -l
```

Expected count: `16` (markup only — the CSS selectors `[data-reveal]` have no leading space) (3 step cards + 6 feature cards + 2 price cards + 4 figures + the hero phone).

Footer — directly after `<footer class="footer">`, add:

```html
    <div class="walker" data-walker aria-hidden="true"><i></i></div>
```

- [ ] **Step 6: Run the checker to see it pass**

Run: `python scripts/check_site.py`
Expected: `all checks passed`

- [ ] **Step 7: Check it in the browser (desktop)**

Load `http://127.0.0.1:8000/settled/` at desktop size. Then:
1. Wait 5s; `javascript_tool`: `[document.querySelector(".hero .lead").classList.contains("is-done"), getComputedStyle(document.querySelector(".shot-settled")).opacity]` → `[true, "1"]`.
2. Screenshot within ~3s of a fresh reload to catch the `SETTLED!` pop over the phone (reload and screenshot again if missed); another screenshot after 6s shows the settled screen with the pop gone.
3. Scroll to `#features`, wait 1s; `javascript_tool`: `[document.querySelector('.nav-links a[href="#features"]').getAttribute("aria-current"), [...document.querySelectorAll("#features .card")].every(c => c.classList.contains("is-in"))]` → `["true", true]`.
4. Scroll the screens strip horizontally to its end; the last figure gets `.is-in` and fades up.
5. Scroll to the bottom; screenshot the footer — green-logo sprite walking on the 1px border above "© 2026 Settled".
6. `document.documentElement.scrollWidth <= innerWidth` → `true`; `read_console_messages` `onlyErrors: true` → none.

- [ ] **Step 8: Check it at phone width**

`resize_window` preset `mobile`, reload; repeat 1, 5 and 6 and screenshot the hero (phone above the text, dialog wrapping cleanly). `resize_window` preset `desktop` when done.

- [ ] **Step 9: Commit**

```bash
git add settled/index.html scripts/check_site.py
git commit -m "feat: Settled JRPG accents — glove, typed dialog, glint, SETTLED! phone, reveals, walker

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Privacy page — glove and walker

**Files:**
- Modify: `scripts/check_site.py` (`GAME_MARKUP`)
- Modify: `settled/privacy.html` (end of `<style>`, footer)

**Interfaces:**
- Consumes: `GAME_MARKUP` / `check_game_markup` (Task 3); `game.js` walker contract (Task 2); `glove.png` and sheet row 1 of `hans-walk.png` (Task 1).

- [ ] **Step 1: Write the failing check**

Add to `GAME_MARKUP`:

```python
    "settled/privacy.html": {"data-type": 0, "data-reveal": 0, "data-spy": 0, "data-walker": 1},
```

- [ ] **Step 2: Run the checker to see it fail**

Run: `python scripts/check_site.py`
Expected: exit 1 with exactly:
```
[game] settled/privacy.html: expected 1 x data-walker, found 0
[game] settled/privacy.html: CSS must use url("../assets/game/glove.png")
[game] settled/privacy.html: CSS must use url("../assets/game/hans-walk.png")
```

- [ ] **Step 3: Add the CSS**

In `settled/privacy.html`, insert immediately before `  </style>`:

```css
    /* ---- game accents (quiet subset) — docs/superpowers/specs/2026-09-25-jrpg-accents-design.md ---- */

    /* glove cursor on nav links (desktop only), 1x */
    .nav-links a { position: relative; }
    .nav-links a::before {
      content: "";
      position: absolute; top: 50%; right: 100%;
      width: 16px; height: 11px;
      margin: -6px -2px 0 0;
      background: url("../assets/game/glove.png") no-repeat;
      image-rendering: pixelated;
      visibility: hidden;
      pointer-events: none;
    }

    /* walking mini-Hans (green row) on the footer's top border */
    .footer { position: relative; }
    .walker { position: absolute; left: 0; right: 0; bottom: calc(100% + 1px); height: 48px; pointer-events: none; }
    .walker i {
      position: absolute; left: 0; bottom: 0;
      width: 32px; height: 48px;
      background: url("../assets/game/hans-walk.png") 0 100% / 400% 200% no-repeat;
      image-rendering: pixelated;
    }
    .walker.is-paused, .walker.is-paused i { animation-play-state: paused; }
    .walker.is-still, .walker.is-still i { animation: none; }
    .walker.is-still i { left: var(--gutter); }

    @media (min-width: 721px) {
      .nav-links { gap: 30px; }
      .nav-links a:hover::before,
      .nav-links a:focus-visible::before { visibility: visible; }
      .walker { height: 72px; }
      .walker i { width: 48px; height: 72px; }
    }

    @media (prefers-reduced-motion: no-preference) {
      .nav-links a::before { animation: glove-bob .7s steps(1, end) infinite; }
      .walker { animation: walk 12s linear infinite; }
      .walker i { animation: walk-frames .64s steps(4) infinite; }
    }
    @media (prefers-reduced-motion: reduce) {
      .walker i { left: var(--gutter); }
    }

    @keyframes glove-bob { 0%, 100% { transform: none; } 50% { transform: translateX(-4px); } }
    @keyframes walk { from { transform: translateX(-48px); } to { transform: translateX(100%); } }
    @keyframes walk-frames { to { background-position-x: 133.333%; } }
```

- [ ] **Step 4: Add the walker markup**

Directly after `<footer class="footer">`, add:

```html
    <div class="walker" data-walker aria-hidden="true"><i></i></div>
```

- [ ] **Step 5: Run the checker to see it pass**

Run: `python scripts/check_site.py`
Expected: `all checks passed`

- [ ] **Step 6: Check it in the browser**

Load `http://127.0.0.1:8000/settled/privacy.html` at desktop size. Hover `Features` in the nav and screenshot (glove left of it, not overlapping `← Hans De Guzman`). Scroll to the bottom and screenshot the sprite on the footer border (main's 96px bottom padding keeps it clear of the "← Back to Settled" link). Confirm the policy text is fully visible at once (no typing), `scrollWidth <= innerWidth`, no console errors.

- [ ] **Step 7: Commit**

```bash
git add settled/privacy.html scripts/check_site.py
git commit -m "feat: privacy page gets the nav glove and footer walker

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Cross-page verification

**Files:**
- Modify only if a check below fails: whichever page/CSS/JS the failure points to.

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Static checks**

Run: `python scripts/make_sprites.py && git status --short assets/game && python scripts/check_site.py`
Expected: the success line, no modified PNGs, `all checks passed`.

- [ ] **Step 2: game.js tests**

Load `http://127.0.0.1:8000/tests/game-test.html`, wait 2s, `get_page_text` → `ALL PASS`.

- [ ] **Step 3: Keyboard pass**

On `/` at desktop size: reload, immediately click the page body at the top and press Tab repeatedly (screenshot after each of the first 6 presses). Expected: focus goes `hansukun` → Skills → Apps → Contact → the hero dialog if it is still typing (press Enter there: the text completes, the ▼ shows, and the box drops out of the tab order; if typing already finished, the dialog is skipped — both are correct) → `Get in touch →` → `LinkedIn`; nav links and buttons show the glove plus the browser focus ring. Continue to the Settled app card: glove left of the card.

- [ ] **Step 4: JS-off content**

Run:

```bash
python -c "import urllib.request as u; h=u.urlopen('http://127.0.0.1:8000/').read().decode(); print(all(s in h for s in ['<b>WordPress</b>', 'End of status screen', '7+ yrs']))"
python -c "import urllib.request as u; h=u.urlopen('http://127.0.0.1:8000/settled/').read().decode(); print('the spreadsheet you already keep, as an app' in h)"
```

Expected: `True` twice — all copy is in the served HTML; nothing depends on JS to exist. (CSS hides reveal targets only under `.js`, which only the script sets.)

- [ ] **Step 5: Reduced-motion review**

For each of the three pages, read the game CSS block and confirm every `animation:` / `transition:` declaration sits inside `@media (prefers-reduced-motion: no-preference)` — run `grep -n "animation:\|transition:" index.html settled/index.html settled/privacy.html` and match each hit to a no-preference block (the only allowed hits outside one are `animation: none` in `.walker.is-still` and the pre-existing `.btn`/`.app` transitions, which already sit in the portfolio's no-preference block). In `game.js`, confirm the `reduced` branches: typewriter returns early with `.is-done`, reveal adds `.is-in` at once, walker adds `.is-still`.

- [ ] **Step 6: Visual sweep**

At desktop size and at `mobile`, screenshot the hero, first section and footer of all three pages. Check against the spec: nothing overlaps, the glove never covers text, the sprite sits on each footer's border line, no horizontal scroll (`scrollWidth <= innerWidth` on each), no console errors on any page. `resize_window` preset `desktop` at the end.

- [ ] **Step 7: Fix and commit (only if anything above failed)**

Fix at the source, re-run Steps 1–6 for the affected page, then:

```bash
git add -A -- index.html settled scripts assets tests
git commit -m "fix: JRPG accents verification fixes

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 8: Hand off**

Tell Hans what was verified, with screenshots, and ask him to spot-check once with Windows *Settings › Accessibility › Visual effects › Animation effects* turned off (the built-in browser can't emulate reduced motion): the dialog should appear already complete, bars full, the sprite standing still near the left of each footer, and the Settled phone staying on the month screen.
