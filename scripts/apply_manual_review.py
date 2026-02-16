#!/usr/bin/env python3
import os, csv, re, sqlite3
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MISSING = os.path.join(root, 'reports', 'manual_review_missing_coords.csv')
DB = os.path.join(root, 'brueter.sqlite')

text = open(MISSING, encoding='utf-8', errors='replace').read()
# gather web_ids from original missing_coords_cleaned.csv to be safe
miss_file = os.path.join(root, 'reports', 'missing_coords_cleaned.csv')
web_ids = []
with open(miss_file, encoding='utf-8') as fh:
    r = csv.DictReader(fh)
    for row in r:
        try:
            web_ids.append(int(row['web_id']))
        except Exception:
            pass

latlon_re = re.compile(r'(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)')
found = {}
for wid in web_ids:
    s = str(wid)
    pos = text.find(s)
    if pos == -1:
        # try with quotes
        pos = text.find('"'+s)
    if pos == -1:
        continue
    # search for latlon after pos within next 400 chars
    m = latlon_re.search(text, pos, pos+800)
    if m:
        lat = float(m.group(1))
        lon = float(m.group(2))
        found[wid] = (lat, lon)

if not found:
    print('No manual lat/lon found in', MISSING)
    raise SystemExit(0)

conn = sqlite3.connect(DB)
cur = conn.cursor()
inserted = 0
skipped = 0
for wid,(lat,lon) in found.items():
    # check if geolocation_osm already has this web_id
    cur.execute('SELECT web_id, latitude, longitude FROM geolocation_osm WHERE web_id = ?', (wid,))
    r = cur.fetchone()
    if r:
        skipped += 1
        continue
    # get a location string (strasse or address) from gebaeudebrueter
    cur.execute('SELECT strasse, plz, ort FROM gebaeudebrueter WHERE web_id = ?', (wid,))
    row = cur.fetchone()
    if row:
        loc = ', '.join([str(x) for x in row if x])
    else:
        loc = 'manual'
    complete = 'manual_review_applied'
    cur.execute('INSERT INTO geolocation_osm (web_id, longitude, latitude, location, complete_response) VALUES (?,?,?,?,?)', (wid, lon, lat, loc, complete))
    inserted += 1

conn.commit()
conn.close()
print('Inserted', inserted, 'skipped(existing):', skipped)
print('Applied manual coords for web_ids:', list(found.keys()))
