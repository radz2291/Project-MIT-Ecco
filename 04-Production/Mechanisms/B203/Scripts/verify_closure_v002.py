"""Create precise local/source output hashes and agreed public review file list."""
from pathlib import Path
import hashlib,json,re
BASE=Path(__file__).resolve().parents[1];PROD=BASE.parents[1];ROOT=PROD.parent;TASK=PROD/'Records/Tasks/T-009';EVID=TASK/'Evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads((EVID/'build-render_v002.json').read_text());qa=json.loads((EVID/'video-qa_v002.json').read_text())
for row in rows:
    p=ROOT/row['scene'];assert sha(p)==row['scene_sha256']
for row in qa:
    p=ROOT/row['video'];assert sha(p)==row['sha256']
sources=[PROD/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend',PROD/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend',PROD/'Shared/Assets/WellAssembly/config_authorized_v003.json']
assert sha(sources[0])=='704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7'
artifacts=[ROOT/r['scene'] for r in rows]+[ROOT/r['video'] for r in qa]+list((BASE/'Scripts').glob('*v002.py'))
manifest={'candidate':'B203 v002','root':str(ROOT),'sources':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p)} for p in sources],
 'artifacts':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p),'local_only':p.suffix in ('.blend','.mp4')} for p in artifacts],
 'binaries_backup':'Local organized only; Git excludes media, no remote backup asserted',
 'checks':{'scene_hashes_match_render':True,'video_hashes_match_decode':True,'product_hash_preserved':True,'frames':576,'fps':24,'seconds':24}}
(EVID/'output-manifest_v002.json').write_text(json.dumps(manifest,indent=2))
# Check all local Markdown links before freezing integration list.
docs=[BASE/'README.md',TASK/'report.md',TASK/'review-questions_v002.md']
for doc in docs:
    for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
        if '://' not in link:assert (doc.parent/link).exists(),(doc,link)
paths=[BASE/'README.md',TASK/'report.md',TASK/'review-questions_v002.md',TASK/'git-handoff_v002.md']
paths+=list((BASE/'Scripts').glob('*v002.py'))
paths+=[EVID/n for n in ['build-render_v002.json','fresh-open-verification_v002.json','video-qa_v002.json','output-manifest_v002.json','visual-qa_v002.md']]
paths+=[BASE/f'Previews/v002/B203_{c}_f144_v002.png' for c in ('retrieval','support','channel','wear')]
paths+=[BASE/'Previews/v002/B203_review-sheet_v002.jpg',EVID/'git-files_v002.txt',EVID/'integration-ready_v002.json']
relative=sorted(str(p.relative_to(ROOT)).replace('\\','/') for p in paths)
(EVID/'git-files_v002.txt').write_text('\n'.join(relative)+'\n')
(EVID/'integration-ready_v002.json').write_text(json.dumps({'ready':True,'integrator':'T7','git_mutations_by_T9':False,'files':relative,'task':'T9','candidate':'v002','report':'04-Production/Records/Tasks/T-009/report.md','video_frames':576,'sha256_video':qa[-1]['sha256'],'checks':'fresh-open, geometry, full decode and sequential visual QA pass for declared conceptual scope','technical_acceptance':'pending Radzi / B206','scope':'Stage only listed permitted files; no media/raw/superseded outputs'},indent=2))
print('CLOSURE_PASS',len(relative))
