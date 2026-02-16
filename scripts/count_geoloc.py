import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.db import connect_sqlite

conn=connect_sqlite('brueter.sqlite')
cur=conn.cursor()
for t in ('geolocation_osm','geolocation_google'):
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"{t}:", cur.fetchone()[0])
    except Exception as e:
        print(f"{t}: ERROR -", e)
try:
    cur.execute("SELECT COUNT(DISTINCT web_id) FROM (SELECT web_id FROM geolocation_osm UNION ALL SELECT web_id FROM geolocation_google)")
    print('distinct_web_ids_with_geoloc:', cur.fetchone()[0])
except Exception as e:
    print('distinct_web_ids_with_geoloc: ERROR -', e)
conn.close()
