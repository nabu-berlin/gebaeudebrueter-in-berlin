import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.db import connect_sqlite

p = os.environ.get('BRUETER_DB', 'brueter.sqlite')
try:
    c = connect_sqlite(p)
    cur = c.cursor()
    cur.execute('select count(*) from gebaeudebrueter where new=1')
    new = cur.fetchone()[0]
    cur.execute('select count(*) from geolocation_osm')
    osm = cur.fetchone()[0]
    cur.execute('select count(*) from geolocation_google')
    g = cur.fetchone()[0]
    print(f'new={new}, geolocation_osm={osm}, geolocation_google={g}')
    c.close()
except Exception as e:
    print('ERROR', e)
