import { createEventBus } from './event-bus.js';
import { createAppState } from './state.js';
import { createMapController } from '../map/map-controller.js';
import { createLayerController } from '../map/layer-controller.js';
import { createLocationController } from '../map/location-controller.js';
import { createPopupLoader } from '../markers/popup-loader.js';
import { createMarkerFactory } from '../markers/marker-factory.js';
import { createMarkerController } from '../markers/marker-controller.js';
import { createFilterController } from '../ui/filter-controller.js';
import { createBottomSheetController } from '../ui/bottom-sheet-controller.js';
import { createNavController } from '../ui/nav-controller.js';
import { createModalController } from '../ui/modal-controller.js';
import { EVENT_NAMES } from '../shared/constants.js';
import { qs } from '../shared/dom-utils.js';

function run() {
  const eventBus = createEventBus();
  const state = createAppState(eventBus);

  const mapController = createMapController();
  const map = mapController.init('map');

  const layerController = createLayerController(map);
  layerController.init();

  const popupLoader = createPopupLoader();
  const markerFactory = createMarkerFactory({
    popupLoader,
    eventBus,
    eventNames: EVENT_NAMES,
  });
  const markerController = createMarkerController({ markerFactory, layerController });

  const filterRoot = qs('[data-role="filter-root"]');
  const filterController = createFilterController({
    root: filterRoot,
    options: markerController.getFilterOptions(),
    eventBus,
  });

  const bottomSheetController = createBottomSheetController({
    sheetElement: qs('[data-role="filter-sheet"]'),
    state,
  });

  const navController = createNavController({
    sheetElement: qs('[data-role="nav-sheet"]'),
    backdropElement: qs('[data-role="nav-backdrop"]'),
    state,
  });

  createModalController({
    modalElement: qs('[data-role="marker-modal"]'),
    contentElement: qs('[data-role="marker-modal-content"]'),
    state,
    eventBus,
  });

  const locationController = createLocationController({ map, eventBus });
  locationController.bind();

  eventBus.on(EVENT_NAMES.FILTER_APPLY, (filterState) => {
    state.patchState({ activeFilters: filterState });
    markerController.applyFilter(filterState);
    bottomSheetController.close();
  });

  eventBus.on(EVENT_NAMES.FILTER_RESET, () => {
    state.patchState({ activeFilters: { species: [], status: [] } });
    markerController.applyFilter({ species: [], status: [] });
  });

  markerController.applyFilter(state.getState().activeFilters);

  const filterBindings = filterController.bind();

  document.addEventListener('click', (event) => {
    const actionEl = event.target.closest('[data-action]');
    if (!actionEl) {
      return;
    }
    const action = actionEl.getAttribute('data-action');
    if (action === 'toggle-nav') {
      navController.open();
    }
    if (action === 'close-nav') {
      navController.close();
    }
    if (action === 'open-filter') {
      navController.close();
      bottomSheetController.open();
    }
    if (action === 'close-filter') {
      bottomSheetController.close();
    }
    if (action === 'apply-filter') {
      filterBindings.apply();
    }
    if (action === 'reset-filter') {
      filterBindings.reset();
    }
    if (action === 'close-marker-modal') {
      eventBus.emit(EVENT_NAMES.MARKER_CLOSE);
    }
    if (action === 'locate') {
      eventBus.emit(EVENT_NAMES.LOCATION_REQUEST);
    }
    if (action === 'share-map' && navigator.share) {
      navigator.share({
        title: 'Gebäudebrüter in Berlin',
        url: location.href,
      });
    }
  });
}

run();
