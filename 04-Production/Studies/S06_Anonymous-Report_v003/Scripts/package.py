from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json,hashlib,numpy as np
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];BASE=B.with_name('S06_Sculpted-Information_v002')
checks=[]
for f in (1,142,216):
    old=np.array(Image.open(BASE/f'Cache/journey/{f:04d}.png'));new=np.array(Image.open(B/f'Previews/check_{f:03d}.png'))
    diff=abs(old.astype(int)-new.astype(int));checks.append({'frame':f,'pixel_equal':bool(np.array_equal(old,new)),'max_channel_difference':int(diff.max()),'mean_channel_difference':float(diff.mean())})
    assert np.array_equal(old,new),checks[-1]
for f in range(1,217):assert hashlib.sha256((BASE/f'Cache/journey/{f:04d}.png').read_bytes()).digest()==hashlib.sha256((B/f'Cache/journey/{f:04d}.png').read_bytes()).digest()
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
video=B/'Previews/S06_cinematic-study_v003.mp4'
subprocess.run([str(ff),'-y','-framerate','24','-i',str(B/'Cache/journey/%04d.png'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,capture_output=True)
decode=subprocess.run([str(ff),'-v','error','-i',str(video),'-f','null','-','-progress','pipe:1'],check=True,capture_output=True,text=True)
count=[int(x.split('=')[1]) for x in decode.stdout.splitlines() if x.startswith('frame=')][-1];assert count==288
ending=B/'Previews/S06_ending-only_v003.mp4'
subprocess.run([str(ff),'-y','-ss','9','-i',str(video),'-t','3','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(ending)],check=True,capture_output=True)
sheet=Image.new('RGB',(1280,3*386),(9,17,24));draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
for i,f in enumerate((216,224,232,240,252,288)):
    im=Image.open(B/f'Cache/journey/{f:04d}.png');im.thumbnail((640,360));x=(i%2)*640;y=(i//2)*386
    sheet.paste(im,(x,y+26));draw.text((x+12,y+2),'%.2f s'%((f-1)/24),font=font,fill=(180,199,209))
sheet.save(B/'Previews/S06_ending-contact_v003.jpg',quality=92)
t=json.loads((B/'Records/render-timings.json').read_text());assert len(t)==72 and max(v['seconds'] for v in t)<5
out={'decoded_frames':count,'duration_seconds':12,'first_216_source_frames_identical':True,'native_early_frame_comparisons':checks,'revised_frame_count':72,'render_seconds_total':sum(v['seconds'] for v in t),'mean_seconds_per_frame':sum(v['seconds'] for v in t)/72,'max_seconds_per_frame':max(v['seconds'] for v in t),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'decode_errors':decode.stderr}
(B/'Records/media-verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
