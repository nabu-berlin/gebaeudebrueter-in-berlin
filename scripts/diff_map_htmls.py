import sys
from pathlib import Path

def extract_marker_count(text):
    for line in text.splitlines():
        if 'Markers:' in line:
            try:
                part = line.split('Markers:')[-1]
                return int(''.join(ch for ch in part if ch.isdigit()))
            except Exception:
                continue
    return None

p = Path(__file__).parent
f1 = p.parent / 'docs' / 'GebaeudebrueterMultiMarkers.html'
f2 = p.parent / 'GebaeudebrueterMultiMarkers.html'
if not f1.exists() or not f2.exists():
    print('One or both files missing:', f1, f2)
    sys.exit(2)

s1 = f1.read_text(encoding='utf-8', errors='ignore')
s2 = f2.read_text(encoding='utf-8', errors='ignore')

c1 = extract_marker_count(s1)
c2 = extract_marker_count(s2)

lines1 = s1.splitlines()
lines2 = s2.splitlines()

# compute simple diff stats
set1 = set(lines1)
set2 = set(lines2)
only1 = [l for l in lines1 if l not in set2][:20]
only2 = [l for l in lines2 if l not in set1][:20]

print('docs file:', f1)
print('root file:', f2)
print('\nMarker counts:')
print('  docs:', c1)
print('  root:', c2)
print('\nTop differences (first 20 unique lines present only in docs):')
for l in only1:
    print('> ', l)
print('\nTop differences (first 20 unique lines present only in root):')
for l in only2:
    print('< ', l)

# show a small context diff for the Markers line
for i, line in enumerate(lines1):
    if 'Markers:' in line:
        start = max(0, i-3)
        print('\nContext around docs Markers:')
        print('\n'.join(lines1[start:start+7]))
        break
for i, line in enumerate(lines2):
    if 'Markers:' in line:
        start = max(0, i-3)
        print('\nContext around root Markers:')
        print('\n'.join(lines2[start:start+7]))
        break
