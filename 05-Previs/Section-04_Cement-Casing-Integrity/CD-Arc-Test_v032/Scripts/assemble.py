from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,re,hashlib,statistics
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
rows=json.loads((B/'Records/timings-render.json').read_text());assert [r['frame'] for r in rows]==list(range(1,121)) and max(r['seconds'] for r in rows)<5
for f in range(1,121):
 im=Image.open(B/'Work/Frames'/f'S04_CD_{f:04d}.png').convert('RGB');d=ImageDraw.Draw(im);d.rectangle((0,692,1280,720),fill=(12,22,28));d.text((20,699),'ILLUSTRATIVE GEOMETRY AND RESPONSE — PRESENTATION TRANSITION TEST — NOT FIELD DATA',font=small,fill=(205,220,225));im.save(B/'Work/Assembly'/f'S04_CD_{f:04d}.png',compress_level=1)
 if f in [1,17,25,33,41,48,65,90,120]:im.save(B/'Previews'/f'S04_CD_review_{f:04d}_v032.png')
video=B/'Previews/S04_CD_arc-and-style_v032.mp4';r=subprocess.run([str(FF),'-y','-framerate','24','-i',str(B/'Work/Assembly/S04_CD_%04d.png'),'-frames:v','120','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],capture_output=True,text=True);(B/'Records/encode.log').write_text(r.stderr);assert r.returncode==0
r=subprocess.run([str(FF),'-i',str(video),'-map','0:v:0','-f','null','-'],capture_output=True,text=True);(B/'Records/decode.log').write_text(r.stderr);assert r.returncode==0 and re.search(r'frame=\s*120',r.stderr)
frames=[1,17,25,33,41,48,65,90,120];sheet=Image.new('RGB',(1280,792),(14,25,34));d=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
 im=Image.open(B/'Work/Assembly'/f'S04_CD_{f:04d}.png');im.thumbnail((426,240));x=i%3*426;y=i//3*264;sheet.paste(im,(x,y));d.text((x+8,y+242),f'{(f-1)/24:.2f}s / frame {f}',font=small,fill=(215,230,235))
sheet.save(B/'Previews/S04_CD_contact-sheet_v032.jpg',quality=94)
values=[r['seconds'] for r in rows];report={'video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'duration_seconds':5,'frames':120,'fps':24,'resolution':[1280,720],'full_decode':True,'render_seconds_mean':statistics.mean(values),'render_seconds_max':max(values),'all_final_frames_under5seconds':True,'full_section_integration':False,'human_approval':'pending'};(B/'Records/delivery.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
