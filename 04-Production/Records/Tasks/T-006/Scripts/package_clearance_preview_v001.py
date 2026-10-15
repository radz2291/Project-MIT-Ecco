"""Review encoding and complete-video decode verification; raw renders preserved."""
import subprocess,json,time
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006'
frames=TASK/'Previews/clearance-frames_v001'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
video=TASK/'Previews/B102_clearance-fixture_v001.mp4'
filters="drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='T6  /  Accepted T5 v002 - minimum-ID clearance fixture':x=40:y=35:fontsize=25:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='12.3in published ID limit | 360deg + 100mm control test | No selected well or BHA':x=40:y=655:fontsize=19:fontcolor=white"
t=time.perf_counter()
cmd=[ffmpeg,'-y','-framerate','24','-i',str(frames/'frame_%04d.png'),'-vf',filters,
     '-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(video)]
r=subprocess.run(cmd,capture_output=True,text=True)
(TASK/'Evidence/video-encode_v001.txt').write_text(r.stderr,encoding='utf-8');r.check_returncode()
decode=subprocess.run([ffmpeg,'-v','error','-i',str(video),'-f','null','-'],capture_output=True,text=True)
decode.check_returncode();assert not decode.stderr.strip(),decode.stderr
reader=imageio_ffmpeg.read_frames(str(video),pix_fmt='rgb24')
metadata=next(reader);count=0;selected={}
for i,data in enumerate(reader,1):
    count=i
    if i in (1,13,25,37,49,61,73,85,96):selected[i]=Image.frombytes('RGB',(1280,720),data)
assert count==96 and metadata['size']==(1280,720) and abs(metadata['fps']-24)<.001 and abs(metadata['duration']-4)<.05
# Contact sheet samples the entire motion in chronological order.
sheet=Image.new('RGB',(1440,900),'#101823');d=ImageDraw.Draw(sheet)
for n,(frame,im) in enumerate(selected.items()):
    x=(n%3)*480;y=(n//3)*300
    sheet.paste(ImageOps.contain(im,(480,270)),(x,y));d.text((x+12,y+275),f'Frame {frame:03d} / {(frame-1)/24:.2f}s',fill='white')
sheet.save(TASK/'Previews/B102_clearance-motion-sheet_v001.jpg')
for page in range(4):
    allsheet=Image.new('RGB',(1280,1200),'#101823');draw=ImageDraw.Draw(allsheet)
    for j in range(24):
        frame=page*24+j+1;x=(j%4)*320;y=(j//4)*200
        with Image.open(frames/f'frame_{frame:04d}.png') as raw:
            allsheet.paste(raw.resize((320,180)),(x,y))
        draw.text((x+8,y+183),f'{frame:03d}',fill='white')
    allsheet.save(TASK/f'Previews/all-frames-{page+1}_v001.jpg')
summary={'path':str(video.relative_to(ROOT.parent)).replace('\\','/'),'frames_decoded':count,
         'metadata':metadata,'decode_errors':decode.stderr,'encode_and_decode_seconds':time.perf_counter()-t,
         'audio':'none','limit':'Fixture/test-motion preview only; not a mechanical film shot or confirmed deployment'}
(TASK/'Evidence/video-qa_v001.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
