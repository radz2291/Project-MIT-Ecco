import subprocess,json,time
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B.parents[2];FF=R/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
def run(args):
 p=subprocess.run([str(FF),'-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True);assert p.returncode==0,p.stderr
vid=[];report={}
for c in 'BC':
 rows=json.loads((B/'Records'/f'timings-{c}.json').read_text());assert len(rows)==120 and max(r['seconds'] for r in rows)<5
 dest=B/'Previews'/f'S04_{c}_formation-acquisition_v009.mp4';title='B - CEMENT BACKING' if c=='B' else 'C - FLUID CHANNEL OUTSIDE STEEL'
 filt=f"pad=iw:ih+100:0:50:color=0x172027,drawtext=fontfile='C\\:/Windows/Fonts/segoeui.ttf':text='{title}':x=20:y=10:fontsize=25:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/segoeui.ttf':text='Acquisition display finish - illustrative, not field data':x=20:y=h-35:fontsize=19:fontcolor=0xc6dce5"
 t=time.perf_counter();run(['-y','-framerate',24,'-i',B/'Work'/f'{c}_%04d.png','-vf',filt,'-c:v','libx264','-preset','fast','-crf',18,'-pix_fmt','yuv420p',dest]);run(['-i',dest,'-f','null','-']);vid.append(dest)
 report[c]={'frames':120,'fps':24,'duration_seconds':5,'resolution_with_caption_bars':[1280,820],'render_seconds':sum(r['seconds'] for r in rows),'mean_seconds_per_frame':sum(r['seconds'] for r in rows)/120,'max_seconds_per_frame':max(r['seconds'] for r in rows),'encode_decode_seconds':time.perf_counter()-t,'video':str(dest)}
pair=B/'Previews/S04_BC_matched-acquisition_v009.mp4';run(['-y','-i',vid[0],'-i',vid[1],'-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-c:v','libx264','-preset','fast','-crf',18,'-pix_fmt','yuv420p',pair]);run(['-i',pair,'-f','null','-'])
for f,name in [(1,'establish'),(25,'send'),(32,'contact'),(35,'glitch'),(55,'decay')]:
 run(['-y','-i',B/'Work'/f'B_{f:04d}.png','-i',B/'Work'/f'C_{f:04d}.png','-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-frames:v',1,B/'Previews'/f'S04_BC_{name}_unlabelled_v009.png'])
report['verification']='Three MP4 files completely decoded without errors. Both inputs 120 frames; same synchronized timing. No full18s integration.'
(B/'Records/media-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
