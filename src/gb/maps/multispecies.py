import json

SPECIES_COLORS = {
    'Mauersegler': '#1f78b4',
    'Sperling': '#33a02c',
    'Schwalbe': '#6a3d9a',
    'Fledermaus': '#000000',
    'Star': '#b15928',
    'Andere': '#ff7f00',
}

STATUS_INFO = {
    'verloren': {'label': 'Nicht mehr', 'color': '#616161', 'short': '×'},
    'sanierung': {'label': 'Sanierung', 'color': '#e31a1c', 'short': 'S'},
    'ersatz': {'label': 'Ersatzmaßn.', 'color': '#00897b', 'short': 'E'},
    'kontrolle': {'label': 'Kontrolle', 'color': '#1976d2', 'short': 'K'},
    'none': {'label': 'Ohne Status', 'color': '#9e9e9e', 'short': '—'},
}

STATUS_PRIORITY = ['verloren', 'sanierung', 'ersatz', 'kontrolle']
NEUTRAL_FILL = '#cccccc'


def pick_primary_status(row):
    statuses = []
    for key in STATUS_PRIORITY:
        try:
            val = row[key]
        except Exception:
            val = None
        if val:
            statuses.append(key)
    primary = statuses[0] if statuses else None
    return primary, statuses


def species_list_from_row(row):
    def safe_bool(col):
        try:
            return bool(row[col])
        except Exception:
            return False

    flags = {
        'Mauersegler': safe_bool('mauersegler'),
        'Sperling': safe_bool('sperling'),
        'Schwalbe': safe_bool('schwalbe'),
        'Fledermaus': safe_bool('fledermaus'),
        'Star': safe_bool('star'),
        'Andere': safe_bool('andere'),
    }
    return [name for name, flag in flags.items() if flag]


def conic_gradient_for_species(species):
    if not species:
        return NEUTRAL_FILL
    n = min(len(species), 4)
    seg_angle = 360 / n
    stops = []
    for i, sp in enumerate(species[:n]):
        start = round(i * seg_angle, 2)
        end = round((i + 1) * seg_angle, 2)
        color = SPECIES_COLORS.get(sp, '#9e9e9e')
        stops.append(f'{color} {start}deg {end}deg')
    return f"conic-gradient({', '.join(stops)})"


def build_divicon_html(species, status_key, all_statuses, address_text):
    gradient_fill = conic_gradient_for_species(species)
    status_color = STATUS_INFO[status_key]['color'] if status_key else '#9e9e9e'
    status_short = STATUS_INFO[status_key]['short'] if status_key else ''
    status_label = STATUS_INFO[status_key]['label'] if status_key else ''

    data_species = json.dumps(species, ensure_ascii=False)
    data_statuses = json.dumps(all_statuses, ensure_ascii=False)

    html = f'''
  <div class="ms-marker"
     data-species='{data_species}'
     data-statuses='{data_statuses}'
     data-statuscolor="{status_color}"
     data-statuslabel="{status_label}"
     data-address="{address_text}"
         style="--ms-marker-fill:{gradient_fill}; --ms-status-color:{status_color};">
        <div class="ms-badge">{status_short}</div>
  </div>
  '''
    return html
