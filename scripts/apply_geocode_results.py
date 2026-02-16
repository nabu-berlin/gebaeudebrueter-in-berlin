import csv
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.config import REPORTS_DIR
from gb.common.db import connect_sqlite

DB = os.environ.get('BRUETER_DB', 'brueter.sqlite')
IN_CSV = REPORTS_DIR / 'geocode_missing_results.csv'

def is_blank(v):
    return v is None or str(v).strip() == ''

def main():
    if not os.path.exists(IN_CSV):
        print('Input CSV not found:', IN_CSV)
        return
    conn = connect_sqlite(DB)
    cur = conn.cursor()
    updated = 0
    with open(IN_CSV, newline='', encoding='utf-8') as fh:
        r = csv.DictReader(fh)
        for row in r:
            web_id = row.get('web_id')
            provider = row.get('provider')
            lat = row.get('lat')
            lon = row.get('lon')
            address = row.get('address')
            if provider == 'osm' and not is_blank(lat) and not is_blank(lon):
                try:
                    cur.execute(('INSERT OR REPLACE INTO geolocation_osm (web_id, longitude, latitude, location, complete_response) '
                                 'VALUES (?,?,?,?,?)'), (web_id, lon, lat, address, str(row)))
                    updated += 1
                except Exception as e:
                    print('DB write error for', web_id, e)
            elif provider == 'google' and not is_blank(lat) and not is_blank(lon):
                try:
                    cur.execute(('INSERT OR REPLACE INTO geolocation_google (web_id, longitude, latitude, location, complete_response) '
                                 'VALUES (?,?,?,?,?)'), (web_id, lon, lat, address, str(row)))
                    updated += 1
                except Exception as e:
                    print('DB write error for', web_id, e)
    conn.commit()
    conn.close()
    print(f'Wrote {updated} geolocation rows to DB from {IN_CSV}')

if __name__ == '__main__':
    main()
