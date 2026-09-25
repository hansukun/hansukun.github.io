# JRPG accents — design

**Date:** 2026-09-25
**Status:** approved in brainstorming, awaiting spec review
**Builds on:** `2026-09-17-settled-site-design.md`, `2026-09-18-portfolio-home-design.md`
**Supersedes:** the "no JS" rule in both earlier specs, and the "Motion" line in each.

## Goal

Add animations and pixel-art graphics that nod to classic JRPGs (Final Fantasy, Suikoden)
without changing either site's brand. The portfolio keeps its brutalist near-black / white /
blue look; the Settled pages keep their rounded, green, Inter look. Both gain the same
family of game accents, so the two read as made by the same person.

Chosen in brainstorming (mockups in `.superpowers/brainstorm/275-1790330254/`):

- Portfolio: direction **C, "Brutalist + 16-bit accents"** — every accent, nothing borrowed
  from the other directions.
- Settled: option **A, "Same accents, Settled's own skin"**; the privacy page gets a quiet
  subset.
- A small shared script is allowed. Pixel art ships as real PNG sprite sheets, drawn from
  scratch — no art from any existing game.

## Non-goals

- No FF-style blue menu windows, Suikoden frames, starfield, command-menu nav, or locked
  `???` app slot (directions A/B, not chosen).
- No glove cursor on non-interactive elements (skill, step, feature, pricing cards; the
  disabled Play badge).
- No custom mouse cursor, sound, easter eggs, or sprite interactions.
- No colour changes to either palette; no layout changes beyond what is listed here.
- No build step, bundler, or third-party JS.

## File layout

```
assets/game/
├── hans-walk.png        64×48 sprite sheet: 4 frames × 16×24; row 0 blue, row 1 green
├── glove.png            16×11 pointer
└── game.js              shared script, loaded with defer by all three pages
scripts/make_sprites.py  pixel grids as text → writes the two PNGs (Pillow)
```

- Portfolio references `assets/game/…`; `settled/index.html` and `settled/privacy.html`
  reference `../assets/game/…`.
- `make_sprites.py` and its PNG output are both committed. Re-running it is deterministic.

## Pixel art (`scripts/make_sprites.py`)

Grids are strings, one character per pixel, `.` = transparent. The script validates every
row's width and every grid's height, and exits non-zero on a mismatch.

### Mini-Hans walk sprite

Chibi of Hans facing right: medium messy black hair with a blue sheen, no glasses, black
tee with one accent-coloured logo pixel, jeans, white sneakers, light skin.

Palette:

| Key | Colour | Use |
|-----|--------|-----|
| `O` | `#07070a` | outline |
| `H` | `#1c1d26` | hair |
| `h` | `#46527a` | hair sheen |
| `S` | `#f6d3b3` | skin |
| `s` | `#dba987` | skin shade (ear, neck) |
| `e` | `#07070a` | eye |
| `m` | `#c98b72` | mouth |
| `T` | `#24262e` | tee |
| `t` | `#4b4f60` | tee highlight |
| `L` | `#3b6cff` row 0 / `#22c55e` row 1 | tee logo pixel |
| `J` | `#2d3f6f` | jeans |
| `j` | `#1f2b4d` | jeans shade |
| `W` | `#ececf1` | sneakers |

Head (15 rows, shared by every frame):

```
......OOOOO.....
....OOHHHHHOO...
...OHHHhhHHHHO..
..OHHHhhhHHHHHO.
..OHHHHHHHHHHHHO
.OHHHHHHHHHHHHO.
.OHHHHHHHHhHHHHO
.OHHHHHHSHSSHSO.
.OHHHHSSSSSSSSO.
.OHHHHSSSSHHSSO.
..OHHssSSSSeSSO.
..OHHssSSSSeSSO.
...OHSSSSSSSmO..
....OOSSSSSOO...
.....OssSO......
```

Bodies (8 rows each):

```
stand             stepA             stepB
....OTTTTTO.....  ....OTTTTTO.....  ....OTTTTTO.....
...OTtTTTTTO....  ...OTtTTTTTO....  ...OTtTTTTTO....
...OTtTTLTTO....  ...OTtTTLTTOSO..  .OSOTtTTLTTO....
...OTtTSSTTO....  ...OTTTTTTTOO...  ..OOTtTTTTTO....
....OJJJJJO.....  ...OJJJJJJO.....  ....OJJJJJJO....
....OJJjJJO.....  ..OJJO..OJJO....  ...OJJO.OJJO....
....OWWOWWWO....  .OWWWO...OWWWO..  ..OWWWO.OWWWO...
....OOOOOOOO....  .OOOOO...OOOOO..  ..OOOOO.OOOOO...
```

- Frame = head rows 0–14 + body rows 15–22, in a 16×24 cell. Row 23 holds a ground
  shadow: x 4–11, `rgba(0,0,0,.55)`.
- Frame order: `stand`, `stepA`, `stand`, `stepB`. In the two step frames the head
  rows are drawn 1px lower (bob). Rows are painted top to bottom, so body rows overwrite
  the shifted head row where both are opaque — exactly as in the approved preview
  (`sprite-v3.html`).
- Sheet: 64×48. Row 0 uses the blue logo pixel (portfolio), row 1 the green (Settled).

### Glove cursor

Original white glove pointing right. `c` = cuff `#b8c4d6`, `k` = knuckle line `#8894a8`,
`W` = `#ffffff`, `O` = `#000000`.

```
................
.OOOOOOOOOOOOOO.
OccWWWWWWWWWWWWO
OccWWWWWWWWWWWWO
OccWWWWWWWWWWWWO
OccWWWWWOOOOOOO.
OccWkkkkO.......
OccWWWWWO.......
OccWkkkkO.......
OccWWWWWO.......
.OOOOOOO........
```

## Rendering rules (both sites)

- Pixel art is shown only at integer scales with `image-rendering: pixelated`: sprite 3×
  (48×72) from 720px up and 2× (32×48) below; glove 1.5× is not an integer, so the glove is
  shown at 1× (16×11) below 720px and 2× (32×22) from 720px up.
- The glove is a CSS `::before` background on the interactive element, positioned just
  outside its left edge, vertically centred. It is decorative and never replaces the
  browser focus outline.
- Glove bob: `translateX(0 → -4px)`, `steps(2)`, 0.7s, infinite.
- Sprite walk: `background-position` over the sheet with `steps(4)` at 0.64s per cycle
  (160ms a frame), plus a linear `translateX` across the footer container width in 12s,
  looping back in from the left edge.

## `assets/game/game.js`

Plain ES2017, no dependencies, about 4 KB, loaded `<script src="…/game.js" defer>`. It
reads `prefers-reduced-motion` once at start and listens for changes. Features are driven
by attributes, so one file serves all three pages and a page without an attribute simply
skips that feature:

1. **Typewriter — `[data-type]`.** On start, keeps the original element as a visually
   hidden copy for screen readers and inserts an `aria-hidden` typed copy. Types text
   nodes character by character (inline `<b>` elements keep their formatting) at 30ms a
   character, starting 400ms after `DOMContentLoaded`. When done, adds `.is-done`, which
   shows the blinking `▼`. Click, tap, Enter or Space on the box finishes it instantly.
   The box gets `tabindex="0"` only while typing, and loses it on completion.
2. **Reveal on view — `[data-reveal]`.** An `IntersectionObserver` (threshold 0.2) adds
   `.is-in` once per element. CSS handles what `.is-in` does (bar fill, card rise, phone
   swap). A `--stagger` custom property on siblings sets their delay.
3. **Nav scroll-spy — `nav [data-spy]`.** Observes the sections the nav links point to
   and sets `aria-current="true"` on the link for the section in view; the glove follows
   `[aria-current]`.
4. **Sprite pause — `[data-walker]`.** Adds `.is-paused` (`animation-play-state: paused`)
   while the footer is off-screen.

Under reduced motion: the typewriter is skipped (the original text stays), `.is-in` is set
on every `[data-reveal]` immediately, and the walker gets `.is-still`. Nav scroll-spy
still runs, because it is state, not motion.

Without JS: nothing is hidden. The markup holds the full text; reveals default to their
final state and animate only when `html.js` (set as the script's first line) is present.

## Portfolio (`index.html`)

- **Glove.** On nav links with `[aria-current]`, `:hover` or `:focus-visible` — from 720px
  up only; below that, the active link turns `--accent`. On `.btn` and `.app` for `:hover`
  and `:focus-visible`, alongside the existing press effect.
- **Hero dialog.** `.lead` becomes a dialog box: 2px `--text` border, `--surface`
  background, `4px 4px 0 var(--accent)` shadow, mono text, padding leaving room for the
  `▼` (blinking `--accent`, 1s `steps(1)`) in the bottom-right. `data-type` on it. Copy is
  unchanged.
- **Shine.** `h1 .block` gets `position: relative; overflow: hidden` and an `::after`
  white-to-transparent skewed band sweeping left to right every 3.5s.
- **Scanline.** A `.hero::before` band 60px tall,
  `linear-gradient(transparent, rgba(59,108,255,.06), transparent)`, translating top to
  bottom over 6s, `pointer-events: none`, behind the content.
- **EXP bars.** Each skill card gets a last row: `EXP`, a bar, `7+ YRS` (mono, 10–11px,
  `--muted`). Bar: 6px tall, 1px `--dim` border, `--accent` fill. All three are full
  (7+ years each). Cards carry `data-reveal` and `--stagger` 0 / 150 / 300ms; the fill
  animates `width 0 → 100%` over 1.2s ease-out on `.is-in`. The Android callout gets no
  bar.
- **Sprite.** A `div.walker[data-walker]` in the footer, positioned on the footer's top
  border, using sheet row 0. The contact section's bottom padding grows by the sprite
  height so the sprite never overlaps the buttons.
- **Footer copy.** "Built with plain HTML & CSS" is replaced with
  `End of status screen · Thanks for viewing` (rendered uppercase by the existing footer
  style).

## Settled (`settled/index.html`)

- **Glove.** On nav links (`Features`, `Pricing` via scroll-spy; `← Hans De Guzman`,
  `Privacy` on hover/focus) and on footer links. Not on cards or the disabled Play badge.
- **Shine.** The `em` "settled." gets a text-clipped glint: `background: linear-gradient`
  of `--accent` with a white band, `background-clip: text`, `color: transparent`, band
  position animated every 3.5s. Falls back to plain `--accent` text where `background-clip:
  text` is unsupported.
- **Hero dialog.** `.hero .lead` becomes a rounded dialog box: 12px radius, `--card`
  background, 1px `--border`, Inter text at its current size, green `▼`. `data-type` on it.
  Copy is unchanged.
- **Phone "SETTLED!" moment.** The hero phone stacks `month` and `month-settled`
  (existing webp/png pairs). The phone carries `data-reveal`; 2.5s after `.is-in`, the
  settled screenshot crossfades in over 0.6s and a `SETTLED!` badge (mono, bold, black on
  `--accent`) pops over the screen — scale 0 → 1.25 → 1, then fades after 1.5s. Plays once
  per page load. The `month-settled` image is `loading="lazy"` with `alt=""` (the
  visible `month` image keeps the descriptive alt).
- **Scanline.** Inside the phone screen only, clipped to its 28px radius:
  `rgba(34,197,94,.12)` band, 4s loop.
- **Scroll reveals.** The existing `.card, .strip figure` rise moves from
  `animation-timeline: view()` to `data-reveal` + `.is-in`, so it works in every browser.
  The `@supports (animation-timeline: view())` block is removed.
- **Sprite.** Same `.walker` on the footer's top border, using sheet row 1.

## Privacy (`settled/privacy.html`)

Quiet subset: glove on nav, in-text and footer links; sprite in the footer (row 1). No
typing, shine, scanline or reveals.

## Reduced motion

Under `prefers-reduced-motion: reduce`, in CSS and `game.js`:

- No typing, shine, scanline, reveals, crossfade or pop. Bars show full; the Settled phone
  shows `month`.
- Glove still appears on hover/focus/current, without the bob.
- Sprite stands on frame 1 near the left of the footer.

## Accessibility and performance

- Glove and sprite are CSS backgrounds or empty `aria-hidden` elements — invisible to
  screen readers. The typed copy is `aria-hidden`; the full sentence is read instead.
- No colour changes; contrast figures from the earlier specs still hold.
- PNGs under 2 KB each; `game.js` about 4 KB, `defer`, no libraries.
- Animations use `transform` / `opacity`, except the sprite's `background-position` step on
  a 48×72 box. The sprite pauses while off-screen; the scanlines are compositor-only
  transforms and keep running.

## `scripts/check_site.py`

- Replace "pages must not contain `<script>`" with: every page has exactly one `<script>`,
  its `src` resolves to `assets/game/game.js` from that page's directory, it has `defer`,
  and no page has inline script content. External script hosts stay forbidden.
- Existing link-resolution, host allowlist and colour-token checks stay. New CSS colours
  must be an existing token or `rgba()` of one.
- New: `assets/game/hans-walk.png` is 64×48 and `assets/game/glove.png` is 16×11.
- Update the module docstring to describe both sites.

## Verification

- `python scripts/make_sprites.py` then `python scripts/check_site.py` both pass.
- Serve with the `site` launch config and load `/`, `/settled/`, `/settled/privacy.html` in
  the built-in browser at desktop width and at 375×812:
  - each effect appears where this spec puts it;
  - Tab moves the glove through nav, buttons and the app card;
  - clicking the dialog skips the typing;
  - the sprite loops, and pauses when scrolled away;
  - the Settled phone swaps once, with the pop;
  - no horizontal scroll and no console errors.
- JS-off: every sentence is present in the served HTML.
- Reduced motion: review the CSS and JS branches, then ask Hans to spot-check once with
  Windows "Animation effects" off.

## Commits

1. This spec.
2. `scripts/make_sprites.py` and the generated PNGs.
3. `assets/game/game.js` and the `check_site.py` update.
4. Portfolio changes.
5. Settled and privacy changes.
6. Verification fixes.

## Later, not now

- More sprite poses (idle blink, wave) or a sprite per app.
- A hop when the sprite is clicked.
