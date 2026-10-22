import subprocess,json,hashlib,shutil,statistics
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
frames=B/'Work/Frames';P=B/'Previews';video=P/'S05_twisted-pad_interaction_v001.mp4'
assert len(list(frames.glob('S05_*.png')))==144
r=subprocess.run([str(ff),'-y','-framerate','24','-i',str(frames/'S05_%04d.png'),'-frames:v','144','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],capture_output=True,text=True,check=True)
(B/'Records/encode.log').write_text(r.stderr)
r=subprocess.run([str(ff),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True)
stride=1280*720*3;assert len(r.stdout)==stride*144
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
sheet=Image.new('RGB',(1280,792),(14,20,25));d=ImageDraw.Draw(sheet)
for i,f in enumerate([1,13,25,37,49,61,73,85,97,109,121,144]):
 im=Image.frombytes('RGB',(1280,720),r.stdout[(f-1)*stride:f*stride]);im.thumbnail((320,180));x=(i%4)*320;y=(i//4)*264;sheet.paste(im,(x,y+28));d.text((x+10,y+5),f'{(f-1)/24:.2f}s / frame {f}',font=font,fill='white')
sheet.save(P/'motion-review.jpg',quality=93)
for f,name in [(1,'entry'),(72,'interaction'),(144,'exit')]:
 Image.frombytes('RGB',(1280,720),r.stdout[(f-1)*stride:f*stride]).save(P/(name+'.png'))
palette=Image.new('RGB',(1280,400),(14,20,25));d=ImageDraw.Draw(palette)
for i,name in enumerate(['amber','cyan']):
 im=Image.open(P/f'interaction_{name}.png');im.thumbnail((640,360));palette.paste(im,(640*i,40));d.text((640*i+20,10),name.upper()+' / identical camera, geometry and timing',font=font,fill='white')
palette.save(P/'palette-comparison.jpg',quality=95)
timings=json.loads((B/'Records/render-timings.json').read_text())
result={'decoded_frames':144,'seconds':6,'fps':24,'resolution':[1280,720],'codec':'H.264','batch_max_seconds':max(q['seconds'] for q in timings),'batch_mean_seconds':statistics.mean(q['seconds'] for q in timings),'all_batch_frames_below_5s':all(q['seconds']<5 for q in timings),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'inspection':'12 chronological frames decoded from actual MP4; owner normal-speed comprehension review pending'}
(B/'Records/media-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
(P/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>S05 / Hydraulic interaction proof</title><style>body{background:#10191f;color:#dce4e9;font:17px Segoe UI,sans-serif;margin:32px auto;max-width:1280px}video,img{max-width:100%;display:block;margin:20px 0}p{max-width:820px;color:#aabac4}</style><h1>Section 5 · Hydraulic interaction</h1><p>Six-second Stage 6 proof. Watch the fluid tracers and rock fragments bend around the stationary tool. Illustrative paths, not CFD. Amber is the trial video palette; cyan comparison below.</p><video src="S05_twisted-pad_interaction_v001.mp4" controls autoplay loop muted></video><h2>Palette comparison</h2><img src="palette-comparison.jpg"><h2>Entry / interaction / exit</h2><img src="entry.png"><img src="interaction.png"><img src="exit.png">''',encoding='utf-8')
