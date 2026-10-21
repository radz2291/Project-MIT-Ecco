from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,hashlib,re,statistics,sys
B=Path(__file__).resolve().parents[1];ROOT=B.parents[4];FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',21);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
CACHE=Path(json.loads((B/'Records/storage.json').read_text())['cache_work_root']) if (B/'Records/storage.json').exists() else B/'Work'
def sm(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
rows=json.loads((B/'Records/timings-render.json').read_text());prepare='--prepare' in sys.argv
assert max(r['seconds'] for r in rows)<5
if not prepare:assert [r['frame'] for r in rows]==list(range(1,433))
selected=[1,40,85,94,104,190,206,216,261,280,300,318,336,365,400,432]
for f in range(1,len(rows)+1):
 if prepare and (CACHE/'Assembly'/f'S04_{f:04d}.png').exists() and (f not in selected or (B/'Previews'/f'S04_review_{f:04d}_v033.png').exists()):continue
 im=Image.open(CACHE/'Frames'/f'S04_{f:04d}.png').convert('RGBA');layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
 for start,end,title in [(63,141,'Supported backing'),(175,261,'Reduced backing'),(337,450,'Inner-wall wear')]:
  if start<=f<=end:
   a=sm((f-start)/8)*sm((end-f)/8);box=d.textbbox((0,0),title,font=font);d.rounded_rectangle((16,17,48+box[2],58),radius=5,fill=(12,22,28,round(145*a)));d.text((30,25),title,font=font,fill=(225,235,240,round(255*a)))
 if f>=336:d.text((20,669),'Wireframe tool: explanatory view',font=small,fill=(185,205,215,255))
 d.rectangle((0,692,1280,720),fill=(10,20,25,190));d.text((20,699),'ILLUSTRATIVE GEOMETRY AND RESPONSE — NOT FIELD DATA',font=small,fill=(205,220,225,255));im=Image.alpha_composite(im,layer).convert('RGB');im.save(CACHE/'Assembly'/f'S04_{f:04d}.png',compress_level=1)
 if f in selected:im.save(B/'Previews'/f'S04_review_{f:04d}_v033.png')
if prepare:sys.exit(0)
video=B/'Previews/S04_continuous_ABCD_v033.mp4';r=subprocess.run([str(FF),'-y','-framerate','24','-i',str(CACHE/'Assembly/S04_%04d.png'),'-frames:v','432','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],capture_output=True,text=True);(B/'Records/encode.log').write_text(r.stderr);assert r.returncode==0
r=subprocess.run([str(FF),'-i',str(video),'-map','0:v:0','-f','null','-'],capture_output=True,text=True);(B/'Records/decode.log').write_text(r.stderr);assert r.returncode==0 and re.search(r'frame=\s*432',r.stderr)
values=[r['seconds'] for r in rows];report={'video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'frames':432,'fps':24,'duration_seconds':18,'resolution':[1280,720],'full_decode':True,'render_seconds_mean':statistics.mean(values),'render_seconds_max':max(values),'render_seconds_sum':sum(values),'all_frames_under5seconds':True,'single_camera':True,'D_detection_tied_to_sensor':True,'integration_scope':'A B C D full continuous18second previs','human_approval':'pending'};(B/'Records/delivery.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(1280,816),(15,22,28));d=ImageDraw.Draw(sheet)
for i,f in enumerate(selected):
 im=Image.open(CACHE/'Assembly'/f'S04_{f:04d}.png');im.thumbnail((320,180));x=i%4*320;y=i//4*204;sheet.paste(im,(x,y));d.text((x+8,y+182),f'{(f-1)/24:.2f}s / frame {f}',font=small,fill='white')
sheet.save(B/'Previews/S04_contact-sheet_v033.jpg',quality=94);print(json.dumps(report,indent=2))
