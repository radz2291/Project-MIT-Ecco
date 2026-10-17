"""Encode/decode exact full saved-consumer render; chronological review sheets."""
import json,hashlib,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
try:import imageio_ffmpeg
except ModuleNotFoundError:
    sys.path.insert(0,str(Path.home()/'.cache/codex-b202m-deps'));import imageio_ffmpeg
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';P=B/'Previews/MotionRevision_v007b';E=R/'04-Production/Records/Tasks/T-027/Evidence';files=sorted((P/'Frames').glob('frame_*.png'));assert len(files)==720,len(files)
video=P/'B202-M_motion-revision_v007b.mp4';cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-framerate','24','-start_number','1','-i',str(P/'Frames/frame_%04d.png'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
r=subprocess.run(cmd,capture_output=True,text=True);(E/'encode_motion-revision_v007b.log').write_text(r.stderr);assert r.returncode==0
reader=imageio_ffmpeg.read_frames(str(video),pix_fmt='rgb24');meta=next(reader);n=0;diff=[];previous=None;frames={};means=[]
selected=(1,7,60,168,240,336,384,480,552,601,648,684,720)
for raw in reader:
    frame=np.frombuffer(raw,dtype=np.uint8).reshape((540,960,3));n+=1;means.append(float(frame.mean()))
    if previous is not None:diff.append(float(np.abs(frame.astype(float)-previous).mean()))
    if n in selected or n%12==0:frames[n]=Image.fromarray(frame.copy())
    previous=frame.astype(float)
reader.close();assert n==720 and abs(meta['fps']-24)<.01 and abs(meta['duration']-30)<.05 and min(means)>2
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
def sheet(items,path,title,cols=3,width=480):
    height=round(width*540/960);rows=(len(items)+cols-1)//cols;im=Image.new('RGB',(cols*width,45+rows*(height+28)),(16,20,26));d=ImageDraw.Draw(im);d.text((18,10),title,font=font,fill='white')
    for i,(f,pic) in enumerate(items):
        x=(i%cols)*width;y=45+(i//cols)*(height+28);im.paste(pic.resize((width,height)),(x,y));d.text((x+10,y+height+3),f'Frame {f:03d} / {(f-1)/24:.2f}s',font=font,fill='white')
    im.save(path,quality=92)
sheet([(f,frames[f]) for f in selected],P/'B202-M_review-sheet_v007b.jpg','B202-M full mechanical v007b / 30s / synthetic examples')
sequence=[(f,frames[f]) for f in range(12,721,12)]
for j in range(5):sheet(sequence[j*12:(j+1)*12],P/f'chronological_{j+1:02d}_v007b.jpg',f'v007b chronological sample sheet {j+1}/5 / each 0.5s')
for f in selected:frames[f].save(P/f'decoded_{f:04d}.jpg',quality=94)
html='''<!doctype html><html><head><meta charset="utf-8"><title>B202-M full mechanical v007b</title><style>body{margin:36px auto;max-width:1100px;background:#12171d;color:#e2e9ef;font:17px Segoe UI,sans-serif}video{width:100%}p{line-height:1.5;color:#b8c6d2}button{padding:10px;margin:4px;background:#304957;color:white;border:0;border-radius:5px}</style></head><body><h1>The Shape Left Behind — full mechanical v007b</h1><p>30seconds · 720frames ·24fps ·960×540 · synthetic recorded examples · human review pending</p><video id="v" controls src="B202-M_motion-revision_v007b.mp4"></video><div><button onclick="v.currentTime=0;v.play()">Measurement</button><button onclick="v.currentTime=5.5;v.play()">Expected / measured</button><button onclick="v.currentTime=9;v.play()">Depth discovery</button><button onclick="v.currentTime=14;v.play()">Enlargement / tight</button><button onclick="v.currentTime=18;v.play()">Spiral through depth</button><button onclick="v.currentTime=25;v.play()">Acoustic variation</button><button onclick="v.playbackRate=.5;v.play()">Half speed</button><button onclick="v.playbackRate=1;v.play()">Normal speed</button></div><p>First14seconds retain the accepted opening for provenance. The reusable correction shows paired enlargement/tight examples with a source-camera5x inset, then source spiral contours/crest, a two-properties bridge and the independent varying acoustic-response field. Original data and fixed0–0.4 range remain; one declared contrast transfer applies to every warm frame. Separate case captions; no bit passage, new data, rock-type claims or unwrapping. This30second mechanism library is not a30second S03 shot. The report maps an18second selection for T15.</p><p>For a cold-viewer check: play with sound off without explaining the intended message first. Ask: Point to the tight location, trace the spiral through depth, explain what the warm response varies with, and distinguish the illustrative scenarios. Record the response verbatim before discussing it. Separate MIT technical interpretation/calibration review is still required.</p></body></html>'''
(P/'review_v007b.html').write_text(html,encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();outputs=[B/'Scenes/B202-M_motion-revision_v007b.blend',video,P/'B202-M_review-sheet_v007b.jpg',P/'review_v007b.html',E/'replay_manifest_v007b.json',E/'verification_motion-revision_v007b.json']
qa={'status':'PASS','decoded_frames':n,'fps':meta['fps'],'duration_s':meta['duration'],'width':960,'height':540,'nonblank_frame_mean_min':min(means),'adjacent_frame_mean_pixel_delta':{'min':min(diff),'max':max(diff),'mean':sum(diff)/len(diff)},'cut_frames':[337,433,529,601],'key_frames':list(selected),'chronological_sample_interval_frames':12,'outputs':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in outputs],'scope':'All720frames decoded/nonblank. Agent chronological visual inspection recorded separately; no human comprehension/acceptance inferred.'}
(E/'playback_qa_v007b.json').write_text(json.dumps(qa,indent=2));print(json.dumps({'status':'PASS','frames':n,'duration':meta['duration'],'video_bytes':video.stat().st_size}))
