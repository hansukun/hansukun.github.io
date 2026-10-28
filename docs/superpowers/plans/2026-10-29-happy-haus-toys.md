# Happy Haus Toys Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the Happy Haus Toys catalog (layout A, "Shop front") as a real, public one-page site at `works/happy-haus-toys/`, and list it in the portfolio's Works section.

**Architecture:** One hand-written `index.html` holds every product as static markup, so the shelves and specs read without JavaScript. `style.css` carries the world tokens and components. `app.js` adds the behavior on top: opening bins, color swatches, and copying the order note when a parent taps the Instagram DM link. `scripts/check_site.py` is the static test suite. A browser test page covers `app.js`, following the existing `tests/game-test.html` pattern.

**Tech Stack:** HTML5, CSS (custom properties, grid, `mask`, `color-mix`), vanilla JS (no modules, no build), Google Fonts (Baloo 2, Nunito, Patrick Hand), Python 3 + Pillow (checker, icon), impeccable CLI (provenance, detector, finish review).

**Spec:** `docs/superpowers/specs/2026-10-29-happy-haus-toys-design.md`. The product record is `works/happy-haus-toys/PRODUCT.md`. The approved mockup is `works/happy-haus-toys/mockups/a-shop-front.html` with `mockups/world.css` and `mockups/order.js`; its layout CSS is in `works/happy-haus-toys/.impeccable/source/a.css`. The build reproduces that mockup.

## Global Constraints

- Working directory for every command: `E:\Hans\Projects\Web App Dev Page`. Windows: create files longer than ~40 lines with the Write/Edit tools, not heredocs.
- Before Task 1, branch off `main`: `git checkout -b feat/happy-haus-toys`.
- Static files only, no build step. All paths relative (`assets/...`), never root-absolute.
- External resources: only the Google Fonts stylesheet, `https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@500;700;800&family=Patrick+Hand&display=swap`.
- Instagram URLs, exactly: DM `https://ig.me/m/happyhaustoys`; profile `https://www.instagram.com/happyhaustoys/`.
- Tokens on `:root` in `style.css`, exact values: `--ink: #164a90; --ink-deep: #0e3363; --ink-soft: #33598f; --cream: #fdf6e6; --peach: #fbe2cc; --paper: #f3e6d0; --tape: #fbe07a; --coral: #ee6f45; --sun: #f5b52e; --leaf: #7fa47a; --sky: #4a86c5; --cocoa: #8b5e3c; --holiday: #a5121c`. `body` has an explicit background.
- The logo (`assets/logo-art.png`) only ever sits on the scalloped cream `.badge`.
- Product copy is word for word from this table, which matches PRODUCT.md. Prices are written `₱13,450` (peso sign, comma thousands). Descriptions are the spec's approved one-liners.

| id | Name | Shelf | Price | Colors (swatch hex → image) | Size | Includes | Description |
|---|---|---|---|---|---|---|---|
| forest-house | Forest House slide set | Climb & slide | 13450 | Autumn Beige `#c9a27a` → forest-house-beige; Spring Green `#b6c46a` → forest-house-green | L 1860 × W 2050 × H 1640 mm | 2 slides; Basketball hoop; Telescope toy; Climbing ladder; Hide-and-seek nook / storage; Two-way ladder orientation | Two slides side by side, with a basketball hoop in the middle. |
| forest-nest | Forest Nest slide set | Climb & slide | 12450 | Autumn Beige `#c9a27a` → forest-nest-beige; Spring Green `#b6c46a` → forest-nest-green | L 1860 × W 2050 × H 1640 mm | 1 slide + 1 climbing frame; Basketball hoop; Telescope toy; Climbing ladder; Hide-and-seek nook / storage; Two-way ladder and slide orientation | One slide plus a climbing frame to scramble up. |
| tree | Rotating Tree bookshelf | Read & store | 3950 | White & Grey `#e4e1da` → tree-white; Classic Green `#6f8f5a` → tree-green | Ø 570 × H 1216 mm | 360° rotation; 6 storage panels; 6 side book panels | A Christmas tree of books that turns all the way round. |
| whale | Whale 2-in-1 bookshelf & storage | Read & store | 4600 | Grey & White `#cdd1d4` → whale | L 670 × W 290 × H 980 mm | 4-layer bookshelf; 4 removable bins | Covers forward on top, toys in the bins below. |
| bubble | Bubble 2-in-1 bookshelf & storage | Read & store | 2600 | Beige `#e2cbad` → bubble | L 660 × W 350 × H 810 mm | 2-layer bookshelf; 4 removable bins | Books face out on two shelves, toys go in four bins below. |
| shop | Shop play storage | Play pretend | 3200 | White & Grey `#d8d9da` → shop-grey; Beige `#e2cbad` → shop-beige | L 800 × W 330 × H 1000 mm | Shop counter with awning; 6 removable bins | A little shop front that tidies the toys away. |
| serene | Serene Playhouse | Play pretend | 3950 | Grey & White `#cdd1d4` → serene | L 1080 × W 800 × H 1100 mm | Arched door with curtains; Side play counter | A whole house with a curtained door and a side counter. |

- Shelf order: Climb & slide, Read & store, Play pretend; products in table order within each shelf. The Rotating Tree bin carries the "Holiday edition" cloud.
- Shared perks, in order: Easy installation, Rounded corners, Stable support, Odor-free HDPE, Safe and durable.
- Never state delivery, shipping, fees, cash on delivery, payment methods, warranty, stock counts, reviews or ratings.
- Fixed copy: headline `On-hand playhouses, slides & shelves for your little ones.`; subline `Pick a piece off the shelf, choose its color, and message us on Instagram to order.`; counter `Found the one?` / `We reply on Instagram.` / `Message us`; perks heading `Every piece is`; footer `Happy Haus Toys` / `On-hand items, ordered by message.` / `@happyhaustoys on Instagram`; bin buttons `Message to order` and `Back to the shelf`.
- Order notes, exactly (price via `peso()`):
  - product: `Hi Happy Haus! I'd like to order the {name} in {color} ({price}). Is it available?`
  - counter: `Hi Happy Haus! I'd like to ask about your toys.`
- Toasts, exactly:
  - copied: `Order note copied. Paste it in the chat with @happyhaustoys.` (handle in `<b>`)
  - copy failed, product: `Tell us in the chat: {name} – {color}` (product and color in `<b>`)
  - copy failed, counter: `Say hi to @happyhaustoys in the chat.` (handle in `<b>`)
- The page is public: no `noindex`.
- No impeccable direction contract, brief text or comments about it in any shipped file.
- Commit after each task with `feat:`/`chore:`/`docs:` messages ending in `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Run checks with `python scripts/check_site.py` (exit 0, prints `all checks passed`).
- Run browser tests against the `site` preview server (`.claude/launch.json`, port 8000): open `http://localhost:8000/tests/happy-haus-test.html` and read `#result`.

## Review Focus

- **Clipboard blocked** (Instagram's in-app browser, plain http, a denied permission): the DM link still opens, and the toast tells the parent what to type. Pinned by `copy failure falls back to naming the product` in Task 3.
- **Pop-ups blocked:** the order buttons are real `<a target="_blank">` links that JS never `preventDefault`s, so the browser opens the DM natively. Pinned by `order click does not cancel navigation` in Task 3.
- **JavaScript fails to load:** every product's details are readable. The HTML has no `hidden` on `.bin-detail`; `init()` hides them. Pinned by `[hh] detail panels must not be hidden in markup` in Task 2 and `init hides every detail` in Task 3.
- **Keyboard users:** Escape closes the open bin, and "Back to the shelf" returns focus to its bin. Pinned by `escape closes and refocuses` in Task 3.
- **Narrow phones (320px):** long names such as "Bubble 2-in-1 bookshelf & storage" wrap inside their tags with no sideways scroll. Pinned by the 320px measurement in Task 4.

---

## File map

| Path | Responsibility |
|---|---|
| `works/happy-haus-toys/index.html` | The catalog: head and meta, shop front, three shelves of bins (all products as static markup), perks, footer, counter bar. |
| `works/happy-haus-toys/style.css` | Tokens, world components (tape, note, badge, sticker, holiday cloud, swatches, order button, perks, toast), shop-front layout. Port of `mockups/world.css` plus `.impeccable/source/a.css`. |
| `works/happy-haus-toys/app.js` | Behavior: `window.HappyHaus` API plus auto `init()`. |
| `works/happy-haus-toys/assets/products/*.webp` (+ `.json` provenance) | Product photos (exist; Task 1 fixes and records them). |
| `works/happy-haus-toys/assets/logo-art.png`, `assets/icon.png`, `assets/og.jpg` | Logo art, 180×180 favicon on its badge, 1200×630 share image. |
| `scripts/make_hh_icon.py` | Builds `assets/icon.png` from `logo-art.png` on the scalloped badge. |
| `scripts/check_site.py` | Gains the Happy Haus checks. |
| `tests/happy-haus-test.html` | Browser tests for `app.js`. |
| `index.html` (root) | Works card replaces the `.work-empty` placeholder. |
| `assets/works/happy-haus-toys.png` | 1280×800 screenshot for the Works card. |
| `works/happy-haus-toys/mockups/` | Deleted in Task 5. |

---

### Task 1: Product images: fixes, provenance, favicon

**Files:**
- Modify: `works/happy-haus-toys/.impeccable/source/crops.py` (git-ignored; Serene patch)
- Modify: `works/happy-haus-toys/assets/products/serene.webp` (re-cropped), any other crop the recheck flags
- Create: `works/happy-haus-toys/assets/products/*.webp.json`, `works/happy-haus-toys/assets/logo-art.png.json` (provenance sidecars written by impeccable)
- Create: `scripts/make_hh_icon.py`, `works/happy-haus-toys/assets/icon.png`
- Modify: `scripts/check_site.py`

**Interfaces:**
- Produces: `HH_DIR = "works/happy-haus-toys"`, `HH_POSTS: dict[str, str]` (image stem → Instagram post id, from the spec's table) and `check_hh_assets(_) -> list[str]` in `check_site.py`, registered in `CHECKS` as `("hh-assets", check_hh_assets, [None])`.
- Produces: `assets/icon.png`, 180×180 RGBA.

- [ ] **Step 1: Write `check_hh_assets`.** It fails if any of these is false:
  - each of the 11 `assets/products/{stem}.webp` and `assets/logo-art.png` exists;
  - each has a provenance sidecar (`<file>.json`) whose text contains its post id from `HH_POSTS` (logo → `De042ngEgbD`);
  - `assets/icon.png` exists and is 180×180 (read the IHDR like `png_size`).
- [ ] **Step 2: Run the checker and confirm it fails.** Run `python scripts/check_site.py`. Expect `[hh-assets]` lines: no sidecars, no icon.
- [ ] **Step 3: Fix the Serene crop.** In `crops.py`, replace Serene's clone patch so neither the "Grey+White Color" label nor the "L 1080mm…" dimension label leaves a seam or fragment. Then run `python crops.py <tmp-out>` from `.impeccable/source/` and copy only `serene.webp` over the shipped one.
- [ ] **Step 4: Recheck every crop.** Make a full-size contact sheet of all 11 shipped crops and look at it. Re-crop any image that shows leftover tape, label text or the logo badge. The re-crop gate is visual: no baked-in text visible.
- [ ] **Step 5: Embed provenance.** For each image, run the command below with the prompt text `Sourced from Instagram @happyhaustoys, post https://www.instagram.com/happyhaustoys/p/<id>/ (slide 1); cropped and label-patched with .impeccable/source/crops.py.` For the logo, the text names the logo badge on post `De042ngEgbD`.

  ```
  "C:/Users/deguz/.claude/plugins/cache/impeccable/impeccable/4.5.2/skills/impeccable/scripts/impeccable" embed-prompt <file> --prompt "<text>"
  ```
- [ ] **Step 6: Write `scripts/make_hh_icon.py`.** It draws the badge's scallop path (the SVG path in `mockups/world.css` `.badge::before`, viewBox 0 0 200 200) filled `#fffaf0`, places `logo-art.png` at 70% width centered, saves a 180×180 PNG to `works/happy-haus-toys/assets/icon.png`, then runs it. Embed provenance on `icon.png` the same way (origin: built by the script from `logo-art.png`).
- [ ] **Step 7: Run the checker; expect `all checks passed`.**
- [ ] **Step 8: Commit** `scripts/check_site.py scripts/make_hh_icon.py works/happy-haus-toys/assets works/happy-haus-toys/PRODUCT.md docs/superpowers/specs/2026-10-29-happy-haus-toys-design.md docs/superpowers/plans/2026-10-29-happy-haus-toys.md` with `chore: Happy Haus spec, plan, product images and favicon`. Don't add `works/happy-haus-toys/mockups/`; it is deleted in Task 5.

### Task 2: The catalog page (markup and styles)

**Files:**
- Create: `works/happy-haus-toys/index.html`, `works/happy-haus-toys/style.css`
- Modify: `scripts/check_site.py`

**Interfaces:**
- Consumes: product images and `assets/icon.png` from Task 1.
- Produces: the markup contract `app.js` relies on. Per product:
  - `<article class="bin" id="p-{id}" data-product="{id}" data-name="{Name}" data-price="{price integer}">`
  - inside it, `<button class="bin-face" type="button" aria-expanded="false" aria-controls="d-{id}">`, which wraps `.bin-seat > .bin-photo > img[data-photo]` and the `.tag`;
  - then `<div class="bin-detail" id="d-{id}">`, with no `hidden` attribute.
  - Detail contents:
    - two-color products: `ul.swatches` of `<button class="swatch" type="button" data-swatch="{i}" data-color="{Color}" data-src="assets/products/{image}.webp" aria-pressed="true|false">`, the first pressed;
    - single-color products: `<p class="one-color">Comes in {Color}</p>`;
    - an element `[data-color-label]` showing the current color name;
    - `<a class="order" href="https://ig.me/m/happyhaustoys" target="_blank" rel="noopener" data-order data-color="{first color}">`;
    - `<button class="bin-close" type="button">`.
  - The counter bar holds `<a class="order order--sun" href="https://ig.me/m/happyhaustoys" target="_blank" rel="noopener" data-order>`, with no `data-color` and outside any `.bin`.
  - Scripts: exactly one, `<script src="app.js" defer></script>`, and no inline scripts.
- Produces: `check_hh_page`, `check_hh_catalog`, `check_hh_claims` in `check_site.py`. Add `"ig.me"` and `"www.instagram.com"` to `ALLOWED_EXTERNAL_HOSTS`. Register `HH = "works/happy-haus-toys/index.html"` with `check_links` and the three new checks, but **not** in `PAGES`: `check_page_basics` requires `game.js`, which this page doesn't load.

- [ ] **Step 1: Write the checks.**
  - **`check_hh_page`:**
    - `lang="en"`, a `<title>` containing `Happy Haus`, the viewport meta, and a `<meta name="description">`;
    - `og:title`, `og:description`, `og:image` with content ending `assets/og.jpg`, `og:url`, and `twitter:card` = `summary_large_image`;
    - no `noindex`, and `<link rel="icon" href="assets/icon.png">`;
    - `style.css` linked, the Google Fonts URL from the Global Constraints present, and the single deferred `app.js` script with no inline scripts;
    - every token from the Global Constraints defined in `style.css`, and `body` has a background there.
  - **`check_hh_catalog`:**
    - for each table row: `id="p-{id}"`, its name, `peso(price)`, every color name, the size string, every include line and the description all appear in the page text;
    - the three shelf titles appear in order, along with the five perks, the headline, the subline, `Message to order`, `Back to the shelf` and `Found the one?`;
    - exactly 7 `class="bin"`;
    - no `.bin-detail` tag carries `hidden` (message: `[hh] detail panels must not be hidden in markup`);
    - every `aria-controls` value matches an id;
    - `https://ig.me/m/happyhaustoys` appears at least 8 times (7 bins plus the counter).
  - **`check_hh_claims`:** the page text matches none of `deliver|shipping|cash on delivery|\bCOD\b|warranty|in stock|\breview|testimonial|\brated\b` (case-insensitive).
- [ ] **Step 2: Run the checker; expect `[hh]` failures (page missing).**
- [ ] **Step 3: Write `style.css`.** Port `mockups/world.css` (tokens and components) and `.impeccable/source/a.css` (layout), using the token values above. Fold in what the mockup round already fixed:
  - sprinkles only on `.front`;
  - the toast hidden with `visibility` when inactive;
  - the counter button `white-space: nowrap`;
  - `line-height: 1.3` on `.bin-line`.

  Add `.bin.open` focus styling and theme `::selection`, `:focus-visible` and the scrollbar from the palette.
- [ ] **Step 4: Write `index.html`.** Follow the generated `mockups/a-shop-front.html` structure with the markup contract above. All product copy comes from the table. Add the head meta from Step 1:
  - `og:url`: `https://hansukun.github.io/works/happy-haus-toys/`
  - `og:image`: `https://hansukun.github.io/works/happy-haus-toys/assets/og.jpg`
  - description: `On-hand playhouses, slides, bookshelves and toy storage for little ones. Browse colors, sizes and prices, then message Happy Haus Toys on Instagram to order.`
- [ ] **Step 5: Run the checker; expect `all checks passed`** (og.jpg's existence is checked in Task 5).
- [ ] **Step 6: Commit** with `feat: Happy Haus Toys catalog page`.

### Task 3: Behavior (`app.js`) with browser tests

**Files:**
- Create: `tests/happy-haus-test.html`, `works/happy-haus-toys/app.js`

**Interfaces:**
- Consumes: the markup contract from Task 2.
- Produces: `window.HappyHaus` with:
  - `peso(n: number): string` returns `₱13,450` for `13450`;
  - `orderNote(name?: string, color?: string, price?: number): string` returns the product note, or the counter note when `name` is absent;
  - `setColor(bin: Element, i: number): void` presses swatch `i`, sets `img[data-photo]` `src` to its `data-src` and `alt` to `{name} in {color}`, sets every `[data-color-label]` text and the bin's `[data-order]` `data-color`;
  - `openBin(bin: Element): void` closes any other open bin, then adds `.open`, unhides `.bin-detail`, sets `aria-expanded="true"` and scrolls the bin into view (`behavior: 'auto'` under reduced motion);
  - `closeBin(bin: Element, opts?: { focus?: boolean }): void`;
  - `init(root: ParentNode = document): void` hides every `.bin-detail`, then wires clicks (bin face toggles; swatch calls `setColor`; close button calls `closeBin({focus: true})`; `[data-order]` copies the note), plus Escape on keydown.
  - `app.js` calls `init()` on `DOMContentLoaded` unless `window.HAPPY_HAUS_NO_AUTOINIT === true`.
  - The order click starts `navigator.clipboard.writeText(note)` synchronously in the handler. It never calls `preventDefault()` or `window.open`. On success it shows the copied toast; on rejection, or with no clipboard API, it shows the matching failure toast.
  - The toast is a single `.toast[role="status"]` that `init` appends to `document.body`. It gets `.show` for 4200 ms.

- [ ] **Step 1: Write `tests/happy-haus-test.html`.**
  - **Setup:** same shell as `tests/game-test.html` (`noindex`, a `#result` `<pre>`). It sets `window.HAPPY_HAUS_NO_AUTOINIT = true`, loads `../works/happy-haus-toys/app.js`, and holds a fixture that follows the contract: a two-color `forest-nest` bin, a single-color `whale` bin and a counter link.
  - **Clipboard stub:** replace `navigator.clipboard` (`Object.defineProperty`) with a stub that records text and resolves or rejects on demand.
  - **Link guard:** a `window` click listener records `defaultPrevented` and only then calls `preventDefault()`, so links don't navigate during tests.
  - **Output:** `PASS n/n`, or one `FAIL name: detail` line per failure.
  - **Tests:**
    - `peso formats thousands`: `peso(13450) === "₱13,450"`, `peso(2600) === "₱2,600"`.
    - `product note is exact`: `orderNote("Forest Nest slide set","Autumn Beige",12450) === "Hi Happy Haus! I'd like to order the Forest Nest slide set in Autumn Beige (₱12,450). Is it available?"`.
    - `counter note is exact`: `orderNote() === "Hi Happy Haus! I'd like to ask about your toys."`.
    - `init hides every detail`: after `init(fixture)`, every `.bin-detail` has `hidden`, and every `.bin-face` has `aria-expanded="false"`.
    - `opening one bin closes the other`: open whale, then forest-nest; only forest-nest has `.open` and a visible detail.
    - `swatch swaps photo, label and order color`: click swatch 1 of forest-nest. The img `src` ends `forest-nest-green.webp`, the alt is `Forest Nest slide set in Spring Green`, `[data-color-label]` reads `Spring Green`, the order link's `data-color` is `Spring Green`, and swatch 1 has `aria-pressed="true"` while swatch 0 has `"false"`.
    - `order copies the chosen color`: after that swatch, clicking the order link writes the Spring Green note to the stub, and the toast text is `Order note copied. Paste it in the chat with @happyhaustoys.`.
    - `order click does not cancel navigation`: the recorded `defaultPrevented` from the app's handler is `false`.
    - `copy failure falls back to naming the product`: with the stub rejecting, the whale order toast reads `Tell us in the chat: Whale 2-in-1 bookshelf & storage – Grey & White`.
    - `counter copies the general note`: the counter link writes the counter note.
    - `escape closes and refocuses`: open forest-nest, dispatch Escape. The bin is closed and `document.activeElement` is its `.bin-face`.
    - `back to the shelf refocuses`: same, through `.bin-close`.
- [ ] **Step 2: Run the tests and confirm they fail.** Start the `site` preview and open the test page. `#result` shows failures (`HappyHaus` undefined).
- [ ] **Step 3: Write `app.js` to the interface above** (an IIFE; no globals other than `window.HappyHaus`).
- [ ] **Step 4: Run the tests again; expect `PASS 12/12`.** Also open `/works/happy-haus-toys/` and confirm the console has no errors.
- [ ] **Step 5: Commit** `tests/happy-haus-test.html works/happy-haus-toys/app.js` with `feat: Happy Haus bins, swatches and order notes`.

### Task 4: Visual verification and impeccable finish

**Files:**
- Modify: `works/happy-haus-toys/style.css`, `index.html` (review fixes only)
- Create: `works/happy-haus-toys/DESIGN.md` (impeccable documenter), `works/happy-haus-toys/.impeccable/review/*.png` (git-ignored captures)

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: the finished page that Task 5 screenshots.

- [ ] **Step 1: One capture round.**
  - **Captures:** with the sign's swing animation settled, capture `.impeccable/review/mobile.png` (390 wide, full page) and `desktop.png` (1440 wide, full page) with one bin open, plus `user-<width>.png` at the pane's own width.
  - **Narrow-phone check:** at 320×700, run `document.documentElement.scrollWidth <= 320` in the page; it must return `true`.
  - **Compare:** check the captures against `mockups/a-shop-front.html` at the same widths.
- [ ] **Step 2: Run the detector once:**

  ```
  impeccable detect --json works/happy-haus-toys/index.html works/happy-haus-toys/style.css
  ```

  - Fix the mechanical findings.
  - `cream-palette` and the awning's `repeating-stripes-gradient` are brief-pinned. Pass them to the reviewer as such; don't "fix" them.
- [ ] **Step 3: Spawn `impeccable-finish-reviewer`** with:
  - the original request, the confirmed answers (from the spec's "What the user decided") and the artifact path;
  - the screenshot paths;
  - the direction contract from `works/happy-haus-toys/.impeccable/surfaces/index-html.md`;
  - the detector findings;
  - the chosen mockup as the critique reference (code-led, no comp);
  - the craft-floor reference path.

  Act on its disposition per impeccable's new-work section 7. The budget is at most two fix rounds; if items are still open after that, put the table in front of the user.
- [ ] **Step 4: Spawn `impeccable-documenter`** with the project root `works/happy-haus-toys`, the artifact, the direction contract, PRODUCT.md and new-work's `document.md`. Verify `DESIGN.md` and `.impeccable/design.json` exist and carry tokens.
- [ ] **Step 5: Re-run `python scripts/check_site.py` and the browser tests; expect both green.**
- [ ] **Step 6: Commit** the page fixes and `DESIGN.md` with `feat: Happy Haus finish review fixes and design record`.

### Task 5: Portfolio Works card, share image, cleanup

**Files:**
- Create: `assets/works/happy-haus-toys.png` (1280×800), `works/happy-haus-toys/assets/og.jpg` (1200×630)
- Modify: `index.html` (root, Works section), `scripts/check_site.py`
- Delete: `works/happy-haus-toys/mockups/`

**Interfaces:**
- Consumes: the finished page from Task 4.

- [ ] **Step 1: Add checks.**
  - **To `check_portfolio`:**
    - `works/happy-haus-toys/` is in the hrefs, and `assets/works/happy-haus-toys.png` is in the srcs;
    - `Happy Haus Toys` is in the text, and `work-empty` is not in the html.
  - **To `check_hh_assets`:**
    - `assets/works/happy-haus-toys.png` is 1280×800;
    - `works/happy-haus-toys/assets/og.jpg` exists and is 1200×630 (read the JPEG size with Pillow);
    - `works/happy-haus-toys/mockups` does not exist.
  - Leave `GAME_MARKUP[PORTFOLIO]` unchanged: the card must not add `data-reveal`, `data-spy`, `data-type` or `data-walker`.
- [ ] **Step 2: Run the checker; expect the new failures.**
- [ ] **Step 3: Capture the screenshots.** `assets/works/happy-haus-toys.png` is the page's first screen at 1280×800. `og.jpg` is a 1200×630 crop of the first screen at 1200 wide (awning, sign and headline). Embed provenance on both (origin: screenshot of the built page).
- [ ] **Step 4: Replace `.work-empty` with the card.** Copy the commented "Build hosted on this site" template, with:
  - `href="works/happy-haus-toys/"` and URL text `hansukun / works / happy-haus-toys`;
  - meta `Kids' furniture catalog · 2026` and title `Happy Haus Toys`;
  - tags `HTML`, `CSS`, `JavaScript`;
  - `alt="Happy Haus Toys catalog, shop-front first screen"`.

  Keep the comment template above it.
- [ ] **Step 5: Delete `works/happy-haus-toys/mockups/`.** It was never committed, so a plain delete is enough.
- [ ] **Step 6: Run the checker and browser tests, and look at the root page's Works section** at 390 and 1440 wide. Expect all green, with the card in its browser frame.
- [ ] **Step 7: Commit** with `feat: list Happy Haus Toys in Works`, then stop for the user's review. Don't push or open a PR unless they ask.
