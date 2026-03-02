import { setHidden } from '../shared/dom-utils.js';

export function createNavController({ sheetElement, backdropElement, state }) {
  function open() {
    state.patchState({ navOpen: true });
    setHidden(sheetElement, false);
    setHidden(backdropElement, false);
  }

  function close() {
    state.patchState({ navOpen: false });
    setHidden(sheetElement, true);
    setHidden(backdropElement, true);
  }

  return {
    open,
    close,
  };
}
