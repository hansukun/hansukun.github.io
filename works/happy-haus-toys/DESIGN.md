---
name: Happy Haus Toys
description: A little toy shop front for on-hand kids' furniture, ordered by Instagram message.
colors:
  ink: "#164a90"
  ink-deep: "#0e3363"
  ink-soft: "#33598f"
  cream: "#fdf6e6"
  badge-cream: "#fffaf0"
  kraft: "#f3e6d0"
  tape-yellow: "#fbe07a"
  sun: "#f5b52e"
  coral: "#ee6f45"
  cocoa: "#8b5e3c"
  holiday-red: "#a5121c"
typography:
  display:
    fontFamily: "\"Baloo 2\", \"Nunito\", system-ui, sans-serif"
    fontSize: "clamp(34px, 8.8vw, 66px)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "\"Baloo 2\", \"Nunito\", system-ui, sans-serif"
    fontSize: "27px"
    fontWeight: 800
    lineHeight: 1.05
  title:
    fontFamily: "\"Baloo 2\", \"Nunito\", system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 700
    lineHeight: 1.3
  tag:
    fontFamily: "\"Baloo 2\", \"Nunito\", system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 800
    lineHeight: 1.1
  body:
    fontFamily: "\"Nunito\", system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 500
    lineHeight: 1.55
  label:
    fontFamily: "\"Baloo 2\", \"Nunito\", system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 800
  hand:
    fontFamily: "\"Patrick Hand\", \"Nunito\", cursive"
    fontSize: "15px"
    fontWeight: 400
    letterSpacing: "0.06em"
rounded:
  note: "4px"
  tag: "8px 8px 14px 14px"
  toast: "16px"
  photo: "20px 20px 30px 30px"
  pill: "999px"
spacing:
  xs: "8px"
  sm: "10px"
  md: "14px"
  lg: "22px"
  shelf: "48px"
  section: "64px"
components:
  button-order:
    backgroundColor: "{colors.ink}"
    textColor: "#ffffff"
    typography: "{typography.headline}"
    rounded: "{rounded.pill}"
    padding: "0 26px"
    height: "54px"
  button-order-hover:
    backgroundColor: "{colors.ink-deep}"
  button-order-sun:
    backgroundColor: "{colors.sun}"
    textColor: "{colors.ink-deep}"
    rounded: "{rounded.pill}"
    height: "46px"
    padding: "0 18px"
  button-close:
    backgroundColor: "{colors.badge-cream}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0 20px"
    height: "54px"
  swatch:
    backgroundColor: "{colors.badge-cream}"
    textColor: "{colors.ink-deep}"
    rounded: "{rounded.pill}"
    padding: "6px 14px 6px 6px"
    height: "40px"
  swatch-selected:
    backgroundColor: "{colors.tape-yellow}"
    textColor: "{colors.ink-deep}"
  tape-label:
    backgroundColor: "{colors.tape-yellow}"
    textColor: "{colors.ink}"
    typography: "{typography.headline}"
    padding: "0.18em 0.7em 0.1em"
  price-sticker:
    backgroundColor: "{colors.sun}"
    textColor: "{colors.ink-deep}"
    rounded: "50%"
    width: "4.6em"
  kraft-note:
    backgroundColor: "{colors.kraft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.note}"
    padding: "18px"
  hang-tag:
    backgroundColor: "{colors.badge-cream}"
    textColor: "{colors.ink}"
    typography: "{typography.tag}"
    rounded: "{rounded.tag}"
    padding: "16px 12px 10px"
  counter-bar:
    backgroundColor: "{colors.ink}"
    textColor: "#ffffff"
    rounded: "{rounded.pill}"
    padding: "8px 8px 8px 20px"
  toast:
    backgroundColor: "{colors.ink-deep}"
    textColor: "#ffffff"
    rounded: "{rounded.toast}"
    padding: "14px 18px"
---

# Design System: Happy Haus Toys

## Overview

**Creative North Star: "The Little Toy Shop Front"**

The page is the shop itself, built from the craft materials of the shop's Instagram graphics: a yellow and cream striped awning with a scalloped hem, the logo hanging on its scalloped cream badge from two cocoa strings, sprinkle confetti on warm cream, and products standing in bins on wooden shelf planks with paper tags hanging below. Everything is stuck on, pinned or hung; very little is a flat panel.

Navy rounded type carries all the talking. Yellow is the material of labels (washi tape, price stickers, the selected swatch), and the photos carry the product. Small tilts (between -4 and 8 degrees) make each label look placed by hand. Density is low: one or two big moves per viewport, with generous gaps between shelves.

Motion is a single, soft overshoot curve: the sign swings once into place, the open bin's details rise in, photos lift a few pixels on hover. All of it collapses under reduced motion.

**Key Characteristics:**
- Warm cream ground with sparse multicolor sprinkles; the header carries the denser sprinkle field.
- Navy (ink) for every word; yellow for every sticker and label; coral only for focus and small icons.
- Craft objects as components: washi tape, kraft note, price sticker, hang tag, scalloped badge, shelf plank.
- Pills for every interactive control; soft navy-tinted lift shadows for anything that sits on the page.
- Hand-placed tilt on stuck-on objects, never on text blocks or controls.

## Colors

A warm, toy-box palette: deep navy ink on cream paper, with sun and tape yellows as the label material.

### Primary
- **Shop Navy** (ink): all headings, tag names, link color, the order button, the pinned counter bar, the ink strip above the awning.
- **Night Navy** (ink-deep): body text, order-button hover, the toast, text on yellow.
- **Faded Navy** (ink-soft): spec terms on the kraft note, swatch hover border, scrollbar thumb.

### Secondary
- **Washi Yellow** (tape-yellow): the tape labels (shelf titles, section headings, the open bin's color name), the selected swatch fill, text selection, bold text in the toast. Applied at 92% so the tape reads a touch see-through.
- **Sun Yellow** (sun): price stickers, awning stripes, the counter's Message us button.

### Tertiary
- **Crayon Coral** (coral): focus outline and the feature icons on the "Every piece is" note. Nothing else.
- **Twine Cocoa** (cocoa): the sign strings and hang-tag strings; tints the shelf plank shadow.
- **Holiday Red** (holiday-red): the Holiday edition cloud only, a brand badge carried from the shop's posts.

### Neutral
- **Shop Cream** (cream): page ground under the sprinkles.
- **Badge Cream** (badge-cream): the logo badge, photo frames, hang tags, swatches and the secondary pill. One step lighter than the ground so cut-outs lift off it.
- **Kraft Paper** (kraft): speckled kraft notes that carry specs and shared features.

### Named Rules
**The Yellow Is Material Rule.** Yellow appears as a physical thing (tape, sticker, stripe, selected chip), never as a text color on a light ground or as a large flat panel (the one yellow text is the bolded handle inside the navy toast).

**The Ink Speaks Rule.** Every readable word is a navy, or white on navy. Accent colors never set running text.

## Typography

**Display Font:** Baloo 2 (with Nunito, system-ui)
**Body Font:** Nunito (with system-ui)
**Hand Font:** Patrick Hand (with Nunito, cursive), for the Holiday edition cloud only

**Character:** Baloo 2 at 700 to 800 is the rounded, bubbly voice of the shop's post graphics; Nunito at 500 to 800 keeps body copy equally soft but quiet.

### Hierarchy
- **Display** (800, clamp(34px, 8.8vw, 66px), 0.95): the one headline in the shop front, max 14ch, balanced, tight -0.02em tracking.
- **Headline** (800, 27px, 1.05): shelf titles, always set on washi tape. The order button uses the same face at 19px.
- **Title** (700, 22px, 1.3): the one-line description at the top of an open bin.
- **Tag** (800, 17px, 1.1): product names on hang tags, balanced.
- **Body** (Nunito 500, 16px, 1.55): base copy; the intro line runs 17px at 700, max 34ch. Spec values run 700 with tabular figures.
- **Label** (Baloo 2 800, 14px): spec terms on the kraft note (in Faded Navy), counter-bar lines in Nunito 800 14px.

### Named Rules
**The Heavy Weights Rule.** Nothing on the page is set lighter than 500; headings and labels sit at 700 to 800, matching the chunky post graphics.

**The Tabular Price Rule.** Prices and dimensions use tabular figures so peso amounts and millimetres line up.

## Layout

Mobile-first and centered. The shop front (ink strip 14px, awning 96px, a 172px hanging sign, the headline) stacks centered; the store below is capped at 1180px with 16px side padding.

Shelves stack with 48px between them; each starts with its centered tape title. Bins flow in a wrapping flex row that centers short shelves: 2 columns with a 14px gap on phones, 3 columns with a 22px gap from 720px, 4 from 1060px; row gaps 30px rising to 36px. An open bin takes the full row; from 720px it splits into photo and details (1 : 1.15 columns, 34px gap).

The shared-features note sits 64px below the last shelf. A navy counter bar is pinned 12px from the bottom (max 560px wide), so the footer reserves 128px of bottom padding. Spacing steps observed: 8, 10, 14, 16, 22, 30 to 36, 48, 64px.

## Elevation & Depth

Depth is physical and soft: things sit on the cream like paper and plastic on a table. Shadows are navy-tinted (never grey), negatively spread so they pool under the object, and wood-toned under the shelf plank. No hard offset shadows, no glows.

### Shadow Vocabulary
- **Lift** (`box-shadow: 0 10px 24px -12px rgb(14 51 99 / .35), 0 2px 6px -2px rgb(14 51 99 / .18)`): bin photos, price stickers, the shared-features note.
- **Badge float** (`filter: drop-shadow(0 6px 10px rgb(14 51 99 / .18))`): the scalloped logo badge.
- **Hang tag** (`box-shadow: 0 6px 14px -8px rgb(14 51 99 / .4)`): paper tags under the shelf.
- **Plank** (`box-shadow: 0 9px 12px -8px rgb(139 94 60 / .65)`): the wooden shelf edge under each bin.
- **Pinned** (`box-shadow: 0 16px 30px -14px rgb(14 51 99 / .7)`): counter bar; the toast uses `0 16px 30px -12px` at .6.
- **Button** (`box-shadow: 0 10px 20px -10px rgb(14 51 99 / .6)`): order button; the sun variant tints it cocoa at .55.

### Named Rules
**The Tinted Shadow Rule.** Shadows take the color of what casts them: navy for objects, cocoa for wood. Never neutral black.

## Shapes

Rounded and toy-like. Every control is a full pill (999px). Photos sit in a 6px badge-cream frame with a bin silhouette (20px top corners, 30px bottom). Hang tags are 8px on top and 14px below. Kraft notes are almost square (4px) so they read as cut paper. Price stickers are circles. The logo always sits on a scalloped twelve-lobe badge; the awning hem scallops in 46px arcs; tape labels have bitten ends from a repeated radial mask.

Stuck-on objects are tilted by hand: tape -1.5 or 1.2 degrees, stickers 8, the holiday cloud -4, tags alternating -2 and 2, the features note -0.4.

## Components

### Buttons
Chunky, friendly and unmistakable; there is one action.
- **Shape:** full pill (999px), 54px tall, 26px side padding, a 22px stroke icon before the label.
- **Primary (Message to order):** Shop Navy fill, white Baloo 2 800 at 19px, Button shadow.
- **Hover / Focus:** fills Night Navy and lifts 1px over 0.2s on the shared ease; focus is the global 3px coral outline at 3px offset.
- **Sun variant (Message us):** Sun Yellow fill with Night Navy text, cocoa-tinted shadow, darker sun on hover; used inside the navy counter bar at 46px tall.
- **Secondary (Back to the shelf):** Badge Cream pill with a 2px navy border at 25%, Shop Navy 800 text; border goes full navy on hover.

### Chips (swatches)
- **Style:** Badge Cream pill, 40px tall, 2px navy border at 18%, a 26px color dot followed by the color name in 700 14px. Color is never shown alone.
- **State:** selected (aria-pressed) fills Washi Yellow with a full navy border; hover darkens the border to Faded Navy.

### Cards / Containers
- **Bin:** the product card is a framed photo (4:5) standing on a wooden plank, a price sticker pinned top right, with a paper hang tag on a cocoa string below carrying the name and color dots. The whole bin is one button; hover lifts the photo 5px over 0.35s.
- **Kraft note:** speckled kraft paper (4px radius, 18px padding) holding a two-column spec list (5.6em term column).
- **Background:** Badge Cream frames and tags on Shop Cream; Kraft Paper for notes.

### Navigation
None. The page is one shop front; shelves are the only structure and the pinned counter bar is the only persistent chrome.

### Washi Tape Label (signature)
Inline Baloo 2 800 on Washi Yellow at 92%, bitten ends from a radial mask, tilted -1.5 degrees (variants 1.2 and 0). Used for shelf titles, section headings, and the open bin's color name on its photo.

### Price Sticker (signature)
A Sun Yellow circle (min 4.6em) with Night Navy 800 tabular figures, tilted 8 degrees with Lift shadow, pinned to the photo's top right corner.

### Hanging Sign and Awning (signature)
Sun and pale-cream stripes 46px wide, a scalloped hem, and the logo badge hung on two cocoa strings that swings once into place (1.8s, settling from -10 degrees).

### Counter Bar and Toast
A pinned navy pill bar with a two-line prompt and the sun order button. Copying an order note raises a Night Navy toast (16px radius) above it, with the handle bolded in Washi Yellow.

## Do's and Don'ts

### Do:
- **Do** put the logo only on its scalloped Badge Cream badge.
- **Do** set every label that names a group or a color on washi tape, and every price on a Sun Yellow sticker.
- **Do** show color as a dot plus its name; never color alone.
- **Do** use the single ease `cubic-bezier(.16, 1, .3, 1)` for all motion, and let reduced motion collapse it.
- **Do** keep controls as full pills at least 40px tall (54px for the order action).
- **Do** tint shadows navy (or cocoa under wood) with negative spread.

### Don't:
- **Don't** set running text in yellow, coral or red; words are navy, or white on navy.
- **Don't** tilt paragraphs, buttons or swatches; tilt belongs to stuck-on objects (tape, stickers, tags, notes).
- **Don't** use hard offset shadows, grey shadows or glows.
- **Don't** add a second kind of action; every path ends in Message to order.
- **Don't** use square corners on controls or frames; only the kraft note is near-square.
