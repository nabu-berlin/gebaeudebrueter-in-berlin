import re
from pathlib import Path

multi = Path('docs') / 'GebaeudebrueterMultiMarkers.html'

def extract(path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    ids = set(int(m) for m in re.findall(r'index\.php\?ID=(\d+)', txt))
    ids2 = set(int(m) for m in re.findall(r'>(\d{3,6})<', txt))
    return ids.union(ids2)

ids_multi = extract(multi)
print('multi_count', len(ids_multi))
txt_multi = multi.read_text(encoding='utf-8', errors='ignore')
print('multi L.marker count', txt_multi.count('L.marker('))
print('multi var marker count', txt_multi.count('var marker_'))
for sample in [385,1784,1214,1680]:
    print(sample, 'in multi?', sample in ids_multi)
