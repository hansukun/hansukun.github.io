/* Game accents for hansukun.github.io.
   Design: docs/superpowers/specs/2026-09-25-jrpg-accents-design.md
   Opt-in per element: [data-type] typewriter, [data-reveal] reveal-on-view,
   [data-spy] nav scroll-spy, [data-walker] sprite pause. Visuals live in each page's CSS. */
(() => {
  "use strict";
  document.documentElement.classList.add("js");

  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const hasIO = "IntersectionObserver" in window;
  const SR_ONLY = "position:absolute;width:1px;height:1px;margin:-1px;padding:0;" +
    "overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0";

  // Types a box's text one character at a time. Screen readers get an untouched copy;
  // the typed copy is aria-hidden and keeps its layout because hidden characters still
  // take up space.
  function typewriter(box, reduced, charMs, startDelay) {
    if (reduced) {
      box.classList.add("is-done");
      return { finish() {} };
    }
    const full = document.createElement("span");
    full.style.cssText = SR_ONLY;
    while (box.firstChild) full.appendChild(box.firstChild);
    const shown = full.cloneNode(true);
    shown.removeAttribute("style");
    shown.setAttribute("aria-hidden", "true");

    const textNodes = [];
    const walk = document.createTreeWalker(shown, NodeFilter.SHOW_TEXT);
    while (walk.nextNode()) textNodes.push(walk.currentNode);
    const chars = [];
    for (const node of textNodes) {
      const frag = document.createDocumentFragment();
      for (const ch of node.nodeValue) {
        const span = document.createElement("span");
        span.textContent = ch;
        span.style.visibility = "hidden";
        chars.push(span);
        frag.appendChild(span);
      }
      node.replaceWith(frag);
    }
    box.append(full, shown);
    box.tabIndex = 0;

    let next = 0;
    let timer = 0;
    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      chars.forEach((c) => { c.style.visibility = ""; });
      box.classList.add("is-done");
      box.removeAttribute("tabindex");
    };
    const tick = () => {
      if (next >= chars.length) return finish();
      chars[next++].style.visibility = "";
      timer = setTimeout(tick, charMs);
    };
    box.addEventListener("click", finish);
    box.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        finish();
      }
    });
    timer = setTimeout(tick, startDelay);
    return { finish };
  }

  // Adds .is-in to each element the first time it is at least 20% in view.
  function reveal(els, reduced) {
    if (reduced || !hasIO) {
      els.forEach((el) => el.classList.add("is-in"));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }
      }
    }, { threshold: 0.2 });
    els.forEach((el) => io.observe(el));
  }

  // Marks the nav link whose section crosses the middle of the viewport.
  function spy(links) {
    const bySection = new Map();
    for (const a of links) {
      const id = (a.getAttribute("href") || "").split("#")[1];
      const section = id && document.getElementById(id);
      if (section) bySection.set(section, a);
    }
    if (!bySection.size || !hasIO) return;
    const inBand = new Set();
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) inBand.add(e.target);
        else inBand.delete(e.target);
      }
      let current = null;
      bySection.forEach((a, section) => {
        if (!current && inBand.has(section)) current = section;
      });
      bySection.forEach((a, section) => {
        if (section === current) a.setAttribute("aria-current", "true");
        else a.removeAttribute("aria-current");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    bySection.forEach((a, section) => io.observe(section));
  }

  // Pauses a walking sprite while it is off-screen; holds it still under reduced motion.
  function walker(el, reduced) {
    if (reduced) el.classList.add("is-still");
    if (!hasIO) return;
    new IntersectionObserver((entries) => {
      for (const e of entries) el.classList.toggle("is-paused", !e.isIntersecting);
    }).observe(el);
  }

  function start(options) {
    const opts = options || {};
    const root = opts.root || document;
    const followSystem = opts.reduced === undefined;
    const reduced = followSystem ? motion.matches : opts.reduced;
    const charMs = "charMs" in opts ? opts.charMs : 30;
    const startDelay = "startDelay" in opts ? opts.startDelay : 400;
    const all = (sel) => Array.from(root.querySelectorAll(sel));

    const typers = all("[data-type]").map((box) => typewriter(box, reduced, charMs, startDelay));
    const reveals = all("[data-reveal]");
    reveal(reveals, reduced);
    spy(all("[data-spy]"));
    const walkers = all("[data-walker]");
    walkers.forEach((el) => walker(el, reduced));

    if (followSystem) {
      motion.addEventListener("change", () => {
        if (motion.matches) {
          typers.forEach((t) => t.finish());
          reveals.forEach((el) => el.classList.add("is-in"));
          walkers.forEach((el) => el.classList.add("is-still"));
        } else {
          walkers.forEach((el) => el.classList.remove("is-still"));
        }
      });
    }
  }

  window.hansGame = { start };
  if (!window.hansGameManual) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", () => start());
    else start();
  }
})();
