#!/usr/bin/env python3
import csv, os, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.db import connect_sqlite

DB = 'brueter.sqlite'
OUT = os.path.join(os.path.dirname(__file__), 'scraped_full_export.csv')

if not os.path.exists(DB):
    print('ERROR: DB not found:', DB)
    sys.exit(2)

conn = connect_sqlite(DB)
cur = conn.cursor()
# prefer known table
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gebaeudebrueter'")
if cur.fetchone():
    table = 'gebaeudebrueter'
else:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    if not tables:
        print('ERROR: no tables found in DB')
        sys.exit(3)
    table = tables[-1]

cur.execute(f"PRAGMA table_info({table})")
cols = [r[1] for r in cur.fetchall()]
cur.execute(f"SELECT * FROM {table} ORDER BY id")
rows = cur.fetchall()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(cols)
    for r in rows:
        writer.writerow(r)

print('WROTE', OUT, 'ROWS', len(rows))
conn.close()
