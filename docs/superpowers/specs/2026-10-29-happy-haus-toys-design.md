# Happy Haus Toys catalog: design

Date: 2026-10-29
Status: draft, awaiting approval
Product record: `works/happy-haus-toys/PRODUCT.md` (catalog, prices, brand, what must not be invented)
Approved mockup: `works/happy-haus-toys/mockups/a-shop-front.html` (layout A, "Shop front"), chosen over B (taped feed) and C (growth chart)

## Intent

Happy Haus Toys is a small shop that sells on-hand kids' furniture (playhouses, slide sets, bookshelves, toy storage) through its Instagram account, @happyhaustoys. This is a standalone catalog site for it. It lives inside the hansukun portfolio repo and is listed in the portfolio's Works section, but it is the shop's real site: the shop has agreed to it (confirmed by the user). Real parents will use it and real orders will arrive in the shop's DMs.

The visitor is a parent who tapped through from Instagram on a phone. They want to see every piece, its colors, its size, what comes with it and its price, then message the shop to order. Success: a parent gets from the link to "Message to order" with the product and color already decided, and the page feels like the shop's Instagram rather than a generic store.

## Goals

- One page that shows all 7 products from the shop's Instagram, grouped onto three shelves: **Climb & slide** (Forest House slide set, Forest Nest slide set), **Read & store** (Rotating Tree bookshelf, Whale 2-in-1, Bubble 2-in-1), **Play pretend** (Shop play storage, Serene Playhouse).
- For each product: real photos, every color option, size, what's included, price in pesos, and the five shared features (easy installation, rounded corners, stable support, odor-free HDPE, safe and durable). PRODUCT.md is the source of truth for names, colors, sizes, includes and prices, and the page copies it word for word (the order note uses those exact names). It was reconciled with the mockup on 2026-10-29.
- Each product also gets a one-line description. *My call: these are written by me from the captions and photos, not supplied by the shop; the user should check them.* They describe, they don't claim:
  - Forest House slide set: "Two slides side by side, with a basketball hoop in the middle."
  - Forest Nest slide set: "One slide plus a climbing frame to scramble up."
  - Rotating Tree bookshelf: "A Christmas tree of books that turns all the way round."
  - Whale 2-in-1: "Covers forward on top, toys in the bins below."
  - Bubble 2-in-1: "Books face out on two shelves, toys go in four bins below."
  - Shop play storage: "A little shop front that tidies the toys away."
  - Serene Playhouse: "A whole house with a curtained door and a side counter."
- One ordering path: **Message to order** copies a ready-made note naming the product, color and price, then opens the Instagram DM (`https://ig.me/m/happyhaustoys`). Instagram links can't pre-fill a message, which is why the note is copied.
- The same playful look as the shop's Instagram posts (the user asked for this explicitly).
- A Works card on the portfolio home page that opens the site.

## Non-goals

- No cart, checkout, payment, accounts or stock levels.
- No delivery areas, fees, payment methods or warranty: these are undecided and must not appear.
- No reviews, testimonials, customer counts or other invented proof.
- No CMS or admin. Product data lives in the page source.

## Anti-goals (would be a failure even if it works)

- Looking like a generic e-commerce template (headline + button + a row of equal cards).
- The shop metaphor tipping into a game: it must stay a catalog a parent can scan in seconds.
- Any spec that exists only inside a photo. Every size, color and price is real text.
- Sharing any visual DNA with the dark portfolio around it. This site has its own identity.

## Constraints

- Static HTML, CSS and JS with no build step (user's choice), served by GitHub Pages from `works/happy-haus-toys/`. The page must work when opened at `/works/happy-haus-toys/` with relative asset paths.
- Mobile-first. Design at 375–390px wide, then scale up to desktop.
- Fonts from Google Fonts, the same way the portfolio and Settled pages already load theirs (Baloo 2 for display, Nunito for body, Patrick Hand only for the "Holiday edition" cloud). *My call: matches the repo; `scripts/check_site.py` already allows those hosts.*
- Accessible: AA contrast, keyboard reachable, visible focus, color never the only signal (each swatch shows its name), `prefers-reduced-motion` respected.
- Public and indexable: no `noindex` (the mockups carry one; the real page must not). It gets a real title, description and Open Graph/Twitter tags with a preview image, because parents will share the link.

## What the user decided

- Who it's for: parents browsing from Instagram on a phone.
- Next step: Message to order via Instagram DM.
- Photos: download from the shop's Instagram (done), cropped as the first version.
- Products: all 7 from Instagram, not just the 4 in the screenshots.
- Prices: shown.
- Feel: the same playful look as the Instagram posts.
- Stack: plain HTML/CSS/JS.
- Layout: mockup A, "Shop front".
- Status: a real client site the shop agreed to, listed under "Client work".

## The design (layout A, as in the approved mockup)

The page is the little toy shop itself, borrowed from the shop's own "Shop play storage" piece.

**World (shared tokens, already in `mockups/world.css`):** navy ink `#164a90` / `#0e3363` for type; tape yellow `#fbe07a`; cream `#fdf6e6` and peach `#fbe2cc` grounds; logo accents coral `#ee6f45`, sun `#f5b52e`, leaf `#7fa47a`, sky `#4a86c5`, cocoa `#8b5e3c`; holiday red `#a5121c`. Components:
- **Washi-tape labels** with bitten ends for section names, product titles and color names.
- **Speckled kraft-paper note** that specs are written on.
- **Scalloped cream badge** the logo always sits on. The logo art is only clean on cream, so it is never placed on another color.
- **Sun-yellow price sticker** and the **red dashed "Holiday edition" cloud** used on the Rotating Tree.

**First screen (mobile):** an ink top edge, then a full-width yellow-and-cream striped awning with a scalloped hem. Below it, the logo badge hangs from two strings as the shop sign and swings once into place on load: the one signature motion. Then the headline "On-hand playhouses, slides & shelves for your little ones." and one line: "Pick a piece off the shelf, choose its color, and message us on Instagram to order." The header area alone carries the sprinkle confetti; the shelves sit on plain cream so the photos stay clear. A "Found the one? We reply on Instagram. [Message us]" counter bar stays pinned to the bottom of the screen the whole time.

**Shelves:** each category gets a tape label, then a grid of **bins**: 2 columns on phones, 3 from 720px, 4 from 1060px. Each bin holds:
- the product photo in a cream bin with a rounded lip, sitting on a wooden plank that joins up with its neighbors to read as one shelf;
- a paper price tag hanging off the plank on a string, with the product name, the price on a yellow highlighter stroke, and small color dots.

**Opening a product:** tapping a bin opens it in place across the full row (no modal). On phones the details stack under the photo; from 720px they sit beside it. The details show:
- a one-line description;
- color swatches with names, which swap the photo;
- the kraft note with size and an "Includes" list;
- **Message to order**, plus "Back to the shelf", which closes the bin and returns focus to it.

Only one bin is open at a time, and opening one scrolls it into view.

**Lower page:** a peach "Every piece is" band with the five shared features as small icons drawn in one stroke style, then a footer with the badge, "Happy Haus Toys · On-hand items, ordered by message" and a link to the Instagram profile.

**Message to order:** copies `Hi Happy Haus! I'd like to order the {product} in {color} ({price}). Is it available?` and opens the DM in a new tab. A toast confirms "Order note copied. Paste it in the chat with @happyhaustoys." If copying fails, the toast names the product and color instead. The pinned "Message us" button opens the DM with a general note.

## Assets

- Photos are already downloaded and cropped into `works/happy-haus-toys/assets/products/*.webp` (11 files, one per product color).
- The 28 original Instagram images (1536×1920, named `<post id>_<slide>.jpg`), their captions (`captions.json`), the crop script (`crops.py`, run from that folder) and the mockup generator are in `works/happy-haus-toys/.impeccable/source/`. That folder is git-ignored and never ships.
- Source post for each shipped image (all slide 1 of `https://www.instagram.com/happyhaustoys/p/<id>/`):

  | Image | Post |
  |---|---|
  | tree-white | De05qQQEi2z |
  | tree-green | De05sxuEqCW |
  | forest-house-beige | De05SmAkpin |
  | forest-house-green | De05KsWEtDz |
  | forest-nest-beige | De0e8zYEq6J |
  | forest-nest-green | De0fHyTElXr |
  | shop-grey | De04-ltkqmY |
  | shop-beige | De047OGkp_K |
  | whale | De042ngEgbD |
  | bubble | De0ekwAkqoO |
  | serene | De0dvSqkohY |
  | logo-art.png | De042ngEgbD (logo badge, top center) |
- Logo artwork is in `works/happy-haus-toys/assets/logo-art.png` (transparent, meant for the cream badge only).
- **Known fixes for the real build:**
  - The Serene Playhouse crop has a visible seam where a color label was patched; redo that patch or pick another crop of the same photo.
  - Recheck every crop at full size for leftover label fragments.
- Each shipped image needs its origin recorded (source: the @happyhaustoys Instagram post it came from). Use impeccable's `embed-prompt` provenance for rasters.
- A 1280×800 screenshot of the finished site goes in `assets/works/happy-haus-toys.png` for the Works card.

## Portfolio integration

In the root `index.html` Works section, replace the `.work-empty` placeholder with an "On this site" card. Copy the commented template already in that section. It links to `works/happy-haus-toys/`; the URL bar shows `hansukun / works / happy-haus-toys`; the meta line is "Kids' furniture catalog · 2026"; the title is "Happy Haus Toys"; tags are HTML, CSS and JavaScript. *My call: a single project isn't marked `--featured`.*

## Housekeeping

- *My call:* the shipped site is `works/happy-haus-toys/index.html` with its CSS and JS beside it. The three mockups, `mockups/` and its generator are throwaway and get deleted when the real page lands. PRODUCT.md stays in the folder.
- *My call:* extend `scripts/check_site.py` to cover the new page: title mentions "Happy Haus", links and assets resolve, and only allowed external hosts are used (add `ig.me` and `www.instagram.com`).
- impeccable's process continues on the build: direction contract in the surface brief, the finish review, then DESIGN.md recorded from the built site.

## Left to the builder

- File split (one `index.html` with inline or adjacent CSS/JS), and whether product markup is hand-written or rendered from a data block, as long as the first screen and the shelves are in the HTML without waiting on JS.
- Exact spacing, breakpoints within the stated ranges, and motion timing, within the approved mockup.
- The exact meta copy and how the social preview image is made (a crop of the first screen is fine).
- Whether the pinned counter bar hides while a product is open.
