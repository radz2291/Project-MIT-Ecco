from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,hashlib,re,statistics
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',21);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
def sm(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
for f in range(1,433):
 im=Image.open(B/'Work/Frames'/f'S04_{f:04d}.png').convert('RGBA');layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
 for start,end,title in [(63,141,'Supported backing'),(175,261,'Reduced backing'),(318,450,'Inner-wall wear')]:
  if start<=f<=end:
   a=sm((f-start)/8)*sm((end-f)/8);box=d.textbbox((0,0),title,font=font);d.rounded_rectangle((16,17,48+box[2],58),radius=5,fill=(12,22,28,round(145*a)));d.text((30,25),title,font=font,fill=(225,235,240,round(255*a)))
 d.rectangle((0,692,1280,720),fill=(10,20,25,190));d.text((20,699),'ILLUSTRATIVE GEOMETRY AND RESPONSE — NOT FIELD DATA',font=small,fill=(205,220,225,255));im=Image.alpha_composite(im,layer).convert('RGB');im.save(B/'Work/Assembly'/f'S04_{f:04d}.png',compress_level=1)
 if f in [1,63,85,141,158,175,197,235,261,290,318,350,404,432]:im.save(B/'Previews'/f'S04_review_{f:04d}_v020.png')
video=B/'Previews/S04_sequential-camera_v020.mp4'
r=subprocess.run([str(FF),'-y','-framerate','24','-i',str(B/'Work/Assembly/S04_%04d.png'),'-frames:v','432','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],capture_output=True,text=True);(B/'Records/encode.log').write_text(r.stderr);assert r.returncode==0
r=subprocess.run([str(FF),'-i',str(video),'-map','0:v:0','-f','null','-'],capture_output=True,text=True);(B/'Records/decode.log').write_text(r.stderr);assert r.returncode==0 and re.search(r'frame=\s*432',r.stderr)
original=json.loads((B/'Records/timings-render.json').read_text());patch=json.loads((B/'Records/timings-patch.json').read_text());assert len(patch)==87 and [r['frame'] for r in patch]==list(range(175,262));merged={r['frame']:r for r in original};merged.update({r['frame']:r for r in patch});assert len(merged)==432
values=[r['seconds'] for r in merged.values()];assert max(values)<5
report={'video':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'frames':432,'fps':24,'duration_seconds':18,'resolution':[1280,720],'single_camera':True,'sequential_B_then_C':True,'split_screen':False,'comparison_window':False,'full_decode':True,'render_seconds_final_frame_mean':statistics.mean(values),'render_seconds_final_frame_max':max(values),'render_seconds_final_frame_sum':sum(values),'total_batch_render_seconds_including_C_timing_correction':sum(r['seconds'] for r in original+patch),'C_timing_correction_frames':len(patch),'source_time_scale_B_and_C':.64,'render_budget_under5_all_attempts':max(r['seconds'] for r in original+patch)<5}
(B/'Records/delivery.json').write_text(json.dumps(report,indent=2));(B/'Records/timings-final.json').write_text(json.dumps([merged[f] for f in sorted(merged)],indent=2))
frames=[1,40,63,85,120,141,158,175,197,235,261,290,318,350,404,432];sheet=Image.new('RGB',(1280,816),(15,22,28));d=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
 im=Image.open(B/'Work/Assembly'/f'S04_{f:04d}.png');im.thumbnail((320,180));x=i%4*320;y=i//4*204;sheet.paste(im,(x,y));d.text((x+8,y+182),f'{(f-1)/24:.2f}s / frame {f}',font=small,fill='white')
sheet.save(B/'Previews/S04_contact-sheet_v020.jpg',quality=92)
print(json.dumps(report,indent=2))
