import re
from pathlib import Path

p = Path(__file__).parent
f_docs = p.parent / 'docs' / 'GebaeudebrueterMultiMarkers.html'
f_root = p.parent / 'GebaeudebrueterMultiMarkers.html'

if not f_docs.exists() or not f_root.exists():
    print('Missing files:', f_docs.exists(), f_root.exists())
    raise SystemExit(2)

text_docs = f_docs.read_text(encoding='utf-8', errors='ignore')
text_root = f_root.read_text(encoding='utf-8', errors='ignore')

patterns = [r'\?ID=(\d+)', r'gbHumanConfirmReport\([^,]+,\s*(\d+),', r'Fundort-ID[^0-9]*(\d{1,6})']

def extract(text):
    s = set()
    for pat in patterns:
        for m in re.findall(pat, text):
            try:
                s.add(int(m))
            except Exception:
                pass
    # as a fallback try to parse marker popup anchors that include the numeric ID in HTML
    # find occurrences of ">web_id</a> patterns
    for m in re.findall(r'>(\d{1,6})<\/a>', text):
        try:
            s.add(int(m))
        except:
            pass
    return s

sd = extract(text_docs)
sr = extract(text_root)

only_docs = sorted(sd - sr)
only_root = sorted(sr - sd)
common = sorted(sd & sr)

print('counts: docs={}, root={}, common={}'.format(len(sd), len(sr), len(common)))
print('\nOnly in docs (count={}):'.format(len(only_docs)))
print(','.join(map(str, only_docs[:200])))
print('\nOnly in root (count={}):'.format(len(only_root)))
print(','.join(map(str, only_root[:200])))
print('\nSample common (first 50):')
print(','.join(map(str, common[:50])))

# write outputs for convenience
out = p.parent / 'reports' / 'diff_marker_webids.txt'
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, 'w', encoding='utf-8') as fh:
    fh.write('counts: docs={}, root={}, common={}\n'.format(len(sd), len(sr), len(common)))
    fh.write('\nOnly in docs ({}):\n'.format(len(only_docs)))
    fh.write('\n'.join(map(str, only_docs)))
    fh.write('\n\nOnly in root ({}):\n'.format(len(only_root)))
    fh.write('\n'.join(map(str, only_root)))
    fh.write('\n\nCommon ({}):\n'.format(len(common)))
    fh.write('\n'.join(map(str, common)))
print('\nWrote detailed list to', out)
