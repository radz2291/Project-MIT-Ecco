"""Decode complete local demos and save ordered visual review strips."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat

sys.path.insert(0, str(Path.home()/'.cache/codex-b202m-deps'))
import imageio_ffmpeg

def main():
    p=argparse.ArgumentParser()
    p.add_argument('video',type=Path)
    p.add_argument('--name',required=True)
    p.add_argument('--size',type=int,nargs=2,default=[1280,720])
    args=p.parse_args()
    here=Path(__file__).resolve().parent
    target=here/'Evidence/Decoded'
    target.mkdir(parents=True,exist_ok=True)
    reader=imageio_ffmpeg.read_frames(str(args.video),pix_fmt='rgb24')
    meta=next(reader)
    width,height=meta['size']
    frames=[];hashes=[];means=[];stds=[]
    for raw in reader:
        frame=Image.frombytes('RGB',(width,height),raw)
        hashes.append(hashlib.sha256(raw).hexdigest())
        s=ImageStat.Stat(frame);means.append(sum(s.mean)/3);stds.append(sum(s.stddev)/3)
        frames.append(frame.resize((320,180)))
    count=len(frames)
    chosen=sorted(set(round(i*(count-1)/15) for i in range(16))) if count else []
    sheet=Image.new('RGB',(4*320,4*206),(18,20,23));draw=ImageDraw.Draw(sheet)
    for k,idx in enumerate(chosen):
        x=(k%4)*320;y=(k//4)*206
        sheet.paste(frames[idx],(x,y));draw.text((x+8,y+184),f'{idx+1} / {count} - {idx/meta["fps"]:.2f}s',fill=(230,230,230))
    out=target/(args.name+'_chronology_v001.jpg');sheet.save(out,quality=92)
    record={'video':str(args.video.resolve()),'sha256':hashlib.sha256(args.video.read_bytes()).hexdigest(),
            'metadata':meta,'decoded_frames':count,'distinct_decoded_frames':len(set(hashes)),
            'min_mean':min(means) if count else None,'min_stddev':min(stds) if count else None,
            'duration_s':count/meta['fps'],'expected_size':args.size,'dimensions_match':list(meta['size'])==args.size,
            'chronology':str(out.resolve()),'sample_frames':[i+1 for i in chosen],
            'scope':'Full decode and ordered still sampling; viewer comprehension and human acceptance pending'}
    (target/(args.name+'_decode_v001.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in record.items() if k!='metadata'}))
    if count==0 or not record['dimensions_match']:
        raise SystemExit(1)

if __name__=='__main__':
    main()
