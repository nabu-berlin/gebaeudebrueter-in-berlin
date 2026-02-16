# Gebäudebrüter Berlin – Datenpipeline und Karten

Dieses Repository enthält die komplette Pipeline für Gebäudebrüter-Daten in Berlin:

- Scraping der Meldungen
- Datenbereinigung und Qualitätssicherung
- Geokodierung (OSM, optional Google)
- Generierung der interaktiven Karte
- Veröffentlichung über `docs/` (GitHub Pages)

Stand: MultiMarkers ist die aktive Kartenvariante.

Kurzfassung für den operativen Alltag: `README_SHORT.md`

## Inhaltsverzeichnis

- [1. Schnellstart](#1-schnellstart)
  - [Voraussetzungen](#voraussetzungen)
  - [Installation](#installation)
  - [Erste Karte erzeugen](#erste-karte-erzeugen)
- [2. Architektur](#2-architektur)
  - [Datenquellen und Verarbeitung](#datenquellen-und-verarbeitung)
  - [Verzeichnisüberblick (relevant)](#verzeichnisüberblick-relevant)
  - [Aktive Karte](#aktive-karte)
- [3. Typischer Workflow](#3-typischer-workflow)
  - [A) Vollpipeline (empfohlen)](#a-vollpipeline-empfohlen)
  - [B) Einzelne Schritte (manuell)](#b-einzelne-schritte-manuell)
- [4. Zentrale Skripte](#4-zentrale-skripte)
- [5. Karte generieren und publizieren](#5-karte-generieren-und-publizieren)
  - [Lokale Generierung](#lokale-generierung)
  - [Nach `docs/` übernehmen](#nach-docs-übernehmen)
  - [Lokaler Test](#lokaler-test)
  - [GitHub Pages](#github-pages)
- [6. Datenqualität und Reports](#6-datenqualität-und-reports)
- [7. Konfiguration](#7-konfiguration)
- [8. Troubleshooting](#8-troubleshooting)
  - [Filter-UI funktioniert lokal, aber nicht auf Pages](#filter-ui-funktioniert-lokal-aber-nicht-auf-pages)
  - [Marker fehlen](#marker-fehlen)
  - [Geocoding liefert wenig Treffer](#geocoding-liefert-wenig-treffer)
- [9. Entwicklungshinweise](#9-entwicklungshinweise)
- [10. Lizenz](#10-lizenz)

## 1. Schnellstart

### Voraussetzungen

- Python 3.10+ (empfohlen)
- SQLite-Datenbank `brueter.sqlite` im Projektroot
- Optional: `api.key` für Google-Geocoding

### Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Erste Karte erzeugen

```powershell
python scripts/generateMultiSpeciesMap.py
```

Ausgabe: `GebaeudebrueterMultiMarkers.html`

## 2. Architektur

### Datenquellen und Verarbeitung

1. Scraper liest Meldungen von der Quellseite.
2. Bereinigung normalisiert Texte/Adressen und setzt Flags.
3. Geokodierung ergänzt Koordinaten.
4. Renderer erzeugt HTML-Karte mit Filter-UI, Clustering und Popups.

### Verzeichnisüberblick (relevant)

- `scripts/` – Pipeline-Skripte und Utilities
- `src/gb/` – modulare Logik (DB, Map-Transform, Rendering)
- `docs/` – veröffentlichte Website-Artefakte (Pages)
- `reports/` – QA- und Pipeline-Reports (CSV/TXT)

### Aktive Karte

- Aktiv: `GebaeudebrueterMultiMarkers.html`
- Legacy-Karten wurden entfernt (Single-Species/Meldungen getrennt)

## 3. Typischer Workflow

### A) Vollpipeline (empfohlen)

```powershell
python scripts/run_full_pipeline.py
```

Optional mit Geocoding + Übernahme:

```powershell
python scripts/run_full_pipeline.py --geocode --apply-results --batch-size 50
```

Die Pipeline führt (wenn vorhanden) u. a. aus:

- `nabuPageScraper.py`
- `data_cleansing.py`
- `prepare_missing_coords.py`
- `filter_missing_by_species.py`
- `run_geocode_batch.py` (Batch-Erstellung)
- `geocode_missing.py` (optional)
- `apply_geocode_results.py` (optional)
- `convert_date_format.py`
- `generateMultiSpeciesMap.py`

Zusammenfassung: `reports/pipeline_summary.txt`

### B) Einzelne Schritte (manuell)

```powershell
python scripts/nabuPageScraper.py
python scripts/data_cleansing.py
python scripts/generateLocationForPageMap.py
python scripts/generateMultiSpeciesMap.py
```

## 4. Zentrale Skripte

- `scripts/generateMultiSpeciesMap.py`
  - erzeugt die aktive Karte
  - nutzt modulare Map-Logik aus `src/gb/maps/*`
  - enthält Konfiguration für Feedback- und Melde-E-Mails

- `scripts/run_full_pipeline.py`
  - orchestriert End-to-End-Lauf
  - optionales Geocoding über Batch-Mechanik
  - schreibt Laufbericht nach `reports/pipeline_summary.txt`

- `scripts/ci_publish_maps.py`
  - CI-orientiertes Generieren + Konsistenzprüfung
  - prüft geolokalisierte IDs gegen HTML
  - kopiert Ergebnis nach `docs/`

## 5. Karte generieren und publizieren

### Lokale Generierung

```powershell
python scripts/generateMultiSpeciesMap.py
```

### Nach `docs/` übernehmen

```powershell
Copy-Item -Path "GebaeudebrueterMultiMarkers.html" -Destination "docs/GebaeudebrueterMultiMarkers.html" -Force
```

### Lokaler Test

```powershell
python -m http.server 8000
```

Dann im Browser öffnen:

- `http://localhost:8000/GebaeudebrueterMultiMarkers.html`
- `http://localhost:8000/docs/GebaeudebrueterMultiMarkers.html`

### GitHub Pages

- Veröffentlichung erfolgt aus `docs/`.
- `docs/index.html` kann als Weiterleitung auf die gewünschte Karten-URL dienen.

## 6. Datenqualität und Reports

Wichtige QA-Dateien in `reports/`:

- `all_data_with_flags.csv`
- `geolocated_all.csv`
- `missing_coords*.csv`
- `manual_review_missing_coords.csv`
- `bad_coords.csv`
- `marker_validation_report.csv`
- `pipeline_summary.txt`

Empfohlene Prüfungen:

```powershell
python scripts/check_db_state.py
python scripts/check_latlon.py
python scripts/check_marker_presence.py
```

## 7. Konfiguration

Konfiguration der Kartenerzeugung liegt in `scripts/generateMultiSpeciesMap.py` im `CONFIG`-Block.

Wichtige Keys:

- `DB_PATH`
- `OUTPUT_HTML`
- `NABU_BASE_URL`
- `FEEDBACK_EMAIL_RECIPIENT`
- `REPORT_EMAIL_TO`
- `REPORT_EMAIL_CC`
- `ONLINE_FORM_URL`

Hinweis E-Mail-Links:

- „Feedback“ verwendet `FEEDBACK_EMAIL_RECIPIENT`.
- „Beobachtung melden“ verwendet `REPORT_EMAIL_TO` plus `REPORT_EMAIL_CC`.

## 8. Troubleshooting

### Filter-UI funktioniert lokal, aber nicht auf Pages

- Asset-Pfade prüfen (`docs/assets/...` vs. `assets/...`).
- Browser-Cache leeren oder Query-Parameter-Version erhöhen.
- Prüfen, ob `docs/assets/js/map-controls.js` und `docs/assets/css/map-controls.css` geladen werden.

### Marker fehlen

- Sind Koordinaten in DB vorhanden?
- Sind Datensätze durch Flags ausgeschlossen (`is_test`, `noSpecies`, `dataExcluded`)?
- QA-Skripte und Reports prüfen.

### Geocoding liefert wenig Treffer

- Adressqualität und PLZ prüfen.
- Batches über `prepare_missing_coords.py` / `run_geocode_batch.py` neu aufsetzen.
- Optional Google-Key (`api.key`) validieren.

## 9. Entwicklungshinweise

- Neue Business-Logik nach Möglichkeit in `src/gb/...` implementieren.
- Skripte in `scripts/` als thin wrapper halten.
- Große generierte Artefakte sparsam committen; für Veröffentlichung primär `docs/` aktualisieren.

## 10. Lizenz

Siehe `LICENSE`.

Bei externen Datenquellen und APIs (z. B. Geocoding) bitte Nutzungsbedingungen und Lizenzbedingungen separat prüfen.
