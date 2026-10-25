from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[1];R=B.parents[3];d=json.loads((B/'Records/delivery.json').read_text());v=json.loads((B/'Records/verification.json').read_text());reuse=json.loads((B/'Records/reuse-verification.json').read_text())
report=f'''# S07 v002 — added beauty close-up

Status: owner review pending. Authority: direct request to add one beauty reveal close-up from a different perspective before the wide shot.

## Change

The original camera view is retained through frame 60. At frame 61 (2.5 seconds), a deliberate edit introduces a reverse three-quarter angle looking along the actual pads. That view glides gently through frame 94, then retreats into the original wide composition by frame 146. The closing camera hold and editable branding are unchanged. Duration remains eight seconds / 192 frames at 24 fps, 1280×720.

Only the camera, focus and invisible title placement within frames 61–145 changed. No hardware, dimensions, materials, light rig, source report imagery or timing of the final identity was changed. Product remains stationary. Previous v001 native/movie remain intact.

## Delivery

- `Previews/S07_Monumental-Precision_v002.mp4`
- `Scenes/S07_Monumental-Precision_v002.blend`
- `Previews/S07_second-beauty_v002.png`
- `Previews/S07_final-product-hero_v002.png`
- `Previews/S06-to-S07_transition_v002.mp4`

The Blender branding collection has independently editable `ECCO ENP3` and `MIT LOGO`; official branding is still the owner's replacement. All file images and fonts are packed.

## Verification and cost

Saved source reopened, exact source vertices/topology and all-frame hardware transforms checked. S06 approved artifacts and source master hashes unchanged. Reused opening/closing camera, focus and branding transforms match v001 exactly ({reuse['reused_frames']} frames). The 85 revised frames were newly rendered after representative benchmarks passed. Full S07 192-frame and transition-preview 240-frame decodes passed without errors. Executor inspected the additional angle, cut and pullback through timed frame sequences; owner playback review remains outstanding.

New rendering: {d['new_render_seconds']:.1f} seconds for 85 frames, average {d['new_render_seconds']/85:.2f} seconds/frame. Maximum complete-frame render across the delivered sequence: {d['render_max_seconds']:.2f} seconds, below the strict five-second cap. 107 unchanged frames were reused from verified v001. Encoding: {d['encode_seconds']:.1f} seconds. No expensive finishing performed.

## Source and handoff

Previous implementation: `Sequence_v001`, publishing base `676aa4a5a9dde94363c17d04821bd11fd67d35eb`. v002 is a separate implementation; previous directions and acceptance history are preserved. Original source-length and temporary-cap limitations remain as recorded in v001. No exact alloy, performance, engineering certification or client approval is implied.

Recovery location: `D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v002`, hash verified on the same machine. Heavy media/native files are local only. Scripts and text/JSON evidence are published to the established project repository; exact remote parity is recorded in `sync-verification.json`. This task has direct owner authorization, no invented Work ticket number. Stop at owner review; no whole-film assembly or client publication.
'''
(B/'Records/production-report.md').write_text(report,encoding='utf-8')
task=R/'04-Production/Records/Tasks/S07-v002-Revision';task.mkdir(parents=True,exist_ok=True);(task/'report.md').write_text('# S07 v002 — review handoff\n\nDirect owner revision. See [production report](../../../Shots/S07/Sequence_v002/Records/production-report.md) and [review delivery](../../../Shots/S07/Sequence_v002/README.md).\n',encoding='utf-8')
backup=Path('D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v002');manifest=[]
for p in B.rglob('*'):
 if not p.is_file() or 'Cache' in p.relative_to(B).parts or p.suffix in ('.log','.blend1') or p.name in ('asset-manifest.json','recovery-verification.json','sync-verification.json'):continue
 rel=p.relative_to(B);dst=backup/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==hashlib.sha256(dst.read_bytes()).hexdigest();manifest.append({'path':rel.as_posix(),'sha256':sha,'bytes':p.stat().st_size})
for name,data in [('asset-manifest.json',manifest),('recovery-verification.json',{'recovery_root':str(backup),'files_verified':len(manifest),'same_machine_only':True,'cache_included':False})]:
 (B/'Records'/name).write_text(json.dumps(data,indent=2));shutil.copy2(B/'Records'/name,backup/'Records'/name)
print('PACKAGED',len(manifest))
