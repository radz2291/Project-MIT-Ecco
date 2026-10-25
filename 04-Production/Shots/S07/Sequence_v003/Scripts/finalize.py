from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[1];R=B.parents[3]
d=json.loads((B/'Records/delivery.json').read_text());v=json.loads((B/'Records/verification.json').read_text())
report=f'''# S07 v003 — continuous beauty reveal

Status: owner review pending. Direct owner authorization; no new Work ticket invented.

## Result

The previous frame-61 cut is replaced by a continuous eased camera arc between the two detail perspectives. The camera retreats to a centered full-product view, holds, then fades the whole image to black. Both MIT LOGO and ECCO ENP3 text objects are removed. Owner adds a separate logo frame in post. Eight seconds, 192 frames at 24 fps, 1280×720.

The S06 laptop editorial dissolve remains; the product-camera portion is one continuous take. Source geometry, dimensions, stationary hardware, materials and lighting remain unchanged. Previous v001/v002 and approved S06 artifacts remain intact. Source-length and provisional-cap limitations documented in v001 carry forward.

## Verification

Saved source reopened. Exact mesh vertices/topology and all-frame source matrices verified. Packed images/fonts and no external libraries. Full-product framing is centered and inside frame. No text objects remain. Fade reaches black at frame 190; native PNGs have at most one level of output dither. Encoding explicitly pins the final three frames to black. S07 video decoded all 192 frames and boundary preview all 240 frames without errors. Executor checks cover timed frames and camera trajectory; owner playback review remains pending.

## Cost

All 192 frames newly rendered: {d['render_total_seconds']:.1f} seconds total, {d['render_average_seconds']:.2f} seconds/frame average, {d['render_max_seconds']:.2f} seconds maximum. Representative benchmarks passed before batch. Every complete frame is below five seconds. Encoding took {d['encode_seconds']:.1f} seconds. No expensive finishing.

## Delivery and preservation

Review media and editable native are linked in ../README.md. Heavy files stay local. Hash-verified same-machine recovery: D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v003. This is not an off-machine backup. Scripts, contracts and verification records are published to the established project Git repository; exact remote parity is recorded in sync-verification.json. No engineering certification, client approval, audio finishing or film assembly is claimed.
'''
(B/'Records/production-report.md').write_text(report,encoding='utf-8')
task=R/'04-Production/Records/Tasks/S07-v003-Revision';task.mkdir(parents=True,exist_ok=True)
(task/'report.md').write_text('# S07 v003 — review handoff\n\nDirect owner revision. [Production report](../../../Shots/S07/Sequence_v003/Records/production-report.md) and [review delivery](../../../Shots/S07/Sequence_v003/README.md).\n',encoding='utf-8')
backup=Path('D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v003');manifest=[]
for p in B.rglob('*'):
 if not p.is_file() or 'Cache' in p.relative_to(B).parts or p.suffix in ('.log','.blend1') or p.name in ('asset-manifest.json','recovery-verification.json','sync-verification.json'):continue
 rel=p.relative_to(B);dst=backup/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==hashlib.sha256(dst.read_bytes()).hexdigest();manifest.append({'path':rel.as_posix(),'sha256':sha,'bytes':p.stat().st_size})
for name,data in [('asset-manifest.json',manifest),('recovery-verification.json',{'recovery_root':str(backup),'files_verified':len(manifest),'same_machine_only':True,'cache_included':False})]:
 (B/'Records'/name).write_text(json.dumps(data,indent=2));shutil.copy2(B/'Records'/name,backup/'Records'/name)
print('PACKAGED',len(manifest))
