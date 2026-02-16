import sqlite3
import folium
from folium import plugins
import sys
import importlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
  sys.path.insert(0, str(SRC_DIR))

maps_multispecies = importlib.import_module('gb.maps.multispecies')
maps_query = importlib.import_module('gb.maps.query')
maps_transform = importlib.import_module('gb.maps.transform')
maps_render = importlib.import_module('gb.maps.render')
maps_controls = importlib.import_module('gb.maps.controls_template')

SPECIES_COLORS = maps_multispecies.SPECIES_COLORS
STATUS_INFO = maps_multispecies.STATUS_INFO
pick_primary_status = maps_multispecies.pick_primary_status
species_list_from_row = maps_multispecies.species_list_from_row
build_divicon_html = maps_multispecies.build_divicon_html
fetch_multispecies_rows = maps_query.fetch_multispecies_rows
build_marker_payload = maps_transform.build_marker_payload
format_stand_display = maps_render.format_stand_display
inject_map_ui = maps_render.inject_map_ui
build_controls_html = maps_controls.build_controls_html

CONFIG = {
  'DB_PATH': 'brueter.sqlite',
  'OUTPUT_HTML': 'GebaeudebrueterMultiMarkers.html',
  'NABU_BASE_URL': 'http://www.gebaeudebrueter-in-berlin.de/index.php',
  'FEEDBACK_EMAIL_RECIPIENT': 'detlefdev@gmail.com',
  'REPORT_EMAIL_TO': 'meldung@gebaeudebrueter-in-berlin.de',
  'REPORT_EMAIL_CC': 'detlefdev@gmail.com',
  'ONLINE_FORM_URL': 'https://berlin.nabu.de/wir-ueber-uns/bezirksgruppen/steglitz-zehlendorf/projekte/gebaeudebrueter/12400.html',
}

DB_PATH = CONFIG['DB_PATH']
OUTPUT_HTML = CONFIG['OUTPUT_HTML']


def main():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()

  try:
    cur.execute('SELECT MAX(update_date) as last FROM gebaeudebrueter')
    last_raw = cur.fetchone()[0]
  except Exception:
    last_raw = None

  controls_html = build_controls_html(
    species_colors=SPECIES_COLORS,
    status_info=STATUS_INFO,
    online_form_url=CONFIG['ONLINE_FORM_URL'],
    email_recipient=CONFIG['FEEDBACK_EMAIL_RECIPIENT'],
  )

  m = folium.Map(location=[52.5163, 13.3777], tiles='cartodbpositron', zoom_start=12)
  marker_cluster = plugins.MarkerCluster()
  m.add_child(marker_cluster)

  rows = fetch_multispecies_rows(cur)
  url = CONFIG['NABU_BASE_URL']

  count = 0
  for row in rows:
    marker_payload = build_marker_payload(
      row=row,
      url=url,
      report_email_to=CONFIG['REPORT_EMAIL_TO'],
      report_email_cc=CONFIG['REPORT_EMAIL_CC'],
      status_info=STATUS_INFO,
      pick_primary_status_fn=pick_primary_status,
      species_list_from_row_fn=species_list_from_row,
      build_divicon_html_fn=build_divicon_html,
    )
    if marker_payload is None:
      continue

    icon = folium.DivIcon(
      html=marker_payload['icon_html'],
      icon_size=(26, 26),
      icon_anchor=(13, 13),
    )

    folium.Marker(
      location=[marker_payload['latf'], marker_payload['lonf']],
      popup=folium.Popup(marker_payload['popup_html'], max_width=450),
      tooltip=marker_payload['tooltip_text'],
      icon=icon,
    ).add_to(marker_cluster)
    count += 1

  stand_display = format_stand_display(last_raw)
  inject_map_ui(m, controls_html, stand_display, count)

  m.save(OUTPUT_HTML)
  conn.close()


if __name__ == '__main__':
  main()
