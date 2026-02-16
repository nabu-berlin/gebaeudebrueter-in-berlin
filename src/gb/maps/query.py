import sqlite3


def fetch_multispecies_rows(cursor):
    cursor.execute("PRAGMA table_info(gebaeudebrueter)")
    gb_cols = {row[1] for row in cursor.fetchall()}

    where_parts = []
    if 'is_test' in gb_cols:
        where_parts.append("(b.is_test IS NULL OR b.is_test=0)")
    if 'noSpecies' in gb_cols:
        where_parts.append("(b.noSpecies IS NULL OR b.noSpecies=0)")
    if 'no_geocode' in gb_cols:
        where_parts.append("(b.no_geocode IS NULL OR b.no_geocode=0)")
    if 'dataExcluded' in gb_cols:
        where_parts.append("(b.dataExcluded IS NULL OR b.dataExcluded=0)")
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
    try:
        cursor.execute(query)
    except sqlite3.OperationalError:
        fallback_query = (
            "SELECT b.web_id, b.bezirk, b.plz, b.ort, b.strasse, b.anhang, b.erstbeobachtung, b.beschreibung, b.besonderes, "
            "b.mauersegler, b.sperling, b.schwalbe, b.fledermaus, b.star, b.andere, "
            "b.sanierung, b.ersatz, b.kontrolle, b.verloren, "
            "o.latitude AS osm_latitude, o.longitude AS osm_longitude, gg.latitude AS google_latitude, gg.longitude AS google_longitude "
            "FROM gebaeudebrueter b "
            "LEFT JOIN geolocation_osm o ON b.web_id = o.web_id "
            "LEFT JOIN geolocation_google gg ON b.web_id = gg.web_id "
            + where_sql
        )
        cursor.execute(fallback_query)
    return cursor.fetchall()
