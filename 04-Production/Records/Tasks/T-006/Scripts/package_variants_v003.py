"""Encode/fully decode previews and prepare visual QA sheets from actual renders."""
import json,subprocess,time,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006';BASE=TASK/'Previews/v003'
ff=imageio_ffmpeg.get_ffmpeg_exe();rows=json.loads((TASK/'Evidence/preview-renders_v003.json').read_text())
qa=[];review=Image.new('RGB',(1600,5*345),'#101823');d=ImageDraw.Draw(review)
for row_index,row in enumerate(rows):
    name=row['name'];folder=BASE/name;video=BASE/f'B102_{name}_v003.mp4'
    title=f'T6 / {name} / PROVISIONAL ILLUSTRATION'
    bottom='Accepted T5 v002 | Orange adapters and bit are proxies | O05 open before technical lock'
    vf="drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+title+"':x=35:y=30:fontsize=25:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+bottom+"':x=35:y=660:fontsize=20:fontcolor=white"
    t=time.perf_counter()
    p=subprocess.run([ff,'-y','-framerate','24','-i',str(folder/'Frames/frame_%04d.png'),'-vf',vf,
                      '-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(video)],capture_output=True,text=True)
    (TASK/f'Evidence/encode-{name}_v003.txt').write_text(p.stderr,encoding='utf-8');p.check_returncode()
    dec=subprocess.run([ff,'-v','error','-i',str(video),'-f','null','-'],capture_output=True,text=True)
    dec.check_returncode();assert not dec.stderr.strip()
    reader=imageio_ffmpeg.read_frames(str(video),pix_fmt='rgb24');meta=next(reader);count=0;samples={}
    target=[1,row['frames']//3,2*row['frames']//3,row['frames']]
    for i,frame in enumerate(reader,1):
        count=i
        if i in target:samples[i]=Image.frombytes('RGB',(1280,720),frame)
    assert count==row['frames'] and meta['size']==(1280,720) and meta['fps']==24 and abs(meta['duration']-count/24)<.05
    d.text((15,row_index*345+5),name.upper(),fill='white',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24))
    for j,(frame,im) in enumerate(samples.items()):
        review.paste(im.resize((400,225)),(j*400,row_index*345+40))
        d.text((j*400+10,row_index*345+275),f'Frame {frame}',fill='white')
    # All actual frames, in sequence, for complete visual frame inspection.
    for page in range((count+23)//24):
        sheet=Image.new('RGB',(1280,1200),'#101823');draw=ImageDraw.Draw(sheet)
        for j in range(24):
            frame=page*24+j+1
            if frame>count:break
            with Image.open(folder/f'Frames/frame_{frame:04d}.png') as im:sheet.paste(im.resize((320,180)),((j%4)*320,(j//4)*200))
            draw.text(((j%4)*320+10,(j//4)*200+183),str(frame),fill='white')
        sheet.save(folder/f'all-frames-{page+1}_v003.jpg')
    qa.append({'name':name,'video':str(video.relative_to(ROOT.parent)).replace('\\','/'),
               'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'frames':count,'metadata':meta,
               'decode_errors':dec.stderr,'encode_decode_seconds':time.perf_counter()-t,'audio':'none'})
review.save(BASE/'B102_variants_review-sheet_v003.jpg')
# A single review cut makes all five cases easy to inspect.
concat=BASE/'concat_v003.txt';concat.write_text('\n'.join("file '"+str((ROOT.parent/q['video']).resolve()).replace('\\','/')+"'" for q in qa),encoding='utf-8')
combined=BASE/'B102_all-variants_v003.mp4'
p=subprocess.run([ff,'-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(combined)],capture_output=True,text=True);p.check_returncode()
reader=imageio_ffmpeg.read_frames(str(combined),pix_fmt='rgb24');meta=next(reader);total=sum(1 for frame in reader)
assert total==sum(q['frames'] for q in qa)
qa.append({'name':'all-variants','video':str(combined.relative_to(ROOT.parent)).replace('\\','/'),'frames':total,
           'metadata':meta,'sha256':hashlib.sha256(combined.read_bytes()).hexdigest(),'audio':'none'})
(TASK/'Evidence/video-qa_v003.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
print('VIDEO_QA_PASS',[(r['name'],r['frames']) for r in qa])
