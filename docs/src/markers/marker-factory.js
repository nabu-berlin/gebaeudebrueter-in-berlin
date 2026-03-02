export function createMarkerFactory({ popupLoader, eventBus, eventNames }) {
  function makeMarker(markerData) {
    const marker = L.circleMarker(markerData.position, {
      radius: 7,
      color: '#1f6f8b',
      fillColor: '#49a6c7',
      fillOpacity: 0.9,
      weight: 1,
    });

    const popupHtml = popupLoader.renderPopupHtml(markerData);
    marker.bindPopup(popupHtml, {
      autoClose: false,
      closeOnClick: false,
      maxWidth: 320,
    });

    marker.on('click', () => {
      eventBus.emit(eventNames.MARKER_OPEN, markerData);
    });

    return marker;
  }

  return {
    makeMarker,
  };
}
