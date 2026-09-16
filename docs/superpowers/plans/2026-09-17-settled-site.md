# Settled Brochure Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A dark-theme, one-page static brochure site for the Settled Android app plus a privacy policy page, deployable to GitHub Pages as-is.

**Architecture:** Two hand-written HTML files with inline CSS and no JavaScript, sharing one token set. Real device screenshots are captured over `adb`, cropped with Pillow, and embedded in CSS phone frames. A small Python checker script is the test suite: it parses the HTML and asserts structure, links, and assets.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, `clamp()`), Google Fonts (Inter, JetBrains Mono), Python 3.14 + Pillow (screenshot crops, checker), `adb` (captures).

**Spec:** `docs/superpowers/specs/2026-09-17-settled-site-design.md`

## Global Constraints

- Static files only: no build step, no framework, no JavaScript on the pages.
- Only external resources: Google Fonts stylesheet. No other scripts or third-party embeds.
- All asset paths are **relative** (`assets/...`), never root-absolute, because GitHub Pages may serve from a subpath.
- Colors are tokens on `:root`: bg `#0a0a0a`, card `#141414`, border `#262626`, text `#f5f5f5`, muted `#a3a3a3`, accent `#22c55e`, overdue `#ef4444`. `body` has an explicit background.
- Fonts: Inter for prose, JetBrains Mono for amounts, labels, step numbers, eyebrows.
- Layout: max content width 1080px, 16px side gutters, single column below 720px, no horizontal scroll at 375px wide.
- Phone frames scale with `clamp(220px, ..., 320px)`.
- Copy: the app is called **Settled**, Android only, "Coming soon to Google Play". Contact address: `deguzmanhans05@gmail.com`. Credit: "Built by Hans".
- No ad is ever visible in a screenshot on the site.
- Commit after every task with a `feat:`/`chore:`/`docs:` message ending in `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
- Working directory for every command: `E:\Hans\Projects\Web App Dev Page` (a git repo already exists there).
- The app source lives at `C:\Hans\Projects\Android\Budget Checklist` — read-only for this plan, except that Task 2 toggles one checkbox on the user's phone and restores it.
- Windows: long heredocs fail with `ENAMETOOLONG` in the Bash tool. Use the Write/Edit tools for files longer than ~40 lines.

---

## File map

| Path | Responsibility |
|---|---|
| `index.html` | The brochure. Inline `<style>` holds the whole stylesheet (tokens, base, every component). |
| `privacy.html` | Privacy policy. Copies the same `<style>` block. |
| `.nojekyll` | Tells GitHub Pages not to run Jekyll. |
| `assets/icon.svg` | App icon, copied from the app repo. |
| `assets/icon-512.png` | Play Store icon, copied from the app repo. |
| `assets/google-play-badge.svg` | Self-drawn greyed "Coming soon" badge (not Google's trademarked asset). |
| `assets/screens/{month,month-settled,template,history,settings}.{webp,png}` | Cropped device screenshots, 720px wide. |
| `scripts/check_site.py` | Test suite: parses both pages and asserts structure, links, assets, constraints. |
| `scripts/crop_screens.py` | Crops raw captures into `assets/screens/`. Kept so screenshots can be regenerated after the Play release. |

---

### Task 1: Checker script, scaffolding, and page skeleton

**Files:**
- Create: `scripts/check_site.py`
- Create: `.nojekyll`
- Create: `assets/icon.svg`, `assets/icon-512.png` (copies)
- Create: `index.html` (skeleton: head, full stylesheet, nav, empty main, footer)

**Interfaces:**
- Produces: `scripts/check_site.py` — run with `python scripts/check_site.py`; exit 0 on pass, 1 on failure, prints one line per failed check. Later tasks add checks to the `CHECKS` list; each check is a function `(name: str) -> list[str]` returning failure messages, and `CHECKS` entries are `(label, fn, targets)` where `targets` is a list of page names or `[None]`.
- Produces: CSS class names every later task uses: `.container`, `.eyebrow`, `.btn-badge`, `.phone`, `.phone img`, `.grid-3`, `.grid-2`, `.card`, `.section`, `.section-head`, `.strip`, `.price`, `.price--accent`, `.chip`, `.chip--accent`, `.mono`, `.muted`, `.prose`.

- [ ] **Step 1: Write the checker with the first checks (they must fail before the page exists)**

```python
# scripts/check_site.py
"""Static checks for the Settled brochure site. Run: python scripts/check_site.py"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "privacy.html"]
ALLOWED_EXTERNAL_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}
TOKENS = {
    "--bg": "#0a0a0a",
    "--card": "#141414",
    "--border": "#262626",
    "--text": "#f5f5f5",
    "--muted": "#a3a3a3",
    "--accent": "#22c55e",
    "--overdue": "#ef4444",
}


class Page(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self.html = path.read_text(encoding="utf-8")
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.script_srcs: list[str] = []
        self.inline_scripts = 0
        self.lang: str | None = None
        self.title: str | None = None
        self.texts: list[str] = []
        self._in_title = False
        self._in_script = False
        self._in_style = False
        self.feed(self.html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if tag == "img" and "src" in a:
            self.srcs.append(a["src"])
        if tag == "source" and "srcset" in a:
            self.srcs.append(a["srcset"])
        if tag == "link" and a.get("rel") in ("stylesheet", "icon") and "href" in a:
            self.hrefs.append(a["href"])
        if tag == "script":
            self._in_script = True
            if "src" in a:
                self.script_srcs.append(a["src"])
            else:
                self.inline_scripts += 1
        if tag == "style":
            self._in_style = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._in_script = False
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data.strip()
        elif not self._in_script and not self._in_style:
            self.texts.append(data)

    @property
    def text(self) -> str:
        return " ".join(t.strip() for t in self.texts if t.strip())


def load(name: str) -> Page | None:
    p = ROOT / name
    return Page(p) if p.exists() else None


def host_of(url: str) -> str | None:
    m = re.match(r"https?://([^/]+)", url)
    return m.group(1) if m else None


# ---- checks ---------------------------------------------------------------

def check_files_exist(_: str) -> list[str]:
    out = []
    for f in [".nojekyll", "assets/icon.svg", "assets/icon-512.png", *PAGES]:
        if not (ROOT / f).exists():
            out.append(f"missing {f}")
    return out


def check_page_basics(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return [f"{name}: missing"]
    out = []
    if page.lang != "en":
        out.append(f"{name}: <html lang> should be 'en', got {page.lang!r}")
    if not page.title or "Settled" not in page.title:
        out.append(f"{name}: <title> must mention Settled, got {page.title!r}")
    if 'name="viewport"' not in page.html:
        out.append(f"{name}: missing viewport meta")
    if page.inline_scripts or page.script_srcs:
        out.append(f"{name}: pages must not contain <script>")
    return out


def check_tokens(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    for var, value in TOKENS.items():
        if not re.search(rf"{re.escape(var)}\s*:\s*{re.escape(value)}", page.html, re.I):
            out.append(f"{name}: token {var}: {value} not defined on :root")
    if not re.search(r"body\s*\{[^}]*background", page.html, re.S):
        out.append(f"{name}: body has no explicit background")
    return out


def check_links(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    for href in page.hrefs:
        if href.startswith("#"):
            if href != "#" and href[1:] not in page.ids:
                out.append(f"{name}: anchor {href} has no matching id")
        elif href.startswith("mailto:"):
            continue
        elif host := host_of(href):
            if host not in ALLOWED_EXTERNAL_HOSTS and not host.endswith("google.com"):
                out.append(f"{name}: unexpected external host {host}")
        else:
            if href.startswith("/"):
                out.append(f"{name}: root-absolute href {href} breaks on a Pages subpath")
            elif not (ROOT / href.split("#")[0]).exists():
                out.append(f"{name}: href {href} does not resolve")
    for src in page.srcs:
        if src.startswith("/"):
            out.append(f"{name}: root-absolute src {src}")
        elif host_of(src) is None and not (ROOT / src).exists():
            out.append(f"{name}: img src {src} does not resolve")
    return out


CHECKS = [
    ("files", check_files_exist, [None]),
    ("basics", check_page_basics, PAGES),
    ("tokens", check_tokens, PAGES),
    ("links", check_links, PAGES),
]


def main() -> int:
    failures: list[str] = []
    for label, fn, targets in CHECKS:
        for t in targets:
            failures.extend(f"[{label}] {m}" for m in fn(t))
    if failures:
        print("\n".join(failures))
        print(f"\n{len(failures)} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run it and confirm it fails on the missing files**

Run: `python scripts/check_site.py`
Expected: exit 1, lines like `[files] missing .nojekyll`, `[files] missing index.html`, `[files] missing privacy.html`.

- [ ] **Step 3: Scaffold assets and `.nojekyll`**

```bash
mkdir -p assets/screens scripts
: > .nojekyll
cp "C:/Hans/Projects/Android/Budget Checklist/assets/brand/icon.svg" assets/icon.svg
cp "C:/Hans/Projects/Android/Budget Checklist/assets/brand/play-icon-512.png" assets/icon-512.png
```

- [ ] **Step 4: Write the `index.html` skeleton with the full stylesheet**

The stylesheet is complete here on purpose: later tasks only add markup.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Settled — your monthly bills, settled</title>
  <meta name="description" content="Settled is an offline Android checklist for the expenses you pay every month — the spreadsheet you already keep, as an app. Coming soon to Google Play.">
  <meta name="theme-color" content="#0a0a0a">
  <link rel="icon" href="assets/icon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">
  <style>
    :root {
      --bg: #0a0a0a;
      --card: #141414;
      --border: #262626;
      --text: #f5f5f5;
      --muted: #a3a3a3;
      --accent: #22c55e;
      --overdue: #ef4444;
      --font: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
      --mono: "JetBrains Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
      --radius: 16px;
      --gutter: 16px;
      color-scheme: dark;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
    img { max-width: 100%; display: block; }
    a { color: inherit; text-decoration: none; }
    a:hover { color: var(--accent); }
    h1, h2, h3 { margin: 0; line-height: 1.15; letter-spacing: -0.01em; }
    p { margin: 0; }
    code { font-family: var(--mono); font-size: .92em; color: var(--text); }

    .container { max-width: 1080px; margin: 0 auto; padding: 0 var(--gutter); }
    .mono { font-family: var(--mono); }
    .muted { color: var(--muted); }
    .eyebrow {
      font-family: var(--mono);
      font-size: 12px;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--accent);
    }

    /* nav */
    .nav { position: sticky; top: 0; z-index: 10; background: rgba(10,10,10,.85); backdrop-filter: blur(10px); border-bottom: 1px solid var(--border); }
    .nav .container { display: flex; align-items: center; justify-content: space-between; height: 60px; }
    .brand { display: flex; align-items: center; gap: 10px; font-weight: 600; }
    .brand img { width: 28px; height: 28px; border-radius: 7px; }
    .nav-links { display: flex; gap: 22px; font-size: 14px; color: var(--muted); }

    /* sections */
    .section { padding: 88px 0; border-top: 1px solid var(--border); }
    .section-head { max-width: 560px; margin-bottom: 40px; }
    .section-head h2 { font-size: clamp(26px, 3.6vw, 36px); margin-top: 10px; }
    .section-head p { color: var(--muted); margin-top: 12px; font-size: 17px; }

    /* hero */
    .hero { padding: 72px 0 96px; position: relative; overflow: hidden; }
    .hero .container { display: grid; grid-template-columns: 1.15fr .85fr; gap: 48px; align-items: center; }
    .hero h1 { font-size: clamp(38px, 6vw, 64px); font-weight: 700; }
    .hero h1 em { font-style: normal; color: var(--accent); }
    .hero .lead { color: var(--muted); font-size: clamp(17px, 2vw, 20px); margin-top: 20px; max-width: 520px; }
    .hero-cta { margin-top: 32px; display: flex; flex-direction: column; gap: 10px; align-items: flex-start; }
    .hero-cta small { font-family: var(--mono); font-size: 12px; color: var(--muted); letter-spacing: .04em; }
    .hero-visual { position: relative; display: flex; justify-content: center; }
    .glow {
      position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
      width: 420px; height: 420px; border-radius: 50%;
      background: radial-gradient(closest-side, rgba(34,197,94,.28), transparent 70%);
      pointer-events: none;
    }

    /* badge */
    .btn-badge { display: inline-block; opacity: .55; filter: grayscale(1); cursor: not-allowed; }
    .btn-badge img { height: 56px; width: auto; }

    /* phone frame */
    .phone {
      position: relative;
      width: clamp(220px, 28vw, 320px);
      aspect-ratio: 720 / 1180;
      padding: 8px;
      border-radius: 36px;
      background: #1c1c1c;
      box-shadow: 0 0 0 1px #2e2e2e, 0 30px 80px rgba(0,0,0,.6);
      flex-shrink: 0;
    }
    .phone img { width: 100%; height: 100%; object-fit: cover; object-position: top; border-radius: 28px; background: #000; }

    /* grids & cards */
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 26px; }
    .card h3 { font-size: 18px; margin-top: 14px; }
    .card p { color: var(--muted); margin-top: 8px; font-size: 15px; }
    .step-num { font-family: var(--mono); color: var(--accent); font-size: 13px; }
    .icon { width: 36px; height: 36px; border-radius: 10px; background: rgba(34,197,94,.12); display: grid; place-items: center; color: var(--accent); }
    .icon svg { width: 20px; height: 20px; }

    /* screenshot strip */
    .strip { display: flex; gap: 28px; overflow-x: auto; padding: 8px var(--gutter) 24px; margin: 0 calc(-1 * var(--gutter)); scroll-snap-type: x mandatory; scrollbar-width: thin; }
    .strip figure { margin: 0; scroll-snap-align: start; text-align: center; }
    .strip figcaption { margin-top: 14px; font-size: 14px; color: var(--muted); }

    /* pricing */
    .price { display: flex; flex-direction: column; gap: 14px; }
    .price .amount { font-family: var(--mono); font-size: 30px; font-weight: 600; }
    .price .amount small { font-size: 14px; color: var(--muted); font-weight: 400; }
    .price ul { margin: 0; padding: 0; list-style: none; color: var(--muted); font-size: 15px; display: grid; gap: 8px; }
    .price li::before { content: "✓ "; color: var(--accent); font-family: var(--mono); }
    .price--accent { border-color: rgba(34,197,94,.5); box-shadow: 0 0 0 1px rgba(34,197,94,.25) inset; }
    .chip { display: inline-block; align-self: flex-start; font-family: var(--mono); font-size: 11px; letter-spacing: .12em; text-transform: uppercase; padding: 4px 10px; border-radius: 999px; }
    .chip--accent { color: var(--accent); background: rgba(34,197,94,.12); }
    .chip--overdue { color: var(--overdue); background: rgba(239,68,68,.12); }

    /* footer */
    .footer { border-top: 1px solid var(--border); padding: 36px 0; font-size: 14px; color: var(--muted); }
    .footer .container { display: flex; flex-wrap: wrap; gap: 12px 24px; justify-content: space-between; align-items: center; }

    /* prose (privacy page) */
    .prose { max-width: 720px; }
    .prose h1 { font-size: clamp(30px, 4vw, 42px); margin-bottom: 8px; }
    .prose h2 { font-size: 20px; margin-top: 40px; }
    .prose p, .prose li { color: var(--muted); margin-top: 12px; font-size: 16px; }
    .prose a { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; }

    @media (max-width: 720px) {
      .hero { padding: 48px 0 64px; }
      .hero .container { grid-template-columns: 1fr; gap: 40px; }
      .hero-visual { order: -1; }
      .glow { width: 300px; height: 300px; }
      .grid-3, .grid-2 { grid-template-columns: 1fr; }
      .section { padding: 64px 0; }
      .nav-links { gap: 16px; }
    }
    @media (prefers-reduced-motion: no-preference) {
      @supports (animation-timeline: view()) {
        .card, .strip figure { animation: rise .6s ease-out both; animation-timeline: view(); animation-range: entry 0% entry 30%; }
      }
      @keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
    }
  </style>
</head>
<body>
  <header class="nav">
    <div class="container">
      <a class="brand" href="#top"><img src="assets/icon.svg" alt="" width="28" height="28">Settled</a>
      <nav class="nav-links" aria-label="Page">
        <a href="#features">Features</a>
        <a href="#pricing">Pricing</a>
        <a href="privacy.html">Privacy</a>
      </nav>
    </div>
  </header>

  <main id="top">
    <!-- hero: Task 3 -->
    <!-- how it works + features: Task 4 -->
    <!-- screens + pricing: Task 5 -->
  </main>

  <footer class="footer">
    <div class="container">
      <span>© 2026 Settled · Built by Hans</span>
      <span><a href="privacy.html">Privacy policy</a> · <a href="mailto:deguzmanhans05@gmail.com">deguzmanhans05@gmail.com</a></span>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 5: Run the checker; only `privacy.html` and the not-yet-built anchors should fail**

Run: `python scripts/check_site.py`
Expected: exit 1 with `[files] missing privacy.html`, `[basics] privacy.html: missing`, `[links] index.html: anchor #features has no matching id`, `[links] index.html: anchor #pricing has no matching id`, and `[links] index.html: href privacy.html does not resolve`. These are expected until Tasks 4–6; do not remove the links to silence them.

- [ ] **Step 6: Commit**

```bash
git add .nojekyll assets/icon.svg assets/icon-512.png index.html scripts/check_site.py
git commit -m "feat: page skeleton, stylesheet, and site checker

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: Capture and crop device screenshots

**Files:**
- Create: `scripts/crop_screens.py`
- Create: `assets/screens/{month,month-settled,template,history,settings}.webp` and `.png`
- Modify: `scripts/check_site.py` (add `check_screens`)
- Scratch (not committed): `<scratchpad>/raw/*.png`

**Interfaces:**
- Consumes: `adb` at `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`; device `CPH2493` (1240×2772) with `com.hansukun.settled` installed.
- Produces: five 720px-wide screenshots, aspect 720:1180, no status bar, no ad, no tab bar. Task 3 and Task 5 reference them by name.

Important: this is the user's phone with real data. The only state change allowed is ticking **one** checkbox for the "partially paid" hero shot and unticking it afterwards. Do not add, edit, or delete anything.

- [ ] **Step 1: Add the screens check (fails until the files exist)**

Add to `scripts/check_site.py`, above `CHECKS`:

```python
SCREENS = ["month", "month-settled", "template", "history", "settings"]


def check_screens(_: str) -> list[str]:
    out = []
    for s in SCREENS:
        for ext in ("webp", "png"):
            p = ROOT / "assets" / "screens" / f"{s}.{ext}"
            if not p.exists():
                out.append(f"missing assets/screens/{s}.{ext}")
                continue
            if ext == "png":
                head = p.read_bytes()[:24]
                w = int.from_bytes(head[16:20], "big")   # IHDR width
                h = int.from_bytes(head[20:24], "big")   # IHDR height
                if w != 720 or abs(h - 1180) > 4:
                    out.append(f"assets/screens/{s}.png is {w}x{h}, expected 720x1180")
    return out
```

Register it: add `("screens", check_screens, [None]),` to `CHECKS`.

Run: `python scripts/check_site.py`
Expected: ten `[screens] missing ...` lines (plus the pre-existing failures from Task 1 step 5).

- [ ] **Step 2: Install Pillow and write the crop script**

Run: `python -m pip install --user pillow`
Expected: `Successfully installed pillow-...` (or "already satisfied").

```python
# scripts/crop_screens.py
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
```

- [ ] **Step 3: Capture the raw screenshots**

Set up once (Bash tool; `SCRATCHPAD` is this session's scratchpad directory):

```bash
ADB="$LOCALAPPDATA/Android/Sdk/platform-tools/adb.exe"
RAW="$SCRATCHPAD/raw"; mkdir -p "$RAW"
"$ADB" shell am start -n com.hansukun.settled/.MainActivity; sleep 3
```

Tap targets in source pixels (1240×2772): tab bar Month `207 2620`, History `621 2620`, Settings `1037 2620`; previous-month arrow `115 260`; next-month arrow `1125 260`; first item's checkbox `124 759`.

Capture sequence. After **every** capture, `Read` the PNG and confirm no toast, keyboard, or dialog is visible; retake if there is (a React Native warning toast has an × at about `1147 2495`; or wait 5s).

```bash
# 1. month (partially paid). If the current month shows 0 paid, tick the first item.
"$ADB" shell input tap 207 2620; sleep 1
"$ADB" shell input tap 124 759; sleep 1
"$ADB" exec-out screencap -p > "$RAW/month.png"
# expected: header "September 2026", progress bar partly green, one green checkbox,
#           at least one "Overdue · due Nth" line and one "Due Nth" line, no toast.

# 2. month-settled: go back one month; August 2026 was fully paid in earlier captures.
#    If it is not fully paid, keep going back until every pool shows COMPLETED.
"$ADB" shell input tap 115 260; sleep 1
"$ADB" exec-out screencap -p > "$RAW/month-settled.png"
# expected: all checkboxes green, every pool card outlined green with a COMPLETED chip.
"$ADB" shell input tap 1125 260; sleep 1        # back to September (repeat per month stepped)

# 3. history
"$ADB" shell input tap 621 2620; sleep 1
"$ADB" exec-out screencap -p > "$RAW/history.png"

# 4. settings
"$ADB" shell input tap 1037 2620; sleep 1
"$ADB" exec-out screencap -p > "$RAW/settings.png"

# 5. template: Read settings.png, find the row labelled "Template" (or "Monthly
#    template"), convert its displayed y to source pixels (×1.39 if the Read tool
#    displayed the image at 895px wide), tap it, capture.
"$ADB" shell input tap <x> <y>; sleep 1
"$ADB" exec-out screencap -p > "$RAW/template.png"
# expected: the template editor with pool cards and items, no bottom sheet open.
"$ADB" shell input keyevent KEYCODE_BACK; sleep 1

# 6. RESTORE: untick the checkbox ticked in step 1.
"$ADB" shell input tap 207 2620; sleep 1
"$ADB" shell input tap 124 759; sleep 1
"$ADB" exec-out screencap -p > "$RAW/verify-restored.png"
# Read it: the first item must be unticked again and the progress line back to "₱0 of ...".
```

If the month on screen already has a mix of paid and unpaid items when you arrive, skip the tick in step 1 and the untick in step 6.

- [ ] **Step 4: Crop, then eyeball every output**

Run: `python scripts/crop_screens.py "$RAW"`
Expected: five lines like `month: 720x1180`.

`Read` each `assets/screens/*.png`. Requirements: no status-bar icons at the top, no "Test Ad" strip, no tab bar at the bottom. If any is visible, adjust `TOP`/`BOTTOM` in `crop_screens.py` (keeping `BOTTOM - TOP = 2032`) and re-run.

- [ ] **Step 5: Run the checker**

Run: `python scripts/check_site.py`
Expected: no `[screens]` failures remain.

- [ ] **Step 6: Commit**

```bash
git add scripts/crop_screens.py scripts/check_site.py assets/screens
git commit -m "feat: device screenshots for the brochure

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: Hero section and the coming-soon badge

**Files:**
- Create: `assets/google-play-badge.svg`
- Modify: `index.html` — replace `<!-- hero: Task 3 -->`
- Modify: `scripts/check_site.py` — add `check_hero`

**Interfaces:**
- Consumes: `.hero`, `.hero-visual`, `.glow`, `.phone`, `.btn-badge`, `.hero-cta`, `.eyebrow` from Task 1; `assets/screens/month.{webp,png}` from Task 2.

- [ ] **Step 1: Add the hero check**

```python
def check_hero(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    if "Your monthly bills, settled." not in page.text:
        out.append("index.html: hero headline missing")
    if "Coming soon to Google Play" not in page.text:
        out.append("index.html: coming-soon caption missing")
    if "assets/google-play-badge.svg" not in page.srcs:
        out.append("index.html: badge image missing")
    if not any("screens/month.webp" in s for s in page.srcs):
        out.append("index.html: hero phone must show screens/month.webp")
    if re.search(r'href="https?://play\.google\.com', page.html):
        out.append("index.html: badge must not link to Play yet")
    return out
```

Register: `("hero", check_hero, ["index.html"]),`.

Run: `python scripts/check_site.py` — expect four `[hero]` failures.

- [ ] **Step 2: Draw the badge**

Create `assets/google-play-badge.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60" viewBox="0 0 200 60" role="img" aria-label="Coming soon on Google Play">
  <rect x=".5" y=".5" width="199" height="59" rx="8" fill="#141414" stroke="#3a3a3a"/>
  <g transform="translate(14 14)">
    <path d="M2 2 L18 16 L2 30 Z" fill="#8a8a8a"/>
    <path d="M2 2 L26 16 L18 16 Z" fill="#aaaaaa"/>
    <path d="M2 30 L26 16 L18 16 Z" fill="#6f6f6f"/>
  </g>
  <text x="52" y="24" font-family="JetBrains Mono, ui-monospace, monospace" font-size="10" letter-spacing="1.5" fill="#a3a3a3">COMING SOON ON</text>
  <text x="52" y="45" font-family="Inter, system-ui, sans-serif" font-size="19" font-weight="600" fill="#e5e5e5">Google Play</text>
</svg>
```

- [ ] **Step 3: Add the hero markup**

Replace `<!-- hero: Task 3 -->` in `index.html` with:

```html
    <section class="hero">
      <div class="container">
        <div>
          <span class="eyebrow">Android · offline · no account</span>
          <h1 style="margin-top:14px">Your monthly bills, <em>settled.</em></h1>
          <p class="lead">An offline checklist for the expenses you pay every month — the spreadsheet you already keep, as an app.</p>
          <div class="hero-cta">
            <span class="btn-badge" aria-disabled="true" title="Not on Google Play yet">
              <img src="assets/google-play-badge.svg" alt="Coming soon on Google Play" width="200" height="60">
            </span>
            <small>Coming soon to Google Play · listing in review</small>
          </div>
        </div>
        <div class="hero-visual">
          <div class="glow" aria-hidden="true"></div>
          <div class="phone">
            <picture>
              <source srcset="assets/screens/month.webp" type="image/webp">
              <img src="assets/screens/month.png" alt="Settled's month screen: pools of expenses with a checkbox per item, due dates, and a progress bar of what's been paid" width="720" height="1180" fetchpriority="high">
            </picture>
          </div>
        </div>
      </div>
    </section>
```

- [ ] **Step 4: Run the checker and look at the page**

Run: `python scripts/check_site.py` — expect no `[hero]` failures.

Open the page in the built-in browser: `navigate` to `file:///E:/Hans/Projects/Web%20App%20Dev%20Page/index.html` and take a screenshot. Confirm: headline with green "settled.", greyed badge, phone frame with the Month screenshot and a soft green glow behind it.

- [ ] **Step 5: Commit**

```bash
git add assets/google-play-badge.svg index.html scripts/check_site.py
git commit -m "feat: hero with coming-soon badge and month screenshot

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: "How it works" and "Features" sections

**Files:**
- Modify: `index.html` — replace `<!-- how it works + features: Task 4 -->`
- Modify: `scripts/check_site.py` — add `check_features`

**Interfaces:**
- Consumes: `.section`, `.section-head`, `.grid-3`, `.card`, `.step-num`, `.icon`, `.eyebrow`.
- Produces: `id="features"` (nav anchor target) and `id="how"`.

- [ ] **Step 1: Add the check**

```python
FEATURE_TITLES = [
    "Pools and totals",
    "Due-date reminders",
    "Month history and trend",
    "A template that never rewrites history",
    "No account, no sync, no cloud",
    "Backups you control",
]
STEP_TITLES = [
    "Set up your template once",
    "Tick things off as you pay",
    "It rolls into next month",
]


def check_features(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    for i in ("features", "how"):
        if i not in page.ids:
            out.append(f"index.html: missing id={i}")
    for t in FEATURE_TITLES:
        if t not in page.text:
            out.append(f"index.html: feature card '{t}' missing")
    for s in STEP_TITLES:
        if s not in page.text:
            out.append(f"index.html: step '{s}' missing")
    return out
```

Register: `("features", check_features, ["index.html"]),`. Run the checker — expect the new failures.

- [ ] **Step 2: Add the markup**

Replace `<!-- how it works + features: Task 4 -->` with:

```html
    <section class="section" id="how">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">How it works</span>
          <h2>Three steps, once a month.</h2>
          <p>The same routine as the sheet — without the sheet.</p>
        </div>
        <div class="grid-3">
          <div class="card">
            <span class="step-num">01</span>
            <h3>Set up your template once</h3>
            <p>Group your recurring expenses into pools — WALLET, UTILITIES, whatever your sheet calls them — with an amount and an optional due day for each.</p>
          </div>
          <div class="card">
            <span class="step-num">02</span>
            <h3>Tick things off as you pay</h3>
            <p>Each item is a checkbox. Pools total themselves and light up when everything in them is paid. The header keeps score.</p>
          </div>
          <div class="card">
            <span class="step-num">03</span>
            <h3>It rolls into next month</h3>
            <p>A fresh month is generated from your template. Last month stays exactly as you left it.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="features">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Features</span>
          <h2>Everything the spreadsheet did. A few things it couldn't.</h2>
        </div>
        <div class="grid-3">
          <div class="card">
            <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 10h18M9 10v10"/></svg></div>
            <h3>Pools and totals</h3>
            <p>Group items the way your sheet does. Each pool has its own total and turns green when everything in it is paid.</p>
          </div>
          <div class="card">
            <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 8a6 6 0 0 1 12 0v5l2 3H4l2-3zM10 20a2 2 0 0 0 4 0"/></svg></div>
            <h3>Due-date reminders</h3>
            <p>Give an item a due day and get a nudge. Overdue items say so in red. Paying one cancels its reminder.</p>
          </div>
          <div class="card">
            <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg></div>
            <h3>Month history and trend</h3>
            <p>Every month is kept. Flip back to see what you paid, and a chart shows how it's moving.</p>
          </div>
          <div class="card">
            <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h5"/></svg></div>
            <h3>A template that never rewrites history</h3>
            <p>Edit the template and this month and later ones follow. Earlier months read exactly as they did.</p>
          </div>
          <div class="card">
            <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="3"/><path d="M11 18h2"/></svg></div>
            <h3>No account, no sync, no cloud</h3>
            <p>Everything lives in a database on your phone. Works on a plane, in a basement, or with data off.</p>
          </div>
          <div class="card">
            <div class="icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"/></svg></div>
            <h3>Backups you control</h3>
            <p>Back up to Google Drive or a file when you want to, restore when you need to, and export any month as CSV.</p>
          </div>
        </div>
      </div>
    </section>
```

- [ ] **Step 3: Check and view**

Run: `python scripts/check_site.py` — expect no `[features]` failures and the `#features` anchor failure gone.
Screenshot the page in the browser; confirm two rows of three cards on desktop.

- [ ] **Step 4: Commit**

```bash
git add index.html scripts/check_site.py
git commit -m "feat: how-it-works and feature sections

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: Screens strip and pricing

**Files:**
- Modify: `index.html` — replace `<!-- screens + pricing: Task 5 -->`
- Modify: `scripts/check_site.py` — add `check_pricing`

**Interfaces:**
- Consumes: `.strip`, `.phone`, `.grid-2`, `.price`, `.price--accent`, `.chip`, `.chip--accent`; screenshots `month-settled`, `template`, `history`, `settings` from Task 2.
- Produces: `id="pricing"`, `id="screens"`.

- [ ] **Step 1: Add the check**

```python
def check_pricing(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    for i in ("pricing", "screens"):
        if i not in page.ids:
            out.append(f"index.html: missing id={i}")
    for s in ("month-settled", "template", "history", "settings"):
        if not any(f"screens/{s}.webp" in x for x in page.srcs):
            out.append(f"index.html: screens strip missing {s}")
    for t in ("7-day free trial", "Set on Google Play"):
        if t not in page.text:
            out.append(f"index.html: pricing copy '{t}' missing")
    pricing_text = page.text.split("Free to use.", 1)[-1]
    if re.search(r"[₱$€]\s?\d", pricing_text):
        out.append("index.html: pricing must not state a currency amount")
    return out
```

Register: `("pricing", check_pricing, ["index.html"]),`. Run the checker — expect the new failures.

- [ ] **Step 2: Add the markup**

Replace `<!-- screens + pricing: Task 5 -->` with:

```html
    <section class="section" id="screens">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Screens</span>
          <h2>Dark, quiet, and quick to read.</h2>
        </div>
        <div class="strip">
          <figure>
            <div class="phone"><picture><source srcset="assets/screens/month-settled.webp" type="image/webp"><img src="assets/screens/month-settled.png" alt="A fully paid month: every pool outlined green and marked completed" width="720" height="1180" loading="lazy"></picture></div>
            <figcaption>A settled month</figcaption>
          </figure>
          <figure>
            <div class="phone"><picture><source srcset="assets/screens/template.webp" type="image/webp"><img src="assets/screens/template.png" alt="The template editor with pools, items, amounts and reminder settings" width="720" height="1180" loading="lazy"></picture></div>
            <figcaption>The template</figcaption>
          </figure>
          <figure>
            <div class="phone"><picture><source srcset="assets/screens/history.webp" type="image/webp"><img src="assets/screens/history.png" alt="History: past months with totals and a trend chart" width="720" height="1180" loading="lazy"></picture></div>
            <figcaption>History and trend</figcaption>
          </figure>
          <figure>
            <div class="phone"><picture><source srcset="assets/screens/settings.webp" type="image/webp"><img src="assets/screens/settings.png" alt="Settings: template, reminders, backup and restore, export, and the ad-free plan" width="720" height="1180" loading="lazy"></picture></div>
            <figcaption>Settings and backups</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section" id="pricing">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow">Pricing</span>
          <h2>Free to use. Pay only to lose the ads.</h2>
        </div>
        <div class="grid-2">
          <div class="card price">
            <span class="chip chip--accent">Free</span>
            <span class="amount">Free <small>forever</small></span>
            <ul>
              <li>The whole app — pools, reminders, history, backups</li>
              <li>One small banner and an occasional native ad row</li>
              <li>Never an ad in Settings, the template, or a form</li>
            </ul>
          </div>
          <div class="card price price--accent">
            <span class="chip chip--accent">Ad-free</span>
            <span class="amount">Set on Google Play <small>/ month</small></span>
            <ul>
              <li>Everything in Free, with no ads at all</li>
              <li>7-day free trial</li>
              <li>Cancel any time from Google Play</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
```

- [ ] **Step 3: Check and view**

Run: `python scripts/check_site.py` — expect only `privacy.html` failures left.
Screenshot the page; confirm four phones in a scrollable strip and two pricing cards, the right one with a green border.

- [ ] **Step 4: Commit**

```bash
git add index.html scripts/check_site.py
git commit -m "feat: screens strip and pricing

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: Privacy policy page

**Files:**
- Create: `privacy.html`
- Modify: `scripts/check_site.py` — add `check_privacy`

**Interfaces:**
- Consumes: the `<style>` block from `index.html` (copy it verbatim; the unused component rules cost nothing and keep the two files trivially in sync), `.prose`, `.nav`, `.footer`, `.eyebrow`, `.mono`.

- [ ] **Step 1: Add the check**

```python
PRIVACY_HEADINGS = [
    "Summary",
    "What the app stores",
    "Advertising",
    "Google account and Drive",
    "Purchases",
    "Notifications",
    "Children",
    "Changes and contact",
]


def check_privacy(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    for h in PRIVACY_HEADINGS:
        if h not in page.text:
            out.append(f"privacy.html: section '{h}' missing")
    if "drive.appdata" not in page.text:
        out.append("privacy.html: must name the drive.appdata scope")
    if "deguzmanhans05@gmail.com" not in page.text:
        out.append("privacy.html: contact address missing")
    if not re.search(r"Effective \d{1,2} \w+ 20\d\d", page.text):
        out.append("privacy.html: effective date missing")
    if not any(h.startswith("index.html") for h in page.hrefs):
        out.append("privacy.html: no link back to the brochure")
    return out
```

Register: `("privacy", check_privacy, ["privacy.html"]),`. Run the checker — expect `[privacy]` failures (the page is missing, so `load` returns None and the check is skipped; the `[files]`/`[basics]` failures still show — that is the failing state).

- [ ] **Step 2: Write the page**

Create `privacy.html` with the Write tool. Copy the entire `<head>` from `index.html`, changing only the `<title>` to `Privacy policy — Settled` and the description to `How Settled handles your data: everything stays on your phone; ads via Google AdMob; optional Google Drive backups.` Then the body:

```html
<body>
  <header class="nav">
    <div class="container">
      <a class="brand" href="index.html"><img src="assets/icon.svg" alt="" width="28" height="28">Settled</a>
      <nav class="nav-links" aria-label="Page">
        <a href="index.html#features">Features</a>
        <a href="index.html#pricing">Pricing</a>
        <a href="privacy.html">Privacy</a>
      </nav>
    </div>
  </header>

  <main class="container prose" style="padding-top:64px;padding-bottom:96px">
    <span class="eyebrow">Privacy policy</span>
    <h1 style="margin-top:12px">Your data stays on your phone.</h1>
    <p class="mono" style="font-size:13px">Effective 17 September 2026 · applies to the Settled Android app (<code>com.hansukun.settled</code>)</p>

    <h2>Summary</h2>
    <p>Settled is an offline expense checklist. There is no account, no server, and no analytics. Everything you enter is stored in a database on your device and never leaves it unless you back it up yourself. The free version shows ads served by Google AdMob; the ad-free subscription removes them.</p>

    <h2>What the app stores</h2>
    <p>On your device only: your template of recurring expenses, each month generated from it, item names and amounts, which items you have marked paid, due days, and reminder settings. This data is kept in a local SQLite database and is deleted when you uninstall the app. We cannot see it and do not collect it.</p>

    <h2>Advertising</h2>
    <p>The free version shows a small banner and occasional native ad rows served by <strong>Google AdMob</strong>. AdMob may use your device's advertising ID and general device information to show and measure ads, under <a href="https://policies.google.com/technologies/ads">Google's advertising policy</a>. You can reset or limit the advertising ID in your Android settings under <em>Privacy › Ads</em>. Settled does not pass any of your expense data to the ad network. Subscribing to the ad-free plan turns ads off entirely.</p>

    <h2>Google account and Drive</h2>
    <p>Backing up to Google Drive is optional. If you choose it, the app asks you to sign in with Google and requests only the <code>https://www.googleapis.com/auth/drive.appdata</code> scope. That scope gives Settled access to a hidden application folder in your Drive that only this app can read or write; it cannot see any of your other Drive files. Backups are copies of the local database, kept in that folder until you delete them from within the app. You can revoke Settled's access at any time from your <a href="https://myaccount.google.com/permissions">Google account permissions</a>. Signing in shares your Google account name and email with the app so it can show which account is connected; this is not stored anywhere else.</p>

    <h2>Purchases</h2>
    <p>The ad-free subscription is sold through Google Play Billing. Google handles payment; the app only receives confirmation that the subscription is active. Settled never sees your payment details.</p>

    <h2>Notifications</h2>
    <p>Due-date reminders are scheduled locally on your device. Nothing is sent to a server to deliver them. You can turn reminders off per item or deny the notification permission entirely.</p>

    <h2>Children</h2>
    <p>Settled is not directed at children under 13 and does not knowingly collect information from them.</p>

    <h2>Changes and contact</h2>
    <p>If this policy changes, the new version will be published at this address with a new effective date. Questions: <a href="mailto:deguzmanhans05@gmail.com">deguzmanhans05@gmail.com</a>.</p>

    <p style="margin-top:40px"><a href="index.html">← Back to Settled</a></p>
  </main>

  <footer class="footer">
    <div class="container">
      <span>© 2026 Settled · Built by Hans</span>
      <span><a href="privacy.html">Privacy policy</a> · <a href="mailto:deguzmanhans05@gmail.com">deguzmanhans05@gmail.com</a></span>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 3: Run the full checker**

Run: `python scripts/check_site.py`
Expected: `all checks passed`, exit 0. (`check_links` accepts `policies.google.com` and `myaccount.google.com` via `host.endswith("google.com")`.)

- [ ] **Step 4: View it**

Open `file:///E:/Hans/Projects/Web%20App%20Dev%20Page/privacy.html` in the browser; confirm the nav, prose column, and footer render in the dark theme, and the "Back to Settled" link returns to the brochure.

- [ ] **Step 5: Commit**

```bash
git add privacy.html scripts/check_site.py
git commit -m "feat: privacy policy page

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 7: Responsive and accessibility verification

**Files:**
- Modify (only if a check reveals a problem): `index.html`, `privacy.html`

- [ ] **Step 1: Contrast check for muted text**

Run in the browser's JavaScript tool on `index.html`:

```js
const lum = h => { const [r,g,b] = h.match(/\w\w/g).map(x => parseInt(x,16)/255).map(c => c <= .03928 ? c/12.92 : ((c+.055)/1.055)**2.4); return .2126*r+.7152*g+.0722*b; };
const ratio = (a,b) => { const [l1,l2] = [lum(a),lum(b)].sort((x,y)=>y-x); return ((l1+.05)/(l2+.05)).toFixed(2); };
({ mutedOnCard: ratio("#a3a3a3","#141414"), mutedOnBg: ratio("#a3a3a3","#0a0a0a"), accentOnBg: ratio("#22c55e","#0a0a0a") })
```

Expected: every ratio ≥ 4.5 (muted on card ≈ 7.3, accent on bg ≈ 8.3). Record the numbers for the commit message.

- [ ] **Step 2: Mobile layout**

In the built-in browser, `resize_window` to preset `mobile` (375×812), reload `index.html`, and run:

```js
({ scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth })
```

Expected: `scrollW === innerW` (no horizontal scroll). Screenshot the hero and the strip. Confirm the phone appears above the headline (`.hero-visual { order: -1 }`), cards stack in one column, and the strip scrolls horizontally without pushing the page wider.

Repeat the `scrollW` check for `privacy.html`. Then `resize_window` back to preset `desktop`.

- [ ] **Step 3: Desktop layout**

At the pane's desktop width, screenshot the whole page section by section (hero, how, features, screens, pricing, footer). Confirm the sticky nav stays visible while scrolling and every nav link lands on its section.

- [ ] **Step 4: Fix anything found, re-run the checker, commit**

Run: `python scripts/check_site.py` → `all checks passed`.

```bash
git add -A
git commit -m "chore: responsive and contrast verification

Muted on card 7.3:1, accent on bg 8.3:1; no horizontal scroll at 375px.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

If nothing needed fixing, skip the commit — there is nothing to commit.

---

## Deploying (user's step, not part of the plan)

Create an empty GitHub repo, then:

```bash
git remote add origin https://github.com/hansukun/settled-site.git
git push -u origin main
```

In the repo's Settings › Pages, set Source to "Deploy from a branch", branch `main`, folder `/ (root)`. The privacy policy will be at `https://hansukun.github.io/settled-site/privacy.html` — that URL goes into the Play Console.
