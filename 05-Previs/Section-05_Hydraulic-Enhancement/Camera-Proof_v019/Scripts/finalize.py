import json,hashlib,shutil
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];R=B/'Records'
media=json.loads((R/'media-verification.json').read_text());check=json.loads((R/'camera-verification.json').read_text());content=json.loads((R/'content-preservation.json').read_text());baseline=json.loads((R/'source-baseline.json').read_text())
assert content['equal'] and not check['failures'] and media['decoded_frames']==432 and media['all_under_5_seconds']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
native=B/'Scenes/S05_camera-direction_v019.blend';video=B/'Previews/S05_camera-motion_v019.mp4';shared=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
assert sha(Path(baseline['source']))==baseline['source_sha256']
recovery=Path('D:/MIT-ECCO-Render-Recovery/S05-v019-Previs');backup=[]
for p in [native,video,shared]:
 q=recovery/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True)
 if not q.exists():shutil.copy2(p,q)
 assert sha(p)==sha(q);backup.append({'source':str(p),'backup':str(q),'sha256':sha(p),'bytes':p.stat().st_size})
manifest={'version':'v019 camera direction proof','source_v018':baseline['source'],'source_v018_sha256':baseline['source_sha256'],'files':backup,'frame_cache':'D:/MIT-ECCO-Render-Recovery/S05-v019-RenderCache/Frames','same_machine_backup_only':True,'source_geometry_length_m':2.4000000953674316,'borehole_radius_m':.155575,'source_mapping_limit':'O07 functional stage-face and pin/box mapping remains illustrative','live_work_revision':701,'task_authority':'Direct owner v019 camera proof handoff; no new ticket or lifecycle change','review_status':'Owner review pending'}
(R/'asset-manifest.json').write_text(json.dumps(manifest,indent=2))
old=R/'fresh-source-comparison.json'
if old.exists():
 d=json.loads(old.read_text());d['diagnostic_status']='Historical overbroad hash comparison: included camera-parented label world transforms and orphan data. Superseded by content-preservation.json comparing bound content and camera-child local transforms.';old.write_text(json.dumps(d,indent=2))
report=f'''# S05 v019 — Camera-direction proof

The full 18-second camera proof is ready for owner review. It preserves v018 hydraulic geometry, animation and appearance. This is a bounded camera test, not a new finished production render.

## Deliverables

- `Previews/S05_camera-motion_v019.mp4` — 18 seconds, 432 frames, 24 fps, 960 x 540 lightweight EEVEE playblast.
- `Previews/A_arrival.png`, `B_arrival.png`, `C_arrival.png` — three authored 1280 x 720 compositions.
- `Previews/three-arrivals.jpg` — the three views together.
- `Previews/motion-contact-sheet.jpg` — chronological frames covering travel, arrivals and the cut.
- `Scenes/S05_camera-direction_v019.blend` — editable source, camera baked at each frame; original flow controls retained.
- `Records/camera-score.md` — purpose, timing, taste application and AI Director self-critique.

## What changed

A looks upward along the lower body and rises into a nearly upright sculptural arrival. B cuts closer, opens the pad flank through a short partial arc, then slows down for the existing fragment interaction. C continuously follows the flow into the upper region, then retreats and changes its gaze to reconnect the working body. The final camera holds for about 1.3 seconds while circulation and hardware rotation continue.

The final view deliberately crops the remote shaft ends and the existing finite fluid-volume boundaries. It shows the connected hydraulic working regions, not a complete dimensional catalogue view. A more elevated test exposed an amber end disc; that camera was rejected without altering fluid geometry.

## Preservation and verification

Reopened source/candidate comparison matches **{content['items_compared']} content entries**: scene meshes and shape keys, bound hydraulic animation, materials/node values and links, object visibility and transforms at five frames. Legacy hidden camera-parented labels are compared in their local coordinates. No new particle system, fluid simulation, material, light, hardware or environment geometry was introduced. The v018 file SHA remains unchanged.

All 432 camera samples pass the center-target wall-occlusion, camera/solid separation and upward screen-direction checks. Minimum camera-to-solid distance is {check['min_camera_solid_distance_m']:.3f} m. At least one original core fragment is geometrically visible in all 82 frames of the principal observation interval. These tests support visibility and continuity; they do not establish audience comprehension. Existing v018 sampled flow/solid clearance evidence remains applicable because the bound scene content is unchanged.

The first broad hash check was too inclusive: it compared the world transforms of hidden labels parented to the camera and unused datablocks. The corrected bound-content comparison distinguishes those expected camera-dependent differences from changes to the hydraulic scene. The diagnostic history is retained.

## Performance

Three arrivals and transition/entry stills were benchmarked before the playblast. Playblast settings: EEVEE 4 samples, 960 x 540. Arrival stills: EEVEE 6 samples, 1280 x 720. No material refinements.

- Mean playblast frame: **{media['mean_seconds']:.3f} seconds**.
- Slowest playblast frame: **{media['max_seconds']:.3f} seconds**.
- Aggregate 432-frame render time: **{media['total_render_seconds']:.1f} seconds**.
- First-to-last render span: **{media['elapsed_batch_seconds']:.1f} seconds**, including tool/chunk overhead; excludes encoding.
- All 432 frames decoded from the MP4 and every delivered frame rendered in less than 5 seconds.

## Self-review and limits

The inspected arrival stills now have distinct visual roles: perspective-led lower-body arrival, close pad/passage observation and broad integrated composition. The central mechanism gets a quiet recognition interval and the ending settles. This addresses v018's repeated framing approach through camera direction alone.

Normal-speed automated visual playback could not be completed: both browser and desktop playback tools failed to initialize with a missing kernel-assets path. The encoded sequence and chronological stills are verified; owner viewing remains necessary to judge the cut, arc pace and final reveal. No independent viewer acceptance is claimed.

Hydraulic acceleration and diffuser behavior remain qualitative. Exact functional stage-face mapping is still unresolved. Existing occasional wisp/metal visual alignment and low-sample grain were not altered during this camera test. The final view reduces individual fragment size. The film allocation remains provisionally 58–76 seconds; Sections 6/7 and narration were not retimed.

## Records and storage

Owner authority: `Records/owner-direction.txt`. Existing S05-A/B/C scene contracts record this proposed camera revision without marking it accepted. Live Work was read at revision 701: T43 done, T48 review. No archived work resumed.

Native scene, MP4 and exact shared dependency have hash-matching same-machine copies under `D:/MIT-ECCO-Render-Recovery/S05-v019-Previs/`; this is not offsite backup. Heavy media remains local. Reports/scripts/selected review stills are scoped for Git publication; exact publication evidence is recorded separately in `Records/sync-verification.json`.
'''
(B/'README.md').write_text(report,encoding='utf-8');(R/'report.md').write_text(report,encoding='utf-8')
for part in 'ABC':
 p=ROOT/f'04-Production/Shots/S05/S05-{part}/direction.md';text=p.read_text(encoding='utf-8');heading=text.splitlines()[0]
 entry=f'''\n## v019 camera-direction proof — owner review pending\n\nOwner's 23 October camera revision preserves v018 geometry, shaders and hydraulic timing. Candidate: `05-Previs/Section-05_Hydraulic-Enhancement/Camera-Proof_v019/Scenes/S05_camera-direction_v019.blend`; proof MP4 is 18 seconds at 960 x 540/24fps, with 720p arrival stills. This records a tested proposal, not production-camera approval.\n\n'''
 descriptions={'A':'A rises along the annulus from a lower, lengthwise view and settles into an almost upright lower-region composition at frame84. Small residual motion through frame120. Camera-only parallax exposes near shaft, amber passage and distant raised geometry.','B':'A deliberate cut at frame121 enters closer; a partial arc opens the pad flank by frame165. Slow drift through frame246 leaves the original mechanism readable. The camera then follows outgoing fluid continuously into C.','C':'Continuous lift reaches upper detail at frame330, then a retreat with a change of gaze reconnects the working regions by frame402. Camera holds to frame432. Shaft ends and fluid end caps stay outside the intended working-body framing.'}
 entry+=descriptions[part]+'\n\nCamera score, actual transforms, bound-content preservation and clipping/screen-direction checks are in `Camera-Proof_v019/Records/`. E002–E004 guide distinct arrivals and purposeful travel; no studio preset copied. Exact hydraulic stage mapping remains illustrative. Normal-speed visual acceptance awaits owner review; no final finishing or film assembly released.\n\n---\n'
 assert '## v019 camera-direction proof' not in text
 p.write_text(heading+'\n'+entry+text[len(heading)+1:],encoding='utf-8')
print(json.dumps({'ready_for_review':True,'files_backed_up':len(backup),'mean_seconds':media['mean_seconds'],'max_seconds':media['max_seconds'],'total_render_seconds':media['total_render_seconds']}))
