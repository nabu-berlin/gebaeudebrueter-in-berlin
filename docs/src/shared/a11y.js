export function trapEscape(element, onEscape) {
  if (!element) {
    return () => {};
  }
  const keyHandler = (event) => {
    if (event.key === 'Escape') {
      onEscape();
    }
  };
  element.addEventListener('keydown', keyHandler);
  return () => element.removeEventListener('keydown', keyHandler);
}
