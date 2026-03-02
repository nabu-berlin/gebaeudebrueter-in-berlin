export function qs(selector, root = document) {
  return root.querySelector(selector);
}

export function qsa(selector, root = document) {
  return Array.from(root.querySelectorAll(selector));
}

export function setHidden(el, hidden) {
  if (!el) {
    return;
  }
  el.setAttribute('aria-hidden', hidden ? 'true' : 'false');
  el.classList.toggle('is-open', !hidden);
}
