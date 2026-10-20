import json, subprocess, time, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
B=Path(__file__).resolve().parents[1]
R=B.parents[2]
FF=R/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
def folder(c):return B/('Test-2_Inner-Wear' if c=='D' else 'Test-1_Matched-Response')
def annotate(im, title, subtitle):
 im=im.convert('RGB');d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,57),fill=(20,27,32));d.text((16,7),title,font=font,fill='white');d.text((16,33),subtitle,font=small,fill=(181,207,217));d.rectangle((0,im.height-28,im.width,im.height),fill=(20,27,32));d.text((16,im.height-23),'ILLUSTRATIVE GEOMETRY AND RESPONSE | Not field data or direct imaging behind steel',font=small,fill=(181,207,217));return im
def label(c,f):
 t=(f-1)/24
 if c=='D':return 'Physical inner surface' if t<1.3 else 'Dashed: original inner surface' if t<2.3 else 'Cyan: current inner profile' if t<2.8 else 'Sensor-to-wall / reference-to-current comparison; not wall thickness'
 return 'Side sensor → inner steel' if t<1.2 else 'Contact / backing-influenced response / return' if t<1.95 else 'Response decay: same elapsed time in both views'
def run(args):
 p=subprocess.run([str(FF),'-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True);assert p.returncode==0,p.stderr
rows={}
for c in 'BCD':
 p=folder(c);out=p/'Work/Labeled'/c;out.mkdir(parents=True,exist_ok=True)
 for f in range(1,121):
  src=p/'Work'/f'{c}_{f:04d}.png';assert src.exists(),src
  im=Image.open(src);annotate(im,{'B':'SUPPORTED BACKING','C':'CHANNEL BACKING','D':'INNER-WALL WEAR — unchanged source geometry'}[c],label(c,f)).save(out/f'{f:04d}.png')
 dest=p/'Previews'/f'S04_{c}_test_v007.mp4';t=time.perf_counter();run(['-y','-framerate',24,'-i',out/'%04d.png','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p',dest]);rows[c]={'encode_seconds':time.perf_counter()-t,'file':str(dest)}
 run(['-i',dest,'-f','null','-'])
pair=folder('B')/'Previews/S04_BC_matched-response_v007.mp4'
run(['-y','-i',rows['B']['file'],'-i',rows['C']['file'],'-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-c:v','libx264','-crf',18,'-preset','fast','-pix_fmt','yuv420p',pair]);run(['-i',pair,'-f','null','-'])
for f,name in [(32,'Contact'),(72,'Response-decay')]:
 ims=[Image.open(folder(c)/'Work/Labeled'/c/f'{f:04d}.png') for c in 'BC'];im=Image.new('RGB',(1920,540));im.paste(ims[0],(0,0));im.paste(ims[1],(960,0));im.save(folder('B')/'Previews'/f'S04_BC_{name}_v007.png')
for f,name in [(20,'Physical'),(108,'Overlay')]:Image.open(folder('D')/'Work/Labeled/D'/f'{f:04d}.png').save(folder('D')/'Previews'/f'S04_D_{name}_v007.png')
stats={}
for c in 'BCD':
 data=json.loads((B/'Records'/f'timings-{c}.json').read_text());assert len(data)==120
 ts=[r['seconds'] for r in data];stats[c]={'frames':len(ts),'render_total_seconds':sum(ts),'mean_seconds':sum(ts)/len(ts),'max_seconds':max(ts)}
assert max(x['max_seconds'] for x in stats.values())<5
(B/'Records/media-verification.json').write_text(json.dumps({'videos':rows,'pair':str(pair),'decode':'Each of four MP4 files decoded completely without error; each source has 120 frames / 24fps / 5 seconds','render':stats},indent=2))
print(json.dumps(stats,indent=2))
