"""Save explicit still-proposal publication list and output hashes."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parents[3];REPO=P.parent;M=P/'Mechanisms/B201';T=P/'Records/Tasks/T-007';E=T/'Evidence/Still_01'
files=[M/'direction.md',M/'Scripts/build_still01_v004.py',M/'Scripts/verify_still01_v004.py',M/'Scripts/close_still01_v004.py',M/'Previews/Still_01/B201_sensor-origin_still01_v004.png',T/'report.md',T/'still-proposal_01_v004.md',E/'build-render_still01_v004.json',E/'verification_still01_v004.json',T/'report_v005.md',T/'Evidence/direction_before-still-gate.md']
manifest=[]
for p in files+[M/'Scenes/B201_sensor-origin_still01_v004.blend']:
 assert p.is_file(),p
 manifest.append({'path':str(p.relative_to(REPO)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'storage':'permitted tracked review output' if p in files else 'local ignored source, no remote backup implied'})
(E/'output-manifest_still01_v004.json').write_text(json.dumps(manifest,indent=2))
files.append(E/'output-manifest_still01_v004.json')
for p in [T/'report.md',T/'still-proposal_01_v004.md']:
 for q in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):assert (p.parent/q).is_file(),q
(E/'git-files_still01_v004.txt').write_text('\n'.join(str(p.relative_to(REPO)).replace('\\','/') for p in files)+'\n')
print('STILL01_CLOSURE_PASS',len(files))
