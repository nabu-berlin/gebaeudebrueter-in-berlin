# Phase 3 – Datei-Skelett und Migrationspfad

Diese Phase legt ein parallel lauffähiges Modernisierungs-Skelett an, ohne die bestehende Produktionsseite zu überschreiben.

## Neu angelegte Preview-Seite

- `docs/modern.html`
  - Lädt Leaflet + MarkerCluster
  - Lädt modulare Styles aus `docs/src/styles`
  - Startet App über `docs/src/app/bootstrap.js`

## Neu angelegte Modulstruktur

- `docs/src/app`
  - `bootstrap.js`: App-Zusammenbau und Action-Routing
  - `event-bus.js`: Publish/Subscribe
  - `state.js`: zentraler Laufzeit-State
- `docs/src/map`
  - `map-controller.js`: Leaflet-Initialisierung
  - `layer-controller.js`: Cluster-Layer-Management
  - `location-controller.js`: Geolocation-Ansteuerung
- `docs/src/markers`
  - `marker-controller.js`: Marker-Filterung und Rendering
  - `marker-factory.js`: Leaflet-Marker-Erzeugung
  - `popup-loader.js`: Popup-HTML-Erzeugung
- `docs/src/ui`
  - `bottom-sheet-controller.js`
  - `filter-controller.js`
  - `modal-controller.js`
  - `nav-controller.js`
- `docs/src/shared`
  - `constants.js`, `dom-utils.js`, `a11y.js`
- `docs/src/styles`
  - `tokens.css`, `base.css`, `components.css`, `utilities.css`

## Migrationsstrategie (ab nächster Phase)

1. **Datenadapter bauen**
   - Demo-Daten aus `marker-controller.js` durch echte Marker-Daten ersetzen.
   - Ziel: Marker-Daten aus Folium-Ausgabe extrahieren und als JSON bereitstellen.

2. **Feature-Parität aufbauen**
   - Bestehende Filterlogik (Arten/Status) in neue Controller überführen.
   - Report-/Info-Flow modular nachziehen.

3. **Legacy entkoppeln**
   - jQuery-/Bootstrap-Abhängigkeiten aus Zielseite entfernen.
   - Inline-Events (`onclick` etc.) durch delegierte Event-Listener ersetzen.

4. **Switch vorbereiten**
   - Nach erfolgreichem Smoke-Test `docs/index.html` von Redirect auf neue Seite umstellen.

## Hinweise

- Das bestehende `docs/GebaeudebrueterMultiMarkers.html` bleibt unverändert.
- Die neue Struktur ist absichtlich minimal lauffähig, damit der Umbau iterativ und risikoarm erfolgen kann.
