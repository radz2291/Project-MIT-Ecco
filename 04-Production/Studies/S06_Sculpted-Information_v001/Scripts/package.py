import json,subprocess,hashlib,statistics,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];P=B/'Previews'
ff=ROOT/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
results={}
for mode,total,name in [('proof',120,'S06_unfolding-proof_v001.mp4'),('journey',288,'S06_camera-report-study_v001.mp4')]:
    cache=B/f'Cache/{mode}';assert all((cache/f'{f:04d}.png').exists() for f in range(1,total+1))
    video=P/name
    subprocess.run([str(ff),'-y','-framerate','24','-i',str(cache/'%04d.png'),'-frames:v',str(total),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,capture_output=True)
    # Decode every delivered frame, not just the container metadata.
    proc=subprocess.Popen([str(ff),'-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stride=960*540*3;count=0
    while True:
        data=proc.stdout.read(stride)
        if not data:break
        assert len(data)==stride;count+=1
    assert proc.wait()==0 and count==total
    tt=json.loads((B/f'Records/{mode}-timings.json').read_text());assert len(tt)==total
    results[mode]={'frames':count,'fps':24,'duration_seconds':count/24,'resolution':[960,540],'average_frame_seconds':statistics.mean(x['seconds'] for x in tt),'maximum_frame_seconds':max(x['seconds'] for x in tt),'render_total_seconds':sum(x['seconds'] for x in tt),'all_frames_under_5_seconds':all(x['seconds']<5 for x in tt),'all_encoded_frames_decoded':True,'video':video.relative_to(B).as_posix(),'sha256':hashlib.sha256(video.read_bytes()).hexdigest()}
    frames=[1,25,49,73,97,120] if mode=='proof' else [1,49,73,97,121,145,169,193,217,241,265,288]
    sheet=Image.new('RGB',(960,300*((len(frames)+1)//2)),(15,23,29));dr=ImageDraw.Draw(sheet)
    for i,f in enumerate(frames):
        im=Image.open(cache/f'{f:04d}.png').convert('RGB');im.thumbnail((480,270));x=i%2*480;y=i//2*300;sheet.paste(im,(x,y+30));dr.text((x+12,y+1),f'{(f-1)/24:.2f}s',font=font,fill=(180,200,211))
    sheet.save(P/f'{mode}-motion-sampling.jpg',quality=91)
sheet=Image.new('RGB',(1280,3*760),(15,23,29));dr=ImageDraw.Draw(sheet)
for i,(name,label) in enumerate([('01_Sculptural','01 / Sculptural arrival'),('02_Transformation','02 / Opening the same data'),('03_Information','03 / Illustrative report')]):
    im=Image.open(P/f'S06_arrival_{name}.png');sheet.paste(im,(0,i*760+40));dr.text((25,i*760+7),label,font=font,fill=(210,225,232))
sheet.save(P/'S06_three-arrivals.jpg',quality=93)
(B/'Records/media-verification.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
