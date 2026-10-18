"""Local media QA/manifest. Run after queued rendering and visual inspection."""
import json,hashlib,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageStat
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets/Acoustics';T=ROOT/'04-Production/Records/Tasks/T-046';E=T/'Evidence';P=T/'Previews'
FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
if (P/'Frames_A/f0096.png').exists():
 video=P/'Sensing_behavior_v001.mp4'
 if not video.exists():subprocess.run([str(FF),'-v','error','-framerate','24','-i',str(P/'Frames_A/f%04d.png'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
 decoded=P/'Decoded_v001';decoded.mkdir(exist_ok=True)
 subprocess.run([str(FF),'-v','error','-i',str(video),str(decoded/'f%04d.png')],check=True)
 images=sorted(decoded.glob('f*.png'));checks=[];hashes=[];deltas=[]
 for i,p in enumerate(images):
  im=Image.open(p).convert('RGB');hashes.append(sha(p));checks.append(im.size==(1280,720));checks.append(max(ImageStat.Stat(im).stddev)>3)
  if i:
   from PIL import ImageChops
   prev=Image.open(images[i-1]).convert('RGB');deltas.append(sum(ImageStat.Stat(ImageChops.difference(prev,im)).mean))
 chosen=[1,10,14,17,21,23,27,31,35,40,47,53,57,61,65,69,73,77,81,88,92,96]
 sheet=Image.new('RGB',(4*320,6*200),(16,20,23));d=ImageDraw.Draw(sheet)
 for i,f in enumerate(chosen):
  im=Image.open(images[f-1]);im.thumbnail((320,180));x=(i%4)*320;y=(i//4)*200;sheet.paste(im,(x,y));d.text((x+5,y+181),f'Frame {f} / {(f-1)/24:.2f}s',fill='white')
 sheet.save(P/'Sensing_motion-inspection_v001.jpg',quality=92)
 dump(E/'media-verification_v001.json',dict(video=rel(video),sha256=sha(video),bytes=video.stat().st_size,decoded_frames=len(images),fps=24,duration_s=len(images)/24,resolution=[1280,720],all_frames_nonblank_size=all(checks),distinct_decoded_hashes=len(set(hashes)),successive_rgb_deltas=dict(min=min(deltas),max=max(deltas),moving_transitions=sum(x>.05 for x in deltas)),visual_inspection_sheet=rel(P/'Sensing_motion-inspection_v001.jpg'),limitations='Executor decoded/selected-frame visual inspection; no human comprehension/technical acceptance inferred.'))
files=[A/'Acoustics_v001.blend',A/'Acoustics_v002.blend',A/'Acoustics_v003.blend',T/'Scenes/Sensing_reuse_A_v008.blend',T/'Scenes/Sensing_reuse_B_v008.blend']
sources=[ROOT/'04-Production/Shared/Assets/BHA/BHA_film_v006.blend',ROOT/'04-Production/Shared/Assets/WellAssembly/World_environment_v009.blend',ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend',ROOT/'04-Production/Mechanisms/B201/Scenes/B201_pulse-echo_refinement_v006.blend']
art=[dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size,storage='local-native') for p in files]
if (P/'Sensing_behavior_v001.mp4').exists():p=P/'Sensing_behavior_v001.mp4';art.append(dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size,storage='local-video'))
for p in sorted(P.glob('Review_*.png')):art.append(dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size,storage='selected-tracked-still'))
manifest=dict(task='T46',version='v001',base_commit='df1bc5626e820dc3a0b9af286bfcca4ce498d8c0',status='asset_candidate_pending_master_independent_verification_and_Radzi_review',units='metres_seconds',axes='T44 common unscaled world +X longitudinal; acoustic prototypes +Z along propagation/normal',top_collection='ACOUSTICS_MASTER',current_master=rel(A/'Acoustics_v003.blend'),current_consumers=[rel(T/f'Scenes/Sensing_reuse_{k}_v008.blend') for k in ['A','B']],artifacts=art,sources=[dict(path=rel(p),sha256=sha(p),bytes=p.stat().st_size) for p in sources],consumers=['S02-A','S02-B','S02-C','S04-B','S04-D'],event_exports=[rel(E/f'events_{k}_v002.json') for k in ['A','B']],interfaces=['Scripts/acoustic_event_v001.py','Scripts/acoustic_binding_v001.py'],native_backup='All .blend/video/raw frames local Git-ignored. No upload or off-machine backup claimed.',limits=['Illustrative acoustic timing/graphics; no calibrated speed or firing cadence','Inherited sensor references/plugged source limits retained; no invented mud sensor coordinate','No reconstruction, full graphics/output system, actual film shot or engineering certification','Cold-empty-cache initialization cap remains unresolved'],failed_candidates=['Sensing_reuse_A/B_v002.blend and v003.blend: shifted unrelated library links','Sensing_reuse_A/B_v004.blend: camera occluded sensor/effects with retained formation'])
dump(A/'manifest_v001.json',manifest)




