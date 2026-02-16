import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.db import connect_sqlite

conn = connect_sqlite('brueter.sqlite')
cur = conn.cursor()
# gather web_ids that have geolocation in either OSM or Google
cur.execute("SELECT b.web_id, b.plz FROM gebaeudebrueter b JOIN geolocation_osm o ON b.web_id=o.web_id UNION SELECT b.web_id, b.plz FROM gebaeudebrueter b JOIN geolocation_google g ON b.web_id=g.web_id")
rows = cur.fetchall()
bad = []
for w, plz in rows:
    pd = ''.join(ch for ch in str(plz) if ch.isdigit())
    try:
        pn = int(pd) if pd else None
    except Exception:
        pn = None
    if pn is None or not (10000 <= pn <= 14199):
        bad.append((w, plz))

if bad:
    print('Found geolocated records with PLZ outside Berlin range:')
    for w, p in bad:
        print(w, p)
else:
    print('No geolocated records found outside Berlin PLZ range.')

conn.close()
