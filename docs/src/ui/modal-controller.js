import { setHidden } from '../shared/dom-utils.js';
import { EVENT_NAMES } from '../shared/constants.js';

export function createModalController({ modalElement, contentElement, state, eventBus }) {
  function open(markerData) {
    contentElement.innerHTML = [
      `<h2>${markerData.address ?? 'Standortdetails'}</h2>`,
      `<p><b>Arten:</b> ${(markerData.species || []).join(', ') || '—'}</p>`,
      `<p><b>Status:</b> ${(markerData.status || []).join(', ') || '—'}</p>`,
    ].join('');
    state.patchState({ markerModalOpen: true, selectedMarkerId: markerData.id });
    setHidden(modalElement, false);
  }

  function close() {
    state.patchState({ markerModalOpen: false, selectedMarkerId: null });
    setHidden(modalElement, true);
  }

  const unbindOpen = eventBus.on(EVENT_NAMES.MARKER_OPEN, open);
  const unbindClose = eventBus.on(EVENT_NAMES.MARKER_CLOSE, close);

  return {
    open,
    close,
    destroy() {
      unbindOpen();
      unbindClose();
    },
  };
}
