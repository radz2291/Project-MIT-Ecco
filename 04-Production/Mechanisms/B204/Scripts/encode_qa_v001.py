import json,subprocess,hashlib,time
from pathlib import Path
from PIL import Image,ImageDraw
import imageio_ffmpeg
P=Path(__file__).resolve().parents[1];TASK=P.parents[1]/'Records/Tasks/T-010'
frames=sorted((P/'Previews/Frames').glob('B204_*.png'));assert len(frames)==288
ff=imageio_ffmpeg.get_ffmpeg_exe();video=P/'Previews/B204_hydraulic-proof_v001.mp4'
start=time.perf_counter()
subprocess.run([ff,'-y','-framerate','24','-i',str(P/'Previews/Frames/B204_%04d.png'),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,capture_output=True)
reader=imageio_ffmpeg.read_frames(str(video));meta=next(reader);n=0
for _ in reader:n+=1
assert n==288 and meta['size']==(1280,720) and meta['fps']==24
# Review every rendered schematic frame in ordered contact sheets.
for k in range(4):
    sheet=Image.new('RGB',(1280,720),(32,38,45));d=ImageDraw.Draw(sheet)
    for j,p in enumerate(frames[k*72:(k+1)*72]):
        im=Image.open(p).convert('RGB').crop((150,414,1130,556));im.thumbnail((200,42))
        x=(j%6)*213;y=(j//6)*60;sheet.paste(im,(x,y+15));d.text((x,y),f'F{k*72+j+1:03d}',fill='white')
    sheet.save(TASK/f'Evidence/motion-contact_{k+1:02d}_v001.jpg',quality=93)
manifest=[]
for path in [P/'Scenes/B204_hydraulic-proof_v001.blend',video,*[P/f'Previews/B204_inspect_f{f:03d}_v001.png' for f in (1,49,97,145,193,241,288)]]:
    manifest.append({'path':path.relative_to(P.parents[2]).as_posix(),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'storage':'local-only ignored' if path.suffix in ('.mp4','.blend') else 'selected stills eligible for sync'})
(TASK/'Evidence/output-manifest_v001.json').write_text(json.dumps(manifest,indent=2))
(TASK/'Evidence/encode-qa_v001.json').write_text(json.dumps({'decoded_frames':n,'resolution':meta['size'],'fps':meta['fps'],'duration_seconds':n/meta['fps'],'audio':False,'codec':'h264','pixel_format':'yuv420p','encode_and_decode_seconds':time.perf_counter()-start},indent=2))
print(json.dumps({'decoded_frames':n,'video':str(video)}))
