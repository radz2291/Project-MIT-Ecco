from pathlib import Path
import json,hashlib,shutil,subprocess,datetime
B=Path(__file__).resolve().parents[1];R=B.parents[3];backup=Path('D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v006')
date='2026-10-25';statement='ok good.. approve.. pls wrap and do closure';implementation='0862c6fb05fa6e86ecd8524cb25f1ca5b277b6f0'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((B/'Records/verification.json').read_text(encoding='utf-8'));delivery=json.loads((B/'Records/delivery.json').read_text(encoding='utf-8'));manifest=json.loads((B/'Records/asset-manifest.json').read_text(encoding='utf-8'))
for item in manifest:
 p=B/item['path'];assert sha(p)==item['sha256'],('Changed since review',str(p));assert sha(backup/item['path'])==item['sha256'],('Recovery mismatch',item['path'])
native=B/'Scenes/S07_Monumental-Precision_v006.blend';assert sha(native)==v['native_sha256']
FF=R/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
checks=[];artifacts=[{'path':native.relative_to(B).as_posix(),'sha256':sha(native),'bytes':native.stat().st_size,'recovery_sha256_matches':sha(native)==sha(backup/native.relative_to(B))}]
for name,item in delivery['media'].items():
 matches=list((B/'Previews').rglob(name));assert len(matches)==1;p=matches[0];assert sha(p)==item['sha256']
 run=subprocess.run([str(FF),'-v','error','-i',str(p),'-map','0:v:0','-f','framemd5','-'],capture_output=True,text=True);assert run.returncode==0 and not run.stderr.strip()
 count=len([x for x in run.stdout.splitlines() if x and not x.startswith('#')]);assert count==item['decoded_frames']
 checks.append({'path':p.relative_to(B).as_posix(),'fresh_decode_frames':count,'decode_errors':0});artifacts.append({'path':p.relative_to(B).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'recovery_sha256_matches':sha(p)==sha(backup/p.relative_to(B))})
history=[]
for version in range(1,7):
 folder=B.parent/f'Sequence_v{version:03d}';n=folder/f'Scenes/S07_Monumental-Precision_v{version:03d}.blend';p=folder/f'Previews/S07_Monumental-Precision_v{version:03d}.mp4';assert n.exists() and p.exists()
 history.append({'version':f'v{version:03d}','native_exists':True,'movie_exists':True,'selected':version==6})
record={'status':'Owner-approved S07 cinematic previs; closed','approval_date':date,'timezone':'Asia/Kuala_Lumpur','owner_statement':statement,'selected_movie':'Previews/S07_Monumental-Precision_v006.mp4','selected_native':native.relative_to(B).as_posix(),'implementation_commit':implementation,'closure_verified_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'artifacts':artifacts,'fresh_decode_checks':checks,'saved_native_freshly_reopened_and_verified':True,'source_geometry_unchanged':True,'first_two_shots_preserved':True,'work_workspace_revision':747,'matching_work_ticket':None,'work_action':'No S07 ticket exists; direct owner-authorized closure, unrelated tickets untouched','previous_versions':history,'recovery_root':str(backup),'recovery_type':'Hash-verified same-machine D-drive copy; not off-machine backup','media_remote_upload':False,'scope':'Owner approval of S07 v006 previs; logo insertion, audio, film assembly and client delivery remain with Radzi. No engineering certification or client approval inferred.'}
(B/'Records/closure-verification.json').write_text(json.dumps(record,indent=2))
approval=f'''# S07 owner approval — 25 October 2026

**Status: Approved and selected for Section 7 previs handoff.**

Owner statement: “{statement}”

This follows delivery of S07 v006 and selects that exact three-shot candidate, including the stronger close-to-wide pullback in shot 3. Shots 1 and 2 remain the accepted v005 images. The tool stays stationary; camera movement supplies the reveal. No logo or closing text. Final fade to black retained for a separate logo frame in post.

- Selected movie: `Previews/S07_Monumental-Precision_v006.mp4`
- Movie SHA-256: `{delivery['media']['S07_Monumental-Precision_v006.mp4']['sha256']}`
- Selected native: `Scenes/S07_Monumental-Precision_v006.blend`
- Native SHA-256: `{v['native_sha256']}`
- Implementation commit: `{implementation}`
- Eight seconds, 192 frames, 24 fps, 1280×720; cuts at frames 61 and 121.

Approval covers this Section 7 cinematic previs. It does not imply client acceptance, engineering certification, expensive final rendering or completed film assembly. Radzi owns final logo insertion, audio, timeline and client delivery. Source masters and all earlier versions remain intact.
'''
(B/f'Records/owner-approval_{date}.md').write_text(approval,encoding='utf-8')
readme=(B/'README.md').read_text(encoding='utf-8');readme=readme.replace('Updated ending awaits owner review.','Owner approved v006 on 25 October 2026; this section is closed.');readme+='\n[Approval record](Records/owner-approval_2026-10-25.md) · [Closure verification](Records/closure-verification.json)\n';(B/'README.md').write_text(readme,encoding='utf-8')
report=(B/'Records/production-report.md').read_text(encoding='utf-8');report=report.replace('Status: revised ending awaiting owner review.','Status: owner-approved S07 v006; closed on 25 October 2026.').replace('owner playback review remains pending.','owner playback approval is recorded in owner-approval_2026-10-25.md.');report+='\n## Closure\n\nSelected candidate approved by the owner. Fresh native/source checks and media decodes passed; selected video/native/recovery hashes match. See closure-verification.json and owner-approval_2026-10-25.md. No matching S07 ticket exists in live Work revision 747; unrelated tickets were not changed. Prior versions and render caches are retained; no additional visual work or rendering is planned under this scope.\n';(B/'Records/production-report.md').write_text(report,encoding='utf-8')
delivery['review_status']='Owner-approved S07 v006 previs; closed';delivery['approval_record']='Records/owner-approval_2026-10-25.md';(B/'Records/delivery.json').write_text(json.dumps(delivery,indent=2))
(B.parent/'README.md').write_text('''# Section 7 — Product Hero

**Selected: Sequence_v006. Owner approved and closed, 25 October 2026.**

- [Approved eight-second edit](Sequence_v006/Previews/S07_Monumental-Precision_v006.mp4)
- [Individual shot clips](Sequence_v006/Previews/Individual-Shots/)
- [Editable Blender scene](Sequence_v006/Scenes/S07_Monumental-Precision_v006.blend)
- [Approval record](Sequence_v006/Records/owner-approval_2026-10-25.md)
- [Production and closure report](Sequence_v006/Records/production-report.md)

Three shots: detail glide, reverse beauty, and close-to-wide hero pullback. No logo; product fades to black. Owner supplies the separate logo frame, audio and final film assembly. Native/media stay local; hash-verified same-machine recovery at `D:/MIT-ECCO-Render-Recovery/S07-Monumental-Precision_v006`.

Sequences v001–v005 and historical shot folders remain retained history. They are not the selected delivery. Shared masters and other sections are preserved.
''',encoding='utf-8')
task=R/'04-Production/Records/Tasks/S07-Closure';task.mkdir(parents=True,exist_ok=True)
(task/'report.md').write_text(f'''# S07 closure — 25 October 2026

Owner approved v006: “{statement}”

Selected [Section 7 handoff](../../../Shots/S07/README.md), [approval](../../../Shots/S07/Sequence_v006/Records/owner-approval_2026-10-25.md), [production report](../../../Shots/S07/Sequence_v006/Records/production-report.md) and [closure verification](../../../Shots/S07/Sequence_v006/Records/closure-verification.json).

Implementation commit: `{implementation}`. Fresh native and geometry checks passed; 192-frame full edit, 240-frame boundary preview and 60/60/72-frame shot clips decoded without errors. Selected native/media hashes match the reviewed candidate and D-drive recovery. Six native/movie versions remain present. No new rendering or scene modification during closure.

Live MIT ECCO Work revision 747 has no matching S07 production ticket. Direct owner-authorized closure recorded here; no unrelated Work ticket was mutated. Tracked closure records are synchronized to the established GitHub main branch, exact commit and pinned links in Sequence_v006/Records/sync-verification.json. Heavy media is local only, with same-machine recovery rather than an off-machine backup. Final logo, audio and film assembly remain with Radzi.
''',encoding='utf-8')
oldtask=R/'04-Production/Records/Tasks/S07-v006-Revision/report.md';oldtask.write_text('# S07 v006 — approved and closed\n\nSee [closure report](../S07-Closure/report.md), [production report](../../../Shots/S07/Sequence_v006/Records/production-report.md) and [selected media](../../../Shots/S07/Sequence_v006/README.md).\n',encoding='utf-8')
# Refresh the recovery copy and manifest after recording approval; retain all media.
updated=[]
for p in B.rglob('*'):
 if not p.is_file() or 'Cache' in p.relative_to(B).parts or p.suffix in ('.log','.blend1') or p.name in ('asset-manifest.json','recovery-verification.json','sync-verification.json'):continue
 rel=p.relative_to(B);dst=backup/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);assert sha(dst)==sha(p);updated.append({'path':rel.as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
for name,data in [('asset-manifest.json',updated),('recovery-verification.json',{'recovery_root':str(backup),'files_verified':len(updated),'same_machine_only':True,'cache_included':False,'status':'Owner-approved v006 closure'})]:
 (B/'Records'/name).write_text(json.dumps(data,indent=2));shutil.copy2(B/'Records'/name,backup/'Records'/name)
print(json.dumps({'status':record['status'],'artifact_count':len(artifacts),'decoded_media':len(checks),'recovery_files':len(updated),'history_versions_preserved':len(history)},indent=2))
