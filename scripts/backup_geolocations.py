import sqlite3
import csv
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.config import BACKUPS_DIR

DB = os.environ.get('BRUETER_DB', 'brueter.sqlite')
OUT_DIR = BACKUPS_DIR
os.makedirs(OUT_DIR, exist_ok=True)
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def dump(table, out):
    cur.execute(f'SELECT * FROM {table}')
    rows = cur.fetchall()
    if not rows:
        print(f'No rows in {table}, wrote 0')
        return 0
    with open(out, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.writer(fh)
        writer.writerow(rows[0].keys())
        for r in rows:
            writer.writerow([r[k] for k in r.keys()])
    print(f'Wrote {len(rows)} rows to {out}')
    return len(rows)

n1 = dump('geolocation_osm', os.path.join(OUT_DIR, 'geolocation_osm_backup.csv'))
n2 = dump('geolocation_google', os.path.join(OUT_DIR, 'geolocation_google_backup.csv'))
conn.close()
print('Backup complete:', n1, n2)
