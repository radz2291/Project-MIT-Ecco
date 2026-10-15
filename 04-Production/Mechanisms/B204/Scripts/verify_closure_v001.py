import json,re,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[1];PROD=P.parents[1];ROOT=PROD.parent;TASK=PROD/'Records/Tasks/T-010'
docs=[P/'README_v001.md',TASK/'report.md',TASK/'review-questions_v001.md',TASK/'hydraulic-register_v001.md']
checks=[]
for doc in docs:
    for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
        if '://' not in link:
            path=(doc.parent/link).resolve();checks.append({'document':doc.relative_to(ROOT).as_posix(),'target':link,'exists':path.exists()})
assert all(x['exists'] for x in checks),[x for x in checks if not x['exists']]
manifest=json.loads((TASK/'Evidence/output-manifest_v001.json').read_text())
for x in manifest:
    path=ROOT/x['path'];assert path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==x['sha256']
inputs=json.loads((TASK/'Evidence/build-verification_v001.json').read_text())
for file,key in [(PROD/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend','source_sha256'),(PROD/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend','well_sha256')]:
    assert hashlib.sha256(file.read_bytes()).hexdigest()==inputs[key]
data={'local_links':checks,'manifest_hashes_match':True,'shared_master_hashes_unchanged':True,'selected_remote_still':'04-Production/Mechanisms/B204/Previews/B204_inspect_f049_v001.png','other_media':'local only; no backup implied','visual_review':'full-size frames 1,49,288; all 288 schematic frames in ordered contact sheets; no real-time playback claim','candidate':'v001','external_engineering_review':'pending'}
(TASK/'Evidence/closure-verification_v001.json').write_text(json.dumps(data,indent=2))
print(json.dumps({'links':len(checks),'hashes':'pass','shared_sources':'unchanged'}))
