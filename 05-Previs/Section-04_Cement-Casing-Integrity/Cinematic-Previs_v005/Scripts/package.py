from pathlib import Path
import subprocess,json,statistics,hashlib,time
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
FF=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
P=B/'Previews';R=B/'Records';out=P/'S04_cinematic-previs_v005.mp4'
caption="drawtext=fontfile='C\\:/Windows/Fonts/segoeui.ttf':text='ILLUSTRATIVE INTERPRETATION - NOT DIRECT FLUID IMAGERY':x=24:y=h-28:fontsize=13:fontcolor=white@0.7"
st=time.perf_counter();r=subprocess.run([str(FF),'-v','error','-y','-framerate','24','-i',str(B/'Work/S04_%04d.png'),'-frames:v','432','-vf',caption,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],capture_output=True,text=True);(R/'encode.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
encode=time.perf_counter()-st
for f,n in [(1,'Entry'),(116,'Supported-response'),(180,'Channel-response'),(292,'Organic-channel'),(432,'Inner-wear')]:
 subprocess.run([str(FF),'-v','error','-y','-i',str(B/'Work'/f'S04_{f:04d}.png'),'-vf',caption,'-frames:v','1',str(P/f'S04_{n}_v005.png')],check=True)
r=subprocess.run([str(FF),'-v','error','-i',str(out),'-f','framemd5','-'],capture_output=True,text=True,check=True);(R/'decode.txt').write_text(r.stdout);frames=[x for x in r.stdout.splitlines() if x and not x.startswith('#')];assert len(frames)==432
t=json.loads((R/'timings-render.json').read_text());assert len(t)==432 and max(v['seconds'] for v in t)<5
sources=json.loads((R/'source-manifest-full.json').read_text());assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in sources)
report=dict(duration_seconds=18,frames=432,fps=24,resolution=[1280,720],samples=4,renderer='EEVEE/Vulkan',mean_seconds_per_frame=statistics.mean(v['seconds'] for v in t),maximum_seconds_per_frame=max(v['seconds'] for v in t),total_render_seconds=sum(v['seconds'] for v in t),encoding_seconds=encode,all_frames_decoded=True,canonical_sources_unchanged=True,video_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),native_sha256=hashlib.sha256((B/'Scenes/S04_cinematic-previs_v005.blend').read_bytes()).hexdigest(),status='Owner-authorized complete cinematic previs, not final finishing or engineering acceptance',limits=['No narration sync or S03/S05 film assembly','Illustrative response/channel geometry, no direct photographed-fluid claim','Simple preview shading and visibility-mask grain','Machine/file startup excluded; empty-driver-cache timing unproven','Media local, no off-machine backup verified'])
report['superseded_full_batch_render_seconds']=sum(v['seconds'] for v in json.loads((R/'timings-superseded-entry-occlusion.json').read_text()))
report['both_full_batches_render_seconds']=report['total_render_seconds']+report['superseded_full_batch_render_seconds']
(R/'delivery.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
