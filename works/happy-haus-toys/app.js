// Happy Haus Toys: open a bin, pick a color, and copy an order note on the way to the Instagram DM.
// Every product is already in the HTML; without this file the details simply stay open.
(() => {
  const HANDLE = '@happyhaustoys';
  const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  const peso = (n) => '₱' + Number(n).toLocaleString('en-US');

  function orderNote(name, color, price) {
    if (!name) return "Hi Happy Haus! I'd like to ask about your toys.";
    return `Hi Happy Haus! I'd like to order the ${name}${color ? ` in ${color}` : ''} (${peso(price)}). Is it available?`;
  }

  let toastEl = null;
  let toastTimer;
  // parts: strings, or { b: text } for bold runs; built as nodes so product names are never parsed as HTML
  function toast(parts) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'toast';
      toastEl.setAttribute('role', 'status');
      document.body.append(toastEl);
    }
    toastEl.replaceChildren(...parts.map((p) => {
      if (typeof p === 'string') return p;
      const b = document.createElement('b');
      b.textContent = p.b;
      return b;
    }));
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove('show'), 4200);
  }

  function setColor(bin, i) {
    const swatch = bin.querySelector(`[data-swatch="${i}"]`);
    if (!swatch) return;
    const color = swatch.dataset.color;
    bin.querySelectorAll('[data-swatch]').forEach((b) => b.setAttribute('aria-pressed', String(b === swatch)));
    const img = bin.querySelector('img[data-photo]');
    if (img) {
      img.src = swatch.dataset.src;
      img.alt = `${bin.dataset.name} in ${color}`;
    }
    bin.querySelectorAll('[data-color-label]').forEach((el) => { el.textContent = color; });
    bin.querySelectorAll('[data-order]').forEach((a) => { a.dataset.color = color; });
  }

  function closeBin(bin, opts = {}) {
    bin.classList.remove('open');
    bin.querySelector('.bin-detail').hidden = true;
    const face = bin.querySelector('.bin-face');
    face.setAttribute('aria-expanded', 'false');
    if (opts.focus) face.focus();
  }

  function openBin(bin) {
    document.querySelectorAll('.bin.open').forEach((b) => { if (b !== bin) closeBin(b); });
    bin.classList.add('open');
    bin.querySelector('.bin-detail').hidden = false;
    bin.querySelector('.bin-face').setAttribute('aria-expanded', 'true');
    requestAnimationFrame(() => bin.scrollIntoView({ behavior: reducedMotion() ? 'auto' : 'smooth', block: 'start' }));
  }

  function copyOrder(link) {
    const bin = link.closest('.bin');
    const name = bin && bin.dataset.name;
    const color = link.dataset.color;
    const note = orderNote(name, color, bin && bin.dataset.price);
    const failed = () => toast(name
      ? ['Tell us in the chat: ', { b: `${name} – ${color}` }]
      : ['Say hi to ', { b: HANDLE }, ' in the chat.']);
    // started inside the click, before the browser follows the link to Instagram; the link itself is never cancelled
    if (!navigator.clipboard || !navigator.clipboard.writeText) return failed();
    navigator.clipboard.writeText(note).then(
      () => toast(['Order note copied. Paste it in the chat with ', { b: HANDLE }, '.']),
      failed,
    );
  }

  function init(root = document) {
    root.querySelectorAll('.bin-detail').forEach((d) => { d.hidden = true; });
    root.querySelectorAll('.bin-face').forEach((f) => f.setAttribute('aria-expanded', 'false'));

    root.addEventListener('click', (e) => {
      const order = e.target.closest('[data-order]');
      if (order) return copyOrder(order);
      const bin = e.target.closest('.bin');
      if (!bin) return;
      const swatch = e.target.closest('[data-swatch]');
      if (swatch) return setColor(bin, Number(swatch.dataset.swatch));
      if (e.target.closest('.bin-close')) return closeBin(bin, { focus: true });
      if (e.target.closest('.bin-face')) return bin.classList.contains('open') ? closeBin(bin) : openBin(bin);
    });

    document.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape') return;
      const open = root.querySelector('.bin.open');
      if (open) closeBin(open, { focus: true });
    });
  }

  window.HappyHaus = { peso, orderNote, setColor, openBin, closeBin, init };

  if (window.HAPPY_HAUS_NO_AUTOINIT !== true) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => init());
    else init();
  }
})();
