from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parents[1];R=B.parents[3]
delivery=json.loads((B/'Records/delivery.json').read_text());v=json.loads((B/'Records/verification.json').read_text())
assert v['saved_native_reopened'] and delivery['all_complete_frames_under_five_seconds']
report=f'''# S07 v001 — complete cinematic previs

Status: **Ready for owner review**, 25 October 2026. Direct owner full-production handoff; no new approval cycle or isolated proof deliverable. This report does not record acceptance of the new animation.

## Delivered

- `Previews/S07_Monumental-Precision_v001.mp4` — 8 seconds, 192 frames, 24 fps, 1280×720.
- `Scenes/S07_Monumental-Precision_v001.blend` — self-contained editable source, packed source plate and font, editable camera/focus/light/material/compositor controls.
- `Previews/S07_final-product-hero_v001.png` — representative complete-product closing frame.
- `Previews/S06-to-S07_transition_v001.mp4` — the last two seconds of the actual approved S06 movie followed by the complete S07 candidate, 10 seconds total. This is the requested boundary preview, not full-film assembly.
- `S07 EDITABLE BRANDING` — independent native text objects for `ECCO ENP3` and `MIT LOGO`. Select `MIT logo placeholder` to replace it later. No official logo was recreated.

## What happens

The approved S06 laptop endpoint softens and dims into an intimate view of the source ENP3 housing. A continuous camera glide follows the sculpted pads, then retreats into a complete-product diagonal composition. The product itself remains stationary. The camera is still from frame 146; both labels are fully present from frame 162 through 192. Capability effects are omitted to keep the instrument dominant.

The opening is an editorial dissolve using S06's actual rendered endpoint. It is color-managed within this new scene; it is not a claim of a physical camera connection, live transmission or a matching measured dataset. The source S06 sequence and all earlier work remain intact.

## Checks

- Source master file hash unchanged; all ten visible source meshes retain exact vertices/topology and world transforms. All 192 frames checked for stationary hardware.
- Saved Blender source reopened successfully. No linked libraries or unpacked image/font dependencies.
- Complete product fits inside the final frame with reserved branding space. Camera stays outside the source hardware envelope. Final camera hold verified.
- All 192 S07 frames and all 240 transition-preview frames fully decoded without errors.
- Executor inspected entry, detail, pullback, typography, final framing and dense movement frame sequences. This is self-review, not a cold-viewer comprehension study or engineering/client acceptance.

## Render cost

Eevee, 32 samples, full 1280×720 review resolution. Representative pre-batch benchmark maximum: {v['benchmark_max_seconds']:.2f} seconds.

Completed render average: **{delivery['render_average_seconds']:.2f} seconds/frame**. Maximum: **{delivery['render_max_seconds']:.2f} seconds/frame**. Total 192-frame render: **{delivery['render_total_seconds']:.1f} seconds ({delivery['render_total_seconds']/60:.2f} minutes)**. Encoding: {delivery['encode_seconds']:.1f} seconds. These exclude scene construction and internal test frames. Every complete production frame remained strictly below five seconds.

## Provenance and remaining limits

Canonical input is `04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend`. Its imported 2.400 m length, existing unit conversion and removable temporary closure geometry remain unchanged. Detailed closure/sensor authority and the brochure's nominal-length difference remain existing limitations. Satin materials and studio lighting are cinematic interpretation, not a claim of actual alloy or official finish. No new product feature, measurement value or promotional claim was added.

Actual storyboard revision 14 and live Work revision 747 were read. There is no matching S07 task in that workspace; no number/run/status was invented. The direct handoff is the execution authority. Historical shot contracts and stages were not reused as current gates. One new `Sequence_v001` implementation contains S07-A/B/C. Publishing base is `2ab727bb815d92d8dadadda6c88217ee407b583e`; exact new remote parity is recorded in ignored `Records/sync-verification.json` after publishing.

## Retention and handoff

Recovery: `D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v001`. This is a hash-verified copy on the same machine, not off-machine backup. Heavy native/media/input files stay local; permitted scripts and text/JSON evidence are synchronized to the established project repository. The native scene is self-contained; regeneration scripts retain the canonical project-relative input locations. Unrelated Git changes and previous scenes are preserved. Internal frame caches and Blender save backups remain local and are not alternative review candidates.

Stop at owner review of this full eight-second candidate. Radzi handles actual MIT logo replacement, narration/music timing, whole-film assembly and client delivery. No final-resolution finishing or client publication has been initiated.
'''
(B/'Records/production-report.md').write_text(report,encoding='utf-8')
task=R/'04-Production/Records/Tasks/S07-v001-Production';task.mkdir(parents=True,exist_ok=True)
(task/'report.md').write_text('# S07 v001 — production review handoff\n\nDirect owner authorization; no matching numbered Work ticket. See the [canonical production report](../../../Shots/S07/Sequence_v001/Records/production-report.md) and [delivery index](../../../Shots/S07/Sequence_v001/README.md). Status: owner review pending.\n',encoding='utf-8')
backup=Path('D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v001');manifest=[]
for p in sorted(B.rglob('*')):
 if not p.is_file() or 'Cache' in p.relative_to(B).parts or p.suffix in ('.log','.blend1') or p.name in ('asset-manifest.json','recovery-verification.json','sync-verification.json'):continue
 rel=p.relative_to(B);dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==hashlib.sha256(dest.read_bytes()).hexdigest()
 manifest.append({'path':rel.as_posix(),'bytes':p.stat().st_size,'sha256':sha})
source=R/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend';dest=backup/'Inputs/ECCO_film_v002.blend';dest.parent.mkdir(exist_ok=True);shutil.copy2(source,dest)
assert hashlib.sha256(source.read_bytes()).hexdigest()==hashlib.sha256(dest.read_bytes()).hexdigest()
(B/'Records/asset-manifest.json').write_text(json.dumps({'files':manifest,'input_source':str(source),'input_recovery':str(dest),'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest()},indent=2))
(B/'Records/recovery-verification.json').write_text(json.dumps({'recovery_root':str(backup),'files_verified':len(manifest),'source_master_copy_verified':True,'same_machine_only':True,'raw_cache_included':False},indent=2))
for name in ('asset-manifest.json','recovery-verification.json'):shutil.copy2(B/'Records'/name,backup/'Records'/name)
print('PACKAGED AND RECOVERED',len(manifest))
