import json,subprocess,hashlib,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
video=B/'Previews/S06_cinematic-study_v002.mp4'
subprocess.run([str(ff),'-y','-framerate','24','-i',str(B/'Cache/journey/%04d.png'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,capture_output=True)
check=subprocess.run([str(ff),'-v','error','-i',str(video),'-f','null','-','-progress','pipe:1'],check=True,capture_output=True,text=True)
frames=[int(x.split('=')[1]) for x in check.stdout.splitlines() if x.startswith('frame=')];assert frames[-1]==288
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',23)
arr=Image.new('RGB',(1280,3*760),(9,17,24));draw=ImageDraw.Draw(arr)
for i,name in enumerate(['01  WONDER / 2.5 s','02  REVELATION / 5.9 s','03  UNDERSTANDING / 11.5 s']):
    im=Image.open(B/f'Previews/S06_arrival_{i+1:02d}_v002.png');arr.paste(im,(0,760*i+40));draw.text((24,760*i+8),name,font=font,fill=(180,199,209))
arr.save(B/'Previews/S06_three-arrivals_v002.jpg',quality=90)
sheet=Image.new('RGB',(1440,4*296),(9,17,24));draw=ImageDraw.Draw(sheet)
for i,f in enumerate([1,49,73,97,121,145,169,193,217,241,265,288]):
    im=Image.open(B/f'Cache/journey/{f:04d}.png');im.thumbnail((480,270));x=(i%3)*480;y=(i//3)*296
    sheet.paste(im,(x,y+26));draw.text((x+12,y+2),'%.2f s'%((f-1)/24),font=font,fill=(180,199,209))
sheet.save(B/'Previews/S06_motion-sampling_v002.jpg',quality=90)
timings=json.loads((B/'Records/render-timings.json').read_text(encoding='utf-8'))
assert len(timings)==288 and max(x['seconds'] for x in timings)<5
out={'video':video.name,'frames_decoded':frames[-1],'fps':24,'duration_seconds':12,'resolution':[1280,720],'render_seconds_total':sum(x['seconds'] for x in timings),'average_seconds_per_frame':sum(x['seconds'] for x in timings)/len(timings),'maximum_seconds_per_frame':max(x['seconds'] for x in timings),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'decode_errors':check.stderr}
(B/'Records/media-verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
