from pathlib import Path
p = Path(__file__).parent.parent / 'reports' / 'diff_marker_webids.txt'
text = p.read_text(encoding='utf-8')
lines = text.splitlines()
# parse Only in docs section
start = None
for i,l in enumerate(lines):
    if l.strip().startswith('Only in docs'):
        start = i+1
        break
docs = []
if start is not None:
    for l in lines[start:]:
        if not l.strip():
            break
        docs.append(int(l.strip()))
# build set for lookup
docs_set = set(docs)
# find prefixed variants: numbers starting with '20' whose tail is in docs_set
pairs = []
for n in docs:
    s = str(n)
    if s.startswith('20') and len(s) > 2:
        tail = int(s[2:])
        if tail in docs_set:
            pairs.append((n, tail))
# Also detect '20' + tail where tail in common (not in docs list)
# parse common section
comm_start = None
for i,l in enumerate(lines):
    if l.strip().startswith('Common'):
        comm_start = i+1
        break
common = set()
if comm_start is not None:
    for l in lines[comm_start:]:
        if not l.strip():
            break
        try:
            common.add(int(l.strip()))
        except:
            pass
# find prefixed where base in common
pairs_common = []
for n in docs:
    s = str(n)
    if s.startswith('20') and len(s) > 2:
        tail = int(s[2:])
        if tail in common and tail not in docs_set:
            pairs_common.append((n, tail))

out = Path(__file__).parent.parent / 'reports' / 'prefixed_variants.txt'
with open(out, 'w', encoding='utf-8') as fh:
    fh.write('Prefixed pairs where both prefixed and base are in docs-only:\n')
    for a,b in pairs:
        fh.write(f'{a} -> {b}\n')
    fh.write('\nPrefixed pairs where prefixed in docs-only and base in common:\n')
    for a,b in pairs_common:
        fh.write(f'{a} -> {b}\n')
print('Wrote', out)
