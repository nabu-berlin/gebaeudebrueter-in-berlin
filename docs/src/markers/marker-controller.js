export function createMarkerController({ markerFactory, layerController }) {
  const allMarkerData = [
    {
      id: 'demo-1',
      position: [52.52, 13.405],
      species: ['Sperling'],
      status: ['Kontrolle'],
      address: 'Musterstraße 1, Berlin',
    },
    {
      id: 'demo-2',
      position: [52.5, 13.37],
      species: ['Mauersegler'],
      status: ['Sanierung'],
      address: 'Musterstraße 2, Berlin',
    },
  ];

  function applyFilter(filterState) {
    const filtered = allMarkerData.filter((item) => {
      const speciesOk = filterState.species.length === 0 || item.species.some((sp) => filterState.species.includes(sp));
      const statusOk = filterState.status.length === 0 || item.status.some((st) => filterState.status.includes(st));
      return speciesOk && statusOk;
    });

    const leafletMarkers = filtered.map(markerFactory.makeMarker);
    layerController.replaceMarkers(leafletMarkers);
  }

  return {
    applyFilter,
    getFilterOptions: () => ({
      species: ['Sperling', 'Mauersegler'],
      status: ['Kontrolle', 'Sanierung'],
    }),
  };
}
