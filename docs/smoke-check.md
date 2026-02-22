# Smoke-Checkliste: Karten-UI (Cross-Device)

Ziel: Schneller Sicht- und Funktionscheck der Karten-UI auf Mobil, Tablet und Desktop.

## Testumgebungen

- iOS Safari (aktuelles iPhone)
- Android Chrome (aktuelles Android-Gerät)
- Desktop Chrome
- Desktop Firefox
- Desktop Edge

---

## 1) Initiale Darstellung

- [ ] Seite laden (`docs/GebaeudebrueterMultiMarkers.html`)
- [ ] Karte füllt den Viewport korrekt
- [ ] Control oben rechts ist sichtbar und nicht abgeschnitten
- [ ] Keine überlappenden oder abgeschnittenen UI-Elemente

**Erwartet:** Stabile Erstansicht ohne Layout-Brüche auf allen Geräten.

---

## 2) Zoom & Gesten (Mobil)

- [ ] Pinch-Zoom testen
- [ ] Doppeltipp-Zoom testen
- [ ] Karte weiterhin normal verschiebbar/bedienbar

**Erwartet:** Browser-Zoom ist möglich, Bedienung der Karte bleibt erhalten.

---

## 3) Filter-Flow (Mobil)

- [ ] Button `Filter` öffnet Bottom-Sheet
- [ ] Arten/Status ändern
- [ ] `Filter anwenden` klicken
- [ ] Bottom-Sheet schließt sauber
- [ ] Marker-Anzeige entspricht gesetzten Filtern

**Erwartet:** Filter funktionieren konsistent, keine hängenden Overlays.

---

## 4) Rotation & dynamische Browserleisten (Mobil)

- [ ] Hochformat ↔ Querformat wechseln
- [ ] Während Scroll/Interaktion Browserleisten ein-/ausblenden
- [ ] Info-/Submit-Modal in beiden Orientierungen öffnen

**Erwartet:** Keine Safe-Area-Probleme; Modal/Sheet-Höhen bleiben korrekt und nutzbar.

---

## 5) Modal-Interaktion (alle Geräte)

- [ ] `mehr Infos` öffnen/schließen
- [ ] `Nistplatz melden` öffnen/schließen
- [ ] Schließen per `X`
- [ ] Schließen per Klick/Tap außerhalb
- [ ] Schließen per `Esc` (Desktop)

**Erwartet:** Modals sind vollständig bedienbar, Inhalt scrollt bei Bedarf.

---

## Ergebnis

- [ ] **Bestanden**
- [ ] **Nicht bestanden**

### Falls nicht bestanden

- Gerät/Browser:
- Schrittnummer:
- Beobachtung:
- Erwartetes Verhalten:
- Screenshot/Video-Link:
