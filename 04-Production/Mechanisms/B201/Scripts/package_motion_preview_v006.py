"""Encode, decode every delivered frame, and create targeted review evidence."""
import json,subprocess,hashlib,statistics,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Cache/python'))
import numpy as np
import imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[3]; M=P/'Mechanisms/B201'; E=P/'Records/Tasks/T-007/Evidence/Motion_v006'; folder=M/'Previews/Motion_v006/Frames'; out=M/'Previews/Motion_v006/B201_pulse-echo_refinement_v006.mp4'
record=json.loads((E/'build.json').read_text()); times=json.loads((E/'render-times.json').read_text()); assert json.loads((E/'verification.json').read_text())['passed']
assert len(times)==240 and all((folder/f'frame_{f:04d}.png').is_file() for f in range(1,241))
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-framerate','24','-start_number','1','-i',str(folder/'frame_%04d.png'),'-frames:v','240','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(out)]
p=subprocess.run(cmd,capture_output=True,text=True); (E/'encode.log').write_text(p.stderr); assert p.returncode==0,p.stderr[-1000:]
reader=imageio_ffmpeg.read_frames(str(out),pix_fmt='rgb24'); metadata=next(reader); variances=[]; hashes=[]; decoded=E/'Decoded'; decoded.mkdir(exist_ok=True)
selected=set(range(1,241,6))|{24,36,38,39,40,42,44,46,54,60,66,72,100,124,143,150,163,176,191,198,210,222,240}
for count,data in enumerate(reader,1):
 a=np.frombuffer(data,dtype=np.uint8).reshape(metadata['size'][1],metadata['size'][0],3); variances.append(float(a.std())); hashes.append(hashlib.sha256(data).hexdigest())
 if count in selected: Image.fromarray(a).save(decoded/f'f{count:03d}.png')
assert count==240 and metadata['size']==(960,540) and metadata['fps']==24 and min(variances)>10
summary=dict(video=str(out.relative_to(P)),video_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),decoded_frames=count,size=list(metadata['size']),fps=metadata['fps'],duration_seconds=metadata['duration'],silent=True,min_decoded_std=min(variances),distinct_decoded_frames=len(set(hashes)),mean_render_seconds=statistics.mean(x['seconds'] for x in times),max_render_seconds=max(x['seconds'] for x in times),all_delivery_frames_under10seconds=max(x['seconds'] for x in times)<10,executor_media_qa=True)
(E/'video-qa.json').write_text(json.dumps(summary,indent=2))
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
def sheet(frames,path,title):
 canvas=Image.new('RGB',(1280,45+int(np.ceil(len(frames)/4))*204),(13,17,21)); d=ImageDraw.Draw(canvas); d.text((16,10),title,font=font,fill='white')
 for i,f in enumerate(frames):
  im=Image.open(decoded/f'f{f:03d}.png').resize((320,180)); x=(i%4)*320; y=45+(i//4)*204; canvas.paste(im,(x,y)); d.text((x+7,y+181),f'Frame {f} / {(f-1)/24:.2f}s',font=font,fill=(180,193,200))
 canvas.save(path)
for i in range(4):
 frames=[f for f in range(1,241,6) if i*60<f<=(i+1)*60]; sheet(frames,E/f'motion-sheet_{i+1:02d}.png',f'B201 v006 chronological decoded sequence — part {i+1}/4')
sheet([24,36,38,39,40,42,44,46,54,60,72,100],M/'Previews/Motion_v006/B201_director-review_v006.png','B201 v006 — propagation / reflection / local contact / reception / timing')
for f,label in ((36,'contact'),(44,'return'),(72,'timing')): shutil.copy2(decoded/f'f{f:03d}.png',M/f'Previews/Motion_v006/B201_{label}_v006.png')
# Matched phase comparison, with preserved v005 on the left.
before=M/'Previews/Motion_v005/B201_inspect_f038_v005.png'; after=decoded/'f044.png'; pair=Image.new('RGB',(1920,580),(13,17,21)); pair.paste(Image.open(before),(0,40)); pair.paste(Image.open(after),(960,40)); d=ImageDraw.Draw(pair); d.text((18,9),'Preserved v005 — eight frames after contact',font=font,fill='white'); d.text((978,9),'v006 — eight frames after contact',font=font,fill='white'); pair.save(M/'Previews/Motion_v006/B201_before-after_v006.png')
manifest={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/record['scene'],out,M/'Previews/Motion_v006/B201_director-review_v006.png',M/'Previews/Motion_v006/B201_before-after_v006.png']}; (E/'output-manifest.json').write_text(json.dumps(manifest,indent=2)); print(json.dumps(summary,indent=2))
