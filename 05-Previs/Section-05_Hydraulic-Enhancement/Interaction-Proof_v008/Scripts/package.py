import subprocess,json,hashlib,statistics
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
frames=B/'Work/Frames';P=B/'Previews';video=P/'S05_internal-flow_v008.mp4'
assert len(list(frames.glob('S05_*.png')))==72
r=subprocess.run([str(ff),'-y','-framerate','24','-i',str(frames/'S05_%04d.png'),'-frames:v','72','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],capture_output=True,text=True,check=True)
(B/'Records/encode.log').write_text(r.stderr)
r=subprocess.run([str(ff),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True)
stride=1280*720*3;assert len(r.stdout)==stride*72
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
sheet=Image.new('RGB',(1280,672),(14,20,25));d=ImageDraw.Draw(sheet)
for i,f in enumerate([1,7,13,19,25,31,37,43,49,55,61,72]):
 im=Image.frombytes('RGB',(1280,720),r.stdout[(f-1)*stride:f*stride]);im.thumbnail((320,180));x=(i%4)*320;y=(i//4)*224;sheet.paste(im,(x,y+28));d.text((x+10,y+5),f'{(f-1)/24:.2f}s / frame {f}',font=font,fill='white')
sheet.save(P/'motion-review.jpg',quality=94)
for f,name in [(1,'entry'),(36,'interaction'),(72,'exit')]:
 Image.frombytes('RGB',(1280,720),r.stdout[(f-1)*stride:f*stride]).save(P/(name+'.png'))
timings=json.loads((B/'Records/render-timings.json').read_text())
result={'decoded_frames':72,'seconds':3,'fps':24,'resolution':[1280,720],'codec':'H.264','batch_max_seconds':max(q['seconds'] for q in timings),'batch_mean_seconds':statistics.mean(q['seconds'] for q in timings),'all_batch_frames_below_5s':all(q['seconds']<5 for q in timings),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'inspection':'12 chronological decoded MP4 frames prepared for agent inspection; owner normal-speed comprehension review pending'}
(B/'Records/media-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
(P/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>S05 v008 / Hydraulic interaction</title><style>body{background:#10191f;color:#dce4e9;font:17px Segoe UI,sans-serif;margin:32px auto;max-width:1280px}video,img{max-width:100%;display:block;margin:20px 0}p{max-width:850px;color:#aabac4}</style><h1>Section 5 · Hydraulic interaction v008</h1><p>Three-second proof: slow clockwise tool rotation, upward circulation and transported rock fragments. The approved amber annulus contains three soft tracer groups and three matte fragments travelling upward around the rotating pad. Illustrative motion, not CFD or measured operating speed.</p><video src="S05_internal-flow_v008.mp4" controls autoplay loop muted></video><h2>Interaction</h2><img src="interaction.png"><h2>Motion sequence</h2><img src="motion-review.jpg">''',encoding='utf-8')



