import gzip, hashlib, json, re, shutil, struct, subprocess, zipfile
from pathlib import Path
P=Path(__file__).resolve().parent
F=Path(r'C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe')
R=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def ff(*args):
    x=subprocess.run([str(F),'-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,text=True)
    if x.returncode: raise RuntimeError(x.stderr)
    return x
for p in (P/'inspection').glob('*.json'):
    dst=p.with_suffix('.json.gz')
    with p.open('rb') as a,gzip.open(dst,'wb',compresslevel=6) as b: shutil.copyfileobj(a,b)
    h=hashlib.sha256()
    with gzip.open(dst,'rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''): h.update(chunk)
    assert h.hexdigest()==sha(p)
    p.unlink() # Only this job's generated inspection data, preserved losslessly in gzip.
for folder in ['events','appearance','pilot']: (P/folder).mkdir(exist_ok=True)
events=[(0,241),(37,278),(107,348),(117,358),(239,480),(287,528)]
for i,(n,native) in enumerate(events):
    dest=P/'events'/f'{i+1:02d}-f{native}.png'
    ff('-i',P/'motion_reference.mp4','-vf',f'select=eq(n\\,{n})','-frames:v','1','-y',dest)
shutil.copy2(P/'events/01-f241.png',P/'first_frame.png')
shutil.copy2(P/'events/06-f528.png',P/'last_frame.png')
ff('-i',P/'motion_reference.mp4','-vf',"select='eq(n,0)+eq(n,37)+eq(n,107)+eq(n,117)+eq(n,239)+eq(n,287)',scale=480:270,tile=3x2",'-frames:v','1','-y',P/'motion-review.png')
appearance=Path(r'C:/Users/RZ1/Downloads/untitled_Nano Banana 2.1_2026-10-31_13-54-55.png')
shutil.copy2(appearance,P/'appearance/six-shot-look.png')
with appearance.open('rb') as f: w,h=struct.unpack('>II',f.read(24)[16:24])
rects=[]
for i in range(6):
    x0=round((i%3)*w/3);x1=round((i%3+1)*w/3)
    y0=round((i//3)*h/2);y1=round((i//3+1)*h/2)
    ff('-i',appearance,'-vf',f'crop={x1-x0}:{y1-y0}:{x0}:{y0}:exact=1','-frames:v','1','-y',P/'appearance'/f'{i+1:02d}-look.png')
    rects.append([x0,y0,x1,y1])
ff('-i',P/'motion_reference.mp4','-frames:v','120','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-y',P/'pilot/motion_reference-5s.mp4')
ff('-i',P/'pilot/motion_reference-5s.mp4','-vf','select=eq(n\\,119)','-frames:v','1','-y',P/'pilot/last_frame.png')
shutil.copy2(P/'first_frame.png',P/'pilot/first_frame.png')
qa=ff('-i',P/'motion_reference.mp4','-progress','pipe:1','-nostats','-f','null','-').stdout
frames=int(re.findall(r'^frame=(\d+)',qa,re.M)[-1]); micros=int(re.findall(r'^out_time_us=(\d+)',qa,re.M)[-1])
assert frames==288 and micros==12000000,(frames,micros)
src=R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Previews/S01-S02_from-07s_v011.mp4'
assert sha(src)=='849202ae6d1f884753fa6db2674f7468cf6a3879d6b3c023f39ef2733b5e04f9'
manifest={'source_movie':str(src),'source_movie_sha256':sha(src),'source_range':[241,528],'decoded_source_indices':[72,359],'fps':24,'frames':frames,'duration':12,'resolution':[1280,720],'native_video_resolution':[960,540],'retiming':'None; original 24fps inclusive samples','processing':['trim existing complete preview','grayscale conversion','upscale 960x540 to1280x720','H264 re-encode'],'fresh_blender_render':False,'missing_source_dependency':'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend','appearance_source':str(appearance),'appearance_model':'Nano Banana 2.1 per supplied filename; not independently verified','appearance_panel_rectangles':rects,'appearance_crop_note':'Exact native panel crops without stretching; generated sheet proportions are slightly wider than16:9. Node may reframe them.','events':[{'frame':n,'time':i/24,'file':f'events/{j+1:02d}-f{n}.png'} for j,(i,n) in enumerate(events)],'pilot':{'native_frames':[241,360],'duration':5,'retiming':'None; first120frames of full reference','scope':'Opening, camera approach, outgoing pulse and returning echo; no history reveal'},'qa':{'decoded_count':frames,'decoded_duration':micros/1000000,'all_frames_decoded':True,'boundary_images':'Extracted from encoded motion reference','generation_run':False},'hashes':{p.relative_to(P).as_posix():sha(p) for p in P.rglob('*') if p.is_file() and p.suffix in ['.mp4','.png','.gz']}}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print(json.dumps({'frames':frames,'seconds':micros/1000000,'appearance_size':[w,h],'source_unchanged':True}))
