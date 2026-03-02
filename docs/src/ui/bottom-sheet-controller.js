import { setHidden } from '../shared/dom-utils.js';

export function createBottomSheetController({ sheetElement, state }) {
  function open() {
    state.patchState({ filterSheetOpen: true });
    setHidden(sheetElement, false);
  }

  function close() {
    state.patchState({ filterSheetOpen: false });
    setHidden(sheetElement, true);
  }

  return {
    open,
    close,
  };
}
