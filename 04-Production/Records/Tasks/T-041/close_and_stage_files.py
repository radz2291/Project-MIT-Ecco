"""Inventory retained candidate and copy explicit permitted task files to integrator.
Does not stage, commit, push, remove files or copy heavy/private media.
"""
import json,hashlib,sys,re,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[2];root=P.parent;B=P/'Shots/S02/PREVIS-T041';E=R/'Evidence';V=B/'Previews/v003'
verify=json.loads((E/'verification_v003.json').read_text());video=json.loads((E/'video-qa_v003.json').read_text());times=json.loads((E/'render_all_v003.json').read_text())
assert verify['passed'] and video['decoded_frames']==288 and video['container_metadata_verified']
paths=[B/'Scenes/S02_previs_T041_v003.blend',V/'S02_previs_T041_v003.mp4',V/'review_v003.html',*sorted(V.glob('S02_*_v003.png')),*sorted(V.glob('S02_*_v003.jpg'))]
manifest={'candidate':'T41 experimental v003','local_root':str(root),'artifacts':[{'path':str(p.relative_to(root)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'local_only_ignored':p.suffix in ('.blend','.mp4')} for p in paths],'native_hash_matches_verification':hashlib.sha256(paths[0].read_bytes()).hexdigest()==verify['scene_sha256'],'raw_frames':len(list((V/'Frames').glob('frame_*.png'))),'render_seconds':{'mean':statistics.mean(t['seconds'] for t in times),'max':max(t['seconds'] for t in times),'total':sum(t['seconds'] for t in times)},'checks':verify['checks'],'human_comprehension':'pending','engineering_review':'pending','preserved_attempts':['v001','v002']}
assert manifest['native_hash_matches_verification'] and manifest['raw_frames']==288
(E/'artifacts_v003.json').write_text(json.dumps(manifest,indent=2))
# Report's local relative links must resolve; Git online deliberately excludes native/video.
links=[]
for p in [R/'report.md',B/'direction.md',R/'asset-register_v003.md']:
    for href in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
        if '://' in href:continue
        target=(p.parent/href).resolve();links.append({'from':str(p.relative_to(root)),'target':href,'exists':target.exists()})
assert all(x['exists'] for x in links),links
(E/'link_checks_v003.json').write_text(json.dumps(links,indent=2))
# Retained experiments have sources/QA; no raw frames or binary scene/video in Git.
allowed=[*sorted(B.glob('*.md')),*sorted(B.glob('S02-*/direction.md')),*sorted((B/'Scripts').glob('*.py')),*sorted(R.glob('*.md')),*sorted(R.glob('*.py')),*sorted(E.glob('*.json')),V/'review_v003.html',*sorted(V.glob('S02_*_v003.png')),*sorted(V.glob('S02_*_v003.jpg'))]
allowed=[p for p in allowed if not p.name.startswith('live-input')]
names=sorted(set(str(p.relative_to(root)).replace('\\','/') for p in allowed))
(R/'sync-files_v003.json').write_text(json.dumps(names+[str((R/'sync-files_v003.json').relative_to(root)).replace('\\','/')],indent=2))
if len(sys.argv)>1:
    dst=Path(sys.argv[1]).resolve();assert (dst/'.git').exists()
    for name in json.loads((R/'sync-files_v003.json').read_text()):
        target=dst/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((root/name).read_bytes())
print(json.dumps({'files_for_sync':len(names)+1,'artifact_count':len(paths),'render_seconds':manifest['render_seconds'],'links_verified':len(links),'candidate_scene_hash':verify['scene_sha256']},indent=2))
