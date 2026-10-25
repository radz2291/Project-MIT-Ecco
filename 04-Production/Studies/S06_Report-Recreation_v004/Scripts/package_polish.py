from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,time,hashlib
B=Path(__file__).resolve().parents[1]
F=B.parents[1]/'Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
timings=json.loads((B/'Records/polish-render-timings.json').read_text());assert [x['frame'] for x in timings]==list(range(1,289));assert max(x['seconds'] for x in timings)<5
for f in range(1,289):
 with Image.open(B/f'Cache/polished/{f:04d}.png') as im:assert im.size==(1280,720);im.verify()
movie=B/'Previews/S06_cinematic-study_v004_polished.mp4';start=time.perf_counter()
run=subprocess.run([str(F),'-y','-framerate','24','-i',str(B/'Cache/polished/%04d.png'),'-frames:v','288','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],capture_output=True,text=True);assert run.returncode==0
(B/'Records/polish-encode.log').write_text(run.stderr);encoding=time.perf_counter()-start
decode=subprocess.run([str(F),'-v','error','-i',str(movie),'-map','0:v:0','-f','framemd5','-'],capture_output=True,text=True);assert decode.returncode==0 and not decode.stderr.strip();lines=[x for x in decode.stdout.splitlines() if x and not x.startswith('#')];assert len(lines)==288
(B/'Records/polish-decoded-frames.md5').write_text(decode.stdout)
contact=Image.new('RGB',(1600,1032),(11,18,25));draw=ImageDraw.Draw(contact)
for i,f in enumerate([72,96,108,120,145,172,192,204,212,220,228,236,240,248,264,288]):
 im=Image.open(B/f'Cache/polished/{f:04d}.png').convert('RGB');im.thumbnail((400,225));x=i%4*400;y=i//4*258;contact.paste(im,(x,y));draw.text((x+10,y+233),f'{(f-1)/24:.2f}s / {f}',fill=(225,235,245))
contact.save(B/'Previews/S06_polished-transition-review.jpg',quality=94)
# Dense consecutive-frame QA around each join, separate from the clean movie.
for label,frames in [('AB',range(96,125,2)),('BC',range(204,261,4))]:
 sheet=Image.new('RGB',(1600,744),(11,18,25));dr=ImageDraw.Draw(sheet)
 for i,f in enumerate(frames):
  im=Image.open(B/f'Cache/polished/{f:04d}.png').convert('RGB').resize((320,180));x=i%5*320;y=i//5*248;sheet.paste(im,(x,y));dr.text((x+8,y+190),f'Frame {f}',fill='white')
 sheet.save(B/f'Previews/S06_polished-{label}-consecutive.jpg',quality=94)
record={'duration_seconds':12,'frames':288,'fps':24,'resolution':[1280,720],'render_seconds':sum(x['seconds'] for x in timings),'mean_frame_seconds':sum(x['seconds'] for x in timings)/288,'maximum_frame_seconds':max(x['seconds'] for x in timings),'all_frames_under_five_seconds':True,'samples':'16 normally; 32 at frames 90-144; 48 at frames 228-258, saved as native keys','encoding_seconds':encoding,'full_decode_frames':len(lines),'decode_errors':0,'movie_sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'original_movie_preserved':(B/'Previews/S06_cinematic-study_v004.mp4').exists(),'review':'Scoped transition refinement; awaiting owner playback review.'}
record['total_batch_render_seconds_including_steel_fade_repair']=sum(x['seconds'] for x in json.loads((B/'Records/polish-first-pass-timings.json').read_text()))+sum(x['seconds'] for x in timings if x['frame']<=144)
(B/'Records/polish-delivery.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
