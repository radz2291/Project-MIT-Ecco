"""Encode and decode the complete preview; save review player and evidence."""
import json,hashlib,subprocess
from pathlib import Path
import numpy as np
import imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';P=B/'Previews/MotionProof_v002';E=R/'04-Production/Records/Tasks/T-027/Evidence'
files=sorted((P/'Frames').glob('frame_*.png'));assert len(files)==192,len(files)
video=P/'B202-M_motion-proof_v002.mp4'
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-framerate','24','-start_number','1','-i',str(P/'Frames/frame_%04d.png'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
r=subprocess.run(cmd,capture_output=True,text=True);(E/'encode_motion-proof_v002.log').write_text(r.stderr);assert r.returncode==0
reader=imageio_ffmpeg.read_frames(str(video),pix_fmt='rgb24');meta=next(reader);n=0;diff=[];previous=None;decoded=[]
for raw in reader:
    frame=np.frombuffer(raw,dtype=np.uint8).reshape((540,960,3))
    assert frame.shape[:2]==(540,960)
    if previous is not None:diff.append(float(np.abs(frame.astype(float)-previous).mean()))
    if n in (0,11,27,71,115,155,191):decoded.append((n+1,Image.fromarray(frame)))
    previous=frame.astype(float);n+=1
reader.close();assert n==192 and abs(meta['fps']-24)<.01 and abs(meta['duration']-8)<.05
sheet=Image.new('RGB',(1280,1180),(16,20,26));draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
draw.text((22,12),'B202-M / First motion proof v002 — illustrative acquisition replay',font=font,fill='white')
selected=[decoded[i] for i in (0,1,3,4,5,6)]
for i,(f,im) in enumerate(selected):
    x=(i%2)*640;y=55+(i//2)*370;sheet.paste(im.resize((640,360)),(x,y));draw.text((x+12,y+330),f'Frame {f:03d} / {(f-1)/24:.2f}s',font=font,fill='white')
sheet.save(P/'B202-M_review-sheet_v002.jpg',quality=92)
for f,im in decoded:im.save(P/f'decoded_{f:04d}.jpg',quality=94)
html='''<!doctype html><html><head><meta charset="utf-8"><title>B202-M motion proof v002</title><style>body{margin:36px auto;max-width:1100px;background:#12171d;color:#e2e9ef;font:17px Segoe UI,sans-serif}video{width:100%;border-radius:8px}h1{font-size:25px}p{line-height:1.5;color:#b8c6d2}button{padding:10px;margin:4px;background:#304957;color:white;border:0;border-radius:5px}</style></head><body><h1>The Shape Left Behind — first motion proof v002</h1><p>8 seconds · v009 synthetic event replay · D2/D3 review pending</p><video id="v" controls loop src="B202-M_motion-proof_v002.mp4"></video><div><button onclick="v.currentTime=0;v.play()">Sensor event</button><button onclick="v.currentTime=2.5;v.play()">Ring accumulation</button><button onclick="v.currentTime=5.5;v.play()">Camera release</button><button onclick="v.playbackRate=.5;v.play()">Half speed</button><button onclick="v.playbackRate=1;v.play()">Normal speed</button></div><p>Discrete station replay: acquisition pauses during axial travel. Three source sensor events are grouped per orientation. Readings remain fixed in the well; this is recorded information, not live glowing rock or surface telemetry.</p><p>Review: does the moving instrument leave readable knowledge behind? Is the first event clear, and does the release make the depth relationship understandable? Full geometry/amplitude sequence follows targeted feedback.</p></body></html>'''
(P/'review_v002.html').write_text(html,encoding='utf-8')
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
outputs=[B/'Scenes/B202-M_motion-proof_v002.blend',video,P/'B202-M_review-sheet_v002.jpg',P/'review_v002.html',E/'replay_manifest_v002.json',E/'verification_motion-proof_v002.json']
qa={'status':'PASS','decoded_frames':n,'fps':meta['fps'],'duration_s':meta['duration'],'width':960,'height':540,'adjacent_frame_mean_pixel_delta':{'min':min(diff),'max':max(diff),'mean':sum(diff)/len(diff)},'visual_inspection_frames':[f for f,_ in decoded],'outputs':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashfile(p)} for p in outputs],'scope':'All frames decoded, dimensions/duration validated. Agent key-frame and sampled sequential inspection; human motion acceptance pending.'}
(E/'playback_qa_v002.json').write_text(json.dumps(qa,indent=2));print(json.dumps({'status':'PASS','frames':n,'duration':meta['duration'],'video_bytes':video.stat().st_size}))
