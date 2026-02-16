import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.db import connect_sqlite

conn = connect_sqlite(row_factory=True)
cur=conn.cursor()
res={}
cur.execute('SELECT COUNT(*) as c FROM geolocation_osm')
res['geolocation_osm']=cur.fetchone()['c']
cur.execute('SELECT COUNT(*) as c FROM geolocation_google')
res['geolocation_google']=cur.fetchone()['c']
cur.execute('SELECT COUNT(*) as c FROM gebaeudebrueter')
res['geb_count']=cur.fetchone()['c']
# flags
for col in ('noSpecies','is_test'):
    try:
        cur.execute(f'SELECT COUNT(*) as c FROM gebaeudebrueter WHERE {col}=1')
        res[col]=cur.fetchone()['c']
    except Exception:
        res[col]=None
# distinct geolocated web_ids
cur.execute("SELECT COUNT(DISTINCT web_id) as c FROM (SELECT web_id FROM geolocation_osm UNION ALL SELECT web_id FROM geolocation_google)")
res['distinct_geolocated_webids']=cur.fetchone()['c']
# how many rows would generator include (not test, not noSpecies) and have geolocation
cur.execute("SELECT COUNT(DISTINCT b.web_id) as c FROM gebaeudebrueter b LEFT JOIN geolocation_osm o ON b.web_id=o.web_id LEFT JOIN geolocation_google g ON b.web_id=g.web_id WHERE (b.is_test IS NULL OR b.is_test=0) AND (b.noSpecies IS NULL OR b.noSpecies=0) AND ((g.latitude IS NOT NULL AND g.longitude IS NOT NULL) OR (o.latitude IS NOT NULL AND o.longitude IS NOT NULL))")
res['generator_visible_with_geo']=cur.fetchone()['c']
# sample lists
cur.execute("SELECT web_id FROM geolocation_osm LIMIT 10")
res['osm_sample']=[r['web_id'] for r in cur.fetchall()]
cur.execute("SELECT web_id FROM geolocation_google LIMIT 10")
res['google_sample']=[r['web_id'] for r in cur.fetchall()]
cur.execute("SELECT web_id FROM gebaeudebrueter WHERE (is_test IS NULL OR is_test=0) AND (noSpecies IS NULL OR noSpecies=0) AND web_id NOT IN (SELECT web_id FROM geolocation_osm UNION SELECT web_id FROM geolocation_google) LIMIT 10")
res['missing_geo_sample']=[r['web_id'] for r in cur.fetchall()]
print(json.dumps(res, indent=2))
conn.close()
