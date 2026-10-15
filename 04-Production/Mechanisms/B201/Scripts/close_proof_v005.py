"""Verify final media and links; record a bounded publication list."""
from pathlib import Path
import json,hashlib,re,subprocess
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[3];REPO=ROOT.parent;M=ROOT/'Mechanisms/B201';R=ROOT/'Records/Tasks/T-007'
video=M/'Previews/B201_pulse-echo_v005.mp4'
reader=imageio_ffmpeg.read_frames(str(video),pix_fmt='rgb24');meta=next(reader);count=sum(1 for _ in reader)
assert count==432 and meta['size']==(1280,720) and meta['fps']==24 and abs(meta['duration']-18)<.01,meta
links=[]
for p in [R/'report.md',R/'review-questions_v005.md',R/'proof-register_v005.md',M/'README_v005.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if not target.startswith(('http:','https:')):links.append({'source':str(p.relative_to(REPO)),'target':target,'exists':(p.parent/target).is_file()})
pending={'Evidence/output-manifest_v005.json','Evidence/closure_v005.json'}
assert all(x['exists'] or x['target'] in pending for x in links),[x for x in links if not x['exists'] and x['target'] not in pending]
build=json.loads((R/'Evidence/build_v005.json').read_text())
for rel,h in build['inputs'].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h
publish=[M/'README_v005.md',*(M/'Scripts'/n for n in ['build_proof_v005.py','package_preview_v005.py','verify_proof_v005.py','motion_sheets_v005.py','close_proof_v005.py']),M/'Previews/B201_review_f0021_v005.png',M/'Previews/B201_review_f0432_v005.png',R/'report.md',R/'review-questions_v005.md',R/'proof-register_v005.md',*(R/'Evidence'/n for n in ['build_v005.json','render_v005.json','verification_v005.json','video-qa_v005.json'])]
manifest=[]
for p in publish+[M/'Scenes/B201_pulse-echo_v005.blend',video]:
 assert p.is_file(),p
 manifest.append({'path':str(p.relative_to(REPO)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'storage':'permitted tracked candidate' if p in publish else 'local Git-ignored binary, no remote backup'})
(R/'Evidence/output-manifest_v005.json').write_text(json.dumps(manifest,indent=2))
for x in links:
 if x['target'] in pending:x['exists']=True
closure={'media':{**meta,'decoded_frames':count},'links':links,'visual_review':'all432 states in ordered contact sheets; full-size causal/boundary/final labels; no realtime playback claim','structural_checks':86,'source_hashes_unchanged':True,'feedback':'pending Radzi/MIT','passed':True}
(R/'Evidence/closure_v005.json').write_text(json.dumps(closure,indent=2))
assert all((REPO/x['source']).parent.joinpath(x['target']).is_file() for x in links)
publish += [R/'Evidence/output-manifest_v005.json',R/'Evidence/closure_v005.json']
(R/'Evidence/git-files_v005.txt').write_text('\n'.join(str(p.relative_to(REPO)).replace('\\','/') for p in publish)+'\n')
print('B201_CLOSURE_PASS',count,len(links),len(publish))
