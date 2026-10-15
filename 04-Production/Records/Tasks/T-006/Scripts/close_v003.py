"""Verify handoff links, evidence, source immutability and retained output hashes."""
import json,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];REPO=ROOT.parent;TASK=ROOT/'Records/Tasks/T-006';ASSET=ROOT/'Shared/Assets/WellAssembly'
docs=[TASK/'report.md',TASK/'report_v003.md',ASSET/'README.md',ASSET/'README_v003.md']
manifest_path=TASK/'Evidence/output-manifest_v003.json'
manifest_path.write_text('[]',encoding='utf-8')
links=[]
for doc in docs:
    for target in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
        if target.startswith(('http:','https:')):continue
        p=(doc.parent/target.split('#')[0]).resolve();links.append({'document':str(doc.relative_to(REPO)),
            'target':target,'exists':p.is_file()})
assert all(row['exists'] for row in links),[r for r in links if not r['exists']]
for script in list((TASK/'Scripts').glob('*_v003.py'))+[ASSET/'Scripts/build_variants_v003.py']:
    compile(script.read_text(encoding='utf-8'),str(script),'exec')
for path in ('variants-verification_v003.json','editable-consumer-checks_v003.json'):
    assert json.loads((TASK/'Evidence'/path).read_text())['all_pass']
assert all(row['all_pass'] for row in json.loads((TASK/'Evidence/preview-consumer-checks_v003.json').read_text()))
qa=json.loads((TASK/'Evidence/video-qa_v003.json').read_text())
assert qa[-1]['frames']==528 and qa[-1]['metadata']['duration']==22
c=json.loads((ASSET/'config_authorized_v003.json').read_text())
assert hashlib.sha256((ASSET/c['product_library']).resolve().read_bytes()).hexdigest()==c['product_sha256']
assert 'O05' in (REPO/'03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md').read_text(encoding='utf-8')
result={'all_pass':True,'local_links':links,'master_and_consumers_verified':True,
        'source_unchanged':True,'combined_video_frames':528,'combined_video_seconds':22,
        'candidate':'uncommitted; local ignored media/raw frames; no push/backup',
        'visual_review':'All528 raw frames inspected in chronological mosaics; encoded keyframe sheet/profile plot and full-size keyframes reviewed. No real-time playback claim.'}
(TASK/'Evidence/closure-checks_v003.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
files=[p for folder in (TASK,ASSET) for p in folder.rglob('*') if p.is_file() and
       (('v003' in p.name or 'v003' in str(p.parent)) or p in docs) and p!=manifest_path]
manifest=[{'path':str(p.relative_to(REPO)).replace('\\','/'),'bytes':p.stat().st_size,
           'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
manifest_path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('CLOSURE_PASS',len(links),'links;',len(manifest),'output hashes')
