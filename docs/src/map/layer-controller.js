export function createLayerController(map) {
  const clusterLayer = L.markerClusterGroup({
    showCoverageOnHover: false,
  });

  function init() {
    map.addLayer(clusterLayer);
  }

  function replaceMarkers(markers) {
    clusterLayer.clearLayers();
    clusterLayer.addLayers(markers);
  }

  return {
    init,
    replaceMarkers,
    clusterLayer,
  };
}
