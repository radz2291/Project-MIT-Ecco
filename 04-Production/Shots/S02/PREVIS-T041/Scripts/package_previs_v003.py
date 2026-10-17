"""Encode the cheap preview; decode every delivered frame; make review evidence.
Uses Pillow/numpy and FFMPEG_EXE or the existing local media-tool cache.
"""
import os,subprocess,json,hashlib,shutil,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];P=BASE.parents[2];E=P/'Records/Tasks/T-041/Evidence';V=BASE/'Previews/v003';F=V/'Frames'
ffmpeg=Path(os.environ.get('FFMPEG_EXE',str(P/'Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe')))
assert ffmpeg.is_file(),'Provide FFMPEG_EXE'
assert json.loads((E/'verification_v003.json').read_text())['passed']
assert all((F/f'frame_{i:04d}.png').is_file() for i in range(1,289))
video=V/'S02_previs_T041_v003.mp4'
cmd=[str(ffmpeg),'-y','-framerate','24','-start_number','1','-i',str(F/'frame_%04d.png'),'-frames:v','288','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(video)]
r=subprocess.run(cmd,capture_output=True,text=True);(E/'encode_v003.log').write_text(r.stderr);assert r.returncode==0,r.stderr
decode=subprocess.Popen([str(ffmpeg),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
selected={1,12,22,27,32,43,47,56,60,72,81,92,103,118,130,143,157,168,169,192,210,230,242,260,266,288}|set(range(1,289,6))
decoded={};hashes=[];stds=[];differences=[];source_errors=[];last=None;count=0
while True:
    chunk=decode.stdout.read(640*360*3)
    if not chunk:break
    assert len(chunk)==640*360*3
    count+=1;a=np.frombuffer(chunk,dtype=np.uint8).reshape(360,640,3)
    hashes.append(hashlib.sha256(chunk).hexdigest());stds.append(float(a.std()))
    source=np.array(Image.open(F/f'frame_{count:04d}.png').convert('RGB'))
    source_errors.append(float(np.abs(a.astype(float)-source.astype(float)).mean()))
    if last is not None:differences.append(float(np.abs(a.astype(float)-last).mean()))
    if count in selected:decoded[count]=Image.fromarray(a.copy())
    last=a.astype(float)
stderr=decode.stderr.read().decode();assert decode.wait()==0,stderr
assert count==288 and min(stds)>10 and max(source_errors)<3
probe=subprocess.run([str(ffmpeg),'-hide_banner','-i',str(video)],capture_output=True,text=True)
assert '640x360' in probe.stderr and '24 fps' in probe.stderr and '00:00:12.00' in probe.stderr
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
def sheet(frames,path,title):
    canvas=Image.new('RGB',(1280,42+math.ceil(len(frames)/4)*204),(12,18,24));d=ImageDraw.Draw(canvas);d.text((14,10),title,font=font,fill='white')
    for i,f in enumerate(frames):
        x=i%4*320;y=42+i//4*204;canvas.paste(decoded[f].resize((320,180)),(x,y));d.text((x+6,y+183),f'f{f:03d} / {(f-1)/24:.2f}s',font=font,fill=(190,210,220))
    canvas.save(path)
sheet([1,12,22,32,81,92,103,157,169,210,242,288],V/'S02_review-sheet_v003.jpg','T41 S02 v003 / saved-scene render, decoded MP4 / illustrative, review pending')
for part in range(4):
    frames=[f for f in range(1,289,6) if part*72<f<=(part+1)*72]
    sheet(frames,V/f'S02_motion-review_{part+1:02d}_v003.jpg',f'T41 v003 / chronological decoded frames / {part*3}–{part*3+3}s')
for f,label in [(1,'entry'),(22,'contact'),(32,'reception'),(103,'waveform'),(266,'ring'),(288,'exit')]:decoded[f].save(V/f'S02_{label}_v003.png')
qa=dict(video=str(video.relative_to(P)),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),decoded_frames=count,fps=24,size=[640,360],duration_seconds=count/24,silent=True,distinct_decoded_frames=len(set(hashes)),min_pixel_std=min(stds),max_mean_pixel_step=max(differences),static_hold_frames=22,verification_kind='executor decode and sampled-motion review; no independent cold-viewer result',ffmpeg=str(ffmpeg))
qa.update(max_source_to_decode_mean_error=max(source_errors),mean_source_to_decode_error=sum(source_errors)/len(source_errors),container_metadata_verified=True)
(E/'video-qa_v003.json').write_text(json.dumps(qa,indent=2))
html='''<!doctype html><meta charset="utf-8"><title>T41 · S02 previs v003</title><style>body{background:#101820;color:#dbe7ed;font:17px Segoe UI,sans-serif;max-width:1000px;margin:36px auto}video,img{width:100%;height:auto}p{line-height:1.5}a{color:#8cdeea}</style><h1>S02 — First ping</h1><p>T41 / MIT ECCO - PREVIS / experimental v003. 12 seconds, 640×360, 24 fps, silent. Gray blocking preview; not final look or approved production animation.</p><video controls preload="metadata" src="S02_previs_T041_v003.mp4" poster="S02_entry_v003.png"></video><p>First contact 0–3s → returning time 3–7s → surrounding outline 7–12s. Signals, waveform, timing and wall samples are synthetic illustrations. CGI cutaway suppresses rock/mud; the final ring uses an x-ray data overlay. Acoustic-face location and actual deployment orientation remain unverified.</p><p>Review after watching: What returns to ECCO? What does the timing reveal? Why do repeated readings matter? Human comprehension and MIT technical review remain pending.</p><img src="S02_review-sheet_v003.jpg"><p><a href="../../Scenes/S02_previs_T041_v003.blend">Editable local Blender scene</a> · <a href="../../direction.md">Direction and limits</a></p>'''
(V/'review_v003.html').write_text(html,encoding='utf8')
print(json.dumps(qa,indent=2))
