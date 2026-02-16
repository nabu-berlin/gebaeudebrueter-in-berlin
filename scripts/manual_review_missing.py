#!/usr/bin/env python3
import csv
import sqlite3
import os
from datetime import datetime

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(root, 'brueter.sqlite')
MISSING = os.path.join(root, 'reports', 'missing_coords_cleaned.csv')
OUT = os.path.join(root, 'reports', 'manual_review_missing_coords.csv')

web_ids = []
with open(MISSING, newline='', encoding='utf-8') as fh:
    reader = csv.DictReader(fh)
    for r in reader:
        try:
            web_ids.append(int(r['web_id']))
        except Exception:
            pass

if not web_ids:
    print('No web_ids found in', MISSING)
    raise SystemExit(0)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cols = ['web_id','species','strasse','plz','ort','address','flags','beschreibung','is_test','noSpecies']
species_cols = ['mauersegler','sperling','schwalbe','star','fledermaus','andere']

with open(OUT, 'w', newline='', encoding='utf-8') as outfh:
    writer = csv.writer(outfh)
    writer.writerow(cols)
    for wid in web_ids:
        cur.execute('SELECT web_id, strasse, plz, ort, beschreibung, is_test, noSpecies, ' + ','.join(species_cols) + ' FROM gebaeudebrueter WHERE web_id = ?', (wid,))
        row = cur.fetchone()
        address = ''
        flags = ''
        # try to find matching row in missing CSV for address/flags
        # fallback to DB fields
        # open missing CSV again to find matching row
        with open(MISSING, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for r in reader:
                try:
                    if int(r['web_id']) == wid:
                        address = r.get('address','')
                        flags = r.get('flags','')
                        break
                except Exception:
                    pass
        if row:
            # compute species string from boolean columns
            species_list = []
            for sc in species_cols:
                try:
                    if row[sc] and int(row[sc]) == 1:
                        species_list.append(sc)
                except Exception:
                    pass
            species = ';'.join(species_list)
            writer.writerow([row['web_id'], species, row['strasse'], row['plz'], row['ort'], address, flags, row['beschreibung'] or '', row['is_test'], row['noSpecies']])
        else:
            writer.writerow([wid,'','','','','',address,flags,'','',''])

conn.close()
print('Wrote', OUT)