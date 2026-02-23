# Gebäudebrüter in Berlin – GitHub Pages (Display)

Dieses Repository enthält nur die statischen Dateien für die Veröffentlichung der Karte über GitHub Pages.

## Inhalt

- `docs/index.html` (Weiterleitung)
- `docs/GebaeudebrueterMultiMarkers.html` (aktive Karte)
- `docs/assets/` (JS/CSS-Assets)
- `docs/images/` (Bilder)
- `docs/gb_feedback.js`
- `docs/smoke-check.md`

## Generator-Repository

Die Datenpipeline (Scraping, Bereinigung, Geocoding, Transformation, Kartengenerierung) wurde ausgelagert nach:

- `../gebauedebrueter-map-generator`

Dort werden neue Karten erzeugt und anschließend nach `docs/` dieses Repositories publiziert.

## Lokale Vorschau

```powershell
python -m http.server 8000
```

Dann öffnen:

- `http://localhost:8000/docs/`
- oder direkt `http://localhost:8000/docs/GebaeudebrueterMultiMarkers.html`
