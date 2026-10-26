"""Decode existing approved movies; assemble labeled comparisons without rendering."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, subprocess, re
R=Path(__file__).resolve().parents[5]; T=R/'04-Production/Records/Tasks/T-049'
FF=R/'04-Production/Mechanisms/B201/Cache/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
P=T/'Images'; P.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',19)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
sources=json.loads((T/'sources.json').read_text())
frames={'S01':[1,145,220],'S02':[180,190,321],'S03':[60,220,390],'S04':[90,216,365],'S05':[50,205,390],'S06':[40,140,260],'S07':[30,90,160]}
versions={'S01':'Gentle 10s','S02':'v011','S03':'v036','S04':'v033 selected','S05':'v020','S06':'polished v004','S07':'v006'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]; media=[]
for s in sources[:7]:
    id=s['id']; video=s['video']
    if id=='S02':video=video.replace('S02_wall-build','S01-S02_from-07s')
    p=R/video
    out=subprocess.run([str(FF),'-v','error','-i',str(p),'-map','0:v:0','-f','framemd5','-'],capture_output=True,text=True)
    if out.returncode or out.stderr.strip():raise RuntimeError(out.stderr)
    lines=[x for x in out.stdout.splitlines() if x and not x.startswith('#')]
    media.append({'id':id,'video':video,'sha256':sha(p),'decoded_frames':len(lines),'decode_errors':0,'native_offset':168 if id=='S02' else 0,'note':'S02 video starts at native frame169; its first72frames reuse approved S01 renders' if id=='S02' else 'Selected complete movie'})
    for ordinal in frames[id]:
        q=P/f'{id}_video-frame-{ordinal:04d}.jpg'
        proc=subprocess.run([str(FF),'-v','error','-i',str(p),'-vf',f'select=eq(n\\,{ordinal-1})','-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True)
        if proc.returncode:raise RuntimeError(proc.stderr)
        import io
        im=Image.open(io.BytesIO(proc.stdout)).convert('RGB'); im.thumbnail((960,540)); im.save(q,quality=93)
        records.append({'id':q.stem,'image':q.relative_to(T).as_posix(),'source':video,'source_sha256':sha(p),'video_frame_1based':ordinal,'native_frame':ordinal+(168 if id=='S02' else 0),'native':s['native'],'title':f'{id} {versions[id]} | native f{ordinal+(168 if id=="S02" else 0)}','sha256':sha(q),'dimensions':list(im.size)})
earlier=[
 ('T44-hardware','04-Production/Records/Tasks/T-044/Previews/Revision_v007/connection_wide_v003.png','BHA','T44 BHA v007 | wide connection inspection'),
 ('T44-world','04-Production/Records/Tasks/T-044/Previews/Revision_v007/Reuse_A_v002.png','WORLD','T44 environment v009 | reuse A'),
 ('T46-send','04-Production/Records/Tasks/T-046/Previews/Review_send_v002.png','SENSING-PROOF','T46 Acoustics v003 | send'),
 ('T46-contact','04-Production/Records/Tasks/T-046/Previews/Review_contact_v002.png','SENSING-PROOF','T46 Acoustics v003 | contact'),
 ('T46-return','04-Production/Records/Tasks/T-046/Previews/Review_return_v002.png','SENSING-PROOF','T46 Acoustics v003 | return'),
 ('T47-layers','04-Production/Records/Tasks/T-047/Previews/v012/CasedLayerSection_f001_v012.png','CASING','T47 CasedHole v002 | layer section f1'),
 ('T47-wear','04-Production/Records/Tasks/T-047/Previews/v012/CasedWearSection_f001_v012.png','CASING','T47 CasedHole v002 | wear section f1'),
 ('T47-support','04-Production/Records/Tasks/T-047/Previews/v012/CasedSupport_f056_v012.png','CASING-PROOF','T47 support v012 | f56'),
 ('T48-flow','04-Production/Records/Tasks/T-048/Previews/Revision_v007/Flow_B_f0048.png','FLOW-PROOF','T48 Hydraulics v003 | reuse B f48')]
for id,p,native_id,title in earlier:
    q=P/f'{id}.jpg';im=Image.open(R/p).convert('RGB');im.thumbnail((960,540));im.save(q,quality=93)
    records.append({'id':id,'image':q.relative_to(T).as_posix(),'source':p,'source_sha256':sha(R/p),'native':next(s['native'] for s in sources if s['id']==native_id),'title':title,'sha256':sha(q),'dimensions':list(im.size),'correspondence':'Existing selected still, provenance from T44/T46/T47/T48 reports/manifests. No new render. Layer/wear inspection natives identified in image-index.'})
exact_views={
 'T44-hardware':'04-Production/Records/Tasks/T-044/Revision_v007/Scenes/connection_wide_v003.blend',
 'T44-world':'04-Production/Records/Tasks/T-044/Revision_v007/Scenes/Reuse_A_continuity_v002.blend',
 'T47-layers':'04-Production/Records/Tasks/T-047/Scenes/CasedLayerSection_v011.blend',
 'T47-wear':'04-Production/Records/Tasks/T-047/Scenes/CasedWearSection_v011.blend'}
for r in records:
    if r['id'] in exact_views:r['native']=exact_views[r['id']]
def sheet(name,rows):
    w,h=480,318;out=Image.new('RGB',(w*3,h*len(rows)),(17,23,30));draw=ImageDraw.Draw(out)
    for row,ids in enumerate(rows):
        for col,id in enumerate(ids):
            r=next(r for r in records if r['id']==id);im=Image.open(T/r['image']);im.thumbnail((480,270));x=col*w;y=row*h;out.paste(im,(x,y));draw.text((x+10,y+276),r['title'],fill=(227,237,242),font=small)
    out.save(P/name,quality=93)
sheet('01-seven-section-baseline.jpg',[[f'{id}_video-frame-{n:04d}' for n in frames[id]] for id in frames])
sheet('02-hardware-and-world.jpg',[['T44-hardware','S01_video-frame-0220','S07_video-frame-0160'],['T44-world','S03_video-frame-0220','S05_video-frame-0205']])
sheet('03-sensing-and-casing.jpg',[['T46-send','T46-contact','T46-return'],['S02_video-frame-0180','S02_video-frame-0190','S02_video-frame-0321'],['T47-layers','S04_video-frame-0216','T47-wear'],['T47-support','S04_video-frame-0090','S04_video-frame-0365']])
sheet('04-flow-and-data.jpg',[['T48-flow','S05_video-frame-0050','S05_video-frame-0390'],['S03_video-frame-0390','S06_video-frame-0140','S06_video-frame-0260']])
(T/'Evidence/image-manifest.json').write_text(json.dumps(records,indent=2))
(T/'Evidence/media-audit.json').write_text(json.dumps(media,indent=2))
print(json.dumps(media,indent=2));print('IMAGES',len(records))
