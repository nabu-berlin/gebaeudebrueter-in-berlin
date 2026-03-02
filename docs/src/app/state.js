import { DEFAULT_FILTER_STATE } from '../shared/constants.js';

export function createAppState(eventBus) {
  let state = {
    isMobile: window.matchMedia('(max-width: 600px)').matches,
    activeFilters: structuredClone(DEFAULT_FILTER_STATE),
    navOpen: false,
    filterSheetOpen: false,
    markerModalOpen: false,
    selectedMarkerId: null,
  };

  function getState() {
    return state;
  }

  function patchState(partial) {
    state = { ...state, ...partial };
    eventBus.emit('state:changed', state);
  }

  return {
    getState,
    patchState,
  };
}
