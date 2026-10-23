import subprocess,json,hashlib,statistics,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];P=B/'Previews';R=B/'Records';OLD=B.parent/'Camera-Proof_v019';F=Path('D:/MIT-ECCO-Render-Recovery/S05-v020-RenderCache/Frames')
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';video=P/'S05_continuous-camera_v020.mp4'
assert all((F/f'S05_{f:04d}.png').exists() for f in range(1,433))
subprocess.run([str(ff),'-y','-framerate','24','-i',str(F/'S05_%04d.png'),'-frames:v','432','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,capture_output=True)
chosen=[1,25,48,72,96,112,120,121,132,144,156,165,205,246,289,330,370,402,420,432]
sheet=Image.new('RGB',(1280,5*206),(16,23,29));d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
proc=subprocess.Popen([str(ff),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);stride=960*540*3;count=0
while True:
 data=bytearray()
 while len(data)<stride:
  c=proc.stdout.read(stride-len(data))
  if not c:break
  data.extend(c)
 if not data:break
 assert len(data)==stride;count+=1
 if count in chosen:
  im=Image.frombytes('RGB',(960,540),bytes(data));im.thumbnail((320,180));i=chosen.index(count);x=i%4*320;y=i//4*206;sheet.paste(im,(x,y+26));d.text((x+8,y+4),f'{(count-1)/24:.2f}s / f{count}',font=font,fill='white')
assert proc.wait()==0 and count==432
sheet.save(P/'continuous-camera-contact-sheet.jpg',quality=94)
times=json.loads((R/'render-timings.json').read_text());assert len(times)==164
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
media={'frames':432,'fps':24,'seconds':18,'resolution':[960,540],'new_render_frames':164,'reused_v019_frames':268,'reuse_range':[165,432],'mean_new_frame_seconds':statistics.mean(r['seconds'] for r in times),'max_new_frame_seconds':max(r['seconds'] for r in times),'total_new_render_seconds':sum(r['seconds'] for r in times),'all_new_frames_under_5_seconds':all(r['seconds']<5 for r in times),'all_encoded_frames_decoded':True,'video_sha256':sha(video)}
(R/'media-verification.json').write_text(json.dumps(media,indent=2))
report=f'''# S05 v020 — Continuous camera from A into B

Owner-requested correction to the positively reviewed v019. The former cut at frame121 is removed. The complete18-second proof is one continuous camera; B's settled interaction and C's reveal remain unchanged from frame165 onward.

## Camera score

- **0–3 seconds:** Track a source-mesh point on the lower raised steel geometry as ENP3 rotates. The point remains near45.5% of image width and50% of image height. The camera rises and moves slightly around it; the object stays the subject instead of drifting out of attention.
- **3–6.83 seconds:** Gradually transfer gaze from that tracked point to B's pad/passage. Camera height, azimuth, roll and lens change continuously, with no jump at five seconds. The lower feature remains the spatial link during this move.
- **6.83–18 seconds:** Retain the previously reviewed B observation, follow into C and final integrated working-body reveal. The existing circulation and rotation continue at their original timing.

## Delivery

- `Previews/S05_continuous-camera_v020.mp4` —18 seconds,960 x540,24fps.
- `Previews/continuous-camera-contact-sheet.jpg` —full journey with dense sampling around the former cut.
- `Previews/transition-study.jpg` —A tracking and A-to-B connection stills.
- `Scenes/S05_continuous-camera_v020.blend` —editable source, saved at the A arrival.

## Checks

All432 camera samples pass solid separation, center-target wall visibility and upward screen-direction checks. A's tracked source point stays in the same screen location to within0.000001 normalized coordinates over frames1–72. At the former cut, camera position changes by0.01335m, as part of the smooth travel. No cut remains.

Scene-content comparison against v019 passes3412 entries. Actual geometry, materials, hydraulics and rotation are preserved. Frames165–432 have exactly matching camera/optical values; rerenders at165/205/330/420 are pixel-identical to v019. Those268 frames are reused, rather than spending time rendering the same images again. v019 remains unchanged.

New rendering: **{media['mean_new_frame_seconds']:.2f}s/frame average**, **{media['max_new_frame_seconds']:.2f}s maximum**, **{media['total_new_render_seconds']:.1f}s total for164 changed frames**. All432 encoded frames decode. Inherited v019 frame costs and clearance checks remain documented in the prior package.

## Review

The transition stills show the lower shape staying under attention while B's raised geometry becomes larger and the camera moves to its flank. This directly addresses the earlier cut and wandering focus. The final normal-speed feel remains for owner review; browser/desktop playback tooling was unavailable in this session's preceding checks, so no independent audience acceptance is claimed. No material or particle polishing was performed.

The selected lower feature is a camera landmark on actual CAD, not a newly certified accelerator face. Hydraulic trajectories and functional stage mapping retain their existing illustrative limits. Source dimensions and engineering clearances were not changed.

Native scene and MP4 remain local with same-machine recovery copies on D. Scripts/reports/selected stills are scoped for Git publication; see `Records/sync-verification.json` for exact remote evidence. Final finishing and film assembly remain outside scope.
'''
for a,z in [('complete18','complete 18'),('near45','near 45'),('and50','and 50'),('—18','— 18'),(',960',', 960'),(',24',', 24'),('All432','All 432'),('within0','within 0'),('frames1','frames 1'),('by0','by 0'),('passes3412','passes 3412'),('Frames165','Frames 165'),('at165','at 165'),('Those268','Those 268'),('for164','for 164')]:report=report.replace(a,z)
(B/'README.md').write_text(report,encoding='utf-8');(R/'report.md').write_text(report,encoding='utf-8')
backup=Path('D:/MIT-ECCO-Render-Recovery/S05-v020-Previs');files=[]
for p in [B/'Scenes/S05_continuous-camera_v020.blend',video,ROOT/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend']:
 q=backup/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True)
 if not q.exists():shutil.copy2(p,q)
 assert sha(p)==sha(q);files.append({'source':str(p),'backup':str(q),'sha256':sha(p)})
(R/'asset-manifest.json').write_text(json.dumps({'files':files,'same_machine_backup_only':True,'source_v019_preserved':True,'status':'Owner review pending'},indent=2))
print(json.dumps(media))
