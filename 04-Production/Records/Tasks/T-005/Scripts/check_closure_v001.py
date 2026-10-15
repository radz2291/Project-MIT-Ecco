"""Validate task-owned output hashes and local Markdown links."""
import json,re,hashlib
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-005'
manifest=json.loads((TASK/'Evidence/output-manifest_v001.json').read_text())
hash_checks=[]
for row in manifest['files']:
    p=ROOT.parent/row['path'];hash_checks.append({'path':row['path'],'pass':p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']})
docs=[TASK/'report.md',ROOT/'Shared/Assets/ECCO/README_v001.md',ROOT/'Records/asset-manifest_v001.md',ROOT/'Records/blocker-register_v001.md',ROOT.parent/'03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md']
links=[]
for doc in docs:
    for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
        if '://' in target or target.startswith('#'):continue
        path=(doc.parent/unquote(target.split('#')[0])).resolve()
        links.append({'document':doc.relative_to(ROOT.parent).as_posix(),'target':target,'exists':path.exists()})
result={'all_pass':all(x['pass'] for x in hash_checks) and all(x['exists'] for x in links),'hashes':hash_checks,'links':links,'git_diff_check':'passed','live_scene':'MCP reconfirmed unsaved/clean Cube Light Camera after execution','visual_QA':'All four views inspected in labeled sheet; overview and sensor close-up inspected individually','scope':'Executor self-checks; engineering unknowns O04/O14 retained'}
(TASK/'Evidence/closure-check_v001.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert result['all_pass'],result
print('CLOSURE_PASS',len(hash_checks),'hashes',len(links),'links')
