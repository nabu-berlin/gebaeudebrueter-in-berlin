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
OUT_CSV = REPORTS_DIR / 'all_data_with_flags.csv'
PREPARED_CSV = REPORTS_DIR / 'missing_coords_cleaned.csv'
NO_GEOCODE_CSV = REPORTS_DIR / 'no_geocode_marked_prepared.csv'

# load prepare-phase flags (if present)
prepare_map = {}
if os.path.exists(PREPARED_CSV):
    with open(PREPARED_CSV, newline='', encoding='utf-8') as fh:
        r = csv.DictReader(fh)
        for row in r:
            try:
                web_id = int(row.get('web_id') or 0)
            except Exception:
                continue
            prepare_map[web_id] = {
                'flags': row.get('flags',''),
                'cleaned': row.get('cleaned',''),
                'plz': row.get('plz',''),
                'strasse': row.get('address','')
            }

# load no_geocode reasons (aggregate per web_id)
no_geo = {}
if os.path.exists(NO_GEOCODE_CSV):
    with open(NO_GEOCODE_CSV, newline='', encoding='utf-8') as fh:
        r = csv.DictReader(fh)
        for row in r:
            try:
                web_id = int(row.get('web_id') or 0)
            except Exception:
                continue
            reason = row.get('reason','')
            no_geo.setdefault(web_id, set()).add(reason)

conn = connect_sqlite(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# load geolocation maps
osm_map = {}
cur.execute('SELECT web_id, latitude, longitude, location, complete_response FROM geolocation_osm')
for r in cur.fetchall():
    osm_map[r['web_id']] = r

google_map = {}
cur.execute('SELECT web_id, latitude, longitude, location, complete_response FROM geolocation_google')
for r in cur.fetchall():
    google_map[r['web_id']] = r

# fetch all gebaeudebrueter rows
cur.execute('SELECT * FROM gebaeudebrueter')
rows = cur.fetchall()

# prepare header: gebaeudebrueter columns + geoloc + prepare flags + no_geocode_reasons
gb_cols = rows[0].keys() if rows else []
geo_cols = ['osm_lat','osm_lon','osm_location','osm_complete_response',
            'google_lat','google_lon','google_location','google_complete_response']
prep_cols = ['flags','prepare_cleaned','prepare_plz','prepare_address']
extra_cols = ['no_geocode_reasons']
fieldnames = list(gb_cols) + geo_cols + prep_cols + extra_cols

out_path = ensure_parent_dir(OUT_CSV)
with open(out_path, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        web_id = r['web_id']
        out = {k: r[k] for k in gb_cols}
        osm = osm_map.get(web_id)
        if osm:
            out['osm_lat'] = osm['latitude']
            out['osm_lon'] = osm['longitude']
            out['osm_location'] = osm['location']
            out['osm_complete_response'] = osm['complete_response']
        else:
            out['osm_lat'] = out['osm_lon'] = out['osm_location'] = out['osm_complete_response'] = ''
        gg = google_map.get(web_id)
        if gg:
            out['google_lat'] = gg['latitude']
            out['google_lon'] = gg['longitude']
            out['google_location'] = gg['location']
            out['google_complete_response'] = gg['complete_response']
        else:
            out['google_lat'] = out['google_lon'] = out['google_location'] = out['google_complete_response'] = ''
        prep = prepare_map.get(web_id, {})
        out['flags'] = prep.get('flags','')
        out['prepare_cleaned'] = prep.get('cleaned','')
        out['prepare_plz'] = prep.get('plz','')
        out['prepare_address'] = prep.get('strasse','')
        reasons = no_geo.get(web_id)
        out['no_geocode_reasons'] = '|'.join(sorted(reasons)) if reasons else ''
        w.writerow(out)

conn.close()
print(f'Wrote {len(rows)} rows to {out_path}')
