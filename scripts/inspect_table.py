#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('brueter.sqlite')
cur = conn.cursor()
for row in cur.execute("PRAGMA table_info(gebaeudebrueter)"):
    print(row)
conn.close()