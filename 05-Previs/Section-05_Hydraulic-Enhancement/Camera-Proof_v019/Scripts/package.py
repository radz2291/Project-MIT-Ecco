import subprocess,json,hashlib,statistics
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];P=B/'Previews'
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
F=Path('D:/MIT-ECCO-Render-Recovery/S05-v019-RenderCache/Frames');video=P/'S05_camera-motion_v019.mp4'
assert all((F/f'S05_{f:04d}.png').exists() for f in range(1,433))
r=subprocess.run([str(ff),'-y','-framerate','24','-i',str(F/'S05_%04d.png'),'-frames:v','432','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],capture_output=True,text=True,check=True);(B/'Records/encode.log').write_text(r.stderr)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
sheet=Image.new('RGB',(1440,294),(17,25,31));d=ImageDraw.Draw(sheet)
for i,(name,title) in enumerate([('A_arrival','A / Sculptural arrival'),('B_arrival','B / Twisted-pad showcase'),('C_arrival','C / Integrated working body')]):
 im=Image.open(P/(name+'.png')).convert('RGB');im.thumbnail((480,270));sheet.paste(im,(480*i,24));d.text((480*i+8,3),title,font=font,fill='white')
sheet.save(P/'three-arrivals.jpg',quality=95)
chosen=[1,25,49,73,96,120,121,145,165,193,205,221,246,265,289,312,330,350,370,390,402,420,432]
sheet=Image.new('RGB',(1280,6*206),(17,25,31));d=ImageDraw.Draw(sheet)
proc=subprocess.Popen([str(ff),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);stride=960*540*3;count=0
while True:
 data=bytearray()
 while len(data)<stride:
  chunk=proc.stdout.read(stride-len(data))
  if not chunk:break
  data.extend(chunk)
 if not data:break
 assert len(data)==stride;count+=1
 if count in chosen:
  im=Image.frombytes('RGB',(960,540),bytes(data));im.thumbnail((320,180));i=chosen.index(count);x=i%4*320;y=i//4*206;sheet.paste(im,(x,y+26));d.text((x+8,y+3),f'{(count-1)/24:.2f}s / f{count}',font=font,fill='white')
assert proc.wait()==0,proc.stderr.read().decode();assert count==432
sheet.save(P/'motion-contact-sheet.jpg',quality=94)
rows=json.loads((B/'Records/render-timings.json').read_text());assert len(rows)==432
record={'decoded_frames':count,'fps':24,'seconds':18,'resolution':[960,540],'samples':4,'engine':'EEVEE','mean_seconds':statistics.mean(r['seconds'] for r in rows),'max_seconds':max(r['seconds'] for r in rows),'total_render_seconds':sum(r['seconds'] for r in rows),'elapsed_batch_seconds':(F/'S05_0432.png').stat().st_mtime-(F/'S05_0001.png').stat().st_mtime+rows[0]['seconds'],'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'all_under_5_seconds':all(r['seconds']<5 for r in rows)}
(B/'Records/media-verification.json').write_text(json.dumps(record,indent=2))
(P/'review.html').write_text('''<!doctype html><html><head><meta charset="utf-8"><title>S05 v019 camera direction</title><style>body{background:#111b22;color:#e8edef;font:16px Segoe UI;max-width:1280px;margin:24px auto}video{display:block;width:960px;max-width:100%}img{width:100%}button{padding:12px;background:#c58a48;border:0;margin:8px 0}</style></head><body><h1>S05 v019 — Camera direction proof</h1><p>Existing hydraulic animation. Camera and composition study only.</p><button onclick="const v=document.querySelector('video');v.currentTime=0;v.playbackRate=1;v.play()">Play at normal speed</button><video src="S05_camera-motion_v019.mp4" controls playsinline preload="auto"></video><h2>Three arrivals</h2><img src="three-arrivals.jpg"><h2>Motion progression</h2><img src="motion-contact-sheet.jpg"></body></html>''',encoding='utf-8')
print(json.dumps(record))
