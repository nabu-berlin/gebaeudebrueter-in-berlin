import { INITIAL_VIEW, TILE_ATTRIBUTION, TILE_URL } from '../shared/constants.js';

export function createMapController() {
  let map = null;

  function init(containerId = 'map') {
    map = L.map(containerId, {
      zoomControl: true,
      closePopupOnClick: false,
    }).setView(INITIAL_VIEW.center, INITIAL_VIEW.zoom);

    L.tileLayer(TILE_URL, {
      attribution: TILE_ATTRIBUTION,
      maxZoom: 20,
    }).addTo(map);

    return map;
  }

  function getMap() {
    return map;
  }

  return {
    init,
    getMap,
  };
}
