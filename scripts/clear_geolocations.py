import sqlite3
import os

DB = os.environ.get('BRUETER_DB', 'brueter.sqlite')
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute('DELETE FROM geolocation_osm')
cur.execute('DELETE FROM geolocation_google')
conn.commit()

# vacuum to reclaim space (optional)
cur.execute('VACUUM')
conn.close()
print('Cleared geolocation_osm and geolocation_google')
