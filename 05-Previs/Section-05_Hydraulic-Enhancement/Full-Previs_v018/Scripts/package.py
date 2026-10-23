import subprocess,json,hashlib,statistics
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];P=B/'Previews'
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
frames=Path('D:/MIT-ECCO-Render-Recovery/S05-v018-RenderCache/Frames');video=P/'S05_full-cinematic_v018.mp4'
assert all((frames/f'S05_{f:04d}.png').exists() for f in range(1,433))
r=subprocess.run([str(ff),'-y','-framerate','24','-i',str(frames/'S05_%04d.png'),'-frames:v','432','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],capture_output=True,text=True,check=True)
(B/'Records/encode.log').write_text(r.stderr)
chosen=[1,25,49,73,96,120,121,145,169,193,217,241,265,288,289,312,336,360,384,408,420,432]
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16);sheet=Image.new('RGB',(1280,6*210),(14,20,25));d=ImageDraw.Draw(sheet)
process=subprocess.Popen([str(ff),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stride=1280*720*3;count=0;selected={1:'entry',198:'interaction',312:'diffuser',432:'integrated'}
while True:
 data=bytearray()
 while len(data)<stride:
  part=process.stdout.read(stride-len(data))
  if not part:break
  data.extend(part)
 if not data:break
 assert len(data)==stride
 count+=1
 if count in chosen or count in selected:
  im=Image.frombytes('RGB',(1280,720),bytes(data))
  if count in selected:im.save(P/(selected[count]+'.png'))
  if count in chosen:
   i=chosen.index(count);thumb=im.copy();thumb.thumbnail((320,180));x=(i%4)*320;y=(i//4)*210;sheet.paste(thumb,(x,y+26));label='A' if count<=120 else ('B' if count<=288 else 'C');d.text((x+8,y+4),f'{label}   {(count-1)/24:.2f}s / f{count}',font=font,fill='white')
error=process.stderr.read().decode();assert process.wait()==0,error;assert count==432,count
sheet.save(P/'chronological-contact-sheet.jpg',quality=94)
times=json.loads((B/'Records/render-timings.json').read_text());assert len(times)==432 and len({r['frame'] for r in times})==432
result={'frames':count,'duration_seconds':18,'fps':24,'resolution':[1280,720],'codec':'H.264','all_frames_decoded':True,'render_max_seconds':max(r['seconds'] for r in times),'render_mean_seconds':statistics.mean(r['seconds'] for r in times),'all_frames_strictly_below_5s':all(r['seconds']<5 for r in times),'mp4_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'contact_sheet_frames':chosen}
result['total_frame_render_seconds']=sum(r['seconds'] for r in times)
result['elapsed_first_to_last_frame_seconds']=(frames/'S05_0432.png').stat().st_mtime-(frames/'S05_0001.png').stat().st_mtime+times[0]['seconds']
result['elapsed_span_note']='Filesystem completion timestamps plus first-frame duration; includes pauses for verification and supply extension during the batch. Aggregate frame-render time excludes those pauses and encoding.'
(B/'Records/media-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
(P/'review.html').write_text('''<!doctype html><html><head><meta charset="utf-8"><title>S05 v018 — Hydraulic Enhancement</title><style>body{margin:16px auto;max-width:1280px;background:#111b22;color:#e4e9ec;font:16px Segoe UI,sans-serif}h1{font-size:23px;margin:8px 0}p{color:#b7c5cc}video,img{width:100%;display:block}button{background:#bf813d;color:#111;border:0;padding:10px 20px;margin:8px 0;cursor:pointer}</style></head><body><h1>S05 · Hydraulic Enhancement · v018</h1><button onclick="document.querySelector('video').currentTime=0;document.querySelector('video').play()">Play full sequence</button><video src="S05_full-cinematic_v018.mp4" controls preload="auto" playsinline></video><p>18-second previs · A 0–5s · B 5–12s · C 12–18s</p><p>Illustrative circulation and rotation. Morphological stage mapping awaits source confirmation; no CFD or performance result is depicted.</p><img src="chronological-contact-sheet.jpg" alt="Chronological review frames"></body></html>''',encoding='utf-8')
