import hashlib,json,shutil
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];recovery=Path('D:/MIT-ECCO-Render-Recovery/S05-v018-Previs')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
media=json.loads((B/'Records/media-verification.json').read_text());geometry=json.loads((B/'Records/geometry-verification.json').read_text());supply=json.loads((B/'Records/supply-geometry-verification.json').read_text());sources=json.loads((B/'Records/source-geometry-verification.json').read_text())
assert media['all_frames_decoded'] and media['all_frames_strictly_below_5s'] and geometry['failure_count']==0 and supply['failure_count']==0
files=[B/'Scenes/S05_full-cinematic_v018.blend',B/'Previews/S05_full-cinematic_v018.mp4',ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend']
rows=[]
for p in files:
 q=recovery/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True)
 if not q.exists():shutil.copy2(p,q)
 assert sha(p)==sha(q)
 rows.append({'source':str(p),'backup':str(q),'sha256':sha(p),'bytes':p.stat().st_size})
(B/'Records/local-recovery.json').write_text(json.dumps({'same_machine_backup_only':True,'files':rows},indent=2))
refs=[
 'Interaction-Proof_v017/Scenes/S05_rich-amber_v017.blend',
 'Interaction-Proof_v010/Scenes/S05_combined-interaction_v010.blend']
manifest={'candidate':rows[0],'video':rows[1],'shared_dependency':rows[2],'approved_and_comparison_sources':[{'path':str(B.parent/r),'sha256':sha(B.parent/r)} for r in refs],'authorizing_handoff':'Records/owner-production-handoff.txt','live_work_read_revision':701,'live_work_context':'T43 done, T48 review. This directly owner-authorized previs has no separate live ticket; no archived ticket resumed or ticket lifecycle status changed.','frame_cache':'D:/MIT-ECCO-Render-Recovery/S05-v018-RenderCache/Frames','source_limits':['O07 certified stage-face and pin/box mapping unresolved','2.400m CAD retained; not rescaled to brochure nominal2.25m','Existing provisional presentation caps/plates preserved','Illustrative trajectories and advection, not CFD or measured performance'],'reference_records':['04-Production/Records/Tasks/T-048/source-map_v002.md','04-Production/Shared/Assets/Hydraulics/README_v002.md','04-Production/Records/Tasks/T-010/hydraulic-register_v001.md','04-Production/Records/Tasks/T-043/shared-direction_v001.md','03-Context/01_Foundation/02-ENGINEERING_BASELINE.md','03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md','03-Context/02_Storyboard/V2/ECCO_Section_05_Hydraulic_Padlet/PADLET_CAPTIONS.txt','03-Context/02_Storyboard/V3/ECCO_Section_05_Cinematic_Rich_Direction_Package/DIRECTOR_SHOT_ARCHITECTURE_DETAILED.md']}
(B/'Records/asset-manifest.json').write_text(json.dumps(manifest,indent=2))
total=media['total_frame_render_seconds'];elapsed=media['elapsed_first_to_last_frame_seconds']
report=f'''# S05 v018 — Full cinematic previs

Owner-authorized low-cost Section 5 integration, 23 October 2026. **Ready for owner review; not self-approved.** The 18-second section uses approved v017 as its visual foundation and v010 as comparison context. Previous proofs and shared masters remain intact.

## Delivery

- `Previews/S05_full-cinematic_v018.mp4` — 18 seconds, 432 frames, 24 fps, 1280 x 720.
- `Scenes/S05_full-cinematic_v018.blend` — editable, one scene with the three timed compositions and relative source link.
- `Previews/chronological-contact-sheet.jpg` — 22 chronological decoded frames, including both cut boundaries.
- `Previews/entry.png`, `interaction.png`, `diffuser.png`, `integrated.png` — representative decoded movie frames.
- `Previews/review.html` — local playback page.

## Actual sequence

| Local time | Image and purpose |
|---|---|
| 0–5 s | Oblique lower-body framing establishes fixed cut formation, annular fluid and cuttings; camera gently advances toward the lower raised region. |
| 5–12 s | Motivated cut into the twisted-pad close-up; very small upward drift. Original v017 fragment movement occupies frames151–246 at its original rate, with context before and transport afterward. |
| 12–18 s | Follow into the upper working region, then pull back to show the connected hydraulic body. All three regions continue operating. |

The fluid retains v017 amber appearance, long tapered trails and independent world-based advection. Matte warm-grey/earth mineral materials replace the saturated fragment color. Three persistent groups of three source-shaped rocks provide transport continuity. The wisp field is extended longitudinally so the final wide view still has incoming flow. The tool rotates as one assembly; there is no axial tool translation or animated cutaway.

## Render timing

- Mean complete render-to-file time: **{media['render_mean_seconds']:.3f} seconds/frame**.
- Slowest delivered frame: **{media['render_max_seconds']:.3f} seconds**.
- Sum of all 432 frame-render times: **{total:.1f} seconds ({total/60:.2f} minutes)**.
- Elapsed span from first-frame start to last-frame completion: **{elapsed:.1f} seconds ({elapsed/60:.2f} minutes)**, including pauses for verification and the incoming-trail extension. Encoding is excluded.
- EEVEE, 6 samples, 1280 x720. All frame writes strictly below five seconds. `Records/benchmark.json`, `post-supply-benchmark.json` and `render-timings.json` retain evidence.

## Geometry and source verification

Actual 2.400 m hardware and 0.155575 m hole radius preserved. Shared source and v017 hashes unchanged. All nine fragments and seventy finite wisp meshes checked across integer and half-frame times, with no sampled steel/wall intersections; fragment-pair checks also pass. Minimum fragment clearance: {geometry['min_clearance_m']['rock_steel']*1000:.3f} mm to steel and {geometry['min_clearance_m']['rock_wall']*1000:.3f} mm to wall. Full finite fluid boundary has no steel-surface intersection; its cylindrical outside margin is1 mm. Geometry checks do not validate a fluid simulation or every unsampled instant.

The first integration check exposed a discontinuity in the extended particle paths. The approved core was re-evaluated with its source collection enabled; globally connected safe passage candidates replaced the discontinuous added motion. The failed check remains labeled as history. The final incoming-trail extension was separately verified. It lies outside the earlier rendered views; frames1/120/198/240 were re-rendered and pixel-identical.

## Meaning and limits

Strengths to review: the camera first provides surroundings, then gives the pad interaction sustained attention, and ends by reconnecting the body regions. Warm matte cuttings are distinct from amber fluid, and the same fragments persist through the mechanism. Geometry and screen direction stay coherent through the cuts.

Remaining interpretation: the lower/middle/upper windows follow inspected T48 morphology, not certified accelerator/twisted-pad/diffuser face boundaries. No precise pin/box identity has been independently resolved. The diffuser is represented by continued, less-curved downstream flow; pressure recovery is an intended design role, not a computed field. The acceleration beat is qualitative constriction/path change, not a calibrated velocity claim. The wider ending naturally makes individual cuttings less prominent. Owner review must judge whether those three meanings read clearly at normal playback size; visual attractiveness and engineering verification are separate.

Rendering remains inexpensive previs, including visible low-sample grain. No final finishing, client publication, full-film assembly or narration edit was performed.

## Editorial and continuation

Provisional film position0:58–1:16 adds six seconds against the old0:58–1:10 allocation. Sections6/7 and narration were not retimed. Radzi owns that assembly decision. The existing S05-A/B/C contracts contain actual implementation and this editorial conflict; no competing direction brief was created.

## Storage and publication

Native, MP4 and exact shared dependency have hash-matching same-machine copies under `D:/MIT-ECCO-Render-Recovery/S05-v018-Previs/`, preserving relative folder structure. This is not offsite backup. Heavy media stays local. Frame cache is on D to preserve C free space. `Records/asset-manifest.json` and `local-recovery.json` identify the files. Only scoped scripts, contracts, reports, verification records and selected stills are published; exact Git synchronization is recorded in `Records/sync-verification.json` after push.
'''
(B/'README.md').write_text(report,encoding='utf-8');(B/'Records/report.md').write_text(report,encoding='utf-8')
print(json.dumps({'native_sha256':rows[0]['sha256'],'verified_recovery_files':len(rows),'render_mean_seconds':media['render_mean_seconds'],'render_max_seconds':media['render_max_seconds'],'render_total_seconds':total,'elapsed_span_seconds':elapsed}))
