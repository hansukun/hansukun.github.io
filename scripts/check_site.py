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
    if "devhansukun@gmail.com" not in page.text:
        out.append("privacy.html: contact address missing")
    if not re.search(r"Effective \d{1,2} \w+ 20\d\d", page.text):
        out.append("privacy.html: effective date missing")
    if not any(h.startswith("index.html") for h in page.hrefs):
        out.append("privacy.html: no link back to the brochure")
    return out


CHECKS = [
    ("files", check_files_exist, [None]),
    ("basics", check_page_basics, PAGES),
    ("tokens", check_tokens, PAGES),
    ("links", check_links, PAGES),
    ("screens", check_screens, [None]),
    ("hero", check_hero, ["index.html"]),
    ("features", check_features, ["index.html"]),
    ("pricing", check_pricing, ["index.html"]),
    ("privacy", check_privacy, ["privacy.html"]),
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
