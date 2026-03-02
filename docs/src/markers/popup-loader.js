export function createPopupLoader() {
  function renderPopupHtml(markerData) {
    const species = markerData.species?.join(', ') || '—';
    const status = markerData.status?.join(', ') || '—';
    const address = markerData.address || '—';
    return [
      '<div class="popup-card">',
      `<b>Arten</b><br>${species}<br><br>`,
      `<b>Status</b><br>${status}<br><br>`,
      `<b>Adresse</b><br>${address}`,
      '</div>',
    ].join('');
  }

  return {
    renderPopupHtml,
  };
}
