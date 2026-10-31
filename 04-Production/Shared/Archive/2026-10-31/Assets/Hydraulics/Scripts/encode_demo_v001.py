"""Encode/decode local behavior frames, create review-only contact sheet."""
import subprocess,json,hashlib,re
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[5];TASK=ROOT/'04-Production/Records/Tasks/T-048';P=TASK/'Previews/Revision_v003';E=TASK/'Evidence';frames=sorted((P/'Frames_B').glob('Flow_B_f*.png'));assert len(frames)==96
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';video=P/'Hydraulics_behavior_B_v003.mp4'
subprocess.run([str(ff),'-y','-framerate','24','-i',str(P/'Frames_B/Flow_B_f%04d.png'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,capture_output=True)
probe=subprocess.run([str(ff),'-i',str(video)],capture_output=True).stderr.decode('utf-8',errors='replace')
decode=subprocess.run([str(ff),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],check=True,capture_output=True)
size=1280*720*3;assert len(decode.stdout)%size==0;count=len(decode.stdout)//size;assert count==96
for f in [1,48,96]:Image.frombytes('RGB',(1280,720),decode.stdout[(f-1)*size:f*size]).save(E/('encoded_B_f%04d_v003.png'%f))
assert '1280x720' in probe and re.search(r'24 fps',probe) and 'h264' in probe and 'yuv420p' in probe
sheet=Image.new('RGB',(1280,800),(18,22,26));d=ImageDraw.Draw(sheet)
for j,f in enumerate([1,13,25,37,49,61,73,85,96]):
 im=Image.open(frames[f-1]).convert('RGB');im.thumbnail((420,236));x=(j%3)*426;y=(j//3)*266;sheet.paste(im,(x,y+24));d.text((x+4,y+5),f'B / frame{f:03d}',fill='white')
sheet.save(E/'motion-contact_v003.jpg',quality=92)
(E/'encode-qa_v003.json').write_text(json.dumps(dict(path=video.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(video.read_bytes()).hexdigest(),bytes=video.stat().st_size,decoded_frames=count,width=1280,height=720,fps=24,duration_s=4,codec='h264',pixel_format='yuv420p',audio=False,complete_decode=True,source='Exact96 rendered B_v005 frames, no temporal synthesis',contact_sheet='Evidence/motion-contact_v003.jpg'),indent=2),encoding='utf-8')
print(json.dumps(dict(video=str(video),decoded_frames=count)))
