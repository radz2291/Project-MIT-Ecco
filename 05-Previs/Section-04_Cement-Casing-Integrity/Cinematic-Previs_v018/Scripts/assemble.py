from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,time,statistics,hashlib
B=Path(__file__).resolve().parents[1];P=B.parent;ROOT=B.parents[2]
FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',21)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
out=B/'Work/Assembly';out.mkdir(exist_ok=True)
def footer(im):
 layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
 d.rectangle((0,692,1280,720),fill=(10,20,25,190))
 d.text((20,699),'ILLUSTRATIVE GEOMETRY AND RESPONSE — NOT FIELD DATA',font=small,fill=(205,220,225,255))
 return Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
for f in range(1,433):
 if f<=96:im=Image.open(P/'Cinematic-Previs_v006/Work'/f'S04_{f:04d}.png').convert('RGB')
 elif f<=264:
  local=f-97;src=1 if local<24 else min(120,local-23)
  im=Image.new('RGB',(1280,720))
  for i,c in enumerate('BC'):
   panel=Image.open(B/'Work'/c/f'{c}_{src:04d}.png').convert('RGB');assert panel.size==(640,720)
   im.paste(panel,(640*i,0))
  layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
  d.rectangle((0,0,1280,54),fill=(10,20,25,205));d.line((640,0,640,692),fill=(160,185,195,200),width=2)
  d.text((24,15),'CEMENT BACKING',font=font,fill=(220,233,238,255))
  d.text((664,15),'REDUCED BACKING',font=font,fill=(220,233,238,255))
  im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
 else:im=Image.open(B/'Work/D'/f'D_{f-264:04d}.png').convert('RGB')
 assert im.size==(1280,720)
 im=footer(im);im.save(out/f'S04_{f:04d}.png')
 for target,name in [(48,'Entry'),(151,'Contact'),(182,'Response-comparison'),(278,'Physical-wear'),(337,'Wear-profiles'),(420,'Computed-wear')]:
  if f==target:im.save(B/'Previews'/f'S04_{name}_v018.png')
video=B/'Previews/S04_complete-previs_v018.mp4'
t=time.perf_counter()
args=[str(FF),'-y','-framerate','24','-i',str(out/'S04_%04d.png'),'-frames:v','432','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
r=subprocess.run(args,capture_output=True,text=True);(B/'Records/encode.log').write_text(r.stderr);assert r.returncode==0
decode=subprocess.run([str(FF),'-i',str(video),'-map','0:v:0','-f','null','-'],capture_output=True,text=True)
(B/'Records/decode.log').write_text(decode.stderr);assert decode.returncode==0 and 'frame=  432' in decode.stderr
timings={}
for c in 'BCD':
 rows=json.loads((B/'Records'/f'timings-{c}.json').read_text());vals=[r['seconds'] for r in rows]
 assert len(vals)==(168 if c=='D' else 120) and max(vals)<5
 timings[c]={'frames':len(vals),'mean_seconds':statistics.mean(vals),'max_seconds':max(vals),'min_seconds':min(vals),'total_seconds':sum(vals)}
report={'duration_seconds':18,'fps':24,'frames':432,'resolution':[1280,720],'video':str(video),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'full_video_decode':True,'render_timings':timings,'reused_A_frames':96,'new_native_frames':408,'timeline':[{'part':'A','frames':[1,96]},{'part':'B+C synchronized 50/50','frames':[97,264],'source_timing':'1s establish, original5s mechanism,1s response hold'},{'part':'D','frames':[265,432]}],'no_frame_squashing':True,'encode_and_decode_seconds':time.perf_counter()-t,'prior_versions_preserved':True}
(B/'Records/delivery.json').write_text(json.dumps(report,indent=2))
# Chronological visual review at useful transitions and discovery states.
frames=[1,48,96,97,133,151,166,182,214,264,265,278,305,337,396,432]
sheet=Image.new('RGB',(1280,4*204),(15,22,28));d=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
 im=Image.open(out/f'S04_{f:04d}.png');im.thumbnail((320,180));x=(i%4)*320;y=(i//4)*204;sheet.paste(im,(x,y));d.text((x+8,y+182),f'{(f-1)/24:.2f}s / frame {f}',font=small,fill='white')
sheet.save(B/'Previews/S04_contact-sheet_v018.jpg',quality=92)
print(json.dumps(report,indent=2))
