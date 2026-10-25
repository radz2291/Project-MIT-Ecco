from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[1];R=B.parents[3];d=json.loads((B/'Records/delivery.json').read_text());v=json.loads((B/'Records/verification.json').read_text())
new=[x for x in json.loads((B/'Records/render-timings.json').read_text()) if not x.get('reused_from')]
report=f'''# S07 v006 — impact pullback ending

Status: revised ending awaiting owner review. Direct owner feedback accepted the v005 direction and requested a stronger near-to-far pullback in the final shot. Shots 1 and 2 are preserved exactly; no whole-film or client approval inferred.

## Change

Only frames 121–192 change. Shot 3 starts close to the product with the camera already retreating at constant speed for its first eight frames. The retreat then slows smoothly into a centered complete-product composition, retaining a gentle drift through the fade. There is no dead start. Camera distance at the established pose is about {v['third_shot_camera_retreat_ratio']:.2f} times its entry distance. This is an illustrative camera-composition control, not an engineering value.

The three-shot edit and eight-second duration remain. No logo, closing text or opening fade. Final black remains at frame 190. Product geometry and hardware are stationary; no product spin was introduced.

## Preservation and verification

First 120 camera records, evaluated positions/orientations and rendered image hashes match v005. These images are reused exactly. Revised source opens successfully with packed dependencies and no external libraries. Source mesh vertices/topology and all-frame hardware matrices match the canonical source. v005 native, canonical source and approved S06 artifacts retain their hashes. Dimensions, materials, lighting and existing provisional-cover/source-length limitations remain unchanged.

Third-shot entry has nonzero constant velocity; camera distance increases throughout the retreat. Final drift is {v['hero_drift_speed_fraction_of_entry']*100:.1f}% of entry translation speed. Final whole-product framing remains centered and inside the image. Cut interpolation, no branding, direct product entry and fade endpoint verified. Complete edit, boundary preview and individual clips decode without errors. Executor inspected cut and pullback frames; owner playback review remains pending.

## Rendering and handoff

Only 72 revised frames rendered after passing representative benchmarks. New rendering: {d['new_render_seconds']:.1f} seconds, average {d['new_render_seconds']/72:.2f} seconds/frame, maximum {max(x['seconds'] for x in new):.2f} seconds. Every revised and reused complete frame is below five seconds. 120 approved images reused. Eevee 32 samples, 1280×720, 24 fps. No expensive finishing.

Media and source links: ../README.md. Full edit plus separate shot clips supplied. Native/media local only. Hash-verified same-machine recovery: D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v006. Not an off-machine backup. Scripts, contracts and verification records are published to the established repository; exact remote parity is recorded in sync-verification.json. Owner retains final logo, audio and whole-film assembly.
'''
(B/'Records/production-report.md').write_text(report,encoding='utf-8')
task=R/'04-Production/Records/Tasks/S07-v006-Revision';task.mkdir(parents=True,exist_ok=True);(task/'report.md').write_text('# S07 v006 — review handoff\n\n[Production report](../../../Shots/S07/Sequence_v006/Records/production-report.md) and [review media](../../../Shots/S07/Sequence_v006/README.md).\n',encoding='utf-8')
backup=Path('D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v006');manifest=[]
for p in B.rglob('*'):
 if not p.is_file() or 'Cache' in p.relative_to(B).parts or p.suffix in ('.log','.blend1') or p.name in ('asset-manifest.json','recovery-verification.json','sync-verification.json'):continue
 rel=p.relative_to(B);dst=backup/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==hashlib.sha256(dst.read_bytes()).hexdigest();manifest.append({'path':rel.as_posix(),'sha256':sha,'bytes':p.stat().st_size})
for name,data in [('asset-manifest.json',manifest),('recovery-verification.json',{'recovery_root':str(backup),'files_verified':len(manifest),'same_machine_only':True,'cache_included':False})]:
 (B/'Records'/name).write_text(json.dumps(data,indent=2));shutil.copy2(B/'Records'/name,backup/'Records'/name)
print('PACKAGED',len(manifest))
