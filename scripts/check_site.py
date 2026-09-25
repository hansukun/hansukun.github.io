"""Static checks for hansukun.github.io (portfolio + Settled). Run: python scripts/check_site.py"""
from __future__ import annotations

import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORTFOLIO = "index.html"
SETTLED_PAGES = ["settled/index.html", "settled/privacy.html"]
PAGES = [PORTFOLIO, *SETTLED_PAGES]
ALLOWED_EXTERNAL_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com", "www.linkedin.com"}
GAME_JS = "assets/game/game.js"
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


class Page(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self.dir = path.parent
        self.html = path.read_text(encoding="utf-8")
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.scripts: list[dict[str, str | None]] = []
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
            self.scripts.append(a)
            if "src" not in a:
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


def rel(page: Page, target: str) -> str:
    """`target` (repo-root relative) as seen from `page`'s directory, with / separators."""
    return os.path.relpath(ROOT / target, page.dir).replace(os.sep, "/")


# ---- checks ---------------------------------------------------------------

def check_files_exist(_: str) -> list[str]:
    out = []
    for f in [".nojekyll", ".gitignore", "assets/settled-icon.svg", "settled/assets/icon.svg", "settled/assets/icon-512.png", GAME_JS, *PAGES]:
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
    want = TITLE_MUST_MENTION[name]
    if not page.title or want not in page.title:
        out.append(f"{name}: <title> must mention {want}, got {page.title!r}")
    if 'name="viewport"' not in page.html:
        out.append(f"{name}: missing viewport meta")
    if page.inline_scripts:
        out.append(f"{name}: inline <script> is not allowed")
    want = rel(page, GAME_JS)
    if not (len(page.scripts) == 1 and page.scripts[0].get("src") == want and "defer" in page.scripts[0]):
        out.append(f'{name}: must load exactly one <script src="{want}" defer>')
    return out


def check_tokens(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    for var, value in TOKENS.get(name, {}).items():
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
        elif href.startswith("data:"):
            continue
        elif href.startswith("mailto:"):
            continue
        elif host := host_of(href):
            if host not in ALLOWED_EXTERNAL_HOSTS and not host.endswith("google.com"):
                out.append(f"{name}: unexpected external host {host}")
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
    return out


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


def check_hero(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    if "Your monthly bills, settled." not in page.text:
        out.append(f"{name}: hero headline missing")
    if "Coming soon to Google Play" not in page.text:
        out.append(f"{name}: coming-soon caption missing")
    if "assets/google-play-badge.svg" not in page.srcs:
        out.append(f"{name}: badge image missing")
    if not any("screens/month.webp" in s for s in page.srcs):
        out.append(f"{name}: hero phone must show screens/month.webp")
    if re.search(r'href="https?://play\.google\.com', page.html):
        out.append(f"{name}: badge must not link to Play yet")
    return out


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
            out.append(f"{name}: missing id={i}")
    for t in FEATURE_TITLES:
        if t not in page.text:
            out.append(f"{name}: feature card '{t}' missing")
    for s in STEP_TITLES:
        if s not in page.text:
            out.append(f"{name}: step '{s}' missing")
    return out


def check_pricing(name: str) -> list[str]:
    page = load(name)
    if page is None:
        return []
    out = []
    for i in ("pricing", "screens"):
        if i not in page.ids:
            out.append(f"{name}: missing id={i}")
    for s in ("month-settled", "template", "history", "settings"):
        if not any(f"screens/{s}.webp" in x for x in page.srcs):
            out.append(f"{name}: screens strip missing {s}")
    for t in ("7-day free trial", "Set on Google Play"):
        if t not in page.text:
            out.append(f"{name}: pricing copy '{t}' missing")
    pricing_text = page.text.split("Free to use.", 1)[-1]
    if re.search(r"[₱$€]\s?\d", pricing_text):
        out.append(f"{name}: pricing must not state a currency amount")
    return out


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
            out.append(f"{name}: section '{h}' missing")
    if "drive.appdata" not in page.text:
        out.append(f"{name}: must name the drive.appdata scope")
    if "devhansukun@gmail.com" not in page.text:
        out.append(f"{name}: contact address missing")
    if not re.search(r"Effective \d{1,2} \w+ 20\d\d", page.text):
        out.append(f"{name}: effective date missing")
    if not any(h.startswith("index.html") for h in page.hrefs):
        out.append(f"{name}: no link back to the brochure")
    return out


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


CHECKS = [
    ("files", check_files_exist, [None]),
    ("basics", check_page_basics, PAGES),
    ("tokens", check_tokens, PAGES),
    ("links", check_links, PAGES),
    ("screens", check_screens, [None]),
    ("game-assets", check_game_assets, [None]),
    ("hero", check_hero, ["settled/index.html"]),
    ("features", check_features, ["settled/index.html"]),
    ("pricing", check_pricing, ["settled/index.html"]),
    ("privacy", check_privacy, ["settled/privacy.html"]),
    ("backlinks", check_backlinks, SETTLED_PAGES),
    ("portfolio", check_portfolio, [PORTFOLIO]),
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
