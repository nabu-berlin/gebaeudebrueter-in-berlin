import sqlite3
import csv
import os
import sys
import importlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

common_config = importlib.import_module('gb.common.config')
common_db = importlib.import_module('gb.common.db')
common_io = importlib.import_module('gb.common.io')

REPORTS_DIR = common_config.REPORTS_DIR
connect_sqlite = common_db.connect_sqlite
ensure_parent_dir = common_io.ensure_parent_dir

DB = os.environ.get('BRUETER_DB', 'brueter.sqlite')
OUT_CSV = REPORTS_DIR / 'geolocated_all.csv'

conn = connect_sqlite(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Columns to extract from gebaeudebrueter
gb_cols = ['web_id','bezirk','plz','ort','strasse','anhang','beschreibung',
           'mauersegler','kontrolle','sperling','ersatz','schwalbe','wichtig',
           'star','sanierung','fledermaus','verloren','andere']

# header for output
out_fields = ['web_id','provider','latitude','longitude','location','complete_response'] + gb_cols[1:]

rows = []

# query OSM
cur.execute('SELECT g.web_id, g.latitude, g.longitude, g.location, g.complete_response, b.* '
            'FROM geolocation_osm g JOIN gebaeudebrueter b ON b.web_id = g.web_id')
for r in cur.fetchall():
    row = {
        'web_id': r['web_id'],
        'provider': 'osm',
        'latitude': r['latitude'],
        'longitude': r['longitude'],
        'location': r['location'],
        'complete_response': r['complete_response']
    }
    for col in gb_cols[1:]:
        row[col] = r[col]
    rows.append(row)

# query Google
cur.execute('SELECT g.web_id, g.latitude, g.longitude, g.location, g.complete_response, b.* '
            'FROM geolocation_google g JOIN gebaeudebrueter b ON b.web_id = g.web_id')
for r in cur.fetchall():
    row = {
        'web_id': r['web_id'],
        'provider': 'google',
        'latitude': r['latitude'],
        'longitude': r['longitude'],
        'location': r['location'],
        'complete_response': r['complete_response']
    }
    for col in gb_cols[1:]:
        row[col] = r[col]
    rows.append(row)

# write CSV
out_path = ensure_parent_dir(OUT_CSV)
with open(out_path, 'w', newline='', encoding='utf-8') as fh:
    writer = csv.DictWriter(fh, fieldnames=out_fields)
    writer.writeheader()
    for r in rows:
        out = {k: r.get(k, '') for k in out_fields}
        writer.writerow(out)

print(f'Wrote {len(rows)} rows to {out_path}')

conn.close()
