from pathlib import Path
import subprocess,re,json,sys
from PIL import Image,ImageDraw
sys.path.insert(0,r'C:\Users\RZ1\.codex\tmp\ecco-media-runtime')
import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
here=Path(__file__).parent
records=json.loads((here/'Evidence/local-input-inventory_v001.json').read_text())+json.loads((here/'Evidence/external-inputs_v001.json').read_text())
videos=[Path(r['path']) for r in records if r['path'].lower().endswith('.mp4') and Path(r['path']).exists()]
result=[]
for p in videos:
 r=subprocess.run([ff,'-hide_banner','-i',str(p)],capture_output=True,text=True)
 duration=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r.stderr)
 seconds=sum(float(v)*m for v,m in zip(duration.groups(),[3600,60,1])) if duration else None
 result.append(dict(path=str(p),duration_seconds=seconds,video_stream=next((x.strip() for x in r.stderr.splitlines() if 'Video:' in x),None)))
(here/'Evidence/media-probe_v001.json').write_text(json.dumps(result,indent=2))
selected=[r for r in result if any(k in r['path'] for k in ['02-Reference\\client','ECCO_First_Ping_Preview','Final_Playblast','A_Surface','D_Tool'])]
sheet=Image.new('RGB',(900,len(selected)*190),'white');d=ImageDraw.Draw(sheet)
checks=[]
for row,r in enumerate(selected):
 d.text((4,row*190),Path(r['path']).name[:110],fill='black')
 for col,t in enumerate([0.0,r['duration_seconds']*.5,max(0,r['duration_seconds']-.12)]):
  dest=here/'Private'/f'media-{row}-{col}.png'
  proc=subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-ss',str(t),'-i',r['path'],'-frames:v','1','-vf','scale=290:160:force_original_aspect_ratio=decrease',str(dest)],capture_output=True,text=True)
  checks.append(dict(path=r['path'],time=t,decoded=dest.exists(),error=proc.stderr))
  if dest.exists():sheet.paste(Image.open(dest),(col*300,row*190+25))
sheet.save(here/'Private/media-contact_v001.jpg')
(here/'Evidence/media-decode-check_v001.json').write_text(json.dumps(checks,indent=2))
print(len(result),'video headers inspected;',len(checks),'sample decode checks;',all(x['decoded'] for x in checks))
