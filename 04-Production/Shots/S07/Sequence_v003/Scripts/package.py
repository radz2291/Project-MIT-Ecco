from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,time,hashlib,shutil
B=Path(__file__).resolve().parents[1];R=B.parents[3]
FF=R/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
timings=json.loads((B/'Records/render-timings.json').read_text());assert [r['frame'] for r in timings]==list(range(1,193));assert max(r['seconds'] for r in timings)<5
for f in range(1,193):
 with Image.open(B/f'Cache/frames/{f:04d}.png') as im:assert im.size==(1280,720);im.verify()
def run(args,name):
 t=time.perf_counter();r=subprocess.run([str(FF)]+args,capture_output=True,text=True);(B/f'Records/{name}.log').write_text(r.stderr);assert r.returncode==0,r.stderr[-1200:];return r,time.perf_counter()-t
movie=B/'Previews/S07_Monumental-Precision_v003.mp4'
_,encode_seconds=run(['-y','-framerate','24','-i',str(B/'Cache/frames/%04d.png'),'-frames:v','192','-vf',"drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill:enable='gte(n,189)'",'-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],'encode')
transition=B/'Previews/S06-to-S07_transition_v003.mp4'
s06=R/'04-Production/Studies/S06_Report-Recreation_v004/Previews/S06_cinematic-study_v004_polished.mp4'
run(['-y','-sseof','-2','-i',str(s06),'-i',str(movie),'-filter_complex','[0:v]setpts=PTS-STARTPTS,setsar=1[a];[1:v]setpts=PTS-STARTPTS,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(transition)],'transition-encode')
decode_results={}
for p,count in [(movie,192),(transition,240)]:
 r,_=run(['-v','error','-i',str(p),'-map','0:v:0','-f','framemd5','-'],p.stem+'-decode');lines=[x for x in r.stdout.splitlines() if x and not x.startswith('#')];assert len(lines)==count and not r.stderr.strip()
 (B/f'Records/{p.stem}-frames.md5').write_text(r.stdout);decode_results[p.name]={'decoded_frames':len(lines),'errors':0,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
shutil.copy2(B/'Cache/frames/0160.png',B/'Previews/S07_final-product-hero_v003.png')
shutil.copy2(B/'Cache/frames/0084.png',B/'Previews/S07_second-beauty_v003.png')
def sheet(name,frames,cols=4):
 w,h=320,202;out=Image.new('RGB',(cols*w,((len(frames)+cols-1)//cols)*h),(12,18,23));d=ImageDraw.Draw(out)
 for i,f in enumerate(frames):
  im=Image.open(B/f'Cache/frames/{f:04d}.png').convert('RGB').resize((320,180));x=i%cols*w;y=i//cols*h;out.paste(im,(x,y));d.text((x+8,y+184),f'{(f-1)/24:.2f}s / frame {f}',fill=(220,230,238))
 out.save(B/f'Previews/{name}.jpg',quality=93)
sheet('S07_sequence-review',[1,24,36,48,60,72,84,96,112,132,148,160,172,178,184,192])
sheet('S07_motion-review',list(range(65,154,4)),cols=6)
for f in [190,191,192]:
 assert max(v[1] for v in Image.open(B/f'Cache/frames/{f:04d}.png').convert('RGB').getextrema())<=1 # Blender output dither; encoder pins last three frames to black.
record={'duration_seconds':8,'frames':192,'fps':24,'resolution':[1280,720],'render_total_seconds':sum(r['seconds'] for r in timings),'render_average_seconds':sum(r['seconds'] for r in timings)/192,'render_max_seconds':max(r['seconds'] for r in timings),'samples':32,'all_complete_frames_under_five_seconds':True,'encode_seconds':encode_seconds,'transition_preview_seconds':10,'transition_source':str(s06),'media':decode_results,'new_render_seconds':sum(r['seconds'] for r in timings if not r.get('reused_from')),'newly_rendered_frames':192,'reused_unchanged_frames':0,'review_status':'S07 v003 continuous camera and centered fade to black; owner review pending'}
(B/'Records/delivery.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))
