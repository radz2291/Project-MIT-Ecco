"""Check review links/hashes and explicit publication list, excluding heavy media."""
from pathlib import Path
import json,hashlib,re
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';T=R/'04-Production/Records/Tasks/T-027';E=T/'Evidence';P=B/'Previews/MotionFull_v006d';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
qa=json.loads((E/'playback_qa_v006d.json').read_text());verification=json.loads((E/'verification_motion-full_v006d.json').read_text());links=[]
for link in re.findall(r'\]\(([^)]+)\)',(T/'report.md').read_text(encoding='utf-8')):
    if '://' in link:continue
    target=(T/link.split('#')[0]).resolve();assert target.exists() or target==E/'closure_v006d.json',target;links.append(target.relative_to(R).as_posix())
for out in qa['outputs']:assert sha(R/out['path'])==out['sha256'],out['path']
opening=[]
for f in range(1,337):
    a=Image.open(B/f'Previews/MotionProof_v005b/Frames/frame_{f:04d}.png').convert('RGB');z=Image.open(P/f'Frames/frame_{f:04d}.png').convert('RGB');ok=ImageChops.difference(a,z).getbbox() is None;assert ok,f;opening.append(f)
paths=[B/'B202-M_scene-direction_v001.md',T/'report.md',T/'report_v005b.md']
paths += [B/'Scripts'/name for name in ('build_motion_full_v006.py','build_motion_full_v006b.py','build_motion_full_v006c.py','build_motion_full_v006d.py','verify_motion_full_v006d.py','assemble_render_full_v006d.py','package_motion_full_v006d.py','close_motion_full_v006d.py')]
paths += [E/name for name in ('replay_manifest_v006d.json','verification_motion-full_v006d.json','playback_qa_v006d.json','render_provenance_v006d.json','closure_v006d.json','sync_files_v006d.json')]
paths += [P/'B202-M_review-sheet_v006d.jpg',P/'review_v006d.html']
paths += [P/f'decoded_{f:04d}.jpg' for f in (168,384,528,624,720)]
paths += [P/f'chronological_{i:02d}_v006d.jpg' for i in range(1,6)]
result={'status':'PASS','report_local_links':len(links),'linked_paths':links,'output_hashes_verified':len(qa['outputs']),'accepted_opening_render_pixel_identical_frames':len(opening),'saved_scene_checks':verification['check_count'],'decoded_video_frames':qa['decoded_frames'],'agent_visual_inspection':{'exact_version':'v006d','key_frames':qa['key_frames'],'chronological_sheets':[f'chronological_{i:02d}_v006d.jpg' for i in range(1,6)],'findings':'Expected/actual opening preserved pixel-for-pixel. Explicit cuts separate completed examples. Tight camera approach exposes true small deficit. Labels fit. Fixed-range warm variation remains subtle and unexaggerated. No blank/corrupt frames. Sampled chronological inspection, not independent cold-viewer evidence.'},'human_comprehension':'Pending actual uninstructed non-specialist response; no outside viewer contacted.','MIT_technical_review':'Pending calibration/datum/processing/interpretation; source integrity checks only.','media_status':'Native/video/raw frames local ignored; not uploaded/backed up by Git.','publication_scope':'Explicit B202/T027 files only; unrelated B201/T007 excluded.'}
(E/'closure_v006d.json').write_text(json.dumps(result,indent=2));(E/'sync_files_v006d.json').write_text(json.dumps([p.relative_to(R).as_posix() for p in paths],indent=2));assert all(p.exists() for p in paths)
print(json.dumps({'status':'PASS','links':len(links),'hashes':len(qa['outputs']),'opening_pixel_identical_frames':len(opening),'checks':verification['check_count'],'sync_files':len(paths)}))
