"""Encode the native frame sequence; decode every delivered frame for media QA."""
import json,subprocess,hashlib,statistics
from pathlib import Path
import numpy as np
import imageio_ffmpeg
from PIL import Image
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Motion_v002';folder=M/'Previews/Motion_v002/Frames';out=M/'Previews/Motion_v002/B201_pulse-echo_fast-preview_v002.mp4'
record=json.loads((E/'build.json').read_text());times=json.loads((E/'render-times.json').read_text())
assert len(times)==240 and max(x['seconds'] for x in times)<10
assert all((folder/f'frame_{f:04d}.png').is_file() for f in range(1,241))
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-framerate','24','-start_number','1','-i',str(folder/'frame_%04d.png'),'-frames:v','240','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(out)]
p=subprocess.run(cmd,capture_output=True,text=True);(E/'encode.log').write_text(p.stderr);assert p.returncode==0,p.stderr[-1000:]
reader=imageio_ffmpeg.read_frames(str(out),pix_fmt='rgb24');metadata=next(reader);count=0;variances=[];hashes=[];decode=E/'Decoded';decode.mkdir(exist_ok=True)
selected={1,18,28,36,48,50,107,126,185,202,204,240}
for count,data in enumerate(reader,1):
 a=np.frombuffer(data,dtype=np.uint8).reshape(metadata['size'][1],metadata['size'][0],3);variances.append(float(a.std()));hashes.append(hashlib.sha256(data).hexdigest())
 if count in selected:Image.fromarray(a).save(decode/f'decoded_f{count:03d}.png')
assert count==240 and metadata['size']==(960,540) and metadata['fps']==24
assert min(variances)>10 and len(set(hashes))>60
summary={'video':str(out.relative_to(P)),'video_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'decoded_frames':count,'size':list(metadata['size']),'fps':metadata['fps'],'duration_seconds':metadata['duration'],'silent':True,'min_decoded_std':min(variances),'distinct_decoded_frames':len(set(hashes)),'mean_render_seconds':statistics.mean(x['seconds'] for x in times),'max_render_seconds':max(x['seconds'] for x in times),'median_render_seconds':statistics.median(x['seconds'] for x in times),'all_frames_under10seconds':True,'Still05_included':False,'executor_media_qa':True}
(E/'video-qa.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
