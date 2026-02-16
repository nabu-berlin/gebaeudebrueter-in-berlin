from urllib.parse import quote


def _berlin_plz_ok(row):
    try:
        plz_raw = row['plz'] or ''
    except Exception:
        plz_raw = ''
    plz_digits = ''.join(ch for ch in str(plz_raw) if ch.isdigit())
    plz_num = None
    try:
        if plz_digits:
            plz_num = int(plz_digits)
    except Exception:
        plz_num = None
    return plz_num is not None and (10000 <= plz_num <= 14199)


def _lat_lon(row):
    lat = None
    lon = None
    if row['google_latitude'] is not None and str(row['google_latitude']) != 'None':
        lat = row['google_latitude']
        lon = row['google_longitude']
    elif row['osm_latitude'] is not None and str(row['osm_latitude']) != 'None':
        lat = row['osm_latitude']
        lon = row['osm_longitude']

    if lat is None or lon is None:
        return None, None

    try:
        return float(lat), float(lon)
    except Exception:
        return None, None


def _address_field(row):
    addr_field = None
    try:
        if row['strasse_original'] and str(row['strasse_original']).strip():
            addr_field = row['strasse_original']
    except Exception:
        addr_field = None
    if not addr_field:
        addr_field = row['strasse']
    return addr_field


def _append_mailto_report_link(popup_html, row, addr_field, report_email_to, report_email_cc):
    try:
        web_id = row['web_id']
        full_address = f"{addr_field}, {row['plz']} {row['ort']}".strip().strip(',')
        if not full_address or full_address.lower() == 'none':
            full_address = 'Adresse unbekannt'

        subject = f"Kontrolle Gebäudebrüter-Standort: Fundort-ID {web_id}"
        body = (
            "Hallo NABU-Team,\n\n"
            "ich möchte folgende Beobachtung an den NABU melden.\n\n"
            f"Adresse: {full_address}\n\n"
            f"Fundort-ID: {web_id}\n\n"
            "Datum der Beobachtung: (falls nicht anders angeben, gilt das Datum dieser E-Mail)\n\n"
            "Beobachtete Gebäudebrüter-Art(en):\n\n"
            "Anmerkungen zum Fundort und mögliche Gefährdungen:\n\n\n"
            "Fotos im Anhang: ja/nein\n\n"
            "Die Beobachtung erfolgte durch (Angaben sind optional):\n\n"
            "Anrede:\n\n"
            "Mein Name:\n"
            "PLZ, Wohnort:\n"
            "Straße, Hausnummer:\n\n\n"
            "Hinweis zum Datenschutz: Der NABU erhebt und verarbeitet Ihre personenbezogenen Daten ausschließlich für Vereinszwecke. Dabei werden Ihre Daten - gegebenenfalls durch Beauftragte - auch für NABU-eigene Informationszwecke verarbeitet und genutzt. Eine Weitergabe an Dritte erfolgt niemals. Der Verwendung Ihrer Daten kann jederzeit schriftlich oder per E-Mail an lvberlin@nabu-berlin.de widersprochen werden.\n"
        )
        mailto = (
            f"mailto:{report_email_to}?cc={quote(report_email_cc, safe='')}&"
            f"subject={quote(subject, safe='')}&body={quote(body, safe='')}"
        )
        popup_html += (
            f"<br/><br/><a href=\"{mailto}\" target=\"_blank\" rel=\"noreferrer\" onclick=\"return gbHumanConfirmReport(event, {web_id}, this.href);\" "
            f"class=\"gb-report-link\">Beobachtung melden</a>"
        )
    except Exception:
        pass
    return popup_html


def build_marker_payload(
    row,
    url,
    report_email_to,
    report_email_cc,
    status_info,
    pick_primary_status_fn,
    species_list_from_row_fn,
    build_divicon_html_fn,
):
    if not _berlin_plz_ok(row):
        return None

    latf, lonf = _lat_lon(row)
    if latf is None or lonf is None:
        return None

    species = species_list_from_row_fn(row)
    primary_status, all_statuses = pick_primary_status_fn(row)

    fund_text = ', '.join(species) if species else 'andere Art'
    status_names = [status_info[k]['label'] for k in all_statuses]
    status_text = ', '.join(status_names) if status_names else '—'

    addr_field = _address_field(row)
    popup_html = (
        f"<b>Arten</b><br/>{fund_text}"
        f"<br/><br/><b>Status</b><br/>{status_text}"
        f"<br/><br/><b>Adresse</b><br/>{addr_field}, {row['plz']} {row['ort']}"
        f"<br/><br/><b>Erstbeobachtung</b><br/>{(str(row['erstbeobachtung']) if row['erstbeobachtung'] else 'unbekannt')}"
        f"<br/><br/><b>Beschreibung</b><br/>{(row['beschreibung'] or '')}"
        f"<br/><br/><b>Link zur Datenbank</b><br/><a href={url}?ID={row['web_id']}>{row['web_id']}</a>"
    )
    popup_html = _append_mailto_report_link(
        popup_html,
        row,
        addr_field,
        report_email_to,
        report_email_cc,
    )

    address_text = f"{addr_field}, {row['plz']} {row['ort']}"
    icon_html = build_divicon_html_fn(species, primary_status, all_statuses, address_text)
    tooltip_text = 'Mehrere Arten' if len(species) > 1 else (species[0] if species else 'Andere')

    return {
        'latf': latf,
        'lonf': lonf,
        'popup_html': popup_html,
        'icon_html': icon_html,
        'tooltip_text': tooltip_text,
    }
