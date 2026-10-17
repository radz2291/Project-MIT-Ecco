"""Self-check T31's text proposal; never opens Blender or validates physics."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / '04-Production/Records/Tasks/T-031'
index = json.loads((TASK / 'Evidence/shot-index_v001.json').read_text())
sources = json.loads((TASK / 'Evidence/source-manifest_v001.json').read_text())
assert len(index) == 17
assert len({s['shot_id'] for s in index}) == 17
assert index[0]['start_s'] == 0 and index[-1]['end_s'] == 90
assert all(a['end_s'] == b['start_s'] for a, b in zip(index, index[1:]))
assert sum(s['duration_s'] for s in index) == 90
budgets = {'S01': 10, 'S02': 12, 'S03': 18, 'S04': 18, 'S05': 12, 'S06': 12, 'S07': 8}
for section, seconds in budgets.items():
    assert sum(s['duration_s'] for s in index if s['section'] == section) == seconds
files = [ROOT / s['contract'] for s in index]
files += [ROOT / '04-Production/Direction/B3/film-direction-map_v001.md', TASK / 'report.md']
links = 0
for p in files:
    text = p.read_text(encoding='utf-8')
    if p.name == 'direction.md':
        assert len(re.findall(r'^## \d+\.', text, re.M)) == 11, p
        assert 'proposal_not_approved' in text and 'TBD_AFTER_NATIVE_SCENE_INSPECTION' in text
    for uri in re.findall(r'\]\(([^)]+)\)', text):
        if uri.startswith(('https://', 'http://', '#')):
            continue
        target = (p.parent / uri.split('#')[0]).resolve()
        # This run writes its own evidence file after collecting results.
        if target != (TASK / 'Evidence/verification_v001.json').resolve():
            assert target.exists(), (p, uri)
        links += 1
for source in sources['inputs']:
    assert hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() == source['sha256'], source['path']
outputs = [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
result = {'status': 'PASS', 'shot_count': len(index), 'duration_seconds': 90,
          'frames_at_provisional_24fps': 2160, 'section_budgets_seconds': budgets,
          'contracts_with_11_schema_fields': 17, 'resolved_local_markdown_links': links,
          'unchanged_fingerprinted_inputs': len(sources['inputs']), 'outputs': outputs,
          'limits': 'Text/arithmetic/source-integrity self-check only; no rendered, moving, audience or engineering validation.'}
(TASK / 'Evidence/verification_v001.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'outputs'}))
