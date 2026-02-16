#!/usr/bin/env python3
import sqlite3
conn=sqlite3.connect('brueter.sqlite')
cur=conn.cursor()
print('PRAGMA table_info(geolocation_osm):')
for r in cur.execute("PRAGMA table_info(geolocation_osm)"):
    print(r)
print('\nCREATE SQL:')
for r in cur.execute("SELECT sql FROM sqlite_master WHERE name='geolocation_osm'"):
    print(r[0])
conn.close()
