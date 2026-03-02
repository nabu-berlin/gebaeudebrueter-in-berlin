import { EVENT_NAMES } from '../shared/constants.js';

export function createLocationController({ map, eventBus }) {
  function locate() {
    if (!navigator.geolocation) {
      return;
    }
    navigator.geolocation.getCurrentPosition((position) => {
      const { latitude, longitude } = position.coords;
      map.setView([latitude, longitude], 16);
    });
  }

  function bind() {
    return eventBus.on(EVENT_NAMES.LOCATION_REQUEST, locate);
  }

  return {
    bind,
  };
}
