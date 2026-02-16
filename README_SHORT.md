# Gebäudebrüter Berlin – Kurzfassung

Kurzanleitung für den Standardbetrieb der MultiMarkers-Karte.

## 1) Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Voraussetzung: `brueter.sqlite` liegt im Projektroot.

## 2) Schnellabläufe

### Nur Karte neu bauen

```powershell
python scripts/generateMultiSpeciesMap.py
```

Ergebnis: `GebaeudebrueterMultiMarkers.html`

### Vollpipeline laufen lassen

```powershell
python scripts/run_full_pipeline.py
```

Mit Geocoding + Übernahme:

```powershell
python scripts/run_full_pipeline.py --geocode --apply-results --batch-size 50
```

## 3) Veröffentlichung

```powershell
Copy-Item -Path "GebaeudebrueterMultiMarkers.html" -Destination "docs/GebaeudebrueterMultiMarkers.html" -Force
```

Dann commit/push wie gewohnt.

## 4) Kurzer Funktionstest

```powershell
python -m http.server 8000
```

Im Browser prüfen:

- `http://localhost:8000/GebaeudebrueterMultiMarkers.html`
- `http://localhost:8000/docs/GebaeudebrueterMultiMarkers.html`

Checkliste:

- Filter öffnet/schließt (Desktop + Mobile)
- Marker sichtbar
- Popup-Links funktionieren
- „Beobachtung melden“ geht an `meldung@gebaeudebrueter-in-berlin.de` mit CC `detlefdev@gmail.com`

## 5) Nützliche Checks

```powershell
python scripts/check_db_state.py
python scripts/check_latlon.py
python scripts/check_marker_presence.py
```

## 6) Wo ist die ausführliche Doku?

Siehe `README.md`.
