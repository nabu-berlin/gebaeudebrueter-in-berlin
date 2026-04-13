# Gebäudebrüter in Berlin – Live (GitHub Pages)

Dieses Repository enthält die öffentlich sichtbare Kartenanzeige.
Deployments erfolgen erst nach erfolgreicher Staging-Prüfung und immer per explizitem zweiten Befehl.

## Gesamtworkflow (Kurzüberblick)

1. Lokale Generierung im Generator-Repo.
2. Veröffentlichung in das Staging-Repo (`main` + `docs`).
3. Manuelle Kontrolle der Staging-Seite.
4. Bei Erfolg: explizites Publish in dieses Live-Repo.

## Zielsetzung dieses Repos

- Stabile, öffentliche Darstellung der aktuellen Karte.
- Keine experimentellen Zwischenschritte im Live-Stand.
- Klarer Freigabeprozess über Staging.

## Funktionen / Struktur

- `docs/GebaeudebrueterMultiMarkers.html` – aktuelle Live-Karte.
- `docs/generated/<sha>/` – versionsierte Build-Artefakte aus Staging.
- `docs/assets/` – bestehende Live-Assets; werden beim `publish-live` nicht überschrieben.

## Prozessschritte (Freigabe)

Der Live-Deploy wird aus dem Generator-Repo gestartet:

```powershell
python scripts/run_full_pipeline.py --verbose publish-live --sha <sha>
```

Der Befehl kopiert aus Staging nach Live:

- `docs/GebaeudebrueterMultiMarkers.html`
- `docs/generated/<sha>/`

Danach wird in diesem Repo automatisch ausgeführt:

- `git add .`
- `git commit -m "Deploy map <sha>"`
- `git push origin main`
- `git pull origin main`

## Handlungsanweisungen

- Live nur nach dokumentierter manueller Staging-Prüfung freigeben.
- Bei Problemen kein `publish-live` ausführen; stattdessen im Generator korrigieren und neu stagen.
