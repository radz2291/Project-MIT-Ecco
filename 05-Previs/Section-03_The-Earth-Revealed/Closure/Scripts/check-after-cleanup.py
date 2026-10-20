import bpy,json,hashlib,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[2];C=R/'Closure'
expected=['v009','v014','v023','v028','v033','v036'];actual=sorted(p.name for p in R.iterdir() if p.is_dir() and p.name.startswith('v'))
missing=[];changed=[]
manifest=json.loads((C/'Retained-file-manifest.json').read_text())
for row in manifest:
 p=R/row['path']
 if not p.is_file():missing.append(row['path']);continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:changed.append(row['path'])
archive=json.loads((C/'Archived-provenance-manifest.json').read_text());archive_errors=[]
for row in archive:
 p=R/row['archive']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:archive_errors.append(row['archive'])
scenes=[]
for row in json.loads((C/'Localized-dependency-verification.json').read_text()):
 p=R/row['scene'];bpy.ops.wm.open_mainfile(filepath=str(p));issues=[]
 if bpy.data.libraries:issues.append('External Blender libraries present')
 for i in bpy.data.images:
  if i.source=='FILE':
   target=Path(bpy.path.abspath(i.filepath)).resolve()
   if not i.packed_file or not target.is_file():issues.append('Missing image: '+i.name)
   if not target.is_relative_to((R/row['version']).resolve()):issues.append('Image outside retained version: '+i.name)
 scenes.append({'scene':row['scene'],'reopened':True,'issues':issues})
ff=R.parents[1]/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
video=R/'v036/Previews/S03_v036_final_24fps.mp4'
proc=subprocess.run([str(ff),'-v','error','-i',str(video),'-progress','pipe:1','-f','null','-'],capture_output=True,text=True)
(C/'Post-cleanup-video-decode.log').write_text(proc.stdout+proc.stderr)
report={'checked_at':time.strftime('%Y-%m-%dT%H:%M:%S'),'expected_versions':expected,'remaining_versions':actual,'version_folders_correct':expected==actual,'retained_files_checked':len(manifest),'missing_retained_files':missing,'changed_retained_files':changed,'archived_history_files_checked':len(archive),'archive_errors':archive_errors,'scenes':scenes,'video_decodes_432_frames':proc.returncode==0 and 'frame=432' in proc.stdout}
report['ready_to_wrap']=report['version_folders_correct'] and not missing and not changed and not archive_errors and all(not x['issues'] for x in scenes) and report['video_decodes_432_frames']
(C/'Post-cleanup-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
assert report['ready_to_wrap'],'Cleanup verification failed'
