import argparse
import csv
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gb.common.config import REPORTS_DIR
from gb.common.db import connect_sqlite
from gb.common.io import ensure_parent_dir
from gb.maps.multispecies import (
    STATUS_INFO,
    build_divicon_html,
    pick_primary_status,
    species_list_from_row,
)
from gb.maps.transform import build_marker_payload

HOUSE_NUMBER_RE = re.compile(r"\b\d+[a-zA-Z]?\b")


def ensure_data_excluded_column(cursor):
    cursor.execute("PRAGMA table_info(gebaeudebrueter)")
    columns = {row[1] for row in cursor.fetchall()}
    if 'dataExcluded' not in columns:
        cursor.execute("ALTER TABLE gebaeudebrueter ADD COLUMN dataExcluded INTEGER")
        return True
    return False


def fetch_rows_for_validation(cursor):
    cursor.execute("PRAGMA table_info(gebaeudebrueter)")
    gb_cols = {row[1] for row in cursor.fetchall()}

    where_parts = []
    if 'is_test' in gb_cols:
        where_parts.append("(b.is_test IS NULL OR b.is_test=0)")
    if 'noSpecies' in gb_cols:
        where_parts.append("(b.noSpecies IS NULL OR b.noSpecies=0)")
    if 'no_geocode' in gb_cols:
        where_parts.append("(b.no_geocode IS NULL OR b.no_geocode=0)")
    where_sql = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""

    query = (
        "SELECT b.web_id, b.bezirk, b.plz, b.ort, b.strasse, b.strasse_original, b.anhang, b.erstbeobachtung, b.beschreibung, b.besonderes, "
        "b.mauersegler, b.sperling, b.schwalbe, b.fledermaus, b.star, b.andere, "
        "b.sanierung, b.ersatz, b.kontrolle, b.verloren, "
        "o.latitude AS osm_latitude, o.longitude AS osm_longitude, gg.latitude AS google_latitude, gg.longitude AS google_longitude "
        "FROM gebaeudebrueter b "
        "LEFT JOIN geolocation_osm o ON b.web_id = o.web_id "
        "LEFT JOIN geolocation_google gg ON b.web_id = gg.web_id "
        + where_sql
    )
    cursor.execute(query)
    return cursor.fetchall()


def compute_invalid_map_rows(cursor):
    rows = fetch_rows_for_validation(cursor)
    invalid = []

    for row in rows:
        payload = build_marker_payload(
            row=row,
            url='http://www.gebaeudebrueter-in-berlin.de/index.php',
            email_recipient='detlefdev@gmail.com',
            status_info=STATUS_INFO,
            pick_primary_status_fn=pick_primary_status,
            species_list_from_row_fn=species_list_from_row,
            build_divicon_html_fn=build_divicon_html,
        )
        if payload is None:
            continue

        species = species_list_from_row(row)
        has_species = len(species) > 0
        plz = str(row['plz'] or '').strip()
        has_plz = any(ch.isdigit() for ch in plz)
        street = str(row['strasse'] or '').strip()
        has_street = bool(street)
        has_house_number = bool(HOUSE_NUMBER_RE.search(street))

        if has_species and has_plz and has_street and has_house_number:
            continue

        reason = []
        if not has_species:
            reason.append('missing_species')
        if not has_plz:
            reason.append('missing_plz')
        if not has_street:
            reason.append('missing_street')
        if has_street and not has_house_number:
            reason.append('missing_house_number')

        invalid.append(
            {
                'web_id': int(row['web_id']),
                'plz': plz,
                'strasse': street,
                'reason': '|'.join(reason),
            }
        )

    return invalid


def write_report(invalid_rows):
    out = REPORTS_DIR / 'data_excluded_candidates.csv'
    out_path = ensure_parent_dir(out)
    with open(out_path, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['web_id', 'reason', 'plz', 'strasse'])
        writer.writeheader()
        for row in sorted(invalid_rows, key=lambda x: x['web_id']):
            writer.writerow(row)
    return out_path


def main():
    parser = argparse.ArgumentParser(description='Maintain persistent dataExcluded marker flags.')
    parser.add_argument(
        '--mode',
        choices=['add', 'sync', 'clear'],
        default='add',
        help='add: mark newly invalid rows, sync: reset then mark current invalid rows, clear: remove all flags',
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Dry validation mode: compute and report deltas without writing DB changes.',
    )
    parser.add_argument(
        '--fail-on-delta',
        action='store_true',
        help='With --check: exit non-zero when new candidates must be added to dataExcluded.',
    )
    parser.add_argument(
        '--fail-on-any-delta',
        action='store_true',
        help='With --check: exit non-zero on any delta (new candidates or stale flags).',
    )
    args = parser.parse_args()

    conn = connect_sqlite(row_factory=True)
    cur = conn.cursor()

    added_column = ensure_data_excluded_column(cur)
    if added_column:
        conn.commit()

    cur.execute('SELECT COUNT(*) AS c FROM gebaeudebrueter WHERE dataExcluded=1')
    before = cur.fetchone()['c']
    cur.execute('SELECT web_id FROM gebaeudebrueter WHERE dataExcluded=1')
    flagged_ids_before = {int(r['web_id']) for r in cur.fetchall()}

    changed = 0
    invalid_rows = []
    invalid_ids = set()
    to_add = set()
    stale = set()

    if args.mode != 'clear':
        invalid_rows = compute_invalid_map_rows(cur)
        invalid_ids = {row['web_id'] for row in invalid_rows}
        to_add = invalid_ids - flagged_ids_before
        stale = flagged_ids_before - invalid_ids

    if args.check:
        report_path = write_report(invalid_rows) if invalid_rows else None
        print(f'mode={args.mode}')
        print('check_only=True')
        print(f'flagged_before={before}')
        print(f'candidates_now={len(invalid_ids)}')
        print(f'to_add_count={len(to_add)}')
        print(f'stale_count={len(stale)}')
        if report_path:
            print(f'report={report_path}')
        if args.fail_on_any_delta and (to_add or stale):
            raise SystemExit(2)
        if args.fail_on_delta and to_add:
            raise SystemExit(2)
        conn.close()
        return

    if args.mode == 'clear':
        cur.execute('UPDATE gebaeudebrueter SET dataExcluded=NULL WHERE dataExcluded=1')
        changed = cur.rowcount if cur.rowcount is not None else 0
    else:
        invalid_ids_sorted = sorted(invalid_ids)

        if args.mode == 'sync':
            cur.execute('UPDATE gebaeudebrueter SET dataExcluded=NULL WHERE dataExcluded=1')

        if invalid_ids_sorted:
            placeholders = ','.join(['?'] * len(invalid_ids_sorted))
            cur.execute(
                f'UPDATE gebaeudebrueter SET dataExcluded=1 WHERE web_id IN ({placeholders})',
                invalid_ids_sorted,
            )
            changed = cur.rowcount if cur.rowcount is not None else len(invalid_ids_sorted)

    conn.commit()

    cur.execute('SELECT COUNT(*) AS c FROM gebaeudebrueter WHERE dataExcluded=1')
    after = cur.fetchone()['c']

    report_path = write_report(invalid_rows) if invalid_rows else None

    print(f'mode={args.mode}')
    print(f'flagged_before={before}')
    print(f'flagged_after={after}')
    print(f'changed_rows={changed}')
    if report_path:
        print(f'report={report_path}')

    conn.close()


if __name__ == '__main__':
    main()
