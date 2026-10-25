from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[1];R=B.parents[3]
d=json.loads((B/'Records/delivery.json').read_text());v=json.loads((B/'Records/verification.json').read_text())
report=f'''# S07 v004 — rear-face traverse and collar beauty reveal

Status: owner review pending. Direct owner revision; no invented Work ticket.

## Change and direction

The previous second close-up stayed around the same pads. v004 moves over the shoulder to the rear face, travels past other actual body details and settles on the end collar before retreating to the centered product. AI Director guidance informs the meaningful arrival and parallax during travel. The camera remains continuous. Projected product-axis framing avoids a horizon flip while crossing over the top. First 36 camera frames are preserved exactly. The wide view now comes from the rear side to continue that journey.

Eight seconds, 192 frames, 24 fps, 1280×720. No logo or closing text. Fade at frames 164–190 retained; the owner adds a separate logo frame in post. S06 laptop editorial dissolve remains, so the continuous physical take refers to the product-camera journey.

## Preservation and verification

Actual source meshes/topology and all-frame transforms verified; stationary hardware, dimensions, lighting and materials unchanged. Existing source-length and provisional-cover limits remain as recorded in v001. The saved native reopens with packed dependencies and no external libraries. Earlier v003 native, canonical source and approved S06 artifacts retain their hashes. All previous versions retained.

Camera reaches the positive-Y rear face and collar region. Largest sampled translation step: {v['maximum_camera_step_m']:.4f} m/frame; angular step: {v['maximum_angular_step_degrees']:.2f} degrees/frame. Camera radial clearance remains positive. These are animation diagnostics, not measured operating velocities. Final full-product bounds are centered and remain inside frame. No text objects remain. Native fade reaches black; one-level output dither is removed by pinning the final three encoded frames to black.

S07 decoded 192 frames and S06 boundary preview decoded 240 frames without errors. Executor inspected timed frames for reveal, orientation and ending. Owner playback review remains pending; no cold-viewer, engineering or client acceptance is claimed.

## Rendering

All 192 frames newly rendered after representative benchmarks passed. Total {d['render_total_seconds']:.1f} seconds; average {d['render_average_seconds']:.2f} seconds/frame; maximum {d['render_max_seconds']:.2f} seconds/frame. Every complete frame below five seconds. Encoding {d['encode_seconds']:.1f} seconds. Eevee 32 samples; no expensive finishing.

## Handoff

Animation, native and still links are in ../README.md. Local recovery: D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v004. Hash verified on the same machine, not an off-machine backup. Heavy native/media stay local. Scripts/contracts/JSON evidence published to the established project repository, with exact parity in sync-verification.json. Stop at owner review. Final audio, logo insertion and film assembly belong to the owner.
'''
(B/'Records/production-report.md').write_text(report,encoding='utf-8')
task=R/'04-Production/Records/Tasks/S07-v004-Revision';task.mkdir(parents=True,exist_ok=True)
(task/'report.md').write_text('# S07 v004 — review handoff\n\nDirect owner revision. [Production report](../../../Shots/S07/Sequence_v004/Records/production-report.md) and [review media](../../../Shots/S07/Sequence_v004/README.md).\n',encoding='utf-8')
backup=Path('D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v004');manifest=[]
for p in B.rglob('*'):
 if not p.is_file() or 'Cache' in p.relative_to(B).parts or p.suffix in ('.log','.blend1') or p.name in ('asset-manifest.json','recovery-verification.json','sync-verification.json'):continue
 rel=p.relative_to(B);dst=backup/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==hashlib.sha256(dst.read_bytes()).hexdigest();manifest.append({'path':rel.as_posix(),'sha256':sha,'bytes':p.stat().st_size})
for name,data in [('asset-manifest.json',manifest),('recovery-verification.json',{'recovery_root':str(backup),'files_verified':len(manifest),'same_machine_only':True,'cache_included':False})]:
 (B/'Records'/name).write_text(json.dumps(data,indent=2));shutil.copy2(B/'Records'/name,backup/'Records'/name)
print('PACKAGED',len(manifest))
