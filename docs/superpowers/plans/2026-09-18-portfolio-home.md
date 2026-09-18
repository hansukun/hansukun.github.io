# Portfolio Home Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the root of `hansukun.github.io` a lean portfolio for Hans De Guzman (Web Developer — WordPress, React, Vue, Android/React Native on the side) and move the existing Settled brochure to `/settled/`, linked from the portfolio's Apps section.

**Architecture:** One new hand-written `index.html` with inline CSS and no JavaScript, in a bold-grid dark style deliberately unlike the Settled page. The Settled pages and assets move as a unit into `settled/` with `git mv` (their links are relative, so nothing inside them changes except two back-links). The existing Python checker `scripts/check_site.py` is the test suite: it is extended to check all three pages, resolving links per page, with a per-page colour-token set and portfolio-specific content checks.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, `clamp()`), Google Fonts (Space Grotesk, JetBrains Mono), Python 3.14 (checker), `python -m http.server` + the built-in browser for verification.

**Spec:** `docs/superpowers/specs/2026-09-18-portfolio-home-design.md`

## Global Constraints

- Static files only: no build step, no framework, **no `<script>` on any page** (the checker fails on one).
- Only external hosts: `fonts.googleapis.com`, `fonts.gstatic.com`, `www.linkedin.com`.
- All asset and page paths are **relative**, never root-absolute (GitHub Pages may serve from a subpath).
- Portfolio tokens on `:root`, exact values: `--bg: #0b0b0d`, `--grid: #1c1c22`, `--surface: #121216`, `--text: #f4f4f5`, `--muted: #a1a1aa`, `--dim: #3f3f46`, `--accent: #3b6cff`. `body` has an explicit background. Dark-only.
- Settled tokens stay exactly as they are: `--bg: #0a0a0a`, `--card: #141414`, `--border: #262626`, `--text: #f5f5f5`, `--muted: #a3a3a3`, `--accent: #22c55e`, `--overdue: #ef4444`.
- Portfolio type: Space Grotesk (400 body, **700** headings — its heaviest weight) and JetBrains Mono for eyebrows, labels, buttons, tags, meta lines. One Google Fonts `<link>` with `display=swap`.
- Portfolio layout: max content width 960px; 16px gutters (24px from 720px up); skills 3→1 and apps 2→1 columns below 720px; H1 `clamp(44px, 10vw, 88px)`; no horizontal scroll at 375px.
- Copy rules: name **Hans De Guzman**; title **Web Developer**; email `devhansukun@gmail.com`; LinkedIn `https://www.linkedin.com/in/hansdg/`; Android work is **React Native**. **No mention of an employer or "US company" anywhere.** No GitHub link.
- Settled pages are moved, not rewritten. The only edits: a `← Hans De Guzman` nav link to `../` and the footer credit `Built by <a href="../">Hans De Guzman</a>`.
- Commit after every task with a `feat:`/`chore:`/`docs:` message ending in `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
- Working directory for every command: `E:\Hans\Projects\Web App Dev Page` (git repo, branch `main`, currently clean).
- Windows: long heredocs fail with `ENAMETOOLONG` in the Bash tool. Use the Write/Edit tools for files longer than ~40 lines. Git warns about LF→CRLF; that is fine.

---

## File map

| Path | Responsibility |
|---|---|
| `index.html` | **New.** The portfolio. Inline `<style>` holds the whole stylesheet. |
| `assets/settled-icon.svg` | **New.** Copy of `settled/assets/icon.svg`, used by the Settled app card. |
| `settled/index.html` | Moved from `/index.html`. Settled brochure. Gains nav back-link and footer credit link. |
| `settled/privacy.html` | Moved from `/privacy.html`. Same two edits. |
| `settled/assets/**` | Moved from `/assets`. Icon, badge, screenshots. Unchanged. |
| `scripts/check_site.py` | The test suite. Repointed at the new paths; per-page tokens; new `check_backlinks` and `check_portfolio`. |
| `.gitignore` | Already has `.superpowers/`. Task 4 adds `.claude/`. |
| `.nojekyll` | Unchanged. |

---

### Task 1: Move Settled into `settled/` and repoint the checker

**Files:**
- Modify: `scripts/check_site.py` (constants at top, `check_files_exist`, `check_screens`, `CHECKS`, `check_links`, `Page`, and the hard-coded `index.html:`/`privacy.html:` message prefixes)
- Move: `index.html` → `settled/index.html`, `privacy.html` → `settled/privacy.html`, `assets/` → `settled/assets/`

**Interfaces:**
- Produces: module constants `PORTFOLIO = "index.html"`, `SETTLED_PAGES`, `PAGES`, `SETTLED_TOKENS`, `TOKENS: dict[str, dict[str, str]]` (page → token set) and `Page.dir` (the page's directory) that Tasks 2 and 3 extend.

- [ ] **Step 1: Repoint the checker's constants (the failing test)**

In `scripts/check_site.py`, replace the block from `PAGES = [...]` through the end of the `TOKENS = {...}` dict with:

```python
PORTFOLIO = "index.html"
SETTLED_PAGES = ["settled/index.html", "settled/privacy.html"]
PAGES = [PORTFOLIO, *SETTLED_PAGES]
ALLOWED_EXTERNAL_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com", "www.linkedin.com"}
SETTLED_TOKENS = {
    "--bg": "#0a0a0a",
    "--card": "#141414",
    "--border": "#262626",
    "--text": "#f5f5f5",
    "--muted": "#a3a3a3",
    "--accent": "#22c55e",
    "--overdue": "#ef4444",
}
TOKENS: dict[str, dict[str, str]] = {p: SETTLED_TOKENS for p in SETTLED_PAGES}
```

- [ ] **Step 2: Give `Page` its directory and resolve links per page**

In the `Page.__init__`, right after `self.path = path`, add:

```python
        self.dir = path.parent
```

In `check_files_exist`, change the list to:

```python
    for f in [".nojekyll", ".gitignore", "settled/assets/icon.svg", "settled/assets/icon-512.png", *PAGES]:
```

In `check_tokens`, change `for var, value in TOKENS.items():` to:

```python
    for var, value in TOKENS.get(name, {}).items():
```

In `check_links`, replace the `else:` branch for relative hrefs and the `for src` loop with:

```python
        else:
            if href.startswith("/"):
                out.append(f"{name}: root-absolute href {href} breaks on a Pages subpath")
            else:
                target = page.dir / href.split("#")[0]
                if not target.exists() or (target.is_dir() and not (target / "index.html").exists()):
                    out.append(f"{name}: href {href} does not resolve")
    for src in page.srcs:
        if src.startswith("/"):
            out.append(f"{name}: root-absolute src {src}")
        elif host_of(src) is None and not (page.dir / src).exists():
            out.append(f"{name}: img src {src} does not resolve")
```

Also in `check_links`, before the `elif href.startswith("mailto:")` line, add a branch that skips data URIs (the portfolio's favicon in Task 3 is an inline SVG):

```python
        elif href.startswith("data:"):
            continue
```

In `check_screens`, change `p = ROOT / "assets" / "screens" / f"{s}.{ext}"` to:

```python
            p = ROOT / "settled" / "assets" / "screens" / f"{s}.{ext}"
```

and the two message strings from `assets/screens/` to `settled/assets/screens/`.

- [ ] **Step 3: Make the Settled-specific messages use the page name and retarget `CHECKS`**

Run from the repo root (Git Bash `sed`): this rewrites every `"index.html: …"` / `"privacy.html: …"` message prefix, f-string or not, to `f"{name}: …"`.

```bash
sed -i -E 's/f?"(index|privacy)\.html: /f"{name}: /g' scripts/check_site.py
```

Then replace the `CHECKS` list with:

```python
CHECKS = [
    ("files", check_files_exist, [None]),
    ("basics", check_page_basics, PAGES),
    ("tokens", check_tokens, PAGES),
    ("links", check_links, PAGES),
    ("screens", check_screens, [None]),
    ("hero", check_hero, ["settled/index.html"]),
    ("features", check_features, ["settled/index.html"]),
    ("pricing", check_pricing, ["settled/index.html"]),
    ("privacy", check_privacy, ["settled/privacy.html"]),
]
```

- [ ] **Step 4: Run the checker to verify it fails for the right reason**

Run: `python scripts/check_site.py`
Expected: exit 1 with lines including `[files] missing settled/assets/icon.svg`, `[files] missing settled/index.html`, `[basics] settled/index.html: missing`, and `[screens] missing settled/assets/screens/month.webp`. Nothing else should be surprising.

- [ ] **Step 5: Move the Settled files**

```bash
mkdir -p settled && git mv index.html settled/index.html && git mv privacy.html settled/privacy.html && git mv assets settled/assets && git status --short
```

Expected: `R` (rename) rows for `index.html`, `privacy.html` and every file under `assets/`; `M scripts/check_site.py`.

- [ ] **Step 6: Run the checker again**

Run: `python scripts/check_site.py`
Expected: only `[files] missing index.html` and `[basics] index.html: missing` (the portfolio doesn't exist yet — Task 3 creates it). No `settled/…` failures.

- [ ] **Step 7: Commit**

```bash
git add -A && git commit -m "chore: move the Settled site to /settled/

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: Back-links from the Settled pages to the portfolio

**Files:**
- Modify: `scripts/check_site.py` (new `check_backlinks`, one `CHECKS` row)
- Modify: `settled/index.html` (nav ≈ line 155, media query line 147, footer ≈ line 320)
- Modify: `settled/privacy.html` (nav line 161, media query line 147, footer line 203)

**Interfaces:**
- Consumes: `SETTLED_PAGES`, `load()`, `Page.hrefs`, `Page.text` from Task 1.
- Produces: `check_backlinks(name) -> list[str]`.

- [ ] **Step 1: Write the failing check**

Add to `scripts/check_site.py` directly after `check_privacy`:

```python
def check_backlinks(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    if "../" not in page.hrefs:
        out.append(f"{name}: no link back to the portfolio (href=\"../\")")
    if "Built by Hans De Guzman" not in page.text:
        out.append(f"{name}: footer credit should read 'Built by Hans De Guzman'")
    return out
```

Add to `CHECKS`, after the `"privacy"` row:

```python
    ("backlinks", check_backlinks, SETTLED_PAGES),
```

- [ ] **Step 2: Run the checker to verify it fails**

Run: `python scripts/check_site.py`
Expected: four `[backlinks]` lines (two per Settled page) in addition to the two `index.html` lines from Task 1.

- [ ] **Step 3: Add the nav back-link to both Settled pages**

In `settled/index.html`, the nav is:

```html
      <nav class="nav-links" aria-label="Page">
        <a href="#features">Features</a>
```

Change to:

```html
      <nav class="nav-links" aria-label="Page">
        <a href="../" aria-label="Back to Hans De Guzman's portfolio"><span aria-hidden="true">←</span><span class="back-text"> Hans De Guzman</span></a>
        <a href="#features">Features</a>
```

In `settled/privacy.html`, the nav is:

```html
      <nav class="nav-links" aria-label="Page">
        <a href="index.html#features">Features</a>
```

Change to:

```html
      <nav class="nav-links" aria-label="Page">
        <a href="../" aria-label="Back to Hans De Guzman's portfolio"><span aria-hidden="true">←</span><span class="back-text"> Hans De Guzman</span></a>
        <a href="index.html#features">Features</a>
```

In **both** files, inside the `@media (max-width: 720px)` block, change the line

```css
      .nav-links { gap: 16px; }
```

to

```css
      .nav-links { gap: 16px; }
      .back-text { display: none; }
```

so on phones only the arrow shows and four links still fit beside the brand at 375px.

- [ ] **Step 4: Link the footer credit in both Settled pages**

In both `settled/index.html` and `settled/privacy.html`, change

```html
      <span>© 2026 Settled · Built by Hans</span>
```

to

```html
      <span>© 2026 Settled · Built by <a href="../">Hans De Guzman</a></span>
```

- [ ] **Step 5: Run the checker**

Run: `python scripts/check_site.py`
Expected: no `[backlinks]` failures. What remains: the two `index.html` lines (`[files] missing index.html`, `[basics] index.html: missing`) and four `[links] settled/…: href ../ does not resolve` lines (nav + footer on each Settled page). Those `[links]` lines are expected here — `../` points at the root `index.html`, which Task 3 creates — and they clear then. Anything else is a real failure.

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "feat: link the Settled pages back to the portfolio

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: The portfolio page

**Files:**
- Create: `assets/settled-icon.svg` (copy)
- Create: `index.html`
- Modify: `scripts/check_site.py` (`PORTFOLIO_TOKENS`, `TOKENS`, `check_page_basics` title rule, new `check_portfolio`, `check_files_exist`, `CHECKS`)

**Interfaces:**
- Consumes: `PORTFOLIO`, `SETTLED_PAGES`, `TOKENS`, `load()`, `Page` from Task 1.
- Produces: `check_portfolio(name) -> list[str]`; `TITLE_MUST_MENTION: dict[str, str]`.

- [ ] **Step 1: Copy the Settled icon for the app card**

```bash
mkdir -p assets && cp settled/assets/icon.svg assets/settled-icon.svg && ls assets
```

Expected: `settled-icon.svg`.

- [ ] **Step 2: Write the failing portfolio checks**

In `scripts/check_site.py`, directly after the `TOKENS: dict[...] = {...}` line from Task 1, add:

```python
PORTFOLIO_TOKENS = {
    "--bg": "#0b0b0d",
    "--grid": "#1c1c22",
    "--surface": "#121216",
    "--text": "#f4f4f5",
    "--muted": "#a1a1aa",
    "--dim": "#3f3f46",
    "--accent": "#3b6cff",
}
TOKENS[PORTFOLIO] = PORTFOLIO_TOKENS
TITLE_MUST_MENTION = {PORTFOLIO: "Hans De Guzman", **{p: "Settled" for p in SETTLED_PAGES}}
```

In `check_page_basics`, replace

```python
    if not page.title or "Settled" not in page.title:
        out.append(f"{name}: <title> must mention Settled, got {page.title!r}")
```

with

```python
    want = TITLE_MUST_MENTION[name]
    if not page.title or want not in page.title:
        out.append(f"{name}: <title> must mention {want}, got {page.title!r}")
```

In `check_files_exist`, add `"assets/settled-icon.svg"` to the list, after `".gitignore"`.

Add after `check_backlinks`:

```python
PORTFOLIO_COPY = [
    "Hans De Guzman",
    "Remote · Web Developer",
    "What I work with",
    "WordPress",
    "React",
    "Vue",
    "React Native",
    "Things I've shipped",
    "Coming soon to Google Play",
    "More coming soon",
    "Let's build something.",
    "devhansukun@gmail.com",
]
LINKEDIN = "https://www.linkedin.com/in/hansdg/"


def check_portfolio(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    for i in ("skills", "apps", "contact"):
        if i not in page.ids:
            out.append(f"{name}: missing id={i}")
    for t in PORTFOLIO_COPY:
        if t not in page.text:
            out.append(f"{name}: copy '{t}' missing")
    if re.search(r"US company|employer", page.text, re.I):
        out.append(f"{name}: must not mention an employer")
    if "settled/" not in page.hrefs:
        out.append(f"{name}: Settled card must link to settled/")
    if "mailto:devhansukun@gmail.com" not in page.hrefs:
        out.append(f"{name}: no mailto link")
    if not re.search(rf'href="{re.escape(LINKEDIN)}"[^>]*target="_blank"[^>]*rel="noopener"', page.html):
        out.append(f"{name}: LinkedIn link must open in a new tab with rel=noopener")
    if "assets/settled-icon.svg" not in page.srcs:
        out.append(f"{name}: Settled card icon missing")
    if "Space+Grotesk" not in page.html or "JetBrains+Mono" not in page.html:
        out.append(f"{name}: must load Space Grotesk and JetBrains Mono")
    if not re.search(r"body\s*\{[^}]*background-image:\s*linear-gradient", page.html, re.S):
        out.append(f"{name}: body should carry the grid background")
    return out
```

Add to `CHECKS`, after the `"backlinks"` row:

```python
    ("portfolio", check_portfolio, [PORTFOLIO]),
```

- [ ] **Step 3: Run the checker to verify it fails**

Run: `python scripts/check_site.py`
Expected: `[files] missing index.html`, `[basics] index.html: missing`; nothing from `[portfolio]` yet (it returns `[]` for a missing page — that's fine, the `[files]`/`[basics]` lines cover it).

- [ ] **Step 4: Write `index.html`**

Create `index.html` with exactly this content (use the Write tool):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hans De Guzman — Web Developer</title>
  <meta name="description" content="Hans De Guzman is a remote web developer working with WordPress, React and Vue, and shipping Android apps built with React Native on the side.">
  <meta name="theme-color" content="#0b0b0d">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%233b6cff'/%3E%3Ctext x='16' y='23' text-anchor='middle' font-family='monospace' font-weight='700' font-size='20' fill='%230b0b0d'%3EH%3C/text%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;700&display=swap">
  <style>
    :root {
      --bg: #0b0b0d;
      --grid: #1c1c22;
      --surface: #121216;
      --text: #f4f4f5;
      --muted: #a1a1aa;
      --dim: #3f3f46;
      --accent: #3b6cff;
      --font: "Space Grotesk", system-ui, -apple-system, "Segoe UI", sans-serif;
      --mono: "JetBrains Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
      --gutter: 16px;
      color-scheme: dark;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background-color: var(--bg);
      background-image:
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
      background-size: 28px 28px;
      color: var(--text);
      font-family: var(--font);
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
    img { max-width: 100%; display: block; }
    a { color: inherit; text-decoration: none; }
    h1, h2, h3, p { margin: 0; }
    b { font-weight: 700; }

    .container { max-width: 960px; margin: 0 auto; padding: 0 var(--gutter); }
    .eyebrow {
      display: block;
      font-family: var(--mono);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .16em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 12px;
    }

    /* nav */
    .nav { position: sticky; top: 0; z-index: 10; background: var(--bg); border-bottom: 2px solid var(--text); }
    .nav .container {
      display: flex; align-items: center; justify-content: space-between; height: 52px;
      font-family: var(--mono); font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
    }
    .nav-links { display: flex; gap: 20px; }
    .nav a:hover, .nav a:focus-visible { color: var(--accent); }

    /* hero */
    .hero { padding: 80px 0 72px; }
    h1 {
      font-size: clamp(44px, 10vw, 88px);
      font-weight: 700;
      line-height: .92;
      letter-spacing: -.04em;
      text-transform: uppercase;
    }
    h1 .block { display: inline-block; background: var(--accent); color: var(--bg); padding: 0 .12em; }
    .lead { font-family: var(--mono); color: var(--muted); font-size: 15px; max-width: 480px; margin-top: 24px; }
    .lead b { color: var(--text); }
    .btn-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
    .btn {
      display: inline-block;
      padding: 10px 16px;
      border: 2px solid var(--text);
      background: var(--bg);
      font-family: var(--mono);
      font-weight: 700;
      font-size: 12px;
      letter-spacing: .06em;
      text-transform: uppercase;
      box-shadow: 4px 4px 0 var(--accent);
    }
    .btn--ghost { box-shadow: none; }
    .btn--ghost:hover, .btn--ghost:focus-visible { border-color: var(--accent); color: var(--accent); }

    /* sections */
    .section { padding: 64px 0; border-top: 2px solid var(--text); scroll-margin-top: 52px; }
    h2 { font-size: clamp(26px, 4vw, 34px); font-weight: 700; letter-spacing: -.03em; text-transform: uppercase; }
    h3 { font-size: 18px; font-weight: 700; letter-spacing: -.02em; text-transform: uppercase; }

    /* skills */
    .skills { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 28px; }
    .card { border: 2px solid var(--text); background: var(--surface); padding: 20px; }
    .card p { color: var(--muted); font-size: 14px; margin-top: 8px; }
    .tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }
    .tag { font-family: var(--mono); font-size: 11px; border: 1px solid var(--dim); padding: 2px 8px; }
    .callout {
      margin-top: 16px;
      border: 2px dashed var(--accent);
      background: rgba(59, 108, 255, .06);
      padding: 18px 20px;
      display: flex; flex-wrap: wrap; gap: 8px 24px; align-items: center; justify-content: space-between;
    }
    .callout p { color: var(--muted); font-size: 14px; margin-top: 4px; }
    .callout .tags { margin-top: 0; }

    /* apps */
    .apps { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin-top: 28px; }
    .app {
      display: flex; flex-direction: column; gap: 12px;
      border: 2px solid var(--text);
      background: var(--surface);
      padding: 20px;
      box-shadow: 6px 6px 0 var(--accent);
    }
    .app-head { display: flex; align-items: center; gap: 12px; }
    .app-head img { width: 44px; height: 44px; border-radius: 11px; flex-shrink: 0; }
    .app h3 { font-size: 20px; }
    .meta { font-family: var(--mono); font-size: 11px; color: var(--muted); letter-spacing: .04em; }
    .app p { font-size: 14px; }
    .app .go { margin-top: auto; font-family: var(--mono); font-weight: 700; font-size: 12px; letter-spacing: .06em; text-transform: uppercase; }
    .app-soon {
      display: grid; place-items: center; min-height: 160px;
      border: 2px dashed var(--dim);
      color: var(--muted);
      font-family: var(--mono); font-size: 12px; letter-spacing: .1em; text-transform: uppercase;
    }

    /* contact */
    .contact h2 { font-size: clamp(30px, 5vw, 44px); }
    .contact p { color: var(--muted); margin-top: 12px; max-width: 460px; }

    /* footer */
    .footer {
      border-top: 2px solid var(--text);
      padding: 20px 0;
      font-family: var(--mono); font-size: 11px; letter-spacing: .06em; text-transform: uppercase;
      color: var(--muted);
    }
    .footer .container { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 24px; }

    @media (min-width: 720px) {
      :root { --gutter: 24px; }
    }
    @media (max-width: 719.98px) {
      .hero { padding: 56px 0 48px; }
      .section { padding: 48px 0; }
      .skills, .apps { grid-template-columns: 1fr; }
      .nav-links { gap: 14px; }
    }
    @media (prefers-reduced-motion: no-preference) {
      .btn:not(.btn--ghost), .app { transition: transform .12s ease, box-shadow .12s ease; }
      .btn:not(.btn--ghost):hover, .btn:not(.btn--ghost):focus-visible,
      .app:hover, .app:focus-visible { transform: translate(2px, 2px); box-shadow: 2px 2px 0 var(--accent); }
    }
  </style>
</head>
<body>
  <header class="nav">
    <div class="container">
      <a href="#top">hansukun</a>
      <nav class="nav-links" aria-label="Page">
        <a href="#skills">Skills</a>
        <a href="#apps">Apps</a>
        <a href="#contact">Contact</a>
      </nav>
    </div>
  </header>

  <main id="top">
    <section class="hero">
      <div class="container">
        <span class="eyebrow">Remote · Web Developer</span>
        <h1>Hans<br>De Guzman<br><span class="block">Web Dev</span></h1>
        <p class="lead">I build sites and apps with <b>WordPress</b>, <b>React</b> and <b>Vue</b>. Recently started shipping <b>Android</b> apps on the side.</p>
        <div class="btn-row">
          <a class="btn" href="mailto:devhansukun@gmail.com">Get in touch →</a>
          <a class="btn btn--ghost" href="https://www.linkedin.com/in/hansdg/" target="_blank" rel="noopener">LinkedIn</a>
        </div>
      </div>
    </section>

    <section class="section" id="skills">
      <div class="container">
        <span class="eyebrow">01 / Skills</span>
        <h2>What I work with</h2>
        <div class="skills">
          <div class="card">
            <h3>WordPress</h3>
            <p>Custom themes and plugins, block editor, WooCommerce, performance and hosting.</p>
            <div class="tags"><span class="tag">PHP</span><span class="tag">Gutenberg</span><span class="tag">ACF</span><span class="tag">WooCommerce</span></div>
          </div>
          <div class="card">
            <h3>React</h3>
            <p>Component-driven front ends, hooks, state, and integration with REST/GraphQL APIs.</p>
            <div class="tags"><span class="tag">TypeScript</span><span class="tag">Next.js</span><span class="tag">Tailwind</span></div>
          </div>
          <div class="card">
            <h3>Vue</h3>
            <p>Vue 3 with the Composition API, Pinia, and Nuxt for full apps and admin UIs.</p>
            <div class="tags"><span class="tag">Vue 3</span><span class="tag">Pinia</span><span class="tag">Nuxt</span></div>
          </div>
        </div>
        <div class="callout">
          <div>
            <h3>Android — on the side</h3>
            <p>Built with React Native. First app in review on Google Play; more in the works.</p>
          </div>
          <div class="tags"><span class="tag">React Native</span><span class="tag">Google Play</span></div>
        </div>
      </div>
    </section>

    <section class="section" id="apps">
      <div class="container">
        <span class="eyebrow">02 / Apps</span>
        <h2>Things I've shipped</h2>
        <div class="apps">
          <a class="app" href="settled/">
            <div class="app-head">
              <img src="assets/settled-icon.svg" alt="" width="44" height="44">
              <div>
                <h3>Settled</h3>
                <span class="meta">Android · Coming soon to Google Play</span>
              </div>
            </div>
            <p>An offline checklist for the bills you pay every month — the spreadsheet you already keep, as an app.</p>
            <span class="go">View the app page →</span>
          </a>
          <div class="app-soon" aria-hidden="true">More coming soon</div>
        </div>
      </div>
    </section>

    <section class="section contact" id="contact">
      <div class="container">
        <span class="eyebrow">03 / Contact</span>
        <h2>Let's build something.</h2>
        <p>Open to remote work. Email is the fastest way to reach me.</p>
        <div class="btn-row">
          <a class="btn" href="mailto:devhansukun@gmail.com">devhansukun@gmail.com</a>
          <a class="btn btn--ghost" href="https://www.linkedin.com/in/hansdg/" target="_blank" rel="noopener">LinkedIn →</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <span>© 2026 Hans De Guzman</span>
      <span>Built with plain HTML &amp; CSS</span>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 5: Run the checker**

Run: `python scripts/check_site.py`
Expected: `all checks passed`, exit 0. If a `[portfolio] copy '…' missing` line appears, the HTML text and `PORTFOLIO_COPY` disagree on an apostrophe or spacing — fix the HTML to match the list (plain `'`, not a curly quote).

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "feat: portfolio home page

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: Browser verification

**Files:**
- Create: `.claude/launch.json` (dev-server config, ignored by git)
- Modify: `.gitignore` (add `.claude/`)
- Modify: `index.html`, `settled/index.html`, `settled/privacy.html` — only if a check below fails

**Interfaces:**
- Consumes: the three pages from Tasks 1–3.

- [ ] **Step 1: Ignore the launch config and add it**

Append `.claude/` to `.gitignore`:

```bash
printf '.claude/\n' >> .gitignore && cat .gitignore
```

Expected: two lines, `.superpowers/` and `.claude/`.

Create `.claude/launch.json`:

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "site",
      "runtimeExecutable": "python",
      "runtimeArgs": ["-m", "http.server", "8000", "--bind", "127.0.0.1"],
      "port": 8000
    }
  ]
}
```

- [ ] **Step 2: Start the server and check the portfolio at desktop width**

Use the built-in browser: `preview_start` with `name: "site"`, then `navigate` to `http://localhost:8000/`. Take a screenshot. Then run with `javascript_tool`:

```js
({
  noHScroll: document.documentElement.scrollWidth <= window.innerWidth,
  grotesk: document.fonts.check('700 16px "Space Grotesk"'),
  mono: document.fonts.check('700 12px "JetBrains Mono"'),
  icon: [...document.images].every(i => i.complete && i.naturalWidth > 0),
  settledHref: document.querySelector('a.app').getAttribute('href'),
  h1: document.querySelector('h1').innerText,
})
```

Expected: `noHScroll: true`, `grotesk: true`, `mono: true`, `icon: true`, `settledHref: "settled/"`, `h1` containing `HANS`, `DE GUZMAN`, `WEB DEV`. Read the console with `read_console_messages` (`onlyErrors: true`): no 404s.

- [ ] **Step 3: Check the portfolio at phone width**

`resize_window` with `preset: "mobile"` (375×812), reload, screenshot, then run the same `javascript_tool` snippet. Expected: `noHScroll: true`; skills and apps are single-column in the screenshot; the H1 does not clip at the right edge. Then `resize_window` with `preset: "desktop"`.

- [ ] **Step 4: Follow the links**

Click the Settled app card. Expected: URL becomes `http://localhost:8000/settled/`, the Settled hero (`Your monthly bills, settled.`) shows, and the nav's first link reads `← Hans De Guzman`. Click that link. Expected: back on `http://localhost:8000/`. Navigate to `http://localhost:8000/settled/privacy.html`, click the footer `Hans De Guzman` link. Expected: back on `/`. At the mobile preset on `/settled/`, screenshot the nav: only `←` shows for the back-link and the four links fit beside the brand without wrapping or overflow.

- [ ] **Step 5: Contrast spot-check**

With `javascript_tool` on `/`:

```js
const lum = h => { const [r,g,b] = h.match(/\w\w/g).map(x => parseInt(x,16)/255).map(c => c <= .03928 ? c/12.92 : ((c+.055)/1.055)**2.4); return .2126*r+.7152*g+.0722*b; };
const ratio = (a,b) => { const [l1,l2] = [lum(a),lum(b)].sort((x,y)=>y-x); return ((l1+.05)/(l2+.05)).toFixed(2); };
({ mutedOnBg: ratio('#a1a1aa','#0b0b0d'), mutedOnSurface: ratio('#a1a1aa','#121216'), blockText: ratio('#0b0b0d','#3b6cff') })
```

Expected: `mutedOnBg` ≥ 7, `mutedOnSurface` ≥ 6.5, `blockText` ≥ 4.5.

- [ ] **Step 6: Fix anything that failed, re-run the checker, commit**

If any step above failed, fix the page, re-run that step, then:

Run: `python scripts/check_site.py`
Expected: `all checks passed`.

```bash
git add -A && git commit -m "chore: portfolio responsive and contrast verification

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

If nothing needed fixing, the commit contains only the `.gitignore` line — that's fine.

- [ ] **Step 7: Stop the preview server**

`preview_stop` on the `site` server. Confirm `git status --short` is empty.
