"""Package local proof media, inspect hashes/frames and produce scoped manifest.

Run with bundled Python after queued renders. Does not invoke Blender or Git.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image,ImageStat
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets/CasedHole';T=ROOT/'04-Production/Records/Tasks/T-047';P=T/'Previews/v003';E=T/'Evidence'
FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
def encode():
 rows=[]
 for name in ['Retrieval','Support']:
  frames=P/'Frames'/name;files=sorted(frames.glob('*.png'));assert len(files)==96,(name,len(files))
  video=P/('Cased'+name+'_v003.mp4');assert not video.exists(),video
  subprocess.run([str(FF),'-y','-framerate','24','-i',str(frames/('Cased'+name+'_f%03d_v003.png')),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  decoded=P/'Cache'/(name+'_Decoded');decoded.mkdir(exist_ok=True,parents=True);subprocess.run([str(FF),'-i',str(video),'-vsync','0',str(decoded/'frame_%03d.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE);imgs=sorted(decoded.glob('*.png'));assert len(imgs)==96
  pixels=[]
  for p in imgs:
   with Image.open(p) as im:assert im.size==(1280,720);pixels.append(dict(frame=p.name,stddev=ImageStat.Stat(im).stddev))
  assert all(max(p['stddev'])>1 for p in pixels)
  assert len({sha(p) for p in imgs})>1,'Playable proof must contain changing frames'
  source=T/'Scenes'/('Cased'+name+('_v006.blend' if name=='Support' else '_v004.blend'))
  rows.append(dict(video=rel(video),sha256=sha(video),bytes=video.stat().st_size,source_native=rel(source),source_sha256=sha(source),decoded_frames=len(imgs),fps=24,duration_s=4,nonblank=True,distinct_frames=len({sha(p) for p in imgs}),inspection='All decoded frames dimension/nonblank checked; selected chronological frames inspected separately by executor/master.'))
 dump(E/'media-verification_v003.json',rows)
def manifest():
 source=json.loads((E/'source-inspection_v001.json').read_text());inputs=[]
 for row in source:
  p=ROOT/row['path'];assert sha(p)==row['sha256'];inputs.append(dict(path=row['path'],sha256=row['sha256'],unchanged=True))
 for p in [ROOT/'04-Production/Shared/Assets/Acoustics/Acoustics_v002.blend',ROOT/'04-Production/Shared/Assets/Acoustics/Scripts/acoustic_event_v001.py',ROOT/'04-Production/Shared/Assets/Acoustics/Scripts/acoustic_binding_v001.py',ROOT/'04-Production/Shared/Assets/Acoustics/Scripts/build_sensing_v001.py',ROOT/'04-Production/Records/Tasks/T-045/event-contract_v001.json']:
  inputs.append(dict(path=rel(p),sha256=sha(p),role='Shared T46 event/prototype dependency or T45 common contract; consumed without edits.'))
 inputs.append(dict(path='04-Production/Shared/Assets/Acoustics/Acoustics_v003.blend',sha256=sha(ROOT/'04-Production/Shared/Assets/Acoustics/Acoustics_v003.blend'),role='Final active thin-arc sensing prototypes; previous v002 is retained in predecessors.'))
 native=sorted(A.glob('*.blend'))+sorted((T/'Scenes').glob('*.blend'))
 videos=sorted(P.glob('*.mp4'));artifacts=[dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size,storage='local_only_ignored_no_offmachine_backup_claimed') for p in native+videos]
 still_names=['CasedHardware_f001_v003.png','CasedChannel_f001_v005.png','CasedWearGraze_f001_v005.png','CasedWearSection_f001_v005.png','CasedRetrieval_f048_v003.png','CasedRetrieval_f096_v003.png','CasedSupport_f018_v006.png','CasedSupport_f076_v006.png']
 stills=[]
 for n in still_names:
  p=P/n
  if p.exists():
   with Image.open(p) as im:stills.append(dict(path=rel(p),sha256=sha(p),dimensions=list(im.size),bytes=p.stat().st_size))
 dump(A/'manifest_v001.json',dict(task='T47',task_id='de4e8339-fbdd-4c40-9f30-bf61302ed04e',baseline_commit='df1bc5626e820dc3a0b9af286bfcca4ce498d8c0',units='metres',axis='T44 common +X downhole; retrieval toward negativeX',master='CasedHole_v002.blend',conditions=dict(casing_ri_m=.1589405,casing_ro_m=.1698625,cement_ro_m=.22225,axial_interval_m=[-5.5,0],channel_axial_m=[-2.5,-.4],channel_azimuth_rad=[.3,.8],preexisting_wear_max_m=.004),inputs=inputs,artifacts=artifacts,approval_stills=stills,consumer_map={'S04-A':'retrieval and layer context','S04-B':'qualitative support/actual A-SENSING event adapter','S04-C':'localized exterior channel','S04-D':'pre-existing inner wear/registered nominal contour'},limits=['Illustrative timing/support/wear, no quantified bond/thickness/fluid identity','No native upload or offmachine backup claim','Normal GPU-cache tests only; T44 empty-cache initialization limit unresolved','Executor checks do not grant human appearance/engineering/client acceptance']))
 manifest_path=A/'manifest_v001.json';published=json.loads(manifest_path.read_text())
 current=[A/'CasedHole_v002.blend']+[T/'Scenes'/n for n in ['CasedReuse_A_v002.blend','CasedReuse_B_v002.blend','CasedHardware_v003.blend','CasedChannel_v005.blend','CasedWearGraze_v005.blend','CasedWearSection_v005.blend','CasedRetrieval_v004.blend','CasedSupport_v006.blend']]
 published['current_native_candidates']=[dict(path=rel(p),sha256=sha(p)) for p in current]
 published['event_export']='04-Production/Records/Tasks/T-047/Evidence/actual-cased-events_v006.json'
 published['saved_verification']='04-Production/Records/Tasks/T-047/Evidence/saved-final-verification_v006.json'
 published['storage']={'native_video_raw_frames_cache':'Local and ignored; no native upload/offmachine backup claimed','selected_stills_scripts_reports_json':'Explicit T45 integrator allow-list; no Git writes by builder'}
 dump(manifest_path,published)
 # Exact explicit integrator allow-list. Raw/decoded frame directories and native/video never included.
 allowed=sorted([p for p in A.rglob('*') if p.is_file() and p.suffix in ['.py','.md','.json'] and '__pycache__' not in str(p)]+[p for p in T.rglob('*') if p.is_file() and p.suffix in ['.md','.json']]+[P/n for n in still_names if (P/n).exists()]+[T/'Previews/v001/CasedReuse_B_f001_v002.png'])
 allowed=[p for p in allowed if p.name!='tracked-files_v001.json'];dump(E/'tracked-files_v001.json',dict(integrator='T45 only',paths=[rel(p) for p in allowed]+[rel(E/'tracked-files_v001.json')]))
if len(sys.argv)>1 and sys.argv[1]=='encode':encode()
manifest();print('T47_PACKAGE_MANIFEST_SAVED')
