from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,statistics,hashlib,re
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',21);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
def sm(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
rows=[]
for f in range(1,433):
 im=Image.open(B/'Work/Main'/f'S04_{f:04d}.png').convert('RGBA')
 if 121<=f<=253:
  progress=sm((f-121)/12) if f<=133 else 1-sm((f-235)/18)
  x=round(1280-640*progress);native=min(120,max(1,f-120))
  panel=Image.open(B/'Work/C'/f'C_{native:04d}.png').convert('RGBA');assert panel.size==(640,720)
  im.alpha_composite(panel,(x,0));layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
  d.rectangle((x,0,x+640,54),fill=(12,23,28,210));d.text((x+24,16),'REDUCED BACKING',font=font,fill=(225,236,240,255));d.line((x,0,x,692),fill=(170,190,200,220),width=2)
  if progress>.05:
   d.rectangle((0,0,640,54),fill=(12,23,28,round(210*progress)));d.text((24,16),'CEMENT BACKING',font=font,fill=(225,236,240,round(255*progress)))
  im=Image.alpha_composite(im,layer);rows.append({'frame':f,'C_left_pixel':x,'C_native_frame':native})
 layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer);d.rectangle((0,692,1280,720),fill=(10,20,25,190));d.text((20,699),'ILLUSTRATIVE GEOMETRY AND RESPONSE — NOT FIELD DATA',font=small,fill=(205,220,225,255));im=Image.alpha_composite(im,layer).convert('RGB')
 im.save(B/'Work/Assembly'/f'S04_{f:04d}.png',compress_level=1)
 if f in [1,97,133,151,182,245,254,290,318,350,404,432]:im.save(B/'Previews'/f'S04_review_{f:04d}_v019.png')
video=B/'Previews/S04_continuous-camera_v019.mp4'
r=subprocess.run([str(FF),'-y','-framerate','24','-i',str(B/'Work/Assembly/S04_%04d.png'),'-frames:v','432','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],capture_output=True,text=True);(B/'Records/encode.log').write_text(r.stderr);assert r.returncode==0
r=subprocess.run([str(FF),'-i',str(video),'-map','0:v:0','-f','null','-'],capture_output=True,text=True);(B/'Records/decode.log').write_text(r.stderr);assert r.returncode==0 and re.search(r'frame=\s*432',r.stderr)
timings={}
for c,name,count in [('Main','timings-render.json',432),('C','timings-C-render.json',120)]:
 vals=[r['seconds'] for r in json.loads((B/'Records'/name).read_text())];assert len(vals)==count and max(vals)<5;timings[c]={'frames':count,'mean_seconds':statistics.mean(vals),'max_seconds':max(vals),'total_seconds':sum(vals)}
report={'video':str(video),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'full_decode':True,'frames':432,'fps':24,'duration_seconds':18,'resolution':[1280,720],'main_camera_uninterrupted':True,'main_source_each_output_frame':'Work/Main/S04_<same frame number>.png','C_window_range':[121,253],'C_slide_in':[121,133],'C_slide_out':[235,253],'timings':timings}
(B/'Records/delivery.json').write_text(json.dumps(report,indent=2));(B/'Records/C-window-score.json').write_text(json.dumps(rows,indent=2))
frames=[1,55,97,121,127,133,151,182,235,245,254,290,318,350,404,432];sheet=Image.new('RGB',(1280,816),(15,22,28));d=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
 im=Image.open(B/'Work/Assembly'/f'S04_{f:04d}.png');im.thumbnail((320,180));x=i%4*320;y=i//4*204;sheet.paste(im,(x,y));d.text((x+8,y+182),f'{(f-1)/24:.2f}s / frame {f}',font=small,fill='white')
sheet.save(B/'Previews/S04_contact-sheet_v019.jpg',quality=92)
print(json.dumps(report,indent=2))
