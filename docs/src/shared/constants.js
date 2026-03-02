export const INITIAL_VIEW = {
  center: [52.5, 13.4],
  zoom: 11,
};

export const DEFAULT_FILTER_STATE = {
  species: [],
  status: [],
};

export const TILE_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

export const TILE_ATTRIBUTION = '&copy; OpenStreetMap contributors';

export const EVENT_NAMES = {
  FILTER_APPLY: 'filter:apply',
  FILTER_RESET: 'filter:reset',
  MARKER_OPEN: 'marker:open',
  MARKER_CLOSE: 'marker:close',
  LOCATION_REQUEST: 'location:request',
};
