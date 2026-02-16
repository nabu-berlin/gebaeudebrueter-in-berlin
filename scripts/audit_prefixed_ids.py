import sqlite3, csv
from pathlib import Path

DB = 'brueter.sqlite'
pairs_file = Path('reports/prefixed_variants.txt')
out_csv = Path('reports/prefixed_audit.csv')

pairs = []
for line in pairs_file.read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if '->' in line:
        left,right = [p.strip() for p in line.split('->',1)]
        try:
            pairs.append((int(left), int(right)))
        except:
            pass

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
results = []
for pref, base in pairs:
    r = {'prefixed': pref, 'base': base}
    # existence in gebaeudebrueter
    cur.execute('SELECT COUNT(*) as c FROM gebaeudebrueter WHERE web_id=?', (pref,))
    r['pref_exists'] = cur.fetchone()['c'] > 0
    cur.execute('SELECT COUNT(*) as c FROM gebaeudebrueter WHERE web_id=?', (base,))
    r['base_exists'] = cur.fetchone()['c'] > 0
    # fetch sample data if exists
    if r['pref_exists']:
        cur.execute('SELECT web_id, plz, ort, strasse, beschreibung FROM gebaeudebrueter WHERE web_id=?', (pref,))
        row = cur.fetchone()
        r['pref_plz'] = row['plz']
        r['pref_strasse'] = row['strasse']
    else:
        r['pref_plz'] = r['pref_strasse'] = None
    if r['base_exists']:
        cur.execute('SELECT web_id, plz, ort, strasse, beschreibung FROM gebaeudebrueter WHERE web_id=?', (base,))
        row = cur.fetchone()
        r['base_plz'] = row['plz']
        r['base_strasse'] = row['strasse']
    else:
        r['base_plz'] = r['base_strasse'] = None
    # geolocation counts
    cur.execute('SELECT COUNT(*) as c FROM geolocation_osm WHERE web_id=?', (pref,))
    r['pref_osm_geo'] = cur.fetchone()['c']
    cur.execute('SELECT COUNT(*) as c FROM geolocation_google WHERE web_id=?', (pref,))
    r['pref_google_geo'] = cur.fetchone()['c']
    cur.execute('SELECT COUNT(*) as c FROM geolocation_osm WHERE web_id=?', (base,))
    r['base_osm_geo'] = cur.fetchone()['c']
    cur.execute('SELECT COUNT(*) as c FROM geolocation_google WHERE web_id=?', (base,))
    r['base_google_geo'] = cur.fetchone()['c']
    results.append(r)

conn.close()

# write CSV
fields = ['prefixed','base','pref_exists','base_exists','pref_plz','pref_strasse','base_plz','base_strasse','pref_osm_geo','pref_google_geo','base_osm_geo','base_google_geo']
with out_csv.open('w', encoding='utf-8', newline='') as fh:
    writer = csv.DictWriter(fh, fieldnames=fields)
    writer.writeheader()
    for r in results:
        writer.writerow(r)

# print summary
both = [r for r in results if r['pref_exists'] and r['base_exists']]
only_pref = [r for r in results if r['pref_exists'] and not r['base_exists']]
only_base = [r for r in results if not r['pref_exists'] and r['base_exists']]
none = [r for r in results if not r['pref_exists'] and not r['base_exists']]
print('Pairs total:', len(results))
print('Both exist:', len(both))
print('Only prefixed exists:', len(only_pref))
print('Only base exists:', len(only_base))
print('Neither exists:', len(none))
print('Wrote audit to', out_csv)
