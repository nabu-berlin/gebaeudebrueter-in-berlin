#!/usr/bin/env python3
import sqlite3
import sys
import os

# ensure repo root on path so scripts.address_utils can be imported
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.insert(0, root)

from scripts.address_utils import sanitize_street

DB = os.path.join(root, 'brueter.sqlite')

def intval(v):
    return 1 if v else 0

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute('SELECT rowid, web_id, strasse, strasse_original FROM gebaeudebrueter')
    rows = cur.fetchall()
    total = len(rows)
    updated = 0

    for row in rows:
        rowid, web_id, strasse, strasse_original = row
        cleaned, flags, original = sanitize_street(strasse or '')

        # Prepare values
        vals = {
            'strasse_original_val': strasse_original if strasse_original else (strasse or ''),
            'has_comma': intval(flags.get('has_comma')),
            'has_slash': intval(flags.get('has_slash')),
            'has_range': intval(flags.get('has_range')),
            'multiple_numbers': intval(flags.get('multiple_numbers')),
            'multiple_streets': intval(flags.get('multiple_streets')),
            'kept_text_after_number': intval(flags.get('kept_text_after_number')),
        }

        cur.execute('''
            UPDATE gebaeudebrueter SET
                strasse_original = ?,
                has_comma = ?,
                has_slash = ?,
                has_range = ?,
                multiple_numbers = ?,
                multiple_streets = ?,
                kept_text_after_number = ?
            WHERE rowid = ?
        ''', (
            vals['strasse_original_val'],
            vals['has_comma'],
            vals['has_slash'],
            vals['has_range'],
            vals['multiple_numbers'],
            vals['multiple_streets'],
            vals['kept_text_after_number'],
            rowid
        ))
        updated += 1

    conn.commit()
    conn.close()
    print(f'Processed {total} rows; updated {updated} rows')

if __name__ == '__main__':
    main()
