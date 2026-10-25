"""Record the explicit 25 October owner approval and verify the selected handoff."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json,subprocess
B=Path(__file__).resolve().parents[1];P=B.parents[1]
recovery=Path('D:/MIT-ECCO-Render-Recovery/S06-Report-Recreation_v004')
now=datetime.now(timezone(timedelta(hours=8))).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
movie='Previews/S06_cinematic-study_v004_polished.mp4';native='Scenes/S06_cinematic-study_v004_polished.blend'
delivery=json.loads((B/'Records/polish-delivery.json').read_text());assert sha(B/movie)==delivery['movie_sha256']
artifacts=[]
for rel in [movie,native,'Data/story_field.npz']:
 p=B/rel;assert p.is_file() and (recovery/rel).is_file();h=sha(p);assert h==sha(recovery/rel)
 artifacts.append({'path':rel,'bytes':p.stat().st_size,'sha256':h,'recovery_sha256_matches':True})
assert sha(B/'Scenes/S06_cinematic-study_v004.blend')==json.loads((B/'Records/polish-build.json').read_text())['source_sha256']
assert 'POLISH VERIFIED' in (B/'Records/closure-native-verification.log').read_text()
ff=P/'Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
decoded=subprocess.run([str(ff),'-v','error','-i',str(B/movie),'-map','0:v:0','-f','framemd5','-'],capture_output=True,text=True)
assert decoded.returncode==0 and not decoded.stderr.strip()
rows=[l for l in decoded.stdout.splitlines() if l and not l.startswith('#')];assert len(rows)==288
timings=json.loads((B/'Records/polish-render-timings.json').read_text());assert len(timings)==288 and max(r['seconds'] for r in timings)<5
approval={'status':'Owner-approved S06 cinematic previs; closed','approval_date':'2026-10-25','timezone':'Asia/Kuala_Lumpur','owner_statement':'S6 is approved, pls do your closure and wrap.','selected_movie':movie,'selected_native':native,'implementation_commit':'2abde39be7ead179157afae2eda0d4663f1fe557','closure_verified_at':now,'artifacts':artifacts,'fresh_video_decode_frames':len(rows),'fresh_video_decode_errors':0,'saved_native_reopened_and_verified':True,'source_native_unchanged':True,'render_max_seconds':max(r['seconds'] for r in timings),'work_workspace_revision':747,'matching_work_ticket':None,'recovery_root':str(recovery),'recovery_type':'Hash-verified same-machine D-drive copy; not an off-machine backup','media_remote_upload':False,'scope':'Approval of this S06 previs; final film assembly and client delivery remain with Radzi. No engineering certification or calibrated field-data claim.'}
(B/'Records/closure-verification.json').write_text(json.dumps(approval,indent=2),encoding='utf-8')
(B/'Records/owner-approval_2026-10-25.md').write_text(f'''# S06 owner approval — 25 October 2026

**Status: Approved and selected for the S06 previs handoff.**

Owner instruction: “S6 is approved, pls do your closure and wrap.”

The instruction follows delivery of the polished v004 animation and applies to that exact candidate, not the earlier unpolished video.

- Selected movie: `{movie}`
- Selected editable native: `{native}`
- Movie SHA-256: `{artifacts[0]['sha256']}`
- Native SHA-256: `{artifacts[1]['sha256']}`
- Duration: 12 seconds; 288 frames; 24 fps; 1280 × 720.
- Implementation commit: `2abde39be7ead179157afae2eda0d4663f1fe557`.

Approval covers the complete S06 A→B→C previs and its transition refinement. This records owner acceptance, not independent engineering certification, calibrated measurements, client acceptance or completed film assembly. Radzi retains film assembly, audio, final timeline and client delivery. Earlier versions and shared masters remain preserved.
''',encoding='utf-8')
(B/'APPROVED_DELIVERY.md').write_text('''# S06 — approved previs handoff

Approved by the owner on **25 October 2026**. Use the **polished v004** candidate.

- [Approved 12-second video](Previews/S06_cinematic-study_v004_polished.mp4)
- [Approved editable Blender scene](Scenes/S06_cinematic-study_v004_polished.blend)
- [Transition review sheet](Previews/S06_polished-transition-review.jpg)
- [Approval record](Records/owner-approval_2026-10-25.md)
- [Closure report](Records/closure-report.md)

The Blender scene contains the camera, animation, geometry and packed font. `Data/story_field.npz` supports script regeneration; it is not required to play the saved scene. Geometry and amplitude remain separate illustrative channels, with no original report imagery or identifying measurements displayed.

Recovery copy: `D:/MIT-ECCO-Render-Recovery/S06-Report-Recreation_v004`. Media and native files are local only; the D-drive copy is on the same machine. Previous candidates remain available for history. No further S06 work is active; film assembly is with Radzi.
''',encoding='utf-8')
(B/'Records/closure-report.md').write_text(f'''# S06 v004 — approved previs closure

**Closed: 25 October 2026, Asia/Kuala_Lumpur. Owner approved the polished S06 previs.**

## Authority and selected output

Direct owner instruction: “S6 is approved, pls do your closure and wrap.” Stable local closure key: `S06-v004-Closure`. Live MIT ECCO Work was reread at revision 747 and has no matching S06 ticket; no ticket number or lifecycle run was invented and unrelated tickets were not changed. Implementation base: `2abde39be7ead179157afae2eda0d4663f1fe557`.

The selected handoff is the single continuous 12-second A→B→C polished v004 animation: contextual borehole reconstruction, unfolding geometry with independent amplitude, and recreated anonymous report on a laptop. The record supersedes pending-review wording in historical build/check evidence.

Local root: `{B.as_posix()}`.

| Deliverable | Relative path | Status |
|---|---|---|
| Selected video | `{movie}` | Owner approved |
| Editable scene | `{native}` | Reopened and verified |
| Entry point | `APPROVED_DELIVERY.md` | Selected-file handoff |
| Regeneration field | `Data/story_field.npz` | Local illustrative input |
| Approval | `Records/owner-approval_2026-10-25.md` | Exact owner instruction and hashes |

## Closure verification

- Selected movie hash matches the reviewed delivery; fresh FFmpeg decode confirms all 288 frames without errors.
- Saved native reopened in isolated Blender 5.2. Mesh positions/topology/colors, all 288 geometry/amplitude shape states and final camera match the preserved source constraints. No external image or linked-library dependencies; fonts packed.
- Selected movie, native and regeneration field match their D-drive recovery hashes. Source native remains unchanged. Exact hashes and current evidence are in `closure-verification.json`.
- 1280 × 720, 24 fps; average {delivery['mean_frame_seconds']:.2f} seconds/frame; maximum {delivery['maximum_frame_seconds']:.2f}. Retained-frame rendering: {delivery['render_seconds']:.2f} seconds. Total batch rendering including the steel-fade correction: {delivery['total_batch_render_seconds_including_steel_fade_repair']:.2f} seconds. Every final frame is under five seconds.
- These are agent self-checks plus explicit owner approval; they are not independent audience or engineering verification.

## Retention, recovery and synchronization

Prior proofs, the original v004 movie/native and source masters remain intact. Useful render caches and evidence stay in their existing labeled folders; no broad cleanup or deletion was performed. Recovery is `{recovery.as_posix()}`, a same-machine copy. Media/data/native files remain local and excluded from Git. Permitted scripts and text/JSON records are published to the established project repository; exact closure commit and remote parity are recorded in `sync-verification.json` after publication. The old V2 proposed shot inventory is historical and was not overwritten.

## Handoff and limits

No outstanding work remains for this approved S06 previs. Radzi owns film assembly, sound, narration, final timeline and client feedback. Any later change requires a new scoped instruction. This closure does not authorize final finishing, publication of restricted imagery, engineering certification or claims that the illustrative reconstruction is a calibrated client dataset.
''',encoding='utf-8')
readme=B/'README.md';t=readme.read_text(encoding='utf-8');start=t.index('**Current review candidate:**');end=t.index('\n',start)
t=t[:start]+'**Approved and closed — 25 October 2026.** The owner selected the polished v004 S06 previs. Start with [APPROVED_DELIVERY.md](APPROVED_DELIVERY.md) for the exact video, editable native, approval and closure records. Historical review wording below records earlier stages and is superseded by this approval.'+t[end:];readme.write_text(t,encoding='utf-8')
delivery['review']='Owner approved 2026-10-25; S06 previs closed';delivery['approval_record']='Records/owner-approval_2026-10-25.md';(B/'Records/polish-delivery.json').write_text(json.dumps(delivery,indent=2),encoding='utf-8')
task=P/'Records/Tasks/S06-v004-Closure';task.mkdir(parents=True,exist_ok=True)
(task/'report.md').write_text('''# S06 v004 closure — owner-authorized work

Status: **Owner approved and closed, 25 October 2026**.

Stable local key: `S06-v004-Closure`. There is no corresponding numbered Rolladice Work ticket at workspace revision 747; this folder records the directly authorized closure without inventing a ticket number.

The canonical [closure report](../../../Studies/S06_Report-Recreation_v004/Records/closure-report.md) contains authority, exact selected outputs, verification, source/recovery status and handoff boundaries. The [approved delivery index](../../../Studies/S06_Report-Recreation_v004/APPROVED_DELIVERY.md) identifies the retained movie and editable native. No further S06 work is active.
''',encoding='utf-8')
print(json.dumps({'status':approval['status'],'fresh_decode_frames':len(rows),'selected_artifacts':artifacts},indent=2))
