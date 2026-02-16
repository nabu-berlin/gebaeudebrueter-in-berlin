import os, sqlite3, csv, shutil, datetime
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.config import BACKUPS_DIR

ROOT = os.path.dirname(os.path.dirname(__file__))
DB = os.path.join(ROOT, 'brueter.sqlite')
BACKUP_DIR = str(BACKUPS_DIR)

def backup_db():
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(BACKUP_DIR, exist_ok=True)
    dest = os.path.join(BACKUP_DIR, f'brueter.sqlite.restorebak.{ts}')
    shutil.copy2(DB, dest)
    print('DB backup written to', dest)

def restore_csv_to_table(csvfile, table):
    print('Restoring', csvfile, '->', table)
    path = os.path.join(BACKUP_DIR, csvfile)
    if not os.path.exists(path):
        print('  backup not found:', path); return 0
    rows = []
    with open(path, 'r', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            # CSV has headers: id,web_id,longitude,latitude,location,complete_response
            web_id = int(r.get('web_id') or 0)
            # ensure numeric lat/lon
            lon = r.get('longitude')
            lat = r.get('latitude')
            location = r.get('location')
            complete_response = r.get('complete_response')
            # skip entries without both lat and lon to satisfy NOT NULL constraints
            if lat in (None, '', 'None') or lon in (None, '', 'None'):
                continue
            try:
                latf = float(lat)
                lonf = float(lon)
            except Exception:
                continue
            rows.append((web_id, latf, lonf, location, complete_response))
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    # delete old rows
    cur.execute(f'DELETE FROM {table}')
    # insert
    cur.executemany(f'INSERT INTO {table} (web_id, latitude, longitude, location, complete_response) VALUES (?, ?, ?, ?, ?)', rows)
    conn.commit()
    cur.execute(f'SELECT COUNT(*) as c FROM {table}')
    c = cur.fetchone()[0]
    conn.close()
    print(f'  inserted {len(rows)} rows, table now has {c}')
    return c

if __name__ == '__main__':
    backup_db()
    counts = {}
    counts['osm'] = restore_csv_to_table('geolocation_osm_backup.csv', 'geolocation_osm')
    counts['google'] = restore_csv_to_table('geolocation_google_backup.csv', 'geolocation_google')
    print('Done. Restored counts:', counts)
