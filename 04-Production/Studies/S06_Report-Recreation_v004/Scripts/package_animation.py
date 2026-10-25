from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,time,hashlib,shutil
B=Path(__file__).resolve().parents[1]
F=B.parents[1]/'Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
timings=json.loads((B/'Records/animation-render-timings.json').read_text())
assert [x['frame'] for x in timings]==list(range(1,289)) and max(x['seconds'] for x in timings)<5
for f in range(1,289):
    with Image.open(B/f'Cache/animation/{f:04d}.png') as im:assert im.size==(1280,720);im.verify()
movie=B/'Previews/S06_cinematic-study_v004.mp4';start=time.perf_counter()
encode=subprocess.run([str(F),'-y','-framerate','24','-i',str(B/'Cache/animation/%04d.png'),'-frames:v','288','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],capture_output=True,text=True)
(B/'Records/animation-encode.log').write_text(encode.stderr);assert encode.returncode==0
encode_seconds=time.perf_counter()-start
decode=subprocess.run([str(F),'-v','error','-i',str(movie),'-map','0:v:0','-f','framemd5','-'],capture_output=True,text=True)
assert decode.returncode==0 and not decode.stderr.strip()
decoded=[x for x in decode.stdout.splitlines() if x and not x.startswith('#')];assert len(decoded)==288
(B/'Records/animation-decoded-frames.md5').write_text(decode.stdout)
contact=Image.new('RGB',(1600,972),(11,18,25));draw=ImageDraw.Draw(contact)
for i,f in enumerate([1,48,96,120,144,168,192,216,230,244,264,288]):
    im=Image.open(B/f'Cache/animation/{f:04d}.png').convert('RGB');im.thumbnail((400,225));x=i%4*400;y=i//4*324;contact.paste(im,(x,y));draw.text((x+12,y+237),f'{(f-1)/24:.2f}s / frame {f}',fill=(220,235,245))
contact.save(B/'Previews/S06_animation-contact_v004.jpg',quality=92)
shutil.copy2(B/'Cache/animation/0276.png',B/'Previews/S06_animation-poster_v004.png')
result={'frames':288,'fps':24,'duration_seconds':12,'resolution':[1280,720],'engine':'EEVEE','samples':16,'render_sum_seconds':sum(t['seconds'] for t in timings),'render_mean_seconds':sum(t['seconds'] for t in timings)/288,'render_min_seconds':min(t['seconds'] for t in timings),'render_max_seconds':max(t['seconds'] for t in timings),'encoding_seconds':encode_seconds,'all_frames_under_five_seconds':True,'full_video_decode_frames':len(decoded),'decode_errors':0,'movie_sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'review_status':'Owner animation review pending','cold_shader_note':'Initial check shader compilation spikes are recorded separately; these statistics describe the final 288-frame production run.'}
initial=json.loads((B/'Records/animation-initial-run-timings.json').read_text())
result['total_batch_render_seconds_including_transition_repairs']=sum(t['seconds'] for t in initial)+sum(t['seconds'] for t in timings if t['frame']>=96)
result['transition_repairs']='Frames 96-288 rerendered after full-sequence QA: continuous target framing, complete-boundary framing checks, and depth-correct dithered laptop fade.'
(B/'Records/animation-delivery.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
