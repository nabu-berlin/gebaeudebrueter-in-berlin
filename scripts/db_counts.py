import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.db import connect_sqlite

DB = 'brueter.sqlite'

def main():
    conn = connect_sqlite(DB)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    for t in tables:
        cur.execute(f"SELECT count(*) FROM '{t}'")
        print(f"{t}: {cur.fetchone()[0]}")
    conn.close()

if __name__ == '__main__':
    main()
