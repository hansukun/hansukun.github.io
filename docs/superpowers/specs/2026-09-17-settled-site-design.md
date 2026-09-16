# Settled brochure site — design

**Date:** 2026-09-17
**Status:** approved in brainstorming, awaiting spec review

## Goal

A one-page, dark-theme brochure site that advertises **Settled**, the Android app in
`hansukun/settled` (local checkout: `C:\Hans\Projects\Android\Budget Checklist`). The
app is not yet on Google Play; the site says "coming soon" and is ready to flip to a real
listing link. The site also hosts the privacy policy the Play Console requires before ads
can be served.

Hosted on GitHub Pages as plain static files. No build step, no framework, no JS
dependencies.

## Non-goals

- No email capture, analytics, or third-party scripts other than Google Fonts.
- No iOS mention; the app is Android-only.
- No Play listing copy beyond what the page needs.

## Files

```
E:\Hans\Projects\Web App Dev Page\
├── index.html                 brochure, inline CSS
├── privacy.html               privacy policy, same theme
├── .nojekyll                  GitHub Pages serves files as-is
├── assets/
│   ├── icon.svg               copied from app repo assets/brand/icon.svg
│   ├── icon-512.png           copied from app repo assets/brand/play-icon-512.png
│   ├── google-play-badge.svg  greyed "coming soon" badge
│   └── screens/               month, month-settled, template, history, settings
│                              as .webp (+ .png fallback), ~720px wide, cropped
└── docs/superpowers/specs/2026-09-17-settled-site-design.md
```

## `index.html` sections, top to bottom

1. **Nav** — icon + "Settled" wordmark; links: Features, Pricing, Privacy.
2. **Hero** — H1 "Your monthly bills, settled." Sub-line: "An offline checklist for the
   expenses you pay every month — the spreadsheet you already keep, as an app." Greyed
   Google Play badge with the caption "Coming soon to Google Play". Phone frame showing
   `screens/month` with a soft green glow behind it.
3. **How it works** — three numbered steps: set up your template once; tick things off as
   you pay; it rolls into next month.
4. **Features** — six cards:
   - Pools and totals — group items the way your sheet does; each pool has its own total
     and lights up when everything in it is paid.
   - Due-date reminders — a day per item; overdue items say so; paying one cancels its
     reminder.
   - Month history and trend — every month is kept; a chart shows what you paid over time.
   - A template that never rewrites history — edits reach this month and later ones;
     earlier months read exactly as they did.
   - No account, no sync, no cloud — everything lives in a database on the phone.
   - Backups you control — to Google Drive or a file, plus CSV export.
5. **Screens** — four phone frames in a horizontal strip with one-line captions:
   settled month, template editor, history, settings.
6. **Pricing** — two cards. *Free*: the whole app, one small banner and an occasional
   native ad row. *Ad-free*: monthly subscription with a 7-day free trial, price "set on
   Google Play". No paywall copy beyond that.
7. **Footer** — "Built by Hans", privacy link, contact `mailto:` (placeholder until the
   user supplies an address), copyright year.

## Visual system

- Colors: background `#0a0a0a`, card `#141414`, border `#262626`, text `#f5f5f5`, muted
  `#a3a3a3`, accent `#22c55e` (the app's paid green), overdue `#ef4444` used once as a
  demo chip. Defined as tokens on `:root`. The page is dark-only; `body` has an explicit
  background.
- Type: Inter for prose (Google Fonts), JetBrains Mono for amounts, labels and step
  numbers. Section eyebrows are uppercase, letter-spaced, mono — echoing the app's pool
  headers.
- Phone frame: a CSS-only rounded rectangle (`border-radius` 36px, 8px dark bezel) around
  the screenshot. Frames scale with `clamp()` between 220px and 320px wide.
- Layout: max content width 1080px; 16px side gutters; single column below 720px; no
  horizontal scroll at 375px.
- Motion: optional CSS-only fade-up on scroll (`animation-timeline: view()` with a
  no-motion fallback). Disabled under `prefers-reduced-motion`.

## Screenshot pipeline (throwaway, lives in the scratchpad)

1. `adb shell am start -n com.hansukun.settled/.MainActivity`.
2. For each screen: navigate by `adb shell input tap` on the tab bar / Settings rows,
   wait, `adb exec-out screencap -p > raw/<name>.png`.
3. Review each raw capture by eye. Retake if a toast, keyboard, or dialog is in the way.
4. Pillow crops: drop the status bar (top ≈ 120 px at 1240×2772), drop everything from
   the ad banner down on the Month screens (keep the tab bar out entirely; the phone frame
   implies it), and drop the system nav bar on the others. Resize to 720 px wide. Write
   `.webp` (quality 85) and `.png`.
5. The Month capture used in the hero should show a partially paid month with at least
   one "Overdue · due Nth" line and one "Due Nth" line, so the reminder feature is visible.

The raw captures show a "Test Ad" banner because the installed build is a debug build;
the crop removes it. Nothing on the site shows an ad.

## `privacy.html`

Same tokens and nav as the brochure. Sections:

- Summary — data stays on the phone; no account; no analytics.
- What the app stores — template, months, items, paid state, reminders, in SQLite on the
  device; deleted when the app is uninstalled.
- Advertising — Google AdMob in the free tier; AdMob may use the advertising ID; link to
  Google's ad policy and the device-level opt-out; the ad-free subscription removes ads.
- Google account and Drive — optional sign-in for backup; scope
  `https://www.googleapis.com/auth/drive.appdata` only; backups are visible only to the
  app; revoke from Google account settings.
- Purchases — handled by Google Play Billing; the app never sees payment details.
- Notifications — scheduled locally on the device.
- Children — not directed at children under 13.
- Changes and contact — effective date, contact address (placeholder).

Marked as a draft for the user's review; the page itself carries no "draft" banner.

## Verification

- Load `index.html` and `privacy.html` in the built-in browser at desktop width and at
  375×812. Confirm no horizontal scroll, all images load, in-page anchors and the privacy
  link resolve, the badge is visibly disabled.
- Check contrast of muted text against the card background is ≥ 4.5:1.
- Confirm the repo has `.nojekyll` and relative asset paths (Pages may serve from a
  subpath).

## Later, not now

- Swap the badge for the real Play listing URL once published.
- Feature graphic (1024×500) for the Play listing could reuse the hero art.
