import sqlite3
ids = [76,402,535,739,1328,1460,1623,2208]
db='brueter.sqlite'
conn=sqlite3.connect(db)
cur=conn.cursor()
for t in ('geolocation_osm','geolocation_google'):
    cur.execute(f"DELETE FROM {t} WHERE web_id IN ({','.join(['?']*len(ids))})", ids)
    print(f"Deleted from {t}:", cur.rowcount)
conn.commit()
conn.close()
