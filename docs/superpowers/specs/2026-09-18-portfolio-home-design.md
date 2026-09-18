# Portfolio home page — design

**Date:** 2026-09-18
**Status:** approved in brainstorming, awaiting spec review
**Builds on:** `2026-09-17-settled-site-design.md`

## Goal

Turn the root of `hansukun.github.io` into a lean personal portfolio for **Hans De Guzman,
Web Developer** — WordPress, React and Vue, with Android (React Native) apps on the side.
The existing Settled brochure moves to `/settled/` and is linked from the portfolio's Apps
section. More app cards will be added as more apps ship.

Plain static HTML with inline CSS, same as the Settled site. No build step, no JS, no
third-party scripts other than Google Fonts.

## Non-goals

- No work-history, client, or project-gallery section — the web skills are presented as
  skills only.
- No GitHub link, contact form, analytics, or light theme.
- No redirect stubs at the old `/privacy.html` or root Settled URLs; nothing has been
  submitted to Play Console or AdMob yet, so the move is clean.
- No mention of a current employer anywhere on the page.

## File layout and URLs

```
/                          hansukun.github.io
├── index.html             portfolio (new)
├── assets/
│   └── settled-icon.svg   copy of settled/assets/icon.svg, for the app card
├── settled/
│   ├── index.html         moved from /index.html
│   ├── privacy.html       moved from /privacy.html
│   └── assets/            moved from /assets (icon, badge, screens)
├── scripts/check_site.py  updated to check all three pages
├── .gitignore             new; ignores .superpowers/
└── .nojekyll
```

- Portfolio at `/`, Settled at `/settled/`, privacy policy at `/settled/privacy.html` —
  the URL to paste into Play Console later.
- The Settled pages use relative paths (`assets/…`, `privacy.html`), so the folder moves
  as a unit with `git mv` and no internal links change.

## `index.html` (portfolio) sections, top to bottom

1. **Nav** — sticky, 2px white bottom border, JetBrains Mono uppercase. Left: `hansukun`.
   Right: `Skills · Apps · Contact`, in-page anchors.
2. **Hero** — eyebrow `Remote · Web Developer`. H1 `HANS DE GUZMAN` over two lines, then
   `WEB DEV` as a blue colour-block word. Sub-line in mono: *I build sites and apps with
   WordPress, React and Vue. Recently started shipping Android apps on the side.* Buttons:
   `Get in touch →` (`mailto:devhansukun@gmail.com`) and `LinkedIn`
   (`https://www.linkedin.com/in/hansdg/`, new tab, `rel="noopener"`).
3. **01 / Skills** — heading "What I work with". Three cards:
   - **WordPress** — Custom themes and plugins, block editor, WooCommerce, performance and
     hosting. Tags: PHP · Gutenberg · ACF · WooCommerce.
   - **React** — Component-driven front ends, hooks, state, and integration with
     REST/GraphQL APIs. Tags: TypeScript · Next.js · Tailwind.
   - **Vue** — Vue 3 with the Composition API, Pinia, and Nuxt for full apps and admin UIs.
     Tags: Vue 3 · Pinia · Nuxt.

   Below the cards, a dashed callout: **Android — on the side** · *Built with React
   Native. First app in review on Google Play; more in the works.* Tags: React Native ·
   Google Play.
4. **02 / Apps** — heading "Things I've shipped". Two-column grid of app cards. Each card
   is one `<a>` wrapping: icon (44px, rounded), name, meta line, one-line description,
   `View the app page →`. First card: **Settled** · `Android · Coming soon to Google Play`
   · *An offline checklist for the bills you pay every month — the spreadsheet you already
   keep, as an app.* · links to `settled/`. Second slot: a dashed, non-link placeholder
   reading `More coming soon`. Adding an app later means copying one card block and moving
   the placeholder down.
5. **03 / Contact** — heading "Let's build something." · *Open to remote work. Email is the
   fastest way to reach me.* Buttons: `devhansukun@gmail.com` (mailto) and `LinkedIn →`.
6. **Footer** — `© 2026 Hans De Guzman` · `Built with plain HTML & CSS`.

## Visual system

Deliberately distinct from the Settled page: bold grid / brutalist, on near-black.

- **Colours**, as tokens on `:root`: bg `#0b0b0d`, grid line `#1c1c22`, surface
  `#121216`, text and borders `#f4f4f5`, muted `#a1a1aa`, dim border `#3f3f46`, accent
  `#3b6cff`. Dark-only; `color-scheme: dark`; explicit `body` background.
- **Grid paper**: two `linear-gradient`s on `body` at 28px spacing. No images.
- **Type**: Space Grotesk for headings (700 — its heaviest weight — uppercase, tracking
  −0.04em) and body (400);
  JetBrains Mono for eyebrows, labels, buttons, tags, meta lines. One Google Fonts `<link>`
  with `display=swap`.
- **Shapes**: no `border-radius` except the app icon. 2px `--text` borders on cards,
  buttons, nav bottom, section tops. Primary buttons and app cards carry an offset shadow
  `4px 4px 0 var(--accent)`; on hover/focus they translate `2px, 2px` and the shadow
  shrinks to `2px 2px 0` — a pressed effect. The Android callout and the "More coming soon"
  slot use dashed borders.
- **Layout**: max content width 960px; 16px side gutters (24px from 720px up). Skills grid
  3 → 1 column and Apps grid 2 → 1 column below 720px. H1 size
  `clamp(44px, 10vw, 88px)`. No horizontal scroll at 375px.
- **Motion**: only the hover shift; wrapped in `prefers-reduced-motion: no-preference`.
- **Contrast**: muted `#a1a1aa` on `#0b0b0d` ≈ 7.6:1; block text `#0b0b0d` on `#3b6cff`
  ≈ 4.6:1, used only at heading size.

## Changes to the Settled pages

`settled/index.html` and `settled/privacy.html` are moved, not rewritten. Two edits each:

- Nav: a first link `← Hans De Guzman` → `../`, muted, ahead of the existing links.
- Footer: "Built by Hans" becomes `Built by <a href="../">Hans De Guzman</a>`.

Titles, meta, assets and copy stay as they are.

## `scripts/check_site.py`

- `PAGES = ["index.html", "settled/index.html", "settled/privacy.html"]`.
- Relative `href`/`src` targets resolve against each page's own directory.
- Colour-token check is per page: the existing Settled token set applies to the two
  `settled/` pages; a portfolio token set (the colours above) applies to `index.html`.
- External host allowlist gains `www.linkedin.com`. Fonts hosts stay allowed. No
  `<script>` anywhere remains a hard check.

## Verification

- `python scripts/check_site.py` passes.
- Serve the repo root with a local static server and load `/`, `/settled/`,
  `/settled/privacy.html` in the built-in browser at desktop width and at 375×812: no
  horizontal scroll, fonts and images load, every nav, app-card, button and footer link
  lands where it should, and the Settled back-links return to `/`.
- Spot-check contrast of muted text and the blue colour block.

## Commits

1. `git mv` the Settled pages and assets into `settled/`, add the back-links, add
   `.gitignore`.
2. Portfolio `index.html` and `assets/settled-icon.svg`.
3. `check_site.py` update and verification fixes.

## Later, not now

- More app cards as apps ship.
- A GitHub link, if wanted.
- Swap the Settled card's "Coming soon" meta for the Play listing once published.
